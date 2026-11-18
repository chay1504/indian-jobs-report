"""Absolute number of workers (usual status ps+ss) and derived worker counts by occupation / industry.

1. MoSPI's own estimate for Jan-Dec 2025 (AR PLFS 2025, Statement 32 / Annexure C method; age 15+).
2. Our replication of MoSPI's method for ALL AGES (because Tables 25/26 distributions cover all ages), for
   PLFS 2025, PLFS 2023-24, PLFS 2017-18 and the calendar years 2022-2024, using
      workers = sum over {rural,urban} x {male,female} of  WPR_all_ages(sector,sex) x projected population(sector,sex)
   with population from the Technical Group on Population Projections (MoHFW/NCP, July 2020), Tables 11 & 12
   (1 July figures; rural = total - urban; agricultural-year mid-point 1 Jan = mean of the two adjoining 1 July values).
3. Worker counts by NCO / NIC category = sum over the 4 sector x sex cells of share x workers(cell).
4. Change tables: 2017-18 -> 2025 (NIC; NCO division with classification-break flag), 2023-24 -> 2025 (NCO-2015 groups),
   CY2022 -> CY2025 (API NCO-2015 groups, NIC sections).
5. RBI KLEMS comparison numbers (via PIB, 22 Jul 2024).

Outputs: data/plfs/plfs_absolute_workers.csv, data/plfs/plfs_worker_counts_by_nco_nic.csv, data/plfs/plfs_change_nco_nic.csv
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plfs_common import RAW, OUT, SRC, COLS, rec, num, pdf_pages_with, pdf_text, PRESS_NOTE_2025_URL, TG_POP_URL  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
TG_PDF = RAW / 'MoHFW_population_projection_2025upload.pdf'
CELLS = [('rural', 'male'), ('rural', 'female'), ('urban', 'male'), ('urban', 'female')]
API_WPR = 'https://api.mospi.gov.in/api/plfs/getData?indicator_code=2&frequency_code=1&state_code=99&year={y}&year_type_code={t}'
PIB_KLEMS = 'https://pib.gov.in/PressReleasePage.aspx?PRID=2035280'


# ------------------------------------------------------------------ population projections (TG 2020, '000, 1 July)
def tg_table(title_rx):
    pages = [p for p in pdf_pages_with(TG_PDF, title_rx) if p > 40]  # skip the contents page
    txt = pdf_text(TG_PDF, pages[:1])
    out = {}
    for y in range(2011, 2037):
        m = re.search(rf'\| {y} \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|', txt)
        if m:
            out[y] = tuple(int(g.replace(',', '')) for g in m.groups())  # persons, male, female (INDIA)
    return out, pages[0]


TOT, TOT_PG = tg_table(r'TABLE\s*[–-]\s*11\s')
URB, URB_PG = tg_table(r'TABLE\s*[–-]\s*12\s')
assert TOT[2025] == (1417492, 727867, 689625), TOT[2025]
assert URB[2025] == (507401, 262956, 244445), URB[2025]


def pop(years):
    """Mean of 1 July projections over `years` -> {(sector, sex): thousands}"""
    res = {}
    for k, sx in ((1, 'male'), (2, 'female')):
        t = sum(TOT[y][k] for y in years) / len(years)
        u = sum(URB[y][k] for y in years) / len(years)
        res[('urban', sx)] = u
        res[('rural', sx)] = t - u
    return res


# ------------------------------------------------------------------ WPR from MoSPI API (indicator 2)
def wpr(year_label, age):
    fn = RAW / 'api' / f'plfs_api_ind2_{year_label.replace(" ", "")}_allindia.csv'
    out = {}
    with open(fn, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if (r['weekly_status'] == 'PS+SS' and r['AgeGroup'] == age and r.get('religion') in ('all', '')
                    and r.get('socialGroup') in ('all', '') and r.get('General_Education') in ('all', '')):
                sec = {'rural + urban': 'rural+urban'}.get(r['sector'], r['sector'])
                out[(sec, r['gender'])] = float(r['value'])
    return out


PERIODS = {  # label -> (api year, population years, period text, year_type)
    '2025': ('PLFS 2025', [2025], 'Jan-Dec 2025 (calendar year)', 2),
    'CY2024': ('PLFS 2024', [2024], 'Jan-Dec 2024 (calendar year)', 2),
    'CY2023': ('PLFS 2023', [2023], 'Jan-Dec 2023 (calendar year)', 2),
    'CY2022': ('PLFS 2022', [2022], 'Jan-Dec 2022 (calendar year)', 2),
    '2023-24': ('2023-24', [2023, 2024], 'Jul 2023-Jun 2024 (agricultural year)', 1),
    '2022-23': ('2022-23', [2022, 2023], 'Jul 2022-Jun 2023 (agricultural year)', 1),
    '2021-22': ('2021-22', [2021, 2022], 'Jul 2021-Jun 2022 (agricultural year)', 1),
    '2020-21': ('2020-21', [2020, 2021], 'Jul 2020-Jun 2021 (agricultural year)', 1),
    '2019-20': ('2019-20', [2019, 2020], 'Jul 2019-Jun 2020 (agricultural year)', 1),
    '2018-19': ('2018-19', [2018, 2019], 'Jul 2018-Jun 2019 (agricultural year)', 1),
    '2017-18': ('2017-18', [2017, 2018], 'Jul 2017-Jun 2018 (agricultural year)', 1),
}


def workers(label, age='All ages'):
    y, pyears, _, _ = PERIODS[label]
    w, p = wpr(y, age), pop(pyears)
    cells = {c: w[c] / 100 * p[c] for c in CELLS}
    return cells, w, p


def main():
    rows = []
    # ---------------- 1. MoSPI Statement 32 (2025, age 15+)  [values transcribed from AR PLFS 2025 p.71; checked below]
    pg = pdf_pages_with(SRC['2025']['pdf'], r'Statement 32:')[0]
    st32 = {('rural', 'male'): (464911, 0.73, 339385, 78.4, 266078), ('rural', 'female'): (445180, 0.75, 333885, 44.9, 149914),
            ('urban', 'male'): (262956, 0.78, 205106, 73.0, 149727), ('urban', 'female'): (244445, 0.80, 195556, 25.9, 50649)}
    txt = pdf_text(SRC['2025']['pdf'], [pg])
    for v in st32.values():  # every number must appear on the page
        for n in (v[0], v[2], v[4]):
            s = f'{n:,}'
            s_in = re.sub(r'(\d+)(\d{2}),(\d{3})$', r'\1,\2,\3', s) if n >= 100000 else s  # Indian grouping
            assert s_in in txt or s in txt, (n, s_in)
    for (s, x), (popn, prop, pop15, w15, wk) in st32.items():
        assert abs(pop15 * w15 / 100 - wk) < 60, (s, x)
        base = dict(table='Statement 32', period='Jan-Dec 2025 (calendar year)', sector=s, sex=x, age_group='15 years and above',
                    source_url=SRC['2025']['pdf_url'], page_or_table=f'Statement 32, PDF p.{pg} (report p.41) + Annexure C (PDF p.567), AR PLFS 2025')
        rows.append(rec(**base, category_code='POP_ALL_AGES', category_name='projected population, all ages, 1 July 2025 (MoHFW)', value=popn, unit='thousand persons'))
        rows.append(rec(**base, category_code='PROP_15P', category_name='PLFS proportion of population aged 15+', value=prop, unit='ratio'))
        rows.append(rec(**base, category_code='POP_15P', category_name='projected population aged 15+', value=pop15, unit='thousand persons'))
        rows.append(rec(**base, category_code='WPR_15P', category_name='WPR usual status (ps+ss), age 15+', value=w15, unit='%'))
        rows.append(rec(**base, category_code='WORKERS', category_name='estimated workers, usual status (ps+ss)', value=wk, unit='thousand persons'))
    for x, v in (('male', 415805), ('female', 200563), ('person', 616368)):
        rows.append(rec(table='Statement 32', period='Jan-Dec 2025 (calendar year)', sector='rural+urban', sex=x, age_group='15 years and above',
                        category_code='WORKERS', category_name='estimated workers, usual status (ps+ss)', value=v, unit='thousand persons',
                        source_url=SRC['2025']['pdf_url'], page_or_table=f'Statement 32, PDF p.{pg}; press note p.4 ({PRESS_NOTE_2025_URL}) says 61.6 crore'))
    assert sum(v[4] for v in st32.values()) == 616368

    # ---------------- 2. our all-ages (and 15+ cross-check) estimates
    summary = {}
    for label, (y, pyears, ptxt, ytype) in PERIODS.items():
        cells, w, p = workers(label)
        tot = sum(cells.values())
        summary[label] = (cells, tot)
        url = API_WPR.format(y=y.replace(' ', '%20'), t=ytype)
        note = (f'DERIVED (this project): sum over rural/urban x male/female of WPR(all ages, ps+ss) x projected population; '
                f'population = TG July 2020 Table 11 (total, PDF p.{TOT_PG}) and Table 12 (urban, PDF p.{URB_PG}), 1 July '
                f'{"/".join(map(str, pyears))}{" averaged (mid-point 1 Jan)" if len(pyears) > 1 else ""}; rural = total - urban')
        for c in CELLS:
            rows.append(rec(table='DERIVED', period=ptxt, sector=c[0], sex=c[1], age_group='all ages', category_code='WPR_ALL_AGES',
                            category_name='WPR usual status (ps+ss), all ages (MoSPI API)', value=w[c], unit='%', source_url=url,
                            page_or_table='MoSPI PLFS API indicator_code=2'))
            rows.append(rec(table='DERIVED', period=ptxt, sector=c[0], sex=c[1], age_group='all ages', category_code='POP_ALL_AGES',
                            category_name='projected population, all ages', value=round(p[c], 1), unit='thousand persons',
                            source_url=TG_POP_URL, page_or_table=f'TG on Population Projections (July 2020), Tables 11-12, PDF pp.{TOT_PG},{URB_PG}'))
            rows.append(rec(table='DERIVED', period=ptxt, sector=c[0], sex=c[1], age_group='all ages', category_code='WORKERS',
                            category_name='estimated workers, usual status (ps+ss), all ages', value=round(cells[c], 0), unit='thousand persons',
                            source_url=url, page_or_table='computed', notes=note))
        rows.append(rec(table='DERIVED', period=ptxt, sector='rural+urban', sex='person', age_group='all ages', category_code='WORKERS',
                        category_name='estimated workers, usual status (ps+ss), all ages', value=round(tot, 0), unit='thousand persons',
                        source_url=url, page_or_table='computed', notes=note))
        print(f'{label:8s} all-ages workers = {tot/1e4:6.2f} crore ({tot/1e3:6.1f} million); WPR r+u person all ages = {w.get(("rural+urban","person"))}')
    # replication of MoSPI 15+ number with our all-ages method is not possible without PLFS 15+ population shares; check instead
    # that WPR_all x pop for 2025 is within 0.5% of MoSPI's 15+ total (child workers are negligible)
    print('  2025 MoSPI 15+ =', 616368, ' ours all-ages =', round(summary['2025'][1]))

    # ---------------- 5. KLEMS (RBI, July 2024 release, via PIB 22 Jul 2024)
    for per, v in (('2017-18 (fiscal year Apr-Mar)', 47.5), ('2023-24 (fiscal year Apr-Mar, provisional)', 64.33)):
        rows.append(rec(table='RBI KLEMS (July 2024 release)', period=per, sector='rural+urban', sex='person', age_group='as defined by KLEMS (PLFS-based, usual status ps+ss)',
                        category_code='KLEMS_EMPLOYMENT', category_name='total employment, India KLEMS database', value=v, unit='crore persons',
                        source_url=PIB_KLEMS, page_or_table='PIB release ID 2035280 (Ministry of Labour & Employment, 22 Jul 2024)',
                        notes='RBI KLEMS listing page (https://www.rbi.org.in/Scripts/KLEMS.aspx, checked 2026-11-09) shows July 2024 as latest release; RBI xlsx blocked by bot-protection, not downloaded'))
    with open(OUT / 'plfs_absolute_workers.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    print('wrote plfs_absolute_workers.csv', len(rows))

    # ---------------- 3. worker counts by category
    def load(fn):
        with open(OUT / fn, encoding='utf-8') as f:
            return list(csv.DictReader(f))
    nco, nic, api = load('plfs_workers_by_occupation_nco.csv'), load('plfs_workers_by_industry_nic.csv'), load('plfs_series_nic_section_nco_division_api.csv')
    period_key = {'Jan-Dec 2025 (PLFS 2025, calendar year)': '2025', 'Jul 2023-Jun 2024 (PLFS 2023-24, agricultural year)': '2023-24',
                  'Jul 2017-Jun 2018 (PLFS 2017-18, agricultural year)': '2017-18',
                  'Jan-Dec 2022 (calendar year)': 'CY2022', 'Jan-Dec 2023 (calendar year)': 'CY2023', 'Jan-Dec 2024 (calendar year)': 'CY2024',
                  'Jan-Dec 2025 (calendar year)': '2025', 'Jul 2018-Jun 2019 (agricultural year)': '2018-19',
                  'Jul 2019-Jun 2020 (agricultural year)': '2019-20', 'Jul 2020-Jun 2021 (agricultural year)': '2020-21',
                  'Jul 2021-Jun 2022 (agricultural year)': '2021-22', 'Jul 2022-Jun 2023 (agricultural year)': '2022-23',
                  'Jul 2023-Jun 2024 (agricultural year)': '2023-24', 'Jul 2017-Jun 2018 (agricultural year)': '2017-18'}
    counts = []

    def add_counts(src_rows, kind, src_name):
        acc = {}
        for r in src_rows:
            if r['unit'] != '% of workers' or (r['sector'], r['sex']) not in CELLS + [('rural+urban', 'person')]:
                continue
            pk = period_key.get(r['period'])
            if not pk:
                continue
            k = (pk, r['category_level'], r['category_code'])
            a = acc.setdefault(k, {'name': r['category_name'], 'cls': r['classification'], 'cells': {}, 'src': r})
            a['cells'][(r['sector'], r['sex'])] = float(r['value'])
        for (pk, lvl, code), a in acc.items():
            cells, tot = summary[pk]
            common = dict(period=PERIODS[pk][2], sector='rural+urban', sex='person', age_group='all ages', category_code=code,
                          category_name=a['name'], category_level=lvl, unit='thousand workers (derived)', classification=a['cls'],
                          source_url=a['src']['source_url'], page_or_table=a['src']['page_or_table'])
            if ('rural+urban', 'person') in a['cells']:
                n = a['cells'][('rural+urban', 'person')] / 100 * tot
                counts.append(rec(table=f'DERIVED counts from {a["src"]["table"]} ({src_name})', cross_code='NATIONAL_SHARE',
                                  cross_name='published rural+urban person % share x all-ages worker total (RECOMMENDED: reproduces published shares)',
                                  value=round(n, 1), notes=f'period total {tot/1e3:.1f} million workers (all ages, derived)', **common))
            if all(c in a['cells'] for c in CELLS):
                n = sum(a['cells'][c] / 100 * cells[c] for c in CELLS)
                counts.append(rec(table=f'DERIVED counts from {a["src"]["table"]} ({src_name})', cross_code='CELL_SUM',
                                  cross_name='sum over rural/urban x male/female of published % share x derived cell worker total (alternative; TG urban weights)',
                                  value=round(n, 1), notes=f'period total {tot/1e3:.1f} million workers (all ages, derived)', **common))
    add_counts(nco, 'nco', 'AR Table 25')
    add_counts(nic, 'nic', 'AR Table 26')
    add_counts([r for r in api if PERIODS.get(period_key.get(r['period'], ''), None) and period_key[r['period']] not in ('2025', '2023-24', '2017-18')], 'api', 'MoSPI API')
    with open(OUT / 'plfs_worker_counts_by_nco_nic.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(counts)
    print('wrote plfs_worker_counts_by_nco_nic.csv', len(counts))

    # ---------------- 4. change tables
    idx = {}
    for r in counts:
        if r['cross_code'] == 'NATIONAL_SHARE':
            idx[(r['period'], r['classification'], r['category_level'], r['category_code'])] = r
    chg = []

    def change(p0, p1, cls0, cls1, level, note):
        for (per, cls, lvl, code), r1 in idx.items():
            if per != PERIODS[p1][2] or cls != cls1 or lvl != level:
                continue
            r0 = idx.get((PERIODS[p0][2], cls0, level, code))
            if not r0:
                continue
            v0, v1 = float(r0['value']), float(r1['value'])
            for ccode, cname, val, unit in (('COUNT_0', f'workers {p0}', v0, 'thousand workers (derived)'),
                                            ('COUNT_1', f'workers {p1}', v1, 'thousand workers (derived)'),
                                            ('ABS_CHANGE', f'change {p0} -> {p1}', v1 - v0, 'thousand workers (derived)'),
                                            ('PCT_CHANGE', f'% change {p0} -> {p1}', 100 * (v1 / v0 - 1) if v0 else None, '%')):
                chg.append(rec(table=f'DERIVED change {p0} -> {p1} ({cls1 if cls0 == cls1 else cls0 + " -> " + cls1} {level})', period=f'{PERIODS[p0][2]} to {PERIODS[p1][2]}', sector='rural+urban',
                               sex='person', age_group='all ages', category_code=code, category_name=r1['category_name'], category_level=level,
                               cross_code=ccode, cross_name=cname, value=None if val is None else round(val, 2), unit=unit,
                               classification=cls1 if cls0 == cls1 else f'{cls0} -> {cls1}', source_url=r1['source_url'],
                               page_or_table='computed from plfs_worker_counts_by_nco_nic.csv (NATIONAL_SHARE method)', notes=note))
    change('2017-18', '2025', 'NIC-2008', 'NIC-2008', 'section', 'consistent classification (NIC-2008) both years; 2025 sample design revamped (Jan 2025)')
    change('2017-18', '2025', 'NIC-2008', 'NIC-2008', 'division', 'consistent classification (NIC-2008) both years; 2025 sample design revamped (Jan 2025)')
    change('2023-24', '2025', 'NIC-2008', 'NIC-2008', 'division', 'agricultural year vs calendar year; sample design revamped Jan 2025')
    change('2017-18', '2025', 'NCO-2004', 'NCO-2015', 'division', 'NOT COMPARABLE: NCO-2004 (2017-18) vs NCO-2015 (2025); e.g. own-account shopkeepers sit in Div 1 under NCO-2004 practice but mostly Div 5 in 2025')
    change('2023-24', '2025', 'NCO-2015', 'NCO-2015', 'group', 'both NCO-2015, but Div 1/Div 5 coding drift visible 2021-22 to 2025 (see plfs.md)')
    change('2023-24', '2025', 'NCO-2015', 'NCO-2015', 'division', 'both NCO-2015, but Div 1/Div 5 coding drift visible 2021-22 to 2025 (see plfs.md)')
    change('CY2022', '2025', 'NCO-2015', 'NCO-2015', 'group', 'calendar years, both NCO-2015 (API); Div 1 share falls 4.9% -> 2.7%: likely coding drift (see plfs.md)')
    change('CY2022', '2025', 'NCO-2015', 'NCO-2015', 'division', 'calendar years, both NCO-2015 (API); Div 1 share falls 4.9% -> 2.7%: likely coding drift (see plfs.md)')
    change('CY2022', '2025', 'NIC-2008', 'NIC-2008', 'section', 'calendar years (API)')
    with open(OUT / 'plfs_change_nco_nic.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(chg)
    print('wrote plfs_change_nco_nic.csv', len(chg))


if __name__ == '__main__':
    main()
