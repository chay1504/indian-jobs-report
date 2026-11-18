"""Build data/formal_sectors/sector_headcount_pay.csv from figures collected in research/formal_sectors.md.

All inputs are hard-coded from the cited primary/secondary sources (see source_url + notes per row).
Derived values (per-head pay, growth %) are computed here so the arithmetic is auditable.
Run: .venv/Scripts/python.exe -I scripts/formal_sectors/build_sector_csv.py
"""
import csv
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "formal_sectors", "sector_headcount_pay.csv")

CR = 1e7  # 1 crore rupees


def g(new, old):
    return round((new / old - 1) * 100, 1)


def per_head(crore, n):
    return round(crore * CR / n)


rows = []


def add(sector, sub, hc, hc_year, pay, pay_measure, pay_year, edu, growth, url, notes, conf):
    rows.append(dict(sector=sector, sub_sector=sub, headcount=hc, headcount_year=hc_year,
                     pay_annual_inr=pay, pay_measure=pay_measure, pay_year=pay_year,
                     education_typical=edu, growth_5yr_pct=growth, source_url=url, notes=notes,
                     confidence=conf))


# ---------------- IT-BPM ----------------
NASSCOM_PR26 = "https://d3r3sr3o54kk15.cloudfront.net/s3fs-public/media_pdf/India%E2%80%99s%20tech%20industry%20continues%20to%20redefine%20AI-led%20transformation%2C%20efficiency%20and%20skilling--%20Nasscom%20Annual%20Strategic%20Review%202026.pdf"
NASSCOM_PR25 = "https://nasscom.in/sites/default/files/media_pdf/Nasscom%20SR%20Press%20release.pdf"
NASSCOM_ES26 = "https://nasscom.in/modules/custom/nasscom_general/docs/Nasscom-Strategic%20Review-2026-Executive%20Summary.pdf"
add("IT-BPM", "Tech industry total (IT services + BPM + ER&D + software products + hardware; incl. GCCs)",
    5950000, "FY2025-26 (E)", "", "", "",
    "BE/BTech/MCA/BSc for IT; graduate (any) for BPM", "",
    f"{NASSCOM_PR26}; {NASSCOM_PR25}; {NASSCOM_ES26}",
    "NASSCOM SR2026 press release p1: net employee growth ~2.3% in FY26; exec summary p4: 'employment expanding to nearly 6 mn'. "
    "5.95 mn / +1.35 lakh net adds is NASSCOM's figure as reported by Business Today 24-Feb-2026 (not in the release text). "
    "SR2025 release: FY2024 restated 5.67 mn (after GCC restatement), FY2025E 5.8 mn (+126k; later revised to ~5.82 mn/+133k). "
    f"FY24->FY26 growth = {g(5.95, 5.67)}% over 2 yrs; no restated 5-yr series published. Segment headcount split (IT services/BPM/ER&D/products) is NOT published in the public release; revenue split FY26E: IT services $149bn, ER&D $63bn, BPM $59bn, products $23bn, hardware $21bn. Pay: no NASSCOM pay figure; see company rows.",
    "medium")
add("IT-BPM", "Global Capability Centres (GCCs) - subset of tech total",
    1900000, "FY2023-24", "", "", "", "BE/BTech/MBA/CA", "",
    "https://nasscom.in/knowledge-center/publications/india-gcc-landscape-report-5-year-journey",
    "NASSCOM-Zinnov GCC landscape page: 'As of FY2024, Indian GCCs ... employ over 1.9 million people'; >1,700 GCCs, $64.6bn revenue; headcount expected to cross 2.5 mn by 2030. "
    "Included inside the NASSCOM industry total (SR2025 note on GCC restatement) - do not add. A FY2026 figure of ~2.36 mn circulates only via secondary aggregators (unverified).",
    "medium")
add("IT-BPM", "Customer service / contact centre (CX) workforce",
    2250000, "2023", "", "", "", "Class 12 / graduate", "",
    "https://niti.gov.in/sites/default/files/2025-10/Roadmap_for_Job_Creation_in_the_AI_Economy.pdf",
    "NITI Aayog (with NASSCOM, BCG) Roadmap for Job Creation in the AI Economy, Oct 2025, p.11 and p.21: 'CX jobs headcount was 2 to 2.5 million in 2023' (value here = midpoint). "
    "Scenarios: 1.8 mn (headwinds) to 3.1 mn (tailwinds) by ~2030. Same report: total tech workforce (incl. tech jobs in other sectors) 7.5-8 mn in 2023. Overlaps NASSCOM BPM headcount; no pay figure.",
    "medium")

IT = [
    # name, hc FY22, FY23, FY24, FY25, FY26, emp cost FY26 (cr), cost/head lakh FY26, MRE FY26 (Rs), MRE note, url
    ("TCS", 592195, 614795, 601546, 607979, 584519, 154994, 25.99, 845000,
     "MRE not printed; ~Rs 8.45 lakh DERIVED = CEO pay Rs 2,811.3 lakh / ratio 332.8 (AR26 p167); MRE +5.1% in FY26. BRSR FY26 medians (other than BoD/KMP): men Rs 18.3 lakh, women Rs 11.9 lakh - inconsistent with derived figure, hence low confidence on pay.",
     "https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/ar/annual-report-2025-2026.pdf", "low"),
    ("Infosys", 314015, 343234, 317240, 323578, 328594, 95094, 29.16, 1113024,
     "MRE Rs 11,13,024 FY26 vs Rs 10,72,008 FY25 (AR FY26, NSE copy p.58, verified). Standalone 2,52,753 employees; India 2,58,502 of 3,28,594 (20-F). Avg India salary hike 11% FY26.",
     "https://nsearchives.nseindia.com/annual_reports/AR_29297_INFY_2025_2026_A_8985010_29052026200926.pdf", "high"),
    ("Wipro", 236204, 248813, 234054, 233346, 242156, 55586, 23.38, 947000,
     "MRE Rs 9.47 lakh FY26 (-3.18%); FY25 Rs 9.79 lakh (AR26 p284). FY22-23 headcount = permanent employees on rolls of the Company (may be narrower than group). India permanent employees 1,90,064 (BRSR FY26 p505).",
     "https://www.wipro.com/investors/annual-reports/", "high"),
    ("HCLTech", 208877, 225944, 227481, 223420, 227181, 74143, 32.91, "",
     "MRE not printed; HCLTech reports MRE for GLOBAL employees at PPP (AR26 p138), +5.4% FY26. BRSR FY26 PPP medians: men Rs 14.83 lakh, women Rs 8.24 lakh (p260). FY26 cost includes Rs 850 cr restructuring.",
     "https://www.hcltech.com/investors/annual-reports", "medium"),
    ("Tech Mahindra", 151173, 152400, 145455, 148731, 147623, 30479, 20.57, 590000,
     "MRE Rs 5.9 lakh FY26 (-4.89%), Rs 6.2 lakh FY25, Rs 6.63 lakh FY24, standalone permanent employees (1,19,337 in Mar-2026) (AR26 p303/324/555). Group headcount includes BPO staff.",
     "https://insights.techmahindra.com/investors/tml-integrated-annual-report-fy-2025-2026.pdf", "high"),
    ("LTIMindtree (LTM)", 79594, 84546, 81650, 84307, 87950, 26287, 30.52, 1721000,
     "MRE Rs 17.21 lakh FY26 (-1.2%), Rs 17.42 lakh FY25 (AR26 p173/223). ~88.5% of employees in India (AR26 p102). FY22 headcount is pre-merger (L&T Infotech+Mindtree combined as reported).",
     "https://www.ltm.com/wp-content/uploads/investors/2026/05/integrated-annual-report-fy26.pdf", "high"),
]
for name, h22, h23, h24, h25, h26, cost, cph, mre, note, url, conf in IT:
    add("IT-BPM", f"{name} (company, global headcount; subset of tech total)",
        h26, "31-Mar-2026", mre,
        ("Median remuneration of employees (MRE), Companies Act s.197 / Rule 5 disclosure, standalone entity"
         + (" - DERIVED from CEO pay / CEO:MRE ratio" if name == "TCS" else "")) if mre else "",
        "FY2025-26" if mre else "",
        "BE/BTech/MCA/BSc", g(h26, h22),  # 4-yr FY22-FY26; see notes
        url,
        f"Headcount FY22 {h22:,}; FY23 {h23:,}; FY24 {h24:,}; FY25 {h25:,}; FY26 {h26:,} (4-yr change FY22-FY26 {g(h26, h22)}%). "
        f"Consolidated employee benefit expense FY26 Rs {cost:,} cr -> Rs {cph} lakh per average employee (global incl. onsite; overstates India pay). " + note,
        conf)
add("IT-BPM", "Cognizant - India employees (subset of tech total)", 256900, "31-Dec-2025", "", "", "",
    "BE/BTech/MCA/BSc", "",
    "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001058290&type=10-K",
    f"10-K 'Workforce' section: India 258,500 (2022), 254,000 (2023), 241,500 (2024), 256,900 (2025) of 351,600 total; 3-yr change {g(256900, 258500)}%. No employee-cost line in 10-K, no MRE.",
    "high")
add("IT-BPM", "Pay benchmark: IT services fresher (campus mass-hiring tracks)", "", "", 400000,
    "Typical entry CTC, mass-hiring track (~Rs 3.4-4.5 lakh); premium tracks Rs 7-21 lakh", "2025-26",
    "BE/BTech/MCA/BSc", "",
    "secondary: company recruitment banners/job portals as reported in press (TCS Ninja ~3.36L; Wipro Elite ~3.5L; Cognizant GenC ~4L; HCLTech regular ~4.5L)",
    "SECONDARY, not an official pay table. Infosys CHRO (Dec 2025) said Specialist Programmer packages go 'up to Rs 21 lakh'; HCLTech CPO (Q3FY26 call) said elite-cadre pay is 3-4x regular entry. Entry pay has been roughly flat for years.",
    "low")

# ---------------- Banking (RBI STRBI 2024-25, Table 12 employees; Table 2 earnings & expenses) ----------------
RBI = "https://data.rbi.org.in/#/dbie/reports/Publication/Time-Series%20Publications/Statistical%20Tables%20Relating%20to%20Banks%20in%20India"
rbi_t = "RBI Statistical Tables Relating to Banks in India 2024-25 (released 29-Dec-2025), Table 12 'Bank-wise and Category-wise Employees of SCBs' (as at 31-Mar-2025)"
pay_m = "Payments to and provisions for employees (STRBI Table 2, FY2024-25) / employees at 31-Mar-2025; includes pension/gratuity provisions and all grades"
banks = [
    ("Public sector banks (12)", 757641, 790659, 177893.70, "Officers 4,23,650; clerks 2,47,776; sub-staff 86,215. SBI alone 2,36,226. PSB pay is set by IBA bipartite settlements (clerks/sub-staff) and joint notes (officers); per-head cost is high partly because of pension provisions.", "high"),
    ("Private sector banks", 838150, 554418, 98841.48, "Officers 7,93,326 (95%); clerks 36,637; sub-staff 8,187 - private banks classify almost all staff as officers. HDFC Bank 2,14,521; ICICI 1,30,957; Axis 1,04,453; Kotak 75,323. Excludes outsourced/contract sales staff.", "high"),
    ("Foreign banks", 28041, 23581, 11211.30, "Officers 26,056.", "high"),
    ("Small finance banks", 177797, 95249, None, "Officers 1,25,260; clerks 24,798; sub-staff 27,739. Pay not computed (group total row of Table 2 not extracted).", "high"),
    ("Payments banks", 6958, 2048, None, "", "high"),
]
for sub, n, n20, cost, note, conf in banks:
    add("Banking", sub, n, "31-Mar-2025", per_head(cost, n) if cost else "", pay_m if cost else "", "FY2024-25" if cost else "",
        "Graduate (clerk/PO entry via IBPS/SBI exams); MBA/CA for specialist officers",
        g(n, n20), RBI, f"{rbi_t}. 2019-20 base {n20:,}. " + note, conf)
add("Banking", "ALL scheduled commercial banks - total (sum of rows above; RRBs not included)", 1808587, "31-Mar-2025",
    per_head(299244.28, 1808587), pay_m, "FY2024-25", "Graduate", g(1808587, 1465955), RBI,
    f"{rbi_t}. All-SCB by category: officers 13,75,212 (5-yr {g(1375212, 1003974)}%), clerks 3,10,462 ({g(310462, 318381)}%), sub-staff 1,22,913 ({g(122913, 143600)}%). TOTAL ROW - do not add to group rows.",
    "high")
add("Banking", "PSB clerks (category split; overlaps PSB row)", 247776, "31-Mar-2025", "", "", "", "Graduate (IBPS Clerk)",
    g(247776, 281989), RBI, f"{rbi_t}. PSB clerks fell from 2,81,989 (2019-20). Useful as the 'bank clerk' occupation tile; overlaps PSB total.", "high")
add("Banking", "PSB officers (category split; overlaps PSB row)", 423650, "31-Mar-2025", "", "", "", "Graduate (IBPS PO) / professional",
    g(423650, 396469), RBI, f"{rbi_t}. Overlaps PSB total.", "high")

# ---------------- Insurance ----------------
IRDAI = "https://irdai.gov.in/annual-reports"
add("Insurance", "Life insurance individual agents (commission-based, often part-time)", 3123000, "31-Mar-2025", "", "", "",
    "Class 10/12 + IRDAI agent exam", "", IRDAI,
    "IRDAI Annual Report 2024-25, para II.2.1.1 (PDF p.295): 31.23 lakh individual life agents (LIC 14.87 lakh, private 16.37 lakh), +7.87% y/y from 28.95 lakh. Agents are licences, not FTE jobs; many are part-time. No IRDAI table of insurer EMPLOYEES found.",
    "high (count) / low (as employment)")
add("Insurance", "General + standalone health insurance individual agents", 773107 + 1549000, "31-Mar-2025", "", "", "",
    "Class 10/12 + IRDAI agent exam", "", IRDAI,
    "IRDAI AR 2024-25 paras II.2.1.3-4: general insurers 7,73,107 agents (+12.17%); standalone health insurers 15.49 lakh (+18.66%). Possible overlap with life agents (composite agents). Not FTE jobs.",
    "medium")

# ---------------- Government ----------------
BUD26 = "https://www.indiabudget.gov.in/doc/eb/stat22.xlsx"
BUD22 = "https://www.indiabudget.gov.in/budget2022-23/doc/eb/stat22.pdf"
bud_t = "Union Budget 2026-27 Expenditure Profile, Statement 22 'Estimated strength of establishment and provisions therefor' (strength actual on 1-Mar-2025; pay+allowances = 2024-25 actuals, excl. travel)"
pm = "Pay + allowances (incl. DA, HRA etc.; excl. travel) per sanctioned-in-position employee, 2024-25 actuals"
gov = [
    ("Central govt civilian employees - TOTAL (all ministries; excl. armed forces personnel)", 3302539, 3180400, 160473.76 + 166226.32,
     "TOTAL ROW: includes Railways, central police (CAPFs etc.), Posts. Estimated strength 1-Mar-2026: 35,77,657. 2024-25 actual pay Rs 1,60,474 cr + allowances Rs 1,66,226 cr."),
    ("Indian Railways employees", 1212958, 1252347, 64212.14 + 60152.45, "Railways shrank 3.1% since 2020; estimated 12,30,224 (2026)."),
    ("Central police (MHA 'Police': CAPFs - CRPF, BSF, CISF, ITBP, SSB, AR - plus Delhi Police, IB etc.)", 1101452, 1003573, 53737.04 + 61185.82, "Estimated 12,02,988 (2026). State police forces are NOT included (state govt; BPR&D site unreachable)."),
    ("Department of Posts", 474386, 403817, 8356.40 + 13771.25, "Low per-head pay suggests the count includes Gramin Dak Sevaks (part-time allowance-paid) - not verified."),
]
for sub, n, n20, crore, note in gov:
    add("Government", sub, n, "1-Mar-2025", per_head(crore, n), pm, "FY2024-25",
        "Class 10 (MTS) to graduate (SSC CGL) to UPSC CSE graduate", g(n, n20), f"{BUD26}; {BUD22}",
        f"{bud_t}. 2020 base (Budget 2022-23 Statement 22, actual 1-Mar-2020) {n20:,}. " + note, "high")
other_n = 3302539 - 1212958 - 1101452 - 474386
other_n20 = 3180400 - 1252347 - 1003573 - 403817
other_cr = (160473.76 + 166226.32) - (64212.14 + 60152.45) - (53737.04 + 61185.82) - (8356.40 + 13771.25)
add("Government", "Other central ministries & departments (tax depts, audit, defence civilians, atomic energy, UTs etc.)",
    other_n, "1-Mar-2025", per_head(other_cr, other_n), pm, "FY2024-25",
    "Graduate (SSC CGL / UPSC) mostly", g(other_n, other_n20), f"{BUD26}; {BUD22}",
    f"Residual = total minus Railways, central police, Posts. Includes Direct Taxes 49,129; Indirect Taxes 58,865; Indian Audit & Accounts 40,652; Defence (Civil) 71,371; Atomic Energy 32,503 (1-Mar-2025).",
    "high")
add("Government", "Pay benchmark: 7th CPC pay matrix entry basic pay (central govt)", "", "", "",
    "Monthly BASIC pay at entry of level (excl. DA/HRA): L1 Rs 18,000 (MTS); L6 Rs 35,400; L7 Rs 44,900; L8 Rs 47,600; L10 Rs 56,100 (Group A entry)", "2016-present",
    "L1: Class 10; L4-L7: graduate (SSC); L10: graduate + UPSC", "",
    "https://cdnbbsr.s3waas.gov.in/s3kv023775142a8f900c2d362210cdaad9/uploads/2026/03/2026031079.pdf",
    "L6/L7/L8/L10 verified in KVS OM F.11022/1/2019 (22-Jan-2026). L1 Rs 18,000 minimum pay is the 7th CPC minimum (not re-downloaded this session). DA rate not verified this session; the per-head budget rows above already include DA. 8th CPC: status not verified this session (see md).",
    "high (L6-L10) / medium (L1)")

# ---------------- Education ----------------
UDISE = "https://dashboard.udiseplus.gov.in (UDISE+ 2024-25 booklet, Tables 4.2-4.6, pp.53-57); https://pib.gov.in/PressReleasePage.aspx?PRID=2161543"
kvs = "https://cdnbbsr.s3waas.gov.in/s3kv023775142a8f900c2d362210cdaad9/uploads/2026/03/2026031079.pdf"
add("Education", "School teachers - government schools", 5149771, "2024-25", 35400 * 12,
    "BASIC pay only, KVS PRT entry (7th CPC L6 Rs 35,400/month) - central benchmark; state govt teacher scales differ", "2026",
    "Class 12 + D.El.Ed (primary) / graduate + B.Ed; TET", "", f"{UDISE}; {kvs}",
    "UDISE+ 2024-25: 50.9% of 1,01,22,420 teachers. TGT L7 Rs 44,900; PGT L8 Rs 47,600 basic/month. Total teachers 2020-21 96.96 lakh -> 2025-26 1,02,73,020 (+5.9%, series break in 2022-23).",
    "high (count) / medium (pay)")
add("Education", "School teachers - government-aided schools", 757624, "2024-25", "", "", "", "Graduate + B.Ed; TET", "", UDISE, "UDISE+ 2024-25 (7.5%). Aided teachers are usually on state govt scales.", "high")
add("Education", "School teachers - private unaided recognised schools", 3962114, "2024-25", "", "", "", "Graduate + B.Ed (often not enforced)", "", UDISE,
    "UDISE+ 2024-25 (39.1%). No official pay figure (needs PLFS unit-level data; PLFS lane).", "high (count)")
add("Education", "School teachers - other managements (madrasa, unrecognised etc.)", 252911, "2024-25", "", "", "", "varies", "", UDISE, "UDISE+ 2024-25 (2.5%).", "high")
add("Education", "Higher-education teachers (universities, colleges, standalone)", 1732000, "2023-24", 57700 * 12,
    "BASIC pay only, Assistant Professor entry (UGC 7th CPC Academic Level 10, Rs 57,700/month); applies to govt/aided posts", "2017-present",
    "PG + NET/PhD", g(17.32, 15.03156), "https://pib.gov.in/PressReleasePage.aspx?PRID=2282525",
    "AISHE 2023-24 (released 8-Jul-2026): 17.32 lakh teachers; 59,533 of 64,756 HEIs responded (undercount). Growth is 4-yr (2019-20 15,03,156). Pay source: MHRD letter 1-7/2015-U.II(1), 2-Nov-2017 (via gconnect.in, secondary copy). Private college pay: gap.",
    "high (count) / medium (pay)")

# ---------------- Health ----------------
add("Health", "Allopathic doctors - registered (Indian Medical Register)", 1535155, "Jul-2026", 56100 * 12,
    "BASIC pay only, central govt doctor entry (7th CPC Level 10, Rs 56,100/month) excl. 20% NPA, DA, HRA; private pay: no official figure", "2026",
    "MBBS", "", "https://pib.gov.in/PressReleasePage.aspx?PRID=2288843",
    "Registered stock, not employment; govt assumes 80% available (=> ~12.3 lakh active, derived). NMC series: 13,08,009 (Jun-2022) -> 13,88,185 (Mar-2026) = +6.1%; jump to 15.35 lakh reflects switch to IMR, not growth. NPA rule secondary (gconnect).",
    "high (register) / low (as employment)")
add("Health", "AYUSH practitioners - registered", 751768, "Jul-2026", "", "", "", "BAMS/BHMS/BUMS/BSMS", "", "https://pib.gov.in/PressReleasePage.aspx?PRID=2288843",
    "Registered stock; series inconsistent so no growth computed.", "medium")
add("Health", "Nurses & midwives - registered (RN&RM 34,87,731; ANM 10,59,246; LHV 55,156)", 4602133, "31-Dec-2025", "", "", "",
    "GNM diploma / BSc Nursing (RN&RM); ANM diploma", g(46.02133, 33.41),
    "https://sansad.in/getFile/lsapps/loksabhaquestions/annex/188/AU1138_TmyJq8.pdf",
    "Lok Sabha USQ 1138 (24-Jul-2026) Annexure I, source INC/state councils; some states' data to 2021-24. Only 14,24,148 enrolled on NRTS. 33.41 lakh in 2022 (PIB 5-Apr-2022) -> +37.7% in ~4 yrs. Registered stock, not employment. No official nurse pay series.",
    "high (register) / low (as employment)")
add("Health", "Pharmacists - registered", 1600000, "2023 (Feb)", "", "", "", "D.Pharm / B.Pharm", "",
    "https://www.millenniumpost.in/nation/india-has-16l-registered-pharmacists-508295",
    "Lok Sabha reply Feb-2023 as reported by PTI (secondary; PCI register not accessed).", "low")
add("Health", "Dentists - registered", 319000, "2024 (Feb)", "", "", "", "BDS", "",
    "secondary: Business Standard Feb-2024 citing DCI register; Rajya Sabha 8-Feb-2022 2.89 lakh (via medicaldialogues.in)",
    "Secondary only.", "low")
add("Health", "ASHA workers", 1033000, "2026", 2000 * 12,
    "Central FIXED monthly incentive Rs 2,000 x 12 (routine/recurring activities); excludes task-based incentives and state top-ups", "2024",
    "Class 8-10 (NHM guideline; not re-verified)", g(10.33, 10.47324),
    "https://pib.gov.in/PressReleasePage.aspx?PRID=2296281; https://pib.gov.in/PressReleasePage.aspx?PRID=2079023",
    "Count: Parliamentary Standing Committee report (PIB 7-Aug-2026). 2019 base 10,47,324 (NHM-MIS, PIB 13-Mar-2020); growth is ~7-yr. Increase of fixed incentive to Rs 3,500 approved by Mission Steering Group 4-Mar-2025 per a Jul-2025 Lok Sabha reply (secondary, implementation date not found). Honorarium workers, not employees.",
    "high (count) / medium (pay)")
add("Health/ICDS", "Anganwadi workers (AWW)", 1348135, "31-Dec-2023", 4500 * 12,
    "Central honorarium Rs 4,500/month x 12 (cost-shared with states; states add top-ups); + Rs 500/month performance incentive", "since 1-Oct-2018",
    "Class 12 (Saksham guidelines; not re-verified)", "",
    "https://pib.gov.in/PressReleasePage.aspx?PRID=2003433; https://pib.gov.in/PressReleasePage.aspx?PRID=2226338",
    "In-position per Poshan Tracker (Rajya Sabha USQ 627, PIB 7-Feb-2024); sanctioned 13,99,697 (2019). Mini-AWW Rs 3,500 (being upgraded). No hike under consideration (PIB 11-Feb-2026).",
    "high")
add("Health/ICDS", "Anganwadi helpers (AWH)", 1023068, "31-Dec-2023", 2250 * 12,
    "Central honorarium Rs 2,250/month x 12 + Rs 250/month performance incentive; states add top-ups", "since 1-Oct-2018",
    "Class 10", "", "https://pib.gov.in/PressReleasePage.aspx?PRID=2003433",
    "Sanctioned 12,82,847 (2019).", "high")

# ---------------- Professions ----------------
add("Professions", "Chartered accountants (ICAI members)", 452825, "1-Apr-2026", 1250000,
    "Average CTC offered to newly qualified CAs at ICAI campus placements (~Rs 12-13 lakh p.a.; ICAI statements)", "2024-2026",
    "CA (ICAI) after Class 12/graduation", g(452825, 327081),
    "https://resource.cdn.icai.org/9368177th-annual-report-gazette-india.pdf",
    "ICAI 77th Annual Report 2025-26 Gazette pp.282-284: 3,29,670 associates + 1,23,155 fellows; 4,23,105 on 1-Apr-2025; 3,27,081 in 2021. Members include those in practice, industry, abroad and retired. Campus pay is a fresher offer average (secondary via Taxscan / ICAI briefing); top offers Rs 26.6-29 lakh.",
    "high (count) / medium (pay)")
add("Professions", "Company secretaries (ICSI members)", 78000, "Jan-2026", "", "", "", "CS (ICSI)", "",
    "secondary: ICSI press release via PTI wire (theweek.in), 20-Jan-2026", "'over 78,000 members'; ~2.5 lakh students.", "medium")
add("Professions", "Cost & management accountants (ICMAI members)", 100000, "2024-25", "", "", "", "CMA (ICMAI)", "",
    "ICMAI Annual Report 2024-25 p.2/p.20", "'approximately 1,00,000 members' (rounded self-description); 1,630 new associates in FY25.", "low")
add("Professions", "Advocates (enrolled with State Bar Councils)", 2000000, "2025", "", "", "", "LLB (3-yr/5-yr) + AIBE", "",
    "secondary: lawinsider.in / lawchakra.in (Oct-2025) citing Rajya Sabha reply and state-council totals (20,13,081)",
    "Enrolment stock, includes non-practising. 2019 Rajya Sabha reply 16,39,105 (snippet only). Not verified from BCI.", "low")
add("Professions", "Architects (Council of Architecture register)", 105000, "undated (~2024)", "", "", "", "BArch", "",
    "secondary: constructionworld.in interview with CoA president", "~85,000 with valid registration. Not verified from coa.gov.in.", "low")

# ---------------- Platform / gig ----------------
add("Platform/gig", "Gig & platform workers (NITI Aayog estimate, all sectors)", 7700000, "2020-21", "", "", "",
    "mixed: 47% medium-skill, 22% high-skill, 31% low-skill jobs", "",
    "https://www.niti.gov.in/sites/default/files/2022-06/25th_June_Final_Report_27062022.pdf",
    "NITI Aayog 'India's Booming Gig and Platform Economy' (Jun-2022) Exec Summary pp.xvii-xviii (PDF pp.19-20): 68 lakh (2019-20), 77 lakh (2020-21) = 2.6% of non-farm workforce; projected 2.35 crore by 2029-30. By sector: ~26.6 lakh retail trade & sales, ~13 lakh transport, 6.3 lakh finance & insurance, 6.2 lakh manufacturing. 1-yr growth 2019-20 to 2020-21 = +13.2% (no 5-yr series). Model estimate from PLFS, not a count. No official earnings series. Overlaps retail/transport tiles; also listed in informal_sectors lane - do not double count.",
    "low (model estimate)")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows -> {OUT}")
for r in rows:
    print(r["sector"], "|", r["sub_sector"][:60], "|", r["headcount"], "|", r["pay_annual_inr"], "|", r["growth_5yr_pct"])
