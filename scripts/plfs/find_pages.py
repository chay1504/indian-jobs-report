"""Print first/last PDF page (1-based) on which a regex appears. Usage: find_pages.py file.pdf regex [regex...]"""
import sys, re, pymupdf
d = pymupdf.open(sys.argv[1])
texts = [p.get_text() for p in d]
for pat in sys.argv[2:]:
    rx = re.compile(pat)
    pages = [i + 1 for i, t in enumerate(texts) if rx.search(t)]
    print(f'{pat!r}: n={len(pages)} pages={pages[:12]}{"..." if len(pages) > 12 else ""}')
