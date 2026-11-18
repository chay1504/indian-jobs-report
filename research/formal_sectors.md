# Formal / white-collar sectors: headcount and pay (India)

Lane: headcount and pay for India's formal white-collar occupations, the likely high-AI-exposure "red" tiles. Compiled 2026-11-09.
Machine-readable table: `data/formal_sectors/sector_headcount_pay.csv` (46 rows), built by `scripts/formal_sectors/build_sector_csv.py`. The script holds every input and does all the arithmetic, so each derived number can be checked.
Raw sources: `data/raw/formal_sectors/` (subfolders `it_companies/` and `health_edu_prof/`).

**How to read this**
- Pay figures measure different things: a statutory median, cost per employee, entry basic pay, or an honorarium. The `pay_measure` column says which. Don't compare them as like-for-like medians.
- Several rows overlap: TOTAL rows, company rows that sit inside the NASSCOM total, and bank category splits. The `notes` column flags each one. For the treemap, use non-overlapping leaves only.
- Professional registers (doctors, nurses, CAs, advocates) count stock, not employment. The government assumes about 80% of registered doctors are active.
- Search budget: web search ran out mid-task, because it is shared across agents. After that I used only direct fetches of known official URLs plus the RBI DBIE portal, so some items below remain gaps.

---

## 1. IT-BPM

| Item | Headcount | Period | Source |
|---|---|---|---|
| Tech industry total, incl. GCCs | **~5.95 mn** (≈+1.35 lakh net adds, +2.3%) | FY2025-26E | NASSCOM SR2026 press release p1 (+2.3%); exec summary p4 ("nearly 6 mn"). The 5.95 mn figure is NASSCOM's as reported by Business Today, 24-Feb-2026 |
| Same, earlier years | 5.67 mn (restated) / 5.8 mn | FY2024 / FY2025E | NASSCOM SR2025 press release p1 (note on GCC restatement) |
| GCCs (subset) | **>1.9 mn**; >1,700 GCCs | FY2024 | nasscom.in GCC landscape (5-year journey) page |
| Customer-service (CX) workforce | **2.0–2.5 mn** | 2023 | NITI Aayog *Roadmap for Job Creation in the AI Economy* (Oct 2025) pp.11, 21. Same report: tech workforce 7.5–8 mn including tech jobs in other sectors |

- **Segment split:** NASSCOM's public releases give revenue by segment but not headcount. FY26E revenue: IT services $149bn, ER&D $63bn, BPM $59bn, software products $23bn, hardware $21bn. Headcount by segment is a **gap** (it sits behind the member paywall).
- **Growth:** FY24→FY26 is +4.9% over two years. NASSCOM has published no restated five-year series.

### Top IT employers (official annual reports)
Columns: year-end headcount; consolidated employee benefit expense ÷ average headcount (global, so it includes onsite staff paid in USD); MRE = statutory *median remuneration of employees* (Companies Act s.197 / Rule 5, standalone entity).

| Company | FY23 | FY24 | FY25 | FY26 | FY22→26 | Cost/head FY26 | MRE FY26 |
|---|---|---|---|---|---|---|---|
| TCS | 614,795 | 601,546 | 607,979 | **584,519** | −1.3% | ₹26.0 L | ~₹8.45 L (derived¹) |
| Infosys | 343,234 | 317,240 | 323,578 | **328,594** | +4.6% | ₹29.2 L | **₹11.13 L** (FY25 ₹10.72 L) |
| Wipro | 248,813² | 234,054 | 233,346 | **242,156** | +2.5% | ₹23.4 L | **₹9.47 L** (−3.2%) |
| HCLTech | 225,944 | 227,481 | 223,420 | **227,181** | +8.8% | ₹32.9 L | n.d. (global, PPP basis) |
| Tech Mahindra | 152,400 | 145,455 | 148,731 | **147,623** | −2.3% | ₹20.6 L | **₹5.9 L** (−4.9%) |
| LTIMindtree | 84,546 | 81,650 | 84,307 | **87,950** | n/a³ | ₹30.5 L | **₹17.21 L** |
| Cognizant (India only) | 254,000 (CY23) | 241,500 | 256,900 (CY25) | — | −0.6% (CY22→25) | n.d. | n.d. |

¹ TCS doesn't print an absolute MRE. ~₹8.45 L = CEO pay ÷ CEO:MRE ratio (332.8, AR26 p167). TCS's own BRSR gives medians of ₹18.3 L (men) and ₹11.9 L (women) for employees other than directors and KMP, which doesn't reconcile, so confidence is low.
² Wipro FY22–23 counts "permanent employees on the rolls of the Company", which may be narrower than the group.
³ FY22 is pre-merger.

- **FY26 drop:** the top five firms' combined headcount fell by about 7,400. That is the first net decline in two decades (IANS, 25-Apr-2026, secondary). NASSCOM still has the industry adding about 1.35 lakh.
- **India share:** Infosys 78.7% (20-F FY26); Wipro 78.5% (BRSR); LTIMindtree 88.5%; Cognizant 73.1%.
- **Fresher pay (secondary only):** mass-hiring tracks pay about ₹3.4–4.5 lakh (TCS Ninja ~₹3.36 L, Wipro Elite ~₹3.5 L, Cognizant GenC ~₹4 L, HCLTech regular ~₹4.5 L). Premium tracks pay ₹7–21 L; the Infosys CHRO said "up to ₹21 lakh" for Specialist Programmer in Dec 2025. Mass-hiring entry pay has been roughly flat for years.
- **Where the files are:** every annual report is in `data/raw/formal_sectors/it_companies/`. A sub-agent extracted these figures. I re-verified TCS FY26 headcount (584,519), TCS employee benefit expense (₹1,54,994 cr) and Infosys MRE (₹11,13,024, AR p.58) against the PDFs.
- **Confidence:** high for headcount and expense; MRE high except TCS (low) and HCLTech (n.d.).

## 2. Banking: RBI *Statistical Tables Relating to Banks in India 2024-25*
Source: Table 12 "Bank-wise and Category-wise Employees of SCBs" (as at 31-Mar-2025) and Table 2 "Earnings and Expenses", both on RBI DBIE (released 29-Dec-2025). Extracts are in `rbi_strbi_table12_employees_SCB.txt` (full series 2014-15 to 2024-25) and `rbi_strbi_table2_earnings_expenses_extract.txt`.

| Group | Officers | Clerks | Sub-staff | **Total 2025** | Total 2020 | 5-yr | Employee cost / head |
|---|---|---|---|---|---|---|---|
| Public sector banks | 4,23,650 | 2,47,776 | 86,215 | **7,57,641** | 7,90,659 | −4.2% | ₹23.5 L |
| Private sector banks | 7,93,326 | 36,637 | 8,187 | **8,38,150** | 5,54,418 | **+51.2%** | ₹11.8 L |
| Foreign banks | 26,056 | 1,251 | 734 | 28,041 | 23,581 | +18.9% | ₹40.0 L |
| Small finance banks | 1,25,260 | 24,798 | 27,739 | 1,77,797 | 95,249 | +86.7% | n.c. |
| Payments banks | 6,920 | – | 38 | 6,958 | 2,048 | – | n.c. |
| **All SCBs** | **13,75,212** | **3,10,462** | **1,22,913** | **18,08,587** | 14,65,955 | +23.4% | ₹16.5 L |

- **What "cost per head" means:** "payments to and provisions for employees" ÷ employees. It includes pension and gratuity provisions, which is a large part of the PSB figure. It is not a median salary.
- **Category trends, 2020→2025, all SCBs:** officers +37%, clerks −2.5%, sub-staff −14%. PSB clerks fell 12%. The private-bank boom is almost entirely in the "officer" category.
- **Exclusions:** Regional Rural Banks, cooperative banks, and outsourced or contract sales staff are not in this table.
- **Gaps:** IBA 12th Bipartite pay scales (entry pay for clerks and officers) could not be fetched once search was exhausted. Bank-level counts are in the raw file (SBI 2,36,226; HDFC Bank 2,14,521).

## 3. Insurance, NBFC, brokers
- **Life insurance agents:** 31.23 lakh individual agents (LIC 14.87 L, private 16.37 L), up 7.87% year on year. Source: IRDAI Annual Report 2024-25, para II.2.1.1, PDF p.295.
- **General and health agents:** 7,73,107 with general insurers; 15.49 lakh with standalone health insurers.
- **Caveat on agents:** they are commission-earning licensees and many are part-time. Don't use them as FTE white-collar jobs.
- **Insurer employees:** the IRDAI report has no table for them. LIC and private-insurer annual reports would be needed. **Gap.**
- **NBFC / fintech / stock-broker employment:** no official count found. SEBI registers firms, not staff. **Gap**; use PLFS for NIC 64–66.

## 4. Government
**Central government civilian establishment.** Source: Union Budget 2026-27 *Expenditure Profile*, Statement 22 "Estimated strength of establishment" (`union_budget_2026-27_eb_stat22_establishment.xlsx`). Strength is the actual on 1-Mar-2025. Pay = 2024-25 actual pay plus allowances (DA, HRA and others; travel excluded) ÷ strength. The 2020 base comes from the Budget 2022-23 Statement 22.

| Unit | 1-Mar-2025 | 1-Mar-2020 | 5-yr | Pay+allowances / head (2024-25) |
|---|---|---|---|---|
| **All central civilian** | **33,02,539** | 31,80,400 | +3.8% | **₹9.89 L** |
| Railways | 12,12,958 | 12,52,347 | −3.1% | ₹10.25 L |
| Central police (MHA "Police": CAPFs, Delhi Police, IB…) | 11,01,452 | 10,03,573 | +9.8% | ₹10.43 L |
| Dept of Posts | 4,74,386 | 4,03,817 | +17.5% | ₹4.66 L (probably includes Gramin Dak Sevaks; unverified) |
| Everything else (tax depts 1.08 L, audit 40,652, defence civilians 71,371…) | 5,13,743 | 5,20,663 | −1.3% | ₹12.7 L |

- **Estimates ahead:** 35.78 lakh for 1-Mar-2026 and 36.20 lakh for 1-Mar-2027 (many vacancies are budgeted).
- **Pay matrix (basic pay/month at entry of level, excluding DA and HRA):** L6 ₹35,400, L7 ₹44,900, L8 ₹47,600, L10 ₹56,100 (Group A entry), verified in KVS OM 22-Jan-2026. L1 (MTS) ₹18,000 is the 7th CPC minimum, which I didn't re-download.
- **Typical gross pay:** a clerk/assistant at L4–L7 or an officer at L10 earns roughly basic × (1 + DA + HRA). The budget per-head figures above already include DA.
- **DA rate and 8th CPC status:** not verified this session because search was exhausted. My unverified understanding is that the 8th CPC was constituted in 2025 and has not reported, so 7th CPC scales still apply. Confirm with the tax/policy lane before publishing.
- **Not covered by this statement:**
  - **Armed forces personnel:** not in Statement 22. **Gap.**
  - **State government employees:** RBI *State Finances* reports salary spending, not headcount. **Gap.** PLFS public administration (NIC 84) is the practical source.
  - **State police (BPR&D *Data on Police Organisations*):** bprd.nic.in was unreachable. **Gap.**
  - **CPSEs (DPE *Public Enterprises Survey 2024-25*):** the release dated 17-Dec-2025 exists on dpe.gov.in, but its PDF attachments aren't exposed outside the JavaScript front end. **Gap.**

## 5. Education
- **School teachers, UDISE+ 2024-25** (booklet Tables 4.2–4.6, pp.53–57): total **1,01,22,420**. Government 51,49,771 (50.9%); government-aided 7,57,624 (7.5%); private unaided 39,62,114 (39.1%); others 2,52,911 (2.5%).
- **Latest total and trend:** 2025-26 total is 1,02,73,020 (PIB 7-Jul-2026). 2020-21 was 96.96 lakh, so about +5.9% over five years, but there is a series break in 2022-23.
- **Higher-education teachers:** **17.32 lakh** (AISHE 2023-24, released 8-Jul-2026; partial response). 2019-20 was 15.03 lakh, so +15.2% over four years.
- **Pay, entry basic/month:**
  - KVS PRT L6 ₹35,400 / TGT L7 ₹44,900 / PGT L8 ₹47,600 (KVS OM).
  - UGC Assistant Professor Academic Level 10, ₹57,700 (MHRD letter 2-Nov-2017, via a secondary copy).
  - State scales differ.
  - Private-school and private-college pay has no official published figure. It needs PLFS unit-level data (PLFS lane).
- **Coaching / edtech employment:** no credible estimate (only an industry claim of 75,000 edtech jobs). **Gap.**

## 6. Health
| Item | Count | Period | Pay (what it is) | Source |
|---|---|---|---|---|
| Allopathic doctors (Indian Medical Register) | **15,35,155** registered (~12.3 L active at the government's 80% assumption) | Jul-2026 | Central govt entry L10 ₹56,100 basic/month plus 20% NPA (NPA from a secondary source); no private-pay series | PIB PRID 2288843 (Lok Sabha) |
| AYUSH practitioners | 7,51,768 | Jul-2026 | – | same |
| Nurses & midwives (INC) | **46,02,133** (RN&RM 34,87,731; ANM 10,59,246; LHV 55,156) | 31-Dec-2025 | none official | Lok Sabha USQ 1138, 24-Jul-2026, Annexure I |
| Pharmacists | ~16 lakh | Feb-2023 | – | PTI report of Lok Sabha reply (low confidence) |
| Dentists | ~3.19 lakh | Feb-2024 | – | secondary (low) |
| ASHA workers | **10.33 lakh** | 2026 | ₹2,000/month central fixed incentive (+ task incentives + state top-ups); a rise to ₹3,500 approved Mar-2025 (implementation date unverified) | PIB 2296281, 2079023 |
| Anganwadi workers / helpers | **13,48,135 / 10,23,068** in position | 31-Dec-2023 | Central honorarium ₹4,500 / ₹2,250 per month (+₹500 / ₹250 incentive; states top up) | PIB 2003433, 2226338 |

- **Doctor series break:** the NMC series went from 13.08 L (Jun-2022) to 13.88 L (Mar-2026). The jump to 15.35 L comes from switching to the IMR, not real growth.
- **Nurse growth:** +37.7% since 2022 (33.41 L).

## 7. Professions
| Body | Members | Period | Notes / pay | Confidence |
|---|---|---|---|---|
| ICAI (CAs) | **4,52,825** | 1-Apr-2026 | 3,27,081 in 2021, so +38.4% over five years. Campus placement average for newly qualified CAs is about ₹12–13 L p.a. (ICAI statements, via secondary sources); top offers ₹26.6–29 L | high / medium (pay) |
| ICSI (company secretaries) | ~78,000 | Jan-2026 | PTI wire | medium |
| ICMAI (cost accountants) | ~1,00,000 | 2024-25 | rounded self-description | low |
| Advocates | ~20 lakh enrolled | 2025 | secondary; enrolment ≠ practice | low |
| Architects (CoA) | ~1.05 lakh registered (~85k valid) | ~2024 | secondary interview | low |

- **Not found:** engineers (no registry), journalists and media, advertising and creative, telecom, e-commerce. No official headcount or credible estimate turned up for any of these, so they are **gaps**. PLFS by NCO/NIC (other lanes) is the right source.

## 8. Platform / gig
- **NITI Aayog estimate (Jun-2022 report, Exec Summary, PDF pp.19–20):** **77 lakh** gig workers in 2020-21 (68 lakh in 2019-20), equal to 2.6% of the non-farm workforce. Projected to reach **2.35 crore by 2029-30**.
- **By sector:** retail and sales ~26.6 L, transport ~13 L, finance and insurance 6.3 L, manufacturing 6.2 L.
- **By skill:** 47% medium-skill, 22% high-skill, 31% low-skill.
- **Overlap and earnings:** this is a model estimate that overlaps retail and transport, and the informal_sectors lane already lists it, so don't double count. There is no official earnings series for delivery or ride-hailing work.

## 9. Retail, security, clerks, call centres
- **Call-centre / CX agents:** 2.0–2.5 mn (NITI 2025; see section 1).
- **Private security guards:** covered in `data/informal_sectors/sector_headcount_pay.csv`. There is no official count; the industry claims 7–10 mn, and e-Shram has 4.7 lakh registrations. Left out here to avoid double counting.
- **Retail sales staff, office clerks, data-entry operators:** no official stand-alone counts. Use PLFS NCO codes (NCO 41xx–44xx clerks, 52xx sales). **Gap** in this lane.

---

## Observations for the "2% taxpayer" question (descriptive only)
- **Median pay in Indian IT is lower than its reputation.** At the large IT firms, statutory median pay runs from ₹5.9 L (TechM) through ₹9.5 L (Wipro) and ₹11.1 L (Infosys) to ₹17.2 L (LTIMindtree). Mass-hiring freshers start at about ₹3.5–4.5 L. A large share of the ~6 mn IT-BPM workforce therefore sits in the middle of the formal-pay distribution, not at the top. Compare against the tax lane's thresholds.
- **Banks:** the 18.1 lakh SCB employees cost ₹16.5 L per head including provisions. Private banks, at ₹11.8 L per head, drove all the headcount growth.
- **Central government:** 33 lakh civilian employees cost ₹9.9 L per head, all-in.
- **Combined, these core formal white-collar pools** (IT-BPM ~6 mn, SCBs 1.8 mn, central civilian 3.3 mn, school and college teachers ~11.9 mn, of whom about 6 mn are on government or aided payrolls) are each a small slice of a ~600 mn workforce. That is consistent with the formal salaried taxpayer base being narrow.

## Gaps (priority order)
1. **Headcount and pay with no source found:** CPSE employment and pay (DPE PE Survey 2024-25 PDFs unreachable); state government employees; state police; armed forces.
2. **Bank pay scales:** IBA 12th Bipartite entry pay; insurer employee counts (LIC and others); NBFC, fintech and broker staff.
3. **Pay not found:**
   - NASSCOM segment-wise headcount (IT services / BPM / ER&D / products) and any pay data.
   - Private-sector pay for teachers, nurses and doctors, which needs PLFS microdata.
   - Gig earnings.
4. **No count found:** retail, clerical, journalism, telecom and e-commerce. Use PLFS (other lanes).
5. **Not verified this session:** 8th CPC status, current DA rate, and TCS and HCLTech absolute MRE.

## Files
- `data/formal_sectors/sector_headcount_pay.csv`: 46 rows with columns sector, sub_sector, headcount, headcount_year, pay_annual_inr, pay_measure, pay_year, education_typical, growth_5yr_pct, source_url, notes, confidence. The `growth_5yr_pct` column holds the nearest available multi-year change, and `notes` gives the exact period.
- `scripts/formal_sectors/build_sector_csv.py` builds the CSV; `scripts/formal_sectors/pdftext.py` extracts PDF text.
- `data/raw/formal_sectors/`:
  - NASSCOM SR2025 and SR2026 press releases; GCC page HTML
  - RBI STRBI Table 12 and Table 2 extracts
  - Union Budget Statement 22 for 2021-22, 2022-23 and 2026-27
  - IRDAI AR 2024-25
  - NITI gig report (PDF and text)
  - `it_companies/`: annual reports FY23–FY26 for 6 firms; Cognizant 10-Ks; Infosys and Wipro 20-Fs
  - `health_edu_prof/`: UDISE+ booklet; Lok Sabha nurses annexure; ICAI and ICMAI annual reports; KVS OM; PIB releases
