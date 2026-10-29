"""TechNext Services Catalogue builder (A5).  python _src/build.py  ->  print.html + book/book.json

A5 since 29 Oct 2026 ("hard to read on laptop and mobile ... reformat to smaller page eg a4 > a5").
Type stays at print sizes (body 9pt, nothing under 8pt except labels), so on screen it reads ~1.4x
larger than the A4 edition; content that no longer fits is split over more pages.
Every page() call is one A5 page. The plan is built first, then page numbers (PMAP), then HTML.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from css import CSS
from data import PRACTICES, S, ODOO_CATS, INDUSTRIES, IND_EXTRA
from industries import IND_DETAIL
from visuals import VIS, oi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITION = "Edition 2026/27"
PR = {p["id"]: p for p in PRACTICES}
PMAP = {}
PLAN = []           # dict(fn, pid, kind, anchor, label)

def page(fn, pid=None, kind="std", anchor=None, label=""):
    PLAN.append(dict(fn=fn, pid=pid, kind=kind, anchor=anchor, label=label))

def pn(a):
    return f"{PMAP.get(a, 0):02d}"

def chrome(n, pid, inner, kind="std", label=""):
    even = n % 2 == 0
    tabs = ""
    if pid:
        tabs = '<div class="tabs">' + "".join(
            f'<a href="#d-{p["id"]}" class="tab{" on" if p["id"] == pid else ""}"><span>{p["n"]} · {p["tab"]}</span></a>' for p in PRACTICES) + "</div>"
    if kind == "bare":
        return f'<section class="page{" even" if even else ""}" id="p{n}">{inner}</section>'
    sect = PR[pid]["name"] if pid else label
    rh = ("" if kind == "div" else
          f'<div class="rh"><div class="l"><img src="assets/logo/technext-horizontal-blue.png" alt="TechNext"><i></i>Services Catalogue</div>'
          f'<div class="r">{sect}{" · <b>" + PR[pid]["n"] + "</b>" if pid else ""}</div></div>')
    rf = f'<div class="rf"><div class="pn">{n:02d}</div><div>{EDITION} · technext.asia · Odoo Ready Partner</div></div>'
    return f'<section class="page{" even" if even else ""}{" div" if kind == "div" else ""}" id="p{n}">{rh}{tabs}{inner}{rf}</section>'

def head(eb, title, lead=None, h="h1", size=None):
    st = f' style="margin-top:3mm{";font-size:" + str(size) + "pt" if size else ""}"'
    out = f'<div class="eyebrow b">{eb}</div><div class="{h}"{st}>{title}</div>'
    if lead:
        out += f'<p class="lead" style="margin-top:3.4mm">{lead}</p>'
    return out

def cont(eb, title=None):
    out = f'<div class="eyebrow b">{eb} · continued</div>'
    if title:
        out += f'<div class="h2" style="margin-top:2.6mm">{title}</div>'
    return out

def ul(items, size=None, gap=None, extra=""):
    li = "".join(f'<li{f" style=\"font-size:{size}pt\"" if size else ""}>{x}</li>' for x in items)
    return f'<ul class="inc" style="{f"gap:{gap}mm;" if gap else ""}{extra}">{li}</ul>'

def sec(letter, title, mt=5):
    return f'<div class="sec-h" style="margin-top:{mt}mm"><span class="n">{letter}</span><span class="t">{title}</span></div>'

def qa(q, a):
    return f'<div class="qa"><div class="q">{q}</div><p>{a}</p></div>'

# ================================================================ front matter
def cover(n):
    return (f'<div class="div" style="position:absolute;inset:0"><div class="grid-bg"></div>'
            '<svg viewBox="0 0 400 400" style="position:absolute;right:-48mm;top:-30mm;width:170mm;height:170mm;opacity:.10"><g fill="none" stroke="#fff" stroke-width=".6">'
            + "".join(f'<circle cx="200" cy="200" r="{r}"/>' for r in range(40, 200, 22)) + '</g></svg>'
            '<img src="assets/logo/technext-horizontal-white.png" style="position:absolute;left:12mm;top:12mm;height:6.4mm" alt="TechNext">'
            '<div style="position:absolute;right:12mm;top:13.4mm;font:700 6.4pt/1 var(--fb);letter-spacing:.16em;color:#9DB3DD;text-transform:uppercase">' + EDITION + '</div>'
            '<div style="position:absolute;left:12mm;right:12mm;top:46mm">'
            '<div class="eyebrow" style="color:#6FA0F5">BIR Compliance · Odoo ERP · Enterprise AI · Websites</div>'
            '<div style="font:800 44pt/.98 var(--fd);color:#fff;letter-spacing:-.04em;margin-top:5mm">Services<br>Catalogue</div>'
            '<div style="width:18mm;height:1.1mm;background:#6FA0F5;margin:7mm 0 6mm"></div>'
            '<div style="font:400 10.6pt/1.5 var(--fb);color:#DDE7F8">Your trusted expert adviser for ERP and compliance. Nineteen services across four practices, led by BIR requirements, set up in your Odoo. You don\'t need to hire your own team.</div>'
            '<a href="#bir-einv" style="display:inline-flex;align-items:center;gap:3mm;margin-top:7mm;background:#FFF4DC;border-radius:99px;padding:2.2mm 4mm 2.2mm 3mm">'
            '<span style="font:800 6.2pt/1 var(--fb);letter-spacing:.14em;color:#A96B00">BIR E-INVOICING DEADLINE</span><span style="font:800 9.4pt/1 var(--fd);color:#0F2350">31 Dec 2026</span></a></div>'
            '<div style="position:absolute;left:12mm;right:12mm;bottom:12mm">'
            '<div style="background:#fff;border-radius:2.2mm;padding:2.2mm 3mm;display:inline-block"><img src="assets/logo/odoo-ready-partner.png" style="height:9mm" alt="Odoo Ready Partner"></div>'
            '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:7mm;padding-top:5mm;border-top:.25mm solid rgba(255,255,255,.25)">' + "".join(
                f'<div><div style="font:800 16pt/1 var(--fd);color:#fff">{v}</div><div style="font:600 6.8pt/1.3 var(--fb);color:#9DB3DD;margin-top:1.4mm">{k}</div></div>'
                for v, k in [("25+", "countries served"), ("90+", "enterprise clients"), ("3", "hubs: SG · PH · VN"), ("4", "practices")]) + '</div></div></div>')

def about1(n):
    return f'''<div class="ct" id="about">{head("About TechNext", 'Your trusted expert adviser for <span class="mk">ERP and compliance.</span>')}
<p class="lead" style="margin-top:5mm">TechNext Pte. Ltd. is a Singapore-based Odoo Ready Partner. For Philippine companies we lead with Odoo, set up by our own experts for BIR requirements: e-invoicing planning, CAS or CBA books, 2307s and alphalists. We also implement Odoo ERP end to end, build enterprise AI, and run websites and brand design.</p>
<p class="p" style="margin-top:3.6mm">Sales, discovery and on-site work run from our Singapore headquarters. Odoo configuration, custom modules and integrations are built at our main development and consulting hub in Taguig City, Metro Manila, and our AI engineers in Ho Chi Minh City join whenever AI is in scope. One project, one team, and the same people after go-live.</p>
<div class="card w" style="margin-top:6mm;padding:5mm"><div class="eyebrow" style="color:var(--navy)">How we work</div>
{ul(["<b>Discovery before a pitch.</b> We map how the business runs before we propose anything.", "<b>Standard first.</b> Configure before customising; custom only where it earns its place.",
     "<b>Written scope and quotation.</b> You see what is included, and what is not, before work starts.", "<b>Yours to keep.</b> Accounts, data, sites and master files stay in your name."], extra="margin-top:3mm")}</div></div>'''

def about2(n):
    stats = "".join(f'<div class="stat"><div class="v">{v}</div><div class="k">{k}</div></div>' for v, k in
                    [("25+", "Countries with clients"), ("90+", "Enterprise clients"), ("3", "Hubs in Singapore, the Philippines and Vietnam"), ("31 Dec", "BIR e-invoicing deadline, 2026")])
    cards = "".join(f'<a href="#d-{p["id"]}" class="card" style="display:flex;flex-direction:column;gap:1.6mm{";border:.5mm solid var(--blue)" if p["id"] == "bir" else ""}">'
                    f'<div style="font:800 17pt/1 var(--fd);color:var(--mist)">{p["n"]}</div><div class="h3">{p["name"]}</div>'
                    f'<div class="ps">{p["lead"].split(". ")[0].rstrip(".")}.</div></a>' for p in PRACTICES)
    return f'''<div class="ct">{cont("About TechNext", 'Four practices, <span class="mk">one team.</span>')}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm 6mm;margin-top:5mm;padding-top:5mm;border-top:.5mm solid var(--ink)">{stats}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:3.4mm;margin-top:6mm">{cards}</div>
<div class="small" style="margin-top:auto;padding-top:4mm">TechNext Pte. Ltd. · UEN 202699888G · 261 Waterloo Street, #03-36, Waterloo Centre, Singapore 180261</div></div>'''

def _crow(code, name, a, guide=False):
    return (f'<a href="#{a}" style="display:grid;grid-template-columns:15mm 1fr 8mm;align-items:baseline;padding:1.7mm 0;border-bottom:.25mm solid var(--line)">'
            f'<span style="font:700 6.6pt/1 var(--fb);letter-spacing:.1em;color:{"var(--muted)" if guide else "var(--blue)"}">{code}</span>'
            f'<span style="font:{"500" if guide else "600"} 8.8pt/1.3 var(--fb);color:{"var(--body)" if guide else "var(--ink)"}">{name}</span>'
            f'<span style="text-align:right;font:700 8.8pt/1 var(--fd);color:var(--ink)">{pn(a)}</span></a>')

CEXTRA = {"bir": [("bir-pains", "Where BIR compliance hurts"), ("bir-check", "BIR self-check"), ("bir-rules", "The BIR rules and what Odoo covers")],
          "erp": [("odoo-apps", "Odoo apps we implement"), ("method", "Our implementation method"), ("hosting", "Where Odoo runs")],
          "ai": [("ai-principles", "How our AI stays in control")], "mkt": [("offer", "Website design with your Odoo")]}

def cblock(p):
    rows = "".join(_crow(s["code"], s["name"], s["id"]) for s in S if s["p"] == p["id"])
    rows += "".join(_crow("GUIDE", t, a, True) for a, t in CEXTRA[p["id"]])
    return (f'<div><a href="#d-{p["id"]}" style="display:flex;align-items:baseline;gap:3mm;padding-bottom:2mm;border-bottom:.5mm solid var(--ink)">'
            f'<span style="font:800 14pt/1 var(--fd);color:var(--blue)">{p["n"]}</span><span class="h3">{p["name"]}</span>'
            f'<span style="margin-left:auto;font:700 8.8pt/1 var(--fd);color:var(--ink)">{pn("d-" + p["id"])}</span></a>{rows}</div>')

def contents1(n):
    return f'''<div class="ct" id="contents">{head("Contents", 'BIR compliance first. <span class="mk">One team throughout.</span>')}
<div style="margin-top:6mm">{cblock(PRACTICES[0])}</div>
<div class="card w" style="margin-top:6mm;padding:4.4mm"><div class="h4">Reading this catalogue</div><p class="ps" style="margin-top:1.6mm">Each service has a reference code (for example <b>ERP-01</b>). Quote the codes you're interested in when you write to <b>sales@technext.asia</b>, and we'll come back with a written scope. Screens marked <span class="tag am">Sample data</span> are illustrations, not client data.</p></div></div>'''

def contents2(n):
    return f'<div class="ct">{cont("Contents")}<div style="margin-top:4mm;display:flex;flex-direction:column;gap:7mm">{cblock(PRACTICES[1])}{cblock(PRACTICES[2])}</div></div>'

def contents3(n):
    ref = [("industries", "Odoo by industry"), ("ind-retail", "Industry sheets: the modules inside, flow and rollout"), ("local", "Localisation: Singapore, the Philippines, Vietnam"),
           ("offices", "Where we work"), ("start", "How to start")]
    refs = "".join(f'<a href="#{a}" style="display:grid;grid-template-columns:1fr 8mm;padding:1.7mm 0;border-bottom:.25mm solid var(--line)"><span style="font:600 8.8pt/1.3 var(--fb);color:var(--ink)">{t}</span>'
                   f'<span style="text-align:right;font:700 8.8pt/1 var(--fd);color:var(--ink)">{pn(a)}</span></a>' for a, t in ref)
    return (f'<div class="ct">{cont("Contents")}<div style="margin-top:4mm;display:flex;flex-direction:column;gap:7mm">{cblock(PRACTICES[3])}'
            f'<div><div style="padding-bottom:2mm;border-bottom:.5mm solid var(--ink)" class="h3">Reference</div>{refs}</div></div></div>')

def anatomy1(n):
    models = [("Project", "One-off, scoped and quoted in writing before work begins.", "BIR set-up · implementation · customisation · AI · websites · brand"),
              ("Monthly retainer", "A steady monthly plan, scoped to channels and volume.", "Social media management"),
              ("Support plan", "Agreed response targets, tracked on every ticket.", "Odoo support after go-live"),
              ("Standalone discovery", "A written scope that is yours to keep, with or without us.", "Odoo consultation &amp; discovery")]
    cards = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:2mm"><div style="display:flex;align-items:center;gap:2.4mm"><span style="font:800 8.4pt/1 var(--fd);color:#fff;background:var(--blue);border-radius:1.2mm;padding:1.2mm 1.7mm">0{i + 1}</span></div>'
                    f'<div class="h3">{t}</div><p class="ps">{d}</p><div style="margin-top:6mm;padding-top:2mm;border-top:.25mm solid var(--line);font:600 7.6pt/1.4 var(--fb);color:var(--muted)">Used for: <span style="color:var(--ink)">{u}</span></div></div>'
                    for i, (t, d, u) in enumerate(models))
    return f'''<div class="ct" id="anatomy">{head("How we engage", 'Every engagement starts with <span class="mk">a written scope.</span>',
"We don't publish a price list, because no two businesses run the same way. Tell us what's manual today, and we come back with a scope and a quotation that states what is included and what is not. Nothing commits you until you say so.")}
<div style="display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:3.4mm;margin-top:6mm">{cards}</div></div>'''

def anatomy2(n):
    notes = [("Odoo licences", "Billed by Odoo, per user per month, in your name. Our work is quoted separately, so you can see each part clearly."),
             ("Ownership", "Databases, websites, social accounts, analytics and master files stay in your name, handed over completely."),
             ("Approval", "Pages, posts and assets are shared for sign-off. AI waits for a person before anything irreversible.")]
    parts = [("Reference code", "Quote it when you write to us, for example BIR-01"), ("What it is", "The service in one headline and a short summary"),
             ("Illustrated workflow", "A drawn diagram or sample screen, never client data"), ("What's included", "What the scope covers"),
             ("Specification", "Who it suits, how it is delivered and what you keep"), ("Odoo apps involved", "The apps the work touches, where there are any"),
             ("Questions clients ask", "Short answers to what we hear most")]
    nt = "".join(f'<div style="padding:3mm 0;border-bottom:.25mm solid var(--line)"><div class="h4">{t}</div><p class="ps" style="margin-top:1mm">{d}</p></div>' for t, d in notes)
    pt = "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr;gap:2mm;padding:1.6mm 0;border-top:.25mm solid rgba(49,103,202,.18)"><span style="font:800 8pt/1.4 var(--fd);color:var(--blue)">{i + 1}</span>'
                 f'<div style="font-size:8.6pt;line-height:1.4"><b>{t}.</b> {d}</div></div>' for i, (t, d) in enumerate(parts))
    return f'''<div class="ct">{cont("How we engage", 'Clear on cost, <span class="mk">ownership and sign-off.</span>')}
<div style="margin-top:4mm;border-top:.5mm solid var(--ink)">{nt}</div>
<div class="card w" style="margin-top:6mm"><div class="h3">Service page anatomy</div><div style="margin-top:2.4mm">{pt}</div></div></div>'''

def divider(n, p):
    lst = "".join(f'<a href="#{s["id"]}"><span>{s["code"]}</span>{s["name"]}<em>p. {pn(s["id"])}</em></a>' for s in S if s["p"] == p["id"])
    return (f'<div class="grid-bg"></div><div class="num">{p["n"]}</div>'
            '<img class="foot-logo" src="assets/logo/technext-horizontal-white.png" alt="TechNext">'
            f'<div class="in" id="d-{p["id"]}"><div class="eyebrow">Practice {p["n"]} · {p["name"]}</div><div class="h1">{p["title"]}</div>'
            f'<p class="lead">{p["lead"]}</p><div class="list">{lst}</div></div>')

# ================================================================ service pages (2 each)
def service_a(n, s):
    meta = "".join(f'<div><span>{k}</span><b>{v}</b></div>' for k, v in s["meta"])
    return f'''<div class="sv" id="{s["id"]}">
<div style="display:flex;gap:2mm;align-items:center"><span class="ref"><i></i>{s["code"]}</span><span class="eyebrow">{s["name"]}</span></div>
<div class="h1" style="font-size:20pt;margin-top:3.4mm">{s["title"]}</div><p class="lead" style="font-size:9.6pt;margin-top:3mm">{s["lead"]}</p>
<div class="meta2">{meta}</div><div class="slotA"></div>
<div class="vis" style="margin-top:auto">{VIS[s["vis"]]()}</div></div>'''

def service_b(n, s):
    spec = "".join(f'<div class="r"><span>{k}</span><div>{v}</div></div>' for k, v in s["spec"])
    if s["apps"]:
        names = {a: nm for _, apps in ODOO_CATS for a, nm, _, _ in apps}
        names.update({"web_studio": "Studio", "accountant": "Invoicing", "iot": "IoT"})
        spec += '<div class="r"><span>Odoo apps</span><div class="apps">' + "".join(f'<span class="chip">{oi(a, 3.4)}{names.get(a, a)}</span>' for a in s["apps"]) + '</div></div>'
    faq = "".join(qa(q, a) for q, a in s["faq"])
    return f'''<div class="sv">
<div style="display:flex;gap:2mm;align-items:center"><span class="ref"><i></i>{s["code"]}</span><span class="eyebrow">{s["name"]} · continued</span></div>
{sec("A", "What's included", 4)}{ul(s["inc"], gap=1.5)}
<div class="specblk">{sec("B", "Specification", 4.4)}<div class="spec">{spec}</div></div>
<div style="margin-top:2mm">{sec("C", "Questions clients ask", 4)}<div class="faq">{faq}</div></div></div>'''

# ================================================================ BIR guides
PAINS = [("Invoices that can't be sent", "A printed or emailed PDF. If the system can't transmit sales data to the BIR, it needs work before 31 December 2026.", "Invoice flows set up in Odoo; how invoice data reaches the EIS is scoped with you", "BIR-01"),
         ("2307s typed by hand", "Certificates re-typed and chased every quarter.", "2306 and 2307 PDFs generated on vendor bills and, if requested, sent with the payment", "BIR-03"),
         ("Month-end in Excel", "SLSP, SAWT and QAP rebuilt from spreadsheets.", "DAT exports from the same entries as your books", "BIR-03"),
         ("Missing customer 2307s", "A missing certificate is a credit you can't claim.", "Each received 2307 attached to its invoice, with the gaps listed for follow-up", "BIR-03"),
         ("CAS paperwork", "A system description and sample outputs written from scratch.", "The application pack printed from the Odoo you will actually use", "BIR-02"),
         ("Upgrades and the registration", "A major change adopted without an updated registration leaves the registration without effect from that date.", "The registration update planned alongside each Odoo upgrade", "BIR-02"),
         ("Branches doing it differently", "Each branch with its own spreadsheet and invoice habits.", "One database: each branch its own journal and series, one consolidated 2550Q", "BIR-01"),
         ("Digging for an audit", "Ten days to answer an eLA request, with records in five places.", "Audit trail, locked periods and attachments: easier to find and export", "BIR-04")]
BIR_IDS = {"BIR-01": "bir-einv", "BIR-02": "bir-cas", "BIR-03": "bir-forms", "BIR-04": "bir-audit"}

def _pains(rows):
    hd = ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;padding:1.6mm 0;border-bottom:.5mm solid var(--ink)">'
          '<span class="eyebrow">Today</span><span class="eyebrow b">In Odoo, set up by TechNext</span></div>')
    return hd + "".join(f'<div style="padding:2.6mm 0;border-bottom:.25mm solid var(--line)"><div style="display:flex;align-items:center;gap:2.4mm"><div class="h4">{t}</div>'
                        f'<a href="#{BIR_IDS[c]}" class="ref" style="margin-left:auto;flex:none"><i></i>{c}</a></div>'
                        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:1.4mm"><p class="ps" style="color:var(--muted)">{a}</p><p class="ps" style="color:var(--ink)">{b}</p></div></div>'
                        for t, a, b, c in rows)

def bir_pains1(n):
    return f'''<div class="ct" id="bir-pains">{head("BIR compliance · Where it hurts", 'What finance teams tell us <span class="mk">before an Odoo project.</span>',
"Eight BIR pains we hear in almost every Philippine discovery call, and what changes once the BIR work lives in one system. Each row points to the service that addresses it.")}
<div style="margin-top:4mm">{_pains(PAINS[:4])}</div></div>'''

def bir_pains2(n):
    who = [("E-commerce sellers", "Small, medium or large", "Covered"), ("LTS accounts", "Large Taxpayers Service", "Covered"), ("Large taxpayers", "RA 11976, RR 8-2024", "Covered"),
           ("CAS or CBA users", "With invoicing software", "Covered"), ("Micro taxpayers", "Any channel", "Exempt")]
    wc = "".join(f'<div style="background:#fff;border-radius:2mm;padding:2.4mm 2.8mm"><span class="tag {"ok" if s == "Exempt" else "am"}">{s}</span><div class="h4" style="margin-top:1.4mm;font-size:8.6pt">{t}</div>'
                 f'<div style="font:500 7.6pt/1.35 var(--fb);color:var(--muted);margin-top:.6mm">{d}</div></div>' for t, d, s in who)
    return f'''<div class="ct">{cont("BIR compliance · Where it hurts")}<div style="margin-top:3mm">{_pains(PAINS[4:])}</div>
<div class="card w" style="margin-top:auto;padding:4mm"><div class="h3">Who must e-invoice by 31 December 2026</div><div style="font:600 7pt/1 var(--fb);color:var(--muted);margin-top:1.4mm">RR 26-2025 · RMC 98-2026</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm;margin-top:3mm">{wc}</div>
<p style="font-size:7.8pt;line-height:1.4;margin-top:2.6mm;color:var(--muted)">The BIR Commissioner can require other taxpayers to comply; exporters, incentive-registered enterprises and POS users join later. We confirm your group with your accountant in discovery.</p></div></div>'''

CHECK = [("E-invoicing", "bir-einv", "BIR-01", ["We know whether we are covered by the 31 December 2026 deadline", "Our system can transmit invoice data to the BIR's EIS, not just print it", "We have a plan for corrections and for system downtime"]),
         ("Registration", "bir-cas", "BIR-02", ["Our accounting system is registered as a CAS or CBA for the system we use today", "We registered our computerised books in ORUS this year", "No upgrade or new module has changed the system since we registered"]),
         ("Forms and withholding", "bir-forms", "BIR-03", ["Our 2307s are generated from bills, not typed by hand", "SLSP, SAWT and QAP come from our books, not a separate spreadsheet", "Our invoices show creditable withholding as a separate item (RR 6-2026)"]),
         ("Audit", "bir-audit", "BIR-04", ["We could produce an examiner's checklist within 10 calendar days", "Each period is locked after its returns are filed", "Every bill and invoice is stored with its source document"])]

def _check(groups):
    box = '<span style="width:4.2mm;height:4.2mm;border:.35mm solid var(--navy);border-radius:1mm;flex:none;margin-top:.2mm"></span>'
    return "".join(f'<div class="card" style="padding:4mm;display:flex;flex-direction:column;gap:2mm"><div style="display:flex;align-items:center;justify-content:space-between"><div class="h3">{t}</div><a href="#{a}" class="ref"><i></i>{c}</a></div>'
                   + "".join(f'<div style="display:flex;gap:2.6mm;align-items:flex-start;padding:1.6mm 0 0;border-top:.25mm solid var(--line);font:500 8.8pt/1.4 var(--fb);color:var(--ink)">{box}<span>{q}</span></div>' for q in qs) + '</div>'
                   for t, a, c, qs in groups)

def bir_check1(n):
    return f'''<div class="ct" id="bir-check">{head("BIR compliance · Self-check", 'Twelve questions. <span class="mk">Tick what is true today.</span>',
'Three or more boxes left empty, or "not sure"? Bring these pages to a discovery call. An adviser will say what Odoo covers, what it takes, and what to do first before 31 December 2026.')}
<div style="display:flex;flex-direction:column;gap:3.4mm;margin-top:6mm">{_check(CHECK[:2])}</div></div>'''

def bir_check2(n):
    path = [("Confirm your group", "With your accountant: covered now, later, or exempt"), ("Map your invoice flows", "Invoices, credit notes, branches, anything issued outside your system"),
            ("Set up the localisation", "Taxes, withholding, BIR reports and invoice layouts, tested on your data"), ("Plan the EIS route", "What your Odoo version and hosting would need, quoted separately"),
            ("Prepare PTI papers", "You apply; we prepare the process flow and sample invoices from your Odoo"), ("Go live and stay on", "Downtime and correction flows set up before go-live, then support")]
    steps = "".join(f'<div style="background:#fff;border-radius:2mm;padding:2.6mm 3mm"><div style="font:800 11pt/1 var(--fd);color:var(--blue)">{i + 1}</div><div class="h4" style="margin-top:1.2mm;font-size:8.6pt">{t}</div>'
                    f'<div style="font:500 7.6pt/1.35 var(--fb);color:var(--muted);margin-top:.8mm">{d}</div></div>' for i, (t, d) in enumerate(path))
    return f'''<div class="ct">{cont("BIR compliance · Self-check")}<div style="display:flex;flex-direction:column;gap:3.4mm;margin-top:3mm">{_check(CHECK[2:])}</div>
<div class="card w" style="margin-top:6mm;padding:4mm"><div class="h4">From "are we covered?" to an e-invoicing plan for your Odoo</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.2mm;margin-top:2.8mm">{steps}</div></div></div>'''

def bir_rules1(n):
    rules = [("RR 7-2024 (EOPT Act)", "11 Apr 2024", "The invoice replaces the official receipt as proof of sale"),
             ("RR 8-2024", "11 Apr 2024", "Taxpayer classes, micro to large, that decide whether e-invoicing applies now"),
             ("RMC 5-2021 · RMO 9-2021", "2021", "CAS and CBA registration: Acknowledgement Certificate, no Permit to Use"),
             ("RMC 4-2026", "15 Jan 2026", "Computerised books registered online through ORUS, every year"),
             ("RR 26-2025", "5 Sep 2025", "E-invoicing deadline moved to 31 December 2026 for the covered groups"),
             ("RMC 98-2026", "22 Sep 2026", "Working rules: PTI first, EIS Certification within six months, no edits after issue, every branch"),
             ("RMC 110-2026", "12 Oct 2026", "Accreditation rules for e-invoicing service providers"),
             ("RR 6-2026", "In force 16 Oct 2026", "Creditable withholding tax shown as a separate item on invoices"),
             ("RMO 22-2026", "24 Aug 2026", "Audits need a valid eLA, TVN or Mission Order; documents due in 10 days")]
    tb = ('<table class="tbl"><tr><th style="width:40mm">Issuance · date</th><th>What it means for your system</th></tr>'
          + "".join(f'<tr><td><b style="color:var(--ink)">{a}</b><br><span style="font-weight:500">{b}</span></td><td>{c}</td></tr>' for a, b, c in rules) + '</table>')
    return f'''<div class="ct" id="bir-rules">{head("BIR compliance · The rules behind it", 'The issuances that shape <span class="mk">your Odoo setup.</span>',
"The BIR registers your business and your system, not a software brand.")}<div style="margin-top:6mm">{tb}</div></div>'''

def bir_rules2(n):
    odoo = ["Invoice layouts for BIR and CAS requirements, and a Book of Accounts for CAS and CBA", "BIR 2306 and 2307 certificates as PDFs, generated on vendor bills",
            "SLSP, SAWT and QAP with DAT exports, the 2550Q, 1600-VT and 2551Q", "Basic PH payroll: 1601-C items, 2316, 1604-C worksheets"]
    tn = ["No EIS connection: Odoo has none built in and TechNext has not built one; any connection is quoted separately", "Invoice layouts and branch flows checked against the guidelines",
          "Credit-note and manual-invoice catch-up set up before go-live", "Sample outputs and process flow for the CAS and PTI applications you file"]
    return f'''<div class="ct">{cont("BIR compliance · The rules behind it")}
<div class="card" style="margin-top:3mm"><div style="display:flex;align-items:center;gap:2.4mm">{oi("account", 6)}<div class="h3">What Odoo 20 already does</div></div>{ul(odoo, gap=1.4, extra="margin-top:2.6mm")}</div>
<div class="card" style="margin-top:3mm;border:.5mm solid var(--blue)"><div style="display:flex;align-items:center;gap:2.4mm"><img src="assets/logo/technext-horizontal-blue.png" style="height:4.6mm" alt="TechNext"><div class="h3">adds</div></div>{ul(tn, gap=1.4, extra="margin-top:2.6mm")}</div>
<div class="card w" style="margin-top:6mm;padding:4mm"><div class="h4">About "BIR-accredited" claims</div><p style="font-size:8pt;line-height:1.42;margin-top:1.2mm">In its public advisory of 14 September 2026, the BIR said it has not accredited or endorsed any e-invoicing service provider. We say Odoo is set up for BIR requirements; the CAS registration and the PTI are issued to your business. <b>TechNext is an Odoo Ready Partner.</b> We are not affiliated with, accredited by or acting for the BIR or any government agency, and we do not file or register on your behalf.</p></div>
<div class="small" style="margin-top:2.4mm">BIR issuances as available on 21 October 2026, summarised on technext.asia (bir-e-invoicing and the BIR guides). General guidance, not tax advice: confirm with your accountant or RDO before acting.</div></div>'''

# ================================================================ ERP guides
def _apps(cats):
    out = ""
    for cat, apps in cats:
        rows = "".join(f'<div style="display:flex;gap:2.4mm;align-items:center;padding:1.7mm 0;border-bottom:.25mm solid var(--line)">{oi(a, 6)}'
                       f'<div style="flex:1;min-width:0"><div style="font:700 8.8pt/1.2 var(--fd);color:var(--ink);display:flex;gap:1.6mm;align-items:center">{nm}{" <span class=\"tag bl\">Focus</span>" if f else ""}</div>'
                       f'<div style="font:500 7.8pt/1.3 var(--fb);color:var(--muted)">{d}</div></div></div>' for a, nm, d, f in apps)
        out += f'<div><div style="padding-bottom:1.6mm;border-bottom:.5mm solid var(--ink)" class="eyebrow"><span style="color:var(--ink)">{cat}</span></div>{rows}</div>'
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm 5mm">{out}</div>'

def apps1(n):
    return f'''<div class="ct" id="odoo-apps">{head("Odoo apps we implement", 'The full suite, <span class="mk">one database.</span>',
"We implement the full Odoo suite, and our first focus is Accounting, Sales and Inventory. Every app shares the same customers, products and accounts, so adding one later needs no integration project.")}
<div style="margin-top:6mm">{_apps(ODOO_CATS[:2])}</div></div>'''

def apps2(n):
    return f'<div class="ct" id="odoo-apps-2">{cont("Odoo apps we implement")}<div style="margin-top:3mm">{_apps(ODOO_CATS[2:4])}</div></div>'

def apps3(n):
    return f'<div class="ct">{cont("Odoo apps we implement")}<div style="margin-top:3mm">{_apps(ODOO_CATS[4:6])}</div></div>'

def apps4(n):
    return (f'<div class="ct">{cont("Odoo apps we implement")}<div style="margin-top:3mm">{_apps(ODOO_CATS[6:])}</div>'
            '<div class="small" style="margin-top:auto">Odoo app icons are Odoo S.A. marks, shown in their own colours. Licences are billed by Odoo per user per month; Odoo&#8217;s One App Free plan covers a single app.</div></div>')

def method1(n):
    steps = [("Discovery", "We map how orders, stock and money move today and match each step to an Odoo app. Output: a written scope."),
             ("Configuration", "Apps set up on a staging copy, never on live data. Standard features first."),
             ("Data migration", "Customers, vendors and products in full; opening balances and open items. The old system stays for history."),
             ("Training &amp; UAT", "Role-based sessions on your own data; your team runs real tasks end to end."),
             ("Integration", "Banks, payments, stores and the tools you keep, tested on staging with real records."),
             ("Go-live &amp; support", "Cut-over on an agreed date, then support, fixes, month-end help and upgrades.")]
    cards = "".join(f'<div style="display:grid;grid-template-columns:13mm 1fr;gap:3mm;padding:2.8mm 0;border-bottom:.25mm solid var(--line)">'
                    f'<div style="font:800 17pt/1 var(--fd);color:{"var(--blue)" if i < 5 else "var(--deep)"};letter-spacing:-.04em">0{i + 1}</div>'
                    f'<div><div class="h3">{t}</div><p class="ps" style="margin-top:1mm">{d}</p></div></div>' for i, (t, d) in enumerate(steps))
    return f'''<div class="ct" id="method">{head("Our implementation method", 'Six steps, <span class="mk">one team throughout.</span>')}
<div style="border-top:.5mm solid var(--ink);margin-top:6mm">{cards}</div></div>'''

def method2(n):
    need = ["A short description of how your process runs today", "A decision-maker for scope questions",
            "The people who run sales, stock and finance, for discovery and training", "Access to the data you want to bring across"]
    return f'''<div class="ct">{cont("Our implementation method", 'What we need, and <span class="mk">what goes first.</span>')}
<div class="card w" style="margin-top:5mm;padding:5mm"><div class="eyebrow" style="color:var(--navy)">What we need from you</div>{ul(need, extra="margin-top:3mm")}</div>
<div class="card" style="margin-top:3.4mm;padding:5mm"><div class="eyebrow">Timeline</div><p class="p" style="margin-top:2mm">It depends on the number of apps, companies and integrations, and how clean your data is. The timeline is agreed in the written scope at the end of discovery, and the first phase is kept focused so it goes live sooner.</p></div>
<div class="card" style="margin-top:3.4mm;padding:5mm"><div class="eyebrow">Phase 1</div><div style="display:flex;gap:3mm;margin-top:3mm">{"".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;flex:1">{oi(a, 9)}<span style="font:700 8pt/1 var(--fb);color:var(--ink)">{t}</span></div>' for a, t in [("account", "Accounting"), ("sale", "Sales"), ("stock", "Inventory")])}</div>
<p class="ps" style="margin-top:3mm;color:var(--muted)">Where money and stock move. Everything else joins the same database later.</p></div></div>'''

HOST = [("Best for", "Fastest start on standard apps", "Custom development with staging and version control", "Data residency or existing infrastructure"),
        ("Our default", "Most first phases", "When a requirement needs custom code", "Only when IT policy or data rules require it"),
        ("Custom modules", "No. Configuration, plus Studio on the Custom plan", "Yes, version-controlled", "Yes"),
        ("Hosting cost", "Included in the Odoo subscription", "Hosting fees on top of the Custom plan", "Your own infrastructure and operations"),
        ("Upgrades", "Managed by Odoo", "Tested on staging, then scheduled", "Planned and run with you"),
        ("Environments", "Production", "Production, staging and development branches", "As your infrastructure allows"),
        ("Typical client", "Small teams on standard processes", "Growing companies and groups with custom needs", "Regulated or infrastructure-led organisations"),
        ("Move later?", "Yes, to Odoo.sh or on-premise, tested on a copy before switching", "—", "—")]

def _host(rows):
    return ('<table class="tbl" style="font-size:8pt"><tr><th style="width:21mm"></th><th>Odoo Online</th><th class="hi">Odoo.sh</th><th>On-premise / your cloud</th></tr>'
            + "".join(f'<tr><td>{a}</td><td>{b}</td><td class="hi">{c}</td><td>{d}</td></tr>' for a, b, c, d in rows) + '</table>')

def hosting1(n):
    return f'''<div class="ct" id="hosting">{head("Where Odoo runs", 'Hosting is a <span class="mk">scoping decision.</span>',
"We recommend hosting during discovery, based on whether you need custom modules and any data-residency rules, never by default.")}<div style="margin-top:6mm">{_host(HOST[:5])}</div></div>'''

def hosting2(n):
    cards = "".join(f'<div class="card w" style="padding:3.4mm"><div class="h4" style="font-size:8.8pt">{t}</div><p style="font-size:8pt;line-height:1.4;margin-top:1.2mm">{d}</p></div>' for t, d in [
        ("Standard first", "Configuration, then Studio, then custom modules, the lightest option that meets the requirement."),
        ("Upgrade-safe", "Custom work is built as separate modules, so version upgrades stay predictable."),
        ("Your account", "The Odoo subscription and database are in your name. You can export your data at any time.")])
    return f'''<div class="ct">{cont("Where Odoo runs")}<div style="margin-top:3mm">{_host(HOST[5:])}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.6mm;margin-top:5mm">{cards}</div>
<div class="card" style="margin-top:6mm;display:grid;grid-template-columns:1fr 1fr;gap:5mm;padding:4mm">
 <div><div class="eyebrow">Odoo licences</div><p class="ps" style="margin-top:1.6mm">Priced per user per month by Odoo, and paid to Odoo. Prices differ by country and currency; see odoo.com/pricing for your market.</p></div>
 <div><div class="eyebrow">Implementation</div><p class="ps" style="margin-top:1.6mm">Quoted by TechNext in writing: configuration, data migration, training and integration, with support options after go-live.</p></div></div></div>'''

# ================================================================ AI + websites guides
def ai1(n):
    disc = [("RAG knowledge assistants", "Answers from your documents, cited", "AI-01", "ai-rag"), ("AI inside Odoo", "Capture, drafting and lookups in the ERP", "AI-02", "ai-odoo"),
            ("Workflow automation agents", "Multi-step work prepared for release", "AI-03", "ai-auto"), ("AI chatbots", "Web, WhatsApp and in-app, with hand-off", "AI-04", "ai-bot")]
    cards = "".join(f'<a href="#{a}" class="card" style="display:flex;flex-direction:column;gap:1.6mm"><span class="ref" style="align-self:flex-start"><i></i>{c}</span><div class="h3" style="margin-top:1.4mm">{t}</div><div class="ps">{d}</div></a>' for t, d, c, a in disc)
    faq = "".join(f'<div style="padding:2.6mm 0;border-top:.25mm solid rgba(49,103,202,.2)"><div class="h4">{q}</div><p class="ps" style="margin-top:1mm">{a}</p></div>' for q, a in [
        ("Do we have to be on Odoo?", "No. Assistants, agents and chatbots work with the tools you already use. AI inside Odoo is for teams running the ERP."),
        ("Who builds it?", "Our AI engineering hub in Ho Chi Minh City, alongside the Singapore and Taguig City teams on the same project."),
        ("How is it priced?", "On quotation, scoped to the task and the data involved, with a written scope first.")])
    return f'''<div class="ct" id="ai-principles">{head("Enterprise AI · Four disciplines", 'Start with the task that removes <span class="mk">the most manual hours.</span>')}
<div style="display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:3mm;margin-top:5mm">{cards}</div>
<div class="card w" style="margin-top:6mm;padding:4mm 4.4mm">{faq}</div></div>'''

def ai2(n):
    pr = [("Grounded", "Answers come from your own sources and cite them. When documents don't cover a question, it says so."),
          ("Human-approved", "Anything that moves money, commitments or customer data waits for a person."),
          ("Logged", "Every action is logged against the record it touched, and can be replayed or rolled back."),
          ("Scoped", "Access is limited to what each task needs; retrieval follows your access rules."),
          ("Private", "Data stays in your environment; private-cloud or on-premise models where it can't leave."),
          ("Measured", "Accuracy is checked on your own documents before anything runs unattended.")]
    items = "".join(f'<div style="border-left:.8mm solid var(--blue);padding-left:3.4mm"><div class="h3">{t}</div><p class="ps" style="margin-top:1.2mm">{d}</p></div>' for t, d in pr)
    return f'''<div class="ct">{cont("Enterprise AI", 'How our AI <span class="mk">stays in control.</span>')}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm 5mm;margin-top:7mm">{items}</div></div>'''

def offer1(n):
    free = ["Custom multi-page website design, styled to your brand", "Your choice of look, colours and layout, with rounds of changes",
            "Setting up the Website app in your Odoo database", "Contact form, mobile layout and basic SEO", "One hand-over call to show your team how to edit it"]
    pay = ["Your Odoo subscription, paid to Odoo at Odoo's price", "More Odoo apps (CRM, invoicing, inventory, HR) if you add them",
           "Your domain name, if you don't have one yet", "Extra pages, an online shop or support, only if you ask"]
    return f'''<div class="ct" id="offer">{head("Website design with your Odoo", 'We design your website on Odoo. <span class="mk">One system with your sales.</span>',
"Our designers build a full multi-page website around your brand and set it up in your Odoo. It runs on your own Odoo subscription, ready for more apps, with the scope, timeline and quotation agreed with you in writing before we start.")}
<div class="card" style="margin-top:6mm;border:.5mm solid var(--blue)"><div class="eyebrow b">What we design and set up</div>{ul(free, gap=1.4, extra="margin-top:2.6mm")}</div>
<div class="card" style="margin-top:3mm"><div class="eyebrow">Also to plan for</div>{ul(pay, gap=1.4, extra="margin-top:2.6mm")}
<p style="font-size:8pt;margin-top:2.4mm;color:var(--muted)">Our design work and every other cost are quoted in writing before we start.</p></div></div>'''

def offer2(n):
    steps = [("Step 1", "Tell us", "Send the form. We reply within one working day, book a 20-minute call about your business and the style you like, then send a written quotation."),
             ("Step 2", "We build it", "On a timeline agreed with you before we start, we design your website in your Odoo. You review it."),
             ("When you're ready", "Grow on the same system", "Add CRM, invoicing or inventory later. No moving data, no second system.")]
    st = "".join(f'<div style="display:grid;grid-template-columns:30mm 1fr;gap:4mm;padding:3.4mm 0;border-bottom:.25mm solid var(--line)"><div class="eyebrow b" style="padding-top:.8mm">{d}</div><div><div class="h3">{t}</div><p class="ps" style="margin-top:1.2mm">{x}</p></div></div>' for d, t, x in steps)
    return f'''<div class="ct">{cont("Website design with your Odoo", 'How it runs, <span class="mk">step by step.</span>')}
<div style="margin-top:5mm;border-top:.5mm solid var(--ink)">{st}</div>
<div class="card w" style="margin-top:6mm;padding:4.4mm">
 <div class="h4">Who owns the website and the data?</div><p class="ps" style="margin-top:1.2mm">You do. The Odoo subscription and database are in your name, and you can export your data or move to another partner at any time.</p>
 <div class="h4" style="margin-top:3.4mm">I need an online shop or a special feature.</div><p class="ps" style="margin-top:1.2mm">Tell us in the form. Online shops, bookings or custom features are scoped in the same written quotation.</p></div>
<div class="small" style="margin-top:3mm">Ask for a quotation at technext.asia/quotation. Odoo itself is not free; your website runs on your own Odoo subscription, which you pay to Odoo.</div></div>'''

# ================================================================ industries
def ind_no(name):
    return [i[0] for i in INDUSTRIES].index(name) + 1

def industries_index(n):
    rows = ""
    for k, (name, img, apps, desc, pts) in enumerate(INDUSTRIES):
        slug = IND_DETAIL[name]["slug"]
        rows += (f'<a href="#ind-{slug}" style="display:grid;grid-template-columns:24mm 1fr 9mm;gap:3mm;align-items:center;padding:2.3mm 0;border-bottom:.25mm solid var(--line)">'
                 f'<div style="display:flex;gap:1.2mm">{"".join(oi(a, 6.4) for a in apps)}</div>'
                 f'<div><div style="display:flex;gap:2mm;align-items:baseline"><span style="font:700 6.4pt/1 var(--fb);letter-spacing:.12em;color:var(--blue)">0{k + 1}</span><span class="h4">{name}</span></div>'
                 f'<div style="font:500 7.8pt/1.38 var(--fb);color:var(--muted);margin-top:.8mm">{desc}</div></div>'
                 f'<span style="text-align:right;font:700 8.8pt/1 var(--fd);color:var(--ink)">{pn("ind-" + slug)}</span></a>')
    return f'''<div class="ct" id="industries">{head("Odoo by industry", 'Built around <span class="mk">how your sector works.</span>',
"Four pages per sector: the apps we switch on, the modules inside, how the work flows, and how we roll it out.")}
<div style="margin-top:auto;border-top:.5mm solid var(--ink)">{rows}</div></div>'''

def _ihead(name, d, suffix=""):
    return (f'<div style="display:flex;align-items:center;gap:2mm"><span class="ref"><i></i>Industry 0{ind_no(name)}</span><span class="eyebrow b">{name}{suffix}</span></div>')

def ind_1(n, name):
    d = IND_DETAIL[name]
    glance = "".join(f'<span style="display:inline-flex;align-items:center;gap:1.4mm;font:600 7.8pt/1 var(--fb);color:#fff">{oi(m["icon"], 4.2)}{m["name"]}</span>' for m in d["modules"])
    probs = "".join(f'<div style="border-left:.8mm solid var(--blue);padding-left:3.4mm"><div class="h4">{t}</div><p class="ps" style="margin-top:.8mm">{x}</p></div>' for t, x in d["problems"])
    con = "".join(f'<span class="chip" style="height:5.4mm;font-size:7.4pt">{c}</span>' for c in d["connects"])
    return f'''<div class="ct" id="ind-{d["slug"]}">{_ihead(name, d)}
<div class="h1" style="font-size:20pt;margin-top:3mm">{d["title"]}</div>
<p class="lead" style="font-size:9.6pt;margin-top:2.6mm">{d["sub"]}</p>
<div style="margin-top:4mm;background:linear-gradient(120deg,#0F2350,#1E4691);border-radius:2.6mm;padding:3.6mm 4.4mm">
 <div style="font:700 6.2pt/1 var(--fb);letter-spacing:.16em;color:#9DB3DD">ODOO APPS WE SWITCH ON</div><div style="display:flex;flex-wrap:wrap;gap:2mm 4mm;margin-top:2.2mm">{glance}</div>
 <div style="margin-top:3.2mm;padding-top:3mm;border-top:.25mm solid rgba(255,255,255,.25)"><div style="font:700 6.2pt/1 var(--fb);letter-spacing:.16em;color:#9DB3DD">FIRST PHASE · {d["first"].upper()}</div>
 <div style="font:500 8.4pt/1.42 var(--fb);color:#fff;margin-top:1.6mm">{IND_EXTRA[name][0]}</div></div></div>
{sec("A", "What usually slows you down", 4.6)}<div style="display:flex;flex-direction:column;gap:2.8mm">{probs}</div>
<div style="margin-top:auto;padding-top:3mm;border-top:.5mm solid var(--ink);display:flex;flex-wrap:wrap;gap:1.4mm;align-items:center"><span class="eyebrow" style="color:var(--ink);margin-right:1.4mm">Connects to</span>{con}</div></div>'''

def ind_2(n, name):
    d = IND_DETAIL[name]
    mods = ""
    for i, m in enumerate(d["modules"]):
        big = i == 0
        mods += (f'<div class="card" style="padding:3.2mm 3.4mm;display:flex;flex-direction:column;gap:1.8mm{";grid-column:1/-1;border:.5mm solid var(--blue)" if big else ""}">'
                 f'<div style="display:flex;gap:2.2mm;align-items:center">{oi(m["icon"], 7 if big else 5.6)}<div><div class="h4" style="font-size:{10 if big else 8.8}pt">{m["name"]}</div>'
                 f'<div style="font:500 7.6pt/1.3 var(--fb);color:var(--muted);margin-top:.4mm">{m["line"]}</div></div>'
                 f'{"<span class=\"tag bl\" style=\"margin-left:auto\">Core module</span>" if big else ""}</div>'
                 + ul(m["feat"], size=8, gap=1, extra="display:grid;grid-template-columns:1fr 1fr;column-gap:4mm" if big else "") + '</div>')
    reps = "".join(f'<span class="chip" style="height:5.4mm;font-size:7.4pt">{r}</span>' for r in d["reports"])
    return f'''<div class="ct">{_ihead(name, d, " · continued")}
{sec("B", "The modules inside, and what each one does", 3.6)}<div style="display:grid;grid-template-columns:1fr 1fr;gap:2.6mm">{mods}</div>
<div style="margin-top:auto;padding-top:3mm;border-top:.5mm solid var(--ink);display:flex;flex-wrap:wrap;gap:1.4mm;align-items:center"><span class="eyebrow" style="color:var(--ink);margin-right:1.4mm">Reports we set up first</span>{reps}</div></div>'''

def ind_faq(name):
    d, out, seen = IND_DETAIL[name], [], set()
    for q, a in [(IND_EXTRA[name][1], IND_EXTRA[name][2])] + list(d["faq"]):
        k = " ".join(q.lower().split()[:3])
        if k not in seen:
            seen.add(k); out.append((q, a))
    return out

def ind_3(n, name):
    d = IND_DETAIL[name]
    steps = "".join(f'<div class="card" style="padding:3mm 3.2mm;display:flex;flex-direction:column;gap:1.1mm"><div style="display:flex;align-items:center;gap:2mm"><span style="font:800 12pt/1 var(--fd);color:var(--blue)">{i + 1}</span><span class="tag bl">{app}</span></div>'
                    f'<div class="h4" style="font-size:8.8pt">{t}</div><p style="font-size:8pt;line-height:1.38">{b}</p><div style="margin-top:auto;font:500 7.4pt/1.35 var(--fb);color:var(--muted)">Replaces: {r}</div></div>'
                    for i, (app, t, b, r) in enumerate(d["steps"]))
    faq = "".join(qa(q, a) for q, a in ind_faq(name)[:2])
    return f'''<div class="ct" id="ind-{d["slug"]}-2">{_ihead(name, d, " · how it runs")}
<div class="h2" style="margin-top:2.6mm">Six steps, <span class="mk">one Odoo database.</span></div>
{sec("C", "How the work flows", 3.6)}<div style="display:grid;grid-template-columns:1fr 1fr;gap:2.4mm">{steps}</div>
<div class="faq" style="margin-top:auto">{faq}</div></div>'''

def ind_4(n, name):
    d = IND_DETAIL[name]
    rows = "".join(f'<div style="display:grid;grid-template-columns:22mm 1fr 1fr;gap:3mm;padding:1.6mm 0;border-bottom:.25mm solid var(--line);font-size:8pt;line-height:1.36">'
                   f'<b style="font:700 8pt/1.36 var(--fd);color:var(--ink)">{j}</b><span style="color:var(--muted)">{t}</span><span style="color:var(--ink)">{o}</span></div>' for j, t, o in d["ba"])
    phases = "".join(f'<div class="card w" style="padding:3mm 3.2mm"><div class="eyebrow b">Phase {i + 1}</div><div class="h4" style="margin-top:1.2mm;font-size:8.8pt">{t}</div>'
                     + ul(pts, size=8, gap=1, extra="margin-top:1.8mm") + '</div>' for i, (t, pts) in enumerate(d["phases"]))
    faq = "".join(qa(q, a) for q, a in ind_faq(name)[2:])
    return f'''<div class="ct">{_ihead(name, d, " · how it runs")}
{sec("D", "Before and after", 3.6)}
<div style="border-top:.5mm solid var(--ink)"><div style="display:grid;grid-template-columns:22mm 1fr 1fr;gap:3mm;padding:1.4mm 0;border-bottom:.25mm solid var(--line)"><span class="eyebrow">The job</span><span class="eyebrow">Today</span><span class="eyebrow b">With Odoo</span></div>{rows}</div>
{sec("E", "How we roll it out · each phase live first", 4.4)}<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm">{phases}</div>
<div class="faq" style="margin-top:auto">{faq}</div></div>'''

# ================================================================ reference + close
def _country(t, k, pts):
    return (f'<div class="card" style="padding:4mm;display:flex;flex-direction:column;gap:2.4mm"><div style="display:flex;justify-content:space-between;align-items:center"><div class="h2" style="font-size:14pt">{t}</div>'
            f'<span style="font:800 9pt/1 var(--fd);color:#fff;background:var(--blue);border-radius:1.2mm;padding:1.4mm 2mm">{k}</span></div>{ul(pts, gap=1.4)}</div>')

def local1(n):
    ph = ["Set up for BIR requirements: CAS and CBA books and invoices (BIR-01 to BIR-04)", "BIR 2306 and 2307 certificates generated from vendor bills", "SLSP, SAWT and QAP DAT exports, 2550Q, 1600-VT and 2551Q",
          "Basic payroll (Odoo 20): 1601-C items, 2316, 1604-C worksheets; SSS and Pag-IBIG loan deductions", "EIS route scoped with you before 31 Dec 2026; Odoo has no built-in EIS connection"]
    return f'''<div class="ct" id="local">{head("Localisation", 'One database, <span class="mk">each country\'s rules.</span>',
"Odoo runs a company per country in one database, each with its own localisation, currencies and reports, with intercompany transactions between them. Philippine companies start with the BIR work; these are the Odoo 20 changes we plan around.")}
<div style="margin-top:6mm">{_country("Philippines", "PH", ph)}</div></div>'''

def local2(n):
    sg = ["GST and IRAS reporting under Odoo 20 localisation", "SFRS-aligned accounting", "Odoo 20 GST refinements toward InvoiceNow (phased 1 Nov 2025 to 1 Apr 2031)",
          "InvoiceNow through the Access Point you choose; TechNext is not an Access Point", "On-site work from our Waterloo Street HQ"]
    vn = ["Odoo 20 follows Circular 99 for accounting", "01/GTGT VAT reporting", "SInvoice e-invoicing", "AI engineering hub in Ho Chi Minh City"]
    return f'''<div class="ct">{cont("Localisation")}<div style="display:flex;flex-direction:column;gap:3mm;margin-top:3mm">{_country("Singapore", "SG", sg)}{_country("Vietnam", "VN", vn)}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:3mm">
 <div class="card w" style="padding:3.6mm"><div class="h4">Moving to Odoo 20</div><p style="font-size:8pt;line-height:1.4;margin-top:1.2mm">We upgrade existing databases on a staging copy first, migrate customisations and switch over on the date you choose.</p></div>
 <div class="card w" style="padding:3.6mm"><div class="h4">Groups across borders</div><p style="font-size:8pt;line-height:1.4;margin-top:1.2mm">See ERP-08 for consolidation, inter-company eliminations and access per entity.</p></div></div>
<div class="small" style="margin-top:auto">Based on Odoo 20 release notes, BIR issuances to RMC 110-2026 and the Singapore GST InvoiceNow timeline, as summarised on technext.asia in October 2026. Confirm your own compliance dates with your adviser.</div></div>'''

def offices1(n):
    o = [("Singapore", "Headquarters", "261 Waterloo Street, #03-36, Waterloo Centre, Singapore 180261", "Sales, discovery workshops and on-site work with clients in Singapore. Support is led from here."),
         ("Taguig City, Philippines", "Main development &amp; consulting hub", "Level 9, IP Center, Taguig City, Metro Manila", "Odoo configuration, custom modules and integrations, with finance, HR, sales and marketing alongside."),
         ("Ho Chi Minh City, Vietnam", "AI engineering hub", "62 Nguyễn Thị Nhung, Phường Hiệp Bình, Ho Chi Minh City", "AI agents and automation, knowledge and RAG systems, chatbots and assistants, and local LLM deployment.")]
    c = "".join(f'<div style="display:grid;grid-template-columns:11mm 1fr;gap:3mm;padding:4mm 0;border-bottom:.25mm solid var(--line)">'
                f'<div style="font:800 17pt/1 var(--fd);color:var(--blue)">0{i + 1}</div><div><div class="h3" style="font-size:12pt">{t}</div><div class="eyebrow b" style="margin-top:1.4mm">{r}</div>'
                f'<p style="font-size:8.2pt;margin-top:1.8mm;color:var(--ink)">{a}</p><p class="ps" style="margin-top:1.4mm">{d}</p></div></div>' for i, (t, r, a, d) in enumerate(o))
    return f'''<div class="ct" id="offices">{head("Where we work", 'Three hubs, <span class="mk">one project team.</span>',
"We work on-site in Singapore and remotely with clients in 25+ countries. Ask us about on-site work at your location.")}
<div style="margin-top:6mm;border-top:.5mm solid var(--ink)">{c}</div></div>'''

def offices2(n):
    hop = [("Singapore", "Discovery workshops, scope and on-site sessions"), ("Taguig City", "Configuration, custom modules and integrations"),
           ("Ho Chi Minh City", "AI features, when AI is in scope"), ("Singapore", "Go-live, training and support led from HQ")]
    hc = "".join(f'<div style="background:#fff;border-radius:2mm;padding:3.4mm"><div style="font:800 9pt/1 var(--fd);color:var(--blue)">0{i + 1}</div><div class="h4" style="margin-top:1.6mm">{t}</div><div class="ps" style="margin-top:1mm">{d}</div></div>' for i, (t, d) in enumerate(hop))
    stats = "".join(f'<div class="stat"><div class="v">{v}</div><div class="k">{k}</div></div>' for v, k in [("25+", "Countries with clients"), ("90+", "Enterprise clients"), ("3", "Hubs across Asia"), ("1", "Team after go-live")])
    return f'''<div class="ct">{cont("Where we work", 'One project, <span class="mk">handed between hubs.</span>')}
<div class="card w" style="margin-top:5mm;padding:4mm"><div class="eyebrow" style="color:var(--navy)">How one project moves between hubs</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:2.6mm;margin-top:3mm">{hc}</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm 6mm;margin-top:6mm;padding-top:5mm;border-top:.5mm solid var(--ink)">{stats}</div></div>'''

def start1(n):
    steps = [("Tell us", "Send the form at technext.asia or email sales@technext.asia. Share how your business runs today and which BIR forms you file."),
             ("Discovery call", "We walk through how your company works and what would change. No pitch before we understand the problem."),
             ("Written scope", "We say what to set up first and send a written quotation, stating what is included and what is not."),
             ("Go live", "We set it up, train your team and support you after go-live.")]
    sc = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:1.4mm;padding:3.6mm"><div style="font:800 15pt/1 var(--fd);color:var(--blue)">{i + 1}</div><div class="h3">{t}</div><p class="ps">{d}</p></div>' for i, (t, d) in enumerate(steps))
    contact = "".join(f'<div><div style="font:600 6.6pt/1 var(--fb);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)">{k}</div><div style="font:700 9.4pt/1.3 var(--fd);color:var(--ink);margin-top:.8mm">{v}</div></div>'
                      for k, v in [("Email", "sales@technext.asia"), ("BIR guide", "technext.asia/bir-e-invoicing"), ("Web", "technext.asia/quotation"), ("LinkedIn", "linkedin.com/company/technextasia")])
    return f'''<div class="ct" id="start">{head("How to start", 'Tell us what <span class="mk">slows you down.</span>')}
<div style="display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:3mm;margin-top:5mm">{sc}</div>
<div class="card" style="margin-top:6mm;padding:4mm"><div class="eyebrow">Contact</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm 4mm;margin-top:2.6mm">{contact}</div></div></div>'''

def start2(n):
    chk = ["Which BIR forms you file, and whether you are covered for e-invoicing by 31 December 2026", "Which services interest you (use the codes in this catalogue)", "How many users, companies and locations",
           "The systems you use today, and which you'd like to keep", "Integrations you know you need: banks, stores, payment gateways",
           "Any other deadline that matters, such as a financial year-end or InvoiceNow date"]
    return f'''<div class="ct">{cont("How to start")}
<div class="card w" style="margin-top:3mm;padding:4.4mm"><div class="eyebrow" style="color:var(--navy)">Helpful to include in your first message</div>{ul(chk, gap=1.4, extra="margin-top:2.6mm")}</div>
<a href="#bir-check" style="margin-top:4mm;display:block;background:linear-gradient(120deg,#0F2350,#1E4691);border-radius:2.6mm;padding:5mm">
 <div style="display:flex;justify-content:space-between;align-items:center;gap:3mm"><div style="font:700 6.2pt/1 var(--fb);letter-spacing:.16em;color:#9DB3DD">PHILIPPINE COMPANIES · START HERE</div>
 <div style="background:#FFF4DC;border-radius:99px;padding:1.6mm 3mm;font:800 8.4pt/1 var(--fd);color:#0F2350;white-space:nowrap">31 Dec 2026</div></div>
 <div style="font:800 14pt/1.15 var(--fd);color:#fff;letter-spacing:-.02em;margin-top:3mm">Covered by BIR e-invoicing? Start before the deadline.</div>
 <p style="font-size:8.6pt;line-height:1.45;color:#DDE7F8;margin-top:2.2mm">You need a Permit to Issue first, then EIS Certification within six months (RR 26-2025 · RMC 98-2026). Run the twelve-question self-check on p. {pn("bir-check")} and bring it to your discovery call.</p></a>
<div class="card" style="margin-top:6mm;padding:4mm">
 <div class="h4">Who replies?</div><p class="ps" style="margin-top:1mm">The TechNext team, from sales@technext.asia. An adviser who sets up Odoo for BIR requirements joins the discovery call.</p>
 <div class="h4" style="margin-top:3mm">What do you do with my details?</div><p class="ps" style="margin-top:1mm">We use them only to reply. See technext.asia/privacy.</p></div></div>'''

def back(n):
    return ('<div class="div" style="position:absolute;inset:0"><div class="grid-bg"></div>'
            '<div style="position:absolute;left:12mm;right:12mm;top:44mm">'
            '<img src="assets/logo/technext-vertical-white.png" style="height:26mm" alt="TechNext">'
            '<div style="font:800 24pt/1.05 var(--fd);color:#fff;letter-spacing:-.03em;margin-top:11mm">You don\'t need to hire<br>your own team.</div>'
            '<div style="font:500 9.4pt/1.6 var(--fb);color:#DDE7F8;margin-top:5mm">Your trusted expert adviser for ERP and compliance.<br>BIR Compliance · Odoo ERP · AI Automation · Websites · Marketing</div></div>'
            '<div style="position:absolute;left:12mm;right:12mm;bottom:36mm;display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;border-top:.25mm solid rgba(255,255,255,.25);padding-top:5mm">'
            + "".join(f'<div><div style="font:700 6.2pt/1 var(--fb);letter-spacing:.16em;color:#9DB3DD">{k}</div><div style="font:600 8.4pt/1.5 var(--fb);color:#fff;margin-top:1.8mm">{v}</div></div>'
                      for k, v in [("CONTACT", "sales@technext.asia<br>technext.asia/quotation"), ("WEB", "technext.asia<br>@technextasia"),
                                   ("OFFICES", "Singapore · Taguig City<br>Ho Chi Minh City")]) +
            '</div><div style="position:absolute;left:12mm;right:12mm;bottom:12mm;display:flex;justify-content:space-between;align-items:flex-end;gap:5mm">'
            '<div style="font:500 6.4pt/1.6 var(--fb);color:#9DB3DD">TECHNEXT PTE. LTD. (UEN 202699888G)<br>261 Waterloo Street, #03-36, Waterloo Centre, Singapore 180261<br>'
            + EDITION + ' · Information correct as of October 2026.<br>Odoo is a trademark of Odoo S.A.</div>'
            '<div style="background:#fff;border-radius:2.2mm;padding:2.2mm 3mm;flex:none"><img src="assets/logo/odoo-ready-partner.png" style="height:9mm" alt="Odoo Ready Partner"></div></div></div>')

# On load: a service's Specification moves up to its first page whenever it fits above the drawing,
# so neither page of the pair is left with an empty band or an overflow. Section letters follow the order.
FLOW = """<script>(function(){function flow(){var mm=3.7795;document.querySelectorAll('.sv[id]').forEach(function(a){
var pb=a.closest('.page').nextElementSibling,b=pb&&pb.querySelector('.sv'),blk=b&&b.querySelector('.specblk'),slot=a.querySelector('.slotA');if(!blk||!slot)return;
var free=a.querySelector('.vis').getBoundingClientRect().top-a.querySelector('.meta2').getBoundingClientRect().bottom-2.4*mm;
var fits=function(){return blk.getBoundingClientRect().height+4.4*mm<=free};
if(!fits()){a.classList.add('tight');b.classList.add('tight')}if(fits())slot.appendChild(blk);
var lim=b.closest('.page').getBoundingClientRect().bottom-15*mm,mx=0;b.querySelectorAll('*').forEach(function(e){var q=e.getBoundingClientRect();if(q.height&&q.bottom>mx)mx=q.bottom});if(mx>lim){b.classList.add('tight')}else if(blk.parentNode===slot&&a.classList.contains('tight')){b.classList.remove('tight')}
var i=0;a.querySelectorAll('.sec-h .n').forEach(function(n){n.textContent='ABC'[i++]});b.querySelectorAll('.sec-h .n').forEach(function(n){n.textContent='ABC'[i++]});});
document.documentElement.setAttribute('data-flow','1')}
(document.fonts?document.fonts.ready:Promise.resolve()).then(flow)})();</script>"""

# ================================================================ plan
def plan():
    page(cover, kind="bare")
    page(about1, label="About", anchor="about"); page(about2, label="About")
    page(contents1, label="Contents", anchor="contents"); page(contents2, label="Contents"); page(contents3, label="Contents")
    page(anatomy1, label="How we engage", anchor="anatomy"); page(anatomy2, label="How we engage")
    for p in PRACTICES:
        page(lambda n, p=p: divider(n, p), p["id"], "div", "d-" + p["id"])
        pid = p["id"]
        if pid == "bir":
            page(bir_pains1, pid, anchor="bir-pains"); page(bir_pains2, pid)
            page(bir_check1, pid, anchor="bir-check"); page(bir_check2, pid)
        svcs = [s for s in S if s["p"] == pid]
        for i, s in enumerate(svcs):
            if pid == "ai" and i == len(svcs) - 4:
                page(ai1, pid, anchor="ai-principles"); page(ai2, pid)
            page(lambda n, s=s: service_a(n, s), pid, anchor=s["id"]); page(lambda n, s=s: service_b(n, s), pid)
        if pid == "bir":
            page(bir_rules1, pid, anchor="bir-rules"); page(bir_rules2, pid)
        if pid == "erp":
            page(apps1, pid, anchor="odoo-apps"); page(apps2, pid, anchor="odoo-apps-2"); page(apps3, pid); page(apps4, pid)
            page(method1, pid, anchor="method"); page(method2, pid)
            page(hosting1, pid, anchor="hosting"); page(hosting2, pid)
        if pid == "mkt":
            page(offer1, pid, anchor="offer"); page(offer2, pid)
    page(industries_index, label="Odoo by industry", anchor="industries")
    for name, *_ in INDUSTRIES:
        slug = IND_DETAIL[name]["slug"]
        lab = "Odoo by industry · <b>" + name + "</b>"
        page(lambda n, nm=name: ind_1(n, nm), label=lab, anchor="ind-" + slug)
        page(lambda n, nm=name: ind_2(n, nm), label=lab)
        page(lambda n, nm=name: ind_3(n, nm), label=lab, anchor="ind-" + slug + "-2")
        page(lambda n, nm=name: ind_4(n, nm), label=lab)
    page(local1, label="Localisation", anchor="local"); page(local2, label="Localisation")
    page(offices1, label="Where we work", anchor="offices"); page(offices2, label="Where we work")
    page(start1, label="How to start", anchor="start"); page(start2, label="How to start")
    page(back, kind="bare")

def main():
    plan()
    for i, pg in enumerate(PLAN, 1):
        if pg["anchor"]:
            PMAP[pg["anchor"]] = i
    out = [chrome(i, pg["pid"], pg["fn"](i), pg["kind"], pg["label"]) for i, pg in enumerate(PLAN, 1)]
    html = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="color-scheme" content="light"><meta name="robots" content="noindex">'
            '<title>TechNext Services Catalogue</title><style>' + CSS + '</style></head><body><main class="book">' + "".join(out) + '</main>' + FLOW + '</body></html>')
    html = html.encode("ascii", "xmlcharrefreplace").decode("ascii")
    with open(os.path.join(ROOT, "print.html"), "w", encoding="utf-8") as f:
        f.write(html)
    write_bookjson(len(PLAN))
    print("pages:", len(PLAN))

def write_bookjson(n):
    import json
    guides = {"bir": [("Where BIR compliance hurts", "bir-pains"), ("BIR self-check", "bir-check"), ("The BIR rules and what Odoo covers", "bir-rules")],
              "erp": [("Odoo apps we implement", "odoo-apps"), ("Our implementation method", "method"), ("Where Odoo runs", "hosting")],
              "ai": [("How our AI stays in control", "ai-principles")], "mkt": [("Website design with your Odoo", "offer")]}
    chapters = []
    for p in PRACTICES:
        secs = [[f'{s["code"]} · {s["name"]}', PMAP[s["id"]]] for s in S if s["p"] == p["id"]]
        secs += [[g, PMAP[a]] for g, a in guides[p["id"]]]
        secs.sort(key=lambda x: x[1])
        chapters.append({"no": p["n"], "title": p["name"], "page": PMAP["d-" + p["id"]], "sections": secs})
    chapters.append({"no": f"{len(PRACTICES) + 1:02d}", "title": "Industries & reference", "page": PMAP["industries"], "sections": [
        ["Odoo by industry", PMAP["industries"]]] + [
        [nm.replace("&amp;", "&") + ": modules and rollout", PMAP["ind-" + IND_DETAIL[nm]["slug"]]] for nm, *_ in INDUSTRIES] + [["Localisation: SG, PH, VN", PMAP["local"]],
        ["Where we work", PMAP["offices"]], ["How to start", PMAP["start"]]]})
    labels = {"1": "Cover", str(PMAP["about"]): "About TechNext", str(PMAP["contents"]): "Contents", str(PMAP["anatomy"]): "How we engage", str(n): "Back cover"}
    for p in PRACTICES:
        labels[str(PMAP["d-" + p["id"]])] = f'Practice {p["n"]} · {p["name"]}'
    cfg = {
        "_readme": "GENERATED by _src/build.py from the catalogue page plan. Edit _src/build.py / data.py, then rebuild.",
        "title": "Services Catalogue", "edition": "Edition 2026/27", "brand": "TechNext",
        "publisher": "TechNext Pte. Ltd. (UEN 202699888G)",
        "address": "261 Waterloo Street, #03-36, Waterloo Centre, Singapore 180261",
        "contact": {"email": "sales@technext.asia", "website": "https://technext.asia/", "orderEmail": "sales@technext.asia"},
        "shop": {"shopUrl": "https://technext.asia/quotation", "label": "Get a quotation"},
        "settings": {"flipSound": True, "startPage": 1, "indexPages": [], "hideInBookMode": []},
        "front": [["Cover", 1], ["About TechNext", PMAP["about"]], ["Contents", PMAP["contents"]], ["How we engage", PMAP["anatomy"]]],
        "back": [["Back cover · contact", n]],
        "pageLabels": labels, "chapters": chapters, "hotspots": [],
    }
    with open(os.path.join(ROOT, "book", "book.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
