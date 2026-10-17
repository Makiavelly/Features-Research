def modify_features(X, history):
    specs = {'i_n7': (['article_id'], 'n', 7), 'i_n30': (['article_id'], 'n', 30), 'i_n0': (['article_id'], 'n', 0), 'i_r': (['article_id'], 'r', 0), 'u_n30': (['customer_id'], 'n', 30), 'u_n0': (['customer_id'], 'n', 0), 'u_r': (['customer_id'], 'r', 0), 'p_n0': (['customer_id', 'article_id'], 'n', 0), 'p_r': (['customer_id', 'article_id'], 'r', 0), 'ut_n0': (['customer_id', 'product_type_no'], 'n', 0), 'us_n0': (['customer_id', 'section_no'], 'n', 0), 'ud_n0': (['customer_id', 'department_no'], 'n', 0), 'uc_n0': (['customer_id', 'colour_group_code'], 'n', 0), 'upc_n0': (['customer_id', 'product_code'], 'n', 0), 't_n0': (['product_type_no'], 'n', 0), 's_n0': (['section_no'], 'n', 0), 'ut_n30': (['customer_id', 'product_type_no'], 'n', 30), 'us_n30': (['customer_id', 'section_no'], 'n', 30), 'i_price': (['article_id'], 'price', 0), 'u_price': (['customer_id'], 'price', 0), 'u_std': (['customer_id'], 'std', 0), 'i_n365': (['article_id'], 'n', 365), 'u_uniq': (['customer_id'], 'uniq', 0), 'i_uniq': (['article_id'], 'uniq', 0)}
    derived = {'t_share': ('ratio', 'ut_n0', 'u_n0', 3), 's_share': ('ratio', 'us_n0', 'u_n0', 3), 'd_share': ('ratio', 'ud_n0', 'u_n0', 3), 'c_share': ('ratio', 'uc_n0', 'u_n0', 3), 'pc_share': ('ratio', 'upc_n0', 'u_n0', 3), 't_lift': ('lift', 'ut_n0', 'u_n0', 't_n0'), 's_lift': ('lift', 'us_n0', 'u_n0', 's_n0'), 't_share30': ('ratio', 'ut_n30', 'u_n30', 3), 's_share30': ('ratio', 'us_n30', 'u_n30', 3), 'price_gap': ('gap', 'i_price', 'u_price'), 'price_z': ('scaledgap', 'i_price', 'u_price', 'u_std', 0.01), 'i_trend7': ('ratio', 'i_n7', 'i_n30', 3), 'i_trend30': ('ratio', 'i_n30', 'i_n365', 5), 'user_diversity': ('ratio', 'u_uniq', 'u_n0', 1)}
    outputs = ['i_n7', 'i_n30', 'i_n0', 'i_r', 'u_n30', 'u_n0', 'u_r', 'p_n0', 'p_r', 't_share', 's_share', 'd_share', 'c_share', 'pc_share', 'graph_t365', 'graph_s365', 't_lift', 's_lift', 't_share30', 's_share30', 'price_gap', 'price_z', 'i_trend7', 'i_trend30', 'user_diversity', 'i_uniq']
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
