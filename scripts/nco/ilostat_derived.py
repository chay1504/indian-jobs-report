"""Derived India tables from the tidy ILOSTAT extracts (data/ilostat/ilostat_ind_*.csv).
All values: ILOSTAT, source BA:14121 = PLFS (ILO microdata processing), calendar-year averages of quarterly
estimates, employment in thousands, earnings in current INR per month (employees only).

Outputs (data/ilostat/):
  derived_isco08_2digit_profile.csv  ISCO-08 sub-major groups, 2022-2025: employment (T/M/F), employees,
                                      informality rate, weekly hours, change & CAGR 2022->2025, and the
                                      parent major-group mean/median monthly earnings (major-group level only!)
  derived_major_group_profile.csv    ISCO major groups x year 2018-2025: employment, earnings, education shares,
                                      informality, hours (ISCO-88 basis 2018-2020, ISCO-08 basis 2022-2025)
  derived_isic4_2digit_growth.csv     ISIC Rev.4 divisions (= NIC-2008 2-digit), employment 2018-2025, change/CAGR
  derived_skill_level_growth.csv      ILO skill-level groups, 2018-2025 (only occupation series without a break)
Run: python -I ilostat_derived.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

D = Path(r"C:\Users\hp\Downloads\xyz\india_jobs\data\ilostat")
rd = lambda f: pd.read_csv(D / f, dtype={"year": str})
occ, act, ear, edu, ifl, how = (rd("ilostat_ind_emp_by_occupation.csv"), rd("ilostat_ind_emp_by_activity.csv"),
                                rd("ilostat_ind_earnings.csv"), rd("ilostat_ind_education_by_occupation.csv"),
                                rd("ilostat_ind_informality_by_occupation.csv"), rd("ilostat_ind_hours_by_occupation.csv"))
PLFS = "BA:14121"
URL = "https://rplumber.ilo.org/data/indicator/?id={}_A&ref_area=IND&format=.csv"


def series(df, ind, sex="SEX_T", c2=None):
    x = df[(df.indicator == ind) & (df.source == PLFS) & (df.sex == sex)]
    if c2 is not None:
        x = x[x.classif2 == c2]
    return x.set_index(["classif1", "year"])["value"]


def cagr(a, b, n):
    return np.where((a > 0) & (b > 0), (b / a) ** (1 / n) - 1, np.nan)


# ---------------- ISCO-08 2-digit profile (2022-2025) ----------------
Y2 = ["2022", "2023", "2024", "2025"]
emp = series(occ, "EMP_TEMP_SEX_OC2_NB").unstack("year")
emp = emp[emp.index.str.startswith("OC2_ISCO08")][Y2]
lab = occ.drop_duplicates("classif1").set_index("classif1")["classif1_label"]
prof = pd.DataFrame({"isco08_2d": emp.index.str.replace("OC2_ISCO08_", ""),
                     "title": emp.index.map(lab).str.replace(r"^.*?: \S+ - ", "", regex=True)}, index=emp.index)
for y in Y2:
    prof[f"emp_{y}_thou"] = emp[y]
for s, tag in [("SEX_M", "male"), ("SEX_F", "female")]:
    prof[f"emp_2025_{tag}_thou"] = series(occ, "EMP_TEMP_SEX_OC2_NB", s).unstack("year").reindex(emp.index)["2025"]
prof["employees_2025_thou"] = series(occ, "EES_TEES_SEX_OC2_NB").unstack("year").reindex(emp.index)["2025"]
prof["employee_share_2025_pct"] = 100 * prof.employees_2025_thou / prof.emp_2025_thou
prof["informal_rate_2025_pct"] = series(ifl, "EMP_NIFL_SEX_OC2_RT").unstack("year").reindex(emp.index)["2025"]
prof["hours_week_2025"] = series(how, "HOW_TEMP_SEX_OC2_NB").unstack("year").reindex(emp.index)["2025"]
prof["share_of_total_2025_pct"] = 100 * prof.emp_2025_thou / prof.loc["OC2_ISCO08_TOTAL", "emp_2025_thou"]
prof["change_2022_2025_thou"] = prof.emp_2025_thou - prof.emp_2022_thou
prof["change_2022_2025_pct"] = 100 * (prof.emp_2025_thou / prof.emp_2022_thou - 1)
prof["cagr_2022_2025_pct"] = 100 * cagr(prof.emp_2022_thou, prof.emp_2025_thou, 3)
# 3-year average level, less noisy for small groups
prof["emp_avg_2023_2025_thou"] = prof[[f"emp_{y}_thou" for y in ["2023", "2024", "2025"]]].mean(axis=1)
# earnings exist only at major-group level -> attach parent major-group values, clearly labelled
mg = prof.isco08_2d.str[:1]
for ind, tag in [("EAR_EMTA_SEX_OCU_NB", "mean"), ("EAR_EMTM_SEX_OCU_NB", "median")]:
    e = series(ear, ind).unstack("year")
    prof[f"majorgroup_{tag}_monthly_earnings_inr_2025"] = ["" if c == "T" else e.get("2025", {}).get(f"OCU_ISCO08_{c}", np.nan)
                                                         for c in mg]
prof.loc["OC2_ISCO08_TOTAL", ["isco08_2d", "title"]] = ["TOTAL", "Total"]
prof["source"] = ("ILOSTAT (PLFS microdata, ILO processing); EMP_TEMP_SEX_OC2_NB, EES_TEES_SEX_OC2_NB, "
                  "EMP_NIFL_SEX_OC2_RT, HOW_TEMP_SEX_OC2_NB, EAR_EMTA/EMTM_SEX_OCU_NB")
prof["note"] = ""
prof.loc[prof.isco08_2d.isin(["11", "12"]), "note"] = ("NCO-2015 codes 'working proprietors' of businesses to family 1120 "
                                                      "(Managing directors and chief executives); series volatile")
prof.round(3).to_csv(D / "derived_isco08_2digit_profile.csv", index=False)
chk = prof.drop("OC2_ISCO08_TOTAL")[[f"emp_{y}_thou" for y in Y2]].sum() - prof.loc["OC2_ISCO08_TOTAL", [f"emp_{y}_thou" for y in Y2]]
print("2-digit sum minus total (thousands):", chk.round(1).to_dict())

# ---------------- major group profile (2018-2025) ----------------
YA = [str(y) for y in range(2018, 2026)]
rows = []
e_all = series(occ, "EMP_TEMP_SEX_OCU_NB").unstack("year")
mean_e = series(ear, "EAR_EMTA_SEX_OCU_NB").unstack("year")
med_e = series(ear, "EAR_EMTM_SEX_OCU_NB").unstack("year")
infr = series(ifl, "EMP_NIFL_SEX_OCU_RT").unstack("year")
hrs = series(how, "HOW_TEMP_SEX_OCU_NB").unstack("year")
ees = series(occ, "EES_TEES_SEX_OCU_NB").unstack("year")
ed = edu[(edu.indicator == "EMP_TEMP_SEX_OCU_EDU_NB") & (edu.source == PLFS) & (edu.sex == "SEX_T")]
edp = ed.pivot_table(index=["classif1", "year"], columns="classif2", values="value")
EDU = {"below_primary(X+0)": ["EDU_ISCED97_X", "EDU_ISCED97_0"], "primary(1)": ["EDU_ISCED97_1"],
       "lower_secondary(2)": ["EDU_ISCED97_2"], "upper_secondary(3)": ["EDU_ISCED97_3"],
       "post_secondary_nontertiary(4)": ["EDU_ISCED97_4"], "tertiary_first_stage(5)": ["EDU_ISCED97_5"],
       "tertiary_second_stage(6)": ["EDU_ISCED97_6"], "tertiary_total(5+6)": ["EDU_ISCED97_5", "EDU_ISCED97_6"],
       "level_not_stated": ["EDU_ISCED97_UNK"]}
for c in e_all.index:
    if not (c.startswith("OCU_ISCO08") or c.startswith("OCU_ISCO88") or c.startswith("OCU_SKILL")):
        continue
    for y in YA:
        v = e_all.loc[c].get(y, np.nan)
        if pd.isna(v):
            continue
        r = dict(classif1=c, classif1_label=lab.get(c, ""), year=y, emp_thou=v,
                 employees_thou=ees.loc[c].get(y, np.nan) if c in ees.index else np.nan,
                 mean_monthly_earnings_inr=mean_e.loc[c].get(y, np.nan) if c in mean_e.index else np.nan,
                 median_monthly_earnings_inr=med_e.loc[c].get(y, np.nan) if c in med_e.index else np.nan,
                 informal_rate_pct=infr.loc[c].get(y, np.nan) if c in infr.index else np.nan,
                 hours_week=hrs.loc[c].get(y, np.nan) if c in hrs.index else np.nan)
        tot = edp.loc[(c, y), "EDU_ISCED97_TOTAL"] if (c, y) in edp.index else np.nan
        for k, cols in EDU.items():
            r[f"edu_share_{k}_pct"] = (100 * sum(edp.loc[(c, y)].get(cc, 0) if not pd.isna(edp.loc[(c, y)].get(cc, np.nan)) else 0
                                                 for cc in cols) / tot) if (c, y) in edp.index else np.nan
        rows.append(r)
mgp = pd.DataFrame(rows)
mgp["classification"] = np.where(mgp.classif1.str.startswith("OCU_ISCO88"), "ISCO-88 (PLFS coded NCO-2004)",
                        np.where(mgp.classif1.str.startswith("OCU_ISCO08"), "ISCO-08 (PLFS coded NCO-2015)",
                                 "ILO skill level (comparable across the 2021 break)"))
mgp["source"] = "ILOSTAT (PLFS microdata, ILO processing): " + ", ".join(
    ["EMP_TEMP_SEX_OCU_NB", "EES_TEES_SEX_OCU_NB", "EAR_EMTA_SEX_OCU_NB", "EAR_EMTM_SEX_OCU_NB",
     "EMP_NIFL_SEX_OCU_RT", "HOW_TEMP_SEX_OCU_NB", "EMP_TEMP_SEX_OCU_EDU_NB"])
mgp.round(3).to_csv(D / "derived_major_group_profile.csv", index=False)

# ---------------- skill level growth 2018 -> 2025 ----------------
sk = e_all[e_all.index.str.startswith("OCU_SKILL")][YA]
sk = sk.assign(label=sk.index.map(lab), change_2018_2025_pct=100 * (sk["2025"] / sk["2018"] - 1),
               cagr_2018_2025_pct=100 * cagr(sk["2018"], sk["2025"], 7))
sk.round(3).to_csv(D / "derived_skill_level_growth.csv")

# ---------------- ISIC Rev.4 2-digit growth (2018 -> 2025) ----------------
ec = series(act, "EMP_TEMP_SEX_EC2_NB").unstack("year")[YA]
alab = act.drop_duplicates("classif1").set_index("classif1")["classif1_label"]
g = pd.DataFrame({"isic4_2d": ec.index.str.replace("EC2_ISIC4_", ""),
                  "title": ec.index.map(alab).str.replace(r"^.*?: \S+ - ", "", regex=True)}, index=ec.index)
for y in YA:
    g[f"emp_{y}_thou"] = ec[y]
g["change_2018_2025_thou"] = g.emp_2025_thou - g.emp_2018_thou
g["change_2018_2025_pct"] = 100 * (g.emp_2025_thou / g.emp_2018_thou - 1)
g["cagr_2018_2025_pct"] = 100 * cagr(g.emp_2018_thou, g.emp_2025_thou, 7)
g["cagr_2022_2025_pct"] = 100 * cagr(g.emp_2022_thou, g.emp_2025_thou, 3)
g["share_2025_pct"] = 100 * g.emp_2025_thou / ec.loc[ec.index.str.endswith("TOTAL"), "2025"].iloc[0]
g["source"] = "ILOSTAT EMP_TEMP_SEX_EC2_NB (PLFS microdata, ILO processing; ISIC Rev.4 = NIC-2008 2-digit)"
g.round(3).to_csv(D / "derived_isic4_2digit_growth.csv", index=False)
print("done", len(prof), len(mgp), len(g))
