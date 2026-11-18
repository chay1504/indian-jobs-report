"""Fetch PLFS tables from the official MoSPI API (https://api.mospi.gov.in/api/plfs/getData).

Swagger spec: https://api.mospi.gov.in/layout/swagger_user_plfs.yaml (no login needed for GET).
Saves one combined CSV per (indicator, year) under data/raw/plfs/api/ with all-India records only.

Usage: python -I fetch_mospi_api.py INDICATOR_CODE YEAR [YEAR ...]
  YEAR is e.g. "PLFS 2025" (calendar year, year_type_code=2) or "2017-18" (agricultural year, year_type_code=1)
"""
import csv, json, os, ssl, sys, time, urllib.parse, urllib.request

BASE = 'https://api.mospi.gov.in/api/plfs/getData'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
# api.mospi.gov.in needs legacy TLS renegotiation (OpenSSL 3 refuses it by default)
CTX = ssl.create_default_context()
CTX.options |= getattr(ssl, 'OP_LEGACY_SERVER_CONNECT', 0x4)
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'plfs', 'api')


def get(params):
    url = BASE + '?' + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:  # network hiccup: back off and retry
            print('  retry', attempt + 1, e, file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError('failed: ' + url)


def fetch(indicator, year, extra=None):
    ytype = 2 if year.startswith('PLFS') else 1
    params = {'indicator_code': indicator, 'frequency_code': 1, 'year': year, 'year_type_code': ytype,
              'state_code': 99, 'Format': 'JSON', 'limit': 200}
    if extra:
        params.update(extra)
    rows, page = [], 1
    while True:
        params['page'] = page
        d = get(params)
        data = d.get('data') or []
        rows.extend(data)
        meta = d.get('meta_data') or {}
        tp = meta.get('totalPages', 1)
        if page == 1:
            print(f'indicator {indicator} {year}: {meta.get("totalRecords")} records, {tp} pages', flush=True)
        if page >= tp or not data:
            break
        page += 1
        time.sleep(0.4)
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    ind = int(sys.argv[1])
    for year in sys.argv[2:]:
        rows = fetch(ind, year)
        if not rows:
            print('  no data', year)
            continue
        fn = os.path.join(OUT, f'plfs_api_ind{ind}_{year.replace(" ", "")}_allindia.csv')
        keys = list(rows[0].keys())
        with open(fn, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=keys + ['api_query'])
            w.writeheader()
            q = f'{BASE}?indicator_code={ind}&frequency_code=1&year={year}&state_code=99'
            for r in rows:
                r['api_query'] = q
                w.writerow(r)
        print('  wrote', fn, len(rows))


if __name__ == '__main__':
    main()
