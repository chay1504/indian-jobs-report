"""Build tidy CSVs of the distribution of workers (usual status ps+ss, all ages) by
  * occupation (NCO-2015 / NCO-2004 3-digit group, 2-digit sub-division, 1-digit division)  -> Table (25)
  * industry  (NIC-2008 4-digit class, 3-digit group, 2-digit division, section)            -> Table (26)
for PLFS 2025 (Excel), PLFS 2023-24 (Excel) and PLFS 2017-18 (PDF only).

Outputs: data/plfs/plfs_workers_by_occupation_nco.csv, data/plfs/plfs_workers_by_industry_nic.csv
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # our own helper module (python -I drops script dir)

from plfs_common import (OUT, SRC, SECTORS9, NCO2015, NCO2004, rec, num, xlsx_rows, pdf_pages_with, page_range,
                         pdf_tokens, pdf_text, COLS)

sys.stdout.reconfigure(encoding='utf-8')
AGE = 'all ages (table gives no age restriction: all usual-status workers)'


# ---------------------------------------------------------------- NIC names from AR 2025 Annexure I
def nic_names():
    pdf = SRC['2025']['pdf']
    pages = [p for p in pdf_pages_with(pdf, r'BROAD STRUCTURE of NIC') ]
    pages = list(range(pages[0], pages[0] + 4))
    txt = pdf_text(pdf, pages, sep='\n')
    names = {}
    cur = None
    for line in txt.split('\n'):
        m = re.match(r'^Section ([A-U]):\s*(.+)$', line.strip())
        m2 = re.match(r'^Division (\d{2}):\s*(.+)$', line.strip())
        if m:
            cur = m.group(1); names[cur] = m.group(2).strip()
        elif m2:
            cur = m2.group(1); names[cur] = m2.group(2).strip()
        elif cur and line.strip() and not re.match(
                r'^(Appendix|Concepts|Annual Report|C-\d+|ANNEXURE|BROAD|\(SECTIONS|\d{4}$)', line.strip()):
            names[cur] += ' ' + line.strip()  # wrapped continuation line
    fixes = {'andservices': 'and services', 'servicesproducing': 'services producing', 'privatehouseholds': 'private households'}
    for k in names:
        for a, b in fixes.items():  # words run together in the PDF text layer
            names[k] = names[k].replace(a, b)
        names[k] = re.sub(r'\s+', ' ', names[k]).strip()
    for k in list(names):  # a missing colon/newline in the PDF merges two divisions (55 + 56)
        m = re.match(r'^(.*?) Division (\d{2}):? (.+)$', names[k])
        if m:
            names[k] = m.group(1).strip()
            names.setdefault(m.group(2), m.group(3).strip())
    return names, page_range(pages)


NIC, NIC_PAGES = nic_names()


def nco_meta(code_label, classification):
    names = NCO2015 if classification == 'NCO-2015' else NCO2004
    lab = re.sub(r'\s+', ' ', str(code_label)).strip()
    if lab.lower().startswith('division'):
        c = lab.split()[-1]
        return c, names.get(c, ''), 'division'
    if lab.lower().startswith('sub-division'):
        c = lab.split()[-1]
        return c, names.get(c, ''), 'sub-division'
    if re.fullmatch(r'\d{3}', lab):
        sd = lab[:2]
        return lab, f'group {lab} (3-digit title not printed in PLFS report; sub-division {sd}: {names.get(sd, "")})', 'group'
    if lab.lower() == 'total':
        return 'total', 'all workers', 'total'
    return None


def nic_meta(code_label):
    lab = str(code_label).strip()
    if re.fullmatch(r'\d{4}', lab):
        return lab, f'class {lab} (4-digit title not printed in PLFS report; division {lab[:2]}: {NIC.get(lab[:2], "")})', 'class'
    if re.fullmatch(r'\d{3}', lab):
        return lab, f'group {lab} (title not printed in PLFS report; division {lab[:2]}: {NIC.get(lab[:2], "")})', 'group'
    if re.fullmatch(r'\d{2}', lab):
        return lab, NIC.get(lab, ''), 'division'
    if re.fullmatch(r'[A-U]', lab):
        return lab, NIC.get(lab, ''), 'section'
    if lab.lower() == 'total':
        return 'total', 'all workers', 'total'
    if lab.lower().startswith('sub-total'):
        return lab.replace(' ', ''), lab, 'sub-total'
    return None


def emit_wide(rows_out, table, period, code, name, level, vals, unit, cls, url, page, notes=''):
    for (s, x), v in zip(SECTORS9, vals):
        if v is None:
            continue
        rows_out.append(rec(table=table, period=period, sector=s, sex=x, age_group=AGE, category_code=code,
                            category_name=name, category_level=level, value=v, unit=unit, classification=cls,
                            source_url=url, page_or_table=page, notes=notes))


def from_excel(year, n, kind, rows_out):
    S = SRC[year]
    path = S['xlsx_dir'] / S['xlsx_name'].format(n=n)
    url = S['xlsx_url'].format(n=n)
    pages = [p for p in pdf_pages_with(S['pdf'], rf'Table \({n}\)') if p > 80]
    page = f'Table ({n}), Appendix A; Excel {path.name}; same table at {page_range(pages)} of {S["pdf_url"]}'
    cls = 'NCO-2015' if kind == 'nco' else 'NIC-2008'
    count = 0
    for r in xlsx_rows(path):
        lab = r[0]
        vals = [num(v) for v in r[1:10]]
        if sum(v is not None for v in vals) < 9:
            continue
        labs = str(lab).strip().lower()
        if labs.startswith('sample'):
            emit_wide(rows_out, f'Table ({n})', S['period'], 'sample', 'sample workers (unweighted count)', 'sample',
                      vals, 'count (sample persons)', cls, url, page)
            continue
        meta = nco_meta(lab, cls) if kind == 'nco' else nic_meta(lab)
        if not meta:
            print('  skip row', year, n, r[:3])
            continue
        code, name, level = meta
        emit_wide(rows_out, f'Table ({n})', S['period'], code, name, level, vals, '% of workers', cls, url, page)
        count += 1
    print(f'{year} Table {n}: {count} category rows from {path.name}')


def from_pdf_2017(n, kind, rows_out):
    S = SRC['2017-18']
    pages = [p for p in pdf_pages_with(S['pdf'], rf'Table \({n}\)') if p > 200]
    page = f'Table ({n}), Appendix A, {page_range(pages)}'
    cls = 'NCO-2004' if kind == 'nco' else 'NIC-2008'
    toks = pdf_tokens(S['pdf'], pages)
    i, count = 0, 0
    code_rx = (r'^(\d{3}|Sub-division \d{2}|Division [0-9X]|total)$' if kind == 'nco'
               else r'^(\d{4}|\d{3}|\d{2}|[A-U]|total|sub-total.*)$')
    while i < len(toks):
        t = re.sub(r'\s+', ' ', toks[i]).strip()
        if re.match(code_rx, t, re.I):
            nxt = toks[i + 1:i + 10]
            vals = [num(v) if v != '-' else None for v in nxt]
            if len(nxt) == 9 and all((v is not None) or (nxt[k] == '-') for k, v in enumerate(vals)):
                meta = nco_meta(t, cls) if kind == 'nco' else nic_meta(t)
                if meta and any(v is not None for v in vals):
                    code, name, level = meta
                    emit_wide(rows_out, f'Table ({n})', S['period'], code, name, level, vals, '% of workers', cls,
                              S['pdf_url'], page)
                    count += 1
                i += 10
                continue
        i += 1
    # estimated (design-based) workers and sample size rows at the foot of the table
    txt = pdf_text(S['pdf'], pages[-1:])
    for marker, label, unit, note in [
        (r'(estd\.|estimated) \|? ?workers\(00\)', 'estimated workers (00), design-based', 'hundreds of workers (design-based)',
         'PLFS design-based estimate; MoSPI cautions such totals are for combining ratios, not for counting workers'),
        (r'sample workers', 'sample workers (unweighted count)', 'count (sample persons)', '')]:
        m = re.search(marker + r'((?:\s*\|\s*\d+){9})', txt)
        if m:
            vals = [float(x) for x in re.findall(r'\d+', m.group(m.lastindex))]
            emit_wide(rows_out, f'Table ({n})', S['period'], 'estd' if 'estimated' in label else 'sample', label,
                      'sample' if 'sample' in label else 'estimate', vals, unit, cls, S['pdf_url'], page, note)
    print(f'2017-18 Table {n}: {count} category rows from PDF {page}')


def check(rows, label):
    """Print consistency checks: sections/divisions should sum to ~100 for rural+urban person."""
    sel = [r for r in rows if r['sector'] == 'rural+urban' and r['sex'] == 'person' and r['unit'] == '% of workers']
    by = {}
    for r in sel:
        by.setdefault((r['period'], r['category_level']), 0.0)
        by[(r['period'], r['category_level'])] += float(r['value'])
    for k, v in sorted(by.items()):
        print(f'  check {label} {k}: sum={v:.2f}')


def write(rows, fn):
    with open(OUT / fn, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print('wrote', fn, len(rows))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print('NIC names parsed:', len(NIC), 'from AR 2025', NIC_PAGES)
    nco, nic = [], []
    from_excel('2025', 25, 'nco', nco)
    from_excel('2023-24', 25, 'nco', nco)
    from_pdf_2017(25, 'nco', nco)
    from_excel('2025', 26, 'nic', nic)
    from_excel('2023-24', 26, 'nic', nic)
    from_pdf_2017(26, 'nic', nic)
    check(nco, 'NCO')
    check(nic, 'NIC')
    write(nco, 'plfs_workers_by_occupation_nco.csv')
    write(nic, 'plfs_workers_by_industry_nic.csv')


if __name__ == '__main__':
    main()
