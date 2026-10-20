"""Publish the flip-book into the technext.asia website repo at /services-catalogue.

    python tools/publish_site.py <path to TechNext-Website checkout>

technext.asia serves folders without a trailing slash (/services-catalogue), so a relative "assets/..."
would resolve against the site root. Every viewer path is rewritten to an absolute /services-catalogue/...
URL. Only what the viewer needs is copied: the page, reader.js/css, the patched StPageFlip, two logos,
book/ (page images, thumbs, text, hotspots) and the PDF. The target folder is replaced each run.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/services-catalogue/"
PDF = "TechNext-Services-Catalogue-2026-27.pdf"


def main():
    site = os.path.abspath(sys.argv[1])
    assert os.path.isfile(os.path.join(site, "_src", "build.py")), "not a TechNext-Website checkout"
    dst = os.path.join(site, "services-catalogue")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(os.path.join(dst, "assets", "vendor"))
    os.makedirs(os.path.join(dst, "assets", "logo"))

    # page: absolute asset paths, PDF next to the page, canonical on technext.asia
    html = open(os.path.join(ROOT, "viewer.html"), encoding="utf-8").read()   # index.html here only redirects to technext.asia
    for a, b in (('"assets/', '"' + BASE + 'assets/'), ('"book/', '"' + BASE + 'book/'), ('"out/', '"' + BASE)):
        html = html.replace(a, b)
    if 'rel="canonical"' not in html:
        html = html.replace('<meta name="robots"', '<link rel="canonical" href="https://technext.asia/services-catalogue">\n<meta name="robots"', 1)
    assert '"assets/' not in html and '"book/' not in html and '"out/' not in html
    open(os.path.join(dst, "index.html"), "w", encoding="utf-8", newline="\n").write(html)

    js = open(os.path.join(ROOT, "assets", "reader.js"), encoding="utf-8").read()
    for q in ("`", "'", '"'):
        js = js.replace(q + "book/", q + BASE + "book/")
    assert "`book/" not in js and "'book/" not in js
    open(os.path.join(dst, "assets", "reader.js"), "w", encoding="utf-8", newline="\n").write(js)

    shutil.copy2(os.path.join(ROOT, "assets", "reader.css"), os.path.join(dst, "assets"))
    shutil.copy2(os.path.join(ROOT, "assets", "vendor", "page-flip.browser.js"), os.path.join(dst, "assets", "vendor"))
    for logo in ("technext-brandmark-blue.png", "technext-horizontal-blue.png"):
        shutil.copy2(os.path.join(ROOT, "assets", "logo", logo), os.path.join(dst, "assets", "logo"))
    shutil.copytree(os.path.join(ROOT, "book"), os.path.join(dst, "book"))
    shutil.copy2(os.path.join(ROOT, "out", PDF), os.path.join(dst, PDF))

    n = sum(len(f) for _, _, f in os.walk(dst))
    mb = sum(os.path.getsize(os.path.join(d, x)) for d, _, f in os.walk(dst) for x in f) / 1e6
    print(f"published {n} files, {mb:.1f} MB -> {dst}")


if __name__ == "__main__":
    main()
