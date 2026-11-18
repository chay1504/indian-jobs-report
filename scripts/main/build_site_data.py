"""
Merge PLFS occupation stats, AI-exposure scores (two independent passes), ILO GenAI index
cross-check and the income-tax allocation into site/data.json (the India analogue of
karpathy_jobs/site/data.json), plus site/summary.json with headline aggregates.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
D = ROOT / "data" / "derived"
EDU = {0: "Not literate", 1: "Literate, no schooling", 2: "Below primary", 3: "Primary", 4: "Middle",
       5: "Secondary", 6: "Higher secondary", 7: "Diploma", 8: "Graduate", 9: "Postgraduate+"}


def load_scores():
    out = {}
    for tag in ("A", "B"):
        rows = []
        for part in (1, 2):
            p = ROOT / "data" / "scores" / f"pass_{tag}{part}.json"
            if p.exists():
                rows += json.loads(p.read_text(encoding="utf-8"))
        out[tag] = {str(r["occ3"]).zfill(3): r for r in rows}
    return out


def main():
    occ = pd.read_csv(D / "occ3_2025.csv", dtype={"occ3": str})
    meta = pd.read_csv(D / "occ_meta.csv", dtype={"occ3": str, "sub_division": str})
    tax = pd.read_csv(D / "occ_tax_share.csv", dtype={"occ3": str})
    scale = float((D / "scale_factor.txt").read_text().split()[0])
    occ = occ.merge(meta, on="occ3").merge(tax, on="occ3", how="left").fillna({"tax_share": 0, "tax_share_v1": 0})
    sc = load_scores()
    adj_path = ROOT / "data" / "scores" / "adjudicated.json"
    adj = {}
    if adj_path.exists():
        adj = {str(r["occ3"]).zfill(3): r for r in json.loads(adj_path.read_text(encoding="utf-8"))}
    ilo = {}
    ilo_path = D / "ilo_occ3.csv"
    if ilo_path.exists():
        t = pd.read_csv(ilo_path, dtype={"occ3": str})
        ilo = dict(zip(t.occ3, t.ilo_score))

    data = []
    for _, r in occ.iterrows():
        a, b = sc["A"].get(r.occ3), sc["B"].get(r.occ3)
        ea = a["exposure"] if a else None
        eb = b["exposure"] if b else None
        if r.occ3 in adj:
            exp, rat = adj[r.occ3]["exposure"], adj[r.occ3]["rationale"]
        elif ea is not None and eb is not None:
            exp = (ea + eb) / 2  # mean of two independent passes (may be x.5)
            rat = a["rationale"]
        else:
            exp, rat = (ea if ea is not None else eb), (a or b or {}).get("rationale")
        data.append({
            "title": r.title, "slug": r.occ3, "category": r.category,
            "jobs": int(round(r.jobs_raw * scale)), "n_obs": int(r.n_obs),
            "pay": int(round(r.pay_median)) if pd.notna(r.pay_median) else None,
            "pay_mean": int(round(r.pay_mean)) if pd.notna(r.pay_mean) else None,
            "education": EDU.get(int(r.edu_median_ord)) if pd.notna(r.edu_median_ord) else None,
            "edu_ord": int(r.edu_median_ord) if pd.notna(r.edu_median_ord) else None,
            "pct_grad": round(r.pct_grad, 4), "formal": round(r.pct_formal, 4),
            "regular": round(r.pct_regular, 4), "self": round(r.pct_self, 4), "casual": round(r.pct_casual, 4),
            "female": round(r.pct_female, 4), "urban": round(r.pct_urban, 4), "govt": round(r.pct_govt, 4),
            "taxpayer": round(r.pct_taxpayer, 5) if pd.notna(r.pct_taxpayer) else 0,
            "tax_share": round(r.tax_share, 5), "tax_share_v1": round(r.tax_share_v1, 5),
            "exposure": exp, "exposure_a": ea, "exposure_b": eb, "exposure_rationale": rat,
            "ilo": round(ilo[r.occ3], 3) if r.occ3 in ilo else None,
        })
    (ROOT / "site").mkdir(exist_ok=True)
    (ROOT / "site" / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    df = pd.DataFrame(data)
    print("occupations:", len(df), " jobs (crore):", round(df.jobs.sum() / 1e7, 2), " scored:", df.exposure.notna().sum())
    if df.exposure.notna().all():
        J = df.jobs.sum()
        wages = (df.jobs * df.pay_mean).sum()
        print("job-weighted exposure:", round((df.exposure * df.jobs).sum() / J, 2))
        print("earnings-weighted exposure:", round((df.exposure * df.jobs * df.pay_mean).sum() / wages, 2))
        print("tax-weighted exposure:", round((df.exposure * df.tax_share).sum() / df.tax_share.sum(), 2))
        for lo, hi, name in [(0, 2, "Minimal"), (2, 4, "Low"), (4, 6, "Moderate"), (6, 8, "High"), (8, 11, "Very high")]:
            g = df[(df.exposure >= lo) & (df.exposure < hi)]
            print(f"  {name:10s} jobs {g.jobs.sum()/J:6.1%}  earnings {(g.jobs*g.pay_mean).sum()/wages:6.1%}  "
                  f"income-tax {g.tax_share.sum():6.1%}  (v1 {g.tax_share_v1.sum():6.1%})")
        ag = (df.exposure_a - df.exposure_b).abs()
        print("pass agreement: exact", (ag == 0).mean().round(3), " within1", (ag <= 1).mean().round(3), " >=2:",
              df[ag >= 2][["slug", "title", "exposure_a", "exposure_b"]].to_dict("records"))


if __name__ == "__main__":
    main()
