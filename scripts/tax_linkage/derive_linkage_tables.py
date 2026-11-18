"""Derived tables for the occupation -> income-tax linkage lane.

Inputs (all local, see research/tax_linkage.md for URLs):
  data/tax_linkage/cbdt_itr_ay2023-24_individual_income_heads_by_range.csv (parse_itr_stats.py)
  data/plfs/plfs_earnings.csv  (PLFS agent; official PLFS 2025 Table 51)
  data/raw/tax_linkage/indialabourobservatory_plfs-2025-tables.csv (secondary; quantiles, table 7.8)
  Hand-entered official figures with page refs (HCES 2023-24 Table 3.1/3.2; NIPFP WP430 Fig 7;
  ES 2025-26 Stat. App. Table 5.3B; DoE Annual Report on Pay & Allowances 2023-24).
Outputs: data/tax_linkage/*.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/tax_linkage"
LAKH = 1e5

# ------------------------------------------------------------------ 1. ITR thresholds by income head
rng = pd.read_csv(OUT / "cbdt_itr_ay2023-24_individual_income_heads_by_range.csv", dtype={"table": str})
EDGES = [(-np.inf, 0), (0, 0), (0, 1.5), (1.5, 2), (2, 2.5), (2.5, 3.5), (3.5, 4), (4, 4.5), (4.5, 5), (5, 5.5),
         (5.5, 9.5), (9.5, 10), (10, 15), (15, 20), (20, 25), (25, 50), (50, 100), (100, 500), (500, 1000),
         (1000, 2500), (2500, 5000), (5000, 10000), (10000, 50000), (50000, np.inf)]  # Rs lakh


def above(table, x):
    """count and sum (Rs crore) of returns with value > x lakh; uniform density inside the bin containing x."""
    g = rng[rng.table == table].sort_values("row_order").reset_index(drop=True)
    assert len(g) == len(EDGES), (table, len(g))
    n = s = 0.0
    method = "exact (bin edge)"
    for (lo, hi), r in zip(EDGES, g.itertuples()):
        if lo >= x:
            n += r.n_returns
            s += r.sum_crore
        elif lo < x < hi and np.isfinite(hi):
            f = (hi - x) / (hi - lo)
            n += r.n_returns * f
            # mean of the upper part of a uniform bin is (x+hi)/2 lakh
            s += r.n_returns * f * (x + hi) / 2 * LAKH / 1e7
            method = f"interpolated: uniform density in {lo}-{hi} lakh bin (fraction {f:.3f})"
    return n, s, method


rows = []
for x in [5, 7, 10, 12, 12.75, 15, 20, 24, 25, 50, 100, 500]:
    ng, sg, mg = above("2.1", x)
    ns, ss, ms = above("2.2", x)
    nb, sb, mb = above("2.4", x)
    rows.append(dict(threshold_rs_lakh=x,
                     n_gti_above=round(ng), n_salary_above=round(ns), n_business_above=round(nb),
                     salary_count_as_pct_of_gti_count=round(100 * ns / ng, 1),
                     business_count_as_pct_of_gti_count=round(100 * nb / ng, 1),
                     sum_gti_above_cr=round(sg), sum_salary_above_cr=round(ss), sum_business_above_cr=round(sb),
                     pct_of_60cr_workforce_salary_above=round(100 * ns / 60e7, 2),
                     pct_of_60cr_workforce_gti_above=round(100 * ng / 60e7, 2),
                     method=mg if mg == ms == mb else f"GTI: {mg}; salary: {ms}; business: {mb}"))
thr = pd.DataFrame(rows)
thr["note"] = ("AY2023-24 (incomes of FY2022-23). Counts are univariate per income head (CBDT publishes no cross-tab): "
               "n_salary_above = individuals whose SALARY income alone exceeds the threshold. salary_count_as_pct_of_gti_count "
               "is therefore the share of >X earners whose salary alone exceeds X (a lower bound on 'salaried' among top earners). "
               "Workforce denominator 60 crore is the tax agent's convention (data/tax). Thresholds 7/12/12.75/24 are interpolated.")
thr["source"] = "CBDT Income Tax Return Statistics AY2023-24 v1.0, Tables 2.1 (GTI), 2.2 (salary), 2.4 (business), PDF pp.21,22,24"
thr.to_csv(OUT / "itr_salary_business_thresholds_AY2023-24.csv", index=False)
print(thr.drop(columns=["note", "source", "method"]).to_string())

# ------------------------------------------------------------------ 2. HCES 2023-24 fractile shares
FR = ["0-5", "5-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-95", "95-100"]
W = [.05, .05, .1, .1, .1, .1, .1, .1, .1, .1, .05, .05]
MPCE = {  # Rs per person per month, without imputation of free items. HCES 2023-24 report Table 3.1 / 3.2 (PDF pp.40-41)
    ("2023-24", "rural"): [1677, 2126, 2473, 2833, 3162, 3498, 3866, 4304, 4885, 5763, 6929, 10137],
    ("2023-24", "urban"): [2376, 3093, 3687, 4353, 4979, 5622, 6334, 7199, 8353, 10139, 12817, 20310],
    ("2022-23", "rural"): [1373, 1782, 2112, 2454, 2768, 3094, 3455, 3887, 4458, 5356, 6638, 10501],
    ("2022-23", "urban"): [2001, 2607, 3157, 3762, 4348, 4963, 5662, 6524, 7673, 9582, 12399, 20824],
}
ALL = {("2023-24", "rural"): 4122, ("2023-24", "urban"): 6996, ("2022-23", "rural"): 3773, ("2022-23", "urban"): 6459}
hrows = []
for (yr, sec), v in MPCE.items():
    tot = sum(w * m for w, m in zip(W, v))
    for fr, w, m in zip(FR, W, v):
        hrows.append(dict(survey=f"HCES {yr}", sector=sec, fractile_class_pct=fr, pop_share=w, avg_mpce_rs=m,
                          consumption_share_pct=round(100 * w * m / tot, 2),
                          check_weighted_mean_vs_published=f"{tot:.0f} vs {ALL[(yr, sec)]}"))
h = pd.DataFrame(hrows)
h["source"] = ("MoSPI NSS Report 592, Survey on Household Consumption Expenditure 2023-24, Table 3.1 and 3.2 "
               "(printed pp.22-23, PDF pp.40-41); MPCE without imputed free items")
h.to_csv(OUT / "hces_fractile_mpce_and_consumption_shares.csv", index=False)

# top-share summary within sector and pooled national (rural pop share sensitivity)
summ = []
for (yr, sec), v in MPCE.items():
    tot = sum(w * m for w, m in zip(W, v))
    for k, lab in [(1, "top5"), (2, "top10"), (3, "top20"), (7, "top50")]:
        idx = range(12 - k, 12) if k < 7 else range(6, 12)
        share = sum(W[i] * v[i] for i in idx) / tot
        summ.append(dict(survey=f"HCES {yr}", scope=sec, group=lab, consumption_share_pct=round(100 * share, 1),
                         method="exact from published fractile means (within sector)"))
for yr in ["2023-24", "2022-23"]:
    for rs in [0.62, 0.65, 0.68]:
        cells = [(rs * w, m) for w, m in zip(W, MPCE[(yr, "rural")])] + [((1 - rs) * w, m) for w, m in zip(W, MPCE[(yr, "urban")])]
        cells.sort(key=lambda c: -c[1])
        tot = sum(p * m for p, m in cells)
        for target, lab in [(.05, "top5"), (.10, "top10"), (.20, "top20")]:
            acc_p = acc_c = 0.0
            for p, m in cells:
                take = min(p, target - acc_p)
                if take <= 0:
                    break
                acc_p += take
                acc_c += take * m
            summ.append(dict(survey=f"HCES {yr}", scope=f"all-India pooled (rural pop share {rs:.2f})", group=lab,
                             consumption_share_pct=round(100 * acc_c / tot, 1),
                             method="approx: pooled rural+urban fractile cells ranked by mean MPCE; assumes uniform MPCE within cell; "
                                    "rural share of population is an assumption (not in PDF report; Table A2 is Excel-only)"))
hs = pd.DataFrame(summ)
hs.to_csv(OUT / "hces_top_consumption_shares.csv", index=False)
print(hs.to_string())

# ------------------------------------------------------------------ 3. GST incidence (NIPFP WP430)
gst_r = [1.7, 2.3, 5.5, 6.4, 7.3, 8.2, 9.2, 10.3, 11.8, 14.2, 8.8, 14.3]
gst_u = [1.5, 2.0, 4.9, 5.9, 6.7, 7.6, 8.7, 9.9, 11.7, 14.5, 9.3, 17.1]
cons22 = h[h.survey == "HCES 2022-23"]
g = []
for sec, vals in [("rural", gst_r), ("urban", gst_u)]:
    c = cons22[cons22.sector == sec].consumption_share_pct.tolist()
    for fr, gv, cv in zip(FR, vals, c):
        g.append(dict(sector=sec, fractile_class_pct=fr, share_of_gst_burden_pct=gv, share_of_consumption_pct_hces2022_23=cv))
g = pd.DataFrame(g)
g["source"] = ("GST: Mukherjee (2025) NIPFP Working Paper 430, Figure 7 (average of scenarios I and II; HCES 2022-23 basis, "
               "pre-Sept-2025 GST rates; PDF p.14). Consumption: HCES 2022-23 fractile means as in HCES 2023-24 report Table 3.2")
g.to_csv(OUT / "gst_burden_by_mpce_fractile_nipfp.csv", index=False)
print(g.groupby("sector").apply(lambda d: pd.Series({"top5_gst": d.share_of_gst_burden_pct.iloc[-1],
      "top10_gst": d.share_of_gst_burden_pct.iloc[-2:].sum(), "top20_gst": d.share_of_gst_burden_pct.iloc[-3:].sum(),
      "bottom50_gst": d.share_of_gst_burden_pct.iloc[:6].sum(),
      "top5_cons": d.share_of_consumption_pct_hces2022_23.iloc[-1], "top20_cons": d.share_of_consumption_pct_hces2022_23.iloc[-3:].sum()})))

# ------------------------------------------------------------------ 4. occupation earnings vs zero-tax line
pl = pd.read_csv(ROOT / "data/plfs/plfs_earnings.csv")
t51 = pl[pl.table.str.startswith("Table (51)") & pl.unit.str.startswith("Rs") & (pl.sex == "person")
         & pl.category_code.astype(str).str.fullmatch(r"[1-9]|all")]
occ = t51.pivot_table(index=["category_code", "category_name"], columns="sector", values="value").reset_index()
occ.columns.name = None
occ = occ[occ.category_name != "all sections"]  # drop casual-wage row that shares code 'all'
occ = occ.rename(columns={"rural+urban": "avg_monthly_rs_all", "rural": "avg_monthly_rs_rural", "urban": "avg_monthly_rs_urban"})
ZERO = 12.75 * LAKH  # salaried zero-tax gross under new regime from FY2025-26 (Rs 12 lakh rebate + Rs 75,000 std deduction)
occ["avg_annual_rs_all"] = (occ.avg_monthly_rs_all * 12).round(0)
occ["avg_annual_as_pct_of_12.75L"] = (100 * occ.avg_annual_rs_all / ZERO).round(1)
occ["monthly_pay_needed_for_12.75L"] = round(ZERO / 12)
occ["source"] = ("PLFS 2025 (Jan-Dec 2025) Appendix Table (51): average monthly wage/salary earnings of regular wage/salaried "
                 "employees (CWS) by NCO-2015 division; via data/plfs/plfs_earnings.csv (PLFS agent)")
occ.to_csv(OUT / "occupation_earnings_vs_zero_tax_line.csv", index=False)
print(occ[["category_code", "category_name", "avg_monthly_rs_all", "avg_monthly_rs_urban", "avg_annual_rs_all", "avg_annual_as_pct_of_12.75L"]].to_string())

# ------------------------------------------------------------------ 5. earnings-distribution benchmarks
ilo = pd.read_csv(ROOT / "data/raw/tax_linkage/indialabourobservatory_plfs-2025-tables.csv", comment="#")
q = ilo[(ilo.table.astype(str) == "7.8") & (ilo.sex == "person")][["row", "sector", "value", "n"]]
bench = [dict(measure=f"Regular wage/salaried monthly earnings {r.row} ({r.sector})", value=r.value, unit="Rs/month",
              annualised_rs_lakh=round(r.value * 12 / LAKH, 2), period="Jan-Dec 2025",
              source="India Labour Observatory (Kumar & Pradhan), PLFS 2025 unit-level, table 7.8, https://indialabourobservatory.com/data/plfs-2025/earnings/ "
                     "[SECONDARY; its mean Rs 22,699 matches MoSPI Statement 11 exactly]", confidence="medium")
         for r in q.itertuples()]
bench += [
    dict(measure="Top 10% threshold, pre-tax national income per adult (20+)", value=290848, unit="Rs/year", annualised_rs_lakh=2.91,
         period="2022-23", source="WIL WP 2024/09 (Bharti, Chancel, Piketty, Somanchi), Table 2, PDF p.41", confidence="medium (model: tax+survey scaled to national accounts)"),
    dict(measure="Top 1% threshold, pre-tax national income per adult (20+)", value=2073846, unit="Rs/year", annualised_rs_lakh=20.74,
         period="2022-23", source="WIL WP 2024/09, Table 2, PDF p.41", confidence="medium"),
    dict(measure="Top 0.1% threshold, pre-tax national income per adult (20+)", value=8220379, unit="Rs/year", annualised_rs_lakh=82.2,
         period="2022-23", source="WIL WP 2024/09, Table 2, PDF p.41", confidence="medium"),
    dict(measure="Monthly wage at which a worker enters the top 10% of wage earners", value=25000, unit="Rs/month", annualised_rs_lakh=3.0,
         period="PLFS 2019-20", source="Institute for Competitiveness/EAC-PM 'State of Inequality in India' (May 2022) as reported by Business Standard/Down To Earth [SECONDARY]", confidence="low-medium"),
    dict(measure="Households with income > Rs 30 lakh/yr ('rich'): people", value=56000000, unit="persons", annualised_rs_lakh=None,
         period="2020-21", source="PRICE ICE 360 survey 2021 as reported by Business Standard/ThePrint [SECONDARY, household not worker income]", confidence="low"),
]
pd.DataFrame(bench).to_csv(OUT / "earnings_distribution_benchmarks.csv", index=False)

# ------------------------------------------------------------------ 6. central government employees
gov = pd.DataFrame([
    dict(item="Regular civilian employees in position, Group A (Central Govt + UTs)", value=115326, unit="persons", date="01.03.2024", page="Table 20, printed p.41 (PDF p.40)"),
    dict(item="Regular civilian employees in position, Group B", value=304138, unit="persons", date="01.03.2024", page="Table 20, printed p.41 (PDF p.40)"),
    dict(item="Regular civilian employees in position, Group C", value=2737898, unit="persons", date="01.03.2024", page="Table 20, printed p.41 (PDF p.40)"),
    dict(item="Regular civilian employees in position, total", value=3157362, unit="persons", date="01.03.2024", page="Table 20, printed p.41 (PDF p.40)"),
    dict(item="Expenditure on pay & allowances (excl. bonus, leave encashment, TA)", value=275083.75, unit="Rs crore", date="FY2022-23", page="Salient features para 1, printed p.3 (PDF p.5)"),
    dict(item="Employees in position incl. UTs", value=3062000, unit="persons", date="01.03.2023", page="Salient features para 9, printed p.4 (PDF p.6)"),
    dict(item="DERIVED average pay & allowances per employee = 275083.75e7 / 30.62e5", value=round(275083.75e7 / 30.62e5), unit="Rs/year", date="FY2022-23", page="derived"),
])
gov["share_pct"] = None
tot = 3157362
for i in range(3):
    gov.loc[i, "share_pct"] = round(100 * gov.loc[i, "value"] / tot, 2)
gov["source"] = "Dept of Expenditure, Annual Report on Pay and Allowances of Central Government Civilian Employees 2023-24, https://doe.gov.in/files/annual_reports_documents/AnnualReportonPayAllowance202324.pdf"
gov.to_csv(OUT / "central_govt_employees_pay.csv", index=False)
print(gov[["item", "value", "share_pct"]].to_string())

# ------------------------------------------------------------------ 7. IT / services macro
firm = pd.read_csv(OUT / "firm_median_pay.csv")
it = firm[firm.sector.str.contains("IT")]
macro = [
    dict(item="Telecom, computer & information services exports (BPM6 credit)", fy="2022-23", value=152285, unit="USD million", source="Economic Survey 2025-26 Statistical Appendix Table 5.3B (RBI), PDF p.3"),
    dict(item="Telecom, computer & information services exports (BPM6 credit)", fy="2023-24", value=163610, unit="USD million", source="ES 2025-26 Stat. App. Table 5.3B (RBI)"),
    dict(item="Telecom, computer & information services exports (BPM6 credit)", fy="2024-25 (PR)", value=183347, unit="USD million", source="ES 2025-26 Stat. App. Table 5.3B (RBI)"),
    dict(item="Telecom, computer & information services exports (BPM6 credit)", fy="2025-26 Apr-Sep (P)", value=98291, unit="USD million", source="ES 2025-26 Stat. App. Table 5.3B (RBI)"),
    dict(item="Other business services exports (credit; includes GCC-type professional/R&D services)", fy="2024-25 (PR)", value=107212, unit="USD million", source="ES 2025-26 Stat. App. Table 5.3B (RBI)"),
    dict(item="Total services exports (credit)", fy="2024-25 (PR)", value=387553, unit="USD million", source="ES 2025-26 Stat. App. Table 5.3B (RBI)"),
    dict(item="IT&ITeS industry revenue incl. hardware (Nasscom estimate)", fy="2024-25", value=283, unit="USD billion", source="Economic Survey 2025-26 ch.7 para 7.32 (printed p.279) citing Nasscom"),
    dict(item="Global Capability Centres in India", fy="FY24", value=1700, unit="count", source="ES 2025-26 ch.7 para 7.33 & Chart VII.12 (Nasscom)"),
    dict(item="GCC headcount", fy="FY24(E)", value=19, unit="lakh persons", source="ES 2025-26 ch.7 Chart VII.12 (Nasscom)"),
    dict(item="GCC revenue", fy="FY24(E)", value=64.6, unit="USD billion", source="ES 2025-26 ch.7 Chart VII.12 (Nasscom)"),
    dict(item="Software services exports growth (RBI survey)", fy="2024-25", value=7.3, unit="% YoY", source="ES 2025-26 ch.4 para 4.59 (printed p.171) citing RBI survey 2024-25"),
    dict(item="Six listed IT firms: standalone current tax (TCS, Infosys, HCLTech, Wipro, TechM, LTIMindtree)", fy="2024-25",
         value=round(it[it.fiscal_year == "FY2024-25"].current_tax_cr_standalone.sum(), 1), unit="Rs crore", source="firm_median_pay.csv (annual reports); includes overseas-branch taxes"),
    dict(item="Six listed IT firms: standalone current tax", fy="2025-26",
         value=round(it[it.fiscal_year == "FY2025-26"].current_tax_cr_standalone.sum(), 1), unit="Rs crore", source="firm_median_pay.csv (annual reports)"),
    dict(item="Six listed IT firms: standalone employee benefits expense", fy="2025-26",
         value=round(it[it.fiscal_year == "FY2025-26"].employee_benefits_expense_cr_standalone.sum(), 1), unit="Rs crore", source="firm_median_pay.csv; includes onsite staff pay"),
    dict(item="Six listed IT firms: headcount (as reported)", fy="2025-26",
         value=int(it[it.fiscal_year == "FY2025-26"].headcount_total.sum()), unit="persons", source="firm_median_pay.csv"),
    dict(item="Computer & related services: share of company gross tax payable", fy="2023-24 (returns)", value=10.9, unit="%", source="Tax agent: data/tax/corporate_tax_by_industry_FY2023-24.csv (Receipt Budget 2026-27 Annex-7 appendix)"),
]
pd.DataFrame(macro).to_csv(OUT / "it_services_macro.csv", index=False)
print(pd.DataFrame(macro)[["item", "fy", "value", "unit"]].to_string())
