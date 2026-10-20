import subprocess, os, sys, shutil, tempfile, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
prof = tempfile.mkdtemp(prefix="cat-chrome-")
pdf = os.path.join(ROOT, "out", "TechNext-Services-Catalogue-2026-27.pdf")
os.makedirs(os.path.join(ROOT, "out", "pages"), exist_ok=True)
url = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/")
subprocess.run([chrome, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                "--virtual-time-budget=8000", "--run-all-compositor-stages-before-draw", f"--print-to-pdf={pdf}", url], check=True, capture_output=True)
shutil.rmtree(prof, ignore_errors=True)
doc = pymupdf.open(pdf)
print("pdf pages", doc.page_count, "size", doc[0].rect)
dpi = int(sys.argv[1]) if len(sys.argv) > 1 else 110
for i, pg in enumerate(doc, 1):
    pg.get_pixmap(dpi=dpi).save(os.path.join(ROOT, "out", "pages", f"page-{i:02d}.png"))
