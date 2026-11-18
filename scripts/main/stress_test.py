"""Illustrative stress test: how much individual income tax is lost if earnings in
AI-exposed occupations fall by x%? Uses PLFS earners above the tax line for the tax
elasticity and the ITR-calibrated occupation tax shares for weights."""
import json, sys
import numpy as np, pandas as pd
sys.path.insert(0, "scripts/main")
from build_occupations import tax_liability
d = pd.DataFrame(json.load(open("site/data.json", encoding="utf-8")))
exp = dict(zip(d.slug, d.exposure)); share = dict(zip(d.slug, d.tax_share))
c = pd.read_parquet("data/derived/earners_2025.parquet")
c = c[c.annual >= 1.0e6].copy()
c["exp"] = c.occ.map(exp)
sal = (c.kind == "regular").values
base = tax_liability(c.annual.values, sal)
out = []
for thr in (6, 7, 8):
    for cut in (0.05, 0.10, 0.20):
        m = (c.exp >= thr).values
        inc = np.where(m, c.annual.values * (1 - cut), c.annual.values)
        new = tax_liability(inc, sal)
        el = ((base[m] - new[m]) * c.w.values[m]).sum() / (base[m] * c.w.values[m]).sum()
        grp = sum(v for k, v in share.items() if exp.get(k, 0) >= thr)
        out.append({"exposure_ge": thr, "earnings_cut": cut, "tax_drop_in_group": round(el, 3),
                    "group_tax_share": round(grp, 3), "pit_drop": round(el * grp, 4)})
r = pd.DataFrame(out); print(r.to_string())
r.to_csv("data/derived/stress_test.csv", index=False)
