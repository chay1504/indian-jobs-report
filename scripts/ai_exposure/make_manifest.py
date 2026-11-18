"""Write data/raw/ai_exposure/_manifest.csv: file, bytes, sha256, source_url, publisher, title, pub_date, accessed.
Usage: python -I make_manifest.py <raw_dir>"""
import sys, os, hashlib, csv
raw = sys.argv[1]
META = {
 "ilo_wp140_2025.pdf": ("https://www.ilo.org/sites/default/files/2025-05/WP140_web.pdf", "ILO", "Generative AI and Jobs: A Refined Global Index of Occupational Exposure (WP140)", "2025-05-20"),
 "ilo_wp96_2023.pdf": ("https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@dgreports/@inst/documents/publication/wcms_890761.pdf", "ILO", "Generative AI and Jobs: A global analysis of potential effects on job quantity and quality (WP96)", "2023-08"),
 "ilo_wp166_2026_disruption_without_dividend.pdf": ("https://www.ilo.org/sites/default/files/2026-03/wp166_web.pdf", "ILO / World Bank", "Disruption without Dividend? (WP166)", "2026-03-17"),
 "imf_india_article4_2025_cr25314.pdf": ("https://www.imf.org/-/media/files/publications/cr/2025/english/1indea2025003-source-pdf.pdf", "IMF", "India: 2025 Article IV Consultation, Country Report No. 25/314", "2025-11"),
 "wb_sadu_oct2025_full.pdf": ("https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf", "World Bank", "South Asia Development Update Oct 2025: Jobs, AI, and Trade", "2025-10-07"),
 "wb_saeu_oct2026_adopting_ai_for_growth.pdf": ("https://openknowledge.worldbank.org/server/api/core/bitstreams/a3de4d6c-513c-462a-83a0-f8f946954a69/content", "World Bank", "South Asia Economic Update Oct 2026: Adopting AI for Growth", "2026-10"),
 "wb_saeu_apr2026.pdf": ("https://thedocs.worldbank.org/en/doc/3eba06287709efbfb29bd02c5df93370-0310012026/original/SAEU-April-2026.pdf", "World Bank", "South Asia Economic Update Apr 2026: Working with Industrial Policy", "2026-04-08"),
 "wb_wdr2026_bgnote_ai_exposure_export_linked_jobs.pdf": ("https://thedocs.worldbank.org/en/doc/9df559d23a6d80b3dfa2c4bc808f3a20-0050062026/original/The-AI-Exposure-of-Export-Linked-Jobs.pdf", "World Bank (Kruse & Yu)", "The AI Exposure of Export-Linked Jobs (WDR 2026 background note)", "2026-07"),
 "niti_roadmap_job_creation_ai_economy_oct2025.pdf": ("https://niti.gov.in/sites/default/files/2025-10/Roadmap_for_Job_Creation_in_the_AI_Economy.pdf", "NITI Aayog (with NASSCOM, BCG)", "Roadmap for Job Creation in the AI Economy", "2025-10-10"),
 "economic_survey_2025_26_ch14_ai.pdf": ("https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap14.pdf", "Ministry of Finance, GoI", "Economic Survey 2025-26 Ch.14 Evolution of the AI Ecosystem in India", "2026-01-29"),
 "economic_survey_2024_25_ch13_labour_ai.pdf": ("https://www.indiabudget.gov.in/budget2025-26/economicsurvey/doc/eschapter/echap13.pdf", "Ministry of Finance, GoI", "Economic Survey 2024-25 Ch.13 Labour in the AI Era: Crisis or Catalyst?", "2025-01-31"),
 "anthropic_economic_index_sep2025.pdf": ("https://assets.anthropic.com/m/218c82b858610fac/original/Economic-Index.pdf", "Anthropic", "Anthropic Economic Index report: Uneven geographic and enterprise AI adoption", "2025-09"),
 "microsoft_ai_diffusion_2026_q1.pdf": ("https://www.microsoft.com/en-us/research/wp-content/uploads/2026/05/Microsoft-AI-Diffusion-Report-2026-Q1.pdf", "Microsoft AI Economy Institute", "Global AI Diffusion Q1 2026 Trends and Insights", "2026-05"),
 "nasscom_strategic_review_2026_exec_summary.pdf": ("https://nasscom.in/modules/custom/nasscom_general/docs/Nasscom-Strategic%20Review-2026-Executive%20Summary.pdf", "NASSCOM", "Strategic Review 2026 Executive Summary", "2026-02-24"),
 "nasscom_strategic_review_2026_press_release.pdf": ("https://d3r3sr3o54kk15.cloudfront.net/s3fs-public/media_pdf/India%E2%80%99s%20tech%20industry%20continues%20to%20redefine%20AI-led%20transformation,%20efficiency%20and%20skilling--%20Nasscom%20Annual%20Strategic%20Review%202026.pdf", "NASSCOM", "Press release: Annual Strategic Review 2026", "2026-02-24"),
 "naukri_jobspeak_sep2026.pdf": ("https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-September-2026.pdf", "Info Edge (Naukri)", "Naukri JobSpeak September 2026", "2026-10"),
 "naukri_jobspeak_oct2026.pdf": ("https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-October-2026.pdf", "Info Edge (Naukri)", "Naukri JobSpeak October 2026", "2026-11"),
 "icrier_ai_and_jobs.pdf": ("https://www.icrier.org/pdf/AI-and-Jobs.pdf", "ICRIER (supported by OpenAI)", "AI and Jobs: This Time Is No Different", "2026-02"),
 "arxiv_2606.13314_mishra_caste_genai_india.pdf": ("https://arxiv.org/pdf/2606.13314", "arXiv preprint (K. Mishra)", "The Privilege of Exposure: Caste and Generative AI in India's Graduate Labour Market", "2026-06-21 (v2)"),
 "servicenow_pearson_india_ai_jobs_2024_press.pdf": ("https://s205.q4cdn.com/537566246/files/doc_news/Indias-workforce-to-grow-by-33-9-million-with-AI-transformation-driving-2-73-million-tech-jobs-by-2028-ServiceNow-AI-Skills-and-Jobs--UK296.pdf", "ServiceNow (research by Pearson)", "ServiceNow AI Skills and Jobs Report India press release", "2024-11-13"),
}
rows = []
for fn in sorted(os.listdir(raw)):
    p = os.path.join(raw, fn)
    if not os.path.isfile(p) or fn.startswith("_"):
        continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    url, pub, title, date = META.get(fn, ("", "", "", ""))
    rows.append(dict(file=fn, bytes=os.path.getsize(p), sha256=h, source_url=url, publisher=pub, title=title, pub_date=date, accessed="2026-11-09"))
with open(os.path.join(raw, "_manifest.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "files"); [print(r["file"], r["bytes"], "OK" if r["source_url"] else "NO META") for r in rows]
