"""
Allocate India's individual income tax to occupations.

Step 1 (ITR, CBDT AY2023-24 Table 2.1 "Individual - Range of Returned Income"):
    For every returned-income bracket, integrate today's tax law (FY2025-26 new regime,
    tax_liability() in build_occupations.py) over a mean-preserving linear density inside the
    bracket (Pareto tail for the open top bracket). Result: forward-looking tax by bracket.
Step 2 (PLFS 2025 unit data): occupational mix of earners inside each earnings bracket
    (brackets above Rs 25 lakh pooled because the survey has few observations there).
Step 3: occupation tax share = sum over brackets of (bracket tax share x occupation share in bracket).

Also reports the actual AY2023-24 concentration (tax payable distribution, Table 2.11).
Output: data/derived/tax_by_bracket.csv, data/derived/occ_tax_share.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "main"))
from build_occupations import tax_liability  # noqa: E402

SALARY_SHARE = None  # filled from ITR salary table


def bracket_tax(a, b, n, total, salaried_frac, pts=400):
    """Expected total tax for n returns with incomes in [a,b] and given total income."""
    if n <= 0:
        return 0.0
    m = total / n
    if np.isinf(b):  # Pareto tail with mean m above a: alpha = m/(m-a)
        alpha = m / (m - a) if m > a else 3.0
        u = (np.arange(pts) + 0.5) / pts
        x = a * (1 - u) ** (-1 / alpha)
    else:
        mid, half = (a + b) / 2, (b - a) / 2
        # linear density f(x) = 1 + k (x-mid)/half on [a,b]; mean = mid + k*half/3
        k = np.clip((m - mid) * 3 / half, -1, 1)
        u = (np.arange(pts) + 0.5) / pts
        if abs(k) < 1e-9:
            t = 2 * u - 1
        else:  # inverse CDF of f(t) = (1 + k t)/2 on [-1,1]
            t = (-1 + np.sqrt((1 - k) ** 2 + 4 * k * u)) / k
        x = mid + t * half
        x = x * (m / x.mean())  # exact mean match
    tax_sal = tax_liability(x, np.ones_like(x, bool)).mean()
    tax_non = tax_liability(x, np.zeros_like(x, bool)).mean()
    return n * (salaried_frac * tax_sal + (1 - salaried_frac) * tax_non)


def main():
    d = pd.read_csv(ROOT / "data" / "tax" / "itr_distribution_AY2023-24.csv")
    ind = d[d.status.str.contains("ndividual")]
    ri = ind[ind.distribution_variable == "returned_income"].copy()
    ri = ri[~ri.range_label.isin(["Total", "< 0", "= 0"])]
    ri["lower_rs"] = ri.lower_rs.astype(float)
    ri["upper_rs"] = ri.upper_rs.astype(float).fillna(np.inf)
    sal = ind[ind.distribution_variable == "salary_income"]
    sal_total = sal[sal.range_label == "Total"].sum_of_variable_rs_crore.iloc[0]
    gti_total = ind[(ind.distribution_variable == "gross_total_income") & (ind.range_label == "Total")].sum_of_variable_rs_crore.iloc[0]
    sal_frac = sal_total / gti_total
    rows = []
    for _, r in ri.iterrows():
        t = bracket_tax(r.lower_rs, r.upper_rs, r.n_returns, r.sum_of_variable_rs_crore * 1e7, sal_frac)
        rows.append({"range": r.range_label, "lower": r.lower_rs, "upper": r.upper_rs, "n": r.n_returns,
                     "income_cr": r.sum_of_variable_rs_crore, "tax_newregime_cr": t / 1e7})
    tb = pd.DataFrame(rows)
    tot = tb.tax_newregime_cr.sum()
    tb["tax_share"] = tb.tax_newregime_cr / tot
    tb.to_csv(ROOT / "data" / "derived" / "tax_by_bracket.csv", index=False)
    print(f"salary share of GTI: {sal_frac:.1%}")
    print(f"Forward-looking individual tax at AY2023-24 incomes under FY2025-26 law: Rs {tot/1e5:.2f} lakh crore "
          f"(actual AY2023-24 tax payable under then-law: Rs 6.77 lakh crore)")
    pay = tb[tb.tax_newregime_cr > 0]
    print(f"returns with positive tax under today's law: {pay.n.sum()/1e5:.1f} lakh (upper bound: bracket containing 12L counted fully)")
    print(tb[["range", "n", "tax_newregime_cr", "tax_share"]].to_string())

    # ---- PLFS occupational mix by earnings bracket ----
    c = pd.read_parquet(ROOT / "data" / "derived" / "earners_2025.parquet")
    edges = [1.2e6, 1.5e6, 2.0e6, 2.5e6, np.inf]
    labels = ["12-15L", "15-20L", "20-25L", "25L+"]
    c = c[c.annual >= 1.2e6].copy()
    c["b"] = pd.cut(c.annual, edges, labels=labels, right=False)
    mix = c.groupby(["b", "occ"], observed=True).w.sum()
    mix = mix / mix.groupby(level=0).transform("sum")
    nobs = c.groupby("b", observed=True).size()
    print("\nPLFS observations per bracket:", nobs.to_dict())

    # ITR tax mapped onto the same 4 brackets
    def itr_tax(lo, hi):
        s = 0.0
        for _, r in tb.iterrows():
            a, b = r.lower, r.upper
            ov = max(0.0, min(b, hi) - max(a, lo))
            if ov <= 0:
                continue
            frac = 1.0 if np.isinf(b) and np.isinf(hi) else ov / (b - a) if not np.isinf(b) else 1.0
            s += r.tax_newregime_cr * frac
        return s

    btax = {"12-15L": itr_tax(1.0e6, 1.5e6), "15-20L": itr_tax(1.5e6, 2.0e6),
            "20-25L": itr_tax(2.0e6, 2.5e6), "25L+": itr_tax(2.5e6, np.inf)}
    btot = sum(btax.values())
    print("tax share by bracket:", {k: round(v / btot, 3) for k, v in btax.items()})
    occ_share = {}
    for (b, occ), s in mix.items():
        occ_share[occ] = occ_share.get(occ, 0) + s * btax[b] / btot
    v1 = pd.Series(occ_share, name="tax_share_v1")

    # ---- v2: split each bracket's tax into salary vs non-salary income (ITR Table 2.2 vs 2.1) ----
    gti = ind[ind.distribution_variable == "gross_total_income"].copy()
    sal = ind[ind.distribution_variable == "salary_income"].copy()
    for t in (gti, sal):
        t["lower_rs"] = pd.to_numeric(t.lower_rs, errors="coerce")
        t["upper_rs"] = pd.to_numeric(t.upper_rs, errors="coerce").fillna(np.inf)

    def ssum(t, lo, hi):
        m = (t.lower_rs >= lo) & (t.lower_rs < hi) & ~t.range_label.isin(["Total", "< 0", "= 0"])
        return t[m].sum_of_variable_rs_crore.sum()

    groups = {"12-15L": (1.0e6, 1.5e6), "15-20L": (1.5e6, 2.0e6), "20L+": (2.0e6, np.inf)}
    sal_frac_b = {k: min(1.0, ssum(sal, *v) / ssum(gti, *v)) for k, v in groups.items()}
    btax2 = {"12-15L": btax["12-15L"], "15-20L": btax["15-20L"], "20L+": btax["20-25L"] + btax["25L+"]}
    print("\nsalary share of income by bracket (ITR):", {k: round(v, 3) for k, v in sal_frac_b.items()})

    cc = pd.read_parquet(ROOT / "data" / "derived" / "earners_2025.parquet")
    cc = cc[cc.annual >= 1.2e6]

    def mix_of(df):
        m = df.groupby("occ").w.sum()
        return m / m.sum()

    reg, slf = cc[cc.kind == "regular"], cc[cc.kind == "self"]
    sal_mix = {"12-15L": mix_of(reg[reg.annual < 1.5e6]), "15-20L": mix_of(reg[(reg.annual >= 1.5e6) & (reg.annual < 2e6)]),
               "20L+": mix_of(reg[reg.annual >= 2e6])}
    self_mix = {"12-15L": mix_of(slf[slf.annual < 2e6]), "15-20L": mix_of(slf[slf.annual < 2e6]),
                "20L+": mix_of(slf[slf.annual >= 2e6])}
    print("PLFS obs: salaried", {k: int(len(v)) for k, v in sal_mix.items()}, " self-employed pools:",
          len(slf[slf.annual < 2e6].occ.unique()), len(slf[slf.annual >= 2e6].occ.unique()))
    occ2 = {}
    t2 = sum(btax2.values())
    salaried_tax_share = 0.0
    for b, tx in btax2.items():
        sf = sal_frac_b[b]
        salaried_tax_share += tx / t2 * sf
        for occ, sh in sal_mix[b].items():
            occ2[occ] = occ2.get(occ, 0) + tx / t2 * sf * sh
        for occ, sh in self_mix[b].items():
            occ2[occ] = occ2.get(occ, 0) + tx / t2 * (1 - sf) * sh
    print(f"share of forward-looking income tax attributable to salary income: {salaried_tax_share:.1%}")
    out = pd.DataFrame({"tax_share": pd.Series(occ2), "tax_share_v1": v1}).fillna(0).sort_values("tax_share", ascending=False)
    out.index.name = "occ3"
    out.to_csv(ROOT / "data" / "derived" / "occ_tax_share.csv")
    s = pd.read_csv(ROOT / "data" / "nco" / "nco2015_structure.csv", dtype=str)
    t3 = dict(zip(s[s.level == "group"].code.str.zfill(3), s[s.level == "group"].title))
    print("\nEstimated share of individual income tax by occupation (v2 = salary/non-salary split; v1 = pooled):")
    for k, r in out.head(25).iterrows():
        print(f"  {k} {t3.get(k, '?')[:55]:55s} v2 {r.tax_share:6.1%}   v1 {r.tax_share_v1:6.1%}")


if __name__ == "__main__":
    main()
