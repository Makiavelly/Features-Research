def source_from_response(text):
    code=normalize(text)
    check_program(code)
    return code


def prompt(data,memory,seed):
    dataset=Data(data)
    pairs=pd.read_parquet(Path(data)/'train_pairs.parquet')
    examples=pairs[pairs.timestamp==pairs.timestamp.max()].sample(5,random_state=42)
    X=dataset.inputs(examples)
    demos=choose_demonstrations(memory,np.random.default_rng(seed))
    prior=[{'search_MAP_fraction':t['score'],'program':(Path(t['directory'])/'program.py').read_text()} for t in demos]
    return '''You are a data scientist creating useful features for H&M clothing recommendations.
Task: rank each customer's fixed candidate articles for purchases in the next7 days. Maximize validation MAP@12.
Complete ONE Python function: def modify_features(X): return a numeric pandas DataFrame.
X is already a prepared flat numeric table: one row per customer-article pair. No history joins needed.
pd (pandas) and np (numpy) are supplied; no other libraries, files, network or fitting.
Use the existing columns below to create meaningful interactions, ratios, recency/popularity transforms,
and affinities between customer preferences and candidate attributes. Use domain knowledge.
Start from X.copy(), prefer preserving informative columns; you may drop less useful columns as in the examples.
Return a DataFrame with exactly X.index and row order. Numeric output1-78 columns, same schema for every call.
Use vectorized ROWWISE operations only. No groupby, merge, joins, windows, random, ranking across rows,
or dataset statistics such as column.mean(). No learning from the current batch. Missing values are allowed.
Your function is applied in separate chunks and must give identical results regardless of other rows.
For ratios, handle zero denominators; np.log1p on nonnegative counts is supported.
Keep the entire function compact, ideally2-6 new transformations, one short docstring, under2048 output tokens.
Return ONLY the complete function in a python code block; do not generate several versions or explanations.

Column meanings (all supplied by host, NOT invented by Llama):
raw_u_age: customer age. raw_u_fn/raw_u_active: account flags.
raw_u_club_member_status/raw_u_fashion_news_frequency: category codes.
raw_i_*: encoded clothing product/type, graphic, colour, department, index, section, garment categories.
Category codes are identifiers, not continuous measurements; avoid arbitrary arithmetic on them.
h_user_count_7/30/180 and h_article_count_7/30/180: past purchase counts in those calendar-day windows.
h_user_recency/h_article_recency: days since most recent purchase in past180 days.
h_user_price_mean/h_article_price_mean: average normalized past price in past180 days.
h_user_type_count_30/180: customer's purchases of candidate's product_type_no in those windows.
h_user_article_count/h_user_article_recency: past180-day count/recency for this exact customer-article.
h_user_colour_count: customer's past180-day purchases of candidate's colour group.
Missing aggregates mean no matching history; counts may be filled with0 but missing recency is NOT recent.
History is restricted to selected customer cohort and180 days before each cutoff, not population-wide sales.
Only30 base columns exist. Do not invent other history fields, IDs, timestamps, labels or prices of future purchases.
The host scores all803377 supervised training pairs with CPU LightGBM150 rounds/31 leaves, seed42.
Search uses fixed256 validation users and6594 candidates. Test is unavailable during selection.
Previously measured complete transformations include a real working seeded example.
'''+json.dumps({'available_columns':list(X),'five_training_examples':X.to_dict('records'),
               'working_host_seed_example':SEED,
               'previous_programs':prior},separators=(',',':'),default=str)


def repair_prompt(base,parent,error):
    return (base+'\nFix the previous program. Return ONE COMPLETE corrected function, not a patch.\n'
            +'Previous response:\n'+parent+'\nRejection:\n'+error[-3000:]
            +'\nUse only the listed flat columns. No history/groupby/joins. Preserve row index and schema. '
            +'If duplicate choose different useful transformations. Keep code short.')
