# AI exposure of India's workforce: external benchmarks and real-world evidence (2023 to Nov 2026)

Compiled 2026-11-09 for the India version of karpathy/jobs. Scope: AI-exposure estimates for India and evidence of actual impact. PLFS, tax statistics, sector headcounts, NCO/ILOSTAT mappings and tax-occupation linkage are covered by other agents and are not repeated here.

How to read the sourcing:
- **[P]** means I read the primary document myself. A page reference is the printed page number unless it says "PDF p.".
- **[S]** means a secondary source, usually press coverage. The wording or numbers were not checked against the original.
- **[chart]** means the value was read off a figure, so it is approximate (±1 to 2 points).
- Quotes are kept short. Everything else is paraphrased.
- Local copies of the primary PDFs are in `data/raw/ai_exposure/`. `_manifest.csv` there lists each file's URL and SHA-256 hash.

---

## 0. Bottom line for the hypothesis

The hypothesis: *"India will show less red overall, but AI exposure is concentrated in the small high-earning white-collar group that pays most income tax, which is dangerous."*

| Part of hypothesis | Verdict | Strongest evidence |
|---|---|---|
| India shows less red overall | **Strongly supported by every source** | IMF: 26% of Indian employment is in high-exposure occupations, against ~60% in the US and ~70% in the UK [P]. ILO 2025: 20% of employment in lower-middle-income countries is in any exposure gradient, against 34% in high-income countries. The top two gradients cover 3.8% in LMICs and 17.3% in HICs [P]. World Bank: South Asia is the lowest-exposure EMDE region together with SSA, and India and Nepal are the lowest within South Asia [P]. The ILO 2025 index applied to PLFS 2025 puts 3.8% of employed Indians in G3/G4-type occupations (preprint) [P]. |
| Exposure is concentrated in a small, high-earning, white-collar, formal and educated group | **Strongly supported** | World Bank SADU (Oct 2025): AI-exposed jobs are 22% of South Asian jobs but **42% of wage earnings**. Exposure is 17% among informal workers and **60% among formal workers** [P]. IMF: about 75% of Indian college graduates are in high-exposure jobs, against about 17% of workers with middle school or less [chart]. IMF also says AI gains will accrue disproportionately to higher earners, "especially in countries such as India" [P]. Mishra (2026), using the ILO index on PLFS 2025: 16.6% of graduates are in G3/G4-type occupations, against 3.8% of all workers [P, preprint]. |
| ...that pays most income tax | **Plausible but not tested by any source I found** | No study quantifies AI exposure of income-tax payers. The closest is Marcellus (Mukherjea), who defines the middle class through income-tax-return income bands and links its squeeze to AI and automation [P, blog]. The tax-occupation agent's work is needed to close this. |
| ...which is dangerous | **Mixed** | *Risk side:* displacement risk is concentrated in entry-level and mid-skill white-collar work. Post-ChatGPT job postings for the most-exposed, least-complementary occupations fell about 20%, and postings for secondary-education jobs fell 24% [P]. The top-5 IT firms cut net headcount in FY26, and TCS was down 23,460 year on year [S]. The Economic Survey 2024-25 explicitly flags a consumption shock [P]. The World Bank finds India's export-linked jobs are about 1.5x more substitution-exposed than its income level predicts [P]. *Mitigating side:* most exposed Indian jobs are classed as complementary rather than substitutable. The World Bank finds India has the highest complementary share in South Asia, and the IMF splits India's 26% as 14% complementary and 12% at displacement risk. NASSCOM reports the sector was still a net hirer (+2.3%, +135k) in FY26 [P]. ICRIER, RBI DG Poonam Gupta and the IT Secretary all argue no net job loss so far [P/S]. |

Nuance worth showing on the site: in India, **men are more exposed than women**, the reverse of rich countries, because Indian women work disproportionately in agriculture (IMF [P], World Bank [P]). The ILO's 2025 LMIC split is roughly even (male 20%, female 19%). In addition, ILO WP166 (2026) argues that standard exposure indices **overstate** exposure in developing countries, because the same occupation involves fewer non-routine analytical tasks there [P]. Any LLM rubric applied to generic occupation text will share that bias.

---

## 1. ILO

### 1.1 Gmyrek et al. (2025), *Generative AI and Jobs: A Refined Global Index of Occupational Exposure*, ILO Working Paper 140, published 20 May 2025 [P]
- PDF: https://www.ilo.org/sites/default/files/2025-05/WP140_web.pdf (local copy `ilo_wp140_2025.pdf`). Landing page: https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure
- **Occupation-level data obtained.** Annex Table A1 (pp.48–62, PDF pp.51–65) lists every ISCO-08 4-digit occupation with its mean task score, SD and exposure category. I parsed it into `data/ai_exposure/ilo_isco08_scores.csv`:
  - 427 rows. 112 are "exposed": G4 13, G3 38, G2 44, G1 17. The rest are Minimal Exposure (84) and Not Exposed (231). This matches the paper's count of "112 occupations identified as exposed" (p.43).
  - Script: `scripts/ai_exposure/parse_ilo_wp140_tableA1.py`. Column `pdf_page` gives the PDF page; the printed page is pdf_page − 3.
  - The scores measure **GenAI task automation potential on a 0–1 scale**, averaged over tasks. That is a different concept from Karpathy's 0–10 "how much will AI reshape the job", which includes augmentation. Expect professional jobs to sit relatively higher on Karpathy's scale.
  - Titles are reproduced as printed, including source typos such as "Systems Aministrators" and "Government Regulatory AssociatePprofessionals".
  - In 4 rows (1311, 1323, 3154, 5245) the rounded mean/SD printed in the table would map to "Not Exposed" under the Table 5 rule, but the paper labels them "Minimal Exposure". This is a boundary-rounding effect, and I kept the paper's label.
  - The table has 427 codes against ISCO-08's 433 civilian unit groups. Codes not listed need a fallback, such as the 3-digit mean.
- Task-level scores are published as an interactive tree at https://pgmyrek.github.io/2025_GenAI_scores_ISCO08/ (cited on p.37). I found no downloadable data file there or on the ILO page.
- **Gradient definitions** (Table 5, p.38), where μ is the mean task score and σ its SD:
  - G4: μ ≥ 0.6 and μ − σ ≥ 0.5
  - G3: 0.5 ≤ μ < 0.6 and μ + σ ≥ 0.5
  - G2: 0.4 ≤ μ < 0.5 and μ + σ ≥ 0.5
  - G1: μ < 0.4 and μ + σ ≥ 0.5
  - Minimal Exposure: μ < 0.5 and μ + σ > 0.4
  - Not Exposed: everything else
- **Most exposed occupations** (G4): data entry clerks (0.70), typists (0.65), accounting/bookkeeping clerks (0.64), statistical/finance/insurance clerks (0.64), securities dealers (0.63), financial analysts (0.62), contact-centre salespersons (0.61), web and multimedia developers (0.60), credit and loans officers (0.60), general office clerks (0.60). Software developers (2512) score 0.53 (G3), applications programmers 0.57 (G3) and accountants 0.51 (G3).
- By ISCO major group, the mean of unit-group means is: clerical (4) 0.54; professionals (2) 0.39; managers (1) 0.36; technicians (3) 0.35; services and sales (5) 0.26; operators (8) 0.20; agriculture (6) 0.16; crafts (7) 0.17; elementary (9) 0.15.
- **Global results** (pp.43–44 and Fig.20 on p.43):
  - World: 24% of employment is in one of the four gradients, and G4 is 3.3%. G4 covers 4.7% of women's employment and 2.4% of men's.
  - HIC: 34% (women 41%, men 28%; G3+G4 17.3%). LIC: 11%.
  - **Lower-middle income** (India's group) [chart labels, Fig.20]: 20% of employment, or 240 million jobs. G1 6.8, G2 9.3, G3 1.9, G4 1.9. Men 20%, women 19%.
  - Asia-Pacific: 22% (G1 7.8, G2 8.0, G3 3.1, G4 3.2).
- **No India-specific estimate is published** in WP140, its research brief (https://www.ilo.org/publications/generative-ai-and-jobs-2025-update) or its interactive article (https://www.ilo.org/resource/article/how-might-generative-ai-impact-different-occupations).
- The authors frame the estimates as an "upper threshold" of exposure and say they do not measure job loss (p.44).

### 1.2 Gmyrek, Berg & Bescond (2023), ILO Working Paper 96, August 2023 [P]
- PDF: https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@dgreports/@inst/documents/publication/wcms_890761.pdf (local copy `ilo_wp96_2023.pdf`).
- **No India-specific number.** India appears only qualitatively:
  - p.38 notes that call-centre work is prominent in India and the Philippines, which dominate the world call-centre industry.
  - p.42 says India and the Philippines are at risk of losing some call-centre work, but that BPO dominance may provide a foundation for new industries.
- **LMIC results** [chart labels, Fig.9a, p.34]: automation potential 1.3% of employment (15 million jobs), augmentation 12.8% (156 million). In the 59-country microdata, augmentation is 14.4% of LMIC employment (p.30).
- The 2025 paper (p.44) reconciles the two versions. Its G4 share of 3.3% replaces the 2023 "automation" share of 2.3%. Gradients 1–3 total 20.5%, against 29.2% for 2023's augmentation plus "big unknown".

### 1.3 Gmyrek, Viollaz & Winkler (2026), *Disruption without Dividend?*, ILO Working Paper 166, 17 March 2026 [P]
- Joint ILO and World Bank background paper for WDR 2026. PDF: https://www.ilo.org/sites/default/files/2026-03/wp166_web.pdf (local copy `ilo_wp166_2026_disruption_without_dividend.pdf`).
- India is in the sample (2022 GLD data, 3-digit occupations; Table A, PDF p.39), but **no India row is reported**.
- Findings directly relevant to the hypothesis:
  - In low- and lower-middle-income countries, GenAI threatens office-based jobs that are a disproportionate share of the "good" skilled jobs there. The authors call this "white-collar bypass" (p.6, PDF p.9).
  - GenAI's first-order effects are "likely to concentrate on middle-class occupations" (p.20, PDF p.23).
  - Conventional exposure measures **systematically overestimate** GenAI's influence in developing countries, because workers there do fewer non-routine analytical tasks within the same occupation (PIAAC/STEP evidence; p.6).
  - Footnote 29 (PDF p.35) cites Betai & Chen (2025): after ChatGPT, outsourced service positions on a large online labour marketplace fell 39% on average and contract value fell 48%. This bears on Indian freelancers and BPO.

### 1.4 Using ILO scores with Indian data
- PLFS records occupation at NCO-2015 **3-digit**, which corresponds one-to-one with ISCO-08 minor groups (per Mishra 2026, p.3). The 4-digit ILO scores therefore need aggregating to 3 digits for PLFS. Mishra uses an unweighted mean.
- **Mishra (2026), arXiv:2606.13314** (v2, 21 Jun 2026; single author; not peer reviewed) [P]. It applies the ILO 2025 index to PLFS 2025 (449,041 employed persons aged 15–65):
  - Survey-weighted mean "high-exposure share" (G3–G4) is **0.038 for all workers and 0.166 for graduates** (Table 1, p.4).
  - Among graduates, upper-caste workers score 0.189, OBC 0.158, SC 0.136 and ST 0.125 (Table 2, p.8).
  - The paper finds exposure carries a wage premium (≈18 log points with the Eloundou index) and calls exposure "a marker of privilege".
  - The ILO-based 3.8% for India closely matches ILO's own LMIC G3+G4 figure (1.9 + 1.9 = 3.8%).

---

## 2. IMF

### 2.1 Cazzaniga et al. (2024), *Gen-AI: Artificial Intelligence and the Future of Work*, IMF SDN/2024/001, January 2024 [P]
- URL: https://www.imf.org/-/media/Files/Publications/SDN/2024/English/sdnea2024001.ashx
- imf.org blocks scripted downloads (Akamai "Access Denied"), so no local copy is saved. I verified the text and figures against an identical copy of the IMF PDF mirrored at wiki.ubc.ca.
- **India: 26% of employment is in high-exposure occupations**, the lowest of the six microdata countries. The US is almost 60%, the UK almost 70% and Brazil 41% (Section II.2, p.8). India is analysed at ISCO 3-digit level from PLFS (fn 4, p.7).
- India's split [chart, Fig.1 panel 2, p.8]: HEHC (high exposure, high complementarity) ≈14%, HELC (high exposure, low complementarity) ≈12%, low exposure ≈74%.
- Country groups: world ~40% exposed; advanced economies 60% (27% HEHC + 33% HELC); EMs 40% (16 + 24); LICs 26% (8 + 18) (p.7–8).
- Why India is low: most Indian workers are craftspeople, skilled agricultural workers or elementary workers, mostly low-exposure (p.8).
- **By demographic group** [chart, Fig.3, p.10]:
  - Education: Indian college graduates ≈75% high exposure, mostly HEHC; middle school or below ≈17%.
  - Sex: men ≈27%, women ≈21%. The IMF attributes India's reversal of the usual pattern to women's agricultural employment (p.10).
- **Income distribution** (p.10):
  - HELC (displacement-risk) employment is broadly flat across income deciles, with a mildly positive slope in EMs.
  - Complementarity rises with income, so AI's gains are likely to accrue to higher earners, "especially in countries such as India".
- Pizzinelli et al. (2023, IMF WP/23/216) is the underlying working paper.

### 2.2 IMF India 2025 Article IV, Country Report No. 25/314 [P]
- Staff report completed 6 Nov 2025; Executive Board discussion 21 Nov 2025. Local copy `imf_india_article4_2025_cr25314.pdf`; URL https://www.imf.org/-/media/files/publications/cr/2025/english/1indea2025003-source-pdf.pdf
- The AI section is Annex IX, "Boosting Productivity and Innovation in India", paras 14–16, pp.80–82:
  - Nearly 60% of companies report active AI deployment. This comes from the IBM Global AI Adoption Index 2023, a survey skewed to large firms. The World Bank's 2026 firm survey gives 23% (§3.2).
  - AI adoption could raise TFP in emerging Asia including India by 0.3–3 pp over a decade (Cerutti et al. 2025).
  - In India, AI exposure is concentrated in services and manufacturing; agriculture has low exposure.
  - Exposure with high complementarity rises sharply with education.
  - The IMF AI Preparedness Index shows gaps in human capital and labour-market policies. Since AI may disrupt labour markets at a fast pace, social protection is needed.
- Annex IX policy recommendations (p.88): harness AI responsibly, with a framework that addresses labour displacement.
- **Not retrieved:** the 2024 Article IV (Country Report 25/054, Feb 2025). Secondary reports say IMF DMD Gita Gopinath told Davos in January 2025 that about 26% of Indian workers could be affected and about 12% face displacement [S: newsarenaindia.com]. That is consistent with the SDN split.
- IMF MD Georgieva at the India AI Impact Summit (Feb 2026) warned of a severe hit to young entrants to India's workforce [S: Mint via telecomlive.in, 21 Feb 2026; no verbatim quote available].

---

## 3. World Bank

### 3.1 South Asia Development Update, October 2025, "Jobs, AI, and Trade" — Chapter 2, "Artificial Intelligence, Real Impact" [P]
- Released 7 Oct 2025. URL: https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf (local copy `wb_sadu_oct2025_full.pdf`).
- Method:
  - Exposure uses Felten-Raj-Seamans (2023), with complementarity from Pizzinelli et al. (2023), on Global Labor Database LFS microdata for 5 SAR countries and 25 other EMDEs.
  - "Exposed" means an above-median composite exposure score (p.32). This is a relative cutoff, so levels are not comparable with ILO gradients.
- **Headline shares** (pp.27, 32–33):
  - 22% of South Asian jobs are exposed, yet they account for **42% of all wage earnings**.
  - 15% of jobs (28% of earnings) are exposed and complementary.
  - 7% are exposed and substitutable, against 15% in other EMDEs.
  - About 70% of exposed jobs are complementary, the highest share of any EMDE region.
  - India and Nepal have the region's lowest exposure (p.33). India has the highest complementary share of exposed jobs in South Asia (p.33). India's exposed share reads ≈21% from Fig.2.4C [chart].
- **Who is exposed** (p.34):
  - Urban more than rural workers.
  - **Men more than women**, the opposite of advanced economies, because of low female labour-force participation skewed toward agriculture.
  - Mid-sized firms most exposed; micro and small firms least.
  - **Informal workers (90% of the workforce): 17% exposed. Formal workers: 60% exposed.**
- **Education, wages and age** (pp.34–35):
  - Raw exposure rises with education and wages.
  - After adjusting for complementarity, the wage relationship becomes U-shaped and the education gradient falls to 40% of its raw size.
  - Complementarity-adjusted exposure peaks for workers aged **21–25**.
- **Job postings** (Lightcast, pp.36–38):
  - GenAI has reduced monthly listings by about **20%** for the most exposed, most substitutable white-collar occupations (p.27).
  - Listings growth after ChatGPT averaged 41% for the most exposed, least complementary occupations, against 96% for the least exposed (p.37).
  - Business-services jobs grew 35% slower and wages fell 8% relative to other jobs (p.38).
  - Postings for secondary-education-only jobs fell **24%** across the interquartile range of exposure, while degree-level postings were unchanged (p.38).
  - Entry-level jobs with a software developer's exposure grew 21% slower than those with an electrician's (p.38).
  - Declines were driven by software developers, call-centre agents, accountants and proofreaders.
  - AI skills carry a 28% wage premium. 5.8% of Indian white-collar listings in 2025 required AI skills, concentrated in Bengaluru, Hyderabad, Pune and Chennai (p.37).
  - On the services-export angle (p.38): if the drop in listings reflects automation by foreign clients, South Asia could be displaced from the global value chain of knowledge work.

### 3.2 Later World Bank material [P]
- **South Asia Economic Update, April 2026** (`wb_saeu_apr2026.pdf`, Box 2.1, PDF p.18): an interquartile-range increase in AI exposure is associated with a 1.5% decline in job postings. The decline is about twice as large for multinational affiliates. Suppliers to AI-exposed foreign firms hired more slowly.
- **South Asia Economic Update, October 2026, "Adopting AI for Growth"** (`wb_saeu_oct2026_adopting_ai_for_growth.pdf`; https://openknowledge.worldbank.org/server/api/core/bitstreams/a3de4d6c-513c-462a-83a0-f8f946954a69/content):
  - About **23% of Indian firms report using AI, against 43% of US firms**. On a sophistication index, Indian adoption is under a third of the US level (Executive Summary p.xiv; ch.2).
  - Repeats the 7% / 15% / 70% figures (ch.2, PDF p.65).
  - Hiring has slowed at firms with highly AI-exposed workforces.
- **WDR 2026 background note: Kruse & Yu, "The AI Exposure of Export-Linked Jobs"** (July 2026; `wb_wdr2026_bgnote_ai_exposure_export_linked_jobs.pdf`):
  - India is a notable outlier. The share of its export-linked jobs at risk of AI substitution is about one-half above what its income predicts, reaching 5–6% (p.4).
  - This reflects specialisation in business-services exports, about 30% of exports in 2024 (fn 3).
  - The authors expect negative within-sector effects but only moderate aggregate employment impact, while exports may keep growing (p.11).
  - This is the closest institutional evidence on the "IT-export-driven" channel.

---

## 4. Government of India and RBI

### 4.1 NITI Aayog Frontier Tech Hub, *Roadmap for Job Creation in the AI Economy*, released 10 Oct 2025, with NASSCOM and BCG [P]
- URL: https://niti.gov.in/sites/default/files/2025-10/Roadmap_for_Job_Creation_in_the_AI_Economy.pdf (local copy).
- **Tech workforce:** 7.5–8 million in 2023, counting tech services plus tech jobs in other sectors.
  - Headwinds scenario: 6 million by 2031.
  - Tailwinds scenario: up to 10 million (p.13, PDF p.22).
  - The foreword (Debjani Ghosh, PDF p.5) states the range as losing 1.5 million or creating up to 4 million jobs by 2031.
  - Elsewhere (PDF p.11) the report says 2 million new jobs "by 2030". The report is internally inconsistent on dates and amounts.
- **Customer service (CX) workforce:** 2–2.5 million in 2023. Headwinds: 1.8 million by 2031. Tailwinds: 3.1 million (p.13).
- The report claims the tech services sector employs "13% of the total workforce and over 30% of the white-collar talent" (PDF p.10). **The 13% is implausible.** 7.5–8 million is about 1.3% of a ~600 million workforce. Do not cite it.
- It cites a "Centre of Advanced Study in India" claim that over 60% of formal-sector jobs are susceptible to automation by 2030 (PDF p.18). This is third-hand and unverified.
- It also cites the IMF as saying 25% of Indian jobs have high exposure, via the Washington Post (PDF p.11). The IMF's own figure is 26%.
- Roles at risk: L1 support agents, junior QA engineers, entry-level software engineers.
- Productivity estimate: 10–20% across the software development lifecycle.

### 4.2 Economic Survey 2025-26, Ch.14, "Evolution of the AI Ecosystem in India: The Way Forward" (29 Jan 2026) [P]
- URL: https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap14.pdf
- Paras 14.14–14.15 (p.556):
  - AI raises the marginal productivity of capital relative to labour in white-collar services.
  - Low-value-added service tasks are at risk.
  - For India, rapid uncalibrated deployment "risks displacing segments of the workforce faster than the economy can reabsorb them".
- Box XIV.1: US evidence of a lower employment elasticity in professional and business services after 2022.
- Para 14.55 (p.573): proposes an AI Economic Council to "calibrate the pace of AI adoption" and map which jobs and geographies will be affected.

### 4.3 Economic Survey 2024-25, Ch.13, "Labour in the AI Era: Crisis or Catalyst?" (31 Jan 2025) [P]
- URL: https://www.indiabudget.gov.in/budget2025-26/economicsurvey/doc/eschapter/echap13.pdf
- Para 13.11 (p.415): an IIM Ahmedabad survey found 68% of white-collar employees expect partial or full automation of their jobs within 5 years, and 40% fear their skills becoming redundant.
- **Para 13.14 (p.416)** is the closest official statement to the hypothesis:
  - A significant share of the IT workforce is in low-value-added services most susceptible to automation.
  - India is a consumption-based economy, so a displacement-driven fall in consumption "is bound to have macroeconomic implications".
- Para 13.46 (p.425) is the counterweight: exposure of medium- and high-skill jobs may be lower than some estimates suggest.

### 4.4 RBI
- **Deputy Governor Poonam Gupta**, press interaction in Mumbai, ~6 Feb 2026 [S: India TV News, 7 Feb 2026]:
  - An RBI survey found no negative employment effect so far.
  - Productivity gains were "good to high".
  - Managing churn and transition is the challenge.
  - RBI has not published the survey's methodology as far as I could find.
- RBI Bulletin items, May and Aug 2026 (AI and jobs uncertainty; Governor's remarks on back-office automation in banks): surfaced in search, but rbi.org.in served a CAPTCHA, so they are **not verified**. I did not attempt to bypass it.
- Former Governor **Raghuram Rajan**:
  - Feb 2026: disruption to services, but large-scale displacement unlikely [S: Mint/menafn].
  - Aug 2026 Project Syndicate column: proposes a tax on corporate AI token use, partly because governments are "cash-strapped" [S: BusinessToday, 20 Aug 2026].

### 4.5 MeitY
- IT Secretary **S. Krishnan** (PTI interview, 25 Dec 2025) [S: careers360/PTI]: risk to cognitive jobs is less serious in India than in the West, because white-collar jobs are a much smaller share of employment and are mostly in STEM. This is effectively the official version of "less red overall".

---

## 5. Industry, consultancies and AI-usage data

| Source | Date | India numbers | Notes |
|---|---|---|---|
| **NASSCOM Strategic Review 2026** [P] | 24 Feb 2026 | FY26E revenue $315bn (+6.1%), exports $246bn. Direct tech employment **~6.0 mn vs 5.8 mn in FY25, +2.3%, net +135,000**. AI revenue $10–12bn. 2 mn+ upskilled in AI. | Exec summary p.10; press release p.1. Hiring shifting "from volume to skill mix". Local copies saved. |
| **EY India, "AIdea of India: 2025"** [P, press release] | 14 Jan 2025 | GenAI could "transform" **38 mn jobs by 2030**. 24% of tasks fully automatable, 42% augmentable. Productivity +2.61% (organised sector) plus 2.82% (unorganised). Task-level productivity: call centre 80%, software development 61%, IT/ITeS ~19%. | https://www.ey.com/en_in/newsroom/2025/01/unlocking-productivity-gains-gen-ai-to-transform-38-million-jobs-by-2030-ey-india. Based on 10,000+ tasks and ~125 CXOs. Not a job-loss estimate. |
| **ServiceNow / Pearson** [P, press release] | 13 Nov 2024 | Workforce 423.73 mn (2023) → 457.62 mn (2028). **2.73 mn new tech jobs by 2028.** Retail +6.96 mn. | Local copy `servicenow_pearson_india_ai_jobs_2024_press.pdf`. Vendor-commissioned. |
| **Indeed Hiring Lab** [S] | May & Sep 2025 | 1.5% of Indian postings mentioned GenAI (May 2025). 11.7% mentioned AI (Sep 2025, up from 8.2% a year earlier); India second after Singapore. | Press coverage of Hiring Lab India updates. Indeed notes its India data skews to tech. |
| **McKinsey Global Institute**, "Jobs lost, jobs gained" [S] | Dec 2017 | 9% of Indian work hours automatable by 2030 (midpoint), 19% (rapid). | Pre-GenAI. No GenAI-era India estimate found. |
| **BCG** | n/a | Co-author of the NITI roadmap (§4.1). | No separate BCG India exposure number found. |
| **Anthropic Economic Index, Sep 2025 report** [P] | Sep 2025 | India has **7.2% of global Claude.ai usage**, second to the US's 21.6% (p.13). Per-capita AUI **0.27** (p.3). **Coding is over half of Indian usage**, against about a third globally (p.12). India's overrepresented requests are almost all software development (p.23). | Local copy `anthropic_economic_index_sep2025.pdf`. |
| **Anthropic India Country Brief** [P, web] | 16 Feb 2026 | **5.8%** of global Claude.ai use (Nov 2025 data, N = 58,098). Rank 101/116 per capita. **45.2% of tasks software-related, highest in the world.** 51.3% work-related vs 46% globally. Maharashtra 15.5%, Tamil Nadu 13.2%, Karnataka 12.7%, Delhi 10.5%. | https://www.anthropic.com/research/india-brief-economic-index. Shows AI use in India is concentrated in the IT workforce, consistent with the hypothesis. |
| **Microsoft AI Diffusion Report Q1 2026** [P] | May 2026 | Share of India's working-age population using AI: **14.2% (H1 2025) → 15.7% (H2 2025) → 17.6% (Q1 2026)**. Global 17.8%; Global North 27.5%, South 15.4%. | PDF p.18 table; p.2. Telemetry-based model. A secondary source gives 18.5% for Q2 2026 (unverified). |
| **IBM Global AI Adoption Index 2023**, via IMF | 2023 | ~60% of Indian companies actively deployed AI. | Large-firm sample. Contrasts with the World Bank's 23% firm survey. |

---

## 6. Real-world impact evidence, 2024–2026

### 6.1 IT services headcount and hiring
- **TCS**
  - July 2025: TCS announced it would release about **2% of its global workforce (~12,000)**, mainly mid and senior grades.
  - The CEO said the cause was skill mismatch and deployability, **not** AI productivity gains of around 20% [S: Business Today, 28 Jul 2025; Moneycontrol interview, 21 Jul 2025].
  - Reported headcount path [S: Zee Business, The Federal, Business Today citing TCS disclosures]:

    | Date | Headcount | Change |
    |---|---|---|
    | Mar 2025 | 607,979 | |
    | Jun 2025 | 613,069 | |
    | Sep 2025 | 593,314 | −19,755 in the quarter |
    | Dec 2025 | 582,163 | |
    | Mar 2026 | 584,519 | +2,356 in the quarter |

  - FY26 net change: **−23,460**.
  - Fresher offers for FY27: 25,000, against 44,000+ hired in FY26 [S: Business Today, 13 Apr 2026].
- **Top-5 Indian IT firms, FY26** [S: Anand Rathi via CNBC, 30 Apr 2026]:
  - Net headcount fell about 7,000. Other secondary tallies give −6,981 and −7,389.
  - Gross hiring was about 170,000, against a 5-year average of about 230,000.
- **Infosys** plans about 20,000 freshers in FY27 [S].
- **NASSCOM**: the sector as a whole was still a net hirer in FY26 (+135k), see §5. Mid-tier firms, GCCs and ER&D are growing while the big five shrink.
- **UnearthInsight** (Gaurav Vasu) [S: Reuters, 8 Aug 2025]:
  - 400,000–500,000 IT professionals are at risk of layoffs over 2–3 years.
  - About 70% of them have 4–12 years of experience.
  - The sector employed 5.67 mn in March 2025 and accounts for over 7% of GDP.
- **CEO quotes**
  - HCLTech CEO C. Vijayakumar, NASSCOM Technology and Leadership Forum, 24 Feb 2025: HCL is challenging teams to generate twice the revenue with half the workforce, and calls the linear headcount model obsolete [S: Business Standard/Reuters]. At Davos in Jan 2026 he said AI-led productivity may deliver 3–5% growth without adding staff [S: BusinessToday].
  - NASSCOM president Rajesh Nambiar, per a secondary report of a Nikkei interview: entry-level coding and testing are being automated [S, low reliability].
- **ICRIER, "AI and Jobs: This Time Is No Different"** (Feb 2026) [P]
  - Local copy `icrier_ai_and_jobs.pdf`. Acknowledges OpenAI support.
  - Survey of 651 IT firms in 10 cities, Nov 2025–Jan 2026:
    - No evidence of large-scale job losses (p.8).
    - **55% of firms report fewer entry-level jobs** and 35% more; 42% report more mid-level jobs; 82% report no change at senior level (p.16).
    - 32% name data entry and clerical work as the most affected roles.
    - On future employment, 44% expect no change, 28% growth and 27% decline (p.9).
- **Kotak Institutional Equities** [S]
  - Mar 2026 strategy note (Sanjeev Prasad): the average IT worker earns 3–4x the average Indian worker, but an IT slowdown would have a moderate aggregate effect.
  - Aug 2026: AI-driven revenue deflation of 3–3.5% a year in Indian IT services through FY2028.

### 6.2 Naukri JobSpeak (new postings; Info Edge) [P]
Local copies `naukri_jobspeak_sep2026.pdf` and `naukri_jobspeak_oct2026.pdf`.

| | Overall | IT / software services | BPO / ITES | AI/ML | Freshers (0–3 yrs) |
|---|---|---|---|---|---|
| **Sep 2026** (p.2, p.4) | +2% YoY (index 3,053) | **−4%** | +4% (GCC +59%) | **+20%** | +1% |
| **Oct 2026** (p.2, p.4, p.8) | +14% YoY, partly a weak festive base in Oct 2025 | +5% (index 3,119) | +17% | +32% | +15% |

- Methodology caveat (p.7): the index now includes free listings, which gives a "transient uplift". Long-run comparisons with pre-2025 levels are not like-for-like.

### 6.3 BPO, contact centre, content and translation, banking back office
- **Contact centre**
  - ILO gives contact-centre salespersons G4 (0.61) and contact-centre information clerks G3 (0.58).
  - World Bank SADU names call-centre agents among the occupations driving the post-ChatGPT drop in postings (p.37).
  - The NITI CX scenarios are in §4.1.
  - Naukri BPO/ITES postings are still growing, driven by GCCs.
- **Online outsourcing:** the Betai & Chen result (−39% positions, −48% contract value after ChatGPT) is in §1.3.
- **Content and translation:** ILO puts translators at 0.59 (G3), authors 0.55 and journalists 0.54. World Bank flags proofreaders. **I found no India-specific quantitative evidence.** This is a gap.
- **Banking back office:**
  - ILO scores bank tellers 0.58 (G3) and credit officers 0.60 (G4).
  - EY projects 34–38% productivity improvement in Indian banking by 2030 [S].
  - The RBI Governor's August 2026 remarks on back-office automation are unverified (§4.4).
  - **I found no hard India headcount evidence.** This is a gap.

### 6.4 Pre-GenAI causal evidence for India
- Copestake, Marczinek, Pople & Stapleton, "AI and Services-Led Growth: Evidence from Indian Job Adverts" (STEG WP, March 2023; summary at https://www.ideasforindia.in/topics/productivity-innovation/ai-and-services-led-growth-evidence-from-indian-job-adverts.html, 19 Apr 2023) [P, summary page]. Data are Naukri postings, 2010–2019.
  - An establishment's 1% higher AI-vacancy growth goes with **3.61 pp lower non-AI vacancy growth**.
  - Effects are strongest for **managers and professionals**.
  - AI jobs pay a 13–17% premium and are concentrated in 6 metros and large firms.
- This is direct evidence that AI substitutes for high-skill white-collar demand in India.

---

## 7. Who has argued AI threatens India's tax base, middle class or IT-driven consumption

**Explicit income-tax-base arguments:** I found **none** from the CEA, RBI, a brokerage or a peer-reviewed source that quantifies AI's effect on India's income-tax base.

The nearest arguments (short quotes; everything else paraphrased):

1. **Economic Survey 2024-25, para 13.14, p.416** (Ministry of Finance, 31 Jan 2025) [P]. India is consumption-based, and displacement-driven falls in consumption are "bound to have macroeconomic implications". It also says low-value-added IT work is the most susceptible.
2. **Economic Survey 2025-26, para 14.15, p.556** (29 Jan 2026) [P]. Uncalibrated AI deployment risks displacing workers faster than the economy can reabsorb them.
3. **Marcellus Investment Managers** (Nandita Rajhansa & Saurabh Mukherjea), blog of 1 Aug [2025] [P, web]: https://marcellus.in/blogs/white-collar-jobs-growth-and-wage-growth-twin-drivers-of-indias-slowdown/
   - Defines India's middle class as about 40 million people reporting **Rs 5 lakh–1 crore in income-tax returns**.
   - Says each supports roughly 5 other jobs (about 200 million in all; no source given).
   - Attributes the slowdown in white-collar jobs and wages to AI and automation, and says it is behind a consumption slowdown.
   - Mukherjea has also publicly said up to 40 million middle-class jobs are at risk over a decade [S: podcast coverage].
   - A Marcellus piece of 9 Mar [2026] says the IT sector now hires fewer than 0.5 mn a year, against over 1 mn previously, and links this to a structural consumption slowdown [P, web].
   - **This is the closest to the "tax-paying middle class" framing.**
4. **Bernstein**, open letter to PM Modi (Venugopal Garre & Nikhil Arela, 23 Apr 2026) [S: Business Standard, CNBC, Moneylife]. The 10–15 mn IT services, GCC and BPO workforce forms the base of India's "aspirational middle class", and GenAI "challenges that template". It also warns India risks becoming a "permanent consumer" of AI.
5. **GlobalData TS Lombard** (Shumita Sharma Deveshwar), quoted by CNBC on 30 Apr 2026 [S]. Without job creation, India's consumption-led economy will struggle.
6. **Reuters analysis** (8 Aug 2025) [S]. Describes the IT sector's role in building the middle class and its "cars-to-homes" consumption multiplier. UnearthInsight warns layoffs may hit tourism, luxury and real-estate demand.
7. **Kotak Institutional Equities** (Mar 2026) [S]. IT workers earn 3–4x the average, so slower IT hiring or pay growth matters for urban consumption. Kotak judges the aggregate impact moderate.
8. **IMF SDN 2024** [P]. AI gains accrue disproportionately to higher earners, especially in India. This is a distributional argument rather than a fiscal one.
9. **ILO WP166** [P]. GenAI's first-order effects concentrate on middle-class occupations, and LMICs face "white-collar bypass".
10. **Rajan** (Aug 2026) [S]. Proposes a tax on AI token use, partly on revenue grounds. He frames it generally, not as an Indian tax-base argument.

**Counter-arguments**
- **IT Secretary S. Krishnan** (25 Dec 2025, PTI) [S]: India's low white-collar share means lower cognitive-job risk than in the West.
- **RBI DG Poonam Gupta** (Feb 2026) [S]: no negative employment effect so far.
- **ICRIER** (Feb 2026; OpenAI-supported) [P]: "this time is no different"; employment growth has moderated but not reversed.
- **NASSCOM** (Feb 2026) [P]: the sector is still a net hirer at +2.3%.
- **World Bank SADU** [P]: about 70% of South Asia's exposed jobs are complementary, and India has the highest complementary share in the region.
- **World Bank WDR note** [P]: only moderate aggregate employment effects, and exports may keep growing.
- **Kotak** [S]: informal-sector dominance limits economy-wide employment effects.
- **Economic Survey 2024-25, para 13.46** [P]: exposure of skilled jobs may be overstated.
- **Rajan** (Feb 2026) [S]: large-scale displacement unlikely.
- **Oxford Economics** (Alexandra Hermann Prasad, CNBC Apr 2026) [S]: not all jobs are at risk.
- **ILO WP166** [P]: exposure indices overstate developing-country exposure.

---

## 8. Karpathy's project and existing replications
- **karpathy/jobs** (local clone `C:\Users\hp\Downloads\xyz\karpathy_jobs`; prompt.md "Aggregate statistics")
  - 342 BLS OOH occupations, 143.1 million jobs, $8.9 trillion in wages.
  - **Job-weighted mean exposure 4.9/10.**
  - Scores 6–10 cover 41.9% of jobs and 51.9% of wages. Scores 8–10 cover 17.6% of jobs.
  - Mean exposure by pay band: under $35k 3.4, over $100k 6.7. By education: Bachelor's 6.7, no degree or high school 4.1.
- **Karpathy's own statements**
  - Launched around 15 Mar 2026 [S: aihola, 16 Mar 2026].
  - In an X reply he called it a "saturday morning 2 hour vibe coded project" meant to help others explore BLS data (x.com/karpathy/status/2033229482316992999).
  - He took the site down, saying it had been widely misinterpreted. He added that the "exposure" score was an LLM rating of how digital the job is, and had no bearing on what will actually happen, which depends on demand elasticity and more (as quoted by Futurism, 18 Mar 2026 [S]).
  - The README disclaimers (it does not predict job loss and ignores demand elasticity) are in the local repo [P].
  - Reports on whether the site and repo were later reinstated conflict [S].
- **India replications**
  - **github.com/Gokulakrishnxn/Jobs**
    - Data: NCO-2015 occupations; Census 2011 B-25A counts rescaled to PLFS 2023-24 shares; PLFS 2023-24 pay anchors.
    - Scoring: Gemini with the same rubric.
    - Coverage: 367 occupations, about 362.5 mn workers.
    - No hosted demo and no published aggregate results. Repo readme, accessed 9 Nov 2026 [P, web].
  - **github.com/Laksh-star/india-jobs-ai-exposure**
    - Uses NCO-2004 3-digit groups, with 28 canonical rows.
    - The default build runs on seed or approximate data.
    - Demo at laksh-star.github.io/india-jobs-ai-exposure [P, web].
  - Several blog-level "India AI job maps" exist (e.g. dharmendraasimi.com, 25 roles). They are not data-based.
- **Other replications:** llmxlabs/karpathy-jobs, a US archive and extension. **I found no other country replications** (UK, Canada and others), though my searches were limited.
- **Critique:** CSEP (TG Srinivasan, 20 Mar 2026, https://csep.org/blog/which-jobs-are-at-risk-from-ai-evaluating-karpathys-exposure-dashboard/) calls the tool an exploratory heuristic, not a causal model. It recommends an equivalent analysis for India's non-farm labour market.

---

## 9. Suggested cross-validation targets for our India scoring

Machine-readable version: `data/ai_exposure/india_ai_exposure_benchmarks.csv`.

1. **Rank correlation.** Join our NCO-coded Karpathy-style scores to `ilo_isco08_scores.csv` and compute the Spearman correlation with `mean_score`.
   - Expect a high correlation for clerical occupations and a weaker one for professionals and managers. ILO measures automation; Karpathy's score includes augmentation and "reshaping".
   - Flag occupations where our LLM score is 7+ but ILO is "Not Exposed", and the reverse.
2. **Employment-weighted aggregates** should land in the same broad range as the benchmarks:
   - IMF India: 26% high exposure (14% HEHC / 12% HELC).
   - World Bank: about 21% of Indian jobs exposed on an above-median definition, carrying a far larger share of wages (42% for South Asia).
   - ILO: 20% of LMIC employment in any gradient, 3.8% in G3+G4. The ILO-on-PLFS preprint also gives 3.8%.
   - A rough inference of my own, not from any source: US Karpathy 6+ (42%) is about 0.7x the IMF US figure (60%). The same ratio applied to India's 26% suggests roughly 15–20% of Indian employment at Karpathy 6+. The job-weighted mean should be well below the US 4.9.
3. **Distribution checks.** Exposure should rise steeply with education, PLFS wage and formality. World Bank: formal 60% vs informal 17%. IMF: graduates about 75%. Men should be more exposed than women.
4. **LLM bias check (ILO WP166).** Indian jobs within the same occupation title contain fewer non-routine analytical tasks. If the rubric reads generic occupation descriptions, consider adding India-specific task context, or treat our scores as an upper bound.

---

## 10. Gaps and caveats
- **No official India-specific ILO gradient shares** (by sex or overall) are published. WP140 and WP166 use Indian microdata internally but report only income-group and regional aggregates. The ILO-on-PLFS figure comes from a single-author preprint.
- **IMF:** the 2024 Article IV (CR 25/054) text was not retrieved. The SDN PDF could not be saved from imf.org because of an Akamai block; I verified it against an identical mirror copy and did not store that copy. India's HEHC/HELC and education/sex splits are chart reads.
- **RBI** Bulletin and speech texts were behind a CAPTCHA and are unverified. The RBI firm survey Poonam Gupta cited has not been published with numbers.
- **Brokerage notes** (Kotak, Bernstein, Jefferies, TS Lombard, Anand Rathi) are paywalled, so only press summaries were used. I found nothing from Jefferies on this theme.
- **No source quantifies AI exposure of income-tax payers.** This is the key open link for the hypothesis and should be built by joining tax and occupation data with our scores.
- **Company headcounts** (TCS, top-5 IT) come from press reports of company disclosures, not the filings themselves.
- There is little India-specific hard evidence for content/translation and banking back-office impacts.
- **McKinsey** has no GenAI-era India estimate; its 2017 numbers are pre-GenAI and secondary. **BCG** has no standalone India estimate. **Indeed** India figures come from press coverage.
- **Naukri JobSpeak** levels are affected by the 2025–26 methodology change (free listings).
- **NITI roadmap** internal inconsistencies: 2 mn vs 4 mn jobs, 2030 vs 2031, and the implausible "13% of total workforce" claim.
- The Microsoft Q2 2026 India figure (18.5%) is secondary and unverified.

## 11. Files
- `data/ai_exposure/ilo_isco08_scores.csv`: ILO WP140 Table A1, 427 ISCO-08 unit groups. Columns: isco08_code, title, mean_score, sd, gradient, source_url, pdf_page.
- `data/ai_exposure/india_ai_exposure_benchmarks.csv`: benchmark numbers with sources.
- `data/raw/ai_exposure/*.pdf` (20 files) and `data/raw/ai_exposure/_manifest.csv` (URL, publisher, date, SHA-256).
- `scripts/ai_exposure/`:
  - `parse_ilo_wp140_tableA1.py`: Table A1 to CSV, with a check against the gradient rule.
  - `pdf_text.py`: text dump.
  - `render_pages.py`: page images, used for chart reads.
  - `make_manifest.py`: builds the manifest.
