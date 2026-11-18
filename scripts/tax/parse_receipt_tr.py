"""Parse 'Tax Revenue' statement (Receipt Budget, tr.pdf) for major-head totals.
Usage: python -I parse_receipt_tr.py <tr.pdf> ; prints label + 4 columns."""
import sys, re, pymupdf
KEYS = ['Total-Corporation Tax', '2.09.', 'Total-Taxes on Income', 'Total-Wealth Tax', 'Total-Commodity Transaction Tax',
        'Total-Customs', 'Total-Union Excise Duties', 'Total-Service Tax', '8.01.', '8.02.', '8.03.',
        'Total-Goods and Services Tax (GST)', 'Total-Other Taxes and Duties on Commodities and Services',
        'Total-Taxes of Union Territories', 'Net-Less-NCCD', '12. Less-States', 'Total-Tax Revenue']
doc = pymupdf.open(sys.argv[1])
lines = []
for p in doc: lines += [l.strip() for l in p.get_text().split('\n')]
hdr = ' '.join(lines[:30])
print('HEADER:', re.sub(r'\s+', ' ', hdr)[:200])
num = re.compile(r'^-?[\d.]+$|^\.\.\.$')
for i, l in enumerate(lines):
    for k in KEYS:
        if l.startswith(k):
            vals = []
            j = i + 1
            while j < len(lines) and len(vals) < 4:
                if num.match(lines[j]) and not re.match(r'^\d{4}$', lines[j]): vals.append(lines[j])
                elif re.match(r'^\d{4}$', lines[j]): pass  # major head code
                elif vals: break
                j += 1
            print(f'{l[:60]:60s}', vals)
