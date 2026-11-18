"""Dump page text of each downloaded annual report to a text file with page markers,
so figures can be grepped and cited by PDF page. Usage: firm_extract.py <pdf_dir> <out_dir>"""
import os, sys, re
import fitz  # pymupdf

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for fn in sorted(os.listdir(src)):
    if not fn.endswith(".pdf") or (len(sys.argv) > 3 and not fn.startswith(sys.argv[3])):
        continue
    key = fn[:-4]
    try:
        doc = fitz.open(os.path.join(src, fn))
    except Exception as e:
        print(key, "OPEN ERR", e); continue
    hits = {"median remuneration": [], "permanent employees": []}
    with open(os.path.join(out, key + ".txt"), "w", encoding="utf-8") as f:
        for i, pg in enumerate(doc, 1):
            t = pg.get_text("text")
            f.write(f"\n=== PDF PAGE {i} ===\n{t}")
            low = t.lower()
            for h in hits:
                if h in low:
                    hits[h].append(i)
    print(key, "pages", doc.page_count, {k: v[:8] for k, v in hits.items()})
