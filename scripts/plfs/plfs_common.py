"""Shared helpers for building tidy PLFS CSVs from MoSPI Annual Report PDFs/Excel tables.

All inputs are official MoSPI files downloaded into data/raw/plfs/ (see research/plfs.md).
"""
import re
from pathlib import Path

import openpyxl
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / 'data' / 'raw' / 'plfs'
OUT = ROOT / 'data' / 'plfs'

COLS = ['table', 'period', 'sector', 'sex', 'age_group', 'category_code', 'category_name', 'category_level',
        'cross_code', 'cross_name', 'value', 'unit', 'classification', 'source_url', 'page_or_table', 'notes']

# ----------------------------------------------------------------------------------------------
# Source registry
# ----------------------------------------------------------------------------------------------
SRC = {
    '2025': dict(
        period='Jan-Dec 2025 (PLFS 2025, calendar year)',
        pdf=RAW / 'AR_PLFS_2025_Jan-Dec2025_rev29052026.pdf',
        pdf_url='https://www.mospi.gov.in/uploads/publications_reports/publications_reports1780040415321_0624fb13-fb47-40bc-b470-7c7e9635c3ef_PLFS_2025_F_REV_29052026.pdf',
        xlsx_dir=RAW / 'AR2025_appendixA_xlsx',
        xlsx_name='Table__{n}.xlsx',
        xlsx_url='https://www.mospi.gov.in/uploads/documents/publicationsReports/APPENDIX-A/Table__{n}.xlsx',
        label='PLFS Annual Report 2025 (Jan-Dec 2025), rev. 29-05-2026',
    ),
    '2023-24': dict(
        period='Jul 2023-Jun 2024 (PLFS 2023-24, agricultural year)',
        pdf=RAW / 'AR_PLFS_2023-24.pdf',
        pdf_url='https://www.mospi.gov.in/sites/default/files/publication_reports/AnnualReport_PLFS2023-24L2.pdf',
        xlsx_dir=RAW / 'AR2023-24_appendixA_xlsx',
        xlsx_name='Table_{n}.xlsx',
        xlsx_url='https://www.mospi.gov.in/sites/default/files/publication_reports/PLFS_AR23-24/Table_{n}.xlsx',
        label='PLFS Annual Report 2023-24 (Jul 2023-Jun 2024)',
    ),
    '2017-18': dict(
        period='Jul 2017-Jun 2018 (PLFS 2017-18, agricultural year)',
        pdf=RAW / 'AR_PLFS_2017-18.pdf',
        pdf_url='https://www.mospi.gov.in/sites/default/files/publication_reports/Annual%20Report%2C%20PLFS%202017-18_31052019.pdf',
        label='PLFS Annual Report 2017-18 (Jul 2017-Jun 2018)',
    ),
}
PRESS_NOTE_2025_URL = ('https://www.mospi.gov.in/uploads/latestReleases/latest_release_1774607827733_3e8964a9-268b-4cc9-'
                       'ad65-cfc8a9e32f08_Press_note_AR_PLFS_2025_23032025_V2.1_26032026_final.pdf')
TG_POP_URL = 'https://www.mohfw-dohfw.gov.in/static/uploads/2025/10/1c3c2048814bd3747f44e661f8547055.pdf'

SECTORS9 = [(s, x) for s in ('rural', 'urban', 'rural+urban') for x in ('male', 'female', 'person')]

# NCO-2015 division / sub-division titles: PLFS AR 2025, Appendix C, Annexure II (PDF pp. 572-573)
NCO2015 = {
    '1': 'Managers', '11': 'Chief Executives, Senior Officials and Legislators', '12': 'Administrative and Commercial Managers',
    '13': 'Production and Specialized Services Managers', '14': 'Hospitality, Retail and Other Services Managers',
    '2': 'Professionals', '21': 'Science and Engineering Professionals', '22': 'Health Professionals',
    '23': 'Teaching Professionals', '24': 'Business and Administrative Professionals',
    '25': 'Information and Communication Technology Professionals', '26': 'Legal, Social and Cultural Professionals',
    '3': 'Technicians and Associate Professionals', '31': 'Science and Engineering Associate Professionals',
    '32': 'Health Associate Professionals', '33': 'Business and Administration Associate Professionals',
    '34': 'Legal, Social, Cultural and Related Associate Professionals', '35': 'Information and Communications Technicians',
    '4': 'Clerks/Clerical Support Workers', '41': 'General and Keyboard Clerks', '42': 'Customer Services Clerks',
    '43': 'Numerical and Material Recording Clerks', '44': 'Other Clerical Support Workers',
    '5': 'Service and Sales Workers', '51': 'Personal Service Workers', '52': 'Sales Workers', '53': 'Personal Care Workers',
    '54': 'Protective Service Workers',
    '6': 'Skilled Agricultural, Forestry and Fishery Workers', '61': 'Market-Oriented Skilled Agricultural',
    '62': 'Market-Oriented Skilled Forestry, Fishery and Hunting Workers', '63': 'Subsistence Farmers, Fishers, Hunters and Gatherers',
    '7': 'Craft and Related Trades Workers', '71': 'Building and Related Trade Workers (Excluding Electricians)',
    '72': 'Metal, Machinery and Related Trades Workers', '73': 'Handicraft and Printing Workers',
    '74': 'Electrical and Electronics Trades Workers',
    '75': 'Food Processing, Woodworking, Garment and Other Craft and Related Trades Workers',
    '8': 'Plant and Machine Operators and Assemblers', '81': 'Stationary Plant and Machine Operators', '82': 'Assemblers',
    '83': 'Drivers and Mobile Plant Operators',
    '9': 'Elementary Occupations', '91': 'Cleaners and Helpers', '92': 'Agricultural, Forestry and Fishery Labourers',
    '93': 'Labourers in Mining, Construction, Manufacturing and Transport', '94': 'Food Preparation Assistants',
    '95': 'Street and Related Sales and Services Workers', '96': 'Refuse Workers and Other Elementary Workers',
}
# NCO-2004 division / sub-division titles: PLFS AR 2017-18, Chapter Two, Annexure II (PDF p. 70)
NCO2004 = {
    '1': 'Legislators, Senior Officials and Managers', '11': 'Legislators and Senior Officials', '12': 'Corporate Managers',
    '13': 'General Managers', '2': 'Professionals', '21': 'Physical, Mathematical and Engineering Science Professionals',
    '22': 'Life Science and Health Professionals', '23': 'Teaching Professionals', '24': 'Other Professionals',
    '3': 'Technicians and Associate Professionals', '31': 'Physical and Engineering Science Associate Professionals',
    '32': 'Life Science and Health Associate Professionals', '33': 'Teaching Associate Professionals',
    '34': 'Other Associate Professionals', '4': 'Clerks', '41': 'Office Clerks', '42': 'Customer Services Clerks',
    '5': 'Service Workers and Shop & Market Sales Workers', '51': 'Personal and Protective Service Workers',
    '52': 'Models, Sales Persons and Demonstrators', '6': 'Skilled Agricultural and Fishery Workers',
    '61': 'Market Oriented Skilled Agricultural and Fishery Workers', '62': 'Subsistence Agricultural and Fishery Workers',
    '7': 'Craft and related Trades Workers', '71': 'Extraction and Building Trades Workers',
    '72': 'Metal, Machinery and Related Trades Workers', '73': 'Precision, Handicraft, Printing and Related Trades Workers',
    '74': 'Other Craft and Related Trades Workers', '8': 'Plant and Machine Operators and Assemblers',
    '81': 'Stationary-Plant and Related Operators', '82': 'Machine Operators and Assemblers', '83': 'Drivers and Mobile Plant Operators',
    '9': 'Elementary Occupations', '91': 'Sales and Service Elementary Occupations', '92': 'Agricultural, Fishery and Related Labourers',
    '93': 'Labourers in Mining, Construction, Manufacturing and Transport', 'X': 'Workers not Classified by Occupations',
}


def rec(**kw):
    r = {c: '' for c in COLS}
    r.update({k: ('' if v is None else v) for k, v in kw.items()})
    return r


def num(v):
    """Parse a numeric cell/token; returns float or None ('-' / blank / text -> None)."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(',', '')
    if re.fullmatch(r'-?\d+(\.\d+)?', s):
        return float(s)
    return None


def xlsx_rows(path, sheet_index=0):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.worksheets[sheet_index]
    rows = []
    for row in ws.iter_rows(values_only=True):
        vals = ['' if v is None else (str(v).strip() if not isinstance(v, (int, float)) else v) for v in row]
        if any(v != '' for v in vals):
            rows.append(vals)
    return rows


def pdf_pages_with(pdf_path, pattern):
    d = pymupdf.open(pdf_path)
    rx = re.compile(pattern)
    return [i + 1 for i, p in enumerate(d) if rx.search(p.get_text())]


def page_range(pages):
    if not pages:
        return ''
    return f'PDF p.{pages[0]}' if len(pages) == 1 else f'PDF pp.{pages[0]}-{pages[-1]}'


def pdf_tokens(pdf_path, pages):
    """Whitespace-separated tokens of the given 1-based pages, keeping multi-word labels like 'Sub-division 11'."""
    d = pymupdf.open(pdf_path)
    toks = []
    for pg in pages:
        for line in d[pg - 1].get_text().split('\n'):
            line = line.strip()
            if not line:
                continue
            if re.match(r'^(Sub-division|Division|sub-total|Section)\b', line, re.I) or not re.search(r'\d', line):
                toks.append(line)
            else:
                toks.extend(line.split())
    return toks


def pdf_text(pdf_path, pages, sep=' | '):
    d = pymupdf.open(pdf_path)
    out = []
    for pg in pages:
        out.append(sep.join(x.strip() for x in d[pg - 1].get_text().split('\n') if x.strip()))
    return sep.join(out)


def numbers_after(text, marker, n, start=0):
    """Return the first n numeric tokens after `marker` (searching from `start`) in a ' | '-joined text."""
    i = text.find(marker, start)
    if i < 0:
        raise ValueError(f'marker not found: {marker!r}')
    toks = re.split(r'\s*\|\s*|\s+', text[i + len(marker):])
    out = []
    for t in toks:
        v = num(t)
        if v is not None:
            out.append(v)
            if len(out) == n:
                return out
    raise ValueError(f'only {len(out)} numbers after {marker!r}')
