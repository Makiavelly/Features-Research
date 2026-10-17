"""Compile LLM-authored SQL feature programs over time-filtered H&M history.

Only scalar/aggregate expressions are accepted, never executable Python or SQL
statements. Joins, labels, temporal boundaries and row order belong to the host.
"""
import hashlib
import json
import os
from pathlib import Path
import re

import duckdb
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
ITEM_COLUMNS = ["product_code", "product_type_no", "graphical_appearance_no",
                "colour_group_code", "perceived_colour_value_id", "perceived_colour_master_id",
                "department_no", "index_group_no", "section_no", "garment_group_no"]
USER_COLUMNS = ["age", "FN", "Active", "club_member_status", "fashion_news_frequency"]
GROUP_COLUMNS = ["customer_id", "article_id", *ITEM_COLUMNS]
FUNCTIONS = {"count", "sum", "avg", "min", "max", "stddev_pop", "stddev_samp",
             "variance", "median", "quantile_cont", "approx_count_distinct", "mode",
             "coalesce", "nullif", "abs", "sqrt", "ln", "log", "log2", "log10", "exp",
             "pow", "power", "greatest", "least", "round", "floor", "ceil", "cast",
             "filter", "in", "not", "where", "when", "then", "else", "and", "or"}
FORBIDDEN = re.compile(r"\b(select|from|join|union|with|over|attach|detach|copy|pragma|install|load|"
                       r"create|drop|alter|insert|update|delete|read_csv|read_parquet|query|"
                       r"customer_id|article_id|rid|label|target|timestamp|t_dat)\b", re.I)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def validate_expression(expression, aggregate=False):
    if not isinstance(expression, str) or len(expression) > 1000:
        raise ValueError("SQL expression must be a string of <=1000 characters")
    if any(part in expression for part in [";", "--", "/*", "*/", "'", '"', "\\", "."]):
        # Decimal literals are permitted, qualified identifiers and strings are not.
        stripped = re.sub(r"\b\d+\.\d+\b", "0", expression)
        if any(part in stripped for part in [";", "--", "/*", "*/", "'", '"', "\\", "."]):
            raise ValueError("Only numeric SQL expressions, no statements/strings/qualified names")
    checked_expression = expression
    if aggregate:
        checked_expression = re.sub(
            r"\b(?:count\s*\(\s*(?:distinct\s+)?|approx_count_distinct\s*\(\s*)(?:customer_id|article_id)\s*\)",
            "count(*)", checked_expression, flags=re.I)
    forbidden = FORBIDDEN.search(checked_expression)
    if forbidden:
        raise ValueError(f"Forbidden token {forbidden.group(0)!r}: IDs only in grouping keys/counts; no SQL statements, window functions, or labels")
    function_expression = expression
    if os.environ.get("LLMFE_VALIDATOR_VERSION") == "h002":
        # WITHIN GROUP (...) is SQL syntax, not a call to a function GROUP.
        function_expression = re.sub(r"\bWITHIN\s+GROUP\s*\(", "(", expression, flags=re.I)
    for function in re.findall(r"\b([a-zA-Z_][a-zA-Z_0-9]*)\s*\(", function_expression):
        if function.lower() not in FUNCTIONS:
            raise ValueError(f"Function outside allowlist: {function}")
    return expression


def validate_program(program):
    if set(program) - {"rationale", "aggregates", "derived"}:
        raise ValueError("Unknown program keys")
    aggs, derived = program.get("aggregates", []), program.get("derived", [])
    if not isinstance(aggs, list) or not isinstance(derived, list) or len(aggs) > 24 or len(derived) > 12:
        raise ValueError("Maximum 24 aggregates and 12 derived features")
    names = set()
    for entry in aggs + derived:
        if set(entry) - {"name", "keys", "sql"}:
            raise ValueError("Unknown feature keys")
        name = entry["name"]
        if not re.fullmatch(r"f_[a-z][a-z0-9_]{0,45}", name) or name in names:
            raise ValueError("Feature names must be unique f_lowercase_names")
        names.add(name)
        validate_expression(entry["sql"], aggregate=entry in aggs)
    for entry in aggs:
        keys = entry["keys"]
        if (not isinstance(keys, list) or not keys or len(keys) > 2 or len(set(keys)) != len(keys)
                or any(key not in GROUP_COLUMNS for key in keys)):
            raise ValueError("Invalid grouping keys")
        if "customer_id" not in keys and len(keys) != 1:
            raise ValueError("Use one article/category key, customer_id, or customer_id + article/category")
    return program


class FeatureEngine:
    def __init__(self, scratch, data_dir=None):
        self.scratch = Path(scratch)
        self.scratch.mkdir(parents=True, exist_ok=True)
        self.data_dir = Path(data_dir or ROOT / "data/rel-hm/db")
        self.con = duckdb.connect()
        self.con.execute("SET threads=2")
        self.con.execute("SET memory_limit='2300MB'")
        spill = str(self.scratch / "spill").replace("'", "''")
        self.con.execute(f"SET temp_directory='{spill}'")
        self.con.execute("SET max_temp_directory_size='6GB'")
        self.items = pd.read_parquet(self.data_dir / "article.parquet", columns=["article_id", *ITEM_COLUMNS])
        self.users = pd.read_parquet(self.data_dir / "customer.parquet", columns=["customer_id", *USER_COLUMNS])
        self.category_maps = {}
        for column in ITEM_COLUMNS:
            encoded, categories = pd.factorize(self.items[column], sort=True)
            self.category_maps[column] = categories.tolist()
            self.items[column] = encoded.astype(np.int32)
        for column in ["club_member_status", "fashion_news_frequency"]:
            values = self.users[column].astype("category")
            self.category_maps[column] = list(values.cat.categories.astype(str))
            self.users[column] = values.cat.codes.astype(np.float32)
        # This is raw categorical encoding, not historical manual features.
        for name, frame in [("articles", self.items), ("customers", self.users)]:
            self.con.register("input_frame", frame)
            self.con.execute(f"CREATE TABLE {name} AS SELECT * FROM input_frame")
            self.con.unregister("input_frame")
        raw_path = str(self.data_dir / "transactions.parquet").replace("'", "''")
        self.con.execute(f"CREATE TABLE tx AS SELECT * FROM read_parquet('{raw_path}')")
        self.raw_names = [f"raw_u_{col.lower()}" for col in USER_COLUMNS] + [f"raw_i_{col}" for col in ITEM_COLUMNS]
        self.program = None

    def prepare(self, timestamp, users, program):
        self.program = validate_program(program)
        wanted = pd.DataFrame({"customer_id": np.unique(np.asarray(users, dtype=np.int64))})
        self.con.register("wanted_input", wanted)
        self.con.execute("CREATE OR REPLACE TEMP TABLE wanted AS SELECT * FROM wanted_input")
        self.con.unregister("wanted_input")
        cutoff = pd.Timestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        self.con.execute(f"""CREATE OR REPLACE TEMP VIEW history AS
            SELECT t.customer_id,t.article_id,t.price,t.sales_channel_id,
            date_diff('day',t.t_dat,TIMESTAMP '{cutoff}')::INTEGER AS days_ago,
            a.* EXCLUDE(article_id), c.age AS customer_age
            FROM tx t LEFT JOIN articles a USING(article_id)
            LEFT JOIN customers c USING(customer_id)
            WHERE t.t_dat <= TIMESTAMP '{cutoff}'""")
        groups = {}
        for entry in program.get("aggregates", []):
            groups.setdefault(tuple(entry["keys"]), []).append(entry)
        self.groups = []
        for index, (keys, entries) in enumerate(groups.items()):
            table = f"aggregate_{index}"
            feature_sql = ",".join(f"{entry['sql']} AS {entry['name']}" for entry in entries)
            source = "history JOIN wanted USING(customer_id)" if "customer_id" in keys else "history"
            columns = ",".join(keys)
            self.con.execute(f"CREATE OR REPLACE TEMP TABLE {table} AS SELECT {columns},{feature_sql} FROM {source} GROUP BY {columns}")
            self.groups.append((table, keys, entries))

    @property
    def feature_names(self):
        return self.raw_names + [entry["name"] for entry in self.program.get("aggregates", [])] + [entry["name"] for entry in self.program.get("derived", [])]

    def frame(self, pairs):
        # The feature SQL never receives labels, target lists or arbitrary files.
        inputs = pairs[["customer_id", "article_id"]].copy().reset_index(drop=True)
        inputs.insert(0, "rid", np.arange(len(inputs), dtype=np.int64))
        self.con.register("input_pairs", inputs)
        raw = [f'c."{col}" AS raw_u_{col.lower()}' for col in USER_COLUMNS]
        raw += [f"a.{col} AS raw_i_{col}" for col in ITEM_COLUMNS]
        joins, aggregate_select = [], []
        for table, keys, entries in self.groups:
            conditions = []
            for key in keys:
                owner = "p" if key in ["customer_id", "article_id"] else "a"
                conditions.append(f"{table}.{key}={owner}.{key}")
            joins.append(f"LEFT JOIN {table} ON {' AND '.join(conditions)}")
            aggregate_select.extend(f"{table}.{entry['name']} AS {entry['name']}" for entry in entries)
        select = ",".join(["p.rid", *raw, *aggregate_select])
        query = f"SELECT {select} FROM input_pairs p LEFT JOIN customers c USING(customer_id) LEFT JOIN articles a USING(article_id) {' '.join(joins)}"
        # Derived expressions see only raw/aggregate feature columns. Each stage
        # may reference earlier derived features, but cannot access row IDs.
        for entry in self.program.get("derived", []):
            query = f"SELECT *, {entry['sql']} AS {entry['name']} FROM ({query})"
        ordered = ",".join(self.feature_names)
        try:
            frame = self.con.sql(f"SELECT {ordered} FROM ({query}) ORDER BY rid").df()
        finally:
            self.con.unregister("input_pairs")
        if len(frame) != len(inputs) or list(frame) != self.feature_names:
            raise RuntimeError("Feature rows/schema changed")
        for column in frame:
            if not pd.api.types.is_numeric_dtype(frame[column]):
                raise ValueError(f"Non-numeric feature: {column}")
        return frame

    def matrix(self, pairs):
        values = self.frame(pairs).to_numpy(dtype=np.float32)
        return np.nan_to_num(values, nan=-1., posinf=-1., neginf=-1.)

    def close(self):
        self.con.close()
