"""Write firm_median_pay.csv from figures read off the annual-report PDFs (NSE-filed copies).
All figures were located with firm_extract.py / firm_snip.py; page numbers are PDF page (1-based)
and printed page where the extracted text showed one. Unit conversions are done here so the arithmetic is explicit."""
import csv, json, os

RAW = r"C:\Users\hp\Downloads\xyz\india_jobs\data\raw\tax_linkage\company_reports"
OUT = r"C:\Users\hp\Downloads\xyz\india_jobs\data\tax_linkage\firm_median_pay.csv"
U = json.load(open(os.path.join(RAW, "_urls.json")))

mn = lambda x: round(x / 10, 2)        # Rs million -> Rs crore
th = lambda x: round(x / 10000, 2)     # Rs thousand -> Rs crore

# TCS derived MRE = CEO remuneration (Rs lakh, CG report) / CEO-to-median ratio (annexure)
tcs26_ceo = 167.6 + 143.7 + 2500.0     # salary + benefits/perqs/allowances + commission (Rs lakh), FY26 AR pdfp84
tcs25_ceo = 139.5 + 212.8 + 2300.0     # FY25 AR pdfp106
tcs26_mre = round(tcs26_ceo * 1e5 / 332.8)
tcs25_mre = round(tcs25_ceo * 1e5 / 329.8)
sbi26_avg = round(65723.78e7 / 245131)
sbi25_avg = round(64352.24e7 / 236226)

R = []
def row(**k): R.append(k)

row(company="TCS", sector="IT services", fiscal_year="FY2025-26", median_remuneration_rs=tcs26_mre, mre_change_pct=5.1,
    permanent_employees_in_annexure=584519, entity_scope="TCS Ltd (ratio note: employees of the Company excl. subsidiaries); annexure headcount looks group-wide",
    employee_benefits_expense_cr_standalone=112142, employee_benefits_expense_cr_consolidated=154994, headcount_total=584519,
    current_tax_cr_standalone=14178, ceo_to_mre_ratio="332.8 (K Krithivasan)", source_url=U["TCS_FY26"],
    pdf_page="44 (annexure); 84 (CEO pay); 254 (std P&L); 168 (cons P&L); 131 (BRSR)", printed_page="n/a (160 for BRSR)", confidence="medium",
    notes=f"MRE NOT PRINTED - DERIVED: CEO pay Rs {tcs26_ceo:.1f} lakh (167.6 salary+143.7 perqs+2500.0 commission) / 332.8 = Rs {tcs26_mre:,}; implied MRE growth vs FY25 derived = {100*(tcs26_mre/tcs25_mre-1):.2f}% vs printed 5.1%. BRSR median (employees other than BoD/KMP): male Rs 18.3 lakh (n=378,966), female Rs 11.9 lakh (n=205,549) - both ABOVE derived MRE, so BRSR uses a different population/pay definition; unresolved. Rs crore.")
row(company="TCS", sector="IT services", fiscal_year="FY2024-25", median_remuneration_rs=tcs25_mre, mre_change_pct=6.3,
    permanent_employees_in_annexure=607979, entity_scope="TCS Ltd; annexure headcount looks group-wide",
    employee_benefits_expense_cr_standalone=107300, employee_benefits_expense_cr_consolidated=145788, headcount_total=607979,
    current_tax_cr_standalone=14823, ceo_to_mre_ratio="329.8 (K Krithivasan)", source_url=U["TCS_FY25"],
    pdf_page="74 (annexure); 106 (CEO pay); 149 (BRSR)", printed_page="71; 68 (BRSR)", confidence="medium",
    notes=f"MRE NOT PRINTED - DERIVED: CEO pay Rs {tcs25_ceo:.1f} lakh (139.5+212.8+2300.0) / 329.8 = Rs {tcs25_mre:,}. Expense/tax = prior-year comparatives in FY26 AR (pdfp254 std, 168 cons). BRSR: male Rs 16.7 lakh (n=393,937), female Rs 10.6 lakh (n=214,039).")

row(company="Infosys", sector="IT services", fiscal_year="FY2025-26", median_remuneration_rs=1113024, mre_change_pct="~4 (approx., as printed)",
    permanent_employees_in_annexure="", entity_scope="Infosys Ltd (standalone)", employee_benefits_expense_cr_standalone=73239,
    employee_benefits_expense_cr_consolidated=95094, headcount_total=198966 + 129625, current_tax_cr_standalone=10459,
    ceo_to_mre_ratio="742 incl. stock incentives / 289 excl. (Salil Parekh)", source_url=U["INFY_FY26"],
    pdf_page="58 (MRE); 57 (ratio); 169 (BRSR); 210 (std P&L); 288 (cons P&L)", printed_page="88; 87; 199; 240; 318", confidence="high",
    notes="Annexure count of permanent employees not found in extracted text; headcount_total = BRSR permanent employees 198,966 male + 129,625 female = 328,591. BRSR median: male Rs 0.11 cr, female Rs 0.09 cr (rounded to 0.01 cr). Report does not say whether MRE is India-only. NSE file is the 'Revised' (U) filing of 30-May-2026.")
row(company="Infosys", sector="IT services", fiscal_year="FY2024-25", median_remuneration_rs=1072008, mre_change_pct=9.63,
    permanent_employees_in_annexure="", entity_scope="Infosys Ltd (standalone)", employee_benefits_expense_cr_standalone=67466,
    employee_benefits_expense_cr_consolidated=85950, headcount_total=197246 + 126332, current_tax_cr_standalone=10836,
    ceo_to_mre_ratio="752 incl. stock incentives / 290 excl. (Salil Parekh)", source_url=U["INFY_FY25"],
    pdf_page="55 (MRE); 54 (ratio); 158 (BRSR)", printed_page="82; 81; 185", confidence="high",
    notes="headcount_total = BRSR permanent 197,246 + 126,332 = 323,578. BRSR median male Rs 0.11 cr, female Rs 0.08 cr. Expense/tax = comparatives in FY26 AR (pdfp210, 288).")

row(company="HCLTech", sector="IT services", fiscal_year="FY2025-26", median_remuneration_rs="", mre_change_pct=5.4,
    permanent_employees_in_annexure=170811, entity_scope="HCL Technologies Ltd (company); +56,370 on subsidiaries' rolls",
    employee_benefits_expense_cr_standalone=25323, employee_benefits_expense_cr_consolidated=74143, headcount_total=170811 + 56370,
    current_tax_cr_standalone=2743, ceo_to_mre_ratio="291.9 (C Vijayakumar; PPP basis)", source_url=U["HCLTECH_FY26"],
    pdf_page="161-162 (annexure); 283 (BRSR); 323 (std P&L); 398 (cons P&L)", printed_page="135-136; 257; 297; 372", confidence="medium",
    notes="Absolute MRE NOT printed. FY26 median computed over ALL GLOBAL employees with pay converted to INR at country-to-India PPP factors (note 1, pdfp161). CEO paid in USD by HCL America (FY26 base 2.48 + bonus 2.00 + LTI cash 3.94 USD mn + RSU perqs, pdfp219) - not derived. BRSR (PPP-adjusted): male Rs 14.83 lakh (n=166,106), female Rs 8.24 lakh (n=69,361), others Rs 20.05 lakh (n=592).")
row(company="HCLTech", sector="IT services", fiscal_year="FY2024-25", median_remuneration_rs="", mre_change_pct=17.63,
    permanent_employees_in_annexure=167316, entity_scope="HCL Technologies Ltd (company); +56,104 on subsidiaries' rolls",
    employee_benefits_expense_cr_standalone=22414, employee_benefits_expense_cr_consolidated=66755, headcount_total=167316 + 56104,
    current_tax_cr_standalone=3344, ceo_to_mre_ratio="662.57 vs global median; 103.39 vs US median", source_url=U["HCLTECH_FY25"],
    pdf_page="175-177 (annexure); 273 (BRSR)", printed_page="121-123; 218", confidence="medium",
    notes="Absolute MRE NOT printed; median 'taken on a global basis' (note 1, pdfp176). BRSR (USD at INR 82): male Rs 18.18 lakh (n=167,071), female Rs 9.53 lakh (n=67,217). Expense/tax = comparatives in FY26 AR. FY25->FY26 basis change (PPP) makes ratios/medians non-comparable.")

row(company="Wipro", sector="IT services", fiscal_year="FY2025-26", median_remuneration_rs=947425, mre_change_pct=-3.18,
    permanent_employees_in_annexure=242156, entity_scope="Wipro Ltd", employee_benefits_expense_cr_standalone=mn(388809),
    employee_benefits_expense_cr_consolidated=mn(555855), headcount_total=242156, current_tax_cr_standalone=mn(38349),
    ceo_to_mre_ratio="523.96 incl. stock incentives / 278.36 excl. (Srinivas Pallia)", source_url=U["WIPRO_FY26"],
    pdf_page="126-127 (annexure); 191 (std P&L); 297 (cons P&L)", printed_page="139-140; 204; 310", confidence="high",
    notes="MRE excl. WTDs = incl. WTDs = Rs 947,425. Financials printed in Rs million (388,809; 555,855; 38,349) /10 = Rs crore. BRSR refers back to annexure pages.")
row(company="Wipro", sector="IT services", fiscal_year="FY2024-25", median_remuneration_rs=978516, mre_change_pct="",
    permanent_employees_in_annexure=233346, entity_scope="Wipro Ltd", employee_benefits_expense_cr_standalone=mn(383850),
    employee_benefits_expense_cr_consolidated=mn(533477), headcount_total=233346, current_tax_cr_standalone=mn(39934),
    ceo_to_mre_ratio="", source_url=U["WIPRO_FY26"], pdf_page="127 (FY26 AR comparatives)", printed_page="140", confidence="medium",
    notes="FY25 AR could not be read: NSE file AR_26582_WIPRO_2024_2025 downloads truncated (2,293,760 bytes, 0 pages) twice; no web.archive copy. MRE and headcount taken from FY26 AR prior-year figures; FY25 % change and CEO ratio missing.")

row(company="Tech Mahindra", sector="IT services", fiscal_year="FY2025-26", median_remuneration_rs=590000, mre_change_pct=-4.89,
    permanent_employees_in_annexure=119337, entity_scope="Tech Mahindra Ltd (standalone)", employee_benefits_expense_cr_standalone=mn(176630),
    employee_benefits_expense_cr_consolidated=mn(304788), headcount_total=147623, current_tax_cr_standalone=mn(14079),
    ceo_to_mre_ratio="1,085.27* incl. ESOPs (Mohit Joshi)", source_url=U["TECHM_FY26"],
    pdf_page="329-330 (annexure); 432 (BRSR); 472 (std P&L); 582 (cons P&L); 351 (headcount)", printed_page="300-301; 403; 443; 553; 322", confidence="medium",
    notes="MRE printed only as 'Rs 0.59 Mn' (rounded). headcount_total = global headcount 147,623 (MD&A). BRSR median (permanent): male Rs 18.90 lakh (n=91,678), female Rs 16 lakh (n=48,504) - both far ABOVE annexure MRE, i.e. different population/definition; unresolved. 78.1% 'IT headcount offshoring' (pdfp51). Financials in Rs million /10.")
row(company="Tech Mahindra", sector="IT services", fiscal_year="FY2024-25", median_remuneration_rs=620000, mre_change_pct=-6.52,
    permanent_employees_in_annexure=119343, entity_scope="Tech Mahindra Ltd (standalone)", employee_benefits_expense_cr_standalone=mn(171070),
    employee_benefits_expense_cr_consolidated=mn(296238), headcount_total=148731, current_tax_cr_standalone=mn(12353),
    ceo_to_mre_ratio="840.22 incl. ESOPs (Mohit Joshi)", source_url=U["TECHM_FY25"],
    pdf_page="342-343 (annexure); 375 (BRSR)", printed_page="304-305; 337", confidence="medium",
    notes="MRE printed as 'Rs 0.62 Mn'. BRSR: male Rs 18.3 lakh (n=91,252), female Rs 15.4 lakh (n=47,999) - inconsistent with MRE. Headcount 148,731 and financials = comparatives in FY26 AR (pdfp50/351, 472, 582).")

row(company="LTIMindtree (LTM Ltd)", sector="IT services", fiscal_year="FY2025-26", median_remuneration_rs=1721230, mre_change_pct=-1.20,
    permanent_employees_in_annexure=87950, entity_scope="Company excl. subsidiaries", employee_benefits_expense_cr_standalone=mn(238813),
    employee_benefits_expense_cr_consolidated=mn(262869), headcount_total=87950, current_tax_cr_standalone=mn(17679),
    ceo_to_mre_ratio="158.40 (Venugopal Lambu, CEO&MD from 31-May-2025)", source_url=U["LTIM_FY26"],
    pdf_page="174 (annexure); 127 (BRSR); 185 (std P&L); 224 (cons P&L)", printed_page="342-343; 248-249; 364-365; 442-443", confidence="high",
    notes="NSE now lists the company as 'LTM Limited' (symbol LTM). headcount_total = standalone rolls (consolidated not extracted). BRSR: male Rs 17,14,668 (n=60,710), female Rs 11,96,616 (n=27,130). Financials printed 'Rs in Million' (confirmed on pdfp185) /10 = Rs crore.")
row(company="LTIMindtree (LTM Ltd)", sector="IT services", fiscal_year="FY2024-25", median_remuneration_rs=1742148, mre_change_pct=24.43,
    permanent_employees_in_annexure=84307, entity_scope="Company excl. subsidiaries", employee_benefits_expense_cr_standalone=mn(225961),
    employee_benefits_expense_cr_consolidated=mn(246226), headcount_total=84307, current_tax_cr_standalone=mn(15057),
    ceo_to_mre_ratio="186.79 (Debashis Chatterjee)", source_url=U["LTIM_FY25"], pdf_page="143 (annexure); 99 (BRSR)", printed_page="281; 193",
    confidence="high", notes="BRSR: male Rs 17,22,816 (n=58,657), female Rs 12,13,728 (n=25,605). Financials = comparatives in FY26 AR.")

row(company="HDFC Bank", sector="Bank (private)", fiscal_year="FY2025-26", median_remuneration_rs="", mre_change_pct=11.43,
    permanent_employees_in_annexure=211178, entity_scope="HDFC Bank Ltd (standalone)", employee_benefits_expense_cr_standalone=th(260501479),
    employee_benefits_expense_cr_consolidated=37604.81, headcount_total=211178, current_tax_cr_standalone=22823.53,
    ceo_to_mre_ratio="155.95 (Sashidhar Jagdishan)", source_url=U["HDFCBANK_FY26"],
    pdf_page="327-328 (annexure); 609-610 (BRSR); 391 (std Sch.16); 510 (cons); 461 (tax)", printed_page="307-308; 589-590; 371; 490; 441", confidence="medium",
    notes="Absolute MRE NOT printed; MRE % 'includes front line sales and overseas staff' and 'only fixed pay'. BRSR medians (employees other than BoD/KMP): male Rs 6,81,759 (n=154,977), female Rs 4,81,290 (n=56,195) -> overall median must lie between these; non-supervisory staff male Rs 5,11,952 / female Rs 4,26,162. Std employee cost printed Rs '000 260,501,479 /10,000. Current tax net of Rs 1,144.46 cr write-back.")
row(company="HDFC Bank", sector="Bank (private)", fiscal_year="FY2024-25", median_remuneration_rs="", mre_change_pct=9.27,
    permanent_employees_in_annexure=214521, entity_scope="HDFC Bank Ltd (standalone)", employee_benefits_expense_cr_standalone=th(239005294),
    employee_benefits_expense_cr_consolidated=34135.75, headcount_total=214521, current_tax_cr_standalone=19485.15,
    ceo_to_mre_ratio="161.28 (Sashidhar Jagdishan)", source_url=U["HDFCBANK_FY25"], pdf_page="265-266 (annexure); 552 (BRSR)",
    printed_page="269-270; 556", confidence="medium",
    notes="Absolute MRE NOT printed. BRSR: male Rs 5,56,005 (n=158,443), female Rs 3,86,345 (n=56,072). Financials = comparatives in FY26 AR. NSE file is the revised (U) filing of 25-Jul-2025.")

row(company="ICICI Bank", sector="Bank (private)", fiscal_year="FY2025-26", median_remuneration_rs="", mre_change_pct="~12.1",
    permanent_employees_in_annexure=124029, entity_scope="ICICI Bank Ltd incl. overseas staff on rolls", employee_benefits_expense_cr_standalone=th(179748857),
    employee_benefits_expense_cr_consolidated=th(252586237), headcount_total=124324, current_tax_cr_standalone=mn(154512.2),
    ceo_to_mre_ratio="102:1 (Sandeep Bakhshi)", source_url=U["ICICIBANK_FY26"],
    pdf_page="182 (annexure); 477 (BRSR); 260 (std Sch.); 388 (cons Sch.); 327 (tax)", printed_page="n/a", confidence="medium",
    notes="Absolute MRE NOT printed. 124,029 permanent of 124,324 total employees. BRSR (fixed + perqs, excl. overseas, 'median of grade-wise median'): male Rs 698,717 (n=83,868), female Rs 658,450 (n=39,565). Employee cost printed Rs '000; tax Rs million 154,512.2 /10.")
row(company="ICICI Bank", sector="Bank (private)", fiscal_year="FY2024-25", median_remuneration_rs="", mre_change_pct="~11.4",
    permanent_employees_in_annexure=129177, entity_scope="ICICI Bank Ltd incl. overseas staff on rolls", employee_benefits_expense_cr_standalone=th(165408783),
    employee_benefits_expense_cr_consolidated=th(236299361), headcount_total=130957, current_tax_cr_standalone=mn(145884.9),
    ceo_to_mre_ratio="115:1 (Sandeep Bakhshi)", source_url=U["ICICIBANK_FY25"], pdf_page="150 (annexure); 435 (BRSR)", printed_page="n/a",
    confidence="medium", notes="BRSR: male Rs 727,328 (n=87,391), female Rs 659,621 (n=41,156). Financials = comparatives in FY26 AR.")

row(company="Axis Bank", sector="Bank (private)", fiscal_year="FY2025-26", median_remuneration_rs="", mre_change_pct=1.65,
    permanent_employees_in_annexure=101337, entity_scope="Axis Bank Ltd (standalone)", employee_benefits_expense_cr_standalone=th(122659216),
    employee_benefits_expense_cr_consolidated=14006.05, headcount_total=101337, current_tax_cr_standalone=6959.90,
    ceo_to_mre_ratio="101.9 (Amitabh Chaudhry)", source_url=U["AXISBANK_FY26"],
    pdf_page="292-293 (annexure); 428 (std Sch.); 540 (cons Sch.); 492 (tax)", printed_page="223-224; n/a; n/a; 423", confidence="medium",
    notes="Absolute MRE NOT printed; ratio is to 'median remuneration of all employees'. BRSR median table not found in this AR. Std employee cost printed Rs '000.")
row(company="Axis Bank", sector="Bank (private)", fiscal_year="FY2024-25", median_remuneration_rs="", mre_change_pct=4.3,
    permanent_employees_in_annexure=104453, entity_scope="Axis Bank Ltd (standalone)", employee_benefits_expense_cr_standalone=th(121927882),
    employee_benefits_expense_cr_consolidated=13661.28, headcount_total=104453, current_tax_cr_standalone=7477.20,
    ceo_to_mre_ratio="101.8 (Amitabh Chaudhry)", source_url=U["AXISBANK_FY25"], pdf_page="269 (annexure)", printed_page="219",
    confidence="medium", notes="Financials = comparatives in FY26 AR.")

row(company="Kotak Mahindra Bank", sector="Bank (private)", fiscal_year="FY2025-26", median_remuneration_rs="", mre_change_pct=1.69,
    permanent_employees_in_annexure=60357, entity_scope="Kotak Mahindra Bank Ltd (standalone)", employee_benefits_expense_cr_standalone=th(83907790),
    employee_benefits_expense_cr_consolidated=th(129637983), headcount_total=60357, current_tax_cr_standalone=4706.34,
    ceo_to_mre_ratio="239.13x incl. SARs excl. ESOPs (Ashok Vaswani)", source_url=U["KOTAKBANK_FY26"],
    pdf_page="263-264 (annexure); 404 (BRSR); 139 (std P&L); 71 (cons P&L); 190 (tax)", printed_page="266-267; 407; 142; 74; 193", confidence="medium",
    notes="Absolute MRE NOT printed; median over permanent employees employed for whole of FY25 and FY26. BRSR (fixed pay only): male Rs 6.46 lakh (n=43,482), female Rs 5.05 lakh (n=16,509). Employee cost printed Rs '000 (pdfp139 = schedules to Standalone P&L; pdfp71 = Consolidated). Current tax 'Provision for Current Tax' on pdfp190, taken as standalone from its position in the standalone notes (consolidated current tax Rs 6,992.52 cr shown on pdfp100).")
row(company="Kotak Mahindra Bank", sector="Bank (private)", fiscal_year="FY2024-25", median_remuneration_rs="", mre_change_pct=-0.95,
    permanent_employees_in_annexure=61170, entity_scope="Kotak Mahindra Bank Ltd (standalone)", employee_benefits_expense_cr_standalone=th(79183467),
    employee_benefits_expense_cr_consolidated=th(119635966), headcount_total=61170, current_tax_cr_standalone=5381.91,
    ceo_to_mre_ratio="176.89x (Ashok Vaswani)", source_url=U["KOTAKBANK_FY25"], pdf_page="338 (annexure); 483 (BRSR)", printed_page="340; 485",
    confidence="medium", notes="BRSR (fixed only): male Rs 6.01 lakh (n=44,459), female Rs 4.78 lakh (n=16,706). Financials = comparatives in FY26 AR.")

row(company="State Bank of India", sector="Bank (public)", fiscal_year="FY2025-26", median_remuneration_rs="", mre_change_pct="",
    permanent_employees_in_annexure="", entity_scope="SBI standalone (not under Companies Act; no Rule 5 annexure)",
    employee_benefits_expense_cr_standalone=65723.78, employee_benefits_expense_cr_consolidated=72768.24, headcount_total=245131,
    current_tax_cr_standalone=29045.07, ceo_to_mre_ratio="", source_url=U["SBIN_FY26"],
    pdf_page="86 (HR profile); 213 (std Sch.16); 316 (cons); 271 (tax); 563 (BRSR)", printed_page="83; 210; 313; 268; 268-269", confidence="medium",
    notes=f"Staff 31-Mar-2026: Officers 117,620; Associates 102,364; Subordinate & others 25,147. Avg staff cost = Rs 65,723.78 cr / 245,131 = Rs {sbi26_avg:,} per employee (year-end headcount; includes pension/retirement provisions). BRSR 'employees other than BoD/KMP': male 1,26,013 (n=174,819), female 1,12,914 (n=69,848) - unit not stated and looks MONTHLY (BoD 3,54,742 vs 40,96,686 annual in FY25); x12 = Rs 15,12,156 / 13,54,968 (derived, unit unverified).")
row(company="State Bank of India", sector="Bank (public)", fiscal_year="FY2024-25", median_remuneration_rs="", mre_change_pct="",
    permanent_employees_in_annexure="", entity_scope="SBI standalone", employee_benefits_expense_cr_standalone=64352.24,
    employee_benefits_expense_cr_consolidated=70395.70, headcount_total=236226, current_tax_cr_standalone=24843.75, ceo_to_mre_ratio="",
    source_url=U["SBIN_FY25"], pdf_page="73 (HR profile); 487 (BRSR)", printed_page="70; 226-227", confidence="medium",
    notes=f"Staff 31-Mar-2025: Officers 115,066; Associates 94,080; Subordinate & others 27,080. Avg staff cost = Rs 64,352.24 cr / 236,226 = Rs {sbi25_avg:,}. BRSR median: male Rs 13,90,223 (n=170,661), female Rs 12,82,962 (n=65,085). Financials = comparatives in FY26 AR (pdfp213, 316, 271).")

COLS = ["company", "sector", "fiscal_year", "median_remuneration_rs", "mre_change_pct", "permanent_employees_in_annexure", "entity_scope",
        "employee_benefits_expense_cr_standalone", "employee_benefits_expense_cr_consolidated", "headcount_total", "current_tax_cr_standalone",
        "ceo_to_mre_ratio", "source_url", "pdf_page", "printed_page", "confidence", "notes"]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(R)
for r in R:
    print(r["company"][:14], r["fiscal_year"], r["median_remuneration_rs"], r["mre_change_pct"], r["permanent_employees_in_annexure"],
          r["employee_benefits_expense_cr_standalone"], r["employee_benefits_expense_cr_consolidated"], r["headcount_total"], r["current_tax_cr_standalone"], sep=" | ")
print("SBI avg", sbi26_avg, sbi25_avg, "TCS", tcs26_mre, tcs25_mre)
