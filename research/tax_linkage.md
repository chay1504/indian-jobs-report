# Linking occupations and sectors to income-tax contribution (India)

Lane: who the taxpayers are by occupation, employer, sector and place, and how consumption taxes split by spending level.
The tax base and its concentration (ITR counts, tax-payable shares, corporate-tax concentration) are in `research/tax.md` (tax agent). This file does not repeat them; it cites them where needed.

As of 9 Nov 2026. "AY 2023-24" means incomes of FY 2022-23. 1 lakh = 100,000; 1 crore = 10 million.
Confidence: **H** = official primary table; **M** = official data with my derivation or assumption, or a credible secondary source that matches official data; **L** = press report or unverified secondary source.
**[S]** marks a secondary source.

---

## 0. What this means for the hypothesis

The claim: "India shows less red (AI exposure) overall, but the top ~2% pay most income tax and those are exactly the red jobs."

1. **Income tax rests on high-paid salaried staff, so the overlap with high-AI-exposure office work is real.**
   - In AY 2023-24, about **69 lakh individuals had salary alone above the Rs 12.75 lakh zero-tax line** (interpolated). That is about **1.2% of a 60-crore workforce**.
   - Another ~11 lakh had business income above that line.
   - Among everyone with gross total income (GTI) above Rs 12.75 lakh, **77% had salary alone above the line** and only 12% had business income above it (§3).
2. **No occupation is above the line on average.** PLFS 2025 average pay of regular salaried *Managers* is Rs 50,408 a month (Rs 6.0 lakh a year). That is 47% of the zero-tax line, and *Professionals* are at 36% (§1.2).
   - So the tax comes from the **upper tail inside** managerial, professional, IT, finance and senior-government jobs, not from whole occupations.
   - For the treemap: colour tax contribution by the *share of each occupation above the line*, not by its mean.
3. **Big employers: even inside IT and private banks, the median employee is below the zero-tax line.**
   - Typical median employee pay, FY2025-26: Infosys Rs 11.1 lakh; TCS Rs 8.4 lakh (derived, disputed by its own sustainability report); Wipro Rs 9.5 lakh; Tech Mahindra Rs 5.9 lakh.
   - Private-bank gender medians are Rs 4.8–7.0 lakh. The exception is LTIMindtree at Rs 17.2 lakh.
   - Infosys: only its "senior" band (15% of staff, median Rs 25–31 lakh) is clearly above the line (§2.1).
   - So **within IT, AI exposure is highest at the junior end, which pays little income tax.** Revenue risk from AI comes through:
     - (a) the senior tail;
     - (b) corporate tax: IT/ITeS is 10.9% of company tax payable (tax agent);
     - (c) consumption.
4. **Income tax is also concentrated by place.** Maharashtra, Karnataka and Delhi booked **61%** of FY2023-24 direct tax, and the top six states booked 77% (§4).
   - Caveat: collections are booked by the taxpayer's *communication address* (for companies, usually head office), not where the work is done.
5. **Consumption tax is much less concentrated.**
   - The top 20% by spending (MPCE) account for about **35–38% of household consumption** within rural or urban India, and about 39% pooled (HCES 2023-24).
   - NIPFP estimates they bear **37% (rural) and 41% (urban) of GST**, while the bottom 50% bear 29–31% (§5).
   - So an AI shock to the top ~2% would hit income tax hard, but only a slice of GST.

---

## 1. Earnings distribution of workers

### 1.1 How many people earn above each line: income-tax returns (H/M)

Source: CBDT *Income Tax Return Statistics AY 2023-24* v1.0 (June 2024), Individuals, Tables 2.1 (GTI), 2.2 (salary) and 2.4 (business), PDF pp. 21, 22, 24.
URL: https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Approved-version-Income-Tax-Return-Statistics-for-the-AY-2023-24.pdf (local copy `data/raw/tax_linkage/cbdt_itr_stats_AY2023-24.pdf`).
Computed in `scripts/tax_linkage/derive_linkage_tables.py`; output `data/tax_linkage/itr_salary_business_thresholds_AY2023-24.csv`.

| Annual income above | Individuals, GTI above | Salary alone above | Business income alone above | Salary count / GTI count | Salary-above as % of 60 cr workforce |
|---|---|---|---|---|---|
| Rs 5 lakh | 3,99,83,243 | 2,42,39,380 | 85,38,154 | 60.6% | 4.0% |
| Rs 7 lakh* | 2,62,45,773 | 1,80,34,436 | 45,56,949 | 68.7% | 3.0% |
| Rs 10 lakh | 1,24,33,466 | 97,19,947 | 14,82,686 | 78.2% | 1.6% |
| Rs 12 lakh* | 99,42,265 | 77,00,080 | 11,87,942 | 77.4% | 1.3% |
| Rs 12.75 lakh* | 90,08,065 | 69,42,630 | 10,77,414 | 77.1% | 1.2% |
| Rs 15 lakh | 62,05,464 | 46,70,279 | 7,45,827 | 75.3% | 0.8% |
| Rs 24 lakh* | 28,24,014 | 20,18,321 | 3,55,756 | 71.5% | 0.34% |
| Rs 50 lakh | 7,42,129 | 4,52,128 | 1,10,967 | 60.9% | 0.08% |
| Rs 1 crore | 2,27,315 | 1,18,018 | 37,006 | 51.9% | 0.02% |

\* Interpolated assuming uniform density inside the CBDT bin (5.5–9.5 lakh, 10–15 lakh, 20–25 lakh). Rows without an asterisk are exact bin edges. **M** for interpolated rows, **H** otherwise.

Notes:
- The counts are univariate. "Salary alone above X" counts people whose *salary head* exceeds X; CBDT publishes no cross-tab of salary against GTI.
- The 60-crore workforce denominator follows the tax agent's convention.
- PLFS 2025 puts regular wage/salaried workers at **23.6%** of usual-status workers (PLFS 2025 Statement 7, via `data/plfs/plfs_status_in_employment.csv`). On a 60-crore base that is about 14 crore salaried people.
  - So roughly **7% of salaried workers had salary above Rs 10 lakh** and about **5% above Rs 12.75 lakh** (derived, **M**).
- People earning below the filing threshold who do not file are missing. That does not affect counts above Rs 5 lakh much, because TDS forces filing.

### 1.2 Survey view: PLFS 2025 earnings by occupation and the spread of salaries

**By occupation** (official). PLFS 2025 (Jan–Dec 2025), Appendix Table 51: average monthly earnings of regular wage/salaried employees (current weekly status) by NCO-2015 division.
Taken from the PLFS agent's `data/plfs/plfs_earnings.csv`; source xlsx https://www.mospi.gov.in/uploads/documents/publicationsReports/APPENDIX-A/Table__51.xlsx. **H**.
Output: `data/tax_linkage/occupation_earnings_vs_zero_tax_line.csv`.

| NCO division | Rs/month, all India | Rs/month, urban | Annualised, all India | % of Rs 12.75 lakh |
|---|---|---|---|---|
| 1 Managers | 50,408 | 55,360 | 6.05 lakh | 47% |
| 2 Professionals | 38,466 | 42,717 | 4.62 lakh | 36% |
| 3 Technicians & associate professionals | 26,175 | 31,909 | 3.14 lakh | 25% |
| 4 Clerical support | 24,289 | 26,514 | 2.91 lakh | 23% |
| 5 Service & sales | 15,541 | 16,914 | 1.86 lakh | 15% |
| 7 Craft & trades | 16,773 | 17,819 | 2.01 lakh | 16% |
| 8 Plant & machine operators | 17,301 | 18,618 | 2.08 lakh | 16% |
| 9 Elementary | 12,270 | 12,809 | 1.47 lakh | 12% |
| All regular salaried | 22,699 | 26,247 | 2.72 lakh | 21% |

The zero-tax line of Rs 12.75 lakh equals Rs 1,06,250 a month.

**Spread of salaries** **[S]**, **M**. India Labour Observatory (Abhinav Kumar and Ananya Pradhan), computed from PLFS 2025 unit-level data, Table 7.8 (weighted).
URL: https://indialabourobservatory.com/data/plfs-2025/earnings/; CSV saved as `data/raw/tax_linkage/indialabourobservatory_plfs-2025-tables.csv`.
- I checked its mean of Rs 22,699 against MoSPI Statement 11 and it matches exactly, which lends some confidence.
- Regular salaried, all India: **p50 Rs 15,000, p75 Rs 25,800, p90 Rs 48,000 a month** (p90 is Rs 5.8 lakh a year).
- Urban p90 is Rs 55,000. **The zero-tax line is above the 90th percentile of salaried workers**, which is consistent with the ~5% estimate in §1.1.
- No p95 or p99 is published.

**Other benchmarks** (`data/tax_linkage/earnings_distribution_benchmarks.csv`):
- **WIL Working Paper 2024/09** (Bharti, Chancel, Piketty, Somanchi), Table 2 (PDF p.41), 2022-23, pre-tax national income per adult (20+), scaled to national accounts:
  - Top 10% threshold Rs 2.91 lakh; top 1% threshold **Rs 20.7 lakh**; top 0.1% threshold Rs 82.2 lakh.
  - The tax agent already reports these; I verified them against the PDF (`data/raw/tax_linkage/wil_wp2024-09_india_inequality_1922-2023.pdf`). **M**.
- **"State of Inequality in India"** (Institute for Competitiveness for EAC-PM, May 2022), PLFS 2019-20: **Rs 25,000 a month puts a wage earner in the top 10%**. The top 1% earned about 6–7% of wage income and the top 10% about a third. **[S]** via Business Standard and Down To Earth. **L–M**.
- **PRICE ICE 360 (2021)**: about 5.6 crore people live in "rich" households (household income above Rs 30 lakh a year, 2020-21). This is household income, not a worker's. **[S]** via Business Standard and ThePrint. **L**.
- Coverage gap: surveys miss top earners. PLFS has no p99, and WIL scales survey incomes to national accounts. For counts above Rs 10 lakh, rely on ITR data (§1.1).

---

## 2. Tax by employer, sector and occupation

### 2.1 Big employers: median pay vs the zero-tax line (H/M)

Collected from annual reports filed on NSE (Board's report Rule 5(1) annexure and BRSR). The full table, with URL, page and notes for each row, is in `data/tax_linkage/firm_median_pay.csv`.
PDFs are in `data/raw/tax_linkage/company_reports/`; scripts are `scripts/tax_linkage/firm_*.py`.

| Firm | FY26 median remuneration of employees (MRE) | FY25 MRE | Employees (annexure / BRSR) | Below Rs 12.75 lakh? |
|---|---|---|---|---|
| Infosys | **Rs 11,13,024** | Rs 10,72,008 | 3,28,591 | yes |
| TCS | **Rs 8,44,742** (derived) | Rs 8,04,215 (derived) | 5,84,519 | yes by MRE; BRSR disagrees |
| Wipro | Rs 9,47,425 | Rs 9,78,516 | 2,42,156 | yes |
| Tech Mahindra | Rs 0.59 mn (printed rounded) | Rs 0.62 mn | 1,19,337 | yes |
| LTIMindtree | **Rs 17,21,230** | Rs 17,42,148 | 87,950 | **no** |
| HCLTech | not printed (ratio only; global PPP basis) | – | 1,70,811 | unclear |
| HDFC / ICICI / Kotak banks | not printed; BRSR gender medians Rs 4.8–7.0 lakh | – | 2.11 lakh / 1.24 lakh / 0.60 lakh | yes |
| SBI | no MRE; staff cost Rs 65,724 cr ÷ 2,45,131 = **Rs 26.8 lakh/head** (includes pension provisions) | – | 2,45,131 | borderline (FY25 BRSR medians Rs 12.8–13.9 lakh) |

- **TCS derivation** (MRE not printed): CEO pay Rs 2,811.3 lakh ÷ ratio 332.8 = Rs 8.45 lakh (FY26 Annual Report, NSE filing, PDF p.84).
  - The implied growth of 5.04% matches the printed 5.1% (p.44). **M**.
  - TCS's own BRSR (PDF p.131) gives medians of **Rs 18.3 lakh (378,966 men)** and **Rs 11.9 lakh (205,549 women)**. Both cannot describe the same population on the same pay basis. The BRSR likely includes overseas staff or a broader pay definition, but this is unresolved. Treat TCS as uncertain.
- **Infosys BRSR bands, FY26** (Integrated Annual Report 2025-26, printed p.199 / PDF p.169), median in Rs crore:

  | Band | Men (n) | Men median | Women (n) | Women median | Share of staff |
  |---|---|---|---|---|---|
  | Junior | 51,073 | 0.04 | 47,630 | 0.04 | 30.0% |
  | Middle | 1,08,289 | 0.11 | 71,368 | 0.10 | 54.7% |
  | Senior | 39,604 | 0.31 | 10,627 | 0.25 | 15.3% |

  - Inference (**M**): roughly 15% to 40% of Infosys staff earn above the zero-tax line. That is all of the senior band plus an unknown part of the middle band.
- **Six IT services firms together, FY26**: about 16.2 lakh employees, standalone employee cost Rs 2.91 lakh crore, standalone current tax Rs 34,391 crore (FY25: Rs 35,737 crore). The current tax includes taxes paid by overseas branches. **M**.
  - FY25 current tax ≈ **3.6%** of FY2024-25 net corporation tax of Rs 9.86 lakh crore. The denominator is CBDT provisional **[S]**, via https://a2ztaxcorp.net/?p=20860.

### 2.2 Central government employees (H)

Source: Department of Expenditure, *Annual Report on Pay and Allowances of Central Government Civilian Employees 2023-24*, https://doe.gov.in/files/annual_reports_documents/AnnualReportonPayAllowance202324.pdf. Output: `central_govt_employees_pay.csv`.

- **Regular civilian employees in position on 01.03.2024** (Table 20, printed p.41, a scanned table that I read from the page image):

  | Group | Employees | Share |
  |---|---|---|
  | A | 1,15,326 | **3.65%** |
  | B | 3,04,138 | 9.63% |
  | C | 27,37,898 | 86.7% |
  | Total | 31,57,362 | |

- **Pay and allowances, FY2022-23**: Rs 2,75,083.75 crore (para 1). Split: pay 60.45%, DA 21.04%, HRA 5.56%, other 12.95%.
  - Divided by 30.62 lakh employees, that is **about Rs 8.98 lakh per employee per year** (derived). It excludes bonus, leave encashment and TA.
- So the *average* central civil servant was below today's Rs 12.75 lakh line (DA has risen since, so the FY26 average is higher; not computed). Group A, and senior Group B, are above it. Railways and Home Affairs (police) are 72% of headcount.
- Not verified (search budget ran out): 7th CPC pay-matrix entry values and the current DA rate. I did not compute a pay-level-by-level threshold. Defence, CPSEs and state government employees are not covered.

### 2.3 Sector and occupation in tax records

- **Nature-of-business codes** (CBDT ITR Statistics AY 2023-24, Table 7.1, PDF pp.77–91). Output: `data/tax_linkage/cbdt_itr_ay2023-24_business_codes.csv`, 364 codes; checked that corporate + non-corporate = total in every row. **H**.
  - This table gives *counts of returns* only, with no income or tax.
  - **Wholesale & retail trade: 1.47 crore of 2.03 crore** coded returns (**72%**); non-corporate 1.35 crore.
  - Professions (legal, accounting, consultancy and so on): 6.97 lakh.
  - Financial intermediation: 6.62 lakh.
  - Computer & related services: 1.62 lakh, of which 77,890 are companies and 84,190 non-corporate.
  - Healthcare: 2.34 lakh.
  - The non-salaried filer base is mostly small traders, presumptive under s.44AD, in low AI-exposure work.
- **Corporate tax by industry**: see the tax agent's `data/tax/corporate_tax_by_industry_FY2023-24.csv` (Receipt Budget 2026-27, Annexure-7).
  - Computer & related services paid **10.9%** of company gross tax payable (software development 7.4%); financial intermediation paid 27.1%.
- **TDS by deductor category** (government vs non-government; s.192 salary TDS): **no official series found**, by me or the tax agent. CBDT Time Series Table 1.2 shows a "C.T.D.S." line of Rs 40,548 crore in FY2023-24, but it is not defined in the table.
- **Claims like "IT employees pay X% of income tax"**: none verified. No official source publishes personal income tax by employer sector. Any such number is a model.

---

## 3. Salaried vs business vs professional income at the top (H/M)

Source: ITR Statistics AY 2023-24, p.6 (status-wise key values) and Tables 2.1, 2.2, 2.4.

- **Individuals' income by head** (total before loss set-off, Rs 62.38 lakh crore):
  - Salary Rs 35.23 lakh crore (**56.5%**)
  - Business/profession Rs 16.68 lakh crore (**26.7%**)
  - Other sources Rs 6.81 lakh crore (10.9%)
  - Long-term capital gains Rs 2.54 lakh crore (4.1%)
  - Short-term capital gains Rs 0.44 lakh crore
  - House property Rs 0.67 lakh crore
- **Share of individuals above each GTI line whose salary alone exceeds it** (a lower bound on "mainly salaried"):

  | Above | Salaried share | Business share |
  |---|---|---|
  | Rs 12.75 lakh | **77%** | 12% |
  | Rs 50 lakh | **61%** | 15% |
  | Rs 1 crore | **52%** | 16% |
  | Rs 5 crore | **32%** | 14% |

  - The rest are mixed-income people or those whose income is capital gains, interest or dividends.
  - The 52% above Rs 1 crore reproduces the widely reported "52% of crorepatis are salaried" (Business Standard, Oct 2024) **[S]**: 1,18,018 ÷ 2,27,315.
- **Money above Rs 50 lakh**: salary income held by people with salary above Rs 50 lakh = Rs 4.75 lakh crore, against Rs 9.92 lakh crore of GTI held by people with GTI above Rs 50 lakh, i.e. about 48% (derived; different sets of people).
- Professional income (doctors, lawyers, chartered accountants) is inside "business income". CBDT does not separate it, so its share at the top cannot be computed from published tables.
- Professions account for 6.97 lakh of 2.03 crore business-code returns (count only).

---

## 4. Geography

### 4.1 State-wise direct tax collections (H)

Source: CBDT *Time Series Data FY2000-01 to FY2023-24*, Table 1.2 "State and U.T. wise break-up of collection" (PDF pp.3–4; FY2023-24 provisional, from DGIT Systems). I parsed the tax agent's copy, `data/raw/tax/time_series_FY2000-01_to_2023-24.pdf` (official URL https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Final-Approved-Time-Series-Data-2023-24-English.pdf).
Script: `scripts/tax_linkage/parse_statewise_direct_tax.py`; output `data/tax_linkage/statewise_direct_tax_FY2019-FY2024.csv`. State sums reconcile to the printed sub-totals.

| State | FY2022-23 (Rs cr) | Share | FY2023-24 (Rs cr) | Share |
|---|---|---|---|---|
| Maharashtra | 6,05,268 | 36.4% | **7,61,716** | **38.8%** |
| Karnataka | 2,08,169 | 12.5% | 2,34,098 | 11.9% |
| Delhi | 2,21,522 | 13.3% | 2,03,197 | 10.4% |
| Tamil Nadu | 1,07,064 | 6.4% | 1,27,067 | 6.5% |
| Gujarat | 85,019 | 5.1% | 93,301 | 4.8% |
| Telangana | 35,434 | 2.1% | 84,439 | 4.3% |
| Haryana | 45,650 | 2.7% | 70,947 | 3.6% |
| Grand total | 16,63,686 | | 19,61,823 | |

- The top three states hold 61.1% and the top six 76.7% (FY2023-24).
- These shares match the SBI Research figures quoted in the press (Maharashtra 38.9%, Karnataka 11.9%, Delhi 10.4%, TN 6.5%, Gujarat 4.8%) **[S]**.
- **Caveat (printed in the table)**: a state is assigned by the **state code in the taxpayer's communication address**. Company tax and TDS are therefore booked where the company or deductor is registered (for example, Mumbai head offices), not where employees work.
  - The FY2023-24 swing from Andhra Pradesh (57,324 → 26,066) to Telangana (35,434 → 84,439) looks like an address/state-code reclassification. The two states combined went from 92,758 to 1,10,506.
- **FY2024-25** (CBDT Time Series to FY2024-25, released Nov 2025; the official PDF was blocked to me, HTTP 403):
  - Maharashtra Rs 8.97 lakh crore, Karnataka Rs 2.61 lakh crore, Delhi Rs 2.29 lakh crore **[S]** (CAclubindia). **L–M**.
  - Lok Sabha USQ 57 (1 Dec 2025) gives Tamil Nadu Rs 1,32,368.09 crore (6.06%) **[S]**, seen only in a search snippet because sansad.in was unreachable. **L**.

### 4.2 Where IT and GCC jobs are

- Economic Survey 2025-26, ch.7, para 7.33 and Chart VII.12 (citing Nasscom): **1,700+ GCCs (FY24), employing about 19 lakh**, with GCC revenue of USD 64.6 bn (FY24 estimate). It notes expansion into tier-2 and tier-3 cities. **M**. Source: https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap07.pdf, printed pp.279–280.
- **City split (Bengaluru, Hyderabad, Pune, Chennai, NCR, Mumbai): not verified (gap).** The web-search budget ran out. The Deloitte page cited by the Survey gives no city split.
  - Candidate sources: the Nasscom–Zinnov GCC landscape report, STPI state-wise software exports, and Karnataka and Telangana IT department annual reports.

---

## 5. Consumption and GST

### 5.1 HCES 2023-24 MPCE by fractile class (H; pooled estimate M)

Source: MoSPI NSS Report 592, *Survey on Household Consumption Expenditure 2023-24*, Tables 3.1 and 3.2 (printed pp.22–23). URL: https://mospi.gov.in/sites/default/files/publication_reports/Final_Report_HCES_2023-24L.pdf.
Outputs: `data/tax_linkage/hces_fractile_mpce_and_consumption_shares.csv` and `hces_top_consumption_shares.csv`.

- **Average MPCE (2023-24)**: rural Rs 4,122, urban Rs 6,996.
  - Top 5%: rural Rs 10,137, urban Rs 20,310.
  - Bottom 5%: rural Rs 1,677, urban Rs 2,376.
  - The fractile means reproduce the published averages (4,122 and 6,996).
- **Share of consumption** (computed from fractile means):

  | Group | Rural 2023-24 | Urban 2023-24 | All-India pooled (estimate) | 2022-23 rural / urban |
  |---|---|---|---|---|
  | Top 5% | 12.3% | 14.5% | ~14.1–14.4% | 13.9% / 16.1% |
  | Top 10% | 20.7% | 23.7% | ~24.1–24.2% | 22.7% / 25.7% |
  | Top 20% | 34.7% | 38.2% | ~38.8–39.1% | 36.9% / 40.6% |

  - The pooled column assumes a rural population share of 62–68%, because HCES Table A2 (population) is Excel-only. Cells are ranked by mean MPCE, assuming uniform spending within each cell.
- Caveats:
  - MPCE excludes imputed free items (PDS and so on).
  - The survey under-captures rich households' spending.
  - Consumption is not income: the rich save more, so their share of consumption is far below their share of income. The top 10% get 57.7% of income per WIL, against ~24% of consumption.

### 5.2 GST incidence (M)

Source: S. Mukherjee, *Distributional Impact of Indian GST based on the NSSO's HCES 2022-23*, NIPFP Working Paper 430 (July 2025), Abstract and Figure 7 (PDF pp.2, 14). URL: https://nipfp.org.in/media/documents/WP-430_2025.pdf. Output: `gst_burden_by_mpce_fractile_nipfp.csv`.

| Share of GST burden | Rural | Urban |
|---|---|---|
| Top 5% | 14.3% | 17.1% |
| Top 10% | 23.1% | 26.4% |
| Top 20% | **37.3%** | **40.9%** |
| Bottom 50% | 31.4% | 28.6% |

- GST burden shares are slightly above consumption shares: top 5% consumption was 13.9% rural and 16.1% urban in 2022-23. GST is mildly progressive on an expenditure basis (Kakwani and Reynolds-Smolensky indices are positive).
- Assumptions: full pass-through, purchases from registered sellers, no cascading. The rates are **pre-September-2025 (GST 2.0)**, and the analysis is within rural and within urban areas, not national.
- **Oxfam India "Survival of the Richest" (Jan 2023)**: "bottom 50% pay 64.3% of GST, top 10% pay 3–4%". **L**: the method is disputed, it contradicts NIPFP, and the government says it keeps no income-group GST data (Rajya Sabha reply) **[S]**.

---

## 6. IT/ITeS sector macro (H/M)

Output: `data/tax_linkage/it_services_macro.csv`.

- **Telecom, computer & information services exports** (RBI BoP, BPM6; Economic Survey 2025-26 Statistical Appendix Table 5.3B, https://www.indiabudget.gov.in/economicsurvey/doc/stat/tab5.3b.pdf):

  | Year | USD bn |
  |---|---|
  | FY23 | 152.3 |
  | FY24 | 163.6 |
  | FY25 (partially revised) | **183.3** |
  | FY26 H1 (provisional) | 98.3 |

  - Other business services (which include much GCC work) were USD 107.2 bn in FY25. Total services exports were USD 387.6 bn.
- **RBI software-exports survey 2024-25**: software services exports +7.3% YoY; US share 52.9%, Europe 32.8%; about 72% invoiced in USD. Cited in Economic Survey 2025-26 ch.4, paras 4.59 and footnote, because the RBI PDF itself sits behind a CAPTCHA, which I did not bypass. **M**.
- **Nasscom IT&ITeS revenue FY25**: USD 283 bn including hardware, +5.1% (Economic Survey 2025-26, para 7.32). **M**.
- **IT's share of corporate tax**: computer & related services 10.9% of company gross tax payable (FY2023-24 returns; tax agent).
  - The six large IT firms' standalone current tax was Rs 35,737 crore in FY25, about 3.6% of net corporation tax (§2.1).
- **Not found**:
  - an official IT share of GDP (Nasscom's ~7% claim was not verified here);
  - any estimate of *total* (direct + indirect) taxes generated by IT-BPM employment.

---

## Gaps

1. No official personal-income-tax-by-sector or by-employer data; no s.192 salary-TDS series; no TDS-by-deductor-category series.
2. No published PLFS p95/p99 or share of workers above Rs 50,000 / Rs 1 lakh a month. Unit-level microdata needs a login, which I did not attempt.
3. TCS median pay: the statutory MRE and the BRSR medians are inconsistent. HCLTech and the banks do not print an MRE.
4. FY2024-25 state-wise table: only secondary figures. City-level GCC and IT employment shares were not verified.
5. 7th CPC pay-matrix and DA arithmetic was not verified, so there is no count of government employees by pay level above Rs 12.75 lakh.
6. HCES pooled national shares depend on an assumed rural population share; NIPFP incidence uses pre-GST-2.0 rates.
7. The web-search quota (shared across agents) ran out mid-task. Items marked **[S]** came from search snippets or press reports and should be re-checked against primaries.

## Files

- **Data** (`data/tax_linkage/`):
  - `itr_salary_business_thresholds_AY2023-24.csv`
  - `cbdt_itr_ay2023-24_individual_income_heads_by_range.csv`
  - `cbdt_itr_ay2023-24_business_codes.csv`
  - `firm_median_pay.csv`
  - `central_govt_employees_pay.csv`
  - `occupation_earnings_vs_zero_tax_line.csv`
  - `earnings_distribution_benchmarks.csv`
  - `statewise_direct_tax_FY2019-FY2024.csv`
  - `hces_fractile_mpce_and_consumption_shares.csv`
  - `hces_top_consumption_shares.csv`
  - `gst_burden_by_mpce_fractile_nipfp.csv`
  - `it_services_macro.csv`
- **Scripts** (`scripts/tax_linkage/`):
  - `parse_itr_stats.py`
  - `parse_statewise_direct_tax.py`
  - `derive_linkage_tables.py`
  - `firm_*.py`
- **Raw** (`data/raw/tax_linkage/`):
  - CBDT ITR statistics AY2023-24 (copy)
  - HCES 2023-24 report and factsheet
  - NIPFP WP430 and slides
  - WIL WP 2024/09 and issue brief
  - Economic Survey 2025-26 ch.4, 7, 14 and Statistical Appendix Tables 5.3B and 2.3
  - DoE pay & allowances 2023-24
  - PRS Vital Stats
  - PIB ITR note
  - India Labour Observatory CSV
  - `company_reports/` (21 annual reports)
