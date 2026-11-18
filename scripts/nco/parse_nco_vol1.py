"""Parse the NCO-2015 Volume I concordance table (NCO-2015 code structure with NCO-2004 equivalents).

Source: https://dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_I-2015.pdf
Concordance table = printed pp. 33-238 (PDF pages 45-250). Columns (x positions): level label ~72,
code ~129, title ~203, NCO-2004 code ~455.
Run: python -I parse_nco_vol1.py <out.csv>
"""
import re, sys
import pymupdf as fitz
import pandas as pd

PDF = r"C:\Users\hp\Downloads\xyz\india_jobs\data\raw\nco\National_Classification_of_Occupations_Vol_I-2015.pdf"
LEVEL = {"Division": "division", "Sub-": "sub_division", "Sub-Division": "sub_division", "Group": "group",
         "Family": "family"}


def main(out):
    doc = fitz.open(PDF)
    rows, cur = [], None
    for pno in range(44, 251):
        spans = []
        for b in doc[pno].get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    t = s["text"].replace("\u00a0", " ").strip()
                    if not t:
                        continue
                    x0, y0 = s["bbox"][0], s["bbox"][1]
                    if y0 < 60 or y0 > 725 or t in ("NCO 2015", "NCO 2004"):
                        continue
                    spans.append((round(y0), x0, t))
        if any("ALPHABETICAL INDEX" in t for _, _, t in spans):
            break
        spans.sort()
        for y, x, t in spans:
            if x < 120:  # level label column ("Division", "Sub-", "Group", "Family")
                lab = t.split()[0]
                if lab in LEVEL:
                    if lab == "Division" and cur is not None and cur.get("_pending_sub"):
                        cur["_pending_sub"] = False
                        continue  # second half of the two-line "Sub- / Division" label
                    cur = dict(level=LEVEL[lab], code=None, title="", nco2004="", page=pno + 1, y=y,
                               _pending_sub=(lab == "Sub-"))
                    rows.append(cur)
                continue
            if x >= 410:  # NCO-2004 equivalent column
                if cur is not None:
                    cur["nco2004"] = (cur["nco2004"] + " " + t).strip()
                continue
            m = re.match(r"^(\d{4}\.\d{4})\s*(.*)$", t)
            if m:  # 8-digit occupation code (title may share the span)
                cur = dict(level="occupation", code=m.group(1), title=m.group(2), nco2004="", page=pno + 1, y=y,
                           _pending_sub=False)
                rows.append(cur)
                continue
            if cur is None:
                continue
            if cur["level"] != "occupation" and cur["code"] is None and re.fullmatch(r"\d{1,4}", t):
                cur["code"] = t
                continue
            cur["title"] = (cur["title"] + " " + t).strip()
        if cur is not None:
            cur["_pending_sub"] = False
    df = pd.DataFrame(rows).drop(columns=["_pending_sub", "y"])
    df["title"] = df["title"].str.replace(r"\s+", " ", regex=True).str.strip()
    df.to_csv(out, index=False, encoding="utf-8")
    print(df.level.value_counts())
    print(df[df.code.isna()])


if __name__ == "__main__":
    main(sys.argv[1])
