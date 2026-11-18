"""Dump text of a PDF (all pages or range) to a .txt with page markers.
Usage: python -I pdf_text.py <pdf> <out_txt>"""
import sys, fitz
pdf, out = sys.argv[1], sys.argv[2]
doc = fitz.open(pdf)
with open(out, "w", encoding="utf-8") as f:
    for i, p in enumerate(doc):
        f.write(f"\n\n===== PAGE {i+1} =====\n")
        f.write(p.get_text())
print(len(doc), "pages ->", out)
