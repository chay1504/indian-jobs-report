"""Download FY2025-26 and FY2024-25 annual reports (NSE archive copies of the filed AR) with curl -L.
Also re-queries NSE index for LTIMindtree symbol variants."""
import json, os, subprocess, sys, urllib.request, http.cookiejar
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
OUT = r"C:\Users\hp\Downloads\xyz\india_jobs\data\raw\tax_linkage\company_reports"
B = "https://nsearchives.nseindia.com/annual_reports/"
URLS = {
    "TCS_FY26": B + "AR_29263_TCS_2025_2026_A_17427580_15052026234830.pdf",
    "TCS_FY25": B + "AR_26456_TCS_2024_2025_A_27052025233502.pdf",
    "INFY_FY26": B + "AR_29313_INFY_2025_2026_U_8985411_30052026200413.pdf",
    "INFY_FY25": B + "AR_26481_INFY_2024_2025_A_02062025153945.pdf",
    "HCLTECH_FY26": B + "AR_29915_HCLTECH_2025_2026_A_16831072_20072026200555.pdf",
    "HCLTECH_FY25": B + "AR_27254_HCLTECH_2024_2025_A_02082025194851.pdf",
    "WIPRO_FY26": B + "AR_29427_WIPRO_2025_2026_A_8877705_22062026190140.pdf",
    "WIPRO_FY25": B + "AR_26582_WIPRO_2024_2025_A_21062025124943.pdf",
    "TECHM_FY26": B + "AR_29435_TECHM_2025_2026_A_15304795_23062026234616.pdf",
    "TECHM_FY25": B + "AR_26592_TECHM_2024_2025_A_23062025224043.pdf",
    "HDFCBANK_FY26": B + "AR_29735_HDFCBANK_2025_2026_A_12667766_11072026001055.pdf",
    "HDFCBANK_FY25": B + "AR_27115_HDFCBANK_2024_2025_U_25072025220054.pdf",
    "ICICIBANK_FY26": B + "AR_29895_ICICIBANK_2025_2026_A_23776312_18072026185534.pdf",
    "ICICIBANK_FY25": B + "AR_27289_ICICIBANK_2024_2025_A_05082025201317.pdf",
    "AXISBANK_FY26": B + "AR_29441_AXISBANK_2025_2026_A_11309490_25062026131025.pdf",
    "AXISBANK_FY25": B + "AR_26622_AXISBANK_2024_2025_A_27062025104637.pdf",
    "KOTAKBANK_FY26": B + "AR_32041_KOTAKBANK_2025_2026_A_9262663_16092026104828.pdf",
    "KOTAKBANK_FY25": B + "AR_27794_KOTAKBANK_2024_2025_A_12174639_28082025142226.pdf",
    "SBIN_FY26": B + "AR_29279_SBIN_2025_2026_A_22551017_26052026223038.pdf",
    "SBIN_FY25": B + "AR_26445_SBIN_2024_2025_A_21052025215909.pdf",
}

# LTIMindtree symbol lookup
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Accept", "*/*"), ("Referer", "https://www.nseindia.com/")]
for sym in ["LTIM", "LTIMINDTREE", "LTM", "LTI"]:
    try:
        d = json.loads(op.open(f"https://www.nseindia.com/api/annual-reports?index=equities&symbol={sym}", timeout=30).read())
        rows = d.get("data", [])
        print("LTIM lookup", sym, len(rows))
        for r in rows[:3]:
            print("  ", r.get("companyName"), r.get("fromYr"), r.get("toYr"), r.get("submission_type"), r.get("fileName"))
            if r.get("fileName", "").endswith(".pdf") and r.get("toYr") in ("2026", "2025"):
                key = "LTIM_FY" + r["toYr"][2:]
                URLS.setdefault(key, r["fileName"])
        if rows:
            break
    except Exception as e:
        print("LTIM lookup", sym, "ERR", repr(e)[:150])

def get(item):
    k, u = item
    p = os.path.join(OUT, k + ".pdf")
    if os.path.exists(p) and os.path.getsize(p) > 500000:
        return k, os.path.getsize(p), "cached"
    r = subprocess.run(["curl.exe", "-sS", "-L", "-A", UA, "--max-time", "500", "-o", p, u], capture_output=True, text=True)
    sz = os.path.getsize(p) if os.path.exists(p) else 0
    with open(p, "rb") as f:
        head = f.read(5) if sz else b""
    return k, sz, (r.stderr.strip()[:120] or "ok") + f" head={head!r}"

with ThreadPoolExecutor(6) as ex:
    for k, sz, msg in ex.map(get, URLS.items()):
        print(k, sz, msg)
json.dump(URLS, open(os.path.join(OUT, "_urls.json"), "w"), indent=1)
