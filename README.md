# TechNext Services Catalogue (Edition 2026/27)

38-page A4 services catalogue for TechNext Pte. Ltd. Unlisted (noindex).

- `index.html` - the catalogue (screen view, prints to A4)
- `out/TechNext-Services-Catalogue-2026-27.pdf` - print/share PDF
- Build: `python -B _src/build.py` -> `python -B _src/overflow.py` (must print `[]`) -> `python -B _src/render.py 150`
- Content: `_src/data.py` (facts from technext.asia, Oct 2026; no prices, Odoo never "free", no cyber security). Visuals: `_src/visuals.py`. Styles: `_src/css.py`.
