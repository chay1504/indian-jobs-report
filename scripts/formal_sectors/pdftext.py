"""Extract text from a PDF (optionally a page range) using PyMuPDF. Usage: pdftext.py file.pdf [first_page] [last_page] (1-based)"""
import sys, fitz
p = sys.argv[1]
doc = fitz.open(p)
a = int(sys.argv[2]) if len(sys.argv) > 2 else 1
b = int(sys.argv[3]) if len(sys.argv) > 3 else doc.page_count
for i in range(a-1, min(b, doc.page_count)):
    print(f"===== PAGE {i+1} =====")
    print(doc[i].get_text())
