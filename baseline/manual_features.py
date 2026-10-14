"""Hand-written, time-safe SQL aggregates inspired by RelBench's expert study."""
import json
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_CODES = ["product_type_no", "graphical_appearance_no", "colour_group_code",
                 "perceived_colour_master_id", "department_no", "section_no", "garment_group_no"]


def sql_path(path):
    return "'" + str(path).replace("'", "''") + "'"


class ManualFeatures:
    def __init__(self, data_dir=None, cache_dir=None, memory_limit="768MB"):
        self.data_dir = Path(data_dir or ROOT / "data/rel-hm/db")
        self.cache_dir = Path(cache_dir or ROOT / "baseline/cache/manual_v1")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect()
        self.con.execute(f"SET memory_limit='{memory_limit}'")
        self.con.execute("SET threads=2")
        self.con.execute(f"SET temp_directory={sql_path(self.cache_dir / 'spill')}")
        self.con.execute(f"CREATE VIEW tx AS SELECT *, file_row_number AS txn_idx FROM read_parquet({sql_path(self.data_dir / 'transactions.parquet')}, file_row_number=true)")
        article = pd.read_parquet(self.data_dir / "article.parquet", columns=["article_id", *ARTICLE_CODES])
        customer = pd.read_parquet(self.data_dir / "customer.parquet", columns=["customer_id", "age", "FN", "Active", "club_member_status", "fashion_news_frequency"])
        customer["fn_not_null"] = customer.FN.notna().astype(np.int8)
        customer["is_active"] = customer.Active.notna().astype(np.int8)
        customer = customer.drop(columns=["FN", "Active"])
        self.category_maps = {}
        for column in ["club_member_status", "fashion_news_frequency"]:
            categorical = customer[column].astype("category")
            self.category_maps[column] = list(categorical.cat.categories.astype(str))
            customer[column] = categorical.cat.codes.astype(np.int16)
        self.con.register("article_frame", article)
        self.con.register("customer_frame", customer)
        self.con.execute("CREATE TABLE articles AS SELECT * FROM article_frame")
        self.con.execute("CREATE TABLE customers AS SELECT * FROM customer_frame")
        self.con.unregister("article_frame")
        self.con.unregister("customer_frame")
        self.feature_names = None
        self.categorical_names = None

    def prepare(self, timestamp, users):
        self.timestamp = pd.Timestamp(timestamp)
        self.cutoff = f"TIMESTAMP '{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}'"
        wanted = pd.DataFrame({"customer_id": np.unique(np.asarray(users, dtype=np.int64))})
        self.con.register("wanted_frame", wanted)
        self.con.execute("CREATE OR REPLACE TEMP TABLE wanted AS SELECT * FROM wanted_frame")
        self.con.unregister("wanted_frame")
        cutoff = self.cutoff
        self.con.execute(f"""CREATE OR REPLACE TEMP TABLE hist AS
            SELECT t.*, a.department_no, a.section_no, a.perceived_colour_master_id,
                   a.product_type_no, c.age
            FROM tx t JOIN wanted w USING (customer_id)
            LEFT JOIN articles a USING (article_id) LEFT JOIN customers c USING (customer_id)
            WHERE t.t_dat <= {cutoff}""")
        user_aggs = ["count(*) AS u_count_all", "sum(price) AS u_amount_all", "avg(price) AS u_price_all",
                     "count(DISTINCT article_id) AS u_unique_all", "avg(sales_channel_id - 1) AS u_channel2_all",
                     f"date_diff('day', max(t_dat), {cutoff}) AS u_recency_days",
                     "mode(department_no) AS u_mode_department_all", "mode(section_no) AS u_mode_section_all",
                     "mode(perceived_colour_master_id) AS u_mode_colour_all"]
        item_aggs = []
        for week in range(1, 6):
            mask = f"t_dat > {cutoff} - INTERVAL '{week * 7} days' AND t_dat <= {cutoff} - INTERVAL '{(week-1)*7} days'"
            for expression, label in [("count(*)", "count"), ("sum(price)", "amount"), ("avg(price)", "price"),
                                       ("count(DISTINCT article_id)", "unique"), ("avg(sales_channel_id - 1)", "channel2"),
                                       ("mode(department_no)", "mode_department"), ("mode(section_no)", "mode_section"),
                                       ("mode(perceived_colour_master_id)", "mode_colour")]:
                user_aggs.append(f"{expression} FILTER (WHERE {mask}) AS u_{label}_week{week}")
            for expression, label in [("count(*)", "count"), ("sum(price)", "amount"), ("avg(price)", "price"),
                                       ("count(DISTINCT customer_id)", "unique_buyers"), ("avg(age)", "buyer_age")]:
                item_aggs.append(f"{expression} FILTER (WHERE {mask}) AS i_{label}_week{week}")
        user_aggs.append(f"count(*) FILTER (WHERE t_dat > {cutoff} - INTERVAL '28 days') AS u_count_28d")
        self.con.execute(f"CREATE OR REPLACE TEMP TABLE uf AS SELECT customer_id, {', '.join(user_aggs)} FROM hist GROUP BY customer_id")
        self.con.execute(f"""CREATE OR REPLACE TEMP TABLE it AS SELECT article_id,
            count(*) AS i_count_all, sum(price) AS i_amount_all, avg(price) AS i_price_all,
            date_diff('day', max(t_dat), {cutoff}) AS i_recency_days
            FROM tx WHERE t_dat <= {cutoff} GROUP BY article_id""")
        self.con.execute(f"""CREATE OR REPLACE TEMP TABLE iw AS SELECT article_id, {', '.join(item_aggs)}
            FROM tx LEFT JOIN customers USING (customer_id)
            WHERE t_dat <= {cutoff} AND t_dat > {cutoff} - INTERVAL '35 days' GROUP BY article_id""")
        self.con.execute(f"""CREATE OR REPLACE TEMP TABLE pf AS SELECT customer_id, article_id,
            count(*) AS p_count_all, avg(price) AS p_price_all,
            count(*) FILTER (WHERE t_dat > {cutoff} - INTERVAL '7 days') AS p_count_7d,
            count(*) FILTER (WHERE t_dat > {cutoff} - INTERVAL '28 days') AS p_count_28d,
            date_diff('day', max(t_dat), {cutoff}) AS p_recency_days
            FROM hist GROUP BY customer_id, article_id""")
        for name, column in [("dept", "department_no"), ("section", "section_no"), ("colour", "perceived_colour_master_id"), ("type", "product_type_no")]:
            self.con.execute(f"""CREATE OR REPLACE TEMP TABLE affinity_{name} AS
                SELECT customer_id, {column}, count(*) AS a_{name}_count_28d
                FROM hist WHERE t_dat > {cutoff} - INTERVAL '28 days' GROUP BY customer_id, {column}""")

    def history_candidates(self):
        return self.con.sql("""SELECT customer_id, list(DISTINCT article_id) AS candidates FROM
            (SELECT customer_id, article_id, row_number() OVER (PARTITION BY customer_id ORDER BY t_dat DESC, txn_idx DESC) AS r FROM hist)
            WHERE r <= 128 GROUP BY customer_id""").df()

    def query(self):
        cutoff = self.cutoff
        static = ["c.age AS u_age", "c.fn_not_null AS u_fn_not_null", "c.is_active AS u_is_active",
                  "c.club_member_status AS u_club_member_status", "c.fashion_news_frequency AS u_fashion_news_frequency"]
        static.extend(f"a.{column} AS i_{column}" for column in ARTICLE_CODES)
        joins, affinity = [], []
        for name, column in [("dept", "department_no"), ("section", "section_no"), ("colour", "perceived_colour_master_id"), ("type", "product_type_no")]:
            joins.append(f"LEFT JOIN affinity_{name} ad_{name} ON p.customer_id=ad_{name}.customer_id AND a.{column}=ad_{name}.{column}")
            affinity += [f"ad_{name}.a_{name}_count_28d", f"ad_{name}.a_{name}_count_28d / NULLIF(uf.u_count_28d, 0) AS a_{name}_share_28d"]
        matches = []
        for label, column in [("department", "department_no"), ("section", "section_no"), ("colour", "perceived_colour_master_id")]:
            matches.append(f"CAST(uf.u_mode_{label}_all = a.{column} AS INTEGER) AS match_{label}_all")
            matches.extend(f"CAST(uf.u_mode_{label}_week{w} = a.{column} AS INTEGER) AS match_{label}_week{w}" for w in range(1, 6))
        return f"""SELECT p.*, {', '.join(static)}, uf.* EXCLUDE(customer_id),
            it.* EXCLUDE(article_id), iw.* EXCLUDE(article_id), pf.* EXCLUDE(customer_id, article_id),
            {', '.join(affinity + matches)},
            it.i_price_all - uf.u_price_all AS price_gap,
            it.i_price_all / NULLIF(uf.u_price_all, 0) AS price_ratio,
            date_part('week', {cutoff}) AS week_of_year,
            date_part('month', {cutoff}) AS month_of_year
            FROM input_pairs p LEFT JOIN customers c USING(customer_id)
            LEFT JOIN articles a USING(article_id) LEFT JOIN uf USING(customer_id)
            LEFT JOIN it USING(article_id) LEFT JOIN iw USING(article_id)
            LEFT JOIN pf USING(customer_id, article_id) {' '.join(joins)}"""

    def frame(self, pairs):
        self.con.register("input_pairs", pairs)
        result = self.con.sql(self.query()).df()
        self.con.unregister("input_pairs")
        self._set_schema(list(result.columns))
        return result

    def _set_schema(self, columns):
        names = [c for c in columns if c not in ["customer_id", "article_id", "timestamp", "label"]]
        if self.feature_names is not None and names != self.feature_names:
            raise RuntimeError("Feature schema changed across timestamps")
        self.feature_names = names
        self.categorical_names = [c for c in names if c.startswith("u_mode_") or c in
                                  ["u_club_member_status", "u_fashion_news_frequency", *[f"i_{x}" for x in ARTICLE_CODES]]]

    def write(self, pairs, destination):
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        pairs = pairs.copy()
        pairs["timestamp"] = self.timestamp
        self.con.register("input_pairs", pairs)
        query = self.query()
        columns = self.con.sql(query).columns
        self._set_schema(columns)
        casts = [f'CAST("{c}" AS FLOAT) AS "{c}"' if c in self.feature_names else f'"{c}"' for c in columns]
        self.con.execute(f"COPY (SELECT {', '.join(casts)} FROM ({query})) TO {sql_path(destination)} (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 50000)")
        self.con.unregister("input_pairs")

    def save_schema(self, destination):
        Path(destination).write_text(json.dumps({"features": self.feature_names, "categorical_features": self.categorical_names,
            "customer_category_maps": self.category_maps, "cutoff": "transactions.t_dat <= prediction timestamp",
            "expert_sources": ["baseline/expert_upstream/hm/user-churn/feats.sql", "baseline/expert_upstream/hm/item-sales/feats.sql"],
            "adaptation": "Subset of expert user/item aggregate ideas; manually added pair counts, recency, category affinities and matches. No learned features or test targets."}, indent=2))

    def close(self):
        self.con.close()
