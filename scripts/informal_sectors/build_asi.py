"""Parse ASI 2024-25 Summary Results Statement 5A (p.39) and Statement 6 (p.41) -> NIC 2-digit table.
Source PDF: https://microdata.gov.in/NADA/index.php/catalog/309/download/6675 (ASI Summary Results 2024-25)
Output: data/informal_sectors/asi_2024_25_nic2.csv
"""
import sys
from pathlib import Path
import pdfplumber
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
pdf = pdfplumber.open(ROOT / 'data/raw/informal_sectors/mospi_asi_2024-25_summary_results.pdf')

# Statement 5A
t5 = pdf.pages[38].extract_tables()[0]
row = t5[1]
codes = row[0].split()
cols5 = ['factories_operating', 'fixed_capital_lakh', 'working_capital_lakh', 'invested_capital_lakh',
         'gross_pm_lakh', 'persons_engaged', 'input_lakh', 'output_lakh', 'gva_lakh', 'nva_lakh', 'gva_share_pct']
vals5 = {c: row[i + 2].split() for i, c in enumerate(cols5)}
assert all(len(v) == len(codes) for v in vals5.values()), [len(v) for v in vals5.values()]
s5 = pd.DataFrame({'nic2': codes, **vals5})

# Statement 6
t6 = pdf.pages[40].extract_tables()[0]
row = t6[1]
codes6 = row[0].split()
cols6 = ['fc_per_factory_lakh', 'persons_per_factory', 'workers_per_factory', 'output_per_factory_lakh',
         'nva_per_factory_lakh', 'output_per_person_rs', 'gva_per_person_rs', 'nva_per_person_rs', 'wages_per_worker_rs']
vals6 = {c: row[i + 2].split() for i, c in enumerate(cols6)}
assert all(len(v) == len(codes6) for v in vals6.values())
s6 = pd.DataFrame({'nic2': codes6, **vals6})

NAMES = {
 '01': 'Cotton ginning / seed processing (NIC 01632, 01640)', '08': 'Salt production (NIC 08932)',
 '10': 'Food products', '11': 'Beverages', '12': 'Tobacco products', '13': 'Textiles', '14': 'Wearing apparel',
 '15': 'Leather and related products', '16': 'Wood and wood products (excl. furniture)', '17': 'Paper and paper products',
 '18': 'Printing and reproduction of recorded media', '19': 'Coke and refined petroleum products',
 '20': 'Chemicals and chemical products', '21': 'Pharmaceuticals', '22': 'Rubber and plastics products',
 '23': 'Other non-metallic mineral products', '24': 'Basic metals', '25': 'Fabricated metal products',
 '26': 'Computer, electronic and optical products', '27': 'Electrical equipment', '28': 'Machinery and equipment n.e.c.',
 '29': 'Motor vehicles, trailers, semi-trailers', '30': 'Other transport equipment', '31': 'Furniture',
 '32': 'Other manufacturing (incl. jewellery)', '33': 'Repair and installation of machinery',
 '38': 'Waste collection, treatment, materials recovery', '58': 'Publishing activities', 'OT': 'Other industries'}
df = s5.merge(s6, on='nic2', how='outer')
for c in df.columns:
    if c != 'nic2':
        df[c] = pd.to_numeric(df[c])
df.insert(1, 'industry', df.nic2.map(NAMES))
df['workers_approx'] = (df.workers_per_factory * df.factories_operating).round(-2)
df['period'] = 'ASI 2024-25 (Apr 2024-Mar 2025)'
df['source'] = ('MoSPI ASI 2024-25 Summary Results, Statement 5A (p.39) & Statement 6 (p.41); '
                'https://microdata.gov.in/NADA/index.php/catalog/309/download/6675')
df = df.sort_values('persons_engaged', ascending=False)
df.to_csv(ROOT / 'data/informal_sectors/asi_2024_25_nic2.csv', index=False)
print(df[['nic2', 'industry', 'persons_engaged', 'workers_approx', 'wages_per_worker_rs', 'gva_per_person_rs']].to_string())
print('sum persons', df.persons_engaged.sum())
