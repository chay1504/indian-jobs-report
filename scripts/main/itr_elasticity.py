"""Tax elasticity on the actual ITR income distribution (AY2023-24, Table 2.1), today's law."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "scripts/main")
from tax_by_occupation import bracket_tax
d = pd.read_csv("data/tax/itr_distribution_AY2023-24.csv")
ri = d[d.status.str.contains("ndividual") & (d.distribution_variable == "returned_income")]
ri = ri[~ri.range_label.isin(["Total", "< 0", "= 0"])]
def total(scale):
    t = 0
    for _, r in ri.iterrows():
        a = float(r.lower_rs) * scale; b = float(r.upper_rs) * scale if pd.notna(r.upper_rs) else np.inf
        t += bracket_tax(a, b, r.n_returns, r.sum_of_variable_rs_crore * 1e7 * scale, 0.57)
    return t
base = total(1.0)
rows = []
for cut in (0.05, 0.10, 0.20):
    drop = 1 - total(1 - cut) / base
    rows.append({"earnings_cut": cut, "itr_tax_drop": round(drop, 3), "elasticity": round(drop / cut, 2)})
r = pd.DataFrame(rows); print(r.to_string()); r.to_csv("data/derived/itr_elasticity.csv", index=False)
