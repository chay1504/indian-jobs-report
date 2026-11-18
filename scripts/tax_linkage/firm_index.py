"""Query BSE (and NSE fallback) annual-report indexes for the target firms.
Prints the FY2024-25 and FY2025-26 annual report PDF links. Output is data only."""
import json, sys, urllib.request, http.cookiejar

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
FIRMS = {
    "TCS": (532540, "TCS"), "INFY": (500209, "INFY"), "HCLTECH": (532281, "HCLTECH"),
    "WIPRO": (507685, "WIPRO"), "TECHM": (532755, "TECHM"), "LTIM": (540005, "LTIM"),
    "HDFCBANK": (500180, "HDFCBANK"), "ICICIBANK": (532174, "ICICIBANK"),
    "AXISBANK": (532215, "AXISBANK"), "KOTAKBANK": (500247, "KOTAKBANK"), "SBIN": (500112, "SBIN"),
}

def bse(code):
    url = f"https://api.bseindia.com/BseIndiaAPI/api/AnnualReport_New/w?scripcode={code}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.bseindia.com/",
                                              "Origin": "https://www.bseindia.com", "Accept": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace"))

def nse_opener():
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    op.addheaders = [("User-Agent", UA), ("Accept", "*/*"), ("Accept-Language", "en-US,en;q=0.9"),
                     ("Referer", "https://www.nseindia.com/")]
    try:
        op.open("https://www.nseindia.com/", timeout=30).read()
    except Exception as e:
        print("NSE home err", e)
    return op

mode = sys.argv[1] if len(sys.argv) > 1 else "bse"
op = nse_opener() if mode == "nse" else None
for k, (code, sym) in FIRMS.items():
    try:
        if mode == "bse":
            d = bse(code)
            rows = d.get("Table", d) if isinstance(d, dict) else d
            for r in rows[:4]:
                print(k, code, json.dumps(r)[:400])
        else:
            d = json.loads(op.open(f"https://www.nseindia.com/api/annual-reports?index=equities&symbol={sym}", timeout=30).read())
            for r in d.get("data", [])[:3]:
                print(k, json.dumps(r)[:400])
    except Exception as e:
        print(k, "ERR", repr(e)[:200])
