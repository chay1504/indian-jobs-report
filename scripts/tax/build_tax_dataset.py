"""Build tidy CSVs in data/tax/ from the official documents in data/raw/tax/ (+ the CBDT Time Series
FY2000-01..2024-25 PDF, which the official site serves only to browsers; pass its local path as argv[1]).

Run:  .venv/Scripts/python.exe -I scripts/tax/build_tax_dataset.py <path-to-time-series-2024-25.pdf>
Prereq: scripts/tax/parse_itr_stats.py already run for AY 2020-21..2023-24 (data/tax/itr_stats_all_tables_AY*.csv).
"""
import sys, os, re, csv, json
import pandas as pd
import pymupdf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RAW = os.path.join(ROOT, 'data', 'raw', 'tax')
OUT = os.path.join(ROOT, 'data', 'tax')
CR = 1e7  # 1 crore

ITR_URL = {
    '2020-21': 'https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Income-tax-statistics-i-t-return-AY_2020-21.pdf',
    '2021-22': 'https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Income-tax-statistics-i-t-return-AY_2021-22.pdf',
    '2022-23': 'https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Approved-version-Income-Tax-Return-Statistics-for-the-AY-2022-23-14062024.pdf',
    '2023-24': 'https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Approved-version-Income-Tax-Return-Statistics-for-the-AY-2023-24.pdf',
}
TS_URL = 'https://wm.incometaxindia.gov.in/documents/20117/6715095/Final-time-series-data.pdf/99b3f1e8-592e-c841-ee96-b4c3d7c31c25 (landing page https://www.incometaxindia.gov.in/w/direct_tax_collections_as_on_16.03.2025.pdf, released 21-11-2025)'

# Denominators (see research/tax.md for sources)
ADULTS_20PLUS_2022 = 922344832      # WIL WP 2024/09 Table 2 (UN-WPP adults 20+, 2022)
WORKFORCE = 60e7                    # ~60 crore, round figure given in the project brief (PLFS lane)


def load_itr(ay):
    return pd.read_csv(os.path.join(OUT, f'itr_stats_all_tables_AY{ay}.csv'))


# ---------------------------------------------------------------- 1. distribution files
def write_distributions():
    keep = {('Individual', 'Gross Total Income'), ('Individual', 'Salary Income'), ('Individual', 'Returned Income'),
            ('Individual', 'Tax Payable'), ('Company', 'Returned Income'), ('Company', 'Tax Payable'),
            ('All Taxpayers', 'Returned Income'), ('All Taxpayers', 'Tax Payable')}
    for ay in ITR_URL:
        df = load_itr(ay)
        df = df[[(s, v) in keep for s, v in zip(df.status, df.variable)]].copy()
        df['distribution_variable'] = df.variable.str.lower().str.replace(' ', '_')
        df['table'] = 'Table ' + df.table_no.astype(str) + ' "' + df.status + ' - Range of ' + df.variable + f' (AY {ay})", p.' + df.page.astype(str)
        df = df.rename(columns={'sum_rs_crore': 'sum_of_variable_rs_crore'})
        cols = ['ay', 'status', 'distribution_variable', 'range_label', 'lower_rs', 'upper_rs', 'n_returns',
                'sum_of_variable_rs_crore', 'avg_rs_lakh', 'source_url', 'table']
        df[cols].to_csv(os.path.join(OUT, f'itr_distribution_AY{ay}.csv'), index=False)


# ---------------------------------------------------------------- 2. concentration of individual tax
def top_down(bins):
    """bins: list of (lower, upper, n, total) sorted descending by lower. Yields cumulative (n, total)."""
    cn, ct = 0, 0.0
    out = []
    for lo, up, n, t in bins:
        out.append((lo, up, n, t, cn, ct))
        cn += n; ct += t
    return out


def people_for_share(bins, target_rs):
    """Number of top returns needed to reach target tax (Rs). Returns (point, low, high):
    high = within-bin equal-payment assumption (n*X/T); low = top payers in bin pay the bin upper bound."""
    for lo, up, n, t, cn, ct in top_down(bins):
        if ct + t >= target_rs:
            need = target_rs - ct
            high = cn + n * need / t
            low = cn + (need / up if up and up > 0 else n * need / t)
            return (low + high) / 2, low, high
    return None


def share_of_top_n(bins, k):
    """Tax share bounds paid by the top k returns."""
    for lo, up, n, t, cn, ct in top_down(bins):
        if cn + n >= k:
            m = k - cn
            low = ct + m * t / n                       # equal payment within bin
            high = ct + min(t, m * (up if up else t / n))  # top m pay bin upper bound
            return low, high
    return None


def concentration():
    rows, thr = [], []
    for ay, url in ITR_URL.items():
        df = load_itr(ay)
        tp = df[(df.status == 'Individual') & (df.variable == 'Tax Payable')]
        tot = tp[tp.range_label == 'Total'].iloc[0]
        n_all, tax_all = int(tot.n_returns), tot.sum_rs_crore * CR
        zero = int(tp[tp.range_label == '= 0'].n_returns.iloc[0])
        b = tp[(tp.range_label != 'Total') & (tp.lower_rs.notna()) & (tp.lower_rs != '')]
        b = b[b.range_label.str.startswith('>')]
        bins = sorted([(float(r.lower_rs), float(r.upper_rs) if str(r.upper_rs) not in ('', 'nan') else None,
                        int(r.n_returns), r.sum_rs_crore * CR) for r in b.itertuples() if r.n_returns > 0],
                      key=lambda x: -x[0])
        nonzero = sum(x[2] for x in bins)
        base = dict(ay=ay, income_year=f"FY {int(ay[:4])-1}-{ay[2:4]}", individual_returns=n_all,
                    returns_zero_tax=zero, returns_nonzero_tax=nonzero, zero_tax_share_pct=round(100 * zero / n_all, 2),
                    individual_tax_payable_rs_crore=round(tax_all / CR, 2))
        for share in (0.5, 0.75, 0.9, 0.99):
            pt, lo, hi = people_for_share(bins, share * tax_all)
            rows.append({**base, 'metric': f'returns needed for top {int(share*100)}% of individual tax payable',
                         'value_point': round(pt), 'value_low': round(lo), 'value_high': round(hi),
                         'pct_of_individual_filers': round(100 * pt / n_all, 3),
                         'pct_of_nonzero_taxpayers': round(100 * pt / nonzero, 3),
                         'pct_of_adults_20plus_2022': round(100 * pt / ADULTS_20PLUS_2022, 3),
                         'pct_of_workforce_60cr': round(100 * pt / WORKFORCE, 3),
                         'source_url': url, 'table': 'Table 2.11 Individual - Range of Tax Payable; Table 2.10/2.11 totals'})
        for label, k in [('top 1% of individual filers', 0.01 * n_all), ('top 10% of individual filers', 0.10 * n_all),
                         ('top 0.5% of adults(20+)', 0.005 * ADULTS_20PLUS_2022), ('top 1% of adults(20+)', 0.01 * ADULTS_20PLUS_2022),
                         ('top 2% of adults(20+)', 0.02 * ADULTS_20PLUS_2022), ('top 1% of workforce(60cr)', 0.01 * WORKFORCE),
                         ('top 2% of workforce(60cr)', 0.02 * WORKFORCE)]:
            r = share_of_top_n(bins, k)
            lo, hi = (r if r else (tax_all, tax_all))
            rows.append({**base, 'metric': f'share of individual tax payable paid by {label} (n={round(k):,})',
                         'value_point': round(100 * (lo + hi) / 2 / tax_all, 2), 'value_low': round(100 * lo / tax_all, 2),
                         'value_high': round(100 * hi / tax_all, 2), 'pct_of_individual_filers': round(100 * k / n_all, 3),
                         'pct_of_nonzero_taxpayers': round(100 * k / nonzero, 3),
                         'pct_of_adults_20plus_2022': round(100 * k / ADULTS_20PLUS_2022, 3),
                         'pct_of_workforce_60cr': round(100 * k / WORKFORCE, 3),
                         'source_url': url, 'table': 'Table 2.11 Individual - Range of Tax Payable'})
        # cumulative tax-payable table (exact at bin edges)
        for lo_, up_, n_, t_, cn, ct in top_down(bins):
            thr.append(dict(ay=ay, tax_payable_at_least_rs=lo_, returns_at_or_above=cn + n_,
                            tax_rs_crore_at_or_above=round((ct + t_) / CR, 2), share_of_individual_tax_pct=round(100 * (ct + t_) / tax_all, 2),
                            pct_of_individual_filers=round(100 * (cn + n_) / n_all, 3),
                            pct_of_adults_20plus_2022=round(100 * (cn + n_) / ADULTS_20PLUS_2022, 3),
                            pct_of_workforce_60cr=round(100 * (cn + n_) / WORKFORCE, 3), source_url=url,
                            table='Table 2.11 Individual - Range of Tax Payable (cumulated from top)'))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'individual_tax_concentration.csv'), index=False)
    pd.DataFrame(thr).to_csv(os.path.join(OUT, 'individual_tax_payable_cumulative.csv'), index=False)


# ---------------------------------------------------------------- 3. counts above income thresholds
def income_thresholds():
    rows = []
    for ay, url in ITR_URL.items():
        df = load_itr(ay)
        ri = df[(df.status == 'Individual') & (df.variable == 'Returned Income') & df.range_label.str.startswith('>')]
        bins = [(float(r.lower_rs), float(r.upper_rs) if str(r.upper_rs) not in ('', 'nan') else None, int(r.n_returns), r.sum_rs_crore * CR)
                for r in ri.itertuples()]
        n_all = int(df[(df.status == 'Individual') & (df.variable == 'Returned Income') & (df.range_label == 'Total')].n_returns.iloc[0])

        def above(x):
            n_exact = sum(n for lo, up, n, t in bins if lo >= x)
            inc = sum(t for lo, up, n, t in bins if lo >= x)
            method = 'exact (bin edge)'
            for lo, up, n, t in bins:
                if up and lo < x < up:  # linear-density interpolation matched to bin mean
                    w, mid, mean = up - lo, (lo + up) / 2, t / n
                    c = (mean - mid) * 12 / w ** 2      # slope/level ratio of linear density
                    a, b2 = x - mid, up - mid
                    frac = ((b2 - a) + c * (b2 ** 2 - a ** 2) / 2) / w
                    frac = min(max(frac, 0), 1)
                    n_exact += n * frac; method = f'linear-density interpolation in {lo/1e5:.1f}-{up/1e5:.1f} lakh bin (frac={frac:.3f})'
            return n_exact, inc, method
        for x in (5e5, 7e5, 10e5, 12e5, 15e5, 20e5, 25e5, 50e5, 1e7, 5e7, 1e9):
            n, inc, m = above(x)
            rows.append(dict(ay=ay, returned_income_above_rs=int(x), individual_returns=round(n), pct_of_individual_filers=round(100 * n / n_all, 3),
                             pct_of_adults_20plus_2022=round(100 * n / ADULTS_20PLUS_2022, 3), pct_of_workforce_60cr=round(100 * n / WORKFORCE, 3),
                             method=m, source_url=url, table='Table 2.10 Individual - Range of Returned Income'))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'individuals_above_income_thresholds.csv'), index=False)


# ---------------------------------------------------------------- 4. status-wise key values per AY
def status_summary():
    rows = []
    for ay, url in ITR_URL.items():
        df = load_itr(ay)
        for st in ['Individual', 'HUF', 'Firm', 'AOP/BOI', 'Company', 'All Taxpayers']:
            g = df[(df.status == st) & (df.range_label == 'Total')].set_index('variable')
            def v(name):
                m = [i for i in g.index if i.lower().replace('-', ' ') == name]
                return g.loc[m[0], 'sum_rs_crore'] if m else None
            salary_rows = df[(df.status == st) & (df.variable == 'Salary Income') & (df.range_label == '= 0')]
            n_tot = int(g.n_returns.iloc[0])
            rec = dict(ay=ay, status=st, n_returns=n_tot,
                       gross_total_income_rs_crore=v('gross total income'), returned_income_rs_crore=v('returned income'),
                       salary_income_rs_crore=v('salary income'), business_income_rs_crore=v('business income'),
                       tax_payable_rs_crore=v('tax payable'), source_url=url, table='Tables x.1-x.11 (Total rows)')
            if len(salary_rows):
                rec['returns_with_salary_income'] = n_tot - int(salary_rows.n_returns.iloc[0])
            z = df[(df.status == st) & (df.variable == 'Tax Payable') & (df.range_label == '= 0')]
            if len(z): rec['returns_zero_tax_payable'] = int(z.n_returns.iloc[0])
            rows.append(rec)
    d = pd.DataFrame(rows)
    d['salary_share_of_gti_pct'] = (100 * d.salary_income_rs_crore / d.gross_total_income_rs_crore).round(2)
    d.to_csv(os.path.join(OUT, 'itr_status_summary_by_AY.csv'), index=False)


# ---------------------------------------------------------------- 5. central tax revenue composition
RB = {  # file -> (columns, url)
    'receipt_budget_2024-25_tr.pdf': (['Actual 2022-23', 'BE 2023-24', 'RE 2023-24', 'BE 2024-25'], 'https://www.indiabudget.gov.in/budget2024-25/doc/rec/tr.pdf'),
    'receipt_budget_2025-26_tr.pdf': (['Actual 2023-24', 'BE 2024-25', 'RE 2024-25', 'BE 2025-26'], 'https://www.indiabudget.gov.in/budget2025-26/doc/rec/tr.pdf'),
    'receipt_budget_2026-27_tr.pdf': (['Actual 2024-25', 'BE 2025-26', 'RE 2025-26', 'BE 2026-27'], 'https://www.indiabudget.gov.in/doc/rec/tr.pdf'),
}
HEADS = [('Corporation Tax', 'Total-Corporation Tax'), ('Taxes on Income (incl. STT)', 'Total-Taxes on Income'),
         ('of which Securities Transaction Tax', '2.09.'), ('Wealth Tax', 'Total-Wealth Tax'),
         ('Commodity Transaction Tax', 'Total-Commodity Transaction Tax'), ('Customs', 'Total-Customs'),
         ('Union Excise Duties', 'Total-Union Excise Duties'), ('Service Tax', 'Total-Service Tax'),
         ('GST total', 'Total-Goods and Services Tax (GST)'), ('of which CGST', '8.01.'), ('of which IGST', '8.02.'),
         ('of which GST Compensation Cess', '8.03.'),
         ('Other Taxes and Duties on Commodities and Services', 'Total-Other Taxes and Duties on Commodities and Services'),
         ('Taxes of Union Territories', 'Total-Taxes of Union Territories'),
         ('Less NCCD to NDRF', 'Net-Less-NCCD'), ('Less States share', '12. Less-States'), ('Net Tax Revenue to Centre', 'Total-Tax Revenue')]


def rb_values(path):
    lines = []
    for p in pymupdf.open(path):
        lines += [l.strip() for l in p.get_text().split('\n')]
    num = re.compile(r'^-?[\d.]+$|^\.\.\.$')
    found = {}
    for i, l in enumerate(lines):
        for name, key in HEADS:
            if l.startswith(key) and name not in found:
                vals, j = [], i + 1
                while j < len(lines) and len(vals) < 4:
                    if re.match(r'^\d{4}$', lines[j]): pass
                    elif num.match(lines[j]): vals.append(0.0 if lines[j] == '...' else float(lines[j]))
                    elif vals: break
                    j += 1
                found[name] = vals
    return found


def revenue_composition():
    recs = []
    seen = set()
    # latest document wins for overlapping columns
    for f in ['receipt_budget_2026-27_tr.pdf', 'receipt_budget_2025-26_tr.pdf', 'receipt_budget_2024-25_tr.pdf']:
        cols, url = RB[f]
        vals = rb_values(os.path.join(RAW, f))
        for ci, col in enumerate(cols):
            if col in seen: continue
            seen.add(col)
            for name, _ in HEADS:
                v = vals.get(name)
                recs.append(dict(fiscal_year_col=col, head=name, rs_crore=(v[ci] if v and len(v) > ci else None),
                                 source_url=url, table='Receipt Budget, Statement "Tax Revenue" (tr.pdf)'))
    d = pd.DataFrame(recs)
    # Gross tax revenue = sum of gross heads (Corporation..UT taxes, excluding 'of which' rows and deductions)
    gross_heads = ['Corporation Tax', 'Taxes on Income (incl. STT)', 'Wealth Tax', 'Commodity Transaction Tax', 'Customs',
                   'Union Excise Duties', 'Service Tax', 'GST total', 'Other Taxes and Duties on Commodities and Services',
                   'Taxes of Union Territories']
    out = []
    for col, g in d.groupby('fiscal_year_col', sort=False):
        g = g.set_index('head')
        gtr = sum((g.loc[h, 'rs_crore'] or 0) for h in gross_heads)
        for h in g.index:
            r = g.loc[h].to_dict(); r['head'] = h; r['fiscal_year_col'] = col
            r['pct_of_gross_tax_revenue'] = round(100 * r['rs_crore'] / gtr, 2) if r['rs_crore'] is not None else None
            out.append(r)
        out.append(dict(fiscal_year_col=col, head='Gross Tax Revenue (computed: sum of gross heads)', rs_crore=round(gtr, 2),
                        pct_of_gross_tax_revenue=100.0, source_url=g.source_url.iloc[0], table='computed'))
        pit = (g.loc['Taxes on Income (incl. STT)', 'rs_crore'] or 0) - (g.loc['of which Securities Transaction Tax', 'rs_crore'] or 0)
        out.append(dict(fiscal_year_col=col, head='Taxes on Income excl. STT (individuals, HUF, firms, AOPs...)', rs_crore=round(pit, 2),
                        pct_of_gross_tax_revenue=round(100 * pit / gtr, 2), source_url=g.source_url.iloc[0], table='computed'))
        ind = sum((g.loc[h, 'rs_crore'] or 0) for h in ['Customs', 'Union Excise Duties', 'Service Tax', 'GST total',
                                                        'Other Taxes and Duties on Commodities and Services', 'Commodity Transaction Tax'])
        out.append(dict(fiscal_year_col=col, head='Indirect taxes (customs+excise+GST+service+other commodity taxes+CTT)', rs_crore=round(ind, 2),
                        pct_of_gross_tax_revenue=round(100 * ind / gtr, 2), source_url=g.source_url.iloc[0], table='computed'))
    pd.DataFrame(out).to_csv(os.path.join(OUT, 'central_tax_revenue_composition.csv'), index=False)


# ---------------------------------------------------------------- 6. CBDT time series FY2000-01..2024-25
def num_in(s):
    return float(s.replace(',', '').replace(' ', ''))


def time_series(ts_pdf):
    t = ' '.join(' '.join(p.get_text() for p in pymupdf.open(ts_pdf)).split())
    t = t.replace('4,73, 179', '4,73,179')
    t = t[t.find('Actual figures'):]  # skip table of contents
    N = r'(-?[\d,]+(?:\.\d+)?)#?@?\*?'
    yr = r'(\d{4}-\d{2})\*?@?'
    out = []
    s = t[t.find('1.1 Direct Tax Collection'):t.find('1.2 State')]
    for m in re.finditer(yr + r'\s+' + N + r'\s+' + N + r'\s+' + N + r'\s+' + N, s):
        out.append(dict(fy=m.group(1), table='1.1 Direct Tax Collection (Rs crore)', corporate_tax=num_in(m.group(2)),
                        non_corporate_tax_incl_STT=num_in(m.group(3)), other_direct_tax=num_in(m.group(4)), total_net_direct_tax=num_in(m.group(5))))
    s = t[t.find('1.5 Pre-Assessment'):t.find('1.6 Cost')]
    for m in re.finditer(yr + r'\s+' + N + r'\s+' + N + r'\s+' + N + r'\s+' + N + r'\s+' + N + r'\s+' + N, s):
        out.append(dict(fy=m.group(1), table='1.5 Pre/Post-assessment collections, gross (Rs crore)', TDS=num_in(m.group(2)), advance_tax=num_in(m.group(3)),
                        self_assessment_tax=num_in(m.group(4)), regular_assessment_tax=num_in(m.group(5)), other_receipts=num_in(m.group(6)),
                        total_gross_direct_tax=num_in(m.group(7))))
    s = t[t.find('1.4 Direct-Tax GDP'):t.find('1.5 Pre-Assessment')]
    for m in re.finditer(yr + r'\s+' + N + r'\s+' + N + r'\s+([\d.]+)%', s):
        out.append(dict(fy=m.group(1), table='1.4 Direct tax-GDP ratio', total_net_direct_tax=num_in(m.group(2)), gdp_current_rs_crore=num_in(m.group(3)),
                        direct_tax_gdp_pct=float(m.group(4))))
    s = t[t.find('1.3 Contribution'):t.find('1.4 Direct-Tax GDP')]
    for m in re.finditer(yr + r'\s+' + N + r'\s+' + N + r'\s+' + N + r'\s+([\d.]+)%', s):
        out.append(dict(fy=m.group(1), table='1.3 Direct vs indirect (Rs crore)', total_net_direct_tax=num_in(m.group(2)),
                        indirect_taxes_cbic=num_in(m.group(3)), total_taxes=num_in(m.group(4)), direct_share_pct=float(m.group(5))))
    d = pd.DataFrame(out); d['source_url'] = TS_URL
    d.to_csv(os.path.join(OUT, 'cbdt_time_series_collections.csv'), index=False)

    # Tables 1.7, 1.8, 1.9 (counts by PAN category); numbers in order of years
    cnt = []
    for tab, start, end, years in [
        ('1.7 Number of ITRs filed incl. revised (by FY of filing)', '1.7 Number of Income-Tax Returns Filed', '1.8 Number of Persons', [f'FY {y}-{str(y+1)[2:]}' for y in range(2013, 2025)]),
        ('1.8 Number of persons filing ITR (by FY of filing)', '1.8 Number of Persons', '1.9 Number of Taxpayers', [f'FY {y}-{str(y+1)[2:]}' for y in range(2013, 2025)]),
        ('1.9 Number of taxpayers (filers + TDS-deducted non-filers), by AY', '1.9 Number of Taxpayers', 'Note: * A', [f'AY {y}-{str(y+1)[2:]}' for y in range(2013, 2025)])]:
        s = t[t.find(start):]; s = s[:s.find(end, 10)] if end in s[10:] else s
        for cat, pat in [('INDIVIDUAL', r'INDIVIDUAL'), ('HUF', r'\bHUF\b'), ('FIRM', r'\bFIRM\b'), ('COMPANY', r'COMPANY'), ('TOTAL', r'TOTAL')]:
            m = re.search(pat + r'((?:\s+[\d,]{5,})+)', s)
            if not m: continue
            vals = [num_in(x) for x in m.group(1).split()]
            for y, v in zip(years, vals[:len(years)]):
                cnt.append(dict(table=tab, category=cat, period=y, count=int(v), source_url=TS_URL))
    pd.DataFrame(cnt).to_csv(os.path.join(OUT, 'cbdt_returns_filers_taxpayers.csv'), index=False)


# ---------------------------------------------------------------- 7. corporate concentration (Receipt Budget Annex 7, Table 1)
CORP = {
    'FY 2021-22 (AY 2022-23)': ('https://www.indiabudget.gov.in/budget2024-25/doc/rec/allrec.pdf', 'Receipt Budget 2024-25, Annexure-7, Table 1 (p.36)', 1025717, [
        ('Less than zero', 483246, None, 0.51, 0.49, None), ('Zero', 46832, None, 19.04, 8.62, None), ('Rs 0-1 crore', 422389, 1.91, 1.86, 1.98, 24.11),
        ('Rs 1-10 crore', 56472, 6.18, 5.66, 6.11, 23.01), ('Rs 10-50 crore', 11888, 8.95, 8.02, 8.75, 22.75), ('Rs 50-100 crore', 2110, 5.11, 4.54, 4.96, 22.58),
        ('Rs 100-500 crore', 2102, 15.31, 12.93, 14.19, 21.55), ('> Rs 500 crore', 678, 62.54, 47.44, 54.90, 20.42), ('All companies', 1025717, 100, 100, 100, 23.26)]),
    'FY 2022-23 (AY 2023-24)': ('https://www.indiabudget.gov.in/budget2025-26/doc/rec/allrec.pdf', 'Receipt Budget 2025-26, Annexure-7, Table 1 (p.36)', 1075866, [
        ('Less than zero', 493714, None, 0.69, 0.67, None), ('Zero', 48060, None, 20.89, 9.69, None), ('Rs 0-1 crore', 452076, 1.87, 1.82, 1.98, 24.52),
        ('Rs 1-10 crore', 63113, 6.15, 5.91, 6.35, 23.97), ('Rs 10-50 crore', 13405, 8.99, 7.90, 8.82, 22.79), ('Rs 50-100 crore', 2418, 5.22, 4.49, 5.04, 22.47),
        ('Rs 100-500 crore', 2337, 15.18, 12.65, 14.21, 21.75), ('> Rs 500 crore', 743, 62.59, 45.65, 53.24, 19.77), ('All companies', 1075866, 100, 100, 100, 23.24)]),
    'FY 2023-24 (AY 2024-25)': ('https://www.indiabudget.gov.in/doc/rec/allrec.pdf', 'Receipt Budget 2026-27, Annexure-7, Table 1 (p.38)', 1131290, [
        ('Less than zero', 513084, None, 0.49, 0.47, None), ('Zero', 53182, None, 21.61, 11.10, None), ('Rs 0-1 crore', 473572, 1.62, 1.59, 1.71, 23.68),
        ('Rs 1-10 crore', 69524, 5.59, 5.12, 5.63, 22.64), ('Rs 10-50 crore', 15448, 8.46, 7.43, 8.27, 21.96), ('Rs 50-100 crore', 2906, 5.20, 4.55, 5.01, 21.66),
        ('Rs 100-500 crore', 2697, 14.55, 12.19, 13.62, 21.04), ('> Rs 500 crore', 877, 64.58, 47.03, 54.18, 18.85), ('All companies', 1131290, 100, 100, 100, 22.47)]),
}


def corporate():
    rows = []
    for fy, (url, tab, ntot, data) in CORP.items():
        for lab, n, pbt, ti, cit, etr in data:
            rows.append(dict(financial_year=fy, pbt_range=lab, n_companies=n, pct_of_companies=round(100 * n / ntot, 3),
                             share_of_pbt_pct=pbt, share_of_total_income_pct=ti, share_of_cit_liability_pct=cit,
                             effective_tax_rate_pct=etr, source_url=url, table=tab))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'corporate_tax_concentration_by_PBT.csv'), index=False)

    # industry appendix FY 2023-24
    doc = pymupdf.open(os.path.join(RAW, 'receipt_budget_2026-27.pdf'))
    t = ' '.join(' '.join(doc[i].get_text() for i in range(50, 55)).split())
    t = t[t.find('S.No. Sector Sub-sector'):]
    pat = re.compile(r'(\d{1,2}) ([A-Z][A-Za-z ,;&\-()/.]+?) ([\d,]+) ([\d,]+\.\d+) ([\d,]+\.\d+) ([\d.]+)%')
    rows = []
    for m in pat.finditer(t):
        sno, desc, n, tax, pbt, etr = m.groups()
        rows.append(dict(s_no=int(sno), sector_subsector=desc.strip(), n_companies=int(n.replace(',', '')),
                         gross_tax_payable_rs_crore=float(tax.replace(',', '')), pbt_positive_rs_crore=float(pbt.replace(',', '')),
                         effective_tax_rate_pct=float(etr)))
    d = pd.DataFrame(rows).drop_duplicates('s_no').sort_values('s_no')
    total_tax = 899662.24
    d['share_of_corporate_gross_tax_payable_pct'] = (100 * d.gross_tax_payable_rs_crore / total_tax).round(3)
    d['source_url'] = 'https://www.indiabudget.gov.in/doc/rec/allrec.pdf'
    d['table'] = 'Receipt Budget 2026-27, Annexure-7, Appendix: ETR of companies across industry, FY 2023-24 (pp.51-55); Grand total gross tax payable Rs 8,99,662.24 cr'
    d.to_csv(os.path.join(OUT, 'corporate_tax_by_industry_FY2023-24.csv'), index=False)
    print('industry rows', len(d), 'sum tax', round(d.gross_tax_payable_rs_crore.sum(), 2), 'vs', total_tax)


if __name__ == '__main__':
    write_distributions(); concentration(); income_thresholds(); status_summary(); revenue_composition(); corporate()
    if len(sys.argv) > 1: time_series(sys.argv[1])
    print('done')
