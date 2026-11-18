"""
Build one Markdown "occupation page" per NCO-2015 3-digit group (the India analogue of
Karpathy's BLS OOH pages/), combining the official NCO-2015 description with PLFS 2025
statistics. These pages are what the AI-exposure scorer reads.

Output: data/pages/<occ3>.md, data/derived/occ_meta.csv
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
PAGES = ROOT / "data" / "pages"
PAGES.mkdir(parents=True, exist_ok=True)

NIC2 = {
    "01": "Crop & animal production", "02": "Forestry & logging", "03": "Fishing & aquaculture",
    "05": "Coal mining", "06": "Crude petroleum & gas", "07": "Metal ore mining", "08": "Other mining & quarrying",
    "09": "Mining support", "10": "Food products", "11": "Beverages", "12": "Tobacco products", "13": "Textiles",
    "14": "Wearing apparel", "15": "Leather products", "16": "Wood products", "17": "Paper", "18": "Printing",
    "19": "Coke & refined petroleum", "20": "Chemicals", "21": "Pharmaceuticals", "22": "Rubber & plastics",
    "23": "Non-metallic mineral products (bricks, cement, glass)", "24": "Basic metals", "25": "Fabricated metal products",
    "26": "Computer, electronic & optical products", "27": "Electrical equipment", "28": "Machinery",
    "29": "Motor vehicles", "30": "Other transport equipment", "31": "Furniture", "32": "Other manufacturing (jewellery etc.)",
    "33": "Repair & installation of machinery", "35": "Electricity & gas", "36": "Water supply", "37": "Sewerage",
    "38": "Waste collection & recovery", "39": "Remediation", "41": "Construction of buildings", "42": "Civil engineering",
    "43": "Specialised construction", "45": "Motor vehicle trade & repair", "46": "Wholesale trade", "47": "Retail trade",
    "49": "Land transport", "50": "Water transport", "51": "Air transport", "52": "Warehousing & transport support",
    "53": "Postal & courier", "55": "Accommodation", "56": "Food & beverage service", "58": "Publishing",
    "59": "Film, video, TV & music", "60": "Broadcasting", "61": "Telecommunications", "62": "Computer programming & IT consultancy",
    "63": "Information services", "64": "Financial services (banking)", "65": "Insurance & pensions", "66": "Auxiliary financial services",
    "68": "Real estate", "69": "Legal & accounting", "70": "Head offices & management consultancy", "71": "Architecture & engineering",
    "72": "Scientific R&D", "73": "Advertising & market research", "74": "Other professional & technical", "75": "Veterinary",
    "77": "Rental & leasing", "78": "Employment/staffing activities", "79": "Travel agencies", "80": "Security & investigation",
    "81": "Building services & landscaping", "82": "Office admin & business support (incl. BPO/call centres)",
    "84": "Public administration & defence", "85": "Education", "86": "Human health", "87": "Residential care",
    "88": "Social work", "90": "Arts & entertainment", "91": "Libraries & museums", "92": "Gambling & betting",
    "93": "Sports & recreation", "94": "Membership organisations (religious, political)", "95": "Repair of computers & household goods",
    "96": "Other personal services (laundry, beauty, funeral)", "97": "Households as employers of domestic workers",
    "98": "Household own-use production", "99": "Extraterritorial organisations",
}

CATEGORY = {  # NCO-2015 sub-division (2-digit) -> treemap category (BLS-style grouping)
    "11": "Management", "12": "Management", "13": "Management", "14": "Management",
    "21": "Science & engineering", "31": "Science & engineering",
    "22": "Healthcare", "32": "Healthcare", "53": "Healthcare",
    "23": "Education",
    "24": "Business & finance", "33": "Business & finance",
    "25": "Computer & IT", "35": "Computer & IT",
    "26": "Legal, social, arts & media", "34": "Legal, social, arts & media",
    "41": "Office & admin support", "42": "Office & admin support", "43": "Office & admin support", "44": "Office & admin support",
    "51": "Personal services", "52": "Sales", "95": "Sales", "54": "Protective services",
    "61": "Agriculture, forestry & fishing", "62": "Agriculture, forestry & fishing", "63": "Agriculture, forestry & fishing",
    "92": "Agriculture, forestry & fishing",
    "71": "Construction trades", "72": "Metal, machinery & electrical trades", "74": "Metal, machinery & electrical trades",
    "73": "Crafts, food processing & garments", "75": "Crafts, food processing & garments",
    "81": "Machine operators & assemblers", "82": "Machine operators & assemblers",
    "83": "Drivers & transport",
    "91": "Cleaners, helpers & elementary", "94": "Cleaners, helpers & elementary", "96": "Cleaners, helpers & elementary",
    "93": "Labourers (construction, factory, transport)",
}

# NCO-2015 / ISCO-08 minor group 343; the scraped structure file carried a wrong title and no description.
TITLE_FIX = {
    "343": ("Artistic, Cultural and Culinary Associate Professionals",
            "Artistic, cultural and culinary associate professionals combine creative and technical skills to "
            "produce and maintain visual and audio images, and to prepare and plan meals: photographers, "
            "interior designers and decorators, gallery and museum technicians, chefs, and other artistic "
            "and cultural associate professionals."),
}

EDU_LABEL = {0: "Not literate", 1: "Literate, no formal schooling", 2: "Below primary", 3: "Primary", 4: "Middle (Class 8)",
             5: "Secondary (Class 10)", 6: "Higher secondary (Class 12)", 7: "Diploma/certificate", 8: "Graduate",
             9: "Postgraduate & above"}


def lakh(x):
    if x >= 1e7:
        return f"{x / 1e7:.2f} crore"
    return f"{x / 1e5:.1f} lakh"


def main():
    s = pd.read_csv(ROOT / "data" / "nco" / "nco2015_structure.csv", dtype=str)
    occ = pd.read_csv(ROOT / "data" / "derived" / "occ3_2025.csv", dtype={"occ3": str})
    scale = float(open(ROOT / "data" / "derived" / "scale_factor.txt").read().split()[0])
    groups = s[s.level == "group"].set_index(s[s.level == "group"].code.str.zfill(3))
    meta = []
    for _, r in occ.iterrows():
        code = r.occ3
        if code in TITLE_FIX:
            title, desc = TITLE_FIX[code]
        elif code in groups.index:
            g = groups.loc[code]
            title, desc = g.title, str(g.description)
        else:
            title, desc = f"NCO {code}", ""
        fam = s[(s.level == "family") & (s.code.str[:3] == code)]
        occs = s[(s.level == "occupation") & (s.code.str[:3] == code)]
        cat = CATEGORY.get(code[:2], "Other")
        jobs = r.jobs_raw * scale
        lines = [f"# {title}", "", f"NCO-2015 group {code}. Category: {cat}.", "", "## What they do", "", desc, ""]
        if len(fam):
            lines += ["## Occupation families in this group", ""]
            for _, f in fam.iterrows():
                d = str(f.description) if pd.notna(f.description) else ""
                lines.append(f"- **{f.title}** ({f.code}): {d[:400]}")
            lines.append("")
        if len(occs):
            ex = ", ".join(occs.title.dropna().astype(str).head(30).tolist())
            lines += ["## Example job titles (NCO-2015)", "", ex, ""]
        tops = [NIC2.get(x, x) for x in str(r.top_nic2).split(";") if x and x != "nan"]
        lines += [
            "## India: who does this work (PLFS 2025, workers aged 15+)", "",
            f"- Workers: about {lakh(jobs)} (PLFS sample of {int(r.n_obs):,} people)",
            f"- Employment type: {r.pct_self:.0%} self-employed (incl. unpaid family helpers), "
            f"{r.pct_regular:.0%} regular salaried, {r.pct_casual:.0%} casual labour",
            f"- Formal jobs (regular salaried with any social security): {r.pct_formal:.0%}",
            f"- Government/public sector employer: {r.pct_govt:.0%}",
            f"- Women: {r.pct_female:.0%}; urban: {r.pct_urban:.0%}",
            f"- Typical education (median worker): {EDU_LABEL.get(int(r.edu_median_ord), '?') if pd.notna(r.edu_median_ord) else '?'}; "
            f"graduate or above: {r.pct_grad:.0%}",
            f"- Median annual earnings: Rs {r.pay_median:,.0f}" if pd.notna(r.pay_median) else "- Median annual earnings: n/a",
            f"- Main industries: {', '.join(tops)}", "",
        ]
        (PAGES / f"{code}.md").write_text("\n".join(lines), encoding="utf-8")
        meta.append({"occ3": code, "title": title, "category": cat, "sub_division": code[:2]})
    pd.DataFrame(meta).to_csv(ROOT / "data" / "derived" / "occ_meta.csv", index=False)
    print("pages:", len(meta))


if __name__ == "__main__":
    main()
