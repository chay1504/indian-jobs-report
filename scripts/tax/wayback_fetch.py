"""Polite Wayback Machine fetcher for official CBDT PDFs (incometaxindia.gov.in blocks non-browser clients).
Usage: python -I wayback_fetch.py <outname> <original_url> [timestamp]
Saves raw bytes (id_ mode) into data/raw/tax/<outname>, retrying with backoff on 429/5xx."""
import sys, os, time, urllib.request, urllib.error, json, urllib.parse
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'tax'))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.read(), r.geturl()
def main(name, orig, ts=None):
    if not ts:
        for attempt in range(6):
            try:
                _, b, _ = get('https://archive.org/wayback/available?url=' + urllib.parse.quote(orig, safe=''))
                snap = json.loads(b).get('archived_snapshots', {}).get('closest')
                if not snap: print('NOT ARCHIVED', orig); return
                ts = snap['timestamp']; break
            except Exception as e:
                print('avail err', e); time.sleep(30 * (attempt + 1))
    url = f'https://web.archive.org/web/{ts}id_/{orig}'
    for attempt in range(8):
        try:
            st, b, final = get(url)
            if b[:4] == b'%PDF' or name.endswith(('.xlsx', '.xls', '.html')):
                open(os.path.join(OUT, name), 'wb').write(b); print('OK', name, len(b), final); return
            print('not pdf', b[:80])
        except urllib.error.HTTPError as e:
            print('HTTP', e.code, 'attempt', attempt)
        except Exception as e:
            print('ERR', e)
        time.sleep(45 * (attempt + 1))
    print('FAILED', name)
if __name__ == '__main__':
    main(*sys.argv[1:])
