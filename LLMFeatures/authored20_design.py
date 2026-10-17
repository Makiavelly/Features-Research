"""Feature implementation and unmeasured idea sketches from the Codex session.

No provider calls or random feature search. Only separately committed adaptive
proposals are evaluated. Initial sketches were never trained or scored.
"""
import json

KEYS = {
    'u':['customer_id'], 'i':['article_id'], 'p':['customer_id','article_id'],
    't':['product_type_no'], 's':['section_no'], 'd':['department_no'],
    'c':['colour_group_code'], 'v':['perceived_colour_value_id'],
    'a':['graphical_appearance_no'], 'g':['garment_group_no'], 'pc':['product_code'],
}
for prefix in ['t','s','d','c','v','a','g','pc']:
    KEYS['u'+prefix]=['customer_id',KEYS[prefix][0]]

SPECS = {}
for prefix,keys in KEYS.items():
    for days in [0,7,14,30,90,365]:
        SPECS[f'{prefix}_n{days}']=(keys,'n',days)
    for operation in ['r','price','std','q25','q75','age','ch2','dec14','dec30','uniq']:
        SPECS[f'{prefix}_{operation}']=(keys,operation,0)

# Explicit formulas. Each name expands only to its listed fixed dependencies.
DERIVED = {
    'i_trend7':('ratio','i_n7','i_n30',3),
    'i_trend14':('ratio','i_n14','i_n90',5),
    'i_trend30':('ratio','i_n30','i_n365',5),
    'u_trend7':('ratio','u_n7','u_n30',3),
    'u_trend30':('ratio','u_n30','u_n365',5),
    't_trend7':('ratio','t_n7','t_n30',5),
    's_trend7':('ratio','s_n7','s_n30',5),
    'pc_trend7':('ratio','pc_n7','pc_n30',3),
    'pair_share':('ratio','p_n0','u_n0',1),
    'user_diversity':('ratio','u_uniq','u_n0',1),
    'item_buyer_share':('ratio','i_uniq','i_n0',1),
    'price_gap':('gap','i_price','u_price'),
    'type_price_gap':('gap','t_price','u_price'),
    'price_relative':('ratio','i_price','u_price',0.01),
    'price_z':('scaledgap','i_price','u_price','u_std',0.01),
    'price_iqr':('subtract','u_q75','u_q25'),
    'age_gap':('rawgap','raw_u_age','i_age'),
    'type_age_gap':('rawgap','raw_u_age','t_age'),
    'channel_gap':('gap','u_ch2','i_ch2'),
    'channel_match':('match','u_ch2','i_ch2'),
    'pair_recency_gap':('subtract','p_r','u_r'),
}
for prefix in ['t','s','d','c','v','a','g','pc']:
    DERIVED[f'{prefix}_share']=('ratio',f'u{prefix}_n0','u_n0',3)
    DERIVED[f'{prefix}_share30']=('ratio',f'u{prefix}_n30','u_n30',3)
    DERIVED[f'{prefix}_lift']=('lift',f'u{prefix}_n0','u_n0',f'{prefix}_n0')
    DERIVED[f'{prefix}_decshare']=('ratio',f'u{prefix}_dec30','u_dec30',1)
    DERIVED[f'{prefix}_recency_gap']=('subtract',f'u{prefix}_r','u_r')

CORE=['i_n7','i_n30','i_n0','i_r','u_n30','u_n0','u_r','p_n0','p_r']
TRENDS=['i_n14','i_n90','i_trend7','i_trend14','i_trend30','u_trend7','u_trend30']
PREF=['t_share','s_share','d_share','c_share','pc_share']
RECENT=['t_share30','s_share30','d_share30','c_share30','pc_share30']
LIFTS=['t_lift','s_lift','d_lift','c_lift','pc_lift']
PRICE=['i_price','u_price','u_std','price_gap','type_price_gap','price_relative','price_z']

# Initial unmeasured sketches, retained for provenance. NOT a fixed evaluation
# schedule: the user requested adaptive search across three populations instead.
PLANS = [
    ('01_popularity_recency','Популярность, активность и давность',
     CORE+['i_n90','i_uniq','user_diversity']),
    ('02_repurchase','Повторные покупки товара и продуктовой семьи',
     CORE+['p_n7','p_n30','pair_share','pair_recency_gap','upc_n0','upc_r','pc_share','pc_recency_gap']),
    ('03_trends','Короткие и длинные тренды популярности',
     CORE+TRENDS+['t_n7','t_n30','t_trend7','s_trend7','pc_trend7','item_buyer_share']),
    ('04_product_type','Предпочтения продуктовой семьи и типа',
     CORE+['upc_n0','upc_n30','upc_r','ut_n0','ut_n30','ut_r','pc_share','pc_share30','t_share','t_share30','t_lift','pc_lift']),
    ('05_visual_preferences','Цвет, оттенок и рисунок',
     CORE+['uc_n0','uc_r','uv_n0','uv_r','ua_n0','ua_r','c_share','v_share','a_share','c_share30','a_share30','c_lift']),
    ('06_hierarchy','Отдел, секция и группа одежды',
     CORE+['us_n0','us_r','ud_n0','ud_r','ug_n0','ug_r','s_share','d_share','g_share','s_share30','d_share30','g_share30']),
    ('07_recent_preferences','Краткосрочные предпочтения и тренды',
     CORE+PREF+RECENT+['i_trend7','t_trend7','s_trend7','pc_trend7','ut_r','us_r','uc_r']),
    ('08_exponential_decay','Экспоненциальное затухание интересов',
     CORE+['i_dec14','i_dec30','u_dec14','u_dec30','p_dec14','p_dec30','t_decshare','s_decshare','c_decshare','pc_decshare','d_decshare']),
    ('09_price_compatibility','Совместимость цен и разброс бюджета',
     CORE+PRICE+['u_q25','u_q75','price_iqr','p_price','t_price','pc_price','t_share','pc_share']),
    ('10_age_compatibility','Возраст аудитории товара и типа',
     CORE+['i_age','t_age','s_age','age_gap','type_age_gap','t_share','s_share','i_uniq','i_price','price_gap']),
    ('11_channel_preferences','Предпочтения каналов покупок',
     CORE+['u_ch2','i_ch2','t_ch2','pc_ch2','channel_gap','channel_match','t_share','pc_share','price_gap','i_trend7']),
    ('12_category_recency','Давность покупок каждой категории',
     CORE+['ut_r','us_r','ud_r','uc_r','ug_r','upc_r','t_recency_gap','s_recency_gap','c_recency_gap','pc_recency_gap']+PREF),
    ('13_smoothed_lifts','Сглаженные предпочтения относительно популярности',
     CORE+LIFTS+PREF+['g_lift','a_lift','t_n0','s_n0','c_n0','user_diversity','item_buyer_share']),
    ('14_type_copurchase','Совместные покупки разных типов одежды',
     CORE+PREF+['graph_t90','graph_t365','t_lift','t_share30','ut_r','i_trend7','price_gap']),
    ('15_section_copurchase','Совместные покупки разных секций',
     CORE+PREF+['graph_s90','graph_s365','s_lift','s_share30','us_r','i_trend30','price_z']),
    ('16_colour_copurchase','Совместные покупки разных цветов',
     CORE+['graph_c90','graph_c365','c_lift','c_share','c_share30','uc_r','a_share','v_share','t_share','s_share','i_trend7']),
    ('17_multilevel_copurchase','Совместные покупки на нескольких уровнях',
     CORE+PREF+['graph_t90','graph_s90','graph_c90','graph_g90','t_lift','s_lift','c_lift','price_gap','i_trend7']),
    ('18_price_weighted_interests','Ценовая совместимость и затухающие интересы',
     CORE+PRICE+['t_decshare','s_decshare','c_decshare','pc_decshare','p_dec30','i_dec14','u_dec30','t_share30','s_share30','c_share30']),
    ('19_balanced_temporal','Сбалансированный набор временных и личных признаков',
     CORE+TRENDS+PREF+RECENT+LIFTS+['price_gap','price_z','age_gap','p_dec30','user_diversity']),
    ('20_balanced_collaborative','Сбалансированный набор с совместными покупками',
     CORE+PREF+LIFTS+['graph_t90','graph_s90','graph_c90','graph_t365','t_decshare','s_decshare','c_decshare','i_trend7','i_trend30','price_gap','price_z','age_gap','channel_match','user_diversity']),
]

KERNEL = '''def modify_features(X, history):
    specs = SPECS_LITERAL
    derived = DERIVED_LITERAL
    outputs = OUTPUTS_LITERAL
    out = pd.DataFrame(index=X.index)
    if history.empty:
        for name in outputs:
            out['f_' + name] = 0.0
        return out
    memo = {}
    def lookup(series, keys):
        names = [k if k in ('customer_id','article_id') else 'raw_i_'+k for k in keys]
        if len(keys)==1:
            return X[names[0]].map(series).to_numpy(dtype=float)
        index = pd.MultiIndex.from_arrays([X[k].to_numpy() for k in names], names=keys)
        return series.reindex(index).to_numpy(dtype=float)
    def graph(name):
        code = name[6:7]
        days = int(name[7:])
        column = {'t':'product_type_no','s':'section_no','c':'colour_group_code','g':'garment_group_no'}[code]
        h = history.loc[history.days_ago<=days,['customer_id',column]].drop_duplicates()
        values = np.zeros(len(X),dtype=float)
        if h.empty:
            return values
        table = pd.crosstab(h.customer_id,h[column])
        b = table.to_numpy(dtype=float)
        norms = np.sqrt((b*b).sum(axis=0))
        sim = (b.T @ b) / np.maximum(norms[:,None]*norms[None,:],1.0)
        np.fill_diagonal(sim,0.0)
        scores = (b @ sim) / np.maximum(b.sum(axis=1,keepdims=True),1.0)
        rows = table.index.get_indexer(X.customer_id)
        cols = table.columns.get_indexer(X['raw_i_'+column])
        valid = (rows>=0)&(cols>=0)
        values[valid] = scores[rows[valid],cols[valid]]
        return values
    def get(name):
        if name in memo:
            return memo[name]
        if name.startswith('graph_'):
            value = graph(name)
        elif name in specs:
            keys,stat,window = specs[name]
            h = history if window==0 else history.loc[history.days_ago<=window]
            group = h.groupby(keys,sort=False)
            if stat=='n': s = group.size()
            elif stat=='r': s = group.days_ago.min()
            elif stat=='price': s = group.price.mean()
            elif stat=='std': s = group.price.std(ddof=0)
            elif stat=='q25': s = group.price.quantile(0.25)
            elif stat=='q75': s = group.price.quantile(0.75)
            elif stat=='age': s = group.customer_age.mean()
            elif stat=='uniq':
                col = 'article_id' if keys==['customer_id'] else 'customer_id'
                s = group[col].nunique()
            elif stat=='ch2':
                temp = h.assign(weight=(h.sales_channel_id==2).astype(float))
                s = temp.groupby(keys,sort=False).weight.mean()
            else:
                scale = 14.0 if stat=='dec14' else 30.0
                temp = h.assign(weight=np.exp(-h.days_ago/scale))
                s = temp.groupby(keys,sort=False).weight.sum()
            value = lookup(s,keys)
            if stat in ('n','uniq','dec14','dec30'):
                value = np.nan_to_num(value,nan=0.0)
        else:
            args = derived[name]
            op = args[0]
            if op=='rawgap': value = np.abs(X[args[1]].to_numpy(dtype=float)-get(args[2]))
            else:
                a,b = get(args[1]),get(args[2])
                if op=='ratio': value = a/(b+args[3])
                elif op=='gap': value = np.abs(a-b)
                elif op=='subtract': value = a-b
                elif op=='scaledgap': value = np.abs(a-b)/(get(args[3])+args[4])
                elif op=='match': value = a*b+(1.0-a)*(1.0-b)
                else: value = np.log1p(((a+0.5)/(b+5.0))/((get(args[3])+5.0)/(len(history)+5.0)))
        memo[name] = value
        return value
    for name in outputs:
        out['f_'+name] = get(name)
    return out.replace([np.inf,-np.inf],np.nan)
'''


def program(outputs):
    required_specs={}
    required_derived={}
    def add(name):
        if name.startswith('graph_'):return
        if name in SPECS:
            required_specs[name]=SPECS[name]
        elif name not in required_derived:
            formula=DERIVED[name]
            required_derived[name]=formula
            for dependency in formula[1:]:
                if isinstance(dependency,str) and not dependency.startswith('raw_'):add(dependency)
    for name in outputs:add(name)
    return KERNEL.replace('SPECS_LITERAL',repr(required_specs)).replace('DERIVED_LITERAL',repr(required_derived)).replace('OUTPUTS_LITERAL',repr(outputs))


def designs():
    assert len(PLANS)==20 and len({p[0] for p in PLANS})==20
    result=[]
    for ident,description,features in PLANS:
        assert len(features)==len(set(features)) and 1<=len(features)<=36,(ident,len(features))
        result.append({'id':ident,'description':description,'features':features,'code':program(features)})
    return result
