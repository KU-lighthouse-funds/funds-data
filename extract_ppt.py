"""Extract text from KU LH PowerPoint."""
from pathlib import Path
from zipfile import ZipFile
import html as html_lib
import re

pptx = Path(r"C:\Users\Kaja\Documents\Funds\KU LH preaward funding support-AZ-JSJ.pptx")
out = Path(r"C:\Users\Kaja\Documents\Funds\_ppt_extract.txt")

parts = []
with ZipFile(pptx) as z:
    slides = sorted(
        [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")],
        key=lambda s: int(re.search(r"slide(\d+)", s).group(1)),
    )
    for i, name in enumerate(slides, 1):
        xml = z.read(name).decode("utf-8", errors="ignore")
        texts = re.findall(r"<a:t[^>]*>(.*?)</a:t>", xml)
        cleaned = []
        for t in texts:
            t = html_lib.unescape(t)
            if t.strip():
                cleaned.append(t)
        parts.append(f"===== SLIDE {i} ({name}) =====")
        parts.append("\n".join(cleaned))
        parts.append("")

out.write_text("\n".join(parts), encoding="utf-8")
print(f"slides={len(slides)} bytes={out.stat().st_size}")
