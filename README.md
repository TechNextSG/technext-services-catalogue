# TechNext Services Catalogue (Edition 2026/27)

38-page A4 services catalogue for TechNext Pte. Ltd., with an interactive flip-book viewer. Unlisted (noindex).

- `index.html` - **flip-book viewer** (engine from the nivellipso / HST catalogue reader: page curl, Book / Scroll / Pages views, zoom, full-text search, contents, bookmarks, share links `#p=12`; phones get Scroll only)
- `print.html` - the catalogue source page (prints to A4)
- `out/TechNext-Services-Catalogue-2026-27.pdf` - print/share PDF

## Rebuild after a content change

```bash
python -B _src/build.py                 # print.html + book/book.json (contents from the page plan)
python -B _src/overflow.py              # must print []
python -B _src/render.py 150            # PDF + page PNGs
python -B tools/import_pdf.py out/TechNext-Services-Catalogue-2026-27.pdf
python -B tools/build_book.py           # viewer pages, search text, hotspots (PDF internal links -> page jumps)
```

Then bump `?v=` in `index.html` if reader.css / reader.js changed.

- Content: `_src/data.py` (facts from technext.asia, Oct 2026; no prices, Odoo never "free", no cyber security). Visuals: `_src/visuals.py`. Styles: `_src/css.py`.
- Viewer: `assets/reader.js`, `assets/reader.css` (TechNext tokens, light only). StPageFlip in `assets/vendor/` is PATCHED - run `python tools/patch_pageflip.py` after any re-download.
