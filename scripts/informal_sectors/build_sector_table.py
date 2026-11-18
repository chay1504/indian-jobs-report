"""Assemble data/informal_sectors/sector_headcount_pay.csv from the processed WRRI/ASI tables and
hand-transcribed figures (each with its source URL). Derived values are computed here, not typed.

Conventions
- pay_annual_inr: annual rupees, nominal. Daily wage rates are annualised as daily x 312 days
  (26 days x 12 months = full-employment equivalent; an UPPER BOUND for casual/seasonal workers).
- growth_5yr_pct: HEADCOUNT growth where an official like-for-like count exists (period stated in notes);
  blank otherwise. Wage growth is reported in notes, not in this column.
- education_typical: qualitative; none of the sources used here tabulate education by these occupations,
  so entries marked "(assumed)" are judgement calls to be replaced with PLFS microdata.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/informal_sectors/sector_headcount_pay.csv'
wr = pd.read_csv(ROOT / 'data/informal_sectors/wrri_daily_wages.csv')
asi = pd.read_csv(ROOT / 'data/informal_sectors/asi_2024_25_nic2.csv', dtype={'nic2': str})

DAYS = 312
U_WRRI = 'https://labourbureau.gov.in/rural-wages (Excel: https://labourbureau.gov.in/home/excel_download_ruralWage_data?state_id=101)'
U_ESHRAM = 'https://eshram.gov.in/dashboard (Power BI dashboard, Last Updated 09/11/2026)'
U_ASI = 'https://microdata.gov.in/NADA/index.php/catalog/309/download/6675 (ASI 2024-25 Summary Results, Statements 5A & 6)'
U_ASI_PIB = 'https://www.mospi.gov.in/uploads/latestReleases/latest_release_1790768522303_b1ee6ba9-c9d3-481a-b30e-45a24c7f3729_PIB_Note_ASI_2024-25_English.pdf'
U_ASUSE = 'https://www.mospi.gov.in/uploads/latestreleasesfiles/1777360756062-publications_reports1774347275480_658da785-11e1-4df3-9f02-27e08a8675f6_Factsheet_ASUSE_2025-f.pdf'
U_ASUSE_PN = 'https://www.mospi.gov.in/uploads/latestReleases/latest_release_1778063743760_e338f15d-195f-429f-892d-aa4155c7c4ce_Press_Note_ASUSE_2025_Report-English_%281%29.pdf'


def w(occ_prefix, sex='Men', col='avg_daily_wage_agyr_2025_26'):
    r = wr[(wr.occupation.str.startswith(occ_prefix)) & (wr.sex == sex)]
    assert len(r) == 1, occ_prefix
    return float(r[col].iloc[0])


def wg(occ_prefix, sex='Men'):
    """like-for-like WRRI wage growth 2020-21 -> 2024-25 (old series)"""
    return w(occ_prefix, sex, 'pct_chg_2020_21_to_2024_25_same_series')


def a(nic, col):
    return asi.loc[asi.nic2 == nic, col].iloc[0]


def wrri_note(occ_prefix, sex='Men'):
    return (f"WRRI {occ_prefix} ({sex.lower()}): Rs {w(occ_prefix, sex):.2f}/day avg Jul2025-Jun2026 "
            f"(new 787-village series); Rs {w(occ_prefix, sex, 'avg_daily_wage_agyr_2020_21'):.2f} in 2020-21; "
            f"same-series wage growth 2020-21->2024-25 {wg(occ_prefix, sex):+.1f}%")


rows = []
def add(**k):
    rows.append(k)

# ---------------- Agriculture & allied ----------------
add(sector='Agriculture', sub_sector='Cultivators (own-account farmers)',
    headcount=118_800_000, headcount_year='2011 (Census)',
    pay_annual_inr=13661 * 12,
    pay_measure='Avg monthly income per agricultural household (all sources) Rs 13,661 x 12; per HOUSEHOLD, not per worker',
    pay_year='2021-22 (NABARD NAFIS)',
    education_typical='Below secondary (assumed)',
    growth_5yr_pct=None,
    source_url='https://rsdebate.nic.in/bitstream/123456789/695682/2/PQ_247_21122018_U1304_p110_p111.pdf (RS reply 21-12-2018: Census 2011 = 118.8 mn cultivators + 144.3 mn agri labourers); https://static.pib.gov.in/WriteReadData/specificdocs/documents/2024/oct/doc20241010414001.pdf (NAFIS 2021-22)',
    notes=('Census 2011 cultivators ~118.8 mn (rounded). e-Shram (9 Nov 2026) registrations: Cultivator-Crop 21,786,794 + Cultivator-Vegetables 20,072,962 '
           '+ Cotton 318,646 + Fruit 202,371. Agri Census 2015-16: 146.45 mn operational holdings (138.35 mn in 2010-11, +5.86%), avg 1.08 ha; '
           '11th Agri Census 2021-22 fieldwork complete but national results not found published (Lok Sabha reply, Jul 2026). '
           'NSS 77th SAS 2018-19: Rs 10,218/month per agri household (paid-out approach: wages 4,063, crop 3,798, animals 1,582, non-farm 641, leasing 134) '
           '- PIB PRID 1842783. PLFS 2025: agriculture = 43.0% of workers (44.8% in 2024).'),
    confidence='medium (headcount stale; income per household)')

add(sector='Agriculture', sub_sector='Agricultural labourers (casual farm workers)',
    headcount=144_300_000, headcount_year='2011 (Census)',
    pay_annual_inr=round(w('General agricultural labourers') * DAYS),
    pay_measure='WRRI general agricultural labourer daily wage (men) x 312 days; FTE upper bound',
    pay_year='Jul 2025-Jun 2026',
    education_typical='Below primary/primary (assumed)',
    growth_5yr_pct=None, source_url=U_WRRI + '; ' + U_ESHRAM + '; https://rsdebate.nic.in/bitstream/123456789/695682/2/PQ_247_21122018_U1304_p110_p111.pdf',
    notes=(wrri_note('General agricultural labourers') + f"; women Rs {w('General agricultural labourers','Women'):.2f}/day. "
           'e-Shram registrations: Labourer-Agriculture 82,778,948 + Farm Hands & Labourers-Other 22,247,800 (= 105.0 mn). '
           'Census 2011 agricultural labourers ~144.3 mn (rounded). PLFS casual labour (non-public-works) avg daily earnings 2025: male Rs 455, female Rs 315.'),
    confidence='medium')

add(sector='Agriculture', sub_sector='Plantation labourers (tea/coffee/other)',
    headcount=2_414_228 + 447_050 + 69_547, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('Picking workers') * DAYS),
    pay_measure='WRRI picking workers (tea, cotton, tobacco etc.) daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Below primary/primary (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI,
    notes='e-Shram: Labourer-Plantation 2,414,228; Tea Plantation Worker 447,050; Coffee Plantation Worker 69,547 (registrations, not workforce). ' + wrri_note('Picking workers') + f"; women Rs {w('Picking workers','Women'):.2f}",
    confidence='low (registrations only)')

add(sector='Agriculture', sub_sector='Animal husbandry / dairy / poultry workers',
    headcount=3_478_076 + 2_254_962 + 1_431_489 + 945_493, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('Animal husbandry') * DAYS),
    pay_measure='WRRI animal husbandry workers daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Below primary/primary (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI,
    notes=('e-Shram: Dairy farmer 3,478,076; Dairy & livestock producers 2,254,962; Poultry farm workers 1,431,489; Dairy farm worker 945,493. '
           'Most livestock keeping is a subsidiary activity of farm households, so true involvement is far larger. 20th Livestock Census 2019: 535.78 mn livestock; '
           '21st census (2024-25 fieldwork) results not found. ' + wrri_note('Animal husbandry')),
    confidence='low (registrations only)')

add(sector='Agriculture', sub_sector='Fishers and fish farmers',
    headcount=30_000_000, headcount_year='2025 (ministry claim: livelihoods)',
    pay_annual_inr=round(w('Fishermen-inland') * DAYS),
    pay_measure='WRRI inland fishermen daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Below secondary (assumed)', growth_5yr_pct=None,
    source_url='https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251120700601.pdf; ' + U_WRRI,
    notes=('PIB World Fisheries Day factsheet (Nov 2025): sector supports ~30 million livelihoods (not a worker count); fish production 195 lakh t in 2024-25. '
           'e-Shram: Inland & coastal water fishery workers 1,548,649 registrations. ' + wrri_note('Fishermen-inland') +
           f"; coastal/deep-sea Rs {w('Fishermen-coastal'):.2f}/day (thin sample, jumped with new series)."),
    confidence='low')

# ---------------- Construction ----------------
add(sector='Construction', sub_sector='Construction workers (all, BOCW-registered)',
    headcount=57_300_000, headcount_year='2026 (cumulative registrations)',
    pay_annual_inr=round(w('Construction workers') * DAYS),
    pay_measure='WRRI construction worker (roads, dams, projects) daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Primary/middle (assumed)', growth_5yr_pct=None,
    source_url='https://indusaction.org/wp-content/uploads/2026/06/Final-Paper-VVGNLI-and-IA.docx.pdf; ' + U_WRRI + '; ' + U_ESHRAM,
    notes=('~5.73 crore registered with 35 State BOCW welfare boards (VVGNLI/Indus Action paper, Jun 2026; Labour Ministry earlier: ~5.7 crore as of 30 Jun 2024); '
           'registrations include lapsed/duplicate entries. Cess ~Rs 1.13 lakh crore collected, ~Rs 68,000 crore spent. e-Shram Construction sector 29,351,152. '
           'PLFS 2025: construction = 12.0% of workers. ' + wrri_note('Construction workers') + f"; women Rs {w('Construction workers','Women'):.2f}."),
    confidence='medium (headcount = registrations)')

add(sector='Construction', sub_sector='Masons and bricklayers (incl. helpers)',
    headcount=4_749_776 + 3_873_330 + 3_757_628, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('Mason') * DAYS), pay_measure='WRRI mason daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Primary/middle (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI,
    notes='e-Shram: Helper Mason 4,749,776; Bricklayer 3,873,330; Builders-traditional materials 3,757,628; Building construction labourers 7,163,968 (not included). ' + wrri_note('Mason'),
    confidence='medium (pay) / low (headcount)')

add(sector='Construction', sub_sector='Carpenters',
    headcount=2_211_765 + 211_140, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('Carpenter') * DAYS), pay_measure='WRRI carpenter daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Primary/middle (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI,
    notes='e-Shram: Carpenters & joiners (construction) 2,211,765 + Wood & Carpentry sector 211,140. ' + wrri_note('Carpenter'),
    confidence='medium (pay) / low (headcount)')

add(sector='Construction', sub_sector='Plumbers and electricians',
    headcount=552_803 + 549_122 + 293_007, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('Electrician') * DAYS), pay_measure='WRRI electrician daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Secondary + ITI (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI,
    notes=f"e-Shram: Plumbers & pipe fitters 552,803; Helper electrician 549,122; Lineman 293,007. {wrri_note('Electrician')}; plumber Rs {w('Plumbers'):.2f}/day.",
    confidence='medium (pay) / low (headcount)')

# ---------------- Manufacturing ----------------
w2021 = 22_261_548e5 / 12_594_563  # wages to workers (Rs lakh -> Rs) / workers, ASI 2020-21 (PIB note Table 3)
add(sector='Manufacturing (registered factories)', sub_sector='All ASI factory sector',
    headcount=20_996_913, headcount_year='2024-25 (ASI)',
    pay_annual_inr=228_037, pay_measure='ASI wages per worker (wages to workers / workers; excludes supervisory/managerial staff)',
    pay_year='2024-25', education_typical='Secondary (assumed)',
    growth_5yr_pct=round((20_996_913 / 16_089_700 - 1) * 100, 1),
    source_url=U_ASI + '; ' + U_ASI_PIB,
    notes=(f'Persons engaged 20,996,913 of which workers 16,653,810; contract workers = 42% of workers. Emoluments per person engaged Rs 382,451. '
           f'Growth column = persons engaged 2020-21 (16,089,700) -> 2024-25, i.e. 4 years. Wages per worker 2020-21 = Rs {w2021:,.0f} (derived) -> +{(228037/w2021-1)*100:.1f}%.'),
    confidence='high')

for nic, label, edu in [('10', 'Food products', 'Secondary (assumed)'), ('13', 'Textiles', 'Middle/secondary (assumed)'),
                        ('14', 'Wearing apparel (factories)', 'Middle/secondary (assumed)'),
                        ('15', 'Leather and footwear (factories)', 'Middle/secondary (assumed)'),
                        ('12', 'Tobacco products incl. beedi (factories)', 'Primary (assumed)'),
                        ('23', 'Non-metallic minerals (bricks, cement, ceramics)', 'Primary/middle (assumed)'),
                        ('24', 'Basic metals', 'Secondary/ITI (assumed)'), ('25', 'Fabricated metal products', 'Secondary/ITI (assumed)'),
                        ('29', 'Motor vehicles', 'Secondary/ITI (assumed)'), ('32', 'Other manufacturing incl. jewellery', 'Secondary (assumed)')]:
    add(sector='Manufacturing (registered factories)', sub_sector=f'NIC {nic} {label}',
        headcount=int(a(nic, 'persons_engaged')), headcount_year='2024-25 (ASI)',
        pay_annual_inr=int(a(nic, 'wages_per_worker_rs')), pay_measure='ASI wages per worker (NIC 2-digit)',
        pay_year='2024-25', education_typical=edu, growth_5yr_pct=None, source_url=U_ASI,
        notes=f"Persons engaged (all employees incl. supervisory); workers approx {int(a(nic,'workers_approx')):,}; GVA per person engaged Rs {int(a(nic,'gva_per_person_rs')):,}.",
        confidence='high')

add(sector='Manufacturing (unincorporated/informal)', sub_sector='ASUSE manufacturing establishments (all)',
    headcount=34_910_600, headcount_year='2025 (Jan-Dec, ASUSE)',
    pay_annual_inr=140_809, pay_measure='ASUSE emoluments per HIRED worker (hired workers are a minority; owners earn mixed income)',
    pay_year='2025', education_typical='Primary/middle (assumed)', growth_5yr_pct=None, source_url=U_ASUSE,
    notes=('Workers 3,49,106 hundred (2025) vs 3,36,977 hundred (ASUSE 2023-24, Oct23-Sep24): +3.60%. GVA per worker Rs 118,274 (proxy for owner earnings). '
           'Emoluments/hired worker 2023-24 Rs 134,850. Excludes construction and agriculture.'),
    confidence='high')

add(sector='Manufacturing (unincorporated/informal)', sub_sector='Tailoring / wearing apparel (informal units)',
    headcount=round(0.0867 * 128_051_800, -3), headcount_year='2025 (ASUSE)',
    pay_annual_inr=140_809, pay_measure='Proxy: ASUSE manufacturing emoluments per hired worker (no apparel-specific figure in factsheet)',
    pay_year='2025', education_typical='Middle (assumed)', growth_5yr_pct=None, source_url=U_ASUSE_PN + '; ' + U_ESHRAM,
    notes=('Headcount = 8.67% (share of ASUSE workers in "manufacture of wearing apparel", ASUSE 2025 press note Table 1) x 12,80,518 hundred workers. '
           '~22% of all female ASUSE workers are in apparel. e-Shram Apparel sector 21,223,905 registrations (Tailors/dressmakers 12,609,727; Sewers & embroiderers 6,234,928).'),
    confidence='medium')

add(sector='Manufacturing (unincorporated/informal)', sub_sector='Handloom weavers and allied workers',
    headcount=3_522_512, headcount_year='2019-20 (4th Handloom Census)',
    pay_annual_inr=round(w('Weavers') * DAYS), pay_measure='WRRI rural weavers daily wage (men) x 312 (handloom-specific earnings not published as a mean)',
    pay_year='Jul 2025-Jun 2026', education_typical='Below primary/primary (assumed)',
    growth_5yr_pct=None,
    source_url='https://mail.hepcindia.com/img/4th%20Handloom%20Census.pdf; ' + U_WRRI,
    notes=('26.74 lakh weavers + 8.49 lakh allied; >72% women. 67.1% of handloom worker households earn < Rs 5,000/month (Table 17, p.18); '
           '3rd census (2009-10) counted 43.32 lakh -> -18.7% over a decade. ' + wrri_note('Weavers') +
           f"; women Rs {w('Weavers','Women'):.2f} (anomalously above men in new series)."),
    confidence='medium')

add(sector='Manufacturing (unincorporated/informal)', sub_sector='Beedi rollers / tobacco workers',
    headcount=2_764_325, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('Beedi Makers', 'Women') * DAYS), pay_measure='WRRI beedi maker daily wage (WOMEN, who dominate beedi rolling) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Below primary (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI + '; ' + U_ASI,
    notes=(f"e-Shram Tobacco Industry sector 2,764,325. WRRI beedi makers men Rs {w('Beedi Makers'):.2f}/day, women Rs {w('Beedi Makers','Women'):.2f} (lowest of 25 WRRI occupations). "
           f"ASI NIC 12 tobacco factories: wages per worker Rs {int(a('12','wages_per_worker_rs')):,}/yr (lowest NIC)."),
    confidence='medium (pay) / low (headcount)')

add(sector='Manufacturing (unincorporated/informal)', sub_sector='Handicraft and carpet workers',
    headcount=2_396_583, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('Handicraft workers') * DAYS), pay_measure='WRRI handicraft workers daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Primary (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI, notes=wrri_note('Handicraft workers') + '. Bamboo/cane basket weavers: see WRRI table.',
    confidence='low (registrations only)')

add(sector='Manufacturing (unincorporated/informal)', sub_sector='Gems and jewellery workers',
    headcount=4_200_000, headcount_year='2025-11 (industry claim, GJEPC)',
    pay_annual_inr=int(a('32', 'wages_per_worker_rs')), pay_measure='Proxy: ASI NIC 32 (other manufacturing incl. jewellery) wages per worker',
    pay_year='2024-25', education_typical='Middle/secondary (assumed)', growth_5yr_pct=None,
    source_url='https://mail.indianjeweller.in/Indian-Jewellery-News/15684/index.html (GJEPC chairman, Nov 2025); ' + U_ESHRAM + '; ' + U_ASI,
    notes='GJEPC: "over 42 lakh" direct employment (also cited as 4.3 mn). e-Shram Gem & Jewellery sector 1,040,736 registrations. Industry claim, not survey.',
    confidence='low')

add(sector='Manufacturing (unincorporated/informal)', sub_sector='Leather and footwear workers',
    headcount=6_258_785, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=int(a('15', 'wages_per_worker_rs')), pay_measure='Proxy: ASI NIC 15 leather factories wages per worker',
    pay_year='2024-25', education_typical='Primary/middle (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_ASI,
    notes=f"e-Shram 'Leather Industry Works' 6,258,785 (likely includes cobblers/tanning/footwear). ASI leather factories employ {int(a('15','persons_engaged')):,}. No CLE figure verified.",
    confidence='low')

# ---------------- Trade & services ----------------
add(sector='Trade (unincorporated)', sub_sector='Shopkeepers, traders, shop assistants (ASUSE trade)',
    headcount=42_547_800, headcount_year='2025 (ASUSE)',
    pay_annual_inr=144_500, pay_measure='ASUSE trade emoluments per HIRED worker',
    pay_year='2025', education_typical='Secondary (assumed)', growth_5yr_pct=None, source_url=U_ASUSE + '; ' + U_ASUSE_PN,
    notes=('Workers 4,25,478 hundred (+6.93% vs 2023-24). "Other retail trade" alone = 27.55% of all ASUSE workers (~3.53 crore). '
           'GVA per worker Rs 171,363 (owners). Hired-worker emoluments 2023-24: Rs 133,206 (+8.5%).'),
    confidence='high')

add(sector='Trade (unincorporated)', sub_sector='Street vendors',
    headcount=7_550_000, headcount_year='2026-05 (PM SVANidhi cumulative beneficiaries)',
    pay_annual_inr=None, pay_measure='No official earnings series found',
    pay_year='', education_typical='Primary/middle (assumed)', growth_5yr_pct=None,
    source_url='https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/may/doc2026530879401.pdf; https://mohua.gov.in/static/uploads/2026/06/f319d6ae19b2b2b0a4ee05529818cc81.pdf; ' + U_ESHRAM,
    notes=('PIB factsheet (May 2026) and MoHUA (Jun 2026): >75.5 lakh beneficiaries availed >1.12 crore loans (>Rs 17,800 crore) since Jun 2020 - a lower bound on vendor numbers '
           '(a later figure of 76.95 lakh as of 12 Jul 2026 is reported in media; not verified). e-Shram "Street vendors, non-food products" 1,024,241 registrations.'),
    confidence='medium (as a beneficiary count)')

add(sector='Other services (unincorporated)', sub_sector='ASUSE other services (repair, personal services, food stalls, transport units etc.)',
    headcount=50_589_100, headcount_year='2025 (ASUSE)',
    pay_annual_inr=151_122, pay_measure='ASUSE other-services emoluments per HIRED worker',
    pay_year='2025', education_typical='Secondary (assumed)', growth_5yr_pct=None, source_url=U_ASUSE,
    notes='Workers 5,05,891 hundred (+7.40% vs 2023-24). "Other community, social & personal services" = 9.51% of ASUSE workers (~1.22 crore). GVA/worker Rs 170,668.',
    confidence='high')

add(sector='Other services (unincorporated)', sub_sector='Beauty and wellness workers',
    headcount=2_220_088, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=151_122, pay_measure='Proxy: ASUSE other-services emoluments per hired worker',
    pay_year='2025', education_typical='Secondary (assumed)', growth_5yr_pct=None, source_url=U_ESHRAM + '; ' + U_ASUSE,
    notes='e-Shram Beauty & Wellness sector registrations. No dedicated official wage series found.', confidence='low')

add(sector='Household services', sub_sector='Domestic workers (cooks, cleaners, housekeepers)',
    headcount=29_685_391, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('Sweeping/cleaning', 'Women') * DAYS),
    pay_measure='LOOSE PROXY: WRRI rural sweeping/cleaning workers daily wage (women) x 312; no domestic-worker wage series',
    pay_year='Jul 2025-Jun 2026', education_typical='Below primary/primary (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI,
    notes=('e-Shram "Domestic and Household Workers" 29,685,391, of which "Cooks, other" 25,185,986 (likely includes home-makers / mid-day-meal cooks; '
           'treat with caution); plus "Domestic housekeepers" 9,321,605 under Miscellaneous. Labour Bureau All-India Survey on Domestic Workers '
           '(launched Nov 2021) - results not found as of Nov 2026.'),
    confidence='low')

add(sector='Household services', sub_sector='Sanitation workers (sewer/septic tank) and waste pickers',
    headcount=90_915 + 251_756, headcount_year='2026 (NAMASTE profiled)',
    pay_annual_inr=round(w('Sweeping/cleaning') * DAYS), pay_measure='WRRI sweeping/cleaning workers daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Below primary (assumed)', growth_5yr_pct=None,
    source_url='https://www.newsonair.gov.in/namaste-scheme-achieves-milestone-in-advancing-dignity-and-safety-of-sanitation-workers/; https://www.pib.gov.in/blogs/blogsdescr.aspx?feaaid=565; ' + U_WRRI,
    notes=('NAMASTE profiled: 90,915 sewer/septic-tank workers (31 Mar 2026, MoSJE annual report as cited) and ~2.52 lakh waste pickers (Jul 2026, as reported; '
           'other sources say 1.3 lakh) - profiled counts are far below the true workforce. ' + wrri_note('Sweeping/cleaning')),
    confidence='low')

add(sector='Transport', sub_sector='Drivers (car/taxi/van, auto-rickshaw, truck, bus)',
    headcount=3_257_640 + 1_320_447 + 1_002_562 + 277_826, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=round(w('LMV & Tractor drivers') * DAYS), pay_measure='WRRI LMV & tractor driver daily wage (men) x 312',
    pay_year='Jul 2025-Jun 2026', education_typical='Middle/secondary (assumed)', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; ' + U_WRRI,
    notes=('e-Shram: Car/taxi/van drivers 3,257,640; Auto-rickshaw 1,320,447; Heavy truck & lorry 1,002,562; Bus 277,826; cycle-rickshaw/cart pullers 447,100 (excluded). '
           'Automobile & Transportation sector total 8,700,057. No official national count of truck/taxi drivers found. ' + wrri_note('LMV & Tractor drivers')),
    confidence='medium (pay) / low (headcount)')

add(sector='Transport', sub_sector='Gig and platform workers (delivery, ride-hailing etc.)',
    headcount=7_700_000, headcount_year='2020-21 (NITI Aayog estimate)',
    pay_annual_inr=None, pay_measure='No official earnings series found', pay_year='',
    education_typical='Secondary/higher secondary (assumed)', growth_5yr_pct=None,
    source_url='https://www.niti.gov.in/sites/default/files/2022-06/Policy_Brief_India%27s_Booming_Gig_and_Platform_Economy_27062022.pdf; https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc_9692_20260825_14270901.pdf',
    notes=('NITI Aayog (Jun 2022): 68 lakh (2019-20), 77 lakh (2020-21), projected 2.35 crore by 2029-30; ~26.6 lakh in retail/sales, ~13 lakh in transport. '
           'e-Shram: ~11.5 lakh platform workers registered (PIB factsheet, Aug 2026).'),
    confidence='low (model estimate)')

add(sector='Other services', sub_sector='Private security guards',
    headcount=None, headcount_year='',
    pay_annual_inr=None, pay_measure='No official earnings series found', pay_year='',
    education_typical='Secondary (assumed)', growth_5yr_pct=None,
    source_url='https://theprint.in/ani-press-releases/capsi-signs-mou-with-director-general-of-civil-defence/2664294; ' + U_ESHRAM,
    notes='Industry claims 7-10 million guards (CAPSI says 1 crore; ~30,592 PSARA-licensed agencies). No official count. e-Shram Private Security 472,579 registrations. Left blank deliberately.',
    confidence='low')

add(sector='Other services', sub_sector='Hotel, restaurant and tourism workers',
    headcount=4_511_654, headcount_year='2026-11 (e-Shram registrations)',
    pay_annual_inr=151_122, pay_measure='Proxy: ASUSE other-services emoluments per hired worker',
    pay_year='2025', education_typical='Secondary (assumed)', growth_5yr_pct=None, source_url=U_ESHRAM + '; ' + U_ASUSE,
    notes='e-Shram Tourism & Hospitality registrations only; true workforce (PLFS NIC 55-56) is larger - use PLFS agent figure.', confidence='low')

# ---------------- Public works ----------------
add(sector='Public works', sub_sector='MGNREGA workers (rural public works)',
    headcount=66_600_000, headcount_year='FY 2025-26 (individuals who worked)',
    pay_annual_inr=11_460, pay_measure='Avg MGNREGA earnings per HOUSEHOLD per year (42.92 days x avg wage Rs 267.0)',
    pay_year='FY 2025-26', education_typical='Below primary/primary (assumed)',
    growth_5yr_pct=None,
    source_url='https://libtech.in/wp-content/uploads/2026/05/LibTech_India_Tracker_FY-2025-26-6th-May-26_v2.docx.pdf; https://egazette.gov.in/WriteReadData/2026/273958.pdf',
    notes=('LibTech (from nrega.nic.in MIS, 7 Apr 2026; excludes NE states, Goa and small UTs): 6.66 crore workers & 4.91 crore households worked (-9.1%/-8.2% y/y), '
           '210.73 crore persondays (-21.5%), avg 42.92 days/household, avg wage Rs 267.0/day (Rs 252.7 in 2024-25), wage spend Rs 56,265 crore. '
           'Official LS reply: avg 43 days in 2025-26 vs 50 in 2024-25. MGNREGA repealed Dec 2025; replaced by VB-G RAM G Act 2025 from 1 Jul 2026: '
           'notified wage floor Rs 300/day, Haryana Rs 409, Goa 406, Kerala 401, Karnataka 382 (S.O. 3518(E), 30 Jun 2026); guarantee 125 days.'),
    confidence='medium')

# ---------------- Context row ----------------
add(sector='All unorganised', sub_sector='e-Shram registered unorganised workers (all sectors)',
    headcount=320_420_739, headcount_year='2026-11-09 (e-Shram)',
    pay_annual_inr=None, pay_measure='n/a', pay_year='', education_typical='Mixed', growth_5yr_pct=None,
    source_url=U_ESHRAM + '; https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc_9692_20260825_14270901.pdf',
    notes=('Registrations (Aadhaar-seeded, self-declared occupation; excludes income-tax payers and EPFO/ESIC members). 54.35% women. '
           'Agriculture 164,655,991 (51.4%); Domestic 29,685,391; Construction 29,351,152; Apparel 21,223,905; Misc 15,684,720. '
           '31.89 crore on 18 Aug 2026 (PIB). Context row - do not add to other rows.'),
    confidence='high (as registrations)')

df = pd.DataFrame(rows)
cols = ['sector', 'sub_sector', 'headcount', 'headcount_year', 'pay_annual_inr', 'pay_measure', 'pay_year',
        'education_typical', 'growth_5yr_pct', 'source_url', 'notes', 'confidence']
df = df[cols]
df['headcount'] = df['headcount'].astype('Int64')
df['pay_annual_inr'] = df['pay_annual_inr'].astype('Int64')
df.to_csv(OUT, index=False)
pd.set_option('display.width', 220); pd.set_option('display.max_colwidth', 60)
print(df[['sector', 'sub_sector', 'headcount', 'headcount_year', 'pay_annual_inr', 'growth_5yr_pct', 'confidence']].to_string())
