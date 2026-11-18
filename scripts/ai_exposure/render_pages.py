"""Render PDF pages to PNG. Usage: python -I render_pages.py <pdf> <outdir> <page1,page2,...> [zoom]"""
import sys, pymupdf, os
pdf, outdir, pages = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")]
zoom = float(sys.argv[4]) if len(sys.argv) > 4 else 1.6
os.makedirs(outdir, exist_ok=True)
doc = pymupdf.open(pdf)
for p in pages:
    pix = doc[p-1].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    fn = os.path.join(outdir, f"p{p:03d}.png"); pix.save(fn); print(fn)
