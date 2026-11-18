"""Parse the DGE 'Search NCO' web listing (https://dge.gov.in/nat?page=0..6, fetched 2026-11-09) into a CSV and
compare its NCO-2015 occupation codes with those parsed from the NCO-2015 PDF volumes.
Run: python -I parse_dge_web.py
"""
import re, html, glob
import pandas as pd

ROOT = r"C:\Users\hp\Downloads\xyz\india_jobs"
rows = []
for f in sorted(glob.glob(ROOT + r"\data\raw\nco\dge_web\dge_nat_page_*.html")):
    h = open(f, encoding="utf-8").read()
    for tr in re.findall(r"<tr>(.*?)</tr>", h, flags=re.S):
        cells = dict(re.findall(r'class="views-field views-field-([a-z0-9-]+)">(.*?)</td>', tr, flags=re.S))
        if not cells:
            continue
        g = lambda k: html.unescape(re.sub(r"<[^>]+>", "", cells.get(k, ""))).strip()
        rows.append(dict(nco2015_code=g("field-nco-2015"), title=g("title"), nco2004_code=g("field-nco-2004"),
                         division=g("field-div"), sub_division=g("field-sub-div"), group=g("field-grup"),
                         family=g("field-fmly"), page=f.rsplit("_", 1)[-1].split(".")[0]))
web = pd.DataFrame(rows)
web = web.apply(lambda c: c.str.replace(r"\s+", " ", regex=True).str.strip())
web.to_csv(ROOT + r"\data\nco\nco2015_dge_web_listing.csv", index=False, encoding="utf-8")
s = pd.read_csv(ROOT + r"\data\nco\nco2015_structure.csv", dtype=str)
pdf_occ = set(s[s.level == "occupation"].code)
web_occ = set(web.nco2015_code)
print("web rows", len(web), "unique codes", len(web_occ), "pdf occupations", len(pdf_occ))
print("in web not pdf:", len(web_occ - pdf_occ), sorted(web_occ - pdf_occ)[:40])
print("in pdf not web:", len(pdf_occ - web_occ), sorted(pdf_occ - web_occ)[:40])
