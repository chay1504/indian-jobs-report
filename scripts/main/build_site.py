"""
Render site/index.html from site_src/template.html, embedding site/data.json and a META
block (headline facts with sources, stress test, method notes).
Run after build_site_data.py, tax_by_occupation.py and itr_elasticity.py.
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
data = json.loads((ROOT / "site" / "data.json").read_text(encoding="utf-8"))
df = pd.DataFrame(data)
el = pd.read_csv(ROOT / "data" / "derived" / "itr_elasticity.csv")
drop = dict(zip(el.earnings_cut.round(2), el.itr_tax_drop))
scale_note = (ROOT / "data" / "derived" / "scale_factor.txt").read_text().strip()

t6 = df.tax_share[df.exposure >= 6].sum()
t6_adj = t6 + df.tax_share[(df.slug == "112") & (df.exposure < 6)].sum()
stress = []
for thr in (6, 7, 8):
    sh = float(df.tax_share[df.exposure >= thr].sum())
    stress.append({"thr": thr, "share": sh, "drops": [sh * drop[c] for c in (0.05, 0.1, 0.2)]})
PIT_IND = 13.12 * 0.8275  # FY2025-26 RE non-corporate income tax x individuals' share of non-company liability

agree = (df.exposure_a == df.exposure_b).mean()
within1 = ((df.exposure_a - df.exposure_b).abs() <= 1).mean()
x = df.dropna(subset=["ilo"])
corr_ilo = x[["exposure", "ilo"]].corr().iloc[0, 1]
corr_ab = df[["exposure_a", "exposure_b"]].corr().iloc[0, 1]

META = {
    "pit_share_central": "26%", "pit_share_gg": "16%", "top1_adults": "89%", "top2_workforce": "93%",
    "t6_adj": float(t6_adj), "elasticity": f"{drop[0.1] / 0.1:.2f}", "itr_drop_10": float(drop[0.1]),
    "stress": stress, "stress_6_10": stress[0]["drops"][1],
    "pit_individual_lcr": f"about ₹{PIT_IND:.1f} lakh crore of individual income tax (FY 2025-26 revised estimate)",
    "pit_individual_num": PIT_IND,
    "prompt": (ROOT / "data" / "scores" / "rubric.txt").read_text(encoding="utf-8"),
    "facts": [
        "<b>7.55 crore</b> individuals filed returns for AY 2023-24 (income year 2022-23); <b>62.7%</b> owed zero tax. Only <b>2.82 crore</b> people had any tax liability, about 3% of adults. (CBDT ITR statistics, Table 2.11)",
        "About <b>10 lakh returns (0.1% of adults) paid half</b> of all individual income tax; about 41 lakh paid 75%; the top 1% of adults paid about <b>89%</b> and the top 2% of a 60-crore workforce about <b>93%</b>. (CBDT AY 2023-24; this project's ranking of Table 2.11)",
        "Only about <b>72 lakh</b> individuals declared total income above ₹12 lakh in AY 2023-24. Since FY 2025-26 income up to ₹12 lakh is tax-free under the new regime (₹12.75 lakh for salaried), at a cost the Budget put at about ₹1 lakh crore a year. Rates are unchanged for 2026-27 under the Income-tax Act, 2025.",
        "Salary is <b>57%</b> of individuals' gross total income. Of the 51.6 lakh people with returned income above ₹15 lakh, 46.7 lakh had salary above ₹15 lakh. The income-tax base is mostly salaried white-collar workers.",
        "Central gross tax revenue FY 2024-25: non-corporate income tax 31.2%, corporation tax 26.0%, GST 27.0%, excise 7.9%, customs 6.1%, securities transaction tax 1.4% (Receipt Budget 2026-27). Individuals pay about 83% of non-corporate income tax, so roughly <b>a quarter of central taxes</b> and about <b>a sixth of centre-plus-state taxes</b>.",
        "Corporate tax is concentrated too: <b>877 companies</b> with profit above ₹500 crore paid 54% of it. IT, ITeS and BPO companies paid <b>10.9%</b> of company tax and financial firms 27.1% (FY 2023-24).",
        "PLFS 2025: 56% of workers are self-employed, 20% casual labourers and 24% regular salaried. Median earnings from work are about <b>₹1.44 lakh a year</b>; 99% of earners make under ₹9.7 lakh, and only about 0.6% report earnings above ₹12 lakh.",
        "GST is borne far more widely: an NIPFP study on 2022-23 consumption finds the bottom half of households bear about 30% of GST and the top fifth 37–41%.",
    ],
    "nuance": [
        "<b>Exposure is not job loss.</b> Karpathy's score measures how digital a job is. Software employment in India still grew in FY 2025-26 (NASSCOM: +1.35 lakh jobs), and an ICRIER survey of 651 IT firms found no net job loss so far, though 55% report fewer entry-level hires.",
        "<b>The pattern matches other studies.</b> IMF: 26% of Indian employment is highly exposed, against about 60% in advanced economies. World Bank (Oct 2025): AI-exposed jobs are 22% of South Asian jobs but 42% of wage earnings, and 60% of formal workers are exposed against 17% of informal workers.",
        "<b>Income tax is only one channel.</b> The same occupations also drive IT-services exports, a tenth of corporate tax and a large share of urban consumption that pays GST. A shock to them would travel through all three.",
        "<b>The tax comes from the senior tail of these jobs, not the typical worker.</b> Median pay at most large IT employers is below the ₹12.75 lakh line (FY 2025-26 annual reports: Infosys ₹11.1 lakh, Wipro ₹9.5 lakh, Tech Mahindra ₹5.9 lakh; private banks ₹4.8–7.0 lakh). Among everyone above the line in AY 2023-24, 77% had salary alone above it, as did 52% of those above ₹1 crore. AI pressure on junior roles therefore threatens future taxpayers more than today's; pressure on mid-career and senior salaries hits revenue directly.",
        "<b>Productivity can raise the base as well as shrink it.</b> If AI makes each Indian engineer or analyst more valuable, wages and tax could rise. The stress test shows only the downside.",
        "<b>One big occupation is mixed.</b> “Managing directors and chief executives” pays the largest share of income tax (about a fifth), but in PLFS 95% of its workers are self-employed shop and business owners, so it scores only 4.5. Its high-earning corporate tail would score 6–7, which is why the 6+ share is given as a range.",
        "<b>Surveys miss the very rich.</b> PLFS has only 18 sampled people earning above ₹50 lakh. Tax shares therefore come from CBDT's actual income distribution, with PLFS used only for the occupational mix within each income band.",
    ],
    "method": [
        f"<b>Workers.</b> PLFS Calendar Year 2025 unit-level data (MoSPI; 1,148,634 persons, first visit). Usual status (principal + subsidiary), age 15+, occupation = NCO-2015 3-digit group. Re-computed headline rates match MoSPI's published LFPR 59.3%, WPR 57.4%, unemployment 3.1% and the 23.6/56.1/20.2 status split exactly. Occupation-division shares match MoSPI's published Table 25 to within 0.01 points. Counts are scaled to MoSPI's own estimate of 61.6 crore workers aged 15+ (PLFS Annual Report 2025, Statement 32).",
        "<b>Earnings.</b> Current weekly status: regular salaried = last month's wage/salary; self-employed = gross earnings in the last 30 days; casual = wage earnings in the reference week × 30/7. Annualised ×12. Median shown; unpaid family helpers excluded as in PLFS reports. Check: average regular wage/salary computes to ₹22,685 a month against MoSPI's published ₹22,699 (PLFS 2025, Appendix Table 51).",
        "<b>Formal jobs.</b> Regular salaried workers eligible for any social security benefit (PF/pension, gratuity, health/maternity).",
        f"<b>AI exposure.</b> Karpathy's scoring prompt, with only the data-source sentence changed, applied to a page per occupation built from the official NCO-2015 description and PLFS statistics. Two independent passes by Claude agents; the score is their average. Passes agree exactly on {agree:.0%} of occupations and within one point on {within1:.0%} (correlation {corr_ab:.2f}). Correlation with the ILO 2025 GenAI exposure index averaged to the same groups: {corr_ilo:.2f}.",
        "<b>Income tax by occupation.</b> (1) CBDT AY 2023-24 returned-income distribution for individuals, with today's slabs (FY 2025-26 new regime, cess and surcharge) integrated within each band. (2) Each band's tax split into salary and non-salary parts using CBDT's salary-income table. (3) Salary tax allocated by the occupations of PLFS salaried earners in that band; non-salary tax by the occupations of PLFS self-employed earners. A simpler pooled version gives the same ranking.",
        "<b>Stress test.</b> Tax elasticity computed on the CBDT income distribution under today's law (a uniform income fall of 5/10/20%), applied to each exposure group's estimated tax share.",
        "<b>Not done.</b> No forecasts of job numbers; no Outlook layer (India has no BLS-style projections, and PLFS changed occupation codes in 2021 and sample design in 2025).",
    ],
    "sources": [
        ["MoSPI, PLFS Calendar Year 2025 unit-level data", "https://microdata.gov.in/NADA/index.php/catalog/284", "employment, earnings, education, formality"],
        ["MoSPI, PLFS Annual Report 2025 press note (26 Mar 2026)", "https://www.mospi.gov.in/uploads/latestReleases/latest_release_1774607827733_3e8964a9-268b-4cc9-ad65-cfc8a9e32f08_Press_note_AR_PLFS_2025_23032025_V2.1_26032026_final.pdf", "validation targets"],
        ["DGE, National Classification of Occupations 2015", "https://dge.gov.in/nco-2015", "occupation descriptions used for scoring"],
        ["CBDT, Income Tax Return Statistics AY 2023-24", "https://incometaxindia.gov.in/Documents/Direct%20Tax%20Data/Approved-version-Income-Tax-Return-Statistics-for-the-AY-2023-24.pdf", "returns, income and tax by range"],
        ["Receipt Budget 2026-27", "https://www.indiabudget.gov.in/doc/rec/allrec.pdf", "tax composition, corporate tax by profit and industry"],
        ["Budget Speech 2025-26", "https://www.indiabudget.gov.in/budget2025-26/doc/budget_speech.pdf", "₹12 lakh rebate, revenue forgone"],
        ["ILO Working Paper 140, Generative AI and Jobs: A Refined Global Index (2025)", "https://www.ilo.org/sites/default/files/2025-05/WP140_web.pdf", "cross-check scores"],
        ["ILOSTAT India series (PLFS processed by ILO)", "https://rplumber.ilo.org/data/ref_area/?id=IND_A&format=.csv", "2-digit employment, modelled totals"],
        ["IMF SDN/2024/001, Gen-AI and the Future of Work", "https://www.imf.org/-/media/Files/Publications/SDN/2024/English/sdnea2024001.ashx", ""],
        ["World Bank, South Asia Development Update (Oct 2025)", "https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf", ""],
        ["NIPFP, GST incidence by household group (2025)", "https://nipfp.org.in/media/documents/salx37130925sacchidananda-mukherjee.pdf", ""],
        ["NITI Aayog, Roadmap for Job Creation in the AI Economy (Oct 2025)", "https://niti.gov.in/sites/default/files/2025-10/Roadmap_for_Job_Creation_in_the_AI_Economy.pdf", ""],
        ["Karpathy, US Job Market Visualizer", "https://karpathy.ai/jobs/", "original method and US figures"],
        ["github.com/karpathy/jobs", "https://github.com/karpathy/jobs", "scoring prompt and code"],
    ],
}


def safe_json(o):
    return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")


tpl = (ROOT / "site_src" / "template.html").read_text(encoding="utf-8")
html = tpl.replace("__DATA__", safe_json(data)).replace("__META__", safe_json(META))
(ROOT / "site" / "artifact.html").write_text(html, encoding="utf-8")  # body-only, for the Artifact publisher
standalone = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
              '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
              '</head>\n<body>\n' + html + '\n</body>\n</html>\n')
(ROOT / "site" / "index.html").write_text(standalone, encoding="utf-8")  # open directly in a browser
print("wrote site/index.html", len(html) // 1024, "KB;  t6", round(t6, 3), "t6_adj", round(t6_adj, 3), "stress", stress[0])
