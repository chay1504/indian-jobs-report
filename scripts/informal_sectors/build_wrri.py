"""Build All-India WRRI occupation wage table from Labour Bureau monthly CSV.

Input : data/raw/informal_sectors/labourbureau_wrri_all_states_monthly.csv
        (downloaded from https://labourbureau.gov.in/home/excel_download_ruralWage_data?state_id=101)
Output: data/informal_sectors/wrri_daily_wages.csv

Year labels in the source are agricultural years (July-June): e.g. "2025-2026" Jul..Dec = Jul-Dec 2025,
Jan..Jun = Jan-Jun 2026 (verified by month-to-month continuity of the All-India series).
Series break: from July 2025 the data come from the new CPI-AL/RL (2019=100) sample of 787 villages in
34 States/UTs (old: 600 villages, 20 states), so 2025-26 is not like-for-like with earlier years.
"""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
src = ROOT / 'data/raw/informal_sectors/labourbureau_wrri_all_states_monthly.csv'
out = ROOT / 'data/informal_sectors/wrri_daily_wages.csv'

df = pd.read_csv(src)
for c in ['Item', 'State', 'Occupation', 'Year', 'Month']:
    df[c] = df[c].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
ai = df[df.State == 'All India'].copy()

# keep the 25-occupation framework (Nov 2013 onwards)
OCC25 = [
    'Ploughing/Tilling workers',
    'Sowing(including Planting/Transplanting/ Weeding) workers)',
    'Harvesting/Winnowing/Threshing workers',
    'Picking workers (including Tea, Cotton, Tobacco and other commercial crops)',
    'Horticulture workers (including nursery growers)',
    'Fishermen-inland',
    'Fishermen-coastal/deep-sea',
    'Loggers and wood cutters',
    'Animal husbandry workers (including poultry workers, dairy workers & herdsman)',
    'Packaging labourers, agriculture',
    'General agricultural labourers (including watering/irrigation workers, etc.)',
    'Plant protection workers (applying pesticides, treating seeds, etc.',
    'Carpenter', 'Blacksmith', 'Mason', 'Weavers', 'Beedi Makers', 'Bamboo, cane basket weavers',
    'Handicraft workers', 'Plumbers', 'Electrician',
    'Construction workers (for roads, dams, industrial and project construction work & well diggers)',
    'LMV & Tractor drivers', 'Non-agricultural labourers(including porters, loaders)',
    'Sweeping/cleaning workers',
]
ai = ai[ai.Item.isin(OCC25)]
for s in ['Men', 'Women']:
    ai[s] = pd.to_numeric(ai[s], errors='coerce')   # '-' / '@' = not available -> NaN

long = ai.melt(id_vars=['Year', 'Month', 'Occupation', 'Item'], value_vars=['Men', 'Women'],
               var_name='sex', value_name='wage')

def yr_avg(year):
    g = long[long.Year == year].groupby(['Occupation', 'Item', 'sex'])['wage']
    return g.mean().round(2), g.count()

rows = []
yrs = ['2020-2021', '2024-2025', '2025-2026']
avgs = {y: yr_avg(y) for y in yrs}
latest = long[(long.Year == '2026-2027') & (long.Month == 'Aug')].set_index(['Occupation', 'Item', 'sex'])['wage']

for occ in OCC25:
    for sex in ['Men', 'Women']:
        grp = ai.loc[ai.Item == occ, 'Occupation'].iloc[0]
        key = (grp, occ, sex)
        r = {
            'sector': 'Agriculture' if grp.startswith('Agri') else 'Non-Agriculture',
            'occupation': occ,
            'sex': sex,
        }
        for y in yrs:
            m, n = avgs[y]
            tag = y.replace('-20', '_').replace('-', '_')
            r[f'avg_daily_wage_agyr_{y[:4]}_{y[-2:]}'] = m.get(key)
            r[f'months_{y[:4]}_{y[-2:]}'] = int(n.get(key, 0))
        r['daily_wage_aug_2026'] = latest.get(key)
        a20, a24, a25 = (r['avg_daily_wage_agyr_2020_21'], r['avg_daily_wage_agyr_2024_25'],
                         r['avg_daily_wage_agyr_2025_26'])
        r['pct_chg_2020_21_to_2024_25_same_series'] = round((a24 / a20 - 1) * 100, 1) if pd.notna(a20) and pd.notna(a24) else None
        r['pct_chg_2020_21_to_2025_26_series_break'] = round((a25 / a20 - 1) * 100, 1) if pd.notna(a20) and pd.notna(a25) else None
        r['annual_fte_2025_26_inr_x312days'] = round(a25 * 312) if pd.notna(a25) else None
        rows.append(r)

res = pd.DataFrame(rows)
res['unit'] = 'Rs per 8-hour day, nominal, All-India simple average of monthly All-India averages'
res['source_url'] = 'https://labourbureau.gov.in/rural-wages (Excel: https://labourbureau.gov.in/home/excel_download_ruralWage_data?state_id=101)'
res['notes'] = ('Agri-year = Jul-Jun. 2025-26 uses new 787-village/34-State sample (CPI-AL/RL 2019=100) from Jul 2025; '
                'earlier years 600 villages/20 States - level jump at Jul 2025 is partly sample change. '
                'annual_fte = daily x 312 days (26 days x 12) full-employment equivalent, an upper bound for casual workers.')
res.to_csv(out, index=False)
pd.set_option('display.width', 250)
print(res[res.sex == 'Men'][['occupation', 'avg_daily_wage_agyr_2020_21', 'avg_daily_wage_agyr_2024_25',
                             'avg_daily_wage_agyr_2025_26', 'daily_wage_aug_2026',
                             'pct_chg_2020_21_to_2024_25_same_series', 'pct_chg_2020_21_to_2025_26_series_break',
                             'months_2025_26']].to_string())
print(res[res.sex == 'Women'][['occupation', 'avg_daily_wage_agyr_2020_21', 'avg_daily_wage_agyr_2024_25',
                               'avg_daily_wage_agyr_2025_26', 'months_2020_21', 'months_2025_26']].to_string())
