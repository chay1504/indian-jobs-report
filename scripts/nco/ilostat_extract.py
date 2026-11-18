"""Extract tidy India occupation/activity/earnings/education/informality/hours series
from the ILOSTAT bulk file for India (annual), downloaded from
  https://rplumber.ilo.org/data/ref_area/?id=IND_A&format=.csv
plus quarterly EMP_TEMP_SEX_OCU_NB from
  https://rplumber.ilo.org/data/indicator/?id=EMP_TEMP_SEX_OCU_NB_Q&ref_area=IND&format=.csv

Output: data/ilostat/*.csv with columns
  indicator, indicator_label, year, sex, classif1, classif1_label, classif2, classif2_label,
  value, unit, obs_status, source, source_label, ref_period, source_url
Run:  .venv/Scripts/python.exe -I scripts/nco/ilostat_extract.py
"""
import pandas as pd
from pathlib import Path

ROOT = Path(r"C:\Users\hp\Downloads\xyz\india_jobs")
RAW = ROOT / "data" / "raw" / "nco" / "ilostat"
OUT = ROOT / "data" / "ilostat"
OUT.mkdir(parents=True, exist_ok=True)

BULK_URL = "https://rplumber.ilo.org/data/ref_area/?id=IND_A&format=.csv"
IND_URL = "https://rplumber.ilo.org/data/indicator/?id={id}&ref_area=IND&format=.csv"

rd = lambda f: pd.read_csv(RAW / f, dtype=str, encoding="utf-8-sig")
df = rd("IND_A_all.csv")
dic_ind = rd("dic_indicator.csv").drop_duplicates("indicator").set_index("indicator")
c1 = rd("dic_classif1.csv").drop_duplicates("classif1").set_index("classif1")["classif1.label"]
c2 = rd("dic_classif2.csv").drop_duplicates("classif2").set_index("classif2")["classif2.label"]
src = rd("dic_source.csv")
src = src[src.ref_area == "IND"].drop_duplicates("source").set_index("source")["source.label"]
obs = rd("dic_obs_status.csv").set_index("obs_status")["obs_status.label"]

# Reference periods (verified: ILOSTAT annual PLFS value == mean of the 4 calendar quarters, e.g. 2022)
NSS_ROUNDS = {"1994": "NSS 50th round, Jul 1993-Jun 1994", "2000": "NSS 55th round, Jul 1999-Jun 2000",
              "2005": "NSS 61st round, Jul 2004-Jun 2005", "2010": "NSS 66th round, Jul 2009-Jun 2010",
              "2012": "NSS 68th round, Jul 2011-Jun 2012"}


def ref_period(row):
    if row["source"] == "BA:14121":
        if "Q" in row["time"]:
            return f"PLFS, calendar quarter {row['time']} (ILO microdata processing)"
        return f"PLFS, calendar year Jan-Dec {row['time']} (average of 4 quarterly estimates; ILO microdata processing)"
    if row["source"] == "XA:1976":
        return ("ILO modelled estimates, Nov. 2025 vintage (harmonised ISCO-08 / ISIC4 series; "
                + ("PROJECTION" if int(row["time"][:4]) >= 2026 else "modelled estimate") + ")")
    if row["source"] == "BX:2228":
        return NSS_ROUNDS.get(row["time"], "NSS Employment-Unemployment Survey") + " (ILO microdata processing)"
    return ""


def unit_of(ind, cls1, cls2):
    tok = ind.split("_")[1]
    per = "per hour" if (tok[1:3] == "HR" or ind.startswith("SDG_0851")) else "per month"
    if ind.startswith(("EAR_EMTG", "EAR_EHRG")):
        return "Gini index"
    if ind.endswith("_RT"):
        return "%"
    cur = next((c for c in (cls1, cls2) if isinstance(c, str) and c.startswith("CUR_TYPE")), None)
    if cur:
        cls2 = cur
        cur = {"CUR_TYPE_LCU": "INR (current)", "CUR_TYPE_USD": "USD (current, market exchange rate)",
               "CUR_TYPE_PPP": "2021 PPP $"}[cls2]
        return f"{cur} {per}"
    if ind.startswith(("EAR_", "SDG_0851")):
        return f"INR (current) {per}"
    if ind not in dic_ind.index:
        return ""
    um, mult = dic_ind.at[ind, "indicator.unit_measure"], dic_ind.at[ind, "indicator.unit_mult"]
    if um == "persons":
        return f"persons ({mult})"
    if ind.startswith("HOW_"):
        return "hours per week (average, actually worked)"
    return um


def tidy(sub, url):
    sub = sub.copy()
    out = pd.DataFrame({
        "indicator": sub["indicator"],
        "indicator_label": sub["indicator"].map(lambda i: dic_ind.at[i, "indicator.label"] if i in dic_ind.index else ""),
        "year": sub["time"],
        "sex": sub["sex"],
        "classif1": sub["classif1"],
        "classif1_label": sub["classif1"].map(c1),
        "classif2": sub.get("classif2"),
        "classif2_label": sub.get("classif2").map(c2) if "classif2" in sub else None,
        "value": pd.to_numeric(sub["obs_value"], errors="coerce"),
        "unit": [unit_of(i, j, k) for i, j, k in zip(sub["indicator"], sub["classif1"], sub["classif2"])],
        "obs_status": sub["obs_status"].map(obs).fillna(""),
        "source": sub["source"],
        "source_label": sub["source"].map(src),
        "ref_period": sub.apply(ref_period, axis=1),
        "source_url": [url.format(id=i + ("_Q" if "Q" in t else "_A")) for i, t in zip(sub["indicator"], sub["time"])],
    })
    return out.sort_values(["indicator", "source", "year", "sex", "classif1", "classif2"], na_position="first")


GROUPS = {
    "emp_by_occupation.csv": ["EMP_TEMP_SEX_OCU_NB", "EMP_TEMP_SEX_OC2_NB", "EES_TEES_SEX_OCU_NB", "EES_TEES_SEX_OC2_NB",
                              "EMP_TEMP_SEX_STE_OCU_NB", "EMP_TEMP_SEX_OCU_GEO_NB", "EMP_STEM_SEX_OC2_NB",
                              "EMP_STEM_SEX_OCU_NB", "EMP_CARE_SEX_OC2_NB"],
    "emp_by_activity.csv": ["EMP_TEMP_SEX_ECO_NB", "EMP_TEMP_SEX_EC2_NB", "EES_TEES_SEX_EC2_NB", "EES_TEES_SEX_ECO_NB",
                            "EMP_TEMP_SEX_STE_EC2_NB"],
    "emp_occupation_x_activity.csv": ["EMP_TEMP_ECO_OCU_NB", "EMP_TEMP_SEX_OCU_EC2_NB"],
    "earnings.csv": None,  # all EAR_* + SDG_0851
    "education_by_occupation.csv": ["EMP_TEMP_SEX_OCU_EDU_NB", "EES_TEES_SEX_OCU_EDU_NB", "EMP_TEMP_SEX_EDU_EC2_NB",
                                    "EMP_TEMP_SEX_ECO_EDU_NB"],
    "informality_by_occupation.csv": ["EMP_NIFL_SEX_OCU_NB", "EMP_NIFL_SEX_OCU_RT", "EMP_NIFL_SEX_OC2_NB",
                                      "EMP_NIFL_SEX_OC2_RT", "EMP_NIFL_SEX_EC2_NB", "EMP_NIFL_SEX_EC2_RT",
                                      "EMP_TEMP_SEX_IFL_OCU_NB", "EMP_NIFL_SEX_OCU_EDU_RT"],
    "hours_by_occupation.csv": ["HOW_TEMP_SEX_OCU_NB", "HOW_TEMP_SEX_OC2_NB", "HOW_XEES_SEX_OCU_NB",
                                "HOW_XEES_SEX_OC2_NB", "HOW_TEMP_SEX_EC2_NB", "HOW_XEES_SEX_EC2_NB"],
}

MODELLED = ["EMP_2EMP_SEX_OCU_NB", "EMP_2EMP_SEX_ECO_NB", "EMP_2EMP_SEX_AGE_NB", "EMP_2EMP_SEX_STE_NB"]
summary = []
for fname, inds in GROUPS.items():
    if inds is None:
        mask = df.indicator.str.startswith("EAR_") | (df.indicator == "SDG_0851_SEX_OCU_NB")
    else:
        mask = df.indicator.isin(inds)
    sub = df[mask & df.source.isin(["BA:14121", "BX:2228"])]
    t = tidy(sub, IND_URL)
    t.to_csv(OUT / f"ilostat_ind_{fname}", index=False, encoding="utf-8")
    summary.append((fname, len(t), sorted(t.indicator.unique())))

# ILO modelled estimates (harmonised; incl. 2026-2027 projections of total employment)
sub = df[df.indicator.isin(MODELLED) & (df.source == "XA:1976")]
tm = tidy(sub, IND_URL)
tm.to_csv(OUT / "ilostat_ind_modelled_estimates.csv", index=False, encoding="utf-8")
summary.append(("modelled_estimates.csv", len(tm), sorted(tm.indicator.unique())))

# Quarterly major-group employment (PLFS, 2017Q3 onwards)
q = rd("IND_Q_EMP_TEMP_SEX_OCU_NB.csv")
q["classif2"] = None
tq = tidy(q, IND_URL)
tq.to_csv(OUT / "ilostat_ind_emp_by_occupation_quarterly.csv", index=False, encoding="utf-8")
summary.append(("emp_by_occupation_quarterly.csv", len(tq), ["EMP_TEMP_SEX_OCU_NB (quarterly)"]))

# Catalogue of every India indicator with an occupation / activity / education breakdown
df["c1p"] = df.classif1.fillna("").str.split("_").str[:2].str.join("_")
df["c2p"] = df.classif2.fillna("").str.split("_").str[:2].str.join("_")
cat = df.groupby(["indicator", "source"]).agg(
    years=("time", lambda s: " ".join(sorted(set(s)))),
    classif1_types=("c1p", lambda s: "|".join(sorted(set(s) - {""}))),
    classif2_types=("c2p", lambda s: "|".join(sorted(set(s) - {""}))),
    n_obs=("time", "size")).reset_index()
cat["indicator_label"] = cat.indicator.map(lambda i: dic_ind.at[i, "indicator.label"] if i in dic_ind.index else "")
cat["source_label"] = cat.source.map(src)
cat["source_url"] = cat.indicator.map(lambda i: IND_URL.format(id=i + "_A"))
cat = cat[cat.classif1_types.str.contains("OCU|OC2|ECO|EC2|EDU") | cat.classif2_types.str.contains("OCU|OC2|ECO|EC2|EDU")]
cat.to_csv(OUT / "ilostat_ind_catalogue.csv", index=False, encoding="utf-8")
summary.append(("catalogue.csv", len(cat), []))

for s in summary:
    print(s[0], s[1], s[2])
