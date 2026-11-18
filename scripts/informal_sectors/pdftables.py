import sys, pdfplumber
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pdf = pdfplumber.open(sys.argv[1])
for p in sys.argv[2].split(','):
    page = pdf.pages[int(p)-1]
    print(f'=== page {p}')
    for t in page.extract_tables():
        for row in t:
            print(' | '.join('' if c is None else str(c).replace('\n',' ') for c in row))
        print('---')
