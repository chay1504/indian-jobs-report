"""Derived 'who funds the state' shares, combining ITR statistics, Receipt Budget, CBDT time series and
Economic Survey 2025-26 Stat. Appendix Table 2.6. Writes data/tax/tax_dependence_summary.csv. All inputs are
typed here with their sources; arithmetic is shown in the 'formula' column."""
import os, pandas as pd
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'tax')
conc = pd.read_csv(os.path.join(OUT, 'individual_tax_concentration.csv'))
ind = pd.read_csv(os.path.join(OUT, 'corporate_tax_by_industry_FY2023-24.csv'))
top1_adults = conc[(conc.ay == '2023-24') & conc.metric.str.contains('top 1% of adults')].value_point.iloc[0] / 100
I = {  # Rs crore
 'ind_tax_AY2324': 677350.60,          # ITR Stats AY2023-24 Table 2.11 total
 'nonco_tax_AY2324': 1535151.08 - 716578.11,  # ITR Stats AY2023-24 p.6: all-status minus companies
 'gtr_FY2223': 3054191.44,             # Receipt Budget 2024-25 tr.pdf, Actual 2022-23 (sum of gross heads); BAG
 'gg_tax_FY2223': 4809044,             # Economic Survey 2025-26 Stat. App. Table 2.6, general govt tax receipts 2022-23
 'gtr_FY2425': 3796381.72,             # Receipt Budget 2026-27 tr.pdf / Budget at a Glance 2026-27 p.6, Actual 2024-25
 'gg_tax_FY2425RE': 6080098,           # Economic Survey 2025-26 Table 2.6, 2024-25 (RE)
 'nct_FY2425': 1235161,                # CBDT Time Series Table 1.1, Non-corporate tax incl. STT, 2024-25 (prov.)
 'stt_FY2425': 52196.86,               # Receipt Budget 2026-27 tr.pdf item 2.09, Actual 2024-25
 'cit_FY2425': 986766.59,              # Receipt Budget 2026-27 tr.pdf, Total-Corporation Tax Actual 2024-25
 'cit_share_top877': 0.5418,           # Receipt Budget 2026-27 Annex-7 Table 1 (FY2023-24)
}
it = ind[ind.sector_subsector.str.startswith('Computer')].gross_tax_payable_rs_crore.sum()
fin = ind[ind.sector_subsector.str.startswith('Financial Intermediation')].gross_tax_payable_rs_crore.sum()
indiv_share_nonco = I['ind_tax_AY2324'] / I['nonco_tax_AY2324']
est_ind_FY2425 = (I['nct_FY2425'] - I['stt_FY2425']) * indiv_share_nonco
rows = [
 ('Individuals share of non-company income-tax liability, AY2023-24', indiv_share_nonco, 'ind_tax_AY2324 / (all-status tax payable - company tax payable)'),
 ('Individual tax payable AY2023-24 as % of central gross tax revenue FY2022-23', I['ind_tax_AY2324'] / I['gtr_FY2223'], '677,351 / 30,54,191'),
 ('Individual tax payable AY2023-24 as % of general-govt (centre+states) tax receipts FY2022-23', I['ind_tax_AY2324'] / I['gg_tax_FY2223'], '677,351 / 48,09,044'),
 ('Tax paid by top 1% of adults (20+), AY2023-24, as % of central GTR FY2022-23', top1_adults * I['ind_tax_AY2324'] / I['gtr_FY2223'], f'{top1_adults:.4f} x 677,351 / 30,54,191'),
 ('Tax paid by top 1% of adults (20+), AY2023-24, as % of general-govt tax FY2022-23', top1_adults * I['ind_tax_AY2324'] / I['gg_tax_FY2223'], f'{top1_adults:.4f} x 677,351 / 48,09,044'),
 ('ESTIMATE: individual income tax FY2024-25 (Rs crore)', est_ind_FY2425, '(NCT 12,35,161 - STT 52,197) x individual share of non-company liability AY2023-24'),
 ('ESTIMATE: individual income tax as % of central GTR FY2024-25', est_ind_FY2425 / I['gtr_FY2425'], 'above / 37,96,382'),
 ('ESTIMATE: individual income tax as % of general-govt tax 2024-25 (RE)', est_ind_FY2425 / I['gg_tax_FY2425RE'], 'above / 60,80,098'),
 ('ESTIMATE: top 1% of adults share of central GTR FY2024-25 (using AY2023-24 concentration)', top1_adults * est_ind_FY2425 / I['gtr_FY2425'], 'top1 share x estimate / GTR'),
 ('ESTIMATE: top 1% of adults share of general-govt tax 2024-25 (RE)', top1_adults * est_ind_FY2425 / I['gg_tax_FY2425RE'], 'top1 share x estimate / GG tax'),
 ('Corporation tax as % of central GTR FY2024-25', I['cit_FY2425'] / I['gtr_FY2425'], '9,86,767 / 37,96,382'),
 ('ESTIMATE: ~877 companies with PBT>Rs500cr as % of central GTR FY2024-25', I['cit_share_top877'] * I['cit_FY2425'] / I['gtr_FY2425'], '0.5418 x 9,86,767 / 37,96,382 (FY23-24 share applied to FY24-25)'),
 ('Computer & related services (IT/ITeS/BPO) share of company gross tax payable FY2023-24', it / 899662.24, f'{it:,.2f} / 8,99,662.24'),
 ('Financial intermediation share of company gross tax payable FY2023-24', fin / 899662.24, f'{fin:,.2f} / 8,99,662.24'),
 ('ESTIMATE: IT/ITeS companies corporate tax as % of central GTR FY2024-25', (it / 899662.24) * I['cit_FY2425'] / I['gtr_FY2425'], 'IT share x CIT / GTR'),
]
d = pd.DataFrame(rows, columns=['metric', 'value', 'formula'])
d['value'] = d.value.apply(lambda v: round(v * 100, 2) if v < 5 else round(v, 0))
d['unit'] = d.metric.apply(lambda m: 'Rs crore' if 'Rs crore' in m else 'percent')
d.to_csv(os.path.join(OUT, 'tax_dependence_summary.csv'), index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 100)
print(d.to_string()); print('IT', it, 'fin', fin)
