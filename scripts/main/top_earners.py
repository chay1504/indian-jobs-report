import pandas as pd, numpy as np
s = pd.read_csv("data/nco/nco2015_structure.csv", dtype=str)
t3 = dict(zip(s[s.level=="group"].code.str.zfill(3), s[s.level=="group"].title))
c = pd.read_parquet("data/derived/earners_2025.parquet")
W = c.w.sum()
print("CWS earners (crore raw):", round(W/1e7,2))
for thr in [300000, 500000, 700000, 1000000, 1200000, 1275000, 2400000, 5000000, 10000000]:
    m = c.annual >= thr
    print(f">= Rs {thr/1e5:5.2f}L : {c.w[m].sum()/W*100:6.2f}% of earners, {c.w[m].sum()/1e5:8.1f} lakh people (raw w), sample n={m.sum()}")
print("\nmax monthly earnings by kind:", c.groupby("kind").month_earn.max().to_dict())
print("top 1% threshold annual:", c.annual.quantile(0.99), " weighted p99:")
o = np.argsort(c.annual.values); cw = np.cumsum(c.w.values[o])/W
for q in [0.5,0.75,0.9,0.95,0.99,0.995,0.999]:
    print(f"  p{q*100:g}: Rs {c.annual.values[o][np.searchsorted(cw,q)]:,.0f}")
tp = c[c.taxpayer]
g = tp.groupby("occ").agg(w=("w","sum"), tax=("tax", lambda x: (x*tp.loc[x.index,"w"]).sum()), n=("w","size")).sort_values("tax", ascending=False)
g["share_taxpayers"] = g.w/g.w.sum(); g["share_tax"] = g.tax/g.tax.sum()
g["title"] = g.index.map(lambda k: t3.get(k, "?"))
print("\nPLFS taxpayers (new regime FY26) by NCO 3-digit — top 25 by tax:")
print(g.head(25)[["title","n","share_taxpayers","share_tax"]].round(3).to_string())
print("by kind:", (tp.groupby("kind").w.sum()/tp.w.sum()).round(3).to_dict())
