import pandas as pd, numpy as np
p = pd.read_parquet("data/microdata/persons_2025.parquet")
p["w"] = p["mult"].astype(float) / 100
for c in ["pas","sas","acws"]:
    p[c] = pd.to_numeric(p[c], errors="coerce")
print("sum weights (crore):", round(p.w.sum()/1e7,2), " per-month mean (crore):", round(p.groupby('month').w.sum().mean()/1e7,2))
print(p.groupby("month").w.sum().div(1e7).round(1).to_dict())
age15 = p[p.age >= 15]
work = set([11,12,21,31,41,51])
pw = age15.pas.isin(work)
sw = (~pw) & age15.sas.isin(work)
worker = pw | sw
lf = worker | (age15.pas == 81)
W = age15.w
print("15+ pop (crore, sum w):", round(W.sum()/1e7,1))
print("LFPR ps+ss 15+:", round(W[lf].sum()/W.sum()*100,1), " WPR:", round(W[worker].sum()/W.sum()*100,1), " UR:", round((W[lf].sum()-W[worker].sum())/W[lf].sum()*100,1))
st = np.where(pw, age15.pas, age15.sas)
s = pd.Series(st[worker.values]).map(lambda x: {11:'self',12:'self',21:'self',31:'regular',41:'casual',51:'casual'}[x])
print("status shares (ps+ss 15+):", (W[worker].groupby(s.values).sum()/W[worker].sum()*100).round(1).to_dict())
print("workers 15+ (sum of weights, crore):", round(W[worker].sum()/1e7,2))
# all ages
pwa = p.pas.isin(work) | ((~p.pas.isin(work)) & p.sas.isin(work))
print("workers all ages (crore):", round(p.w[pwa].sum()/1e7,2), " WPR all ages:", round(p.w[pwa].sum()/p.w.sum()*100,1))
