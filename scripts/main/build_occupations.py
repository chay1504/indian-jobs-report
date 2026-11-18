"""
Build occupation-level statistics for India from PLFS Calendar Year 2025
unit-level data (first visit, Jan-Dec 2025).

Employment  : usual status (principal + subsidiary), age 15+, occupation = NCO-2015 3-digit
              of the principal activity if a principal-status worker, else of the subsidiary activity.
Earnings    : current weekly status (CWS) workers 15+, occupation = CWS NCO 3-digit:
                regular wage/salaried (31,71,72)  -> ern_reg  (preceding calendar month)
                self-employed (11,12,61,62)       -> ern_self (gross, last 30 days)
                casual labour (41,42,51)          -> wage earnings in reference week x 30/7
              unpaid family helpers (21) have zero earnings by definition and are excluded
              from earnings statistics (as in PLFS reports).
Education   : general education level of usual-status workers.
Formality   : regular wage/salaried AND eligible for any social security benefit (codes 1-7).
Tax         : annualised earnings run through the FY2025-26 new-regime slabs (see tax_liability).

Output: data/derived/occ3_2025.csv, data/derived/earners_2025.parquet
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "derived"
OUT.mkdir(parents=True, exist_ok=True)

WORK = {11, 12, 21, 31, 41, 51}
EDU_ORDER = {  # general education code -> (ordinal, label)
    1: (0, "Not literate"), 2: (1, "Literate, no formal schooling"), 3: (1, "Literate, no formal schooling"),
    4: (1, "Literate, no formal schooling"), 5: (2, "Below primary"), 6: (3, "Primary"), 7: (4, "Middle"),
    8: (5, "Secondary"), 10: (6, "Higher secondary"), 11: (7, "Diploma/certificate"),
    12: (8, "Graduate"), 13: (9, "Postgraduate & above"),
}


def tax_liability(income, salaried):
    """Income tax (incl. 4% cess) under the new regime for FY2025-26 / AY2026-27
    (Finance Act 2025): slabs 0-4L nil, 4-8L 5%, 8-12L 10%, 12-16L 15%, 16-20L 20%,
    20-24L 25%, >24L 30%; sec 87A rebate makes tax nil up to taxable income Rs 12L with
    marginal relief; standard deduction Rs 75,000 for salaried; surcharge 10/15/25% above
    50L/1Cr/2Cr (marginal relief on surcharge ignored)."""
    inc = np.asarray(income, dtype=float)
    taxable = np.where(salaried, np.maximum(inc - 75000, 0), np.maximum(inc, 0))
    slabs = [(400000, 0.0), (800000, 0.05), (1200000, 0.10), (1600000, 0.15),
             (2000000, 0.20), (2400000, 0.25), (np.inf, 0.30)]
    tax = np.zeros_like(taxable)
    lo = 0.0
    for hi, rate in slabs:
        tax += np.clip(taxable - lo, 0, hi - lo) * rate
        lo = hi
    # rebate u/s 87A + marginal relief
    tax = np.where(taxable <= 1200000, 0.0, np.minimum(tax, taxable - 1200000))
    sur = np.select([taxable > 2e7, taxable > 1e7, taxable > 5e6], [0.25, 0.15, 0.10], 0.0)
    return tax * (1 + sur) * 1.04


def wmedian(v, w):
    v = np.asarray(v, float); w = np.asarray(w, float)
    m = ~np.isnan(v)
    v, w = v[m], w[m]
    if len(v) == 0:
        return np.nan
    o = np.argsort(v)
    cw = np.cumsum(w[o])
    return float(v[o][np.searchsorted(cw, cw[-1] / 2)])


def main():
    p = pd.read_parquet(ROOT / "data" / "microdata" / "persons_2025.parquet")
    p["w"] = p["mult"].astype(float) / 100.0
    num = ["pas", "sas", "acws", "gedu_lvl", "ssec_pas", "ssec_sas", "job_pas", "job_sas", "sex", "sec",
           "ern_reg", "ern_self", "age", "etyp_pas", "etyp_sas"]
    for c in num:
        p[c] = pd.to_numeric(p[c], errors="coerce")
    p = p[p.age >= 15].copy()

    # ---------------- usual status employment ----------------
    pw = p.pas.isin(WORK)
    sw = ~pw & p.sas.isin(WORK)
    e = p[pw | sw].copy()
    is_p = pw[pw | sw]
    e["status"] = np.where(is_p, e.pas, e.sas)
    e["occ"] = np.where(is_p, e.ocu_pas, e.ocu_sas)
    e["ind"] = np.where(is_p, e.ind_pas, e.ind_sas)
    e["ssec"] = np.where(is_p, e.ssec_pas, e.ssec_sas)
    e["job"] = np.where(is_p, e.job_pas, e.job_sas)
    e["etyp"] = np.where(is_p, e.etyp_pas, e.etyp_sas)
    e["occ"] = e["occ"].astype("string").str.strip().str.zfill(3)
    e["nic2"] = e["ind"].astype("string").str.strip().str[:2]
    e["edu_ord"] = e.gedu_lvl.map(lambda x: EDU_ORDER.get(int(x), (np.nan,))[0] if pd.notna(x) else np.nan)
    e["regular"] = e.status == 31
    e["casual"] = e.status.isin([41, 51])
    e["selfemp"] = e.status.isin([11, 12, 21])
    e["formal"] = e.regular & e.ssec.between(1, 7)
    e["female"] = e.sex == 2
    e["urban"] = e.sec == 2
    e["govt"] = e.etyp.isin([5, 6, 7])
    e["grad"] = e.edu_ord >= 8
    print("usual-status workers 15+ (crore, raw weights):", round(e.w.sum() / 1e7, 2))
    print("records with missing/blank occupation:", int((e.occ.isna() | (e.occ == "000")).sum()))

    # ---------------- CWS earnings ----------------
    c = p[p.acws.isin([11, 12, 21, 31, 41, 42, 51, 61, 62, 71, 72])].copy()
    c["occ"] = c.ocu_cws.astype("string").str.strip().str.zfill(3)
    casual_week = np.zeros(len(c))
    for d in range(1, 8):
        for a in (1, 2):
            das = pd.to_numeric(c[f"das{a}{d}"], errors="coerce")
            ern = pd.to_numeric(c[f"ern{a}{d}"], errors="coerce").fillna(0)
            casual_week += np.where(das.isin([41, 42, 51]), ern, 0)
    c["kind"] = np.select(
        [c.acws.isin([31, 71, 72]), c.acws.isin([11, 12, 61, 62]), c.acws.isin([41, 42, 51]), c.acws == 21],
        ["regular", "self", "casual", "helper"], "other")
    c["month_earn"] = np.select(
        [c.kind == "regular", c.kind == "self", c.kind == "casual"],
        [c.ern_reg, c.ern_self, casual_week * 30 / 7], np.nan)
    c = c[c.kind != "helper"]
    c["annual"] = c.month_earn * 12
    c["tax"] = tax_liability(c.annual.fillna(0), (c.kind == "regular").values)
    c["taxpayer"] = c.tax > 0
    keep = ["occ", "kind", "w", "month_earn", "annual", "tax", "taxpayer", "sex", "sec", "st", "aind_cws", "gedu_lvl"]
    c[keep].to_parquet(OUT / "earners_2025.parquet", index=False)

    print("\nAverage monthly earnings (CWS, 15+), compare with PLFS 2025 report:")
    for k in ("regular", "self"):
        s = c[c.kind == k]
        print(f"  {k}: mean Rs {np.average(s.month_earn.fillna(0), weights=s.w):,.0f}")
    s = c[c.kind == "casual"]
    print(f"  casual: mean monthly Rs {np.average(s.month_earn.fillna(0), weights=s.w):,.0f}")
    print("Share of CWS earners with positive tax liability:", round(c.w[c.taxpayer].sum() / c.w.sum() * 100, 2), "%")
    print("Implied tax (raw weights, Rs lakh crore):", round((c.tax * c.w).sum() / 1e12, 3))

    # ---------------- aggregate by occupation ----------------
    rows = []
    for occ, g in e.groupby("occ"):
        ce = c[c.occ == occ]
        W = g.w.sum()
        rows.append({
            "occ3": occ,
            "n_obs": len(g),
            "jobs_raw": W,
            "pct_regular": g.w[g.regular].sum() / W,
            "pct_casual": g.w[g.casual].sum() / W,
            "pct_self": g.w[g.selfemp].sum() / W,
            "pct_formal": g.w[g.formal].sum() / W,
            "pct_female": g.w[g.female].sum() / W,
            "pct_urban": g.w[g.urban].sum() / W,
            "pct_govt": g.w[g.govt].sum() / W,
            "pct_grad": g.w[g.grad].sum() / W,
            "edu_median_ord": wmedian(g.edu_ord, g.w),
            "top_nic2": ";".join(g.groupby("nic2").w.sum().sort_values(ascending=False).head(3).index.astype(str)),
            "earn_n": len(ce),
            "pay_median": wmedian(ce.annual, ce.w) if len(ce) else np.nan,
            "pay_mean": float(np.average(ce.annual.fillna(0), weights=ce.w)) if len(ce) else np.nan,
            "pct_taxpayer": ce.w[ce.taxpayer].sum() / ce.w.sum() if len(ce) else np.nan,
            "tax_raw": float((ce.tax * ce.w).sum()) if len(ce) else 0.0,
            "earners_raw": ce.w.sum() if len(ce) else 0.0,
        })
    occ = pd.DataFrame(rows).sort_values("jobs_raw", ascending=False)
    occ.to_csv(OUT / "occ3_2025.csv", index=False)
    print("\noccupations:", len(occ), " total jobs raw (crore):", round(occ.jobs_raw.sum() / 1e7, 2))
    print(occ.head(25)[["occ3", "n_obs", "jobs_raw", "pay_median", "pct_formal", "pct_grad", "pct_taxpayer"]].to_string())


if __name__ == "__main__":
    main()
