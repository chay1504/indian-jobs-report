"""Parse ILO WP140 (Gmyrek et al. 2025) Annex Table A1 -> ilo_isco08_scores.csv
Usage: python -I parse_ilo_wp140_tableA1.py <wp140.pdf> <out.csv>
Table A1 columns: Exposure gradient | 4-digit ISCO-08 code | Occupation name | Mean | SD
Gradient rule (WP140 Table 5): G4 mu>=0.6 & mu-sd>=0.5; G3 0.5<=mu<0.6 & mu+sd>=0.5;
G2 0.4<=mu<0.5 & mu+sd>=0.5; G1 mu<0.4 & mu+sd>=0.5; Minimal mu<0.5 & mu+sd>0.4; else Not Exposed.
"""
import sys, re, csv, pymupdf

SRC = "https://www.ilo.org/sites/default/files/2025-05/WP140_web.pdf"
pdf, out = sys.argv[1], sys.argv[2]
doc = pymupdf.open(pdf)
lines = []
for i, p in enumerate(doc):
    for ln in p.get_text().splitlines():
        lines.append((i + 1, ln.strip()))

# restrict to annex table: from 'Table A1. ISCO-08 occupations by exposure gradient' to '2. Sampling Formula'
start = next(k for k, (pg, l) in enumerate(lines) if pg >= 45 and ("Table A1. ISCO-08" in l))
end = next(k for k, (pg, l) in enumerate(lines) if k > start and l.startswith("2. Sampling Formula"))
seg = [(pg, l) for pg, l in lines[start:end] if l]

HEADERS = {"Exposure", "4-digit code", "Occupation Name", "Mean", "SD", "ILO Working Paper 140", "X",
           "X Table A1. ISCO-08 occupations by exposure gradient", "Table A1. ISCO-08 occupations by exposure gradient"}
num = re.compile(r"^\d+(\.\d+)?$")
rows, i = [], 0
cat_map = {"Gradient 4": "Gradient 4", "Gradient 3": "Gradient 3", "Gradient 2": "Gradient 2",
           "Gradient 1": "Gradient 1", "Not Exposed": "Not Exposed"}
while i < len(seg):
    pg, l = seg[i]
    cat = None
    if l in cat_map:
        cat = cat_map[l]; i += 1
    elif l == "Minimal" and i + 1 < len(seg) and seg[i + 1][1] == "Exposure":
        cat = "Minimal Exposure"; i += 2
    else:
        i += 1
        continue
    # skip page headers that might interleave
    while i < len(seg) and (seg[i][1] in HEADERS or re.fullmatch(r"\d{2}", seg[i][1])):
        i += 1
    code = seg[i][1]; assert re.fullmatch(r"\d{4}", code), (pg, code)
    i += 1
    name_parts = []
    while not num.match(seg[i][1]) or re.fullmatch(r"\d{4}", seg[i][1]) and False:
        name_parts.append(seg[i][1]); i += 1
    mean = float(seg[i][1]); sd = float(seg[i + 1][1]); i += 2
    rows.append(dict(isco08_code=code, title=" ".join(name_parts).replace("\u00ad", ""),
                     mean_score=mean, sd=sd, gradient=cat, pdf_page=pg, source_url=SRC))

# consistency check against Table 5 rule
def rule(m, s):
    if m >= 0.6 and m - s >= 0.5: return "Gradient 4"
    if 0.5 <= m < 0.6 and m + s >= 0.5: return "Gradient 3"
    if 0.4 <= m < 0.5 and m + s >= 0.5: return "Gradient 2"
    if m < 0.4 and m + s >= 0.5: return "Gradient 1"
    if m < 0.5 and m + s > 0.4: return "Minimal Exposure"
    return "Not Exposed"
mism = [(r["isco08_code"], r["mean_score"], r["sd"], r["gradient"], rule(r["mean_score"], r["sd"])) for r in rows
        if rule(r["mean_score"], r["sd"]) != r["gradient"]]
codes = [r["isco08_code"] for r in rows]
print("rows", len(rows), "unique codes", len(set(codes)))
from collections import Counter
print(Counter(r["gradient"] for r in rows))
print("rule mismatches (rounded values in table):", len(mism)); print(mism[:20])
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["isco08_code", "title", "mean_score", "sd", "gradient", "source_url", "pdf_page"])
    w.writeheader(); w.writerows(sorted(rows, key=lambda r: r["isco08_code"]))
