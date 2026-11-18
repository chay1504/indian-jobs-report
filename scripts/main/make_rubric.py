"""Copy Karpathy's AI-exposure rubric (karpathy_jobs/score.py SYSTEM_PROMPT) verbatim,
changing only the sentence that names the data source."""
from pathlib import Path

src = Path(r"C:\Users\hp\Downloads\xyz\karpathy_jobs\score.py").read_bytes().decode("utf-8")
src = src.replace("\r\n", "\n")
start = src.index('SYSTEM_PROMPT = """') + len('SYSTEM_PROMPT = """')
end = src.index('"""', start)
p = src[start:end]
p = p.replace(chr(92) + "\n", "")  # python line-continuation backslashes
p = p.strip()
old = "from the Bureau of Labor Statistics."
assert old in p
p = p.replace(old, "from India's National Classification of Occupations (NCO-2015), with statistics on "
                   "who does this work in India from the Periodic Labour Force Survey 2025.")
Path(r"C:\Users\hp\Downloads\xyz\india_jobs\data\scores\rubric.txt").write_text(p, encoding="utf-8")
print(p)
