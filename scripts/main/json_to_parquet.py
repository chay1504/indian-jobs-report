"""
Stream-convert PLFS 2025 JSON unit-level files (Data_in_JSON.zip) to parquet,
keeping only the fields this project needs.

Records are flat JSON objects (no nesting), so we split the array on object
boundaries and json-decode one record at a time to keep memory low.

Usage: .venv/Scripts/python -I scripts/main/json_to_parquet.py <india_jobs_root>
"""
import json
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
MICRO = ROOT / "data" / "microdata"

PERSON_KEEP = [
    "qtr", "month", "sec", "st", "dc", "mfsu", "sss", "ssu", "srl", "rel",
    "sex", "age", "gedu_lvl", "tedu_lvl", "voc",
    "pas", "ind_pas", "ocu_pas", "has_sas", "loc_pas", "etyp_pas", "wrkr_pas",
    "job_pas", "leave_pas", "ssec_pas",
    "sas", "ind_sas", "ocu_sas", "etyp_sas", "job_sas", "leave_sas", "ssec_sas",
    "acws", "aind_cws", "ocu_cws", "ern_reg", "ern_self", "tothrs_wrk",
    "nsc", "mult",
]
for day in range(1, 8):
    for act in (1, 2):
        PERSON_KEEP += [f"das{act}{day}", f"ern{act}{day}", f"hr{act}{day}"]

HH_KEEP = ["month", "sec", "st", "dc", "mfsu", "sss", "ssu", "hh_size", "hhtype",
           "relg", "sg", "hce_tot", "rent", "interest", "pension", "remit", "inc_tot", "mult"]


OBJ = re.compile(r"\{[^{}]*\}")


def stream_objects(fh, chunk=1 << 24):
    """Yield flat JSON object strings. Records contain no nested braces."""
    buf = ""
    while True:
        data = fh.read(chunk)
        if not data:
            break
        buf += data.decode("utf-8", "replace")
        last = 0
        for m in OBJ.finditer(buf):
            yield m.group(0)
            last = m.end()
        buf = buf[last:]
    if buf.strip(" \n\r\t],"):
        print("WARNING trailing unparsed text:", buf[:200])


def convert(zf, member, keep, out_name):
    cols = {k: [] for k in keep}
    n = 0
    with zf.open(member) as fh:
        for obj in stream_objects(fh):
            rec = json.loads(obj)
            for k in keep:
                cols[k].append(rec.get(k))
            n += 1
            if n % 200000 == 0:
                print(f"  {member}: {n:,}", flush=True)
    df = pd.DataFrame(cols)
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype("string").str.strip()
    df.to_parquet(MICRO / out_name, index=False)
    print(f"wrote {out_name}: {len(df):,} rows")


def main():
    zpath = next(MICRO.glob("*.zip"))
    zf = zipfile.ZipFile(zpath)
    names = zf.namelist()
    hh = next(n for n in names if n.lower().endswith("chhv12025.json"))
    pe = next(n for n in names if n.lower().endswith("cperv12025.json"))
    convert(zf, hh, HH_KEEP, "households_2025.parquet")
    convert(zf, pe, PERSON_KEEP, "persons_2025.parquet")


if __name__ == "__main__":
    main()
