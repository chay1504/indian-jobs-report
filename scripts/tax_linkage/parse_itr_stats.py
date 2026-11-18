"""Parse CBDT 'Income Tax Return Statistics AY 2023-24' (v1.0, June 2024).

Outputs (data/tax_linkage/):
  cbdt_itr_ay2023-24_individual_income_heads_by_range.csv  (tables 2.1, 2.2, 2.4, 2.10, 2.11)
  cbdt_itr_ay2023-24_business_codes.csv                    (table 7.1)
Source PDF: https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Approved-version-Income-Tax-Return-Statistics-for-the-AY-2023-24.pdf
"""
import re
import sys
from pathlib import Path

import pandas as pd
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "data/raw/tax_linkage/cbdt_itr_stats_AY2023-24.pdf"
OUT = ROOT / "data/tax_linkage"
OUT.mkdir(parents=True, exist_ok=True)

doc = pymupdf.open(PDF)
NUM = re.compile(r"^-?[\d,]+(\.\d+)?$")


def num(s):
    s = s.strip()
    if s in ("-", ""):
        return 0.0
    return float(s.replace(",", ""))


# ---------- range tables (individuals) ----------
RANGE_TABLES = {  # page index (0-based) -> (table id, value column name)
    20: ("2.1", "gross_total_income"),
    21: ("2.2", "salary_income"),
    23: ("2.4", "business_income"),
    29: ("2.10", "returned_income"),
    30: ("2.11", "tax_payable"),
}


def parse_range_table(pidx):
    raw = [l.strip() for l in doc[pidx].get_text().split("\n")]
    lines = []
    for l in raw:  # some rows have two numbers on one text line
        toks = l.split()
        if len(toks) > 1 and all(NUM.match(t) or t == "-" for t in toks):
            lines.extend(toks)
        else:
            lines.append(l)
    rows = []
    i = 0
    while i < len(lines):
        l = lines[i]
        if (l.startswith(">") or l.startswith("<") or l.startswith("=")) and not l.startswith("=>"):
            label = l
            vals = []
            j = i + 1
            while j < len(lines) and len(vals) < 3 and (NUM.match(lines[j]) or lines[j] == "-"):
                vals.append(lines[j])
                j += 1
            if len(vals) == 3:
                rows.append((label, num(vals[0]), num(vals[1]), num(vals[2])))
                i = j
                continue
        i += 1
    return rows


frames = []
for pidx, (tid, col) in RANGE_TABLES.items():
    for order, (label, n, s, avg) in enumerate(parse_range_table(pidx)):
        frames.append(dict(table=tid, measure=col, row_order=order, range_inr=label,
                           n_returns=int(n), sum_crore=s, avg_lakh=avg))
rng = pd.DataFrame(frames)
rng["source"] = "CBDT Income Tax Return Statistics AY2023-24 v1.0 (June 2024), Individuals, table " + rng["table"] + f", PDF p.{''}"
rng["source"] = rng.apply(lambda r: f"CBDT ITR Statistics AY2023-24 v1.0, table {r.table} (PDF p.{[k+1 for k,v in RANGE_TABLES.items() if v[0]==r.table][0]})", axis=1)
rng.to_csv(OUT / "cbdt_itr_ay2023-24_individual_income_heads_by_range.csv", index=False)
for tid, g in rng.groupby("table"):
    print(tid, len(g), "rows; n_returns total", g.n_returns.sum(), "sum_crore", round(g.sum_crore.sum(), 2))

# ---------- type of business table 7.1 ----------
recs = []
for pidx in range(76, doc.page_count):
    words = doc[pidx].get_text("words")
    words = [w for w in words if w[1] > 100 and w[1] < 780]  # skip header/footer
    codes = [w for w in words if w[0] < 100 and re.fullmatch(r"\d{1,5}", w[4])]
    if not codes:
        continue
    rows = {c[1]: dict(code=c[4], desc=[], corp=None, noncorp=None, total=None) for c in codes}
    ys = sorted(rows)
    for w in words:
        x0, y0, x1, y1, t = w[:5]
        if x0 < 100:
            continue
        if y0 < ys[0] - 15:  # header rows
            continue
        # nearest code row by y
        y = min(ys, key=lambda yy: abs(yy - y0))
        if x1 > 340 and NUM.match(t):
            if x1 <= 395:
                rows[y]["corp"] = num(t)
            elif x1 <= 455:
                rows[y]["noncorp"] = num(t)
            else:
                rows[y]["total"] = num(t)
        elif x0 < 320:
            rows[y]["desc"].append((y0, x0, t))
    for y in ys:
        r = rows[y]
        desc = " ".join(t for _, _, t in sorted(r["desc"]))
        recs.append(dict(code=r["code"], type_of_business=desc,
                         corporate_taxpayers=r["corp"] or 0, noncorporate_taxpayers=r["noncorp"] or 0,
                         total_taxpayers=r["total"] or 0, pdf_page=pidx + 1))
biz = pd.DataFrame(recs)
# descriptions: word-position assignment mixes adjacent multi-line names, so take them from pdfplumber cells
import pdfplumber
desc_map = {}
with pdfplumber.open(PDF) as pl:
    for pidx in range(76, doc.page_count):
        for tbl in pl.pages[pidx].extract_tables():
            for row in tbl:
                if row and row[0] and re.fullmatch(r"\d{1,5}", str(row[0]).strip()) and row[1]:
                    desc_map[str(row[0]).strip()] = " ".join(str(row[1]).split())
biz["type_of_business"] = biz.code.astype(str).map(desc_map).fillna(biz.type_of_business)
print("descriptions from pdfplumber:", biz.code.astype(str).isin(desc_map.keys()).sum(), "of", len(biz))
biz["sector"] = biz.type_of_business.str.split("-").str[0].str.strip()
bad = biz[(biz.corporate_taxpayers + biz.noncorporate_taxpayers - biz.total_taxpayers).abs() > 0]
print("business codes:", len(biz), "rows; rows where corp+noncorp != total:", len(bad))
if len(bad):
    print(bad.head(20).to_string())
biz["source"] = "CBDT ITR Statistics AY2023-24 v1.0, table 7.1 Type of Business (counts of returns by nature-of-business code)"
biz.to_csv(OUT / "cbdt_itr_ay2023-24_business_codes.csv", index=False)
print(biz.total_taxpayers.sum(), biz.corporate_taxpayers.sum(), biz.noncorporate_taxpayers.sum())
