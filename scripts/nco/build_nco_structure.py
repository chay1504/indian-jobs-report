"""Build data/nco/nco2015_structure.csv (+ comparison with ISCO-08) from the parsed NCO-2015 volumes.

Inputs (run parse_nco_vol1.py / parse_nco_vol2.py first, output into a scratch dir):
  <scratch>/nco_vol2_parsed.csv  (Vol II-A/II-B descriptions; primary source for titles + descriptions)
  <scratch>/nco_vol1_parsed.csv  (Vol I concordance; NCO-2004 equivalents; fills gaps)
  data/raw/nco/insee_nomenclature_N{1..4}_ISCO.xlsx  (official ISCO-08 code lists, via INSEE
       https://www.insee.fr/fr/information/7749176 - used for codes only; titles are French)
  data/raw/nco/ilostat/dic_classif1.csv  (English ISCO-08 1- and 2-digit labels from ILOSTAT)
Run: python -I build_nco_structure.py <scratch_dir>
"""
import sys, re
from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\hp\Downloads\xyz\india_jobs")
SCR = Path(sys.argv[1])
OUT = ROOT / "data" / "nco"
OUT.mkdir(parents=True, exist_ok=True)

v2 = pd.read_csv(SCR / "nco_vol2_parsed.csv", dtype=str).fillna("")
v1 = pd.read_csv(SCR / "nco_vol1_parsed.csv", dtype=str).fillna("")
v1 = v1[v1.code != ""]

LEVELS = ["division", "sub_division", "group", "family", "occupation"]
ISCO = {}
for n, l in zip(range(1, 5), LEVELS):
    x = pd.read_excel(ROOT / "data" / "raw" / "nco" / f"insee_nomenclature_N{n}_ISCO.xlsx", dtype=str)
    ISCO[l] = set(x.iloc[:, 0].str.strip())
dic = pd.read_csv(ROOT / "data" / "raw" / "nco" / "ilostat" / "dic_classif1.csv", dtype=str, encoding="utf-8-sig")
isco_en = {}
for _, r in dic.iterrows():
    m = re.match(r"^(OCU|OC2)_ISCO08_(\d+)$", r["classif1"])
    if m:
        isco_en[m.group(2)] = re.sub(r"^.*?:\s*(\d+\s*[-.]\s*)?", "", r["classif1.label"])

# ---- base table: Vol II, de-duplicated by (level, code)
v2["source"] = "NCO-2015 Vol " + v2["volume"] + " PDF p." + v2["page"]
base = v2.drop_duplicates(["level", "code"], keep="first").copy()

# ---- add hierarchy entries present only in Vol I (e.g. Group 343 has no heading in Vol II)
v1["source"] = "NCO-2015 Vol I (concordance) PDF p." + v1["page"]
key2 = set(zip(base.level, base.code))
extra = v1[[(l, c) not in key2 for l, c in zip(v1.level, v1.code)]].copy()
extra = extra[extra.code.str.fullmatch(r"\d{1,4}|\d{4}\.\d{4}")]
for c in ["description", "isco08_code", "isco08_title", "qp_nos"]:
    extra[c] = ""
base = pd.concat([base, extra[base.columns.intersection(extra.columns)]], ignore_index=True).fillna("")
base["note"] = ""
# an "ISCO 08 Unit Group Details" block printed in non-bold type ends up in the description: move it out
pat = r"\s*ISCO\s*08\s*Unit\s*Group\s*Details:?\s*Code\s*(\d{4})\s*Title\s*(.*)$"
ext = base["description"].str.extract(pat)
hit = ext[0].notna()
base.loc[hit & (base.isco08_code == ""), "isco08_code"] = ext.loc[hit & (base.isco08_code == ""), 0]
base.loc[hit & (base.isco08_title == ""), "isco08_title"] = ext.loc[hit & (base.isco08_title == ""), 1]
base.loc[hit, "description"] = base.loc[hit, "description"].str.replace(pat, "", regex=True)
# Known source inconsistencies (documented, not silently fixed):
# Vol II-A p.373 prints "3127.9900" (no family 3127 exists); Vol I concordance p.106 lists the same title as 3123.9900.
m27 = base.code == "3127.9900"
if m27.any() and (base.code == "3123.9900").any():
    i23 = base.index[base.code == "3123.9900"][0]
    base.loc[i23, "description"] = base.loc[m27, "description"].iloc[0]
    base.loc[i23, "isco08_code"] = base.loc[m27, "isco08_code"].iloc[0]
    base.loc[i23, "note"] = "Vol II-A (PDF p.373) prints this code as 3127.9900; Vol I concordance (PDF p.106) gives 3123.9900"
    base.loc[i23, "source"] += "; description from Vol II-A p.373"
    base = base[~m27]
base.loc[base.code == "8190.0100", "note"] = "Listed only in Vol I concordance; family 8190 is not defined in NCO-2015"
base.loc[base.code == "343", "note"] = ("Group heading absent from Vol II; Vol I (PDF p.124) titles it 'Administrative Associate "
                                        "Professionals' (ISCO-08 343 = Artistic, cultural and culinary associate professionals)")
base = base.reset_index(drop=True)

# ---- fill empty titles from Vol I; attach NCO-2004 equivalents
t1 = dict(zip(zip(v1.level, v1.code), v1.title))
n04 = dict(zip(zip(v1.level, v1.code), v1.nco2004))
base["title"] = [t if t else t1.get((l, c), "") for l, c, t in zip(base.level, base.code, base.title)]
base["nco2004_code"] = [n04.get((l, c), "").replace("`", "").strip() for l, c in zip(base.level, base.code)]

# ---- hierarchy columns
def parents(code, level):
    d = code.replace(".", "")
    return dict(division=d[:1], sub_division=d[:2] if level != "division" else "",
                group=d[:3] if level in ("group", "family", "occupation") else "",
                family=d[:4] if level in ("family", "occupation") else "")

par = pd.DataFrame([parents(c, l) for c, l in zip(base.code, base.level)])
base = pd.concat([base.reset_index(drop=True), par], axis=1)
base["parent_code"] = [
    {"division": "", "sub_division": dv, "group": sd, "family": gr, "occupation": fm}[l]
    for l, dv, sd, gr, fm in zip(base.level, base.division, base.sub_division, base.group, base.family)]

# ---- ISCO-08 mapping
iscol = []
for l, c, stated, fam in zip(base.level, base.code, base.isco08_code, base.family):
    if l != "occupation":
        if c in ISCO[l]:
            iscol.append((c, "identical code in ISCO-08"))
        else:
            iscol.append(("", "NCO-specific: no ISCO-08 equivalent code"))
    else:
        s = stated.strip()
        if re.fullmatch(r"\d{4}", s) and s in ISCO["family"]:
            iscol.append((s, "stated in NCO Vol II (ISCO 08 Unit Group Details)"
                          + ("" if s == fam else "; differs from NCO family")))
        elif fam in ISCO["family"]:
            iscol.append((fam, "inferred from NCO family (Vol II detail missing/unparseable)"))
        else:
            iscol.append(("", "NCO-specific family: no ISCO-08 equivalent"))
base["isco08_code"], base["isco08_match"] = zip(*iscol)
base["isco08_title_en"] = [isco_en.get(c, "") if len(c) <= 2 else "" for c in base.isco08_code]
base.loc[base.level == "occupation", "isco08_title_en"] = base.loc[base.level == "occupation", "isco08_title"]

# ---- skill level by division (NCO-2015 Vol I, p.19 table)
SKILL = {"1": "Not defined", "2": "IV", "3": "III", "4": "II", "5": "II", "6": "II", "7": "II", "8": "II", "9": "I"}
base["nco_skill_level"] = base.division.map(SKILL)

base["level_rank"] = base.level.map({l: i for i, l in enumerate(LEVELS)})
base["sortkey"] = base.code.str.replace(".", "", regex=False).str.ljust(12, "0") + base.level_rank.astype(str)
base = base.sort_values(["sortkey"]).reset_index(drop=True)
cols = ["code", "level", "title", "description", "isco08_code", "isco08_match", "isco08_title_en", "parent_code",
        "division", "sub_division", "group", "family", "nco_skill_level", "nco2004_code", "qp_nos", "source", "note"]
base[cols].to_csv(OUT / "nco2015_structure.csv", index=False, encoding="utf-8")
print(base.level.value_counts().reindex(LEVELS))
print(base.isco08_match.value_counts())

# ---- comparison table NCO-2015 vs ISCO-08 (codes)
rows = []
for l in LEVELS[:4]:
    nco = set(base[base.level == l].code)
    for c in sorted(nco - ISCO[l]):
        rows.append(dict(level=l, code=c, in_nco2015=True, in_isco08=False,
                         nco_title=base[(base.level == l) & (base.code == c)].title.iloc[0]))
    for c in sorted(ISCO[l] - nco):
        rows.append(dict(level=l, code=c, in_nco2015=False, in_isco08=True, nco_title=""))
    rows.append(dict(level=l, code=f"COUNT nco={len(nco)} isco={len(ISCO[l])} common={len(nco & ISCO[l])}",
                     in_nco2015="", in_isco08="", nco_title=""))
pd.DataFrame(rows).to_csv(OUT / "nco2015_vs_isco08_code_differences.csv", index=False, encoding="utf-8")
print(pd.DataFrame(rows).to_string())

# ---- occupations whose stated ISCO-08 unit group differs from their NCO family
occ = base[base.level == "occupation"]
diff = occ[occ.isco08_match.str.contains("differs")]
diff[["code", "title", "family", "isco08_code", "isco08_title_en", "source"]].to_csv(
    OUT / "nco2015_occupations_mapped_to_other_isco08_unit.csv", index=False, encoding="utf-8")
print("occupations mapped to a different ISCO-08 unit group:", len(diff))
