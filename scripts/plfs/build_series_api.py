"""Time series of the distribution of usual-status (ps+ss) workers by NIC-2008 section and by NCO division
(plus NCO sub-division / 3-digit group where the API has them) from the official MoSPI PLFS API
(https://api.mospi.gov.in/api/plfs/getData, indicator_code=4 'Percentage distribution of workers', state=All India).
Raw API pulls are in data/raw/plfs/api/ (made by fetch_mospi_api.py).

Output: data/plfs/plfs_series_nic_section_nco_division_api.csv
"""
import csv
import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plfs_common import RAW, OUT, COLS, NCO2015, NCO2004, rec  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
API = 'https://api.mospi.gov.in/api/plfs/getData?indicator_code=4&frequency_code=1&state_code=99&year={y}&year_type_code={t}'
SECTOR = {'rural': 'rural', 'urban': 'urban', 'rural + urban': 'rural+urban'}
PERIOD = {
    '2017-18': 'Jul 2017-Jun 2018', '2018-19': 'Jul 2018-Jun 2019', '2019-20': 'Jul 2019-Jun 2020',
    '2020-21': 'Jul 2020-Jun 2021', '2021-22': 'Jul 2021-Jun 2022', '2022-23': 'Jul 2022-Jun 2023',
    '2023-24': 'Jul 2023-Jun 2024', 'PLFS 2022': 'Jan-Dec 2022', 'PLFS 2023': 'Jan-Dec 2023',
    'PLFS 2024': 'Jan-Dec 2024', 'PLFS 2025': 'Jan-Dec 2025'}
NCO2004_YEARS = {'2017-18', '2018-19', '2019-20', '2020-21'}  # AR 2021-22 para 3.3.7.1 (PDF p.99): NCO-2015 from Jul 2021


def main():
    out = []
    for f in sorted(glob.glob(str(RAW / 'api' / 'plfs_api_ind4_*_allindia.csv'))):
        with open(f, encoding='utf-8') as fh:
            rows = list(csv.DictReader(fh))
        for r in rows:
            if r['weekly_status'] != 'PS+SS' or r['sector'] not in SECTOR:
                continue
            y = r['year']
            ytype = 2 if y.startswith('PLFS') else 1
            period = PERIOD[y] + (' (calendar year)' if ytype == 2 else ' (agricultural year)')
            url = API.format(y=y.replace(' ', '%20'), t=ytype)
            others = {k: r.get(k, '') for k in ('broad_status_employment', 'enterprise_type', 'enterprise_size',
                                                  'employee_contract', 'broad_industry_work')}
            clean = all(v in ('', 'all', None) for v in others.values()) and not r.get('industry')
            nic, nco = r.get('industry_section') or '', r.get('nco_division') or ''
            if nic and nic != 'All' and (nco in ('', 'all')) and clean:
                code, name = nic.split('_', 1)
                out.append(rec(table='API indicator 4 (NIC section)', period=period, sector=SECTOR[r['sector']],
                               sex=r['gender'], age_group='all ages', category_code=code, category_name=name,
                               category_level='section', value=r['value'], unit='% of workers', classification='NIC-2008',
                               source_url=url, page_or_table='MoSPI PLFS API (eSankhyiki), indicator_code=4'))
            elif nco and nco not in ('all', 'total') and (nic in ('', 'All')) and clean:
                cls = 'NCO-2004' if y in NCO2004_YEARS else 'NCO-2015'
                names = NCO2004 if cls == 'NCO-2004' else NCO2015
                lab = re.sub(r'\s+', ' ', nco).strip()
                m = re.match(r'NCO Division ([0-9X]):', lab)
                note = ''
                if m:
                    code, level = m.group(1), 'division'
                    if cls == 'NCO-2015':
                        note = 'API labels this row with the NCO-2004 division title; PLFS used NCO-2015 from Jul 2021'
                elif lab.startswith('Division'):
                    code, level = lab.split()[-1], 'division'
                elif lab.startswith('Sub-division'):
                    code, level = lab.split()[-1], 'sub-division'
                elif re.fullmatch(r'\d{2,3}', lab):
                    code, level = lab, ('group' if len(lab) == 3 else 'sub-division')
                else:
                    continue
                name = names.get(code, '') if level != 'group' else f'group {code} (sub-division {code[:2]}: {names.get(code[:2], "")})'
                out.append(rec(table='API indicator 4 (NCO)', period=period, sector=SECTOR[r['sector']], sex=r['gender'],
                               age_group='all ages', category_code=code, category_name=name, category_level=level,
                               value=r['value'], unit='% of workers', classification=cls, source_url=url,
                               page_or_table='MoSPI PLFS API (eSankhyiki), indicator_code=4', notes=note))
    # de-duplicate (API sometimes repeats rows)
    seen, ded = set(), []
    for r in out:
        k = (r['table'], r['period'], r['sector'], r['sex'], r['category_level'], r['category_code'])
        if k in seen:
            continue
        seen.add(k)
        ded.append(r)
    with open(OUT / 'plfs_series_nic_section_nco_division_api.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(ded)
    print('wrote plfs_series_nic_section_nco_division_api.csv', len(ded))
    # quick check: sums by period for rural+urban person
    sums = {}
    for r in ded:
        if r['sector'] == 'rural+urban' and r['sex'] == 'person' and r['category_level'] in ('section', 'division'):
            k = (r['period'], r['table'])
            sums[k] = sums.get(k, 0) + float(r['value'])
    for k, v in sorted(sums.items()):
        print(f'  {k}: {v:.1f}')


if __name__ == '__main__':
    main()
