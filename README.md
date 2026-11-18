# India Job Market Visualizer

An India replication of Andrej Karpathy's [US Job Market Visualizer](https://karpathy.ai/jobs/)
([github.com/karpathy/jobs](https://github.com/karpathy/jobs)), plus an analysis of one question:
**are India's AI-exposed jobs the same small group that pays India's income tax?**

- Website: `site/index.html` (open directly in a browser). A private published copy is at https://claude.ai/artifact/V7gVHjhNMqiUXQxm1YdMiv
- Built November 2026 from PLFS January–December 2025 unit-level data and CBDT/Budget tax statistics.

## Headline results

| | India (this project) | US (Karpathy) |
|---|---|---|
| Workers covered | 61.6 crore, 127 NCO-2015 groups | 14.3 crore, 342 BLS occupations |
| Average AI exposure, job-weighted (0–10) | **1.8** | 4.9 |
| Average AI exposure, earnings-weighted | 2.7 | 5.4 |
| Workers in jobs scoring 7+ | **3.9%** | 34.3% |
| Workers in jobs scoring 0–1 | 72% | 4.4% |
| Average exposure, weighted by income tax paid | **5.9** | n/a |

**Checking the claim, piece by piece**

1. *"India will show much less red."* **True.** Farming, construction and labour dominate India's
   workforce. 72% of workers are in occupations scoring 0–1.
2. *"Most tax is paid by the top ~2%."* **True for personal income tax, not for tax overall.**
   - Concentration (CBDT AY 2023-24):
     - The top 2% of a 60-crore workforce pay about **93%** of individual income tax.
     - The top 1% of adults pay about **89%**.
     - About 10 lakh returns pay half of it.
   - But individual income tax is only about **26% of the Centre's gross tax revenue** and about **16% of
     centre-plus-state taxes**. GST, excise and customs are around 41% of central revenue and are paid far
     more widely. Corporate tax is about 26%.
3. *"Those 2% are the jobs in red."* **Largely true.**
   - Occupations scoring 6+ are 5.9% of workers and pay an estimated **51%** of individual income tax.
   - That rises to **73%** if the corporate heads inside "Managing directors & chief executives" are scored
     like corporate managers. In India that group is 95% self-employed shop owners, so it scores 4.5 overall.
   - Occupations scoring 4+ are 12% of workers and pay **93%**.
   - Biggest payers:
     - Business owners/CEOs (22%)
     - Software developers (13%, score 9)
     - Doctors (11%)
     - Business and admin managers (8.5%)
     - Sales/marketing managers (7%)
     - University teachers (6%)
     - Finance professionals (3%)
4. *"So AI is a danger to the tax base."* **A real but bounded risk.**
   - Income tax is progressive: on CBDT's actual income distribution, a 10% fall in income cuts tax about 15%.
   - So a 10% earnings fall in the 6+ occupations would cut individual income tax by about **7.8%**,
     roughly ₹0.85 lakh crore a year at the FY 2025-26 revised estimate.
   - Exposure is not job loss, though. Software employment still grew in FY 2025-26, and productivity gains
     could raise the base instead.

The AI-exposed workforce is the formal, salaried, educated slice of India:
- In jobs scoring 7+, 87% of workers are regular salaried, 66% are formal (salaried with social security) and
  79% are graduates.
- Across all workers, those figures are 24%, 11% and 15%.

## What Karpathy's repo contains (and what was reused)

- **Data:** BLS Occupational Outlook Handbook. 342 occupation pages were scraped with Playwright (non-headless
  because BLS blocks bots), parsed to Markdown, then tabulated: pay, entry education, jobs 2024, 2024–34 outlook.
- **Scoring:** `score.py` sends each occupation page to Gemini Flash (via OpenRouter, temperature 0.2). The
  rubric is a 0–10 "Digital AI Exposure" scale whose key signal is whether the work product is fundamentally
  digital.
  - Anchors: roofer 0–1, electrician 2–3, nurse 4–5, teacher/manager 6–7, software developer 8–9, data entry 10.
- **Site:** `site/index.html`, a squarified canvas treemap. Area = jobs, grouped by BLS category. Four colour
  layers: Outlook, Median pay, Education, AI exposure, each with a stats row.
- **US results** (recomputed from his `data.json`):
  - 143M jobs and $8.9T in wages.
  - Job-weighted exposure 4.9, wage-weighted 5.4.
  - 34.3% of jobs and 41.1% of wages are in occupations scoring 7+.
  - Exposure rises with pay, from 3.4 below $35K to 6.7 at $100K+.
- **Caveat he states:** a high score does not predict job loss. It ignores demand elasticity, regulation and
  social preferences.
- **Reused here:**
  - The rubric, verbatim. Only the sentence naming the data source was changed (`scripts/main/make_rubric.py`).
  - The treemap layout and colour code.
  - The page-per-occupation scoring approach.

## Data and method

| Step | Script | Notes |
|---|---|---|
| Convert PLFS JSON to parquet | `scripts/main/json_to_parquet.py` | 1,148,634 persons, 270,472 households (match MoSPI README) |
| Validate | `scripts/main/validate.py` | Reproduces MoSPI 2025: LFPR 59.3, WPR 57.4, UR 3.1, regular/self/casual 23.6/56.1/20.2 |
| Occupation stats | `scripts/main/build_occupations.py` | Usual status 15+, NCO-2015 3-digit; CWS earnings; formality; tax under FY2025-26 slabs |
| Occupation pages | `scripts/main/make_pages.py` | NCO-2015 description + families + job titles + PLFS stats → `data/pages/*.md` |
| AI exposure | Claude agents, two independent passes | `data/scores/pass_*.json`; 76% exact agreement, 98% within 1 point, r = 0.98; r = 0.91 with ILO 2025 GenAI index |
| Tax by occupation | `scripts/main/tax_by_occupation.py` | CBDT AY2023-24 income distribution × today's slabs; split salary/non-salary; allocated by PLFS occupational mix of high earners |
| Elasticity / stress | `scripts/main/itr_elasticity.py`, `stress_test.py` | Elasticity ≈ 1.55 on CBDT distribution |
| Site | `scripts/main/build_site_data.py`, `build_site.py` | `site_src/template.html` → `site/index.html`, `site/artifact.html` |

**Scaling.** The weights in the PLFS 2025 survey sum to 51.9 crore usual-status workers aged 15+. Counts are
scaled to MoSPI's published estimate of 61.6 crore workers aged 15+ (PLFS AR 2025, Statement 32; factor 1.188). Occupation-division shares match MoSPI Table 25 within 0.01 points. Shares are unaffected.

**Why there is no "Outlook" layer.** India publishes no BLS-style occupational projections. PLFS also switched
from NCO-2004 to NCO-2015 in 2021-22 and changed its sample design in 2025. ILOSTAT's 2-digit occupation series
breaks at 2022 and shows 2024→2025 jumps caused by the redesign. The layer is replaced with Formal jobs.

**Known limitations**
- **Survey vs tax records.** PLFS barely samples very high earners: 18 people above ₹50 lakh. Tax shares
  therefore come from CBDT totals, with PLFS used only for the occupational mix inside each income band. That
  mix is thin above ₹20 lakh, with a few hundred observations.
- **Heterogeneous groups.** Some NCO 3-digit groups mix very different jobs:
  - 112 business owners/CEOs.
  - 441 postmen with proof-readers.
  - 524 call-centre staff with petrol-pump attendants.

  Scores reflect the dominant Indian sub-group.
- **Usage rider.** MoSPI says PLFS unit data is meant for employment and unemployment indicators. Earnings and
  formality are PLFS employment variables. The tax figures are this project's estimates.
- **Data vintage.** The latest published CBDT income-range distribution is AY 2023-24 (incomes of 2022-23). The
  post-2025 regime is modelled by applying today's slabs to that distribution.

## Research files

`research/`:
- `tax.md`: who pays India's taxes, with every figure sourced
- `ai_exposure.md`: ILO, IMF, World Bank, NITI, industry evidence
- `nco_framework.md`: NCO-2015 and ILOSTAT
- `informal_sectors.md`: WRRI wages, e-Shram, ASI, ASUSE, MGNREGA
- Further reports from the PLFS, formal-sector and tax-linkage agents, where present

Tidy CSVs are in `data/<topic>/`. Raw downloads are in `data/raw/`.

## Rebuild

```
.venv/Scripts/python -I scripts/main/json_to_parquet.py .
.venv/Scripts/python -I scripts/main/build_occupations.py .
.venv/Scripts/python -I scripts/main/make_pages.py .
.venv/Scripts/python -I scripts/main/tax_by_occupation.py .
.venv/Scripts/python -I scripts/main/itr_elasticity.py
.venv/Scripts/python -I scripts/main/build_site_data.py .
.venv/Scripts/python -I scripts/main/build_site.py .
```
