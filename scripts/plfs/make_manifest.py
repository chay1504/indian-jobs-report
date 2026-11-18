"""Write data/plfs/plfs_sources_manifest.csv: every raw file used, its official URL, size and SHA-256."""
import csv, hashlib, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plfs_common import RAW, OUT, SRC, PRESS_NOTE_2025_URL, TG_POP_URL  # noqa: E402

URLS = {
    'press_note_AR_PLFS_2025.pdf': PRESS_NOTE_2025_URL,
    'AR_PLFS_2025_Jan-Dec2025_rev29052026.pdf': SRC['2025']['pdf_url'],
    'AR_PLFS_2023-24.pdf': SRC['2023-24']['pdf_url'],
    'AR_PLFS_2017-18.pdf': SRC['2017-18']['pdf_url'],
    'AR_PLFS_2018-19.pdf': 'https://www.mospi.gov.in/sites/default/files/publication_reports/Annual_Report_PLFS_2018_19_HL.pdf',
    'AR_PLFS_2019-20.pdf': 'https://www.mospi.gov.in/sites/default/files/publication_reports/Annual_Report_PLFS_2019_20F1.pdf',
    'AR_PLFS_2020-21.pdf': 'https://www.mospi.gov.in/sites/default/files/publication_reports/Annual_Report_PLFS_2020%2021_0.pdf',
    'AR_PLFS_2021-22.pdf': 'https://www.mospi.gov.in/sites/default/files/publication_reports/AnnualReportPLFS2021-22F1.pdf',
    'AR_PLFS_2022-23.pdf': 'https://www.mospi.gov.in/sites/default/files/publication_reports/AR_PLFS_2022_23N.pdf',
    'PLFS_KeyIndicators_CY2024.pdf': 'https://www.mospi.gov.in/sites/default/files/publication_reports/Key_employment_unemployment_indicators_PLFS_2024_final.pdf',
    'PLFS_Changes_in_2025.pdf': 'https://www.mospi.gov.in/sites/default/files/publication_reports/PLFS_changes_in_2025_Final.pdf',
    'MoHFW_population_projection_2025upload.pdf': TG_POP_URL,
    'PIB_PRID2035280_KLEMS_employment_22Jul2024.html': 'https://pib.gov.in/PressReleasePage.aspx?PRID=2035280',
    'RBI_KLEMS_listing_page_20261109.html': 'https://www.rbi.org.in/Scripts/KLEMS.aspx',
}
rows = []
for p in sorted(RAW.rglob('*')):
    if not p.is_file():
        continue
    rel = p.relative_to(RAW).as_posix()
    if rel.startswith('AR2025_appendixA_xlsx/'):
        url = SRC['2025']['xlsx_url'].format(n=p.stem.replace('Table__', ''))
    elif rel.startswith('AR2023-24_appendixA_xlsx/'):
        url = SRC['2023-24']['xlsx_url'].format(n=p.stem.replace('Table_', ''))
    elif rel.startswith('api/'):
        url = 'https://api.mospi.gov.in/api/plfs/getData (see api_query column inside the file)'
    else:
        url = URLS.get(rel, '')
    rows.append({'file': f'data/raw/plfs/{rel}', 'source_url': url, 'bytes': p.stat().st_size,
                 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'downloaded': '2026-11-09'})
with open(OUT / 'plfs_sources_manifest.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('wrote plfs_sources_manifest.csv', len(rows), 'files; missing URL:', [r['file'] for r in rows if not r['source_url']])
