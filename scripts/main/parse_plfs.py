"""
Parse PLFS Calendar Year 2025 first-visit person-level unit data (CPERV1.txt)
into a compact parquet/CSV with only the fields we need.

Layout: data/raw/microdata_meta/FV_Data_LayoutPLFS_2025.xlsx, sheet "CPERV1".
Input:  data/microdata/ (CPERV1.txt / CHHV1.txt, or a zip containing them)
Output: data/microdata/persons_2025.parquet (+ .csv.gz)

Usage: .venv/Scripts/python -I scripts/main/parse_plfs.py <india_jobs_root>
"""
import io
import sys
import zipfile
from pathlib import Path

import openpyxl
import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
MICRO = ROOT / "data" / "microdata"
LAYOUT = ROOT / "data" / "raw" / "microdata_meta" / "FV_Data_LayoutPLFS_2025.xlsx"

KEEP = [
    "qtr", "month", "sec", "st", "dc", "mfsu", "sss", "ssu", "srl",
    "sex", "age", "gedu_lvl", "tedu_lvl",
    "pas", "ind_pas", "ocu_pas", "has_sas", "loc_pas", "etyp_pas", "wrkr_pas",
    "job_pas", "leave_pas", "ssec_pas",
    "sas", "ind_sas", "ocu_sas", "etyp_sas", "job_sas", "leave_sas", "ssec_sas",
    "acws", "aind_cws", "ocu_cws", "ern_reg", "ern_self", "tothrs_wrk",
    "nsc", "mult",
]
# daily activity status + wage earnings for the 7 days (2 activities per day)
for day in range(1, 8):
    for act in (1, 2):
        KEEP += [f"das{act}{day}", f"ern{act}{day}"]


def read_layout(sheet):
    wb = openpyxl.load_workbook(LAYOUT, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(h).strip() if h else "" for h in rows[0]]
    i_start = hdr.index("Byte Position (Start)")
    i_end = hdr.index("Byte Position (End)")
    i_name = hdr.index("Field_Name")
    spec = {}
    for r in rows[1:]:
        if r[i_name] is None or r[i_start] is None:
            continue
        spec[str(r[i_name]).strip()] = (int(r[i_start]) - 1, int(r[i_end]))
    return spec


def find_file(stem):
    for p in MICRO.rglob("*"):
        if p.is_file() and p.name.lower().startswith(stem.lower()) and p.suffix.lower() == ".txt":
            return p.open("rb")
    for z in MICRO.rglob("*.zip"):
        zf = zipfile.ZipFile(z)
        for n in zf.namelist():
            if Path(n).name.lower().startswith(stem.lower()) and n.lower().endswith(".txt"):
                return io.BytesIO(zf.read(n))
    raise FileNotFoundError(f"{stem}*.txt not found under {MICRO}")


def main():
    spec = read_layout("CPERV1")
    missing = [k for k in KEEP if k not in spec]
    if missing:
        print("WARNING fields not in layout:", missing)
    cols = [k for k in KEEP if k in spec]
    colspecs = [spec[k] for k in cols]
    fh = find_file("CPERV1")
    df = pd.read_fwf(fh, colspecs=colspecs, names=cols, dtype=str, header=None)
    for c in cols:
        df[c] = df[c].str.strip()
    num = [c for c in cols if c not in ("ind_pas", "ind_sas", "ocu_pas", "ocu_sas", "ocu_cws", "aind_cws")]
    for c in num:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["w"] = df["mult"] / 100.0
    print("records:", len(df))
    print("sum of weights (M):", round(df["w"].sum() / 1e6, 1))
    print("by month count:", df["month"].value_counts().sort_index().to_dict())
    out = MICRO / "persons_2025.parquet"
    try:
        df.to_parquet(out, index=False)
    except Exception as e:  # pyarrow may be missing
        print("parquet failed:", e)
    df.to_csv(MICRO / "persons_2025.csv.gz", index=False, compression="gzip")
    print("wrote", MICRO)


if __name__ == "__main__":
    main()
