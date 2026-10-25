"""Python interface with schema, a working seed and prior validation fitness."""
from python_features import HISTORY,render

INSTRUCTION = '''Write a COMPLETE Python feature-engineering program for H&M recommendations.
Return only Python source defining def modify_features(X, history). No SQL/JSON/prose.
Goal: find useful features from purchase history AND customer/article attributes to predict
purchases in the NEXT 7 days and maximize LightGBM validation MAP@12, not training loss.
You may use pandas as pd and numpy as np (already provided, optional imports).
Ordinary vectorized pandas/NumPy, groupby/agg/transform/merge/map, formulas and helper functions
are supported, including literal module constants. No file/network I/O, external libraries,
randomness, eval/query, decorators or private attributes.
Do not train a model; the host trains the same LightGBM for every proposed complete feature set.

X: candidate customer_id,article_id and 15 numeric encoded raw fields:
raw_u_age,raw_u_fn,raw_u_active,raw_u_club_member_status,raw_u_fashion_news_frequency,
raw_i_product_code,raw_i_product_type_no,raw_i_graphical_appearance_no,raw_i_colour_group_code,
raw_i_perceived_colour_value_id,raw_i_perceived_colour_master_id,raw_i_department_no,
raw_i_index_group_no,raw_i_section_no,raw_i_garment_group_no.
history: only purchases at/before current cutoff for the frozen 5000-customer cohort.
History columns: COLUMNS.
days_ago>=0, price is normalized transaction price, sales_channel_id=1/2.
History clothing columns describe the purchased article, using the same category codes as raw_i_*.
No raw_* columns in history. No labels, timestamps, test targets or future rows in either input.
All available past history is supplied, use days_ago to restrict windows. Recency=min(days_ago).
The cohort is not the full H&M population. Purchases are not views; spending is not discount.

Return a pandas DataFrame with EXACTLY X.index and X row order, 1..36 unique numeric
f_lowercase features ONLY (not IDs/raw columns). Host appends the same 15 raw fields.
Missing values are allowed; host maps missing/infinite to -1 as in all previous experiments.
Schema/order must be fixed across cutoffs, empty history, absent groups and batch sizes.
Compute population statistics from history, not the changing candidate batch X.
Avoid per-row loops and huge pivots: the function is called on up to 80000 candidate rows.
Limit 60 seconds per call. Start compact, about 6..12 informative new features.
For merges preserve row order/index. Ratios should handle zero/missing denominators.

WORKING INITIAL EXAMPLE (improve/change the COMPLETE feature set):
def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    recent = history.loc[history['days_ago'] <= 30]
    counts = recent.groupby('article_id').size()
    out['f_item_count_30d'] = X['article_id'].map(counts).fillna(0)
    recency = history.groupby('customer_id')['days_ago'].min()
    out['f_customer_recency'] = X['customer_id'].map(recency)
    return out
'''.replace('COLUMNS',', '.join(HISTORY))


def make_prompt(data,best,previous,config):
    prompt = INSTRUCTION + f'''\nFIXED: {config['train_pairs']} unchanged pairs/4804 user-times/8cutoffs.
LightGBM150rounds/31leaves/4CPU. Search128 users x all5000items.
Top3search + raw compete on disjoint confirmation88; heldout88/test250 never select programs.
Entire output <=2048tokens. Previous best complete Python in YOUR island,
search MAP fraction={best['score']}:\n''' + render(best['program'])
    prompt += '\nThree static training candidate examples (no labels):\n'+config['training_examples']
    if previous:
        prompt += '\nREPAIR: Return the COMPLETE corrected Python. Fix all errors; no prose.\nPrevious response:\n'+previous['text']
        prompt += '\nRejection diagnostics:\n'+previous['error']
        prompt += '\nFor duplicates change useful statistics/windows/groupings/formulas, not just names.'
    return prompt
