# Who pays India's taxes: official facts (as of 9 Nov 2026)

Lane: the tax base and its concentration. Rs figures are in crore (1 crore = 10 million) unless stated.
"AY" = assessment year (the income year is the FY before it: AY 2023-24 = incomes of FY 2022-23).
Every number carries a source. **[S]** marks a secondary source (news or blog) quoting an official figure.
Derived numbers show their arithmetic, or point to the script that computes them.

## 0. Bottom line for the visualizer question

1. **Your claim is right in direction but too generous for personal income tax.** Individual income tax is
   concentrated far more than "the top ~2%". In AY 2023-24, the latest year with a published distribution:
   - **62.7%** of the 7.55 crore individual returns showed **zero tax**.
   - Only **2.82 crore individuals had any tax liability**. That is about **3% of adults (20+)** and about **4.7% of a 60-crore workforce**.
   - **About 1% of adults (≈92 lakh people) paid ≈89%** of all individual income tax (range 87.7–90.1%).
   - **About 0.1% of adults (≈10 lakh returns) paid 50%.** About 0.45% (≈41 lakh) paid 75%.
   - **About 1.2% of adults (≈1.1 crore) paid 90%.**
2. **Personal income tax is not most of the money, though.** Individuals' income tax was about **22% of the
   Centre's gross tax revenue** (FY 2022-23) and about **14% of all centre-plus-state tax receipts**.
   - For FY 2024-25 the estimate is about **26% of central gross tax revenue (GTR)** and about **16% of general-government tax**.
   - So the top ~1% of adults fund roughly **20–23% of central taxes** and about **12–14% of all government taxes** through income tax alone.
   - Indirect taxes (GST, excise, customs) were **~41% of central GTR in FY 2024-25**. State own-tax revenue (another 6.8% of GDP) is almost all indirect.
   - Corporation tax was ~26% of central GTR, and it is itself concentrated: **877 companies (0.08%) paid 54% of corporate tax**.
3. **The Budget 2025 change narrowed the payer base further, deliberately.** From FY 2025-26, income up to
   Rs 12 lakh is tax-free under the new regime (Rs 12.75 lakh for salaried taxpayers).
   - The government estimated **~Rs 1 lakh crore** of direct taxes forgone and said **"1 crore more people"** would pay no tax.
   - In AY 2023-24 only **~72 lakh individuals (9.5% of filers, ~0.8% of adults)** declared total income above Rs 12 lakh (interpolated).
   - Personal income tax now rests on roughly the top ~1% of adults (plus capital-gains taxpayers).
4. **Overlap with high-AI-exposure jobs.** The visible tax-paying base is salaried and formal:
   - **57% of individual gross total income is salary.**
   - Of the 51.6 lakh individuals with returned income above Rs 15 lakh, 46.7 lakh had salary above Rs 15 lakh. That is not the same people, but it shows salaried returns dominate the top.
   - On the corporate side, **IT/ITeS/BPO companies paid 10.9%** and **financial intermediation paid 27.2%** of company gross tax payable (FY 2023-24).
   - So the "red" occupations in a Karpathy-style map (software, BPO, finance, clerical and professional services) sit right on top of the narrow direct-tax base.
   - The other agent's earnings and occupation linkage is needed to put a number on this overlap.

## 1. Returns filed, individual filers, non-zero liability

### 1a. CBDT "Income Tax Return Statistics" (status-wise, after consistency checks)
Source PDFs (official; the site blocks scripts, so copies came via Wayback, see data/raw/tax):
- AY 2020-21: https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Income-tax-statistics-i-t-return-AY_2020-21.pdf (p.5, Table 2.11)
- AY 2021-22: https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Income-tax-statistics-i-t-return-AY_2021-22.pdf (p.5, Table 2.11)
- AY 2022-23: https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Approved-version-Income-Tax-Return-Statistics-for-the-AY-2022-23-14062024.pdf (data to 31-Aug-2023)
- AY 2023-24: https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Approved-version-Income-Tax-Return-Statistics-for-the-AY-2023-24.pdf (data to 31-May-2024; released 16-07-2024)

| AY | All returns analysed | Individual returns | Individuals, tax payable = 0 | Individuals, tax > 0 | Zero-tax share | Individual tax payable (Rs cr) |
|---|---|---|---|---|---|---|
| 2020-21 | 6,39,39,427* | 6,02,28,633 | 4,14,04,049 | 1,88,24,584 | 68.7% | 4,00,805 |
| 2021-22 | 6,75,55,425 | 6,36,95,664 | 4,28,45,074 | 2,08,50,590 | 67.3% | 4,25,994 |
| 2022-23 | 7,25,78,080 | 6,85,44,147 | 4,21,49,330 | 2,63,94,817 | 61.5% | 5,71,307 |
| 2023-24 | 7,97,12,145 | 7,54,61,286 | 4,72,99,925 | 2,81,61,361 | 62.7% | 6,77,351 |

*The AY 2020-21 document's status rows add up to 6,69,14,905, but it prints a total of 6,39,39,427. This is an inconsistency in the source.
"Tax payable" is aggregate liability (tax, surcharge, cess and interest) before credit for TDS or advance tax (Table 2.11 note).

### 1b. Later assessment years (no range-wise statistics published or found yet)
- **AY 2024-25:**
  - 8,67,67,752 ITRs filed up to 30-Nov-2025, reporting taxable income of Rs 1,17,22,177 cr and gross tax payable of Rs 18,69,622 cr.
  - Of these, **8,19,98,000 were e-filed by individuals**, and 6,28,44,891 (76.64%) were under the new regime (s.115BAC).
  - Source: Receipt Budget 2026-27, Annexure-7, printed pp.30 and 41 / PDF pp.36 and 47 (https://www.indiabudget.gov.in/doc/rec/allrec.pdf).
- **FY 2024-25 filings to 31-Dec-2024 (mostly AY 2024-25):** 8,39,73,416 ITRs, of which **5,57,95,391 (66.4%) showed zero tax liability**.
  - Source: Lok Sabha written reply by MoS Pankaj Chaudhary, Feb 2025 **[S]**, as reported by https://studycafe.in/83973416-filed-itr-out-of-which-55795391-filed-zero-tax-liability-itr-upto-december-2024-365622.html.
  - The sansad.in annexure was not located.
- **AY 2023-24:** 4.90 crore individuals reported zero *taxable income*. Rajya Sabha reply, Dec 2024 **[S]** (https://www.tribuneindia.com/news/india/only-6-68-citizens-filed-i-t-returns-in-2023-24).
- **AY 2025-26:** "record 7.3 crore ITRs" filed by 15-Sep-2025 (CBDT post on X) **[S]** (https://www.tribuneindia.com/news/business/itr-filing-deadline-extended-by-a-day-7-crore-returns-submitted).
  - Equity LTCG tax for AY 2025-26 was Rs 1,29,158 cr, against Rs 72,249 cr for AY 2024-25. Source: Lok Sabha USQ 166, 20-Jul-2026 (data/raw/tax/ls_2026-07-20_USQ166_LTCG_revenue.pdf).
- **AY 2026-27 (first year of the Rs 12 lakh rebate):**
  - Over 5.9 crore ITR-1/ITR-2 returns were filed by 31-Jul-2026.
  - "Record 7.8 crore+" returns were filed by 31-Aug-2026 (I-T Dept X post via PTI) **[S]** (https://www.deccanherald.com/india/itr-filing-for-assessment-year-2027-touches-record-78-cr-4131050).
  - **The zero-tax share for AY 2026-27 is not yet published.**

### 1c. CBDT Time Series FY 2000-01 to 2024-25 (released 21-11-2025)
Official landing page: https://www.incometaxindia.gov.in/w/direct_tax_collections_as_on_16.03.2025.pdf.
The PDF (wm.incometaxindia.gov.in/documents/20117/6715095/Final-time-series-data.pdf) is served only to interactive browsers and is not in Wayback.
- A byte copy was taken from the caclubindia attachment of the same file (PDF created 21-11-2025 16:38 IST, title "final draft time series data 2024-25").
- Its headline numbers match press coverage (net Rs 22,26,375 cr; 12.13 crore taxpayers). It was kept outside data/raw/tax because the mirror is not an official host.

| | FY 2020-21 | FY 2021-22 | FY 2022-23 | FY 2023-24 | FY 2024-25 |
|---|---|---|---|---|---|
| ITRs filed, all (Table 1.7) | 7,38,98,581 | 7,30,47,073 | 7,78,16,350 | 8,61,32,779 | 9,18,46,067 |
| ITRs filed, individuals | 6,94,89,484 | 6,86,47,490 | 7,33,11,873 | 8,13,90,736 | 8,68,65,490 |
| Persons filing, individuals (1.8) | 6,31,71,013 | 6,54,61,868 | 6,96,90,925 | 7,63,70,510 | 8,08,80,773 |
| "Taxpayers", individuals, by AY of same label (1.9)† | 7,79,90,888 (AY20-21) | 8,25,04,957 | 8,90,89,795 | 9,91,75,656 | 11,61,36,768 (AY24-25) |

†A "taxpayer" here means a person who filed a return **or had TDS deducted** without filing (Table 1.9 note). It is **not** the number of people with positive liability.
The full series is in data/tax/cbdt_returns_filers_taxpayers.csv.

## 2. Distribution and concentration of individual income tax

The published tables are **univariate**: returns by returned-income range (Table 2.10) and returns by tax-payable range (Table 2.11).
**There is no official cross-tab of tax payable by income range.**
- Concentration is therefore computed on Table 2.11 directly, ranking returns by their own tax payable. This is exact at bin edges.
- Inside a bin there are two bounds:
  - an upper bound, which assumes everyone in the bin pays the bin average;
  - a lower bound, which assumes the top payers in the bin pay the bin's upper limit.
- Denominators:
  - individual filers (Table 2.11 total);
  - adults aged 20+ = 92,23,44,832 (UN-WPP 2022, used in WIL WP 2024/09 Table 2);
  - workforce = 60 crore (round figure from the project brief, PLFS lane).
- Script: scripts/tax/build_tax_dataset.py. Output: data/tax/individual_tax_concentration.csv and individual_tax_payable_cumulative.csv.

**AY 2023-24 (FY 2022-23 incomes): who pays the Rs 6,77,351 cr of individual income tax**

| Share of individual tax | Returns needed (point; range) | % of individual filers | % of adults 20+ | % of 60-cr workforce |
|---|---|---|---|---|
| 50% | 9.96 lakh (9.53–10.40 lakh) | 1.32% | 0.11% | 0.17% |
| 75% | 41.1 lakh (40.8–41.4 lakh) | 5.45% | 0.45% | 0.69% |
| 90% | 1.10 crore (0.92–1.28 crore) | 14.6% | 1.19% | 1.83% |
| 99% | 1.99 crore (1.32–2.66 crore) | 26.4% | 2.16% | 3.32% |
| 100% | 2.82 crore (all non-zero returns) | 37.3% | 3.05% | 4.69% |

Read the other way:

| Group | Share of individual tax paid |
|---|---|
| Top 1% of filers (7.5 lakh) | 45.3% |
| Top 10% of filers | 86.5% |
| Top 0.5% of adults | 77.4% |
| Top 1% of adults (92 lakh) | 88.9% (87.7–90.1%) |
| Top 2% of adults | 96.8% (93.7–100%) |
| Top 1% of a 60-cr workforce | 82.4% |
| Top 2% of a 60-cr workforce | 92.9% |

Exact bin edge: 76.7 lakh returns with tax payable above Rs 1.5 lakh paid Rs 5,86,992 cr, which is **86.7%** (Table 2.11; 28,161,361 − 20,490,677 returns).

**Trend.** The concentration is stable:
- Top 1% of filers: 47.9% (AY 2020-21) → 47.8% → 48.6% → 45.3% (AY 2023-24).
- Returns needed for 50% of the tax: 7.0 lakh → 7.5 lakh → 7.5 lakh → 10.0 lakh.
- The zero-tax share fell from 68.7% to 62.7%.

**So, precisely:** for personal income tax, the "top 2%" claim understates concentration. **~1% of adults pays ~89%, and ~3% of adults pays all of it.** It overstates the fiscal weight, because personal income tax is ~22–26% of central GTR and ~14–16% of all government tax (section 5).

Returned-income distribution (Table 2.10), from data/tax/individuals_above_income_thresholds.csv. The Rs 12 lakh row is interpolated inside the 10–15 lakh bin using a linear density matched to the bin mean.

| Returned income above | AY 2020-21 | AY 2021-22 | AY 2022-23 | AY 2023-24 |
|---|---|---|---|---|
| Rs 7 lakh | 96.9 lakh | 1.03 cr | 1.26 cr | 1.52 cr |
| Rs 10 lakh | 53.5 lakh | 59.0 lakh | 75.3 lakh | 93.3 lakh |
| **Rs 12 lakh (interp.)** | 39.4 lakh | 44.7 lakh | 57.6 lakh | **71.9 lakh** (9.5% of filers; 0.78% of adults) |
| Rs 50 lakh | 3.62 lakh | 3.92 lakh | 5.58 lakh | 6.72 lakh |
| Rs 1 crore | 1.18 lakh | 1.26 lakh | 1.87 lakh | 2.17 lakh |
| Rs 100 crore | 135 | 134 | 297 | 285 |

The 2.17 lakh above Rs 1 crore matches the "2.16 lakh as of 31-Dec-2023" Parliament reply **[S]** (https://business-standard.com/economy/news/people-reporting-annual-income-over-rs-1-cr-increase-to-216-000-in-ay24-124020601433_1.html).
For FY 2024-25 filings (to 31-Mar-2025), news based on department data reports **3,24,067 individuals above Rs 1 crore** **[S]** (https://www.caclubindia.com/news/over-3-24-lakh-individuals-filed-itr-for-income-above-rs-1-crore-in-fy-2024-25-24742.asp):
- Rs 1–5 cr: 2,97,086
- Rs 5–10 cr: 16,797
- above Rs 10 cr: 10,184

## 3. Salaried and non-salaried

| AY | Individual returns with salary > 0 | Share of individual returns | Salary income (Rs cr) | Salary as % of individual GTI | Salary as % of all-status GTI |
|---|---|---|---|---|---|
| 2020-21 | 3,02,26,729 | 50.2% | 23,29,444 | 56.2% | 38.2% |
| 2021-22 | 3,11,76,611 | 48.9% | 24,57,702 | 55.1% | 35.3% (of 69,59,553) |
| 2022-23 | 3,40,29,567 | 49.6% | 29,59,017 | 55.1% | 33.1% (of 89,52,672) |
| 2023-24 | 3,79,64,804 | 50.3% | 35,23,217 | 57.0% | 34.4% (of 1,02,53,113) |

Source: ITR Statistics, p.5–6 and Table 2.2. The count is total individual returns minus returns with salary = 0.
- Salary dominates the top. AY 2023-24 salary above Rs 15 lakh: 46.7 lakh returns; salary above Rs 1 crore: 1.18 lakh returns. Compare the returned-income counts of 51.6 lakh and 2.17 lakh (Tables 2.2 and 2.10).
- Receipt Budget 2026-27, Annex-7, p.41: "more than 50 per cent of the individual taxpayers derive their income primarily from salaries".
- **TDS on salaries (s.192): no official year-wise series was found.** CBDT Time Series Table 1.5 gives **total TDS from all sections** only:

| FY | Total TDS, all sections (Rs cr) | Share of gross direct tax |
|---|---|---|
| 2021-22 | 6,34,243 | |
| 2022-23 | 8,17,970 | |
| 2023-24 | 6,51,922 | |
| 2024-25 | 9,47,915 | 35.1% of gross direct tax (27,03,107) |

TDS covers corporate and non-salary deductions too, so it cannot stand in for salary TDS. Searches of Lok Sabha and Rajya Sabha answers, CAG and CBDT found no s.192 series. **Gap.**

## 4. Budget 2025 regime change and the current law

- **Budget speech 2025-26 (1-Feb-2025), paras 156–161** (data/raw/tax/budget_speech_2025-26.pdf; https://www.indiabudget.gov.in/budget2025-26/doc/budget_speech.pdf):
  - "no income tax payable upto income of Rs 12 lakh (i.e. average income of Rs 1 lakh per month other than special rate income such as capital gains) under the new regime".
  - Rs 12.75 lakh for salaried taxpayers, because of the Rs 75,000 standard deduction.
  - New slabs: 0–4 lakh nil; 4–8 lakh 5%; 8–12 lakh 10%; 12–16 lakh 15%; 16–20 lakh 20%; 20–24 lakh 25%; above 24 lakh 30%.
  - Benefit at Rs 12 lakh: Rs 80,000. At Rs 18 lakh: Rs 70,000. At Rs 25 lakh: Rs 1.1 lakh.
  - **"revenue of about Rs 1 lakh crore in direct taxes and Rs 2600 crore in indirect taxes will be forgone"** (para 161).
- **"1 crore" estimate:** FM Sitharaman at the post-budget press conference said **"1 crore more people will pay no income tax"** **[S]** (https://www.tribuneindia.com/news/business/1-crore-more-people-will-pay-no-income-tax-due-to-hike-in-rebate-fm). This is a government projection, not a measured count.
- **FY 2026-27:**
  - **No change in rates** (Memorandum to Finance Bill 2026: "There is no change proposed in tax rates"; data/raw/tax/memorandum_finance_bill_2026.pdf).
  - The same slabs now sit in **section 202 of the Income-tax Act, 2025**, as default rates.
  - **The Income-tax Act, 2025 came into effect on 1 April 2026** (Budget speech 2026-27, para 99), replacing the 1961 Act. "Tax year" replaces the old "previous year / AY" pair.
  - Budget 2026-27 also raised STT on futures to 0.05% and on options to 0.15% (para 140), and made MAT a final tax at 14% (para 143).
- **Revenue signal:**

| | Rs crore | Change |
|---|---|---|
| "Taxes on Income" (non-corporate incl. STT), Actual 2024-25 | 12,35,171 | |
| BE 2025-26 | 14,38,000 | |
| RE 2025-26 | 13,12,000 | **−8.8% vs BE**; +6.2% over 2024-25 |
| BE 2026-27 | 14,66,000 | |

Source: Receipt Budget 2026-27, tr.pdf p.2. The BE 2026-27 figure in the tr.pdf table differs from the narrative text, which says 14,56,000. The table figure is used here.
- **Who still pays after the change:** individuals with normal income above Rs 12 lakh, plus anyone with special-rate income (capital gains, etc.), plus old-regime filers above Rs 5 lakh.
  - Latest measured base: **~72 lakh individuals above Rs 12 lakh in AY 2023-24**. That is 0.78% of adults and 1.2% of a 60-cr workforce.
  - The equivalent count for FY 2025-26 incomes will be higher because of income growth. **No official count is published yet.**

## 5. Composition of tax revenue

Central gross tax revenue (Receipt Budget "Tax Revenue" statements: https://www.indiabudget.gov.in/budget2024-25/doc/rec/tr.pdf, https://www.indiabudget.gov.in/budget2025-26/doc/rec/tr.pdf, https://www.indiabudget.gov.in/doc/rec/tr.pdf; GTR is cross-checked with Budget at a Glance 2026-27, p.6):

| Rs cr (share of GTR) | Actual 2022-23 | Actual 2023-24 | Actual 2024-25 | RE 2025-26 | BE 2026-27 |
|---|---|---|---|---|---|
| Corporation tax | 8,25,834 (27.0%) | 9,11,055 (26.3%) | 9,86,767 (26.0%) | 11,09,000 (27.2%) | 12,31,000 (28.0%) |
| Taxes on income excl. STT | 8,08,174 (26.5%) | 10,10,978 (29.2%) | 11,82,974 (31.2%) | 12,48,330 (30.6%) | 13,92,300 (31.6%) |
| STT | 25,085 (0.8%) | 33,778 (1.0%) | 52,197 (1.4%) | 63,670 (1.6%) | 73,700 (1.7%) |
| GST (CGST + IGST + compensation cess) | 8,49,132 (27.8%) | 9,57,208 (27.6%) | 10,27,041 (27.0%) | 10,46,480 (25.7%) | 10,19,020 (23.1%) |
| Union excise | 3,19,000 (10.4%) | 3,05,362 (8.8%) | 3,00,253 (7.9%) | 3,36,550 (8.2%) | 3,88,910 (8.8%) |
| Customs | 2,13,372 (7.0%) | 2,33,119 (6.7%) | 2,33,201 (6.1%) | 2,58,290 (6.3%) | 2,71,200 (6.2%) |
| Other (UT taxes, CTT, cesses, etc.) | ~0.4% | ~0.4% | ~0.4% | ~0.4% | ~0.6% |
| **Gross tax revenue** | **30,54,191** | **34,65,518** | **37,96,382** | **40,77,772** | **44,04,086** |

The GST compensation cess ends in 2025-26: Rs 88,000 cr in RE 2025-26, nil in BE 2026-27.
- Central GTR/GDP: 11.5% (2024-25), 11.4% (2025-26 RE), 11.2% (2026-27 BE). Direct taxes are 6.7%, 6.8% and 6.9% of GDP; indirect taxes 4.8%, 4.6% and 4.3% (Budget at a Glance 2026-27, p.7 chart).
- **Combined centre and states** (Economic Survey 2025-26, Statistical Appendix Tables 2.6/2.7; https://www.indiabudget.gov.in/economicsurvey/doc/stat/tab2.7.pdf):

| | 2022-23 | 2023-24 | 2024-25 RE | 2025-26 BE |
|---|---|---|---|---|
| General-government tax receipts (% GDP) | 17.9% | 18.0% | 18.4% | 19.1% |
| General-government tax receipts (Rs cr) | 48,09,044 | 54,07,849 | 60,80,098 | 68,08,169 |
| States' own tax revenue (% GDP) | 6.6% | 6.5% | 6.8% | 7.1% |

- **Personal income tax's weight** (data/tax/tax_dependence_summary.csv, computed by scripts/tax/derived_shares.py):

| Measure | Value | Arithmetic |
|---|---|---|
| Individuals' tax AY 2023-24, % of central GTR FY 2022-23 | 22.2% | 6,77,351 / 30,54,191 |
| Same, % of general-government tax FY 2022-23 | 14.1% | 6,77,351 / 48,09,044 |
| FY 2024-25 estimate of individuals' tax | Rs 9.79 lakh cr | (12,35,161 − 52,197) × 82.75%, the AY 2023-24 individual share of non-company liability |
| Same, % of central GTR | 25.8% | |
| Same, % of general-government tax | 16.1% | |
| Top 1% of adults, % of central GTR | 19.7% (FY 2022-23); ~22.9% (FY 2024-25 estimate) | |
| Top 1% of adults, % of general-government tax | 12.5% (FY 2022-23); ~14.3% (FY 2024-25 estimate) | |

- **GST incidence (contested):**
  - Oxfam India, *Survival of the Richest: The India Story* (Jan 2023): the bottom 50% pay about **64.3%** of GST and the top 10% about 3–4% **[S]** (https://www.thenewsminute.com/news/indias-poorest-half-pays-two-thirds-gst-while-top-richest-pay-only-3-oxfam-172023). Per that coverage, it imputes rates onto the **2011-12** NSS consumption survey.
  - The peer-reviewed estimate on the **2022-23 HCES** reaches a different result: S. Mukherjee (NIPFP), EPW 13-Sep-2025, Vol LX No 37 (https://nipfp.org.in/media/documents/salx37130925sacchidananda-mukherjee.pdf).
    - "In rural areas, the bottom 50% and middle 30% each bear 31% of the burden; the top 20% bear 37%." In urban areas the shares are 29%, 30% and 41%.
    - All four progressivity indices show GST as mildly progressive with respect to consumption.
    - Average GST rate on consumption: urban top 5% 5.40% against bottom 50% 4.89% (Table 9, Scenario I).
  - Another 2022-23-based paper (V. Shekhar, SPJIMR) reportedly finds the bottom 50% bear ~28% of household GST **[S, not opened]** (https://www.spjimr.org/wp-content/uploads/pdf/who-pays-how-much-gst-in-india.pdf).
  - Takeaway: the bottom half bears roughly 30% of GST (consumption basis), not two-thirds. GST is still roughly proportional to *consumption*, so it is a much broader base than income tax.
  - Separately, GST rates were rationalised to 5%/18% plus a 40% demerit rate from 22-Sep-2025 (56th GST Council) **[S]** (https://www.scconline.com/blog/post/2025/09/04/gst-council-56th-meeting-slab-reforms-tribunal-rollouts-2025/). CGST RE 2025-26 is Rs 9,58,480 cr against BE Rs 10,10,890 cr.

## 6. Inequality context

- **WIL Working Paper 2024/09**, Bharti, Chancel, Piketty and Somanchi, *Income and Wealth Inequality in India, 1922-2023: The Rise of the Billionaire Raj* (https://wid.world/document/income-and-wealth-inequality-in-india-1922-2023-the-rise-of-the-billionaire-raj-world-inequality-lab-working-paper-2024-09/), Tables 2–3, year 2022-23, adults 20+:

| Group | Share of pre-tax national income | Share of wealth |
|---|---|---|
| Top 1% | **22.6%** (threshold Rs 20.7 lakh; average Rs 53 lakh) | **40.1%** |
| Top 10% | **57.7%** (threshold Rs 2.91 lakh) | 65.0% |
| Middle 40% | 27.3% | 28.6% |
| Bottom 50% | **15.0%** (average Rs 71,163) | 6.4% |

  - The authors say the income tax system "might be regressive when viewed from the lens of net wealth", and that their estimates are a lower bound because of poor data.
  - Note: the top 10% by national income (9.2 crore adults) is about the same size as the ITR-filing population. Top 1% national income (Rs 20.7 lakh) sits well above the Rs 12 lakh zero-tax line.
- People declaring more than Rs 1 crore and more than Rs 50 lakh: see section 2. There were 2.17 lakh and 6.72 lakh in AY 2023-24 (official tables), and 3.24 lakh above Rs 1 crore in FY 2024-25 filings **[S]**.

## 7. Corporate tax concentration

Receipt Budget Annexure-7 "Statement of Revenue Impact of Tax Incentives", Table 1 (data/tax/corporate_tax_concentration_by_PBT.csv):

| FY (returns) | Companies filing | Companies with PBT > Rs 500 cr | Share of PBT | **Share of CIT liability** | Effective tax rate (big / all) |
|---|---|---|---|---|---|
| 2021-22 (RB 2024-25, PDF p.36) | 10,25,717 | 678 | 62.54% | **54.90%** | 20.42% / 23.26% |
| 2022-23 (RB 2025-26, PDF p.36) | 10,75,866 | 743 | 62.59% | **53.24%** | 19.77% / 23.24% |
| 2023-24 (RB 2026-27, printed p.32 / PDF p.38) | 11,31,290 | 877 | 64.58% | **54.18%** | 18.85% / 22.47% |

- PBT Rs 100–500 cr (2,697 companies) adds a further 13.62%. So **3,574 companies (0.32%) carry 67.8% of corporate tax**.
- 45% of companies report losses (FY 2023-24).
- **By industry, FY 2023-24** (RB 2026-27 Appendix, printed pp.45–49 / PDF pp.51–55; data/tax/corporate_tax_by_industry_FY2023-24.csv; total gross tax payable Rs 8,99,662 cr):

| Industry | Gross tax payable (Rs cr) | Share | ETR |
|---|---|---|---|
| **Computer and related services** | **98,025** | **10.9%** | |
| of which software development (29,004 cos) | 66,609 | 7.4% | 25.1% |
| of which other IT-enabled services | 20,169 | | |
| of which BPO | 4,777 | | |
| **Financial intermediation** | **2,44,227** | **27.1%** | |
| of which commercial banks | 91,741 | | |
| Refined petroleum | 40,882 | 4.5% | |

  - IT/ITeS corporate tax is therefore about **2.8% of central GTR** (FY 2024-25 estimate).
  - **The IT sector's share of *personal* income tax (employees' salaries) is not published.** That belongs to the other agent's occupation-to-tax lane.

## Gaps and caveats

- **Distribution data:**
  - **ITR Statistics for AY 2024-25 or later (range-wise) were not found.** The new incometaxindia.gov.in site has no such page (a guessed URL returned 404). So the concentration figures stop at AY 2023-24, which is before the Rs 7 lakh to Rs 12 lakh rebate change.
  - **There is no official tax-by-income-range cross-tab.** Tax shares are computed on the tax-payable distribution itself (section 2 method), with within-bin bounds.
  - The adults denominator (UN-WPP 2022, 20+) and the workforce denominator (60 cr) are fixed across years, so the AY 2020-21 shares are slightly overstated relative to the population at the time.
- **Not found:**
  - **s.192 salary-TDS series.**
  - **Primary sansad.in copies of the zero-tax-returns replies** (secondary only).
  - The AY 2026-27 zero-tax share.
- **Comparability of the money figures:**
  - "Tax payable" is liability per return. Collections (budget figures) differ by timing and refunds.
  - Mapping AY 2023-24 liability onto FY 2022-23 revenue is approximate.
  - FY 2024-25 shares are labelled ESTIMATE.
- **Provenance of downloads:**
  - The CBDT time series 2024-25 PDF was obtained through a non-official mirror (byte copy; cross-checked).
  - The other CBDT PDFs were obtained through web.archive.org snapshots of the official URLs, because incometaxindia.gov.in returns HTTP 403 to non-browser clients.

## Files

- **Raw (official):** data/raw/tax/
  - itr_stats_AY2020-21..AY2023-24.pdf
  - time_series_FY2000-01_to_2023-24.pdf
  - receipt_budget_20xx-yy(_tr).pdf
  - budget_at_a_glance_2026-27.pdf
  - budget_speech_2025-26.pdf and budget_speech_2026-27.pdf
  - memorandum_finance_bill_2025.pdf and memorandum_finance_bill_2026.pdf
  - economic_survey_2025-26_stat_tab2.6.pdf and economic_survey_2025-26_stat_tab2.7.pdf
  - pib_*.pdf
  - ls_2026-07-20_USQ166_LTCG_revenue.pdf
- **Scripts:** scripts/tax/
  - parse_itr_stats.py
  - parse_receipt_tr.py
  - build_tax_dataset.py
  - derived_shares.py
  - wayback_fetch.py
- **Data:** data/tax/
  - itr_distribution_AY{2020-21..2023-24}.csv
  - itr_stats_all_tables_AY*.csv
  - individual_tax_concentration.csv
  - individual_tax_payable_cumulative.csv
  - individuals_above_income_thresholds.csv
  - itr_status_summary_by_AY.csv
  - central_tax_revenue_composition.csv
  - cbdt_time_series_collections.csv
  - cbdt_returns_filers_taxpayers.csv
  - corporate_tax_concentration_by_PBT.csv
  - corporate_tax_by_industry_FY2023-24.csv
  - tax_dependence_summary.csv
