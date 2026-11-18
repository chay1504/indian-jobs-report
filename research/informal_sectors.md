# India's mass, informal and blue-collar occupations: headcount and earnings

Lane: headcount and pay for informal, mass and blue-collar work. PLFS tables, tax, formal/white-collar, AI exposure, NCO/ILOSTAT and tax-occupation linkage belong to other agents.
Compiled 2026-11-09. All rupee figures are nominal.

Files
- `data/informal_sectors/sector_headcount_pay.csv`: 39 rows in the requested schema. Built by `scripts/informal_sectors/build_sector_table.py`.
- `data/informal_sectors/wrri_daily_wages.csv`: 25 WRRI occupations x 2 sexes. Covers agri-years 2020-21, 2024-25 and 2025-26, plus August 2026. Built by `build_wrri.py`.
- `data/informal_sectors/asi_2024_25_nic2.csv`: ASI 2024-25 by NIC 2-digit (persons engaged, wages per worker, GVA per person). Built by `build_asi.py`.
- `data/raw/informal_sectors/`: source PDFs and CSVs, plus a transcription of the e-Shram dashboard (`eshram_dashboard_snapshot_2026-11-09.csv`).

## Conventions used in the CSV (read before using it)
- **pay_annual_inr**
  - Daily wages are annualised as **daily × 312 days** (26 days × 12 months). This is a full-employment equivalent. For casual and seasonal workers it is an upper bound, because most do not get 312 days of paid work. The daily rate is always given in `notes`.
  - Some rows are not per-worker wages. NAFIS is per household. ASUSE gives emoluments per *hired* worker only. MGNREGA is earnings per household per year. `pay_measure` says which applies to each row.
- **growth_5yr_pct** is *headcount* growth. It is filled only where a like-for-like official count exists: the ASI row, 2020-21 to 2024-25, which is 4 years. Wage growth goes in `notes`.
- **headcount** mixes several kinds of counts, and `headcount_year` labels each one:
  - survey and census counts (ASI, ASUSE, Census 2011, Handloom Census), which are actual workforce estimates
  - registrations (e-Shram, BOCW) and scheme beneficiaries (PM SVANidhi, NAMASTE), which measure registry size, not workforce
  - industry claims (GJEPC, fisheries "livelihoods"), which are low confidence

  **Rows are not additive.** They overlap. For example, ASUSE apparel is a subset of ASUSE manufacturing, and e-Shram rows overlap BOCW.
- **education_typical**: none of the sources here tabulate education for these occupations. Every entry is marked "(assumed)" and should be replaced with PLFS microdata.

## Key findings

1. **None of the 25 rural occupations reaches Rs 2.3 lakh a year, even at full employment.** The best-paid, the rural mason, averaged Rs 722/day (men, Jul 2025 to Jun 2026). That is about Rs 2.25 lakh/yr at 312 days. Carpenters, plumbers and electricians earn Rs 650-670/day, or Rs 2.0-2.1 lakh/yr. Farm operations pay Rs 440-540/day for men and Rs 370-410/day for women. Beedi rolling pays least: women Rs 253/day.
2. **e-Shram holds 32.04 crore unorganised-worker registrations** (32,04,20,739 on 09/11/2026). **51.4% are in Agriculture** (16.47 crore). Next are Domestic and Household (2.97 crore), Construction (2.94 crore), Apparel (2.12 crore) and Miscellaneous (1.57 crore). Women are 54.35% of registrants.
   - Eligibility excludes income-tax payers and EPFO/ESIC members. So this whole registry is, by design, people outside the income-tax net.
3. **Registered factories (ASI 2024-25) employ 2.10 crore people.** That is up 30.5% from 1.61 crore in 2020-21. Average wages are **Rs 2.28 lakh per worker**, ranging from Rs 60,632 (tobacco and beedi factories) to Rs 4.25 lakh (petroleum refining). 42% of factory workers are contract workers.
4. **Unincorporated non-farm enterprises (ASUSE 2025) employ 12.81 crore people:** manufacturing 3.49 crore, trade 4.25 crore, other services 5.06 crore. A *hired* worker earned Rs 1.47 lakh/yr on average. But about 62% of these workers are working owners, not hired staff. GVA per worker was Rs 1.57 lakh.
5. **MGNREGA's last full year (FY 2025-26) shrank.**
   - Workers who got work: 6.66 crore. Persondays: 210.7 crore, down 21.5%. Average: 42.9 days per household at Rs 267/day, which is about **Rs 11,460 per household for the year**.
   - MGNREGA was repealed in December 2025. Its replacement, VB-G RAM G, started on 1 July 2026 with a **Rs 300/day wage floor** (Haryana Rs 409) and a 125-day guarantee.
6. **For the tax question:** every pay figure gathered here is between about Rs 0.8 lakh and Rs 2.3 lakh a year per worker or household. That is far below the Rs 12 lakh income on which the new regime levies no tax from FY 2025-26 (via the s.87A rebate; confirm with the tax agent). Mass informal work is essentially entirely outside the income-tax base.

## 1. Labour Bureau, Wage Rates in Rural India (WRRI)

**Source.** Labour Bureau "Rural Wages" dashboard: https://labourbureau.gov.in/rural-wages. The full monthly state × occupation × sex series from 1998 was downloaded as CSV from `https://labourbureau.gov.in/home/excel_download_ruralWage_data?state_id=101`. Saved as `labourbureau_wrri_all_states_monthly.csv`, with 118,091 rows; the latest month is **August 2026**. Methodology is in `labourbureau_wrri_brief.pdf`.
- Data come from village informants (Panchayat secretary, Patwari and others) in the CPI-AL/RL sample villages.
- Wages are normalised to an 8-hour day, and in-kind payments are converted to cash.
- The All-India figure is the sum of quotations divided by the number of quotations. It is **not population-weighted**, which The Wire has criticised.
- Each figure needs at least 5 quotations.

**Year labels are agricultural years (July-June).** I verified this from the series' month-to-month continuity. For example, "2025-2026" covers July 2025 to June 2026.

**Series break, July 2025.** WRRI moved to the new CPI-AL/RL (2019=100) sample, which has 787 villages in 34 States/UTs; the old sample had 600 villages in 20 States. The CPI-AL/RL note confirms the new series starts with July 2025. All-India wages jumped 8-15% between June and July 2025 (for example, ploughing went from Rs 465 to Rs 532). Much of that jump is the sample change, not real wage growth. So:
- the like-for-like 4-year change is 2020-21 to 2024-25 (old series)
- 2025-26 is the first full year of the new series
- `wrri_daily_wages.csv` also gives the 2020-21 to 2025-26 change and flags it as a series break

**All-India average daily wage, Rs per day.** Each figure is a simple mean of the 12 monthly All-India values, computed by me.

| Group | Occupation | Men 2020-21 | Men 2024-25 | Men 2025-26 | Men Aug-2026 | Men chg 20-21->24-25 (same series) | Women 2025-26 | Men x312 (Rs/yr) |
|---|---|---|---|---|---|---|---|---|
| Agri | Ploughing/tilling | 355 | 450 | 539 | 554 | +26.8% | 409 | 168,302 |
| Agri | Sowing/planting/weeding | 322 | 413 | 476 | 489 | +28.2% | 386 | 148,562 |
| Agri | Harvesting/winnowing/threshing | 317 | 411 | 482 | 494 | +29.6% | 390 | 150,350 |
| Agri | Picking (tea, cotton, tobacco...) | 286 | 377 | 440 | 442 | +31.6% | 372 | 137,224 |
| Agri | Horticulture/nursery | 313 | 413 | 463 | 467 | +32.1% | 371 | 144,590 |
| Agri | Fishermen-inland | 373 | 463 | 504 | 517 | +24.1% | 339 | 157,304 |
| Agri | Fishermen-coastal/deep-sea | 360 | 456 | 736 | 750 | +26.5% | n.a. | 229,754 |
| Agri | Loggers and wood cutters | 406 | 499 | 566 | 573 | +22.7% | 348 | 176,480 |
| Agri | Animal husbandry (dairy, poultry, herding) | 264 | 329 | 406 | 413 | +24.7% | 353 | 126,728 |
| Agri | Packaging labourers, agriculture | 295 | 377 | 463 | 471 | +28.1% | 392 | 144,490 |
| Agri | General agricultural labourer | 312 | 405 | 450 | 461 | +29.9% | 369 | 140,509 |
| Agri | Plant protection (pesticides) | 369 | 451 | 499 | 508 | +22.3% | 405 | 155,822 |
| Non-agri | Carpenter | 471 | 576 | 652 | 661 | +22.4% | n.a. | 203,277 |
| Non-agri | Blacksmith | 382 | 475 | 549 | 556 | +24.4% | 446 | 171,260 |
| Non-agri | Mason | 521 | 648 | 722 | 737 | +24.3% | 437 | 225,139 |
| Non-agri | Weavers | 336 | 386 | 465 | 467 | +14.7% | 538 | 145,096 |
| Non-agri | Beedi Makers | 224 | 263 | 342 | 343 | +17.5% | 253 | 106,701 |
| Non-agri | Bamboo, cane basket weavers | 286 | 338 | 420 | 423 | +18.2% | 315 | 131,115 |
| Non-agri | Handicraft workers | 386 | 438 | 488 | 516 | +13.4% | 423 | 152,190 |
| Non-agri | Plumbers | 480 | 592 | 670 | 679 | +23.2% | n.a. | 209,052 |
| Non-agri | Electrician | 466 | 577 | 661 | 671 | +23.8% | n.a. | 206,154 |
| Non-agri | Construction worker (roads, dams, projects) | 363 | 447 | 517 | 532 | +23.0% | 397 | 161,419 |
| Non-agri | LMV & Tractor drivers | 397 | 505 | 575 | 587 | +27.3% | n.a. | 179,363 |
| Non-agri | Non-agri labourer (porters, loaders) | 316 | 403 | 480 | 487 | +27.6% | 380 | 149,829 |
| Non-agri | Sweeping/cleaning workers | 264 | 338 | 412 | 424 | +28.1% | 359 | 128,450 |

**Data quirks**
- WRRI publishes no women's averages for carpenter, plumber, electrician or LMV driver (too few quotations). Coastal fishermen also have no women's figure.
- Two new-series values look anomalous. Coastal fishermen jumped from Rs 456 to Rs 736, probably because of a thin sample. Women weavers (Rs 538) are above men (Rs 465).
- The Labour Bureau release calendar schedules each month's data for the last working day of the next month, so September 2026 data was due on 30 Oct 2026. The downloadable series still ends at August 2026.
- Over 2020-21 to 2024-25, nominal wage growth was 13-32% across occupations. Craft occupations grew slowest: handicraft +13.4%, weavers +14.7%, beedi +17.5%, bamboo +18.2%. Farm operations grew fastest, at +27-32%. These are nominal figures; I have not deflated them.

**For comparison, from PLFS:** casual labourers (other than public works) earned on average Rs 455/day (men) and Rs 315/day (women) in calendar 2025. Source: PLFS Annual Report 2025 press note, already in `data/raw/plfs/`. The PLFS agent owns this data.

## 2. e-Shram: 32.04 crore registrations by occupation

**Source.** Public e-Shram dashboard, a Power BI embed linked from https://eshram.gov.in/dashboard. Labelled "Last Updated On 09/11/2026", read on 2026-11-09. A transcription is in `data/raw/informal_sectors/eshram_dashboard_snapshot_2026-11-09.csv`. The 30 sector rows sum exactly to the total of **320,420,739**.

Context from the PIB factsheet "5 Years of e-Shram Portal" (25 Aug 2026, `pib_eshram_factsheet_2026-08-25.pdf`):
- 31.89 crore registrations as of 18 Aug 2026; about 11.5 lakh platform workers.
- **Eligibility:** age 16+, unorganised sector, and **not an income-tax payer or EPFO/ESIC member**.

| Sector | Registrations | Biggest sub-occupations (registrations) |
|---|---:|---|
| Agriculture | 164,655,991 | Labourer-Agriculture 82.78 mn; Farm hands & labourers 22.25 mn; Cultivator-Crop 21.79 mn; Cultivator-Vegetables 20.07 mn; Dairy farmer 3.48 mn; Plantation labourer 2.41 mn; Dairy/livestock producers 2.25 mn; Fishery workers 1.55 mn; Poultry 1.43 mn |
| Domestic and Household Workers | 29,685,391 | "Cooks, other" 25.19 mn (*see caveat*); Domestic helpers/cleaners/launderers 3.89 mn; Kitchen porter 0.57 mn |
| Construction | 29,351,152 | Building construction labourers 7.16 mn; Helper mason 4.75 mn; Bricklayer 3.87 mn; Traditional builders 3.76 mn; Carpenters 2.21 mn; Concrete workers 1.97 mn; Painters 1.16 mn |
| Apparel | 21,223,905 | Tailors/dressmakers 12.61 mn; Sewers & embroiderers 6.23 mn; Hand sewers 1.40 mn |
| Miscellaneous | 15,684,720 | Domestic housekeepers 9.32 mn; Street vendors (non-food) 1.02 mn; Wholesale salesmen 0.67 mn; Warehouse pickers 0.59 mn |
| Automobile & Transportation | 8,700,057 | Car/taxi/van drivers 3.26 mn; Auto-rickshaw 1.32 mn; Truck/lorry 1.00 mn; Mechanics 0.97 mn; Cycle-rickshaw/cart 0.45 mn; Bus 0.28 mn |
| Capital Goods & Manufacturing | 6,566,769 | |
| Leather Industry Works | 6,258,785 | |
| Education | 5,429,546 | |
| Electronics & HW | 5,136,154 | |
| Tourism & Hospitality | 4,511,654 | |
| Healthcare | 3,677,926 | |
| Office Admin & Facility Mgmt | 3,201,338 | |
| Tobacco Industry | 2,764,325 | |
| Retail | 2,416,872 | |
| Handicrafts & Carpets | 2,396,583 | |
| Beauty & Wellness | 2,220,088 | |
| Food Industry | 1,912,044 | |
| Gem & Jewellery | 1,040,736 | |
| Professionals | 849,692 | |
| Printing; Private Security; Mining; Service; Glass & Ceramics; Wood & Carpentry; Textile & Handloom; Musical Instruments; Organised Retail; BFSI | 515,456; 472,579; 462,838; 310,534; 295,872; 211,140; 210,128; 121,463; 90,121; 46,880 | |

**Other dashboard figures**
- Gender: female 54.35%.
- Age: 18-40 is 55.29%; 40-50 is 24.12%; over 50 is 20.49%.
- Top states: Uttar Pradesh 84.9 mn, Bihar 32.6 mn, West Bengal 26.8 mn, Madhya Pradesh 19.7 mn, Maharashtra 18.9 mn.
- Channel: CSC 181.0 mn, self-registration 133.4 mn.

**Caveats**
- Occupation is self-declared, and one person picks one occupation.
- Registrations are not workforce counts. They undercount sectors with weak outreach and overcount some categories.
- "Cooks, other" (25.2 mn) is implausibly large for paid cooks. It probably includes home-makers and mid-day-meal cooks. Treat the Domestic category as low confidence.
- The dashboard shows registrations only, with no wages and no education by occupation.
- Sub-occupation lists are partly transcribed (the largest rows only). I read them from the expanded Power BI matrix, which re-collapses on interaction.

## 3. ASI 2024-25: registered factories by NIC 2-digit

**Sources**
- ASI 2024-25 Summary Results, released 30 Sep 2026: https://microdata.gov.in/NADA/index.php/catalog/309/download/6675. Statement 5A (p.39) gives persons engaged; Statement 6 (p.41) gives wages per worker.
- Factsheet: `mospi_asi_2024-25_factsheet.pdf`, Tables 1 and 2.
- PIB note: `mospi_asi_2024-25_pib_note.pdf`, Table 3, which has the 5-year series.

**Totals**

| | 2020-21 | 2024-25 |
|---|---:|---:|
| Persons engaged | 16,089,700 | 20,996,913 |
| Workers | 12,594,563 | 16,653,810 |
| Emoluments per person engaged | | Rs 382,451 |
| Wages per worker | Rs 176,757 (derived) | Rs 228,037 |

- Persons engaged grew 30.5% over 2020-21 to 2024-25; workers grew 32.2%.
- Emoluments per person engaged were Rs 365,748 in 2023-24.
- The 2020-21 wages-per-worker figure is my derivation: wages to workers of Rs 22,261,548 lakh divided by workers. Wages per worker therefore rose 29.0% to 2024-25.
- Contract workers are 42% of all workers (Table 3 of the factsheet).

**Largest employers, with wages per worker**

| NIC | Industry | Persons engaged | Wages per worker (Rs/yr) |
|---|---|---:|---:|
| 10 | Food products | 2,360,847 | 186,751 |
| 13 | Textiles | 1,757,216 | 194,753 |
| 24 | Basic metals | 1,582,424 | 292,597 |
| 29 | Motor vehicles | 1,479,953 | 276,289 |
| 14 | Wearing apparel | 1,460,403 | 175,845 |
| 28 | Machinery n.e.c. | 1,356,244 | 260,759 |
| 20 | Chemicals | 1,150,890 | 251,878 |
| 22 | Rubber & plastics | 1,110,793 | 227,093 |
| 23 | Non-metallic minerals | 1,093,417 | 184,313 |
| 21 | Pharmaceuticals | 1,091,685 | 303,589 |
| 15 | Leather | 437,396 | 189,003 |
| 12 | Tobacco (beedi etc.) | 418,540 | **60,632** |
| 19 | Coke & refined petroleum | 174,232 | **425,189** |

The full 29-row table is in `asi_2024_25_nic2.csv`. "Workers" there is an approximation: workers per factory × operating factories.

Confidence: high. ASI is a census plus sample survey of registered factories. It excludes unregistered and household manufacturing; those are covered by ASUSE.

## 4. ASUSE 2025 (Jan-Dec 2025): unincorporated non-farm enterprises

**Sources**
- Factsheet: `mospi_asuse_2025_factsheet.pdf`, Tables 1-6.
- Press notes, 24 Mar 2026 and 6 May 2026, including the detailed-report note.
- Coverage: manufacturing, trade and other services. Construction and agriculture are excluded.

| | Manufacturing | Trade | Other services | All |
|---|---:|---:|---:|---:|
| Workers 2025 | 3.491 crore | 4.255 crore | 5.059 crore | **12.805 crore** |
| Growth vs ASUSE 2023-24 (Oct 23-Sep 24) | +3.60% | +6.93% | +7.40% | +6.18% |
| Emoluments per hired worker 2025 (Rs/yr) | 140,809 | 144,500 | 151,122 | **146,550** |
| Emoluments per hired worker 2023-24 | 134,850 | 133,206 | 148,743 | 141,071 |
| GVA per worker 2025 (Rs) | 118,274 | 171,363 | 170,668 | 156,539 |

- The hired-worker figure includes employer welfare contributions, and covers both formal and informal hired workers.
- **Workers by status**, from the quarterly table for Oct-Dec 2025: working owners 62%, hired workers 24%, others including unpaid family 14%. In trade, 22% are unpaid family workers. For most workers, the "emoluments per hired worker" figure is therefore not their income; GVA per worker is a better proxy for owners.
- **Top activity categories, by share of workers in 2025:** other retail trade 27.55% (about 3.53 crore); other community, social and personal services 9.51% (about 1.22 crore); manufacture of wearing apparel 8.67% (about 1.11 crore). About 22% of female ASUSE workers are in apparel.
- **Trend:** workers were 10.96 crore in 2022-23 and 12.81 crore in 2025. Emoluments per hired worker rose from Rs 124,842 to Rs 146,550 (+17.4%) over the same period.

## 5. Agriculture: cultivators and labourers

- **Headcounts**
  - **Census 2011:** 118.8 mn cultivators and 144.3 mn agricultural labourers, 263.1 mn agricultural workers in all. Source: Rajya Sabha reply, 21 Dec 2018 (https://rsdebate.nic.in/bitstream/123456789/695682/2/PQ_247_21122018_U1304_p110_p111.pdf). This is the last full count of the split.
  - **e-Shram (Nov 2026):** 105.0 mn registered as agricultural or farm labourers, and 42.4 mn as cultivators.
  - **PLFS 2025:** agriculture is 43.0% of all workers, down from 44.8% in 2024. The PLFS agent has the status-wise split.
- **Operational holdings**
  - Agriculture Census 2015-16: **146.45 mn holdings**, up 5.86% from 138.35 mn in 2010-11. Average holding size 1.08 ha, down from 1.15 ha. Sources: parliamentary replies and PIB.
  - The 11th Agriculture Census (2021-22) has finished all three phases of fieldwork (Lok Sabha reply, 22 Jul 2026). I found **no published national results**.
- **Farm-household income**
  - **NSS 77th round SAS, Jul 2018-Jun 2019:** Rs 10,218 per month per agricultural household, on the paid-out expenses approach. Components: wages 4,063; net crop receipts 3,798; animals 1,582; non-farm business 641; leasing out land 134. On the paid-out plus imputed approach it is Rs 8,337. There were 9.31 crore agricultural households. Source: PIB PRID 1842783.
  - **NABARD NAFIS 2021-22:** Rs 13,661 per month per agricultural household, versus Rs 11,438 for non-agricultural households. About one-third comes from cultivation. Source: `pib_nafis_2021-22_2024-10.pdf`.
  - Both figures are **per household**, with about 1.5-2 earners each. They are not per-worker figures.
- **Livestock:** the 20th Livestock Census (2019) counted 535.78 mn livestock. The 21st census ran fieldwork in 2024-25; **results not found**.
- **Fisheries:** PIB's World Fisheries Day factsheet (Nov 2025) says the sector supports about 30 mn livelihoods and produced 195 lakh tonnes in 2024-25. That is a ministry livelihood claim, not a worker count. e-Shram has 1.55 mn fishery-worker registrations. I did not locate the Handbook of Fisheries Statistics fisher-population table.

## 6. Construction

- **BOCW welfare boards**
  - About **5.73 crore** registered workers across 35 boards. Cess collected: about Rs 1.13 lakh crore. Disbursed: about Rs 68,000 crore. Unspent: about Rs 63,000 crore. Source: VVGNLI and Indus Action paper, June 2026 (`indusaction_vvgnli_bocw_paper_2026.pdf`). The Labour Ministry's earlier figure was about 5.7 crore as of 30 Jun 2024.
  - These are cumulative registrations and include lapsed entries.
- **Other counts:** e-Shram Construction has 2.94 crore registrations. In PLFS 2025, construction is 12.0% of all workers.
- **Pay (WRRI 2025-26, men):** construction worker Rs 517/day; mason Rs 722; carpenter Rs 652; plumber Rs 670; electrician Rs 661; non-agricultural labourer Rs 480. Women construction workers earn Rs 397/day.

## 7. MGNREGA and VB-G RAM G

**FY 2025-26.** Source: LibTech India tracker, 8 May 2026, using nrega.nic.in MIS data as of 7 Apr 2026 (`libtech_mgnrega_tracker_fy2025-26_2026-05-06.pdf`). It excludes the NE states, Goa and small UTs.

| | FY 2024-25 | FY 2025-26 |
|---|---:|---:|
| Registered households | 14.98 crore | 15.46 crore |
| Households that worked | 5.35 crore | 4.91 crore |
| Workers employed | 7.33 crore | 6.66 crore |
| Persondays | 268.44 crore | 210.73 crore |
| Days per household | 50.18 | 42.92 |
| Households completing 100 days | 0.37 crore | 0.22 crore |
| Average wage (Rs/day) | 252.7 | 267.0 |
| Earnings per household (Rs/yr) | 12,680 | **11,460** |
| Wage spend (Rs crore) | 67,835 | 56,265 |

The official Lok Sabha reply gives an average of 43 days in 2025-26 versus 50 in 2024-25, which is consistent.

**VB-G RAM G Act 2025**
- MGNREGA was repealed in December 2025.
- Wage rates from 1 Jul 2026 were notified in Gazette S.O. 3518(E), 30 Jun 2026 (`egazette_vbgramg_wage_rates_2026.pdf`).
- Floor: **Rs 300/day** in most states. Higher rates: Haryana 409, Goa 406, Kerala 401, Karnataka 382, Himachal scheduled areas 375, Nicobar 367, Punjab 360, Andaman 348, Tamil Nadu 345, Maharashtra 317, Andhra Pradesh 312, Telangana 308. Three high-altitude Sikkim gram panchayats get 450.
- Media report the national average rising from Rs 298.8 to Rs 327.4. That figure is secondary and I did not verify it. The guarantee rises to 125 days.

## 8. Other mass occupations

| Occupation | Best count found | Pay evidence | Confidence |
|---|---|---|---|
| Handloom weavers + allied | **35.22 lakh** (4th Handloom Census 2019-20: 26.74 lakh weavers + 8.49 lakh allied; >72% women). The 3rd census (2009-10) counted 43.32 lakh. | **67.1% of handloom-worker households earn < Rs 5,000/month** (Table 17, p.18); WRRI weavers Rs 465/day (men) | medium |
| Street vendors | **>75.5 lakh** PM SVANidhi beneficiaries, with >1.12 crore loans worth >Rs 17,800 crore (PIB factsheet May 2026; MoHUA Jun 2026). This is a lower bound. | none official | medium (as beneficiaries) |
| Domestic workers | e-Shram 2.97 crore (see "Cooks" caveat) plus 0.93 crore "domestic housekeepers". The Labour Bureau All-India Survey on Domestic Workers launched in 2021; **no results found**. | none official; WRRI sweeping/cleaning (women) Rs 359/day used as a loose proxy | low |
| Sanitation workers | NAMASTE profiled **90,915** sewer/septic-tank workers (31 Mar 2026, as cited from the MoSJE annual report) and about 2.5 lakh waste pickers (Jul 2026; other reports say 1.3 lakh) | WRRI sweeping/cleaning (men) Rs 412/day | low (profiled, not total) |
| Gig and platform workers | NITI Aayog (Jun 2022): 68 lakh (2019-20), **77 lakh (2020-21)**, 2.35 crore projected for 2029-30. e-Shram: about 11.5 lakh platform workers. | none official | low |
| Drivers | e-Shram: car/taxi/van 3.26 mn; auto 1.32 mn; truck 1.00 mn; bus 0.28 mn. No official national driver count found. | WRRI LMV & tractor driver Rs 575/day (men) | low (headcount) |
| Security guards | No official count. Industry claims range from 7-10 mn (CAPSI says "1 crore"); about 30,592 PSARA-licensed agencies. e-Shram 0.47 mn. | none official | low (left blank) |
| Gems & jewellery | GJEPC claims "over 42 lakh" direct jobs (Nov 2025). e-Shram 1.04 mn. | ASI NIC 32 Rs 2.36 lakh/worker (factories only) | low |
| Leather | e-Shram 6.26 mn; ASI leather factories 0.44 mn. No Council for Leather Exports figure verified. | ASI NIC 15 Rs 1.89 lakh/worker | low |
| Textiles (whole value chain) | Ministry figures of "45 mn direct" or "5.3 crore" are secondary claims and not used | ASI textiles Rs 1.95 lakh; apparel Rs 1.76 lakh | low |
| Beedi | e-Shram Tobacco 2.76 mn; ASI NIC 12 factories 0.42 mn | WRRI women Rs 253/day; ASI tobacco Rs 60,632/worker/yr (lowest NIC) | medium (pay) |

## Gaps and things I could not verify
- **WRRI**
  - The All-India average is quotation-weighted, not population-weighted.
  - The July 2025 sample change inflates 5-year growth.
  - The series ends at August 2026 even though September 2026 was scheduled for release on 30 Oct 2026.
  - I did not cross-check my computed annual means against the Labour Bureau's own annual report, whose latest edition is 2024-25.
- **Not found or not published**
  - 11th Agriculture Census (2021-22) national results
  - 21st Livestock Census results
  - Labour Bureau All-India Survey on Domestic Workers results
  - Handbook of Fisheries Statistics fisher-population table
  - Labour Bureau Quarterly Employment Survey and Occupational Wage Survey levels. The Labour Bureau site now exposes only Wage Rate Index numbers (base 2016), not wage levels.
- **No official headcount** for truck drivers, taxi or auto drivers, delivery riders, security guards or beauty workers. e-Shram registrations and industry claims are the only figures, and both are low confidence.
- **Not checked against primary documents**
  - BOCW 5.73 crore comes from a VVGNLI and Indus Action paper, not a Lok Sabha reply.
  - The NAMASTE waste-picker count is from media and the PIB blog, and sources conflict.
  - The VB-G RAM G national average wage (Rs 327.4) and the PM SVANidhi figure of 76.95 lakh as of Jul 2026 are media reports only.
- **Education** is not available from any source in this lane. Every `education_typical` entry is an assumption, to be replaced from PLFS microdata.
- **Mining:** only e-Shram registrations (0.46 mn) were found. I found no DGMS employment figure, so mining has no row.
- **Census 2011** cultivator and labourer totals (118.8 mn, 144.3 mn) are rounded figures from a Rajya Sabha reply. The exact Primary Census Abstract figures were not downloaded.

## Sources (main)
- Labour Bureau WRRI dashboard and CSV: https://labourbureau.gov.in/rural-wages ; https://labourbureau.gov.in/home/excel_download_ruralWage_data?state_id=101 ; brief: https://labourbureau.gov.in/uploads/pdf/Wage_Rates_Rural_India_A_Brief.pdf ; CPI-AL/RL base-2019 note: https://labourbureau.gov.in/uploads/public/notice/Detailed-Note-for-CPI---AL--RL-Base-2019-100-July-25pdf-6ca95dbdad61e03ca919d7862d859b4d.pdf
- e-Shram dashboard: https://eshram.gov.in/dashboard ; PIB 5-year factsheet: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc_9692_20260825_14270901.pdf
- ASI 2024-25: https://microdata.gov.in/NADA/index.php/catalog/309/download/6675 ; https://www.mospi.gov.in/uploads/publications_reports/publications_reports1790761607830_02ca8547-c087-4c5c-9826-5d58740ee63f_Factsheet_ASI_2024-25.pdf ; https://www.mospi.gov.in/uploads/latestReleases/latest_release_1790768522303_b1ee6ba9-c9d3-481a-b30e-45a24c7f3729_PIB_Note_ASI_2024-25_English.pdf
- ASUSE 2025: https://www.mospi.gov.in/uploads/latestreleasesfiles/1777360756062-publications_reports1774347275480_658da785-11e1-4df3-9f02-27e08a8675f6_Factsheet_ASUSE_2025-f.pdf ; https://www.mospi.gov.in/uploads/latestReleases/latest_release_1774347321466_c16ddf22-bfff-4097-88a7-b3134e464d51_Press_Note_ASUSE_2025_English.pdf ; https://www.mospi.gov.in/uploads/latestReleases/latest_release_1778063743760_e338f15d-195f-429f-892d-aa4155c7c4ce_Press_Note_ASUSE_2025_Report-English_%281%29.pdf
- MGNREGA FY26: https://libtech.in/wp-content/uploads/2026/05/LibTech_India_Tracker_FY-2025-26-6th-May-26_v2.docx.pdf ; VB-G RAM G wage gazette: https://egazette.gov.in/WriteReadData/2026/273958.pdf
- NAFIS 2021-22: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2024/oct/doc20241010414001.pdf ; SAS 2018-19 income: https://pib.gov.in/PressReleasePage.aspx?PRID=1842783
- Handloom Census 2019-20: https://mail.hepcindia.com/img/4th%20Handloom%20Census.pdf ; PIB handloom factsheet Aug 2026: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc202686945201.pdf
- PM SVANidhi: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/may/doc2026530879401.pdf ; https://mohua.gov.in/static/uploads/2026/06/f319d6ae19b2b2b0a4ee05529818cc81.pdf
- BOCW: https://indusaction.org/wp-content/uploads/2026/06/Final-Paper-VVGNLI-and-IA.docx.pdf
- Fisheries: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251120700601.pdf
- Gig economy: https://www.niti.gov.in/sites/default/files/2022-06/Policy_Brief_India%27s_Booming_Gig_and_Platform_Economy_27062022.pdf
- NAMASTE: https://www.newsonair.gov.in/namaste-scheme-achieves-milestone-in-advancing-dignity-and-safety-of-sanitation-workers/ ; https://www.pib.gov.in/blogs/blogsdescr.aspx?feaaid=565
- GJEPC claim: https://mail.indianjeweller.in/Indian-Jewellery-News/15684/index.html ; security industry claim: https://theprint.in/ani-press-releases/capsi-signs-mou-with-director-general-of-civil-defence/2664294
- Critiques of the WRRI method: https://m.thewire.in/article/economy/labour-bureaus-methodology-is-causing-confusion-in-rural-wage-rates-data-heres-why
