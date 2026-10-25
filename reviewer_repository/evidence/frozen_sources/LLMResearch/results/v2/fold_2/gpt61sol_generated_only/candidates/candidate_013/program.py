import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    st = {
        "f_age":"raw_u_age","f_type_static":"raw_i_product_type_no",
        "f_dept_static":"raw_i_department_no","f_section_static":"raw_i_section_no",
        "f_colour_static":"raw_i_colour_group_code","f_graphic_static":"raw_i_graphical_appearance_no",
        "f_garment_static":"raw_i_garment_group_no","f_index_static":"raw_i_index_group_no",
        "f_value_static":"raw_i_perceived_colour_value_id","f_master_static":"raw_i_perceived_colour_master_id"
    }
    for n,c in st.items():
        out[n] = X[c].fillna(-1).astype(float)
    fs = ["f_item_1","f_item_3","f_item_7","f_item_14","f_item_30","f_item_90","f_item_rec",
          "f_user_7","f_user_30","f_user_90","f_user_rec","f_pair_7","f_pair_30","f_pair_rec",
          "f_type_7","f_type_30","f_type_90","f_dept_30","f_dept_90","f_section_90","f_garment_90",
          "f_colour_90","f_graphic_90","f_product_90","f_item_price","f_user_price"]
    for c in fs: out[c] = 0.0
    if history is None or len(history) == 0: return out
    h = history
    cid, aid = X.customer_id, X.article_id
    def ccount(k,d,n,x):
        z=h.loc[h.days_ago<=d]
        out[n]=X[x].map(z.groupby(k).size()).fillna(0).astype(float)
    for d,n in [(1,"f_item_1"),(3,"f_item_3"),(7,"f_item_7"),(14,"f_item_14"),(30,"f_item_30"),(90,"f_item_90")]:
        ccount("article_id",d,n,"article_id")
    for d,n in [(7,"f_user_7"),(30,"f_user_30"),(90,"f_user_90")]:
        ccount("customer_id",d,n,"customer_id")
    out["f_item_rec"]=aid.map(h.groupby("article_id").days_ago.min()).fillna(999)
    out["f_user_rec"]=cid.map(h.groupby("customer_id").days_ago.min()).fillna(999)
    def aff(hc,xc,d,n):
        z=h.loc[h.days_ago<=d].groupby(["customer_id",hc]).size().rename("v").reset_index()
        q=pd.DataFrame({"customer_id":cid.to_numpy(),hc:X[xc].to_numpy()})
        out[n]=q.merge(z,on=["customer_id",hc],how="left",sort=False)["v"].fillna(0).to_numpy()
    for d,n in [(7,"f_type_7"),(30,"f_type_30"),(90,"f_type_90")]: aff("product_type_no","raw_i_product_type_no",d,n)
    aff("department_no","raw_i_department_no",30,"f_dept_30")
    aff("department_no","raw_i_department_no",90,"f_dept_90")
    aff("section_no","raw_i_section_no",90,"f_section_90")
    aff("garment_group_no","raw_i_garment_group_no",90,"f_garment_90")
    aff("colour_group_code","raw_i_colour_group_code",90,"f_colour_90")
    aff("graphical_appearance_no","raw_i_graphical_appearance_no",90,"f_graphic_90")
    aff("product_code","raw_i_product_code",90,"f_product_90")
    q=pd.DataFrame({"customer_id":cid.to_numpy(),"article_id":aid.to_numpy()})
    for d,n in [(7,"f_pair_7"),(30,"f_pair_30")]:
        z=h.loc[h.days_ago<=d].groupby(["customer_id","article_id"]).size().rename("v").reset_index()
        out[n]=q.merge(z,on=["customer_id","article_id"],how="left",sort=False)["v"].fillna(0).to_numpy()
    z=h.groupby(["customer_id","article_id"]).days_ago.min().rename("v").reset_index()
    out["f_pair_rec"]=q.merge(z,on=["customer_id","article_id"],how="left",sort=False)["v"].fillna(999).to_numpy()
    out["f_item_price"]=aid.map(h.groupby("article_id").price.mean()).fillna(0)
    out["f_user_price"]=cid.map(h.groupby("customer_id").price.mean()).fillna(0)
    return out
