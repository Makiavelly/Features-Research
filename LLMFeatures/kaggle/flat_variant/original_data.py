import json
from pathlib import Path
import pandas as pd
import numpy as np
class Data:
    def __init__(self,root):
        self.root=Path(root)
        self.manifest=json.loads((self.root/'manifest.json').read_text())
        self.items=pd.read_parquet(self.root/'articles.parquet').set_index('article_id')
        # XGBoost allocates categorical histograms up to the maximum code. Compact
        # all static item categories consistently in both X and history.
        self.category_maps={}
        for column in self.items:
            encoded,categories=pd.factorize(self.items[column],sort=True)
            self.category_maps[column]=categories.tolist()
            self.items[column]=encoded.astype('int32')
        self.users=pd.read_parquet(self.root/'customers.parquet').set_index('customer_id')
        self.tx=pd.read_parquet(self.root/'history.parquet')
        self.raw_u=['raw_u_'+c.lower() for c in self.users.columns]
        self.raw_i=['raw_i_'+c for c in self.items.columns]

    def inputs(self,pairs,cutoff):
        pairs=pairs[['customer_id','article_id']].reset_index(drop=True)
        users=self.users.reindex(pairs.customer_id).reset_index(drop=True)
        items=self.items.reindex(pairs.article_id).reset_index(drop=True)
        users.columns=self.raw_u
        items.columns=self.raw_i
        X=pd.concat([pairs,users,items],axis=1)
        cutoff=pd.Timestamp(cutoff)
        history=self.tx[(self.tx.t_dat<=cutoff)&(self.tx.t_dat>cutoff-pd.Timedelta(days=180))].copy()
        assert (history.t_dat<=cutoff).all()
        history['days_ago']=(cutoff-history.t_dat).dt.days.astype('int32')
        history=history.drop(columns='t_dat').merge(self.items.reset_index(),on='article_id',how='left',validate='many_to_one')
        history=history.merge(self.users[['age']].rename(columns={'age':'customer_age'}).reset_index(),on='customer_id',how='left',validate='many_to_one')
        return X,history

