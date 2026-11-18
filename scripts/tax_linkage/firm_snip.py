"""Print compact snippets around a regex in the page-text dumps.
Usage: firm_snip.py <txt_dir> <file_glob_prefixes comma> <regex> <before> <after> [maxhits] [page_filter e.g. 100-200]"""
import os, re, sys, glob

d, prefixes, rx, before, after = sys.argv[1], sys.argv[2].split(","), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
maxhits = int(sys.argv[6]) if len(sys.argv) > 6 else 6
prange = tuple(map(int, sys.argv[7].split("-"))) if len(sys.argv) > 7 and sys.argv[7] != "all" else None
must = re.compile(sys.argv[8], re.I) if len(sys.argv) > 8 else None  # page must match this regex
pat = re.compile(rx, re.I)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for pre in prefixes:
    for fp in sorted(glob.glob(os.path.join(d, pre + "*.txt"))):
        key = os.path.basename(fp)[:-4]
        txt = open(fp, encoding="utf-8").read()
        pages = re.split(r"\n=== PDF PAGE (\d+) ===\n", txt)
        n = 0
        for i in range(1, len(pages), 2):
            pno, t = int(pages[i]), pages[i + 1]
            if prange and not (prange[0] <= pno <= prange[1]):
                continue
            if must and not must.search(t):
                continue
            lines = [l.strip() for l in t.splitlines() if l.strip()]
            nums = [l for l in (lines[:2] + lines[-3:]) if re.fullmatch(r"\d{1,3}", l)]
            last_end = -1
            for m in pat.finditer(t):
                if n >= maxhits:
                    break
                if m.start() < last_end:
                    continue
                last_end = m.end() + after
                s = re.sub(r"\s+", " ", t[max(0, m.start() - before): m.end() + after])
                scope = "CONS" if "consolidated" in t.lower() else "STD?"
                print(f"[{key} pdfp{pno} printed?{nums} {scope}] {s}\n")
                n += 1
