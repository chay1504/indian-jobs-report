"""Dump text of a PDF, page by page, to a UTF-8 text file. Usage: pdf2txt.py in.pdf out.txt"""
import sys, pymupdf
d = pymupdf.open(sys.argv[1])
with open(sys.argv[2], 'w', encoding='utf-8') as f:
    for i, p in enumerate(d):
        f.write(f'\n=====PAGE {i+1}\n')
        f.write(p.get_text())
print(len(d), 'pages')
