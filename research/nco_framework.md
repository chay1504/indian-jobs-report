# India occupation framework (NCO-2015) and occupation-level statistics (ILOSTAT)

Lane: occupation classification and occupation-level statistics for the India version of the "US Job Market Visualizer".
Compiled 2026-11-09. Everything here comes from files downloaded into `data/raw/nco/`. Scripts are in `scripts/nco/`.

---

## 0. Bottom line

| Question | Answer |
|---|---|
| Finest occupation level with **employment** for India | **ISCO-08 2-digit (sub-major groups; 40 civilian cells)** for calendar years **2022, 2023, 2024 and 2025** (ILOSTAT `EMP_TEMP_SEX_OC2_NB`, PLFS microdata processed by the ILO). Before that: **ISCO-88 2-digit** for 2018–2020 (PLFS) and 2010 and 2012 (NSS EUS). **2021 has no 2-digit data**, because of the coding break described below. |
| Finest level with **employment AND earnings** | **ISCO 1-digit (major groups)**: ISCO-08 for **2022–2025** and ISCO-88 for **2018–2020**. ILO skill-level groups cover 2018–2025. There are no 2-digit earnings in ILOSTAT. Earnings cover **employees only**: mean and median monthly and hourly earnings, in current INR, USD and 2021 PPP$ (`EAR_EMTA/EMTM/EHRA/EHRM_SEX_OCU_*`). |
| Same codes in NCO and ISCO? | Yes, at 1, 2 and 3 digits (NCO-2015 sub-division code = ISCO-08 sub-major group code). So the 40 ILOSTAT 2-digit cells map one-to-one to the 40 NCO-2015 sub-divisions. NCO descriptions (4-digit families, 8-digit occupations) can feed LLM scoring of each cell. |
| Classification break | ILOSTAT codes PLFS occupations as **ISCO-88 through 2021Q2 and ISCO-08 from 2021Q3** (quarterly file `ilostat_ind_emp_by_occupation_quarterly.csv`). This fits PLFS moving from NCO-2004 to NCO-2015 with the 2021-22 round. Occupation growth from 2017-18 to the latest year therefore has to cross a classification change. Growth inside a single classification is possible only for 2022→2025 (ISCO-08). |
| NCO-2025? | Not found. The DGE NCO page lists only the NCO-2015 volumes ("Last Updated: 10/05/2024"). The DGE "Search NCO" web listing matches the 2015 PDFs. A web search found no DGE or MoLE release of a revised NCO. MoSPI did release **NIC-2025** (the industry classification, not occupations), according to press coverage found by search. |
| Outlook (growth) | Occupations: ISCO-08 2-digit CAGR 2022→2025 (`derived_isco08_2digit_profile.csv`). Industries: ISIC Rev.4 / NIC-2008 2-digit CAGR 2018→2025 (`derived_isic4_2digit_growth.csv`). RBI KLEMS could not be downloaded (bot protection on `rbidocs.rbi.org.in`). Projections are labelled in `data/nco/india_employment_projections.csv`. |

---

## 1. NCO-2015: structure, sources and alignment with ISCO-08

### 1.1 Sources (downloaded)
- Vol I (code structure, concordance with NCO-2004, alphabetical index; 384 pp.): https://dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_I-2015.pdf
- Vol II-A (descriptions, Divisions 1–5; 587 pp.): https://dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_II-A-2015.pdf
- Vol II-B (descriptions, Divisions 6–9; 581 pp.): https://dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_II-B-2015.pdf
- Landing page: https://dge.gov.in/nco-2015 ("Last Updated : 10/05/2024"). Web listing: https://dge.gov.in/nat?page=0..6 (3,447 rows; saved raw HTML in `data/raw/nco/dge_web/`)
- Official ISCO-08 code lists, used for code comparison only (titles are in French): INSEE https://www.insee.fr/fr/information/7749176 (`insee_nomenclature_N1..N4_ISCO.xlsx`). The ILO's own ISCO pages (ilostat.ilo.org, isco.ilo.org, ilo.org) returned HTTP 403 to scripted requests. English ISCO-08 titles at 1 and 2 digits come from the ILOSTAT code dictionary.

### 1.2 Hierarchy as parsed (`data/nco/nco2015_structure.csv`)
| Level (NCO term) | ISCO-08 term | NCO-2015 count | ISCO-08 count | Difference |
|---|---|---|---|---|
| Division (1 digit) | Major group | 9 | 10 | NCO has no Armed Forces division 0 |
| Sub-division (2 digits) | Sub-major group | 40 | 43 | ISCO 01, 02, 03 (armed forces) absent |
| Group (3 digits) | Minor group | 127 | 130 | ISCO 011, 021, 031 absent |
| Family (4 digits) | Unit group | 436 | 436 | 433 in common. **NCO-only: 6115** Medicinal and Aromatic Plant Cultivators, **6116** Agriculture Information Management, **7419** Electrical and Electronic Equipment Mechanics and Fitters n.e.c. **ISCO-only: 0110, 0210, 0310** |
| Occupation (8 digits, `dddd.ddQQ`) | none | 3,451 | none | NCO-specific level. The last 2 digits flag a Qualification Pack (QP-NOS) of the National Skill Qualification Framework; 879 occupations carry QP-NOS details |

Coding (Vol I, pp. 25–27): the first 4 digits are Division, Sub-division, Group and Family, which correspond to ISCO-08 major, sub-major, minor and unit groups. After the decimal, 2 digits identify the occupation and 2 digits the QP-NOS reference (00 means no QP). Example: 8153.0111 is Sewing Machine Operator, General.

Columns in `nco2015_structure.csv`:
- `code`, `level`, `title`
- `description`: tasks text from Vol II; empty for families 3434 and 3435, which have no description in the PDF
- `isco08_code`, `isco08_match`
- `isco08_title_en`: English title at 1 and 2 digits; for occupations, the title stated in Vol II
- `parent_code`, `division` to `family`
- `nco_skill_level`
- `nco2004_code`: from the Vol I concordance; present for 2,673 occupations
- `qp_nos`
- `source`: volume and page
- `note`

### 1.3 How NCO-2015 differs from ISCO-08
1. **Same code structure at 1–4 digits.** Vol I printed p. 25 maps the first 4 NCO-2015 digits onto ISCO-08 levels (Family = Unit Group). In the parsed data, 433 of 436 ISCO-08 unit groups appear as NCO families; these are all the civilian ones. NCO adds 3 India-specific families (listed above) and drops the armed forces. Page numbers in §1.3 are printed page numbers; the `source` and `note` columns of the CSV use PDF page numbers.
2. **Occupation-to-ISCO mapping is not always the family code.** Vol II prints "ISCO 08 Unit Group Details" for each occupation. For **73 occupations** the stated ISCO-08 unit differs from the NCO family. Examples: 1311.0x "General Manager, Plantation/Horticulture/Dairy…" maps to ISCO 611x/612x; 2424.x "Training and Staff Development" maps to ISCO 2423. Full list: `nco2015_occupations_mapped_to_other_isco08_unit.csv`. Occupations in 7419 point to "Electrical Mechanics and Fitters; Electronics Mechanics and Servicers" with no valid code.
3. **Skill levels are defined in years of schooling, with informal skills counted** (Vol I p. 18). Level I: up to 10 years of formal education and/or informal skills. Level II: 11–13 years. Level III: 14–15 years. Level IV: more than 15 years. Divisions are tied to levels (Vol I p. 19): 1 not defined; 2 = IV; 3 = III; 4–8 = II; 9 = I.
4. **Working proprietors are managers in NCO.** NCO puts "Working Proprietor" job titles in family **1120 Managing Directors and Chief Executives**, for example 1120.2000 *Working Proprietor, Retail Trade*. This probably explains why India's ISCO-08 sub-major group 11 is large and unstable: **14.9 million in 2022, 6.4 million in 2025** (ILOSTAT `EMP_TEMP_SEX_OC2_NB`). The ISCO-88 major group 1 was 28.6 million in 2018. Avoid using managers' growth as an "outlook".
5. **NCO-2004 to NCO-2015.** NCO-2004 was based on ISCO-88: 10 divisions (incl. X "workers not classified"), 30 sub-divisions, 116 groups, 439 families and 2,945 occupations (Vol I p. 13). NCO-2015 dropped Division X (Vol I p. 20).
6. **Source inconsistencies, kept and flagged in the `note` column:**
   - Vol II prints 3127.9900, but Vol I has 3123.9900; the record is kept as 3123.9900.
   - The Group 343 heading is missing from Vol II. Vol I (PDF p. 124) titles it "Administrative Associate Professionals", whereas ISCO-08 343 is artistic, cultural and culinary associate professionals.
   - 8190.0100 "Saw Grinder, Machine" appears only in Vol I, under a family 8190 that does not exist.

### 1.4 Parsing method
- `parse_nco_vol2.py` reads PyMuPDF spans with fonts and positions. Bold 14pt marks headings; the white side tab gives the Division number. Output: 9 / 40 / 126 / 436 / 3,450 records.
- `parse_nco_vol1.py` reads the concordance table, which supplies NCO-2004 equivalents.
- `build_nco_structure.py` merges the two (Vol I fills Group 343 and some titles) and compares codes with ISCO-08.
- `parse_dge_web.py` checks the result against the DGE web listing. Of 3,435 web codes, all but 2 malformed family rows are in the PDF set.

---

## 2. ILOSTAT data for India

### 2.1 Access
- All India annual data in one file (134 MB, 1,177,382 records, 692 indicators): `https://rplumber.ilo.org/data/ref_area/?id=IND_A&format=.csv`. Saved as `data/raw/nco/ilostat/IND_A_all.csv`.
- One indicator: `https://rplumber.ilo.org/data/indicator/?id=<INDICATOR>_A&ref_area=IND&format=.csv` (use `_Q` for quarterly, e.g. `EMP_TEMP_SEX_OCU_NB_Q`).
- Dictionaries: `https://rplumber.ilo.org/metadata/dic/?var=<source|classif1|classif2|indicator|note_source|...>&lang=en&format=.csv`
- Table of contents: `https://rplumber.ilo.org/metadata/toc/indicator/?lang=en&format=.csv`
- Requesting an indicator that does not exist returns `{"error":"deprecated or invalid dataset id"}`. Example: `EMP_TEMP_SEX_OC2_NB_Q`, because there is no quarterly 2-digit series.

### 2.2 Sources and reference periods
| ILOSTAT source code | Survey | Years in ILOSTAT | Reference period |
|---|---|---|---|
| `BA:14121` | PLFS (Periodic Labour Force Survey), ILO processing of the microdata | 2018–2025 annual; 2017Q3–2025Q4 quarterly | **Calendar year.** The annual value equals the mean of the 4 quarterly values; I checked this for 2022–2025 (2022: 444,845.8 thousand = mean of 2022Q1–Q4). Uses a current-weekly-status (7-day) concept, ages 15+, ILO 13th ICLS definitions. Each calendar year mixes two July–June PLFS rounds up to 2024. For 2025 the PLFS itself runs on calendar years. |
| `BX:2228` | NSS Employment-Unemployment Surveys | 1994, 2000, 2005, 2010, 2012 | NSS rounds 50, 55, 61, 66 and 68 (July–June years ending in the year shown) |
| `XA:1976` | ILO modelled estimates (Nov. 2025) | 1991–2025; total employment projected to 2027 | Harmonised model output, not survey data |

**Caveat on levels.** The microdata series gives a 15+ population of 903.1 million and employment of 476.6 million in 2025 (employment-to-population ratio 52.8%; `POP_XWAP_SEX_AGE_NB`, `EMP_TEMP_SEX_AGE_NB`, `EMP_DWAP_SEX_AGE_RT`). The ILO modelled estimate for 2025 is 591.6 million (`EMP_2EMP_SEX_AGE_NB`). The microdata levels follow PLFS weights and CWS. **Use shares and growth rates from this series, not absolute levels.** If you need a headcount, scale the shares to an external total and say which one.

**Caveat on "employees".** In ILOSTAT, employees are 25.3% of employment in 2025: 120.5 million of 476.6 million (`EMP_TEMP_SEX_STE_NB`). PLFS 2025 (usual status) reports regular wage/salaried at 23.6% and casual labour at 20.2% (PLFS Annual Report 2025 press note, p. 8, file `data/raw/plfs/press_note_AR_PLFS_2025.pdf`). The ILO harmonisation therefore cannot be counting all PLFS casual labour as employees; the exact mapping is not documented in the bulk file. ILOSTAT earnings by occupation are best read as **earnings of employees, mostly regular wage/salaried**. Earnings of the self-employed, 56% of PLFS workers, are not in ILOSTAT by occupation.

### 2.3 Indicators saved (full list with years: `data/ilostat/ilostat_ind_catalogue.csv`, 521 indicator × source rows)
Every tidy file has these columns: `indicator, indicator_label, year, sex, classif1, classif1_label, classif2, classif2_label, value, unit, obs_status, source, source_label, ref_period, source_url`.

| File | Indicators | PLFS years | NSS years |
|---|---|---|---|
| `ilostat_ind_emp_by_occupation.csv` | EMP_TEMP_SEX_OCU_NB; **EMP_TEMP_SEX_OC2_NB**; EES_TEES_SEX_OCU/OC2_NB (employees); EMP_TEMP_SEX_STE_OCU_NB (status); EMP_TEMP_SEX_OCU_GEO_NB (rural/urban); EMP_STEM_SEX_OC2/OCU_NB; EMP_CARE_SEX_OC2_NB | OCU: 2018–2025 (ISCO-88 for 2018–20, ISCO-08 for 2022–25, skill level for all). **OC2: 2018–2020 (ISCO-88) and 2022–2025 (ISCO-08); 2021 missing.** STEM: 2022–25 | OCU: 1994–2012; OC2: 2010, 2012 |
| `ilostat_ind_emp_by_occupation_quarterly.csv` | EMP_TEMP_SEX_OCU_NB (quarterly) | 2017Q3–2025Q4 | none |
| `ilostat_ind_emp_by_activity.csv` | EMP_TEMP_SEX_ECO_NB, **EMP_TEMP_SEX_EC2_NB** (ISIC4 2-digit = NIC-2008), EES_TEES_SEX_EC2/ECO_NB, EMP_TEMP_SEX_STE_EC2_NB | 2018–2025 (no break) | 1994–2012 (ISIC3/ISIC4) |
| `ilostat_ind_emp_occupation_x_activity.csv` | EMP_TEMP_ECO_OCU_NB, EMP_TEMP_SEX_OCU_EC2_NB (major group × ISIC 2-digit) | 2018–2025 | 2010, 2012 |
| `ilostat_ind_earnings.csv` | all EAR_* (mean `EMTA` and median `EMTM` monthly; mean `EHRA` and median `EHRM` hourly; Gini `EMTG/EHRG`; gender gap `GGAP`) by occupation (OCU), activity (ECO, 1-digit sections), education, age and area; SDG_0851 | 2018–2025 | 2005, 2010, 2012 (ECO); 2010, 2012 (OCU) |
| `ilostat_ind_education_by_occupation.csv` | EMP_TEMP_SEX_OCU_EDU_NB, EES_TEES_SEX_OCU_EDU_NB, EMP_TEMP_SEX_EDU_EC2_NB, EMP_TEMP_SEX_ECO_EDU_NB | 2018–2025 | 2010, 2012 |
| `ilostat_ind_informality_by_occupation.csv` | EMP_NIFL_SEX_OCU/OC2/EC2_NB and _RT, EMP_TEMP_SEX_IFL_OCU_NB, EMP_NIFL_SEX_OCU_EDU_RT | 2018–2025 (OC2 not 2021) | 2010, 2012 |
| `ilostat_ind_hours_by_occupation.csv` | HOW_TEMP / HOW_XEES by OCU, OC2, EC2 (mean weekly hours actually worked) | 2018–2025 (OC2 not 2021) | none |
| `ilostat_ind_modelled_estimates.csv` | EMP_2EMP_SEX_OCU_NB (major groups; 6 and 9 combined as "96"), EMP_2EMP_SEX_ECO_NB, EMP_2EMP_SEX_AGE_NB (to **2027**, where 2026–27 are projections), EMP_2EMP_SEX_STE_NB | modelled 1991–2027 | none |

Derived tables (`scripts/nco/ilostat_derived.py`):
- `derived_isco08_2digit_profile.csv`. For the 40 sub-major groups: employment 2022–25 (total; male and female for 2025), employees, informality rate, weekly hours, change and CAGR 2022→25, and the parent major group's mean and median monthly earnings, labelled as major-group values. The 2-digit cells sum exactly to the total in every year.
- `derived_major_group_profile.csv`. Major group and skill level × 2018–2025: employment, employees, mean and median earnings, informality, hours, and education shares.
- `derived_isic4_2digit_growth.csv`. 87 ISIC divisions, 2018–2025, change and CAGR.
- `derived_skill_level_growth.csv`.

### 2.4 Key figures, 2025 (ILOSTAT, PLFS microdata, calendar year 2025; employment in millions; earnings in INR per month, employees only)
| ISCO-08 major group | Employment | Employees | Mean earnings | Median earnings | % below primary (ISCED X+0) | % primary (1) | % lower secondary (2) | % upper secondary + post-secondary (3+4) | % tertiary (5+6) | Informal % |
|---|---|---|---|---|---|---|---|---|---|---|
| 1. Managers | 13.4 | 5.4 | 50,473 | 40,000 | 2.5 | 2.9 | 17.1 | 19.9 | 57.6 | 57.1 |
| 2. Professionals | 27.9 | 21.3 | 38,298 | 32,000 | 0.8 | 1.0 | 5.5 | 12.9 | 79.8 | 43.9 |
| 3. Technicians and associate professionals | 12.6 | 9.3 | 26,152 | 20,000 | 1.1 | 2.0 | 19.7 | 29.2 | 48.0 | 53.4 |
| 4. Clerical support workers | 11.1 | 10.1 | 24,252 | 19,500 | 0.3 | 0.8 | 17.9 | 23.3 | 57.5 | 40.4 |
| 5. Service and sales workers | 63.1 | 23.8 | 15,575 | 12,000 | 15.4 | 12.4 | 37.6 | 17.9 | 16.7 | 89.6 |
| 6. Skilled agricultural, forestry and fishery | 161.9 | 1.2 | 13,145 | 10,000 | 39.9 | 14.8 | 30.1 | 9.1 | 6.1 | 99.5 |
| 7. Craft and related trades | 54.7 | 12.8 | 16,825 | 15,000 | 17.9 | 16.6 | 43.4 | 15.3 | 6.7 | 91.7 |
| 8. Plant and machine operators, assemblers | 28.9 | 13.6 | 17,329 | 15,000 | 13.1 | 15.5 | 48.6 | 16.1 | 6.7 | 85.2 |
| 9. Elementary occupations | 103.0 | 23.1 | 11,530 | 10,000 | 40.1 | 18.6 | 32.4 | 6.6 | 2.4 | 89.4 |
| **Total** | **476.6** | **120.5** | **22,220** | **15,000** | 27.3 | 13.7 | 31.9 | 12.3 | 14.8 | 87.2 |

Indicators: EMP_TEMP_SEX_OCU_NB, EES_TEES_SEX_OCU_NB, EAR_EMTA_SEX_OCU_NB, EAR_EMTM_SEX_OCU_NB, EMP_TEMP_SEX_OCU_EDU_NB, EMP_NIFL_SEX_OCU_RT. URL pattern as in §2.1; source BA:14121, year 2025.

Comparison with 2018 (ISCO-88, same indicators). Total mean earnings were 15,679 and median 10,000. Managers (ISCO-88 group 1): 28.6 million, mean 32,460. Elementary: 80.5 million, mean 7,900. Earnings are nominal.

### 2.5 Education categories
ILOSTAT reports PLFS general education as ISCED-97 (`EDU_ISCED97_*`) and as aggregates. In 2025 the aggregates equal these sums exactly:
- Less than basic = X + 0
- Basic = 1 + 2
- Intermediate = 3 + 4
- Advanced = 5 + 6

My reading of the India mapping is an inference: the bulk file does not document it. The numbers fit this reading, with level 2 at 31.9% of workers:
- X = no schooling; 0 = below primary
- 1 = primary
- 2 = middle plus secondary (classes 6–10)
- 3 = higher secondary
- 4 = diploma or certificate below graduate
- 5 = graduate
- 6 = postgraduate and above

So "graduate+" is ISCED 5+6, "higher secondary" is ISCED 3 (+4), "secondary" is ISCED 2 (which includes middle school), and "below primary" is X+0. Education by occupation exists **only at major-group level**: there is no OC2 × EDU series.

---

## 3. Growth ("outlook" analogue)

### 3.1 Occupations
- **Consistent window, ISCO-08 2-digit, 2022→2025** (`derived_isco08_2digit_profile.csv`). Total CAGR is +2.3%.
  - Fastest-growing cells: 94 Food preparation assistants +29.3%/yr (from 0.36 million); 63 Subsistence farmers +21.6% (9.5 to 17.1 million); 96 Refuse and other elementary +15.3%; 42 Customer services clerks +14.7%; 32 Health associate professionals +13.5%.
  - Declining cells: 11 Chief executives/legislators −24.6% and 12 Administrative and commercial managers −18.5% (both affected by the proprietor coding in §1.3 item 4); 62 Forestry and fishery −4.5%; 93 Labourers in mining, construction, manufacturing and transport −1.4%.
  - Flat: 25 ICT professionals +0.5% (3.53 to 3.59 million).
  - Three annual changes are short and noisy for small cells. The file also holds a 2023–25 average.
- **2018→2025 by occupation is not consistent.** It crosses ISCO-88 to ISCO-08 (NCO-2004 to NCO-2015). Even the ILO skill-level series breaks: levels 3–4 were 67.3 million in 2021 and 57.7 million in 2022 (`derived_skill_level_growth.csv`), because managers were re-coded. The ILO modelled major-group series (`EMP_2EMP_SEX_OCU_NB`) shows the same drop for group 1 (40.0 million in 2018, 21.2 million in 2025), so it does not fix the break.
- No official ISCO-88↔ISCO-08 2-digit bridge for India was found. The ILO correspondence table could not be downloaded (HTTP 403).

### 3.2 Industries (ISIC Rev.4 = NIC-2008, no break, 2018→2025; `derived_isic4_2digit_growth.csv`)
- Total employment 347.4 million to 476.6 million (+37.2%, CAGR 4.6%; ILOSTAT microdata, so see the level caveat).
- Large divisions growing fastest (CAGR 2018–25):
  - J62 Computer programming +13.0% (1.99 to 4.68 million)
  - C23 Non-metallic minerals +8.9%
  - Q86 Human health +8.5%
  - C24 Basic metals +8.1%
  - G46 Wholesale +7.4%
  - I56 Food and beverage service +7.3%
  - F43 Specialised construction +7.1%
- Slowest: F42 Civil engineering −0.8%; C16 Wood products −0.1%; C13 Textiles +0.9%; O84 Public administration +1.8%.
- A01 Crop and animal production: 141.5 to 194.5 million (+4.7%/yr; 2022→25 CAGR only +1.2%).

### 3.3 RBI KLEMS (not obtained)
- The RBI KLEMS page (https://www.rbi.org.in/Scripts/KLEMS.aspx, fetched 2026-11-09, saved in `data/raw/nco/klems/`) lists the **July 2024** release as the latest: 27 industries, 1980-81 to 2022-23, plus a provisional total-economy estimate for 2023-24 (RBI press release 2024-2025/649, 08 Jul 2024).
- Data file: https://rbidocs.rbi.org.in/rdocs/content/docs/INDIAKLEMS08072024.xlsx. The server answers scripted requests with a JavaScript bot challenge instead of the file. I did not try to get around it, and **no KLEMS numbers are included here**. Download it manually in a browser.
- Search snippets quote 47.49 crore (2017-18) and 64.33 crore (2023-24, provisional), citing Lok Sabha USQ 3706 of 24 Mar 2025. The PDF URL (dge.gov.in/…/3706_e.pdf) now returns 404, so these figures are **not verified**.

### 3.4 Projections (labelled; `data/nco/india_employment_projections.csv`)
- **ILO modelled estimates (Nov 2025)**, total employment 15+: 2025 591.6 million (estimate); 2026 600.1 million and 2027 608.7 million (projections). No projections by occupation or sector.
- **WEF Future of Jobs Report 2025**, India economy profile, p. 148 (https://reports.weforum.org/docs/WEF_Future_of_Jobs_Report_2025.pdf). This is an employer survey. Expected net role growth 2025–2030, India (global in brackets):
  - AI and ML specialists +176% (+82%)
  - Data analysts and scientists +54% (+41%)
  - BI analysts +17% (+18%)
  - Business development professionals +14% (+19%)
  - Assembly and factory workers +2% (0%)
  - Administrative assistants and executive secretaries −20% (−20%)

  Values were read from the PDF text layer of a chart.
- **Not obtained** (the search budget ran out): NSDC sector skill-gap studies (2013-14 vintage, projections to 2022, now dated) and NITI Aayog gig-economy projections. I did not verify them, so no numbers are given.

---

## 4. Finer-than-2-digit occupation counts
2-digit (ISCO-08) employment is available, so item 5 of the brief (fallback sources) was not needed. Nothing in ILOSTAT goes below 2 digits for India. 3- or 4-digit NCO counts would need PLFS unit-level data (login required, out of scope) or published academic tabulations. I did not search for these: the search budget was used up and they were lower priority.

---

## 5. Suggested use in the treemap
- **Cells:** the 40 ISCO-08 sub-major groups, which are the same as the NCO-2015 sub-divisions. Area = 2025 employment share, or the 2023–25 average to reduce noise.
- **Merge sub-majors 11 and 12 (or all of major group 1)** because of the proprietor coding.
- **Colour, growth:** 2-digit CAGR 2022→25. Industry CAGR 2018→25 is an optional tooltip.
- **Colour, pay:** only major-group (1-digit) employee earnings exist. Label them as such, or derive cell pay outside ILOSTAT, for example from the PLFS report tables in the other lane.
- **Colour, education:** major-group tertiary share (ISCED 5+6), applied to the cells within each group.
- **AI exposure:** score each NCO-2015 sub-division from its families and occupations (`description` column). If needed, weight by NCO occupation counts; there are no employment weights below 2 digits.

## 6. Gaps
1. No earnings below major-group level, and none for the self-employed.
2. No 2-digit data for 2021; 2018–2025 occupation growth crosses a classification break.
3. Absolute levels from ILOSTAT microdata understate employment compared with ILO modelled totals.
4. RBI KLEMS file was not downloadable by script.
5. ILO ISCO-08 English 3- and 4-digit titles and the ISCO-88↔08 correspondence were not downloadable (HTTP 403). NCO's own English titles stand in.
6. NCO-2025 was not found; NCO-2015 is current as far as this search could tell.
7. The web search budget ran out before NSDC, NITI Aayog and academic 3-digit tables could be checked.

## 7. Files
- `research/nco_framework.md` (this file)
- `data/nco/`:
  - nco2015_structure.csv
  - nco2015_vs_isco08_code_differences.csv
  - nco2015_occupations_mapped_to_other_isco08_unit.csv
  - nco2015_dge_web_listing.csv
  - india_employment_projections.csv
- `data/ilostat/`:
  - ilostat_ind_*.csv (9 tidy files plus the catalogue)
  - derived_*.csv (4 files)
- `data/raw/nco/`:
  - NCO Vol I, II-A and II-B PDFs
  - insee_nomenclature_*_ISCO.xlsx
  - ilostat/ (IND_A_all.csv, quarterly OCU file, dictionaries, tables of contents)
  - dge_web/ (HTML)
  - klems/ (RBI pages only)
  - projections/WEF_Future_of_Jobs_Report_2025.pdf
- `scripts/nco/`:
  - ilo_inventory.py
  - ilostat_extract.py
  - ilostat_derived.py
  - pdf_dump.py
  - parse_nco_vol1.py
  - parse_nco_vol2.py
  - build_nco_structure.py
  - parse_dge_web.py
  - build_projections.py
