import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    static = {
        "f_age":"raw_u_age", "f_type":"raw_i_product_type_no",
        "f_dept":"raw_i_department_no", "f_section":"raw_i_section_no",
        "f_colour":"raw_i_colour_group_code", "f_graphic":"raw_i_graphical_appearance_no",
        "f_garment":"raw_i_garment_group_no", "f_index":"raw_i_index_group_no"
    }
    for n, c in static.items():
        out[n] = X[c].fillna(-1).astype(float)
    names = ["f_i3","f_i7","f_i14","f_i30","f_i90","f_irec",
             "f_u7","f_u30","f_u90","f_urec","f_p30","f_prec",
             "f_t7","f_t30","f_t90","f_d30","f_d90","f_s90","f_c90",
             "f_pc90","f_iprice","f_uprice","f_gap","f_ch","f_ishare",
             "f_itrend","f_ushare","f_tshare"]
    for n in names:
        out[n] = 0.0
    if history is None or len(history) == 0:
        return out
    h = history
    cid = X["customer_id"]
    aid = X["article_id"]
    for d,n in [(3,"f_i3"),(7,"f_i7"),(14,"f_i14"),(30,"f_i30"),(90,"f_i90")]:
        out[n] = aid.map(h.loc[h.days_ago<=d].groupby("article_id").size()).fillna(0)
    for d,n in [(7,"f_u7"),(30,"f_u30"),(90,"f_u90")]:
        out[n] = cid.map(h.loc[h.days_ago<=d].groupby("customer_id").size()).fillna(0)
    out["f_irec"] = aid.map(h.groupby("article_id").days_ago.min()).fillna(999)
    out["f_urec"] = cid.map(h.groupby("customer_id").days_ago.min()).fillna(999)

    def match(hc, xc, d, n):
        z = h.loc[h.days_ago<=d].groupby(["customer_id",hc]).size().rename("v").reset_index()
        q = pd.DataFrame({"customer_id":cid.to_numpy(),hc:X[xc].to_numpy()})
        out[n] = q.merge(z,on=["customer_id",hc],how="left",sort=False)["v"].fillna(0).to_numpy()
    for d,n in [(7,"f_t7"),(30,"f_t30"),(90,"f_t90")]:
        match("product_type_no","raw_i_product_type_no",d,n)
    match("department_no","raw_i_department_no",30,"f_d30")
    match("department_no","raw_i_department_no",90,"f_d90")
    match("section_no","raw_i_section_no",90,"f_s90")
    match("colour_group_code","raw_i_colour_group_code",90,"f_c90")
    match("product_code","raw_i_product_code",90,"f_pc90")

    q = pd.DataFrame({"customer_id":cid.to_numpy(),"article_id":aid.to_numpy()})
    z = h.loc[h.days_ago<=30].groupby(["customer_id","article_id"]).size().rename("v").reset_index()
    out["f_p30"] = q.merge(z,on=["customer_id","article_id"],how="left",sort=False)["v"].fillna(0).to_numpy()
    z = h.groupby(["customer_id","article_id"]).days_ago.min().rename("v").reset_index()
    out["f_prec"] = q.merge(z,on=["customer_id","article_id"],how="left",sort=False)["v"].fillna(999).to_numpy()
    out["f_iprice"] = aid.map(h.groupby("article_id").price.mean()).fillna(0)
    out["f_uprice"] = cid.map(h.groupby("customer_id").price.mean()).fillna(0)
    out["f_gap"] = (out["f_iprice"]-out["f_uprice"]).abs()
    out["f_ch"] = aid.map(h.groupby("article_id").sales_channel_id.mean()).fillna(0)
    out["f_ishare"] = out["f_i7"]/(1+out["f_i90"])
    out["f_itrend"] = out["f_i7"]/(1+out["f_i30"]-out["f_i7"])
    out["f_ushare"] = out["f_u7"]/(1+out["f_u90"])
    out["f_tshare"] = out["f_t30"]/(1+out["f_u30"])
    return out
