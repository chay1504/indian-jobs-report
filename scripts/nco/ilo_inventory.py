"""Inventory of ILOSTAT India annual data (raw bulk file IND_A_all.csv).
Lists indicators x source x years, focusing on occupation (OCU/OC2), activity (ECO/EC2), education, earnings."""
import pandas as pd, sys, re
raw = r"C:\Users\hp\Downloads\xyz\india_jobs\data\raw\nco\ilostat"
df = pd.read_csv(raw + r"\IND_A_all.csv", dtype=str, encoding="utf-8-sig")
src = pd.read_csv(raw + r"\dic_source.csv", dtype=str, encoding="utf-8-sig")
src = src[src.ref_area == "IND"].drop_duplicates("source")
#print(src.to_string())
df["c1p"] = df.classif1.fillna("").str.split("_").str[:2].str.join("_")
df["c2p"] = df.classif2.fillna("").str.split("_").str[:2].str.join("_")
g = df.groupby(["indicator", "source"]).agg(years=("time", lambda s: ",".join(sorted(set(s)))), n=("time", "size"),
     c1=("c1p", lambda s: "|".join(sorted(set(s)))), c2=("c2p", lambda s: "|".join(sorted(set(s))))).reset_index()
pat = re.compile(r"OCU|OC2|ECO|EC2|EDU|EAR|HOW|IFL|NIFL")
sel = g[g.indicator.str.contains(pat)]
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120); pd.set_option("display.max_rows", 2000)
#print(sel.to_string())
g.to_csv(sys.argv[1], index=False)
