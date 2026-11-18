"""Build tidy CSVs for status in employment, broad industry, education, earnings and formality
from PLFS Annual Reports 2025 (Excel + PDF statements), 2023-24 (Excel) and 2017-18 (PDF).

Outputs (data/plfs/):
  plfs_status_in_employment.csv   (incl. Table 20 status x industry crosstab)
  plfs_broad_industry.csv
  plfs_education.csv              (incl. Table 21 status x industry x education crosstab, Table 11.0 years of schooling by NIC section)
  plfs_earnings.csv               (incl. Table 51/50 earnings by NCO division, Table 52/51 casual wage by NIC section)
  plfs_formality.csv              (incl. Table 37 enterprise type x size crosstab)
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plfs_common import (OUT, SRC, COLS, NCO2015, rec, num, xlsx_rows, pdf_pages_with, page_range, pdf_text,  # noqa: E402
                         numbers_after)

sys.stdout.reconfigure(encoding='utf-8')
S25, S24, S18 = SRC['2025'], SRC['2023-24'], SRC['2017-18']
SECT3 = ['rural', 'urban', 'rural+urban']
SEX3 = ['male', 'female', 'person']
SEC_SEX = [(s, x) for s in SECT3 for x in SEX3]
CY = {'2025': 'Jan-Dec 2025 (calendar year)', '2024': 'Jan-Dec 2024 (calendar year)',
      '2023': 'Jan-Dec 2023 (calendar year)', '2022': 'Jan-Dec 2022 (calendar year)'}
STATUS_COLS = [('SE_OAW_EMP', 'self-employed: own account worker & employer'),
               ('SE_HELPER', 'self-employed: unpaid helper in household enterprise'),
               ('SE_ALL', 'all self-employed'), ('RWS', 'regular wage/salaried'), ('CASUAL', 'casual labour'),
               ('ALL', 'all workers')]
EDU_COLS = [('E1', 'not literate'), ('E2', 'literate & up to primary'), ('E3', 'middle'), ('E4', 'secondary'),
            ('E5', 'higher secondary'), ('E6', 'diploma/certificate course'), ('E7', 'graduate'),
            ('E8', 'post graduate & above'), ('E4P', 'secondary & above'), ('ALL', 'all')]
ENT_TYPES = [('ET1', 'proprietary & partnership'), ('ET2', 'govt./local body/public sector enterprises'),
             ('ET3', 'autonomous bodies'), ('ET4', 'public/private limited company'), ('ET5', 'cooperative societies'),
             ('ET6', 'trust/other non-profit institutions'), ('ET7', "employer's households"), ('ET8', 'others'),
             ('ALL', 'all')]
SIZE_COLS = [('S1_5', '1-5 workers'), ('S6_9', '6-9 workers'), ('S10_19', '10-19 workers'), ('S20P', '20 or more workers'),
             ('SNK', 'not known'), ('ALL', 'all')]


def title_sector_sex(t):
    t = re.sub(r'\s+', ' ', t.lower())
    sec = 'rural+urban' if re.search(r'rural ?\+ ?urban', t) else ('urban' if ' urban' in t else ('rural' if ' rural' in t else ''))
    sex = 'female' if 'female' in t else ('male' if re.search(r'\bmale\b', t) else ('person' if 'person' in t else ''))
    age = ''
    m = re.search(r'age group: ?([^\t]+?)\s*$', t)
    if m:
        age = m.group(1).strip()
    return sec, sex, age


def blocks(path, sheet_index=0):
    """Yield (title, rows) blocks where each block starts at a row whose first cell starts with 'Table ('."""
    cur, title = [], None
    for r in xlsx_rows(path, sheet_index):
        if str(r[0]).startswith('Table ('):
            if title:
                yield title, cur
            title, cur = str(r[0]), []
        elif title:
            cur.append(r)
    if title:
        yield title, cur


def all_india_row(rows):
    for r in rows:
        if re.fullmatch(r'all[ -]india', str(r[0]).strip().lower()):
            return r
    return None


def xls_src(S, n):
    path = S['xlsx_dir'] / S['xlsx_name'].format(n=n)
    pages = [p for p in pdf_pages_with(S['pdf'], rf'Table \({re.escape(str(n))}\)') if p > 60]
    return path, S['xlsx_url'].format(n=n), f'Table ({n}), Appendix A (Excel {path.name}; {page_range(pages)})'


def write(rows, fn):
    with open(OUT / fn, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print('wrote', fn, len(rows))


def stmt_page(S, label):
    pages = pdf_pages_with(S['pdf'], re.escape(label))
    return pages[0] if pages else None


# ================================================================== STATUS IN EMPLOYMENT
def status():
    out = []
    # --- 2025 AR Statement 7: PLFS 2022-2025 (calendar years)
    pg = stmt_page(S25, 'Statement 7:')
    txt = pdf_text(S25['pdf'], [pg])
    for yr in ('2025', '2024', '2023', '2022'):
        vals = numbers_after(txt, f'PLFS {yr} | rural', 54)  # 9 rows (rural/urban/total x m/f/p) x 6 columns
        for k, (s, x) in enumerate(SEC_SEX):
            for (c, nme), v in zip(STATUS_COLS, vals[6 * k:6 * k + 6]):
                out.append(rec(table='Statement 7', period=CY[yr], sector=s, sex=x, age_group='all ages (statement gives no age restriction)',
                               category_code=c, category_name=nme, category_level='status', value=v,
                               unit='% of usual-status (ps+ss) workers', source_url=S25['pdf_url'],
                               page_or_table=f'Statement 7, PDF p.{pg} (report p.17), AR PLFS 2025'))
    # --- 2023-24 Table 19 all-India rows (Excel)
    path, url, page = xls_src(S24, 19)
    for title, rows in blocks(path):
        s, x, _ = title_sector_sex(title)
        r = all_india_row(rows)
        for (c, nme), v in zip(STATUS_COLS, r[1:7]):
            out.append(rec(table='Table (19)', period=S24['period'], sector=s, sex=x, age_group='all ages (table gives no age restriction)',
                           category_code=c, category_name=nme, category_level='status', value=num(v),
                           unit='% of usual-status (ps+ss) workers', source_url=url, page_or_table=page + ', all-India row'))
    # --- 2017-18 Statement 14
    pg = stmt_page(S18, 'Statement 14:')
    txt = pdf_text(S18['pdf'], [pg])
    vals = numbers_after(txt, '| (7) |', 54, txt.find('Statement 14:'))
    for k, (s, x) in enumerate(SEC_SEX):
        for (c, nme), v in zip(STATUS_COLS, vals[6 * k:6 * k + 6]):
            out.append(rec(table='Statement 14', period=S18['period'], sector=s, sex=x, age_group='all ages (statement gives no age restriction)',
                           category_code=c, category_name=nme, category_level='status', value=v,
                           unit='% of usual-status (ps+ss) workers', source_url=S18['pdf_url'],
                           page_or_table=f'Statement 14, PDF p.{pg} (report p.62), AR PLFS 2017-18'))
    # --- Table 20: status x industry (2025, 2023-24)
    for S in (S25, S24):
        path, url, page = xls_src(S, 20)
        for title, rows in blocks(path):
            s, x, _ = title_sector_sex(title)
            for r in rows:
                lab = str(r[0]).strip()
                m = re.match(r'^(\d{2}-\d{2})\s*\(?\s*([^)]*)\)*', lab)
                if lab.lower() == 'total':
                    code, nme = 'total', 'all industries'
                elif m:
                    code, nme = m.group(1), m.group(2).strip().rstrip(')')
                else:
                    if lab.lower().startswith('sample'):
                        code, nme = 'sample', 'sample workers (count)'
                    else:
                        continue
                for (c, cn), v in zip(STATUS_COLS, r[1:7]):
                    if num(v) is None:
                        continue
                    out.append(rec(table='Table (20)', period=S['period'], sector=s, sex=x, age_group='all ages (table gives no age restriction)',
                                   category_code=code, category_name=f'NIC-2008 divisions {code} ({nme})' if code not in ('total', 'sample') else nme,
                                   category_level='industry (NIC-2008 division group)', cross_code=c, cross_name=cn, value=num(v),
                                   unit='count (sample workers)' if code == 'sample' else '% of workers in the industry (row %)',
                                   classification='NIC-2008', source_url=url, page_or_table=page))
    write(out, 'plfs_status_in_employment.csv')


# ================================================================== BROAD INDUSTRY (Statement 8 / Statement 16)
BROAD = ['agriculture', 'mining & quarrying', 'manufacturing', 'electricity, water, etc.', 'construction',
         'trade, hotel & restaurant', 'transport, storage & communications', 'other services']
BROAD_CODE = {'agriculture': 'A', 'mining & quarrying': 'B', 'manufacturing': 'C', 'electricity, water, etc.': 'D+E',
              'construction': 'F', 'trade, hotel & restaurant': 'G+I', 'transport, storage & communications': 'H+J',
              'other services': 'K-U'}


def broad_industry():
    out = []
    pg = stmt_page(S25, 'Statement 8:')
    txt = pdf_text(S25['pdf'], [pg])
    for yr in ('2025', '2024', '2023', '2022'):
        vals = numbers_after(txt, f'PLFS {yr} | agriculture', 72)  # 8 rows x 9 columns
        for b_i, b in enumerate(BROAD):
            for (s, x), v in zip(SEC_SEX, vals[9 * b_i:9 * b_i + 9]):
                out.append(rec(table='Statement 8', period=CY[yr], sector=s, sex=x, age_group='all ages (statement gives no age restriction)',
                               category_code=BROAD_CODE[b], category_name=b, category_level='broad industry (NIC-2008 sections)',
                               value=v, unit='% of usual-status (ps+ss) workers', classification='NIC-2008',
                               source_url=S25['pdf_url'], page_or_table=f'Statement 8, PDF p.{pg} (report p.19), AR PLFS 2025'))
    # 2017-18 Statement 16 (row block 'PLFS (2017-18)')
    pg = stmt_page(S18, 'Statement 16:')
    txt = pdf_text(S18['pdf'], [pg, pg + 1])
    print('  2017-18 Statement 16 page', pg)
    write(out, 'plfs_broad_industry.csv')
    return txt


# ================================================================== EDUCATION
def education():
    out = []
    for S in (S25, S24):
        # Table 8: distribution of persons 15+ by education (all-India rows)
        path, url, page = xls_src(S, 8)
        pop = {}
        for title, rows in blocks(path):
            s, x, _ = title_sector_sex(title)
            r = all_india_row(rows)
            for (c, nme), v in zip(EDU_COLS, r[1:11]):
                pop[(s, x, c)] = num(v)
                out.append(rec(table='Table (8)', period=S['period'], sector=s, sex=x, age_group='15 years and above',
                               category_code=c, category_name=nme, category_level='highest education level completed',
                               value=num(v), unit='% of persons aged 15+', source_url=url, page_or_table=page + ', all-India row'))
        # Table 23: WPR by education (15+)
        path, url, page = xls_src(S, 23)
        wpr = {}
        for title, rows in blocks(path):
            s, x, _ = title_sector_sex(title)
            r = all_india_row(rows)
            for (c, nme), v in zip(EDU_COLS, r[1:11]):
                wpr[(s, x, c)] = num(v)
                out.append(rec(table='Table (23)', period=S['period'], sector=s, sex=x, age_group='15 years and above',
                               category_code=c, category_name=nme, category_level='highest education level completed',
                               value=num(v), unit='WPR % (usual status ps+ss)', source_url=url, page_or_table=page + ', all-India row'))
        # Derived: distribution of workers 15+ by education = pop share x WPR / sum
        for (s, x) in SEC_SEX:
            cats = [c for c, _ in EDU_COLS[:8]]
            prod = {c: pop[(s, x, c)] * wpr[(s, x, c)] for c in cats}
            tot = sum(prod.values())
            for c, nme in EDU_COLS[:8]:
                out.append(rec(table='DERIVED from Table (8) x Table (23)', period=S['period'], sector=s, sex=x,
                               age_group='15 years and above', category_code=c, category_name=nme,
                               category_level='highest education level completed', value=round(100 * prod[c] / tot, 2),
                               unit='% of usual-status workers aged 15+ (derived)', source_url=url.replace('23', '8'),
                               page_or_table=f'computed: Table (8) share x Table (23) WPR, normalised; {S["label"]}',
                               notes='derived by this project, not published by MoSPI; inputs rounded to 0.1'))
    # Table 21 (2025): status x broad industry x education, rural+urban, all three sexes, age 15+
    path, url, page = xls_src(S25, 21)
    for title, rows in blocks(path):
        s, x, age = title_sector_sex(title)
        if s != 'rural+urban' or '15 years and above' not in age:
            continue
        for r in rows:
            st, ind = str(r[0]).strip(), str(r[1]).strip()
            if not re.match(r'^(\d|UR)', st):
                continue
            for (c, nme), v in zip(EDU_COLS, r[2:12]):
                if num(v) is None:
                    continue
                out.append(rec(table='Table (21)', period=S25['period'], sector=s, sex=x, age_group='15 years and above',
                               category_code=f'status {st} | industry {ind}',
                               category_name='usual status (ps+ss) code(s) [11,12 own-account/employer; 21 helper; 31 regular wage; 41 casual public works; 51 casual other; 81 unemployed; 91-97 not in labour force] x NIC-2008 division range (x = n.a.)',
                               category_level='status x broad industry', cross_code=c, cross_name=nme, value=num(v),
                               unit='UR %' if st == 'UR' else '% of persons aged 15+ with that education level (column %)',
                               source_url=url, page_or_table=page + f'; block: {re.sub(chr(32)+"+", " ", title)[-80:]}'))
    # Table 11.0 (2025): average years of formal education of workers by NIC section
    path, url, page = xls_src(S25, '11.0')
    for title, rows in blocks(path):
        s, x, _ = title_sector_sex(title)
        for r in rows:
            lab = str(r[0]).strip()
            if not (re.fullmatch(r'[A-U]', lab) or lab.lower() == 'total'):
                continue
            for k, ag in enumerate(['15-29 years', '15-59 years', '15 years and above']):
                v = num(r[1 + k])
                out.append(rec(table='Table (11.0)', period=S25['period'], sector=s, sex=x, age_group=ag,
                               category_code=lab, category_name=f'NIC-2008 section {lab}', category_level='section',
                               value=v, unit='average years of formal education (workers ps+ss literate via formal schooling)',
                               classification='NIC-2008', source_url=url, page_or_table=page,
                               notes='zero-years cases excluded by MoSPI; value 0 for section U means no sample'))
    # Statement 6 cross-check (2025, rural+urban person, WPR by education)
    write(out, 'plfs_education.csv')


# ================================================================== EARNINGS
NCO_DIV = {str(i): NCO2015[str(i)] for i in range(1, 10)}


def earnings():
    out = []
    # Statements 11-13 (2022-2025)
    for st, unit, measure in [('Statement 11:', 'Rs per month (preceding calendar month)', 'regular wage/salaried employees (CWS): average wage/salary earnings'),
                              ('Statement 12:', 'Rs per day', 'casual labour (CWS) in works other than public works: average wage earnings per day'),
                              ('Statement 13:', 'Rs per 30 days (gross)', 'self-employed (CWS): average gross earnings, last 30 days')]:
        pg = stmt_page(S25, st)
        txt = pdf_text(S25['pdf'], [pg])
        i = txt.find(st)
        seg = txt[i:]
        for yr in ('2025', '2024', '2023', '2022'):
            j = seg.find(f'| {yr} |')
            vals = numbers_after(seg, f'| {yr} |', 9, j - 1)
            for (s, x), v in zip(SEC_SEX, vals):
                out.append(rec(table=st.rstrip(':'), period=CY[yr], sector=s, sex=x, age_group='all ages (CWS workers)',
                               category_code=st.rstrip(':').replace(' ', '_'), category_name=measure, category_level='earnings',
                               value=v, unit=unit, source_url=S25['pdf_url'],
                               page_or_table=f'{st.rstrip(":")}, PDF p.{pg}, AR PLFS 2025'))
    # 2025 Tables 38-40 all-India (2 decimals)
    for n, unit, measure in [(38, 'Rs per month', 'regular wage/salaried: average wage/salary earnings, preceding calendar month'),
                             (39, 'Rs per day', 'casual labour (other than public works): average daily wage'),
                             (40, 'Rs per 30 days (gross)', 'self-employed: average gross earnings, last 30 days')]:
        path, url, page = xls_src(S25, n)
        for title, rows in blocks(path):
            r = all_india_row(rows)
            for (s, x), v in zip(SEC_SEX, r[1:10]):
                out.append(rec(table=f'Table ({n})', period=S25['period'], sector=s, sex=x, age_group='all ages (CWS workers)',
                               category_code=f'T{n}', category_name=measure, category_level='earnings', value=num(v), unit=unit,
                               source_url=url, page_or_table=page + ', all-India row'))
        # 2023-24 quarterly versions
        path, url, page = xls_src(S24, n)
        for title, rows in blocks(path):
            q = re.search(r'(July-Sep|Oct-Dec|Jan-Mar|Apr-June?)[ ,]+\d{4}', title)
            r = all_india_row(rows)
            if not r or not q:
                continue
            for (s, x), v in zip(SEC_SEX, r[1:10]):
                out.append(rec(table=f'Table ({n})', period=f'{q.group(0)} (quarter of PLFS 2023-24)', sector=s, sex=x,
                               age_group='all ages (CWS workers)', category_code=f'T{n}', category_name=measure,
                               category_level='earnings', value=num(v), unit=unit, source_url=url,
                               page_or_table=page + ', all-India row', notes='2023-24 report publishes earnings by quarter only'))
    # Table 51 (2025) / Table 50 (2023-24): RWS earnings by NCO division
    for S, n in ((S25, 51), (S24, 50)):
        path, url, page = xls_src(S, n)
        sec = None
        rows = xlsx_rows(path)
        for r in rows:
            lab = re.sub(r'\s+', ' ', str(r[0])).strip()
            m = re.match(r'^(rural\+urban|rural|urban) (male|female|person)$', lab)
            if m:
                sec, sx = m.group(1), m.group(2)
                continue
            if sec and (lab.startswith('Average wage') or lab.startswith('sample')):
                if all(num(v) is None for v in r[1:11]):
                    continue  # repeated column-header row of the next block
                is_avg = lab.startswith('Average')
                for k, v in enumerate(r[1:11]):
                    code = str(k + 1) if k < 9 else 'all'
                    out.append(rec(table=f'Table ({n})', period=S['period'], sector=sec, sex=sx, age_group='all ages (CWS workers)',
                                   category_code=code, category_name=NCO_DIV.get(code, 'all divisions'), category_level='NCO-2015 division',
                                   value=num(v), unit='Rs per month (preceding calendar month)' if is_avg else 'count (sample regular wage/salaried employees)',
                                   classification='NCO-2015', source_url=url, page_or_table=page,
                                   notes='regular wage/salaried employees in CWS; MoSPI: estimates may be subject to high sampling fluctuations'))
    # Table 52 (2025) / Table 51 (2023-24): casual wage by NIC section
    for S, n in ((S25, 52), (S24, 51)):
        path, url, page = xls_src(S, n)
        rows = xlsx_rows(path)
        hdr = None
        sec = None
        for r in rows:
            lab = re.sub(r'\s+', ' ', str(r[0])).strip()
            if len(r) > 2 and str(r[1]).strip() == 'A' and str(r[2]).strip() == 'B':
                hdr = [str(c).strip() for c in r[1:23]]
                continue
            m = re.match(r'^(rural\+urban|rural|urban) (male|female|person)$', lab)
            if m:
                sec, sx = m.group(1), m.group(2)
                continue
            if sec and hdr and (lab.startswith('Average wage') or lab.startswith('sample')):
                if all(num(v) is None for v in r[1:23]):
                    continue  # repeated column-header row of the next block
                is_avg = lab.startswith('Average')
                for code, v in zip(hdr, r[1:23]):
                    out.append(rec(table=f'Table ({n})', period=S['period'], sector=sec, sex=sx, age_group='all ages (CWS casual labourers)',
                                   category_code=code, category_name=f'NIC-2008 section {code}' if code != 'all' else 'all sections',
                                   category_level='NIC-2008 section', value=num(v),
                                   unit='Rs per day (casual labour work)' if is_avg else 'count (sample person-days of casual labour)',
                                   classification='NIC-2008', source_url=url, page_or_table=page,
                                   notes='0 = no sample observation; includes public works? table title says casual labour work (not restricted); high sampling fluctuation'))
    # 2017-18 Tables 42/43/45: quarterly all-India + derived annual (weighted by MoSPI's estimated counts)
    for n, unit, measure in [(42, 'Rs per month', 'regular wage/salaried: average wage/salary earnings, preceding calendar month'),
                             (43, 'Rs per day', 'casual labour (other than public works): average daily wage'),
                             (45, 'Rs per 30 days (gross)', 'self-employed: average gross earnings, last 30 days')]:
        pages = [p for p in pdf_pages_with(S18['pdf'], rf'Table \({n}\)') if p > 300]
        acc = {}
        for pg in pages:
            txt = pdf_text(S18['pdf'], [pg])
            q = re.search(r'(July?- ?Sept? 2017|Oct- ?Dec 2017|Jan- ?Mar(?:ch)? 2018|Apr(?:il)?- ?June? 2018)', txt)
            if not q or 'all-India' not in txt:
                continue
            g = q.group(0)
            qlab = ('Jan-Mar 2018' if g.startswith('Jan') else 'Jul-Sep 2017' if g.startswith('Jul') else
                    'Oct-Dec 2017' if g.startswith('Oct') else 'Apr-Jun 2018')
            vals = numbers_after(txt, '| all-India |', 9, txt.find('| all-India |') - 1)
            est = numbers_after(txt, '(00)', 9, txt.find('(00)', txt.find('| all-India |')) - 1)
            for (s, x), v, e in zip(SEC_SEX, vals, est):
                out.append(rec(table=f'Table ({n})', period=f'{qlab} (quarter of PLFS 2017-18)', sector=s, sex=x,
                               age_group='all ages (CWS workers)', category_code=f'T{n}', category_name=measure,
                               category_level='earnings', value=v, unit=unit, source_url=S18['pdf_url'],
                               page_or_table=f'Table ({n}), Appendix A, PDF p.{pg}, all-India row'))
                acc.setdefault((s, x), []).append((v, e))
        for (s, x), lst in acc.items():
            if len(lst) == 4 and sum(e for _, e in lst) > 0:
                wavg = sum(v * e for v, e in lst) / sum(e for _, e in lst)
                out.append(rec(table=f'DERIVED from Table ({n})', period=S18['period'], sector=s, sex=x,
                               age_group='all ages (CWS workers)', category_code=f'T{n}', category_name=measure,
                               category_level='earnings', value=round(wavg, 2), unit=unit, source_url=S18['pdf_url'],
                               page_or_table=f'computed from Table ({n}) quarterly all-India rows, PDF pp.{pages[0]}-{pages[-1]}',
                               notes='derived by this project: quarterly means weighted by MoSPI estimated counts (00) in the same table'))
    write(out, 'plfs_earnings.csv')


# ================================================================== FORMALITY
def formality():
    out = []
    # Statement 9: % of non-agri workers in proprietary & partnership enterprises (2022-2025)
    pg = stmt_page(S25, 'Statement 9:')
    txt = pdf_text(S25['pdf'], [pg])
    seg = txt[txt.find('Statement 9:'):]
    vals = numbers_after(seg, '| (5) |', 36)  # 9 rows x 4 years (2025, 2024, 2023, 2022)
    for k, (s, x) in enumerate(SEC_SEX):
        for yr, v in zip(('2025', '2024', '2023', '2022'), vals[4 * k:4 * k + 4]):
            out.append(rec(table='Statement 9', period=CY[yr], sector=s, sex=x, age_group='all ages',
                           category_code='PP_SHARE_NONAGRI', category_name='% of non-agriculture workers (NIC 05-99) in proprietary & partnership enterprises (informal sector proxy)',
                           category_level='informal sector', value=v, unit='% of usual-status (ps+ss) non-agri workers',
                           source_url=S25['pdf_url'], page_or_table=f'Statement 9, PDF p.{pg}, AR PLFS 2025'))
    # Statement 10: RWS in non-agri: no written contract / no paid leave / no SSB (2022-2025)
    pg = stmt_page(S25, 'Statement 10:')
    txt = pdf_text(S25['pdf'], [pg])
    seg = txt[txt.find('Statement 10:'):]
    for yr in ('2025', '2024', '2023', '2022'):
        p0 = seg.find(f'PLFS {yr} |')
        for code, lab, name in [('NO_CONTRACT', 'had no written job contract', 'no written job contract'),
                                ('NO_PAID_LEAVE', 'not eligible for paid leave', 'not eligible for paid leave'),
                                ('NO_SSB', 'social security benefit', 'not eligible for any specified social security benefit')]:
            p = seg.find(lab, p0)
            vals = numbers_after(seg, lab, 9, p - 1)
            for (s, x), v in zip(SEC_SEX, vals):
                out.append(rec(table='Statement 10', period=CY[yr], sector=s, sex=x, age_group='all ages',
                               category_code=code, category_name=name, category_level='regular wage/salaried employees, non-agriculture',
                               value=v, unit='% of regular wage/salaried employees (ps+ss) in non-agri sector',
                               source_url=S25['pdf_url'], page_or_table=f'Statement 10, PDF p.{pg}, AR PLFS 2025'))
    # Table 36 all-India (2025, 2023-24), Table 35 all-India, Table 37 all-India
    T36 = [('NO_CONTRACT', 'no written job contract'), ('NO_PAID_LEAVE', 'not eligible for paid leave'),
           ('NO_SSB', 'without any specified social security benefit'),
           ('NONE_OF_3', 'not eligible for paid leave AND no written contract AND no SSB')]
    for S in (S25, S24):
        path, url, page = xls_src(S, 36)
        for title, rows in blocks(path):
            s, _, _ = title_sector_sex(title)
            r = all_india_row(rows)
            for k, x in enumerate(SEX3):
                for j, (c, nme) in enumerate(T36):
                    out.append(rec(table='Table (36)', period=S['period'], sector=s, sex=x, age_group='all ages',
                                   category_code=c, category_name=nme, category_level='regular wage/salaried employees, non-agriculture',
                                   value=num(r[1 + 4 * k + j]), unit='% of regular wage/salaried employees (ps+ss) in non-agri sector',
                                   source_url=url, page_or_table=page + ', all-India row'))
        path, url, page = xls_src(S, 35)
        for title, rows in blocks(path):
            s, x, _ = title_sector_sex(title)
            r = all_india_row(rows)
            for (c, nme), v in zip(ENT_TYPES + [('SAMPLE', 'sample workers (count)')], r[1:11]):
                out.append(rec(table='Table (35)', period=S['period'], sector=s, sex=x, age_group='all ages',
                               category_code=c, category_name=nme, category_level='enterprise type (non-agri workers, NIC 05-99)',
                               value=num(v), unit='count (sample workers)' if c == 'SAMPLE' else '% of usual-status non-agri workers',
                               source_url=url, page_or_table=page + ', all-India row'))
        path, url, page = xls_src(S, 37)
        for title, rows in blocks(path):
            s, x, _ = title_sector_sex(title)
            for r in rows:
                lab = re.sub(r'\s+', ' ', str(r[0])).strip()
                et = None
                for c, nme in ENT_TYPES:
                    key = nme.split()[0].lower()[:6]
                    if lab.lower().startswith(key) or (c == 'ET2' and lab.lower().startswith('government')) or \
                            (c == 'ET4' and lab.lower().startswith('public/private')) or (c == 'ET5' and lab.lower().startswith('co-operative')):
                        et = (c, lab)
                        break
                if lab.lower() == 'all':
                    et = ('ALL', 'all enterprise types')
                if not et:
                    continue
                for (sc, sn), v in zip(SIZE_COLS, r[1:7]):
                    out.append(rec(table='Table (37)', period=S['period'], sector=s, sex=x, age_group='all ages',
                                   category_code=et[0], category_name=et[1], category_level='enterprise type (non-agri workers)',
                                   cross_code=sc, cross_name=sn, value=num(v), unit='% of workers in the enterprise type (row %)',
                                   source_url=url, page_or_table=page))
    # 2017-18 Statements 18-21
    for st, code, name, unit in [
            ('Statement 19:', 'NO_CONTRACT', 'no written job contract', '% of regular wage/salaried employees (ps+ss) in non-agri sector'),
            ('Statement 20:', 'NO_PAID_LEAVE', 'not eligible for paid leave', '% of regular wage/salaried employees (ps+ss) in non-agri sector'),
            ('Statement 21:', 'NO_SSB', 'not eligible for any social security benefit', '% of regular wage/salaried employees (ps+ss) in non-agri sector')]:
        pg = stmt_page(S18, st)
        txt = pdf_text(S18['pdf'], [pg])
        seg = txt[txt.find(st):]
        vals = numbers_after(seg, 'PLFS (2017-18) |', 9, 0)
        for (s, x), v in zip(SEC_SEX, vals):
            out.append(rec(table=st.rstrip(':'), period=S18['period'], sector=s, sex=x, age_group='all ages', category_code=code,
                           category_name=name, category_level='regular wage/salaried employees, non-agriculture', value=v, unit=unit,
                           source_url=S18['pdf_url'], page_or_table=f'{st.rstrip(":")}, PDF p.{pg}, AR PLFS 2017-18'))
    write(out, 'plfs_formality.csv')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    status()
    broad_industry()
    education()
    earnings()
    formality()
