"""Dump PDF text page by page: python pdf_dump.py in.pdf out.txt"""
import sys, fitz
doc = fitz.open(sys.argv[1])
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for i, p in enumerate(doc):
        f.write(f"\n=====PAGE {i+1}=====\n")
        f.write(p.get_text())
print(sys.argv[1], doc.page_count)
