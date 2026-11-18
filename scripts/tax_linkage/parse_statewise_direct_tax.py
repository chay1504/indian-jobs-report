"""State/UT-wise direct tax collections, CBDT Time Series Table 1.2 (FY2018-19 .. FY2023-24).

Source PDF (read-only copy downloaded by the tax agent):
  data/raw/tax/time_series_FY2000-01_to_2023-24.pdf  ("Final Approved Time Series Data 2023-24", created 22-10-2024)
  official URL: https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Final-Approved-Time-Series-Data-2023-24-English.pdf
Columns are assigned by x-position of each number relative to the FY header.
Output: data/tax_linkage/statewise_direct_tax_FY2019-FY2024.csv
"""
import re
import sys
from pathlib import Path

import pandas as pd
import pdfplumber

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "data/raw/tax/time_series_FY2000-01_to_2023-24.pdf"
OUT = ROOT / "data/tax_linkage/statewise_direct_tax_FY2019-FY2024.csv"
NUM = re.compile(r"^-?[\d,]+(\.\d+)?@?$|^-$")
FYS = ["FY2018-19", "FY2019-20", "FY2020-21", "FY2021-22", "FY2022-23", "FY2023-24"]

rows = []
with pdfplumber.open(PDF) as pdf:
    for pidx in (2, 3):  # PDF pages 3 and 4
        words = pdf.pages[pidx].extract_words(keep_blank_chars=False, use_text_flow=False)
        # header x-centres
        hdr = [w for w in words if re.match(r"^\d{4}-\d{2}", w["text"]) and "FY" in
               " ".join(x["text"] for x in words if abs(x["top"] - w["top"]) < 3 and x["x1"] <= w["x0"] + 1 and x["x0"] >= w["x0"] - 30)]
        hdr = sorted(hdr, key=lambda w: w["x0"])[:6]
        centres = [(w["x0"] + w["x1"]) / 2 for w in hdr]
        # group words into lines by 'top'
        lines = []  # cluster words into rows: same row if 'top' within 4 pt of the row's first word
        for w in sorted(words, key=lambda w: w["top"]):
            if lines and abs(w["top"] - lines[-1][0]["top"]) < 4:
                lines[-1].append(w)
            else:
                lines.append([w])
        for ws in lines:
            ws = sorted(ws, key=lambda w: w["x0"])
            label = " ".join(w["text"] for w in ws if w["x1"] < centres[0] - 40 and not NUM.match(w["text"]))
            nums = [w for w in ws if NUM.match(w["text"]) and w["x0"] > centres[0] - 60]
            if not label or not nums or label.startswith("States/UT") or label.startswith("(Rs"):
                continue
            rec = {"state_ut": label.strip(), "pdf_page": pidx + 1}
            for w in nums:
                c = (w["x0"] + w["x1"]) / 2
                j = min(range(len(centres)), key=lambda k: abs(centres[k] - c))
                v = w["text"].rstrip("@")
                rec[FYS[j]] = None if v == "-" else float(v.replace(",", ""))
            rows.append(rec)

df = pd.DataFrame(rows)
for fy in FYS:
    if fy not in df:
        df[fy] = None
df = df[["state_ut", *FYS, "pdf_page"]]
gt = df[df.state_ut.str.startswith("Grand Total")]
print(df.to_string())
if len(gt):
    for fy in FYS:
        df[f"share_{fy}_pct"] = (df[fy] / float(gt[fy].iloc[0]) * 100).round(2)
df["source"] = ("CBDT, Time Series Data FY2000-01 to FY2023-24, Table 1.2 'State and U.T. wise break-up of collection' "
                "(Rs crore); FY2018-19..2022-23 Pr.CCA CBDT (NSDL data); FY2023-24 provisional, DGIT(Systems). "
                "State = state code in taxpayer's communication address (Notes 1-2).")
df.to_csv(OUT, index=False)
print("wrote", OUT)
