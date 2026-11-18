# PLFS employment backbone for the India jobs treemap

Lane: employment counts and composition from **published** PLFS (Periodic Labour Force Survey) tables. No unit-level data was used. Nothing was logged into: microdata.gov.in needs an account, so it was not touched.
Compiled 2026-11-09. Every number below gives its source (IDs [S1]..[S12], listed in section 8), the table and page, and the reference period. "PDF p." means the page number in the PDF file. "report p." means the number printed on the page.

---

## 1. Key numbers

| What | Value | Period / age | Source |
|---|---|---|---|
| Workers, usual status (ps+ss), **MoSPI's own absolute estimate** | **61.64 crore** (616,368 thousand): male 415,805 th, female 200,563 th | Jan-Dec 2025, age 15+ | [S1] Statement 32, PDF p.71 (report p.41); method in Annexure C, PDF p.567. The press note [S2] p.4 says "61.6 crore" |
| Same, rural / urban | rural 266,078 + 149,914 th; urban 149,727 + 50,649 th (male + female) | 2025, 15+ | [S1] Statement 32 |
| WPR, usual status (ps+ss) | 57.4% at age 15+; 43.5% at all ages | 2025 | [S1] Table 17.0 (Excel); Statement 4 |
| Workers, all ages (**our calculation**, MoSPI's method applied to all ages) | **61.74 crore** (617.4 million) | 2025 | Derived: all-ages WPR from [S9] times MoHFW/TG projection [S7]. See §4 |
| Same calculation for earlier years | 2023-24: 60.79 cr; 2017-18: 45.82 cr; CY2022: 54.36 cr; CY2023: 60.15 cr; CY2024: 60.64 cr | all ages | Derived, `plfs_absolute_workers.csv` |
| RBI KLEMS total employment (for comparison) | 64.33 crore in 2023-24 (provisional); 47.5 crore in 2017-18 | fiscal years | [S11] PIB release 2035280, 22 Jul 2024. RBI's KLEMS page still lists July 2024 as the latest release |
| Status in employment | self-employed 56.2% (own-account/employer 40.5, unpaid helper 15.6); regular wage/salaried 23.6%; casual 20.2% | 2025, all ages | [S1] Statement 7, PDF p.47 |
| ... the same in 2017-18 | 52.2 (38.6 + 13.6) / 22.8 / 24.9 | Jul 2017-Jun 2018 | [S5] Statement 14, PDF p.100 |
| Broad industry | agriculture 43.0%, manufacturing 12.1, construction 12.0, trade/hotels 12.9, transport/storage/communication 5.8, other services 13.1 | 2025 | [S1] Statement 8, PDF p.49 |
| Occupation divisions (NCO-2015), share of workers | 1 Managers 2.68%; 2 Professionals 5.55; 3 Technicians/associate professionals 2.53; 4 Clerks 2.20; 5 Service & sales 12.79; 6 Skilled agricultural 35.12; 7 Craft 11.37; 8 Plant & machine operators 5.89; 9 Elementary 21.86 | 2025, all ages | [S1] Table 25, PDF pp.229-231 + Excel [S1x] |
| White-collar divisions 1-4 combined | 12.96% of workers, about **80.0 million** (85.7 million under the cell method, see §4) | 2025 | Derived from Table 25 |
| Average earnings, regular wage/salaried (CWS) | Rs 22,699/month (male 24,217, female 18,353) | 2025 | [S1] Statement 11, PDF p.52 |
| ... by NCO division (rural+urban, persons) | Div 1 Rs 50,408; 2 Rs 38,466; 3 Rs 26,175; 4 Rs 24,289; 5 Rs 15,541; 6 Rs 13,377; 7 Rs 16,773; 8 Rs 17,301; 9 Rs 12,270 | 2025 | [S1] Table 51, PDF pp.370-372 |
| Casual labour daily wage (other than public works) | Rs 453/day | 2025 | [S1] Statement 12, PDF p.53 |
| Self-employed gross earnings | Rs 14,861 per 30 days | 2025 | [S1] Statement 13, PDF p.53 |
| Formality of regular wage/salaried employees, non-agriculture | no written contract 58.2%; no paid leave 47.3%; no social security 51.7%; **none of the three 36.9%** | 2025 | [S1] Statement 10 (PDF p.51) and Table 36 all-India row |
| Same in 2017-18 | 71.1% / 54.2% / 49.6% | 2017-18 | [S5] Statements 19-21, PDF pp.108-111 |
| Non-agriculture workers in proprietary or partnership firms (informal-sector proxy) | 73.1% | 2025 | [S1] Statement 9, PDF p.50 |
| Workers aged 15+ with graduate or higher degree | 14.7% (graduate 11.07, post-graduate and above 3.66) | 2025 | Derived from [S1] Table 8 (population share by education) times Table 23 (WPR by education) |

## 2. What exists and what was downloaded

All files are in `data/raw/plfs/`. `data/plfs/plfs_sources_manifest.csv` lists each file with its URL, size and SHA-256.

* **[S1] PLFS Annual Report 2025 (Jan-Dec 2025).** This is the first annual report on a calendar-year basis. It was released on 27 Mar 2026. The file used is the **revised version of 29-05-2026**, found through MoSPI's publications API. It has 653 pages, with detailed tables in Appendix A. **[S1x]** Each Appendix A table also exists as an Excel file, linked from the PDF: `.../uploads/documents/publicationsReports/APPENDIX-A/Table__NN.xlsx`. 22 of these were downloaded. They were checked against the PDF and match (Table 25 values agree to two decimals).
* **[S2] Press note, AR 2025** (the URL in the brief).
* **[S3] PLFS Annual Report 2023-24 (Jul 2023-Jun 2024)**, plus 14 Appendix A Excel files from `.../PLFS_AR23-24/Table_NN.xlsx`.
* **No Jul 2024-Jun 2025 annual report exists.** In January 2025 PLFS moved from the July-June cycle to the calendar year. The press note [S2] endnote (p.11) lists seven agricultural-year reports, 2017-18 to 2023-24, plus calendar-year key indicators for 2021-2024. The MoSPI publication list (queried on 2026-11-09) has no 2024-25 annual report. The bridge is **CY2024 key indicators** ([S4], downloaded) and the 2022-2024 comparison columns inside [S1].
* **[S5] PLFS Annual Report 2017-18.** It has no Excel files, so its tables were parsed from the PDF. ARs 2018-19 to 2022-23 were also downloaded, only to date the classification switch (§5).
* **[S6] "PLFS: Changes in 2025"**, which documents the sample redesign.
* **[S7] Technical Group on Population Projections, July 2020** (NCP/MoHFW). This is the exact file that [S1] cites in its footnote to Statement 32. Table 11 (PDF p.89) gives total population by sex on 1 July. Table 12 (PDF p.102) gives urban population.
* **[S8] MoSPI publications API.** `POST https://www.mospi.gov.in/api/publications-reports/get-web-publications-report-list` was used to find the report URLs.
* **[S9] eSankhyiki / MoSPI PLFS API.** `GET https://api.mospi.gov.in/api/plfs/getData` (the swagger spec is at `https://api.mospi.gov.in/layout/swagger_user_plfs.yaml`). GET calls worked without a token. The server needs legacy TLS renegotiation, which `fetch_mospi_api.py` handles. It serves 8 indicators: LFPR, WPR, UR, percentage distribution of workers, and three earnings measures. Coverage is 2017-18 to 2023-24 and CY2022 to 2025. Raw pulls are in `data/raw/plfs/api/`.
  * Calendar years 2022-2025 include distributions by NCO 3-digit group and NIC 4-digit class, and status by industry.
  * Agricultural years include only NCO 1-digit division and NIC section.
  * The API labels the 2021-22 to 2023-24 NCO rows with NCO-2004 division titles. Those years were actually coded in NCO-2015. The 2023-24 values match AR Table 25 (NCO-2015).
  * The API's agricultural-year status-by-industry rows have no industry label, so they were not used.
  * The API has **no occupation x status or occupation x industry crosstab**. All dimension combinations in the 2025 pull were checked.
* **[S10] RBI KLEMS.** The listing page and the July 2024 manual page were saved. The KLEMS xlsx on rbidocs.rbi.org.in returned a bot-protection challenge page. It was not bypassed, so the KLEMS figures come from [S11], the PIB release.

## 3. Published granularity, and what went into each CSV

All workers are in usual status (ps+ss). The distribution tables (25, 26, 19, 20, Statements 7/8) state no age restriction, so they cover **all ages**. Education tables are for age 15+. Earnings use current weekly status (CWS).

| Need | 2025 [S1] | 2023-24 [S3] | 2017-18 [S5] | CSV |
|---|---|---|---|---|
| (a) occupation | Table 25: NCO-2015 at 3-digit group (about 125 groups), 2-digit and 1-digit; rural/urban x male/female/person | Table 25, same level | Table 25 in NCO-2004 at 3-digit, plus PLFS design-based "estd. workers(00)" | `plfs_workers_by_occupation_nco.csv` |
| (b) industry | Table 26: NIC-2008 4-digit class, 3-digit, 2-digit division and section | same | same, parsed from PDF | `plfs_workers_by_industry_nic.csv`, `plfs_broad_industry.csv` (Statement 8, CY2022-2025) |
| time series | API: NCO division and NIC section for every year 2017-18 to 2025; NCO 3-digit for CY2022-2025 | | | `plfs_series_nic_section_nco_division_api.csv` |
| (c) status | Statement 7 (CY2022-2025) | Table 19, all-India rows | Statement 14 | `plfs_status_in_employment.csv` |
| (g) status x industry | Table 20 (11 NIC groups x 5 statuses) | Table 20 | (not extracted) | same file, `cross_code` = status |
| (d) education | Table 8 (population 15+ by education); Table 23 (WPR by education); derived worker distribution; Table 21 (status x broad industry x education, age 15+); Table 11.0 (years of schooling of workers by NIC section) | Tables 8 and 23 plus the derived distribution | (not extracted) | `plfs_education.csv` |
| (e) earnings | Statements 11-13 (CY2022-2025); Tables 38-40; **Table 51: regular-wage earnings by NCO division**; **Table 52: casual wage by NIC section**; all with sample sizes | Table 50 (by NCO division), Table 51 (by section), Tables 38-40 quarterly | Tables 42/43/45 quarterly, plus a derived annual figure (quarters weighted by MoSPI's estimated counts) | `plfs_earnings.csv` |
| (f) formality | Statements 9 and 10 (CY2022-2025); Table 36 (incl. "none of the three"); Table 35 (enterprise type); Table 37 (enterprise type x size) | Tables 35-37 | Statements 19-21 | `plfs_formality.csv` |
| absolute numbers | Statement 32 | derived | derived | `plfs_absolute_workers.csv`, `plfs_worker_counts_by_nco_nic.csv` |
| change | | | | `plfs_change_nco_nic.csv` |

All CSVs share these columns: `table, period, sector, sex, age_group, category_code, category_name, category_level, cross_code, cross_name, value, unit, classification, source_url, page_or_table, notes`. This is a superset of the requested set. Crosstabs carry the second dimension in `cross_*`. Derived rows have `table` starting with `DERIVED` and an explanation in `notes`.

## 4. Absolute numbers

**MoSPI's figure (2025, age 15+).**
* Method (Annexure C, PDF p.567): take the MoHFW all-ages projection for 1 July 2025 by sex, total and urban. Rural is total minus urban.
* Multiply by the PLFS proportion aged 15+, which comes from sample weights.
* Multiply by WPR at 15+.
* Result: Rural male 339,385 th x 78.4% = 266,078 th; rural female 333,885 x 44.9% = 149,914; urban male 205,106 x 73.0% = 149,727; urban female 195,556 x 25.9% = 50,649.
* **Total 616,368 thousand.** Our script re-checks each product and confirms the numbers appear on the page.

**Our all-ages figure (needed because Tables 25 and 26 cover all ages).**
* Workers = sum over rural/urban and male/female of WPR(all ages, ps+ss) x projected population.
* Population comes from [S7] Tables 11 and 12, 1 July. For agricultural years we averaged the two adjoining 1 July values, giving a 1 January mid-point.
* WPR comes from [S9] indicator 2. It matches [S1] Table 17.0 (2025, all ages: rural 57.2/33.8, urban 57.2/20.7) and [S5] Statement 11 (2017-18: 34.7%).
* Results: 2025 617.4 M; 2023-24 607.9 M; 2017-18 458.2 M.
* The 2025 all-ages total is only about 1.0 M above MoSPI's 15+ figure. That gap is child workers plus rounding of the WPRs.
* Workers, all ages, by year: 2017-18 458.2 M; 2018-19 471.4; 2019-20 514.1; 2020-21 540.3; 2021-22 543.1; 2022-23 564.3; 2023-24 607.9; CY2022 543.6; CY2023 601.5; CY2024 606.4; CY2025 617.4.

**KLEMS comparison.** RBI KLEMS gives 47.5 cr (2017-18) and 64.33 cr (2023-24) [S11]. That is 3.7% and 5.8% above our figures. KLEMS uses a different method, described in RBI's KLEMS 2024 manual, §4.1, on the [S10] page:
* For 2017-18 to 2019-20 it uses a Government of India total.
* After that it grows that total with MoHFW growth rates, applying the same rate to rural and urban.
* It centres each estimate on 1 October of the fiscal year.
* So the two series are not like-for-like. Use PLFS-based figures for the treemap.

**Two ways to turn a share into a count.**

| Method | How it works | Effect |
|---|---|---|
| `NATIONAL_SHARE` (recommended for tile areas) | published rural+urban person share x total | Reproduces MoSPI's published national shares exactly |
| `CELL_SUM` | sum over the four rural/urban x sex cells of cell share x cell workers | Consistent with Statement 32's rural/urban totals |

* The two differ because PLFS's own weights imply that about **28.5%** of workers are urban. This is solved from Table 26 section A: 43.03 = 57.17(1-u) + 7.52u. The MoHFW urban projection used in Statement 32 implies **32.5%**.
* So `CELL_SUM` gives more urban-heavy categories. Examples: agriculture 251.6 M vs 265.7 M; NIC section J 9.1 M vs 8.3 M; NCO divisions 1-4 85.7 M vs 80.0 M.
* Both are in `plfs_worker_counts_by_nco_nic.csv`. Change tables use `NATIONAL_SHARE`.

## 5. Change over time (the "outlook" analog) and why to be careful

1. **The industry series is consistent.** NIC-2008 is used in every year from 2017-18 to 2025.
   * Using `NATIONAL_SHARE` counts, total workers rose 34.7% from 2017-18 to 2025.
   * Faster than average: J information and communication +82% (4.5 to 8.3 M), Q health +74%, I accommodation and food +57%, T households as employers +57%, K finance +50%, G trade +44%, F construction +39%, C manufacturing +35%.
   * Close to or below average: A agriculture +31% (202 to 266 M; its share went from 44.1% to 43.0%), O public administration +18%, P education +16%, B mining -8%.
   * Sources: `plfs_change_nco_nic.csv`, built from [S5] and [S1] Table 26.
2. **The occupation series is broken.**
   * PLFS coded occupations in NCO-2004 up to 2020-21 and in **NCO-2015 from July 2021**. Source: AR 2021-22, para 3.3.7.1, PDF p.99 (report p.59).
   * So 2017-18 to 2025 by occupation is **not comparable**. Division 1 is 7.4% in 2017-18 and 2.68% in 2025. Under NCO-2004 practice, own-account shopkeepers were largely coded as managers (group 121 alone was 5.97% in 2017-18). In 2025 they appear as 522 shop salespersons (6.98%).
   * Even inside NCO-2015 there is a drift. Division 1 went 7.2% (2021-22), 4.9 (CY2022), 3.7 (2022-23), 3.4 (CY2023), 3.3 (CY2024), 2.7 (CY2025). Division 5 rose from 9.8 to 12.8 over the same years. Group 112 (managing directors and chief executives) fell from about 16.5 M (CY2022) to 7.7 M (2025).
   * This looks like a change in coding practice, not real job change. MoSPI publishes no explanation. Treat occupation changes in Divisions 1 and 5 as unreliable.
   * The least-bad occupation outlook proxies are 2023-24 to 2025 or CY2022 to CY2025. Both are in `plfs_change_nco_nic.csv`.
3. **Other breaks in 2025.** The 2025 survey was redesigned [S6]: 2.65 times the sample, district strata, a rotational panel, and a switch to calendar years. MoSPI still prints 2022-2025 side by side in [S1] Statements 7-13, which implies it treats them as comparable. 2023-24 to 2025 also compares an agricultural year with a calendar year.
4. **Status.** The regular wage share was 22.8% (2017-18), 21.7% (2023-24) and 23.6% (2025). The casual share fell from 24.9% to 20.2%. Unpaid helpers rose from 13.6% to 15.6%, driven by rising female participation in agriculture.
5. **Formality.** Lack of a written contract among regular wage employees fell from 71.1% to 58.2%. "No social security benefit" rose slightly, from 49.6% to 51.7%. Both years count the same benefits: PF/pension, gratuity, and health care/maternity ([S5] Statement 21 note; [S1] p.51).

## 6. Building blocks for the "AI threatens the tax base" claim

PLFS cannot say who pays income tax. That is the tax lane. These facts are relevant:

* **The "green" bulk.**
  * NCO Division 6 (skilled agricultural) plus 92 (farm labourers) plus 93 (construction, manufacturing and transport labourers) make up 35.1% + 7.8% + 11.1%, about **54%** of workers.
  * NIC section A is 43.0%. Section F (construction) is 12.0%.
* **The white-collar segment is small.**
  * NCO Divisions 1-4 are 12.96% of workers, about 80 M.
  * ICT professionals (sub-division 25) are 0.70%, about 4.3 M. Group 251 (software developers) is 0.65%, about 4.0 M. ICT technicians (sub-division 35) are 0.15%, about 0.9 M.
  * Clerks (Division 4) are 2.20%, about 13.6 M. Of these, customer services clerks (sub-division 42, which includes call-centre work) are 0.37%, about 2.3 M.
  * By industry: J information and communication is 1.34% (8.3 M) and K finance and insurance is 1.17% (7.2 M).
  * Source: [S1] Tables 25 and 26 with the all-ages total.
* **Pay is concentrated in Divisions 1-3.**
  * Regular wage/salaried earnings in Division 1 are 2.2 times the average, and Division 2 is 1.7 times ([S1] Table 51).
  * Sample sizes behind those averages: 5,273 (Div 1) and 25,048 (Div 2).
  * Table 51 covers employees only. Self-employed "managers" and professionals are not included.
* **Formal salaried jobs are a minority.**
  * Regular wage/salaried employees are 23.6% of workers, about 145 M.
  * Among non-agriculture employees, 48.3% have any specified social security benefit, and 36.9% have none of contract, paid leave or social security.
  * As a rough derived number, non-agriculture regular-wage employees with social security come to about 69 M. That is 23.6% x 617 M, less the roughly 1.2% of agriculture workers who are salaried, times 0.483. This is order-of-magnitude only.
  * Only 11.7% of non-agriculture workers are in public or private limited companies, and 10.3% are in government or public sector bodies ([S1] Table 35, all-India).
* **Education.** 14.7% of workers aged 15+ are graduates or above, about 90 M.

## 7. Files

**Outputs (`data/plfs/`)**

| File | Contents |
|---|---|
| `plfs_workers_by_occupation_nco.csv` | Table 25 for 2025 and 2023-24 (NCO-2015) and 2017-18 (NCO-2004): % of workers, 9 sector x sex cells, plus sample sizes and the 2017-18 design-based totals |
| `plfs_workers_by_industry_nic.csv` | Table 26 for the same three years: NIC class, group, division and section |
| `plfs_series_nic_section_nco_division_api.csv` | API time series for 2017-18 to 2025 by NIC section and NCO division, plus NCO groups for CY2022-2025 |
| `plfs_status_in_employment.csv` | Statement 7, Table 19 and Statement 14, plus the Table 20 status x industry crosstab |
| `plfs_broad_industry.csv` | Statement 8, CY2022-2025 |
| `plfs_education.csv` | Tables 8, 23, 21 and 11.0, plus the derived worker distribution by education |
| `plfs_earnings.csv` | Statements 11-13; Tables 38-40 and 50-52 (2025 and 2023-24); 2017-18 Tables 42/43/45 plus a derived annual figure |
| `plfs_formality.csv` | Statements 9 and 10, Tables 35-37, 2017-18 Statements 19-21 |
| `plfs_absolute_workers.csv` | Statement 32 inputs and outputs; derived all-ages totals for 11 periods with their WPR and population inputs; KLEMS figures |
| `plfs_worker_counts_by_nco_nic.csv` | Derived counts in thousands by NCO and NIC category, both methods |
| `plfs_change_nco_nic.csv` | Derived change: 2017-18 to 2025 (NIC section and division; NCO division flagged not comparable), 2023-24 to 2025 (NCO-2015 group and division, NIC division), CY2022 to 2025 (NCO group and division, NIC section) |
| `plfs_sources_manifest.csv` | Raw file to URL, with bytes and SHA-256 |

**Scripts (`scripts/plfs/`)**, run in this order:
1. `fetch_mospi_api.py`
2. `build_nco_nic.py`
3. `build_series_api.py`
4. `build_statements.py`
5. `build_absolute.py`
6. `make_manifest.py`

They share `plfs_common.py` (sources, NCO title dictionaries, parsers). The helpers `pdf2txt.py`, `xlsx_dump.py` and `find_pages.py` were used for inspection.

## 8. Sources

* [S1] AR PLFS 2025 (rev. 29-05-2026): https://www.mospi.gov.in/uploads/publications_reports/publications_reports1780040415321_0624fb13-fb47-40bc-b470-7c7e9635c3ef_PLFS_2025_F_REV_29052026.pdf
* [S1x] AR 2025 Excel tables: https://www.mospi.gov.in/uploads/documents/publicationsReports/APPENDIX-A/Table__{N}.xlsx
* [S2] Press note, 27 Mar 2026: https://www.mospi.gov.in/uploads/latestReleases/latest_release_1774607827733_3e8964a9-268b-4cc9-ad65-cfc8a9e32f08_Press_note_AR_PLFS_2025_23032025_V2.1_26032026_final.pdf
* [S3] AR PLFS 2023-24: https://www.mospi.gov.in/sites/default/files/publication_reports/AnnualReport_PLFS2023-24L2.pdf, with Excel at `.../publication_reports/PLFS_AR23-24/Table_{N}.xlsx`
* [S4] Key indicators CY2024: https://www.mospi.gov.in/sites/default/files/publication_reports/Key_employment_unemployment_indicators_PLFS_2024_final.pdf
* [S5] AR PLFS 2017-18: https://www.mospi.gov.in/sites/default/files/publication_reports/Annual%20Report%2C%20PLFS%202017-18_31052019.pdf
* [S5b] AR PLFS 2021-22 (NCO switch note, PDF p.99): https://www.mospi.gov.in/sites/default/files/publication_reports/AnnualReportPLFS2021-22F1.pdf
* [S6] PLFS Changes in 2025: https://www.mospi.gov.in/sites/default/files/publication_reports/PLFS_changes_in_2025_Final.pdf
* [S7] Technical Group population projections (July 2020), as cited by [S1]: https://www.mohfw-dohfw.gov.in/static/uploads/2025/10/1c3c2048814bd3747f44e661f8547055.pdf
* [S8] MoSPI publications API: https://www.mospi.gov.in/api/publications-reports/get-web-publications-report-list
* [S9] MoSPI PLFS API: https://api.mospi.gov.in/api/plfs/getData (spec: https://api.mospi.gov.in/layout/swagger_user_plfs.yaml)
* [S10] RBI KLEMS page: https://www.rbi.org.in/Scripts/KLEMS.aspx; manual: https://www.rbi.org.in/Scripts/PublicationReportDetails.aspx?ID=1275
* [S11] PIB (Ministry of Labour and Employment), 22 Jul 2024, "Employment in the Country Increased to 64.33 crore in 2023-24...": https://pib.gov.in/PressReleasePage.aspx?PRID=2035280

## 9. Extraction notes and checks

* **Excel was preferred over PDF.** Excel tables were spot-checked against the PDF and matched.
* **2017-18 was parsed from PDF text.** Each code is followed by exactly nine numbers. These checks passed:
  * Divisions sum to 100.00 and 3-digit groups to 99.93.
  * NIC sections sum to 99.98 and classes to 99.96.
  * API values agree, for example section A 44.1 vs 44.14 and NCO Division 1 7.4 vs 7.36.
* **Statements were parsed from PDF text by position** (for example, 54 numbers after "PLFS 2025 | rural"). Every statement was checked against its Excel all-India row where one exists. Statement 7 matches Table 19, Statement 10 matches Table 36, and Statement 11 matches Table 38.
* **Rounding.** Shares in Tables 25 and 26 are printed to 0.01%, which is about 62,000 workers in 2025. Small NCO groups and NIC classes are therefore very coarse, and many are 0.00. Counts below roughly 0.3 M should not be read as precise.
* **Category titles.** NIC section and division titles come from [S1] Annexure I (PDF pp.568-571). Three run-together words in the PDF text were fixed. NCO division and sub-division titles come from Annexure II (NCO-2015: [S1] PDF pp.572-573; NCO-2004: [S5] PDF p.70). The **3-digit NCO and 4-digit NIC titles are not printed in PLFS**. Those rows are labelled with their parent title only. Join full titles from the NCO/ILOSTAT lane. NCO-2015's 3-digit codes follow the ISCO-08 minor-group structure, but no titles were filled in from memory.
* **Literacy definitions differ.** "Secondary & above" in Table 8 (42.4% of people aged 15+ in 2025) is not the same measure as "at least secondary" in Statement 27 (67.8%). The latter counts middle-school completers as well (para 2.9.2.1, PDF p.67).
* **The Table 52 note** says a casual worker can work in more than one section in a day, so sections need not add up to "all".

## 10. Gaps (not published, or not found)

* **Occupation x industry and occupation x status crosstabs are not published** in any AR or in the API. Producing them needs PLFS unit-level data from microdata.gov.in (login required, not done). The unit records have NCO-2015 3-digit codes, NIC 5-digit codes, status, earnings and contract/leave/social security for every worker.
* No formality (contract, leave, social security) by industry or occupation. The ARs give it only by state.
* No regular-wage earnings by industry, and no self-employed earnings by industry or occupation. Earnings by NCO division cover regular wage/salaried employees only.
* No education by occupation.
* There is no Jul 2024-Jun 2025 annual report. CY2024 is the bridge.
* NCO comparisons from 2017-18 to 2025 are invalid because of the classification change, and 2021-22 to 2025 has the Division 1/5 drift.
* The RBI KLEMS xlsx was blocked by bot protection. The KLEMS numbers come from PIB, and no KLEMS release after July 2024 is listed.
* 2017-18 earnings are published only by quarter. The annual figures here are derived.
* The design-based "estimated workers" printed in AR tables (for example 37.26 crore in 2017-18, [S5] Table 25) are kept only as raw data. MoSPI says such figures "are not intended for providing the number of workers" ([S1] Appendix A note, PDF p.77).

## 11. Confidence

* **High:** all published shares and earnings (machine-extracted, with cross-checks); MoSPI's 61.6 crore; the NCO switch date.
* **Medium:** derived all-ages totals. They use the same projection and method as MoSPI, but the cell-versus-national weighting choice moves category counts by up to 5% (see §4).
* **Low:** any occupation-based change over time, and the rough derived count of employees with social security.
