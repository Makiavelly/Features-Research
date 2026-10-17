"""The model returns complete SQL statements, not the former JSON DSL."""
from full_sql import HISTORY, render

INSTRUCTION = '''Write a COMPLETE DuckDB SQL feature-engineering script for H&M recommendations.
Return ONLY SQL, no JSON/Python/prose. Separate complete SELECT statements with semicolons.
WITH ... SELECT CTEs are welcome. Each query is independent: it can see ONLY history and its own CTEs.
Do not CREATE tables/views: the host executes your SELECTs and handles final candidate joins.
Predict purchases in the NEXT7days; fitness is LightGBM validation MAP@12, not training loss.

history contains only purchases at/before cutoff, from the frozen5000-customer cohort, not full H&M.
Columns: {columns}.
price=normalized purchase price; days_ago=days before cutoff; sales_channel_id=1/2.
The clothing-category columns describe the PURCHASED article; customer_age is numeric age.
There is no gender, raw_*, timestamp, t_dat, label, target, or future data table in this database.
All historical rows are available; time windows use WHERE/FILTER on days_ago.

Each SELECT returns join keys and numeric features named f_lowercase_name.
Supported final keys: customer_id; article_id; ONE clothing category; customer_id+article_id;
or customer_id+ONE clothing category. Return EXACTLY ONE ROW per chosen key combination.
Preserve key names/values. No sales_channel_id/price/age/days_ago join keys. Do not output IDs as features.
All f_* output names must be unique across all queries. At most6 SELECTs and36 output features total.
Start compact, about2-3queries and6-10features. Return a complete set, not a patch.
Intermediate CTE columns may have descriptive names. Ratios/transformations belong in your SELECTs.
The host appends the SAME15 raw customer/article fields as previous experiments automatically.
Only past history goes into your SQL; no labels, candidate rows, other files, tables, or external functions.
Common numeric SQL: count/sum/avg/min/max/stddev_pop/median/quantile_cont, approx_count_distinct,
mode, coalesce/nullif, abs/sqrt/ln/log/power, greatest/least, round/floor/ceil, cast, CASE WHEN.
For age bins return numbers0/1/2, not strings. Use nullif(denominator,0) for ratios.
Quantile syntax: quantile_cont(price,0.5). Mode: mode(customer_age ORDER BY customer_age).
SELECT aliases, CTEs, joins within history-derived CTEs, and numeric window functions are allowed.
Window outputs still must yield one row per final key. Use deterministic ordering, not random().
History is purchases, not views; sum(price) is spending, not discount; recent recency=min(days_ago).

SYNTAX EXAMPLES ONLY, choose your own complete useful feature set:
WITH counts AS (
  SELECT customer_id, count(*) AS total_count,
         count(*) FILTER(WHERE days_ago<=7) AS recent_count
  FROM history GROUP BY customer_id
)
SELECT customer_id, total_count AS f_total_count, recent_count AS f_recent_count,
       recent_count/nullif(total_count,0) AS f_recent_share FROM counts;

SELECT article_id, count(*) FILTER(WHERE days_ago<=7) AS f_item_recent_count,
       avg(price) AS f_item_mean_price FROM history GROUP BY article_id;
'''.replace('{columns}', ', '.join(HISTORY))


def make_prompt(data,best,previous,config):
    prompt=INSTRUCTION+f'''
FIXED COMPARISON: {config['train_pairs']} unchanged training pairs/4804 user-times/8 snapshots.
LightGBM150rounds/31leaves/4threads. Search128users × ALL5000items.
Top3search+raw compete on disjoint confirmation88. Heldout88/test250 not used for selection.
Entire response <=2048tokens. Previous best complete SQL in YOUR island,
search MAP fraction={best['score']}:
'''+render(best['program'])
    # These examples are static fields from an early training snapshot, not labels.
    prompt+='\nRaw training candidate examples (appended by HOST, unavailable inside history SQL):\n'+config['training_examples']
    if previous:
        prompt+='\nREPAIR: Return the COMPLETE corrected SQL script; fix all listed queries.\nPrevious SQL response:\n'+previous['text']
        prompt+='\nRejection diagnostics:\n'+previous['error']
        prompt+='\nFor duplicates change statistics/windows/groupings, not just feature/CTE names. No JSON.'
    return prompt
