"""Parse NCO-2015 Volume II-A and II-B (occupational descriptions, DGE) into a flat table.

Source PDFs (downloaded 2026-11-09):
  https://dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_II-A-2015.pdf
  https://dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_II-B-2015.pdf

Layout: two text columns; headings are Calibri Bold 14pt (blue for Division/Sub Division/Group/Family,
black for 8-digit occupations and "ISCO 08 Unit Group Details"); the Division number appears only as a
white-text side tab on the first page of each Division.

Output: scratch CSV with code, level, title, description, isco08_code, isco08_title, volume, page
Run: python -I parse_nco_vol2.py <out.csv>
"""
import re, sys
import pymupdf as fitz
import pandas as pd

RAW = r"C:\Users\hp\Downloads\xyz\india_jobs\data\raw\nco"
VOLS = {"II-A": RAW + r"\National_Classification_of_Occupations_Vol_II-A-2015.pdf",
        "II-B": RAW + r"\National_Classification_of_Occupations_Vol_II-B-2015.pdf"}
WHITE = 16777215
TOKEN = re.compile(r"^((?:Sub Division|Division|Group|Family)(?=\s+\d)|\d{4}\.\d{4}|ISCO\s*08\s*Unit\s*G\s*roup Details|Qualification Pack Details)")


def page_lines(page):
    """Return (division_tab, lines) where lines = list of dict(text, bold) in reading order."""
    spans, tab = [], None
    W = page.rect.width
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].replace("\u00a0", " ")
                if not t.strip():
                    continue
                x0, y0, x1, y1 = s["bbox"]
                if s["color"] == WHITE:
                    tab = (tab or "") + " " + t.strip()
                    continue
                if y0 < 60 or y0 > 780:  # running header / footer
                    continue
                bold = ("Bold" in s["font"] or s["flags"] & 16) and s["size"] >= 11.5
                if re.fullmatch(r"\s*\d{4}\.\d{4}\s*", t):  # bare 8-digit code = occupation heading
                    bold = True
                spans.append(dict(col=0 if x0 < W / 2 - 5 else 1, y=(y0 + y1) / 2, x=x0, t=t, bold=bold))
    spans.sort(key=lambda s: (s["col"], s["y"], s["x"]))
    lines = []
    for s in spans:
        if lines and lines[-1]["col"] == s["col"] and abs(lines[-1]["y"] - s["y"]) < 4:
            lines[-1]["parts"].append(s)
        else:
            lines.append(dict(col=s["col"], y=s["y"], parts=[s]))
    out = []
    for l in lines:
        parts = sorted(l["parts"], key=lambda s: s["x"])
        # a physical line mixing body text and a bold heading -> emit body first, then the heading
        for grp in ([p for p in parts if not p["bold"]], [p for p in parts if p["bold"]]):
            if grp:
                text = re.sub(r"\s+", " ", " ".join(p["t"].strip() for p in grp)).strip()
                out.append(dict(text=text, bold=grp[0]["bold"]))
    m = re.search(r"Division\s*(\d)", tab or "")
    return (m.group(1) if m else None), out


def parse(vol, path):
    doc = fitz.open(path)
    recs, cur, mode = [], None, None
    cur_div = None

    def flush():
        if cur is not None:
            recs.append(cur.copy())

    heading_buf = []
    for pno in range(doc.page_count):
        tab, lines = page_lines(doc[pno])
        if tab:
            cur_div = tab
        if cur_div is None:  # front matter (title pages, table of contents)
            continue
        if any(l["text"].strip().upper() == "INDEX" for l in lines):
            break
        for ln in lines:
            t = ln["text"]
            if ln["bold"]:
                if TOKEN.match(t) or not heading_buf or heading_buf[-1][0] == "body":
                    heading_buf.append(["head", t, pno + 1, cur_div])
                else:
                    heading_buf[-1][1] += " " + t
            else:
                heading_buf.append(["body", t, pno + 1, cur_div])
    # second pass: build records
    for kind, t, pg, dv in heading_buf:
        if kind == "head":
            m = TOKEN.match(t)
            if m and m.group(1).startswith("ISCO"):
                mode = "isco"
                continue
            if m and m.group(1).startswith("Qualification Pack"):
                mode = "qp"
                rest = t[len(m.group(1)):].strip(" :")
                if rest:
                    cur["qp_nos"] += (" " if cur["qp_nos"] else "") + rest
                continue
            flush()
            mode = "desc"
            if not m:  # Division title (code from white side tab)
                lvl, code, title = "division", dv, t
            elif m.group(1) in ("Division", "Sub Division", "Group", "Family"):
                mm = re.match(r"^(Sub Division|Division|Group|Family)\s+(\d+)\s*(.*)$", t)
                if not mm:
                    lvl, code, title = m.group(1).lower().replace(" ", "_"), None, t
                else:
                    lvl, code, title = mm.group(1).lower().replace(" ", "_"), mm.group(2), mm.group(3)
            else:
                mm = re.match(r"^(\d{4}\.\d{4})\s*(.*)$", t)
                lvl, code, title = "occupation", mm.group(1), mm.group(2)
            cur = dict(code=code, level=lvl, title=title.strip(), description="", isco08_code="", isco08_title="", qp_nos="",
                       volume=vol, page=pg)
        else:
            if cur is None:
                continue
            if mode == "qp":
                cur["qp_nos"] += (" " if cur["qp_nos"] else "") + t
                continue
            if mode == "isco":
                mc = re.match(r"^Code\s+(\S+)", t)
                mt = re.match(r"^Title\s+(.*)$", t)
                if mc:
                    cur["isco08_code"] = mc.group(1)
                elif mt:
                    cur["isco08_title"] = mt.group(1).strip()
                elif cur["isco08_title"]:
                    cur["isco08_title"] += " " + t
                continue
            cur["description"] += (" " if cur["description"] else "") + t
    flush()
    return recs


def clean(df):
    d = df["description"].fillna("")
    # drop the "Occupations in this X are classified into the following Y: ..." trailer lists
    d = d.str.replace(r"\s*Occupations in this (Division|Sub Division|Sub-Division|Group|Family)\b.*$", "", regex=True)
    d = d.str.replace(r"\s+", " ", regex=True).str.replace(r"(\w)- (\w)", r"\1-\2", regex=True).str.strip()
    df["description"] = d
    return df


if __name__ == "__main__":
    allr = []
    for v, p in VOLS.items():
        r = parse(v, p)
        print(v, len(r))
        allr += r
    df = clean(pd.DataFrame(allr))
    df.to_csv(sys.argv[1], index=False, encoding="utf-8")
    print(df.level.value_counts())
