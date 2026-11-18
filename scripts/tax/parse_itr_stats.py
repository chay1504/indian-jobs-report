"""Parse CBDT 'Income Tax Return Statistics' PDFs (AY 2022-23, 2023-24 format) into a tidy CSV of all
'<Status> - Range of <Variable>' tables.
Usage: python -I parse_itr_stats.py <pdf> <AY label> <out_csv> <source_url>
Columns: ay, table_no, status, variable, range_label, lower_rs, upper_rs, n_returns, sum_rs_crore, avg_rs_lakh, page, source_url"""
import sys, re, csv, pymupdf

def num(s):
    s = s.strip()
    if s in ('-', '', '–'): return 0.0
    return float(s.replace(',', '').replace(' ', ''))

def parse_bound(s):
    return float(s.replace(',', ''))

ROW = re.compile(r'(<\s*0|=\s*0|>\s*[\d,]+\s*and\s*<=?\s*[\d,]+|>\s*[\d,]+|Total)\s+([\d,]+|-)\s+(-\s?[\d,]*\d[\d,.]*|[\d,]*\d[\d,.]*|-)\s*(-\s?[\d,]*\d[\d,.]*|[\d,]*\d[\d,.]*|-)?')
TITLE = re.compile(r'(\d+\.\d+)\s*(All Taxpayers|Individual|HUF|Firm|AOP/BOI|Company)\s*[^A-Za-z]{0,3}\s*(?:Range of\s*)?([A-Za-z \-]+?)\s*\(AY')

def main(pdf, ay, out, src):
    doc = pymupdf.open(pdf)
    rows = []
    for pno, page in enumerate(doc, 1):
        raw = page.get_text()
        flat = ' '.join(raw.split())
        m = TITLE.search(flat)
        if not m or 'Range (in INR)' not in flat: continue
        table_no, status, var = m.group(1), m.group(2), m.group(3).strip()
        body = flat[flat.find('Range (in INR)'):]
        body = body[:body.find('Notes')] if 'Notes' in body else body
        # strip header words up to first '<' or '='
        start = min([i for i in (body.find('< 0'), body.find('<0'), body.find('= 0')) if i >= 0] or [0])
        body = body[start:]
        for rm in ROW.finditer(body):
            lab, n, s, a = rm.groups()
            lab = ' '.join(lab.split())
            lo = up = ''
            if lab.startswith('<'): lo, up = '', 0
            elif lab.startswith('='): lo = up = 0
            elif lab == 'Total': pass
            else:
                b = re.findall(r'[\d,]+', lab)
                lo = parse_bound(b[0]); up = parse_bound(b[1]) if len(b) > 1 else ''
            rows.append(dict(ay=ay, table_no=table_no, status=status, variable=var, range_label=lab,
                             lower_rs=lo, upper_rs=up, n_returns=int(num(n)), sum_rs_crore=num(s),
                             avg_rs_lakh=(num(a) if a else ''), page=pno, source_url=src))
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    # integrity check: sum of bins == Total for each table
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0.0]); tot = {}
    for r in rows:
        k = (r['table_no'], r['status'], r['variable'])
        if r['range_label'] == 'Total': tot[k] = (r['n_returns'], r['sum_rs_crore'])
        else: agg[k][0] += r['n_returns']; agg[k][1] += r['sum_rs_crore']
    for k in sorted(agg, key=lambda x: [int(p) for p in x[0].split('.')]):
        t = tot.get(k)
        flag = '' if t and t[0] == agg[k][0] and abs(t[1] - agg[k][1]) < 2 else '  <-- CHECK'
        print(k, 'bins', agg[k][0], round(agg[k][1], 2), 'total', t, flag)
    print('rows', len(rows))

if __name__ == '__main__':
    main(*sys.argv[1:])
