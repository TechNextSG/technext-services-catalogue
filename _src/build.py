"""TechNext Services Catalogue builder.  python _src/build.py  ->  catalogue.html"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from css import CSS
from data import PRACTICES, S, ODOO_CATS, INDUSTRIES, IND_EXTRA
from visuals import VIS, oi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITION = "Edition 2026/27"
PR = {p["id"]: p for p in PRACTICES}
pages = []          # (html, practice_id or None, kind)

def esc_title(t):
    import re
    return re.sub(r"<[^>]+>", "", t)

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
    rf = (f'<div class="rf"><div class="pn">{n:02d}</div><div>{EDITION} · technext.asia · Odoo Ready Partner</div></div>')
    return f'<section class="page{" even" if even else ""}{" div" if kind == "div" else ""}" id="p{n}">{rh}{tabs}{inner}{rf}</section>'

def add(fn, pid=None, kind="std", label="", anchor=None):
    pages.append(dict(fn=fn, pid=pid, kind=kind, label=label, anchor=anchor))

# ---------------------------------------------------------------- pages
def cover(n):
    idx = "".join(f'<div style="display:grid;grid-template-columns:14mm 1fr;padding:1.6mm 0;border-bottom:.25mm solid rgba(255,255,255,.14)">'
                  f'<span style="font:700 6pt/1.4 var(--fb);letter-spacing:.12em;color:#6FA0F5">{s["code"]}</span><span style="font:500 7.4pt/1.4 var(--fb);color:#DDE7F8">{s["name"]}</span></div>' for s in S)
    return (f'<div class="div" style="position:absolute;inset:0"><div class="grid-bg"></div>'
            '<svg viewBox="0 0 400 400" style="position:absolute;right:-60mm;top:-40mm;width:230mm;height:230mm;opacity:.10"><g fill="none" stroke="#fff" stroke-width=".6">'
            + "".join(f'<circle cx="200" cy="200" r="{r}"/>' for r in range(40, 200, 22)) + '</g></svg>'
            '<img src="assets/logo/technext-horizontal-white.png" style="position:absolute;left:17mm;top:17mm;height:8mm" alt="TechNext">'
            '<div style="position:absolute;right:17mm;top:18mm;font:700 6.6pt/1 var(--fb);letter-spacing:.18em;color:#9DB3DD;text-transform:uppercase">' + EDITION + '</div>'
            '<div style="position:absolute;left:17mm;top:62mm;width:112mm">'
            '<div class="eyebrow" style="color:#6FA0F5">Odoo ERP · Enterprise AI · Websites &amp; Marketing · Technology</div>'
            '<div style="font:800 54pt/.98 var(--fd);color:#fff;letter-spacing:-.04em;margin-top:6mm">Services<br>Catalogue</div>'
            '<div style="width:22mm;height:1.2mm;background:#6FA0F5;margin:8mm 0 7mm"></div>'
            '<div style="font:400 12pt/1.5 var(--fb);color:#DDE7F8;max-width:104mm">Eighteen services across four practices, from one team in Singapore, the Philippines and Vietnam. You don\'t need to hire your own team.</div></div>'
            f'<div style="position:absolute;left:136mm;right:17mm;top:62mm"><div style="font:700 6pt/1 var(--fb);letter-spacing:.18em;color:#9DB3DD;margin-bottom:2.4mm">IN THIS CATALOGUE</div>{idx}</div>'
            '<div style="position:absolute;left:17mm;right:17mm;bottom:16mm;display:flex;align-items:flex-end;justify-content:space-between">'
            '<div style="display:flex;gap:10mm">' + "".join(
                f'<div><div style="font:800 18pt/1 var(--fd);color:#fff">{v}</div><div style="font:600 6.4pt/1.3 var(--fb);color:#9DB3DD;margin-top:1.4mm">{k}</div></div>'
                for v, k in [("10+", "countries served"), ("11+", "enterprise clients"), ("3", "hubs: SG · PH · VN"), ("4", "practices")]) + '</div>'
            '<div style="background:#fff;border-radius:2.4mm;padding:2.6mm 3.4mm"><img src="assets/logo/odoo-ready-partner.png" style="height:11mm" alt="Odoo Ready Partner"></div></div></div>')

def about(n):
    return f'''<div class="ct">
<div class="eyebrow b">About TechNext</div>
<div class="h1" style="margin-top:4mm;max-width:150mm">No need to hire your own team for <span class="mk">Odoo, websites, branding or tech.</span></div>
<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:10mm;margin-top:8mm">
 <div>
  <p class="lead">TechNext Pte. Ltd. is a Singapore-based Odoo Ready Partner. We implement Odoo ERP end to end, build enterprise AI, run websites and social media, and deliver IoT, app development and network services for growing companies.</p>
  <p style="margin-top:4mm;font-size:9pt;line-height:1.6">Sales, discovery and on-site work run from our Singapore headquarters. Odoo configuration, custom modules and integrations are built at our main development and consulting hub in Taguig City, Metro Manila, and our AI engineers in Ho Chi Minh City join whenever AI is in scope. One project, one team, and the same people after go-live.</p>
 </div>
 <div class="card w" style="padding:6mm">
  <div class="eyebrow" style="color:var(--navy)">How we work</div>
  <ul class="inc" style="margin-top:4mm">
   <li><b>Discovery before a pitch.</b> We map how the business runs before we propose anything.</li>
   <li><b>Standard first.</b> Configure before customising; custom only where it earns its place.</li>
   <li><b>Written scope and quotation.</b> You see what is included, and what is not, before work starts.</li>
   <li><b>Yours to keep.</b> Accounts, data, sites and master files stay in your name.</li>
  </ul>
 </div>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;margin-top:10mm;padding-top:7mm;border-top:.5mm solid var(--ink)">
 {"".join(f'<div class="stat"><div class="v">{v}</div><div class="k">{k}</div></div>' for v, k in [("10+", "Countries with clients"), ("11+", "Enterprise clients"), ("3", "Hubs in Singapore, the Philippines and Vietnam"), ("4", "Core AI disciplines")])}
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:10mm">
 {"".join(f'<a href="#d-{p["id"]}" class="card" style="display:flex;flex-direction:column;gap:2mm;min-height:52mm"><div style="font:800 20pt/1 var(--fd);color:var(--mist)">{p["n"]}</div><div class="h3">{p["name"]}</div><div style="font-size:7.6pt;line-height:1.45">{p["lead"].split(". ")[0].rstrip(".")}.</div></a>' for p in PRACTICES)}
</div>
<div class="small" style="margin-top:auto;padding-top:6mm">TechNext Pte. Ltd. · UEN 202699888G · 261 Waterloo Street, #03-36, Waterloo Centre, Singapore 180261</div>
</div>'''

def contents(n, pmap):
    blocks = []
    for p in PRACTICES:
        rows = "".join(f'<a href="#{s["id"]}" style="display:grid;grid-template-columns:16mm 1fr 10mm;align-items:baseline;padding:2.2mm 0;border-bottom:.25mm solid var(--line)">'
                       f'<span style="font:700 6.4pt/1 var(--fb);letter-spacing:.1em;color:var(--blue)">{s["code"]}</span><span style="font:600 8.6pt/1.3 var(--fb);color:var(--ink)">{s["name"]}</span>'
                       f'<span style="text-align:right;font:700 8.6pt/1 var(--fd);color:var(--ink)">{pmap[s["id"]]:02d}</span></a>' for s in S if s["p"] == p["id"])
        extra = {"erp": [("odoo-apps", "Odoo apps we implement"), ("method", "Our implementation method"), ("hosting", "Where Odoo runs")],
                 "ai": [("ai-principles", "How our AI stays in control")], "mkt": [("offer", "Website design with your Odoo")], "tech": []}[p["id"]]
        rows += "".join(f'<a href="#{a}" style="display:grid;grid-template-columns:16mm 1fr 10mm;align-items:baseline;padding:2.2mm 0;border-bottom:.25mm solid var(--line)">'
                        f'<span style="font:700 6.4pt/1 var(--fb);letter-spacing:.1em;color:var(--muted)">GUIDE</span><span style="font:500 8.6pt/1.3 var(--fb);color:var(--body)">{t}</span>'
                        f'<span style="text-align:right;font:700 8.6pt/1 var(--fd);color:var(--ink)">{pmap[a]:02d}</span></a>' for a, t in extra)
        blocks.append(f'<div><a href="#d-{p["id"]}" style="display:flex;align-items:baseline;gap:3mm;padding-bottom:2.4mm;border-bottom:.5mm solid var(--ink)">'
                      f'<span style="font:800 16pt/1 var(--fd);color:var(--blue)">{p["n"]}</span><span class="h3">{p["name"]}</span>'
                      f'<span style="margin-left:auto;font:700 8.6pt/1 var(--fd);color:var(--ink)">{pmap["d-" + p["id"]]:02d}</span></a>{rows}</div>')
    ref = [("industries", "Odoo by industry"), ("local", "Localisation: Singapore, the Philippines, Vietnam"), ("offices", "Where we work"), ("start", "How to start")]
    refs = "".join(f'<a href="#{a}" style="display:grid;grid-template-columns:1fr 10mm;padding:2.2mm 0;border-bottom:.25mm solid var(--line)"><span style="font:600 8.6pt/1.3 var(--fb);color:var(--ink)">{t}</span>'
                   f'<span style="text-align:right;font:700 8.6pt/1 var(--fd);color:var(--ink)">{pmap[a]:02d}</span></a>' for a, t in ref)
    return f'''<div class="ct">
<div class="eyebrow b">Contents</div>
<div class="h1" style="margin-top:4mm">Four practices. <span class="mk">One team.</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:9mm 10mm;margin-top:9mm">{"".join(blocks)}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10mm;margin-top:9mm">
 <div><div style="padding-bottom:2.4mm;border-bottom:.5mm solid var(--ink)" class="h3">Reference</div>{refs}</div>
 <div class="card w" style="padding:5mm"><div class="h4">Reading this catalogue</div><p style="font-size:7.8pt;margin-top:2mm">Each service has a reference code (for example <b>ERP-01</b>). Quote the codes you're interested in when you write to <b>sales@technext.asia</b>, and we'll come back with a written scope. Screens marked <span class="tag am">Sample data</span> are illustrations, not client data.</p></div>
</div></div>'''

def anatomy(n):
    models = [("Project", "One-off, scoped and quoted in writing before work begins.", "Implementation · customisation · websites · brand · apps · IoT · networks"),
              ("Monthly retainer", "A steady monthly plan, scoped to channels and volume.", "Social media management"),
              ("Support plan", "Agreed response targets, tracked on every ticket.", "Odoo support · network support"),
              ("Standalone discovery", "A written scope that is yours to keep, with or without us.", "Odoo consultation &amp; discovery")]
    return f'''<div class="ct">
<div class="eyebrow b">How we engage</div>
<div class="h1" style="margin-top:4mm;max-width:150mm">Every engagement starts with <span class="mk">a written scope.</span></div>
<p class="lead" style="margin-top:5mm;max-width:150mm">We don't publish a price list, because no two businesses run the same way. Tell us what's manual today, and we come back with a scope and a quotation that states what is included and what is not. Nothing commits you until you say so.</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:9mm">
 {"".join(f'<div class="card" style="padding:6mm;display:flex;flex-direction:column;gap:2.4mm"><div style="display:flex;align-items:center;gap:3mm"><span style="font:800 9pt/1 var(--fd);color:#fff;background:var(--blue);border-radius:1.4mm;padding:1.4mm 2mm">0{i + 1}</span><span class="h3">{t}</span></div><p style="font-size:8.6pt">{d}</p><div style="margin-top:auto;padding-top:2.4mm;border-top:.25mm solid var(--line);font:600 7pt/1.4 var(--fb);color:var(--muted)">Used for: <span style="color:var(--ink)">{u}</span></div></div>' for i, (t, d, u) in enumerate(models))}
</div>
<div style="margin-top:10mm;display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm;padding-top:7mm;border-top:.5mm solid var(--ink)">
 <div><div class="h4">Odoo licences</div><p style="font-size:8pt;margin-top:1.6mm">Billed by Odoo, per user per month, in your name. Our work is quoted separately, so you can see each part clearly.</p></div>
 <div><div class="h4">Ownership</div><p style="font-size:8pt;margin-top:1.6mm">Databases, websites, social accounts, analytics and master files stay in your name, handed over completely.</p></div>
 <div><div class="h4">Approval</div><p style="font-size:8pt;margin-top:1.6mm">Pages, posts and assets are shared for sign-off. AI waits for a person before anything irreversible.</p></div>
</div>
<div style="margin-top:auto" class="card w"><div style="display:flex;align-items:center;gap:6mm"><div class="h3" style="flex:none">Service page anatomy</div>
 <div style="display:flex;gap:2mm;flex-wrap:wrap">{"".join(f'<span class="chip">{t}</span>' for t in ["Reference code", "What it is", "Illustrated workflow", "What's included", "Specification", "Odoo apps involved", "Questions clients ask"])}</div></div></div>
</div>'''

def divider(n, p, pmap):
    lst = "".join(f'<a href="#{s["id"]}"><span>{s["code"]}</span>{s["name"]}<em>p. {pmap[s["id"]]:02d}</em></a>' for s in S if s["p"] == p["id"])
    return (f'<div class="grid-bg"></div><div class="num">{p["n"]}</div>'
            '<img class="foot-logo" src="assets/logo/technext-horizontal-white.png" alt="TechNext">'
            f'<div class="in" id="d-{p["id"]}"><div class="eyebrow">Practice {p["n"]} · {p["name"]}</div><div class="h1">{p["title"]}</div>'
            f'<p class="lead">{p["lead"]}</p><div class="list">{lst}</div></div>')

def service(n, s):
    p = PR[s["p"]]
    meta = "".join(f'<div class="row"><span>{k}</span><b>{v}</b></div>' for k, v in s["meta"])
    spec = "".join(f'<div class="r"><span>{k}</span><div>{v}</div></div>' for k, v in s["spec"])
    if s["apps"]:
        from data import ODOO_CATS
        names = {a: nm for _, apps in ODOO_CATS for a, nm, _, _ in apps}
        names.update({"web_studio": "Studio", "accountant": "Invoicing", "iot": "IoT"})
        spec += '<div class="r"><span>Odoo apps</span><div class="apps">' + "".join(f'<span class="chip">{oi(a, 3.4)}{names.get(a, a)}</span>' for a in s["apps"]) + '</div></div>'
    faq = "".join(f'<div class="qa"><div class="q">{q}</div><p>{a}</p></div>' for q, a in s["faq"])
    return f'''<div class="sv" id="{s["id"]}">
<div class="sv-top"><div class="ttl"><div style="display:flex;gap:2mm;align-items:center"><span class="ref"><i></i>{s["code"]}</span><span class="eyebrow">{s["name"]}</span></div>
<div class="h1" style="font-size:25pt">{s["title"]}</div><p class="lead" style="font-size:9.6pt">{s["lead"]}</p></div><div class="meta">{meta}</div></div>
<div class="vis">{VIS[s["vis"]]()}</div>
<div class="sv-body"><div><div class="sec-h"><span class="n">A</span><span class="t">What's included</span></div><ul class="inc">{"".join(f"<li>{i}</li>" for i in s["inc"])}</ul></div>
<div><div class="sec-h"><span class="n">B</span><span class="t">Specification</span></div><div class="spec">{spec}</div></div></div>
<div class="faq"><div class="faq-h sec-h"><span class="n">C</span><span class="t">Questions clients ask</span></div>{faq}</div>
</div>'''

def odoo_apps(n, cats, first):
    blocks = ""
    for cat, apps in cats:
        rows = "".join(f'<div style="display:flex;gap:3mm;align-items:center;padding:2.3mm 0;border-bottom:.25mm solid var(--line)">{oi(a, 7)}'
                       f'<div style="flex:1"><div style="font:700 8.4pt/1.2 var(--fd);color:var(--ink);display:flex;gap:2mm;align-items:center">{nm}{" <span class=\"tag bl\">Focus</span>" if f else ""}</div>'
                       f'<div style="font:500 7pt/1.35 var(--fb);color:var(--muted)">{d}</div></div></div>' for a, nm, d, f in apps)
        blocks += f'<div><div style="padding-bottom:2mm;border-bottom:.5mm solid var(--ink)" class="eyebrow" ><span style="color:var(--ink)">{cat}</span></div>{rows}</div>'
    head = ('<div class="eyebrow b">Odoo apps we implement</div><div class="h1" style="margin-top:4mm">The full suite, <span class="mk">one database.</span></div>'
            '<p class="lead" style="margin-top:4mm;max-width:156mm">We implement the full Odoo suite, and our first focus is Accounting, Sales and Inventory. Every app shares the same customers, products and accounts, so adding one later needs no integration project.</p>'
            if first else '<div class="eyebrow b">Odoo apps we implement · continued</div><div class="h2" style="margin-top:4mm">Supply chain, people, marketing, <span class="mk">services and productivity.</span></div>')
    foot = ('<div class="small" style="margin-top:auto">Odoo app icons are Odoo S.A. marks, shown in their own colours. Licences are billed by Odoo per user per month; Odoo\'s One App Free plan covers a single app.</div>')
    return f'<div class="ct" id="{"odoo-apps" if first else "odoo-apps-2"}">{head}<div style="display:grid;grid-template-columns:1fr 1fr;gap:7mm 9mm;margin-top:7mm">{blocks}</div>{foot}</div>'

def method(n):
    steps = [("Discovery", "We map how orders, stock and money move today and match each step to an Odoo app. Output: a written scope."),
             ("Configuration", "Apps set up on a staging copy, never on live data. Standard features first."),
             ("Data migration", "Customers, vendors and products in full; opening balances and open items. The old system stays for history."),
             ("Training &amp; UAT", "Role-based sessions on your own data; your team runs real tasks end to end."),
             ("Integration", "Banks, payments, stores and the tools you keep, tested on staging with real records."),
             ("Go-live &amp; support", "Cut-over on an agreed date, then support, fixes, month-end help and upgrades.")]
    cards = "".join(f'<div style="display:grid;grid-template-columns:16mm 1fr;gap:4mm;padding:4.4mm 0;border-bottom:.25mm solid var(--line)">'
                    f'<div style="font:800 22pt/1 var(--fd);color:{"var(--blue)" if i < 5 else "var(--deep)"};letter-spacing:-.04em">0{i + 1}</div>'
                    f'<div><div class="h3">{t}</div><p style="font-size:8.6pt;margin-top:1.4mm">{d}</p></div></div>' for i, (t, d) in enumerate(steps))
    need = ["A short description of how your process runs today", "A decision-maker for scope questions",
            "The people who run sales, stock and finance, for discovery and training", "Access to the data you want to bring across"]
    return f'''<div class="ct" id="method"><div class="eyebrow b">Our implementation method</div>
<div class="h1" style="margin-top:4mm">Six steps, <span class="mk">one team throughout.</span></div>
<div style="display:grid;grid-template-columns:1.35fr 1fr;gap:10mm;margin-top:7mm">
 <div style="border-top:.5mm solid var(--ink)">{cards}</div>
 <div style="display:flex;flex-direction:column;gap:5mm">
  <div class="card w" style="padding:6mm"><div class="eyebrow" style="color:var(--navy)">What we need from you</div><ul class="inc" style="margin-top:4mm">{"".join(f"<li>{x}</li>" for x in need)}</ul></div>
  <div class="card" style="padding:6mm"><div class="eyebrow">Timeline</div><p style="font-size:8.6pt;margin-top:2.4mm">It depends on the number of apps, companies and integrations, and how clean your data is. The timeline is agreed in the written scope at the end of discovery, and the first phase is kept focused so it goes live sooner.</p></div>
  <div class="card" style="padding:6mm"><div class="eyebrow">Phase 1</div><div style="display:flex;gap:3mm;margin-top:3mm">{"".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;flex:1">{oi(a, 9)}<span style="font:700 7pt/1 var(--fb);color:var(--ink)">{t}</span></div>' for a, t in [("account", "Accounting"), ("sale", "Sales"), ("stock", "Inventory")])}</div>
  <p style="font-size:7.6pt;margin-top:3mm;color:var(--muted)">Where money and stock move. Everything else joins the same database later.</p></div>
 </div></div></div>'''

def hosting(n):
    rows = [("Best for", "Fastest start on standard apps", "Custom development with staging and version control", "Data residency or existing infrastructure"),
            ("Our default", "Most first phases", "When a requirement needs custom code", "Only when IT policy or data rules require it"),
            ("Custom modules", "No. Configuration, plus Studio on the Custom plan", "Yes, version-controlled", "Yes"),
            ("Hosting cost", "Included in the Odoo subscription", "Hosting fees on top of the Custom plan", "Your own infrastructure and operations"),
            ("Upgrades", "Managed by Odoo", "Tested on staging, then scheduled", "Planned and run with you"),
            ("Environments", "Production", "Production, staging and development branches", "As your infrastructure allows"),
            ("Typical client", "Small teams on standard processes", "Growing companies and groups with custom needs", "Regulated or infrastructure-led organisations"),
            ("Move later?", "Yes, to Odoo.sh or on-premise, tested on a copy before switching", "—", "—")]
    tb = ('<table class="tbl"><tr><th style="width:26mm"></th><th>Odoo Online</th><th class="hi">Odoo.sh</th><th>On-premise / your cloud</th></tr>'
          + "".join(f'<tr><td>{a}</td><td>{b}</td><td class="hi">{c}</td><td>{d}</td></tr>' for a, b, c, d in rows) + '</table>')
    return f'''<div class="ct" id="hosting"><div class="eyebrow b">Where Odoo runs</div>
<div class="h1" style="margin-top:4mm">Hosting is a <span class="mk">scoping decision.</span></div>
<p class="lead" style="margin-top:4mm;max-width:156mm">We recommend hosting during discovery, based on whether you need custom modules and any data-residency rules, never by default.</p>
<div style="margin-top:8mm">{tb}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:9mm">
 <div class="card w"><div class="h4">Standard first</div><p style="font-size:7.8pt;margin-top:1.6mm">Configuration, then Studio, then custom modules, the lightest option that meets the requirement.</p></div>
 <div class="card w"><div class="h4">Upgrade-safe</div><p style="font-size:7.8pt;margin-top:1.6mm">Custom work is built as separate modules, so version upgrades stay predictable.</p></div>
 <div class="card w"><div class="h4">Your account</div><p style="font-size:7.8pt;margin-top:1.6mm">The Odoo subscription and database are in your name. You can export your data at any time.</p></div>
</div>
<div class="card" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:8mm;padding:6mm">
 <div><div class="eyebrow">Odoo licences</div><p style="font-size:8pt;margin-top:2mm">Priced per user per month by Odoo, and paid to Odoo. Prices differ by country and currency; see odoo.com/pricing for your market.</p></div>
 <div><div class="eyebrow">Implementation</div><p style="font-size:8pt;margin-top:2mm">Quoted by TechNext in writing: configuration, data migration, training and integration, with support options after go-live.</p></div>
</div></div>'''

def ai_principles(n):
    disc = [("RAG knowledge assistants", "Answers from your documents, cited", "AI-01"), ("AI inside Odoo", "Capture, drafting and lookups in the ERP", "AI-02"),
            ("Workflow automation agents", "Multi-step work prepared for release", "AI-03"), ("AI chatbots", "Web, WhatsApp and in-app, with hand-off", "AI-04")]
    pr = [("Grounded", "Answers come from your own sources and cite them. When documents don't cover a question, it says so."),
          ("Human-approved", "Anything that moves money, commitments or customer data waits for a person."),
          ("Logged", "Every action is logged against the record it touched, and can be replayed or rolled back."),
          ("Scoped", "Access is limited to what each task needs; retrieval follows your access rules."),
          ("Private", "Data stays in your environment; private-cloud or on-premise models where it can't leave."),
          ("Measured", "Accuracy is checked on your own documents before anything runs unattended.")]
    return f'''<div class="ct" id="ai-principles"><div class="eyebrow b">Enterprise AI · Four disciplines</div>
<div class="h1" style="margin-top:4mm">Start with the task that removes <span class="mk">the most manual hours.</span></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:8mm">
 {"".join(f'<a href="#{["ai-rag","ai-odoo","ai-auto","ai-bot"][i]}" class="card" style="min-height:40mm;display:flex;flex-direction:column;gap:2mm"><span class="ref" style="align-self:flex-start"><i></i>{c}</span><div class="h3" style="margin-top:2mm">{t}</div><div style="font-size:7.6pt">{d}</div></a>' for i, (t, d, c) in enumerate(disc))}
</div>
<div style="margin-top:10mm;padding-top:6mm;border-top:.5mm solid var(--ink)"><div class="h2">How our AI <span class="mk">stays in control.</span></div></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6mm 7mm;margin-top:7mm">
 {"".join(f'<div style="border-left:.8mm solid var(--blue);padding-left:4mm"><div class="h3">{t}</div><p style="font-size:8.2pt;margin-top:1.6mm">{d}</p></div>' for t, d in pr)}
</div>
<div class="card w" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:6mm;padding:6mm">
 <div><div class="h4">Do we have to be on Odoo?</div><p style="font-size:7.6pt;margin-top:1.4mm">No. Assistants, agents and chatbots work with the tools you already use. AI inside Odoo is for teams running the ERP.</p></div>
 <div><div class="h4">Who builds it?</div><p style="font-size:7.6pt;margin-top:1.4mm">Our AI engineering hub in Ho Chi Minh City, alongside the Singapore and Taguig City teams on the same project.</p></div>
 <div><div class="h4">How is it priced?</div><p style="font-size:7.6pt;margin-top:1.4mm">On quotation, scoped to the task and the data involved, with a written scope first.</p></div>
</div></div>'''

def offer(n):
    free = ["Custom multi-page website design, styled to your brand", "Your choice of look, colours and layout, with rounds of changes",
            "Setting up the Website app in your Odoo database", "Contact form, mobile layout and basic SEO", "One hand-over call to show your team how to edit it"]
    pay = ["Your Odoo subscription, paid to Odoo at Odoo's price", "More Odoo apps (CRM, invoicing, inventory, HR) if you add them",
           "Your domain name, if you don't have one yet", "Extra pages, an online shop or support, only if you ask"]
    steps = [("Day 1", "Tell us", "Send the form. We reply within one working day and book a 20-minute call about your business and the style you like."),
             ("Day 2–3", "We build it", "We design your website and set it up in your Odoo. You review it and ask for changes."),
             ("When you're ready", "Grow on the same system", "Add CRM, invoicing or inventory later. No moving data, no second system.")]
    return f'''<div class="ct" id="offer">
<div class="eyebrow b">Website design with your Odoo</div>
<div class="h1" style="margin-top:4mm;max-width:156mm">We design your website on Odoo. <span class="mk">Our work is on us.</span></div>
<p class="lead" style="margin-top:4mm;max-width:156mm">Our designers build a full multi-page website around your brand and set it up in your Odoo at no charge. It runs on your own Odoo subscription, ready for more apps, and can be live in as little as three days.</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:8mm">
 <div class="card" style="padding:6mm;border:.5mm solid var(--blue)"><div class="eyebrow b">From TechNext · our work</div><ul class="inc" style="margin-top:4mm">{"".join(f"<li>{x}</li>" for x in free)}</ul></div>
 <div class="card" style="padding:6mm"><div class="eyebrow">What you pay for</div><ul class="inc" style="margin-top:4mm">{"".join(f"<li>{x}</li>" for x in pay)}</ul>
 <p style="font-size:7.6pt;margin-top:3mm;color:var(--muted)">Every cost is stated in writing before we start.</p></div>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:9mm;padding-top:6mm;border-top:.5mm solid var(--ink)">
 {"".join(f'<div><div class="eyebrow b">{d}</div><div class="h3" style="margin-top:2mm">{t}</div><p style="font-size:8pt;margin-top:1.6mm">{x}</p></div>' for d, t, x in steps)}
</div>
<div class="card w" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:8mm;padding:6mm">
 <div><div class="h4">Who owns the website and the data?</div><p style="font-size:7.8pt;margin-top:1.4mm">You do. The Odoo subscription and database are in your name, and you can export your data or move to another partner at any time.</p></div>
 <div><div class="h4">I need an online shop or a special feature.</div><p style="font-size:7.8pt;margin-top:1.4mm">Your website design still comes with it. Online shops, bookings or custom features are quoted separately, in writing.</p></div>
</div>
<div class="small" style="margin-top:4mm">Apply at technext.asia/get-started. Odoo itself is not free; your website runs on your own Odoo subscription, which you pay to Odoo.</div>
</div>'''

def industries(n, items, first):
    cards = ""
    base = 0 if first else 4
    for k, (name, img, apps, desc, pts) in enumerate(items):
        cards += (f'<div class="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column">'
                  f'<div style="height:24mm;background:linear-gradient(140deg,#0F2350,#1E4691 70%,#2D5DB8);position:relative;display:flex;align-items:center;justify-content:space-between;padding:0 5mm">'
                  f'<div><div style="font:700 6pt/1 var(--fb);letter-spacing:.16em;color:#9DB3DD">INDUSTRY 0{base + k + 1}</div><div style="font:800 13.5pt/1.1 var(--fd);color:#fff;margin-top:1.6mm;letter-spacing:-.02em">{name}</div></div>'
                  f'<div style="display:flex;gap:1.6mm">{"".join(oi(a, 7.5) for a in apps)}</div></div>'
                  f'<div style="padding:4.4mm 5mm;display:flex;flex-direction:column;gap:2mm;flex:1"><p style="font-size:8.2pt;color:var(--ink)">{desc}</p>'
                  f'<ul class="inc" style="gap:1.4mm;margin-top:1mm">{"".join(f"<li style=\"font-size:7.6pt\">{x}</li>" for x in pts)}</ul>'
                  f'<div style="margin-top:auto;padding-top:3mm;border-top:.25mm solid var(--line)"><div class="eyebrow b" style="font-size:6pt">Where we start</div><p style="font-size:7.6pt;margin-top:1.4mm;color:var(--ink)">{IND_EXTRA[name][0]}</p></div>'
                  f'<div class="qa" style="padding-top:2.6mm"><div class="q" style="font-size:7.8pt">{IND_EXTRA[name][1]}</div><p>{IND_EXTRA[name][2]}</p></div></div></div>')
    head = ('<div class="eyebrow b">Odoo by industry</div><div class="h1" style="margin-top:4mm">Built around <span class="mk">how your sector works.</span></div>'
            if first else '<div class="eyebrow b">Odoo by industry · continued</div><div class="h2" style="margin-top:4mm">Projects, patients, trips <span class="mk">and memberships.</span></div>')
    return f'<div class="ct" {"id=\"industries\"" if first else ""}>{head}<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:7mm;flex:1;grid-auto-rows:1fr">{cards}</div></div>'

def local(n):
    cols = [("Singapore", "SG", ["GST and IRAS reporting under Odoo 20 localisation", "SFRS-aligned accounting", "Ready for the GST InvoiceNow requirement, phased from 1 Nov 2025 to 1 Apr 2031", "On-site work from our Waterloo Street HQ"]),
            ("Philippines", "PH", ["BIR 2306 and 2307 withholding certificates generated from vendor bills", "Philippine payroll: basic pay, benefits, taxes, overtime", "Forms 1601-C, 2316 and 1604-C with Alphalist DAT exports", "SSS and Pag-IBIG loan deductions; EIS connection planned in discovery where required"]),
            ("Vietnam", "VN", ["Odoo 20 follows Circular 99 for accounting", "01/GTGT VAT reporting", "SInvoice e-invoicing", "AI engineering hub in Ho Chi Minh City"])]
    c = "".join(f'<div class="card" style="padding:6mm;display:flex;flex-direction:column;gap:3mm"><div style="display:flex;justify-content:space-between;align-items:center"><div class="h2" style="font-size:17pt">{t}</div>'
                f'<span style="font:800 10pt/1 var(--fd);color:#fff;background:var(--blue);border-radius:1.4mm;padding:1.6mm 2.2mm">{k}</span></div><ul class="inc">{"".join(f"<li>{x}</li>" for x in pts)}</ul></div>' for t, k, pts in cols)
    return f'''<div class="ct" id="local"><div class="eyebrow b">Localisation</div>
<div class="h1" style="margin-top:4mm">One database, <span class="mk">each country's rules.</span></div>
<p class="lead" style="margin-top:4mm;max-width:156mm">Odoo runs a company per country in one database, each with its own localisation, currencies and reports, with intercompany transactions between them. These are the Odoo 20 changes we plan around.</p>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:8mm">{c}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:8mm">
 <div class="card w" style="padding:6mm"><div class="h4">Moving to Odoo 20</div><p style="font-size:8pt;margin-top:1.6mm">We upgrade existing databases on a staging copy first, migrate customisations and switch over on the date you choose.</p></div>
 <div class="card w" style="padding:6mm"><div class="h4">Groups across borders</div><p style="font-size:8pt;margin-top:1.6mm">See ERP-08 for consolidation, inter-company eliminations and access per entity.</p></div>
</div>
<div class="small" style="margin-top:auto">Based on Odoo 20 release notes and the Singapore GST InvoiceNow timeline, as summarised on technext.asia in October 2026. Confirm your own compliance dates with your adviser.</div></div>'''

def offices(n):
    o = [("Singapore", "Headquarters", "261 Waterloo Street, #03-36, Waterloo Centre, Singapore 180261", "Sales, discovery workshops and on-site work with clients in Singapore. Support is led from here."),
         ("Taguig City, Philippines", "Main development &amp; consulting hub", "Level 9, IP Center, Taguig City, Metro Manila", "Odoo configuration, custom modules and integrations, with finance, HR, sales and marketing alongside."),
         ("Ho Chi Minh City, Vietnam", "AI engineering hub", "62 Nguyễn Thị Nhung, Phường Hiệp Bình, Ho Chi Minh City", "AI agents and automation, knowledge and RAG systems, chatbots and assistants, and local LLM deployment.")]
    c = "".join(f'<div style="display:grid;grid-template-columns:12mm 1fr 1fr;gap:6mm;padding:7mm 0;border-bottom:.25mm solid var(--line)">'
                f'<div style="font:800 22pt/1 var(--fd);color:var(--blue)">0{i + 1}</div><div><div class="h2" style="font-size:16pt">{t}</div><div class="eyebrow b" style="margin-top:2mm">{r}</div>'
                f'<p style="font-size:8.2pt;margin-top:2.6mm;color:var(--ink)">{a}</p></div><p style="font-size:8.6pt;padding-top:1mm">{d}</p></div>' for i, (t, r, a, d) in enumerate(o))
    return f'''<div class="ct" id="offices"><div class="eyebrow b">Where we work</div>
<div class="h1" style="margin-top:4mm">Three hubs, <span class="mk">one project team.</span></div>
<p class="lead" style="margin-top:4mm;max-width:156mm">We work on-site in Singapore and remotely with clients in 10+ countries. Ask us about on-site work at your location.</p>
<div style="margin-top:8mm;border-top:.5mm solid var(--ink)">{c}</div>
<div class="card w" style="margin-top:8mm;padding:6mm"><div class="eyebrow" style="color:var(--navy)">How one project moves between hubs</div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:4mm"><div style="background:#fff;border-radius:2.4mm;padding:4mm"><div style="font:800 9pt/1 var(--fd);color:var(--blue)">01</div><div class="h4" style="margin-top:2mm">Singapore</div><div style="font-size:7.4pt;margin-top:1.2mm">Discovery workshops, scope and on-site sessions</div></div><div style="background:#fff;border-radius:2.4mm;padding:4mm"><div style="font:800 9pt/1 var(--fd);color:var(--blue)">02</div><div class="h4" style="margin-top:2mm">Taguig City</div><div style="font-size:7.4pt;margin-top:1.2mm">Configuration, custom modules and integrations</div></div><div style="background:#fff;border-radius:2.4mm;padding:4mm"><div style="font:800 9pt/1 var(--fd);color:var(--blue)">03</div><div class="h4" style="margin-top:2mm">Ho Chi Minh City</div><div style="font-size:7.4pt;margin-top:1.2mm">AI features, when AI is in scope</div></div><div style="background:#fff;border-radius:2.4mm;padding:4mm"><div style="font:800 9pt/1 var(--fd);color:var(--blue)">04</div><div class="h4" style="margin-top:2mm">Singapore</div><div style="font-size:7.4pt;margin-top:1.2mm">Go-live, training and support led from HQ</div></div></div></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;margin-top:auto;padding-top:7mm">
 {"".join(f'<div class="stat"><div class="v">{v}</div><div class="k">{k}</div></div>' for v, k in [("10+", "Countries with clients"), ("11+", "Enterprise clients"), ("3", "Hubs across Asia"), ("1", "Team after go-live")])}
</div></div>'''

def start(n):
    steps = [("Tell us", "Send the form at technext.asia, email sales@technext.asia or message us on WhatsApp. Share how your business runs today."),
             ("Discovery call", "We walk through how your company works and what would change. No pitch before we understand the problem."),
             ("Written scope", "We say what to set up first and send a written quotation, stating what is included and what is not."),
             ("Go live", "We set it up, train your team and support you after go-live.")]
    chk = ["Which services interest you (use the codes in this catalogue)", "How many users, companies and locations",
           "The systems you use today, and which you'd like to keep", "Integrations you know you need: banks, stores, payment gateways",
           "Any deadline that matters, such as a financial year-end or InvoiceNow date"]
    return f'''<div class="ct" id="start"><div class="eyebrow b">How to start</div>
<div class="h1" style="margin-top:4mm">Tell us what <span class="mk">slows you down.</span></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:8mm">
 {"".join(f'<div class="card" style="min-height:52mm;display:flex;flex-direction:column;gap:2mm"><div style="font:800 20pt/1 var(--fd);color:var(--blue)">{i + 1}</div><div class="h3">{t}</div><p style="font-size:7.8pt">{d}</p></div>' for i, (t, d) in enumerate(steps))}
</div>
<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:6mm;margin-top:8mm">
 <div class="card w" style="padding:6mm"><div class="eyebrow" style="color:var(--navy)">Helpful to include in your first message</div><ul class="inc" style="margin-top:4mm">{"".join(f"<li>{x}</li>" for x in chk)}</ul></div>
 <div class="card" style="padding:6mm;display:flex;flex-direction:column;gap:3.4mm">
  <div class="eyebrow">Contact</div>
  {"".join(f'<div><div style="font:600 6.4pt/1 var(--fb);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)">{k}</div><div style="font:700 10.5pt/1.3 var(--fd);color:var(--ink);margin-top:1mm">{v}</div></div>' for k, v in [("Email", "sales@technext.asia"), ("WhatsApp", "+65 8839 6998"), ("Web", "technext.asia/quotation"), ("LinkedIn", "linkedin.com/company/technextasia")])}
 </div>
</div>
<div class="card" style="margin-top:auto;padding:6mm;display:grid;grid-template-columns:1fr 1fr;gap:8mm">
 <div><div class="h4">Who replies?</div><p style="font-size:7.8pt;margin-top:1.4mm">The TechNext team, from sales@technext.asia. WhatsApp messages go to +65 8839 6998.</p></div>
 <div><div class="h4">What do you do with my details?</div><p style="font-size:7.8pt;margin-top:1.4mm">We use them only to reply. See technext.asia/privacy.</p></div>
</div></div>'''

def back(n):
    return ('<div class="div" style="position:absolute;inset:0"><div class="grid-bg"></div>'
            '<div style="position:absolute;left:17mm;right:17mm;top:70mm">'
            '<img src="assets/logo/technext-vertical-white.png" style="height:34mm" alt="TechNext">'
            '<div style="font:800 30pt/1.05 var(--fd);color:#fff;letter-spacing:-.03em;margin-top:14mm;max-width:150mm">You don\'t need to hire<br>your own team.</div>'
            '<div style="font:500 10pt/1.6 var(--fb);color:#DDE7F8;margin-top:6mm">Odoo ERP Solution and AI Automation · IoT · Apps · Networks</div></div>'
            '<div style="position:absolute;left:17mm;right:17mm;bottom:40mm;display:grid;grid-template-columns:repeat(3,1fr);gap:8mm;border-top:.25mm solid rgba(255,255,255,.25);padding-top:6mm">'
            + "".join(f'<div><div style="font:700 6.2pt/1 var(--fb);letter-spacing:.16em;color:#9DB3DD">{k}</div><div style="font:600 9pt/1.5 var(--fb);color:#fff;margin-top:2mm">{v}</div></div>'
                      for k, v in [("CONTACT", "sales@technext.asia<br>WhatsApp +65 8839 6998"), ("WEB", "technext.asia<br>@technextasia"),
                                   ("OFFICES", "Singapore · Taguig City<br>Ho Chi Minh City")]) +
            '</div><div style="position:absolute;left:17mm;right:17mm;bottom:16mm;display:flex;justify-content:space-between;align-items:flex-end">'
            '<div style="font:500 6.4pt/1.6 var(--fb);color:#9DB3DD">TECHNEXT PTE. LTD. (UEN 202699888G)<br>261 Waterloo Street, #03-36, Waterloo Centre, Singapore 180261<br>'
            + EDITION + ' · Information correct as of October 2026. Odoo is a trademark of Odoo S.A.</div>'
            '<div style="background:#fff;border-radius:2.4mm;padding:2.4mm 3.2mm"><img src="assets/logo/odoo-ready-partner.png" style="height:10mm" alt="Odoo Ready Partner"></div></div></div>')

# ---------------------------------------------------------------- assemble
def plan():
    seq = [("cover", None, "bare", None), ("about", None, "std", "About"), ("contents", None, "std", "Contents"), ("anatomy", None, "std", "How we engage")]
    for p in PRACTICES:
        seq.append(("div:" + p["id"], p["id"], "div", "d-" + p["id"]))
        for s in S:
            if s["p"] == p["id"]:
                seq.append(("svc:" + s["id"], p["id"], "std", s["id"]))
        if p["id"] == "erp":
            seq += [("apps1", "erp", "std", "odoo-apps"), ("apps2", "erp", "std", "odoo-apps-2"), ("method", "erp", "std", "method"), ("hosting", "erp", "std", "hosting")]
        if p["id"] == "ai":
            seq.insert(len(seq) - 4, ("ai-principles", "ai", "std", "ai-principles"))
        if p["id"] == "mkt":
            seq.append(("offer", "mkt", "std", "offer"))
    seq += [("ind1", None, "std", "industries"), ("ind2", None, "std", "industries-2"), ("local", None, "std", "local"),
            ("offices", None, "std", "offices"), ("start", None, "std", "start"), ("back", None, "bare", None)]
    return seq

def main():
    seq = plan()
    pmap = {}
    for i, (key, pid, kind, anchor) in enumerate(seq, 1):
        if anchor:
            pmap[anchor] = i
    labels = {"ind1": "Odoo by industry", "ind2": "Odoo by industry", "local": "Localisation", "offices": "Where we work", "start": "How to start",
              "about": "About", "contents": "Contents", "anatomy": "How we engage"}
    out = []
    for i, (key, pid, kind, anchor) in enumerate(seq, 1):
        if key == "cover": inner = cover(i)
        elif key == "back": inner = back(i)
        elif key == "about": inner = about(i)
        elif key == "contents": inner = contents(i, pmap)
        elif key == "anatomy": inner = anatomy(i)
        elif key.startswith("div:"): inner = divider(i, PR[pid], pmap)
        elif key.startswith("svc:"): inner = service(i, next(s for s in S if s["id"] == key[4:]))
        elif key == "apps1": inner = odoo_apps(i, ODOO_CATS[:4], True)
        elif key == "apps2": inner = odoo_apps(i, ODOO_CATS[4:], False)
        elif key == "method": inner = method(i)
        elif key == "hosting": inner = hosting(i)
        elif key == "ai-principles": inner = ai_principles(i)
        elif key == "offer": inner = offer(i)
        elif key == "ind1": inner = industries(i, INDUSTRIES[:4], True)
        elif key == "ind2": inner = industries(i, INDUSTRIES[4:], False)
        elif key == "local": inner = local(i)
        elif key == "offices": inner = offices(i)
        elif key == "start": inner = start(i)
        out.append(chrome(i, pid, inner, kind, labels.get(key, "")))
    html = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="color-scheme" content="light"><meta name="robots" content="noindex">'
            '<title>TechNext Services Catalogue</title><style>' + CSS + '</style></head><body><main class="book">' + "".join(out) + '</main></body></html>')
    html = html.encode("ascii", "xmlcharrefreplace").decode("ascii")
    with open(os.path.join(ROOT, "print.html"), "w", encoding="utf-8") as f:
        f.write(html)
    write_bookjson(seq, pmap)
    print("pages:", len(seq))


def write_bookjson(seq, pmap):
    import json
    guides = {"erp": [("Odoo apps we implement", "odoo-apps"), ("Our implementation method", "method"), ("Where Odoo runs", "hosting")],
              "ai": [("How our AI stays in control", "ai-principles")], "mkt": [("Website design with your Odoo", "offer")], "tech": []}
    chapters = []
    for p in PRACTICES:
        secs = [[f'{s["code"]} · {s["name"]}', pmap[s["id"]]] for s in S if s["p"] == p["id"]]
        secs += [[g, pmap[a]] for g, a in guides[p["id"]]]
        secs.sort(key=lambda x: x[1])
        chapters.append({"no": p["n"], "title": p["name"], "page": pmap["d-" + p["id"]], "sections": secs})
    chapters.append({"no": "05", "title": "Industries &amp; reference".replace("&amp;", "&"), "page": pmap["industries"], "sections": [
        ["Odoo by industry", pmap["industries"]], ["Odoo by industry (continued)", pmap["industries-2"]], ["Localisation: SG, PH, VN", pmap["local"]],
        ["Where we work", pmap["offices"]], ["How to start", pmap["start"]]]})
    n = len(seq)
    labels = {"1": "Cover", "2": "About TechNext", "3": "Contents", "4": "How we engage", str(n): "Back cover"}
    for p in PRACTICES:
        labels[str(pmap["d-" + p["id"]])] = f'Practice {p["n"]} · {p["name"]}'
    cfg = {
        "_readme": "GENERATED by _src/build.py from the catalogue page plan. Edit _src/build.py / data.py, then rebuild.",
        "title": "Services Catalogue", "edition": "Edition 2026/27", "brand": "TechNext",
        "publisher": "TechNext Pte. Ltd. (UEN 202699888G)",
        "address": "261 Waterloo Street, #03-36, Waterloo Centre, Singapore 180261",
        "contact": {"email": "sales@technext.asia", "website": "https://technext.asia/", "orderEmail": "sales@technext.asia"},
        "shop": {"shopUrl": "https://technext.asia/quotation", "label": "Get a quotation"},
        "settings": {"flipSound": True, "startPage": 1, "indexPages": [], "hideInBookMode": []},
        "front": [["Cover", 1], ["About TechNext", 2], ["Contents", 3], ["How we engage", 4]],
        "back": [["Back cover · contact", n]],
        "pageLabels": labels, "chapters": chapters, "hotspots": [],
    }
    with open(os.path.join(ROOT, "book", "book.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
