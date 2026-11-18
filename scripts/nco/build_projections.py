"""Collect India employment PROJECTIONS (labelled) into data/nco/india_employment_projections.csv.
Sources: ILOSTAT ILO modelled estimates (Nov 2025) total-employment projections; WEF Future of Jobs Report 2025,
India economy profile (employer-survey expectations, 2025-2030). Values copied from the downloaded files.
Run: python -I build_projections.py
"""
import pandas as pd
ROOT = r"C:\Users\hp\Downloads\xyz\india_jobs"
m = pd.read_csv(ROOT + r"\data\ilostat\ilostat_ind_modelled_estimates.csv", dtype={"year": str})
x = m[(m.indicator == "EMP_2EMP_SEX_AGE_NB") & (m.sex == "SEX_T") & (m.classif1 == "AGE_YTHADULT_YGE15")
      & (m.year.isin(["2024", "2025", "2026", "2027"]))]
rows = [dict(source="ILO modelled estimates, Nov. 2025 (ILOSTAT EMP_2EMP_SEX_AGE_NB)", scope="India, total employment, age 15+",
             item="Total employment", metric="persons (thousands)", value=r.value, period=r.year,
             type="projection" if int(r.year) >= 2026 else "modelled estimate (base)",
             url="https://rplumber.ilo.org/data/indicator/?id=EMP_2EMP_SEX_AGE_NB_A&ref_area=IND&format=.csv",
             page_or_table="", note="ILO modelled series; level not comparable with ILOSTAT PLFS-microdata totals (476.6m in 2025)")
        for r in x.itertuples()]
WEF = "https://reports.weforum.org/docs/WEF_Future_of_Jobs_Report_2025.pdf"
for role, net, glob in [("AI and Machine Learning Specialists", 176, 82), ("Data Analysts and Scientists", 54, 41),
                        ("Business Intelligence Analysts", 17, 18), ("Business Development Professionals", 14, 19),
                        ("Assembly and Factory Workers", 2, 0),
                        ("Administrative Assistants and Executive Secretaries", -20, -20)]:
    rows.append(dict(source="WEF Future of Jobs Report 2025 (Jan 2025), Economy Profile India", scope="India, surveyed employers",
                     item=role, metric="expected net role growth 2025-2030, % (India)", value=net, period="2025-2030",
                     type="projection (employer survey)", url=WEF, page_or_table="Economy Profile India, p.148 'Key roles for business transformation'",
                     note=f"global net growth for same role: {glob}%; read from PDF text layer of a chart"))
pd.DataFrame(rows).to_csv(ROOT + r"\data\nco\india_employment_projections.csv", index=False)
print(pd.DataFrame(rows)[["item", "value", "period", "type"]])
