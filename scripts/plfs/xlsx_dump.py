"""Dump every sheet of an xlsx as tab-separated text (non-empty rows). Usage: xlsx_dump.py file.xlsx [maxrows]"""
import sys, openpyxl
sys.stdout.reconfigure(encoding="utf-8")
wb = openpyxl.load_workbook(sys.argv[1], data_only=True, read_only=False)
maxrows = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
for ws in wb.worksheets:
    print(f'### SHEET {ws.title} dims={ws.dimensions}')
    n = 0
    for r, row in enumerate(ws.iter_rows(values_only=True), 1):
        vals = ['' if v is None else str(v).strip().replace('\n', ' ') for v in row]
        if any(vals):
            print(r, '\t'.join(vals).rstrip('\t'))
            n += 1
            if n >= maxrows: break
