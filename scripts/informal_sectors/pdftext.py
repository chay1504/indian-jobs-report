import sys, pymupdf
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc = pymupdf.open(sys.argv[1])
pages = sys.argv[2] if len(sys.argv) > 2 else None
rng = range(len(doc))
if pages:
    a, b = pages.split('-') if '-' in pages else (pages, pages)
    rng = range(int(a)-1, min(int(b), len(doc)))
print('PAGES', len(doc))
for i in rng:
    print(f'--- page {i+1}')
    print(doc[i].get_text())
