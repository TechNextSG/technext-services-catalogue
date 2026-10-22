# One drawn visual per service. Stage = 176mm x 84mm (.vis). Absolute positions in mm.
O = "assets/odoo/"

def oi(a, s=6):
    return f'<img src="{O}{a}.svg" style="width:{s}mm;height:{s}mm" alt="">'

def node(x, y, label, sub="", icon="", cls="", w=None, extra=""):
    ww = f"width:{w}mm;" if w else ""
    ic = oi(icon) if icon and not icon.startswith("<") else icon
    sb = f"<small>{sub}</small>" if sub else ""
    return f'<div class="node {cls}" style="left:{x}mm;top:{y}mm;{ww}{extra}">{ic}<div>{label}{sb}</div></div>'

def wires(paths, color="#3167CA", dash=True, w=0.35, arrow=False):
    d = "".join(f'<path d="{p}" />' for p in paths)
    da = 'stroke-dasharray="1.2 1.2"' if dash else ""
    mk = ('<defs><marker id="ah" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="3.2" markerHeight="3.2" orient="auto">'
          '<path d="M0 0L6 3L0 6z" fill="#3167CA"/></marker></defs>') if arrow else ""
    me = 'marker-end="url(#ah)"' if arrow else ""
    return (f'<svg class="wires" viewBox="0 0 176 84" preserveAspectRatio="none">{mk}<g fill="none" stroke="{color}" '
            f'stroke-width="{w}" {da} {me} stroke-linecap="round">{d}</g></svg>')

def sample(x, y):
    return f'<span class="sample" style="left:{x}mm;top:{y}mm">Sample data</span>'

def lines(n, w0=70, gap=2.6, d=False):
    ws = [w0, w0 - 18, w0 - 6, w0 - 26, w0 - 12, w0 - 20]
    return "".join(f'<div class="line{" d" if d and i == 0 else ""}" style="width:{ws[i % 6]}%;margin-top:{gap if i else 0}mm"></div>' for i in range(n))

# ------------------------------------------------------------------ ERP
def erp_impl():
    cx, cy = 88, 40
    ring = [("account", "Accounting", 1), ("sale", "Sales", 1), ("stock", "Inventory", 1), ("purchase", "Purchase", 0),
            ("crm", "CRM", 0), ("point_of_sale", "Point of Sale", 0), ("mrp", "Manufacturing", 0), ("hr", "Employees", 0)]
    import math
    out, paths = [], []
    for i, (ic, nm, ph1) in enumerate(ring):
        a = -math.pi / 2 + i * 2 * math.pi / len(ring)
        x, y = cx + 62 * math.cos(a), cy + 29 * math.sin(a)
        paths.append(f"M{cx} {cy} L{x:.1f} {y:.1f}")
        cls = "" if not ph1 else "ph1"
        style = "border-color:#3167CA;box-shadow:0 0 0 .8mm rgba(49,103,202,.14),0 6mm 12mm -8mm rgba(31,31,61,.3)" if ph1 else ""
        out.append(f'<div class="node {cls}" style="left:{x - 15:.1f}mm;top:{y - 5:.1f}mm;width:30mm;{style}">{oi(ic)}<div>{nm}'
                   + ('<small style="color:#3167CA;font-weight:700">Phase 1</small>' if ph1 else '<small>Add later</small>') + '</div></div>')
    hub = (f'<div style="position:absolute;left:{cx - 17}mm;top:{cy - 11}mm;width:34mm;height:22mm;border-radius:3mm;background:#0F2350;color:#fff;'
           'display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 10mm 20mm -10mm rgba(15,35,80,.6)">'
           '<div style="font:700 5.6pt/1 var(--fb);letter-spacing:.16em;color:#9DB3DD;text-transform:uppercase">Odoo</div>'
           '<div style="font:800 11pt/1.1 var(--fd);margin-top:1.4mm">One database</div>'
           '<div style="font:500 6pt/1 var(--fb);color:#9DB3DD;margin-top:1.4mm">shared records</div></div>')
    return wires(paths) + hub + "".join(out) + '<div class="cap">Phase 1 where money and stock move, then the rest on the same database</div>'

def discovery():
    steps = [("Enquiry", "crm", "Standard", "ok"), ("Quotation", "sale", "Configure", "bl"), ("Stock pick", "stock", "Configure", "bl"),
             ("Delivery", "stock", "Integrate", "am"), ("Invoice", "account", "Standard", "ok"), ("Payment", "account", "Integrate", "am")]
    out = ['<div style="position:absolute;left:6mm;top:7mm;font:700 6pt/1 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:#62627A">How it runs today</div>',
           '<div style="position:absolute;left:6mm;top:44mm;font:700 6pt/1 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:#62627A">Mapped to Odoo</div>']
    today = ["Email + phone", "Excel template", "Paper list", "Courier portal", "Accounting tool", "Bank portal"]
    paths = []
    for i, (st, ic, kind, c) in enumerate(steps):
        x = 6 + i * 27.5
        out.append(f'<div style="position:absolute;left:{x}mm;top:12mm;width:24mm;height:22mm;border-radius:2.4mm;background:#fff;border:.25mm dashed #B9C6E2;padding:2.4mm">'
                   f'<div style="font:700 5.6pt/1 var(--fb);color:#9DB3DD">STEP {i + 1}</div><div class="h4" style="margin-top:1.4mm;font-size:8pt">{st}</div>'
                   f'<div style="font:500 6pt/1.3 var(--fb);color:#62627A;margin-top:1.2mm">{today[i]}</div></div>')
        out.append(f'<div style="position:absolute;left:{x}mm;top:49mm;width:24mm;height:24mm;border-radius:2.4mm;background:#fff;box-shadow:0 6mm 12mm -8mm rgba(31,31,61,.3);'
                   f'padding:2.4mm;display:flex;flex-direction:column;gap:1.6mm">{oi(ic, 6.5)}<div class="h4" style="font-size:7.8pt">{st}</div><span class="tag {c}" style="align-self:flex-start">{kind}</span></div>')
        paths.append(f"M{x + 12} 34.5 L{x + 12} 48.5")
        if i < 5:
            paths.append(f"M{x + 24.4} 61 L{x + 27.2} 61")
    out.append(sample(140, 5.4))
    return wires(paths) + "".join(out)

def customisation():
    layers = [("Custom modules", "Separate, versioned, documented", "#3167CA", "#fff", 74),
              ("Studio", "Fields, views and rules without code", "#6FA0F5", "#fff", 90),
              ("Configuration", "Odoo's own settings, rules and workflows", "#DDE7F8", "#1E4691", 106),
              ("Odoo core", "Never edited. Upgrades stay predictable", "#0F2350", "#fff", 122)]
    out = []
    for i, (t, s, bg, fg, w) in enumerate(layers):
        y = 9 + i * 17
        out.append(f'<div style="position:absolute;left:{10 + (122 - w) / 2}mm;top:{y}mm;width:{w}mm;height:14mm;border-radius:2.4mm;background:{bg};color:{fg};'
                   f'display:flex;align-items:center;justify-content:space-between;padding:0 4mm;box-shadow:0 6mm 12mm -9mm rgba(15,35,80,.45)">'
                   f'<div style="font:800 9pt/1 var(--fd)">{t}</div><div style="font:500 6.2pt/1.3 var(--fb);opacity:.85;text-align:right;max-width:45mm">{s}</div></div>')
    out.append('<div style="position:absolute;left:140mm;top:9mm;bottom:9mm;width:28mm;display:flex;flex-direction:column;justify-content:space-between">'
               '<div style="font:700 6pt/1.3 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:#1E4691">Heavier change, used only when needed</div>'
               '<svg viewBox="0 0 20 60" style="width:8mm;height:44mm;margin-left:6mm"><path d="M10 58 V4" stroke="#3167CA" stroke-width="1.4" fill="none"/><path d="M4 10 L10 3 L16 10" stroke="#3167CA" stroke-width="1.4" fill="none"/></svg>'
               '<div style="font:500 6.2pt/1.35 var(--fb);color:#4C4C63">Code only when configuration can\'t meet the requirement</div></div>')
    return "".join(out)

def integration():
    cx, cy = 88, 42
    sp = [("Bank feeds", "Reconciliation", 8, 8), ("Payment gateways", "Fees + payouts", 8, 36), ("Carriers", "Labels + tracking", 8, 64),
          ("Online store", "Shopify · WooCommerce", 128, 8), ("Marketplaces", "Orders + stock sync", 128, 36), ("Tools you keep", "API + connectors", 128, 64)]
    out, paths = [], []
    ln = '<svg class="ico" viewBox="0 0 24 24" style="width:5.4mm;height:5.4mm"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
    for t, s, x, y in sp:
        out.append(node(x, y, t, s, ln, w=40))
        ex = x + 40 if x < 80 else x
        paths.append(f"M{ex} {y + 6} C{(ex + cx) / 2} {y + 6} {(ex + cx) / 2} {cy} {cx} {cy}")
    hub = (f'<div style="position:absolute;left:{cx - 15}mm;top:{cy - 15}mm;width:30mm;height:30mm;border-radius:50%;background:#fff;border:.6mm solid #714B67;'
           'display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 0 3mm rgba(113,75,103,.08),0 10mm 20mm -10mm rgba(31,31,61,.4)">'
           '<div style="font:800 12pt/1 var(--fd);color:#714B67;letter-spacing:-.02em">odoo</div><div style="font:600 5.6pt/1 var(--fb);color:#62627A;margin-top:1mm">your database</div>'
           '<div style="font:600 5.6pt/1 var(--fb);color:#714B67;margin-top:1mm;letter-spacing:.1em">TWO-WAY</div></div>')
    return wires(paths) + hub + "".join(out) + '<div class="cap" style="left:62mm">Standard connectors first · tested on staging</div>'

def crm():
    cols = [("New", 4, [("Harbour Goods", "Web form", "S$ —"), ("Lim &amp; Co", "WhatsApp", "")]),
            ("Qualified", 3, [("Pacific Clinic", "Email", ""), ("Northwind", "Referral", "")]),
            ("Proposition", 2, [("Atlas Trading", "Quotation sent", "")]),
            ("Won", 1, [("Bayside F&amp;B", "Quotation opened", "")])]
    out = ['<div class="win" style="left:6mm;top:6mm;width:164mm;height:72mm"><div class="bar odoo"><i></i><i></i><i></i>'
           '<span style="margin-left:2mm">CRM · Pipeline</span></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2.6mm;padding:3mm">']
    for nm, n, cards in cols:
        won = nm == "Won"
        out.append(f'<div><div style="display:flex;justify-content:space-between;font:700 6.6pt/1 var(--fb);color:#1F1F3D;padding-bottom:1.8mm;'
                   f'border-bottom:.6mm solid {"#137A4A" if won else "#3167CA"}">{nm}<span style="color:#62627A">{n}</span></div>')
        for t, s, _ in cards:
            out.append(f'<div style="margin-top:2.2mm;border:.25mm solid #E7E4E9;border-radius:1.8mm;padding:2.2mm;background:#fff">'
                       f'<div style="font:700 6.8pt/1.2 var(--fd);color:#1F1F3D">{t}</div><div style="font:500 5.8pt/1.3 var(--fb);color:#62627A;margin-top:.8mm">{s}</div>'
                       f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:1.6mm"><span class="tag {"ok" if won else "bl"}">{"Won" if won else "Next: call"}</span><span class="av" style="width:3.6mm;height:3.6mm"></span></div></div>')
        out.append("</div>")
    out.append("</div>")
    out.append('<div style="position:absolute;left:3mm;right:3mm;bottom:3mm;display:flex;gap:2mm;align-items:center;font:600 6pt/1 var(--fb);color:#62627A">'
               'Routing: <span class="tag bl">Round-robin</span><span class="tag bl">Territory</span><span class="tag bl">Deal value</span>'
               '<span style="margin-left:auto">Won → quotation pre-filled in Sales</span></div></div>')
    return "".join(out) + sample(146, 2.6)

def training():
    ph = [("1", "Administrators", "Users, access rights, settings"), ("2", "Key users", "Deep sessions per team"),
          ("3", "Each team", "Finance · Sales · Warehouse"), ("4", "UAT", "Real tasks end to end"), ("5", "Go-live", "Guides handed over")]
    out = []
    out.append('<div style="position:absolute;left:10mm;right:10mm;top:21mm;height:.5mm;background:#B9C6E2"></div>')
    for i, (n, t, s) in enumerate(ph):
        x = 10 + i * 33.5
        last = i == 4
        out.append(f'<div style="position:absolute;left:{x}mm;top:15mm;width:12mm;height:12mm;border-radius:50%;background:{"#3167CA" if not last else "#0F2350"};color:#fff;'
                   f'display:flex;align-items:center;justify-content:center;font:800 10pt/1 var(--fd);box-shadow:0 0 0 1.4mm #EAF0FB">{n}</div>'
                   f'<div style="position:absolute;left:{x}mm;top:31mm;width:28mm"><div class="h4" style="font-size:8.4pt">{t}</div>'
                   f'<div style="font:500 6.4pt/1.35 var(--fb);color:#62627A;margin-top:1mm">{s}</div></div>')
    # UAT checklist mock
    out.append('<div class="win" style="left:10mm;top:46mm;width:76mm;height:32mm"><div class="bar"><i></i><i></i><i></i><span style="margin-left:2mm">UAT checklist · Sales</span></div><div style="padding:2.4mm 3mm;display:flex;flex-direction:column;gap:1.8mm">')
    for t, st in [("Create quotation from pricelist", "ok"), ("Confirm order, reserve stock", "ok"), ("Partial delivery and backorder", "am"), ("Invoice and register payment", "bl")]:
        lab = {"ok": "Passed", "am": "Question", "bl": "To run"}[st]
        out.append(f'<div style="display:flex;justify-content:space-between;align-items:center;font:500 6.4pt/1 var(--fb);color:#1F1F3D">{t}<span class="tag {st}">{lab}</span></div>')
    out.append("</div></div>")
    out.append('<div class="win" style="left:92mm;top:46mm;width:74mm;height:32mm;display:flex"><div style="width:22mm;background:#EAF0FB;display:flex;align-items:center;justify-content:center">'
               '<svg class="ico" viewBox="0 0 24 24" style="width:10mm;height:10mm"><path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/></svg></div>'
               '<div style="padding:3mm;flex:1"><div style="font:700 5.6pt/1 var(--fb);letter-spacing:.14em;color:#62627A">QUICK-REFERENCE GUIDE</div>'
               '<div class="h4" style="margin-top:1.4mm;font-size:8pt">Month-end close, step by step</div><div style="margin-top:2mm">' + lines(3, 92) + '</div></div></div>')
    return "".join(out) + sample(150, 41)

def support():
    rows = [("#1042", "Add approval step to purchase orders", "Change", "In progress", "am"),
            ("#1041", "Bank feed missing yesterday's lines", "Fix", "Done", "ok"),
            ("#1039", "Month-end: accrual entries", "Month-end", "Done", "ok"),
            ("#1037", "New user for warehouse team", "Access", "Open", "bl")]
    out = ['<div class="win" style="left:6mm;top:7mm;width:104mm;height:70mm"><div class="bar odoo"><i></i><i></i><i></i><span style="margin-left:2mm">Helpdesk · Your support plan</span></div>'
           '<div style="padding:2mm 3mm"><div style="display:grid;grid-template-columns:11mm 1fr 16mm 17mm;gap:2mm;font:700 5.4pt/1 var(--fb);letter-spacing:.12em;color:#62627A;padding:1.6mm 0;border-bottom:.25mm solid #E7E4E9">'
           '<span>TICKET</span><span>REQUEST</span><span>TYPE</span><span>STATUS</span></div>']
    for n, t, ty, st, c in rows:
        out.append(f'<div style="display:grid;grid-template-columns:11mm 1fr 16mm 17mm;gap:2mm;align-items:center;font:500 6.4pt/1.3 var(--fb);color:#1F1F3D;padding:2.6mm 0;border-bottom:.25mm solid #F0EEF2">'
                   f'<span style="color:#62627A">{n}</span><span>{t}</span><span style="color:#62627A">{ty}</span><span class="tag {c}">{st}</span></div>')
    out.append('<div style="display:flex;gap:6mm;margin-top:3mm">' + "".join(
        f'<div><div style="font:800 13pt/1 var(--fd);color:#3167CA">{v}</div><div style="font:600 5.6pt/1.3 var(--fb);color:#62627A;margin-top:.8mm">{k}</div></div>'
        for v, k in [("1", "channel for requests"), ("100%", "requests tracked"), ("0", "forced cut-overs")]) + '</div></div></div>')
    # upgrade lane
    st = [("Staging copy", "Your database, cloned"), ("Migrate modules", "Your customisations moved"), ("Test", "Your team checks"), ("Upgrade", "On the date you choose")]
    out.append('<div style="position:absolute;left:118mm;top:7mm;width:52mm"><div style="font:700 6pt/1 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:#1E4691;margin-bottom:3mm">Version upgrade path</div>')
    for i, (t, s) in enumerate(st):
        out.append(f'<div style="display:flex;gap:2.6mm;align-items:flex-start;margin-bottom:{3 if i < 3 else 0}mm"><div style="width:6mm;height:6mm;border-radius:50%;background:{"#0F2350" if i == 3 else "#3167CA"};color:#fff;font:800 6.4pt/6mm var(--fd);text-align:center;flex:none">{i + 1}</div>'
                   f'<div style="background:#fff;border-radius:2mm;padding:2mm 2.6mm;flex:1;box-shadow:0 5mm 10mm -8mm rgba(31,31,61,.3)"><div class="h4" style="font-size:7.6pt">{t}</div><div style="font:500 6pt/1.3 var(--fb);color:#62627A;margin-top:.6mm">{s}</div></div></div>')
    out.append("</div>")
    return "".join(out) + sample(88, 3)

def enterprise():
    out, paths = [], []
    out.append(node(63, 6, "Group holding", "Consolidated P&amp;L · balance sheet · cash", '<svg class="ico" viewBox="0 0 24 24" style="stroke:#fff"><path d="M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6"/></svg>', "dark", w=50))
    ents = [("Entity · Singapore", "SG localisation · SGD", 8), ("Entity · Philippines", "PH localisation · PHP", 63), ("Entity · Vietnam", "VN localisation · VND", 118)]
    for t, s, x in ents:
        out.append(node(x, 34, t, s, "account", w=50))
        paths.append(f"M88 18 C88 26 {x + 25} 26 {x + 25} 33.5")
    paths += ["M58 40 L62.5 40", "M113 40 L117.5 40"]
    out.append('<div style="position:absolute;left:52mm;top:31mm;font:700 5.2pt/1 var(--fb);color:#714B67;letter-spacing:.08em">INTER-CO</div>')
    out.append('<div style="position:absolute;left:107mm;top:31mm;font:700 5.2pt/1 var(--fb);color:#714B67;letter-spacing:.08em">INTER-CO</div>')
    out.append('<div style="position:absolute;left:8mm;right:8mm;top:56mm;display:grid;grid-template-columns:repeat(4,1fr);gap:3mm">' + "".join(
        f'<div style="background:#fff;border-radius:2.2mm;padding:2.6mm 3mm;border-left:.8mm solid #3167CA"><div class="h4" style="font-size:7.6pt">{t}</div><div style="font:500 6pt/1.35 var(--fb);color:#62627A;margin-top:.8mm">{s}</div></div>'
        for t, s in [("Pilot first", "Template proven on one entity"), ("Eliminations", "Handled by the system"), ("Record rules", "Each entity sees its own data"), ("Audit trail", "Approval chains logged")]) + "</div>")
    return wires(paths) + "".join(out)

# ------------------------------------------------------------------ AI
def rag():
    out = ['<div class="win" style="left:6mm;top:7mm;width:106mm;height:70mm"><div class="bar"><i></i><i></i><i></i><span style="margin-left:2mm">Knowledge assistant</span></div>'
           '<div style="padding:3.4mm;display:flex;flex-direction:column;gap:3mm">'
           '<div style="align-self:flex-end;max-width:78mm;background:#3167CA;color:#fff;border-radius:3mm 3mm .8mm 3mm;padding:2.4mm 3mm;font:500 7pt/1.4 var(--fb)">How many days of annual leave do staff get in their second year?</div>'
           '<div style="max-width:92mm;background:#F6F8FD;border:.25mm solid #DDE7F8;border-radius:3mm 3mm 3mm .8mm;padding:2.6mm 3mm;font:500 7pt/1.45 var(--fb);color:#1F1F3D">'
           'Staff in their second year are entitled to <b>15 days</b> of annual leave, pro-rated for part-time contracts. Unused days carry over up to 5 days.'
           '<div style="display:flex;gap:1.6mm;margin-top:2.2mm;flex-wrap:wrap"><span class="tag bl">[1] HR Policy 4.2 · p.3</span><span class="tag bl">[2] Employment handbook · p.11</span></div></div>'
           '<div style="max-width:92mm;background:#F6F8FD;border:.25mm dashed #B9C6E2;border-radius:3mm;padding:2.2mm 3mm;font:500 6.6pt/1.4 var(--fb);color:#62627A">'
           'Not covered in the sources you can access. Route to HR?</div></div></div>']
    src = [("Policies", "lock"), ("Manuals", ""), ("Contracts", "lock"), ("Wikis", ""), ("Support tickets", ""), ("PDFs", ""), ("Odoo records", "lock")]
    out.append('<div style="position:absolute;left:120mm;top:7mm;width:50mm"><div style="font:700 6pt/1 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:#1E4691;margin-bottom:2.6mm">Connected sources</div>')
    for t, l in src:
        lk = '<svg class="ico" viewBox="0 0 24 24" style="width:3.6mm;height:3.6mm;stroke:#714B67"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>' if l else ""
        out.append(f'<div style="display:flex;align-items:center;justify-content:space-between;background:#fff;border-radius:1.8mm;padding:2mm 2.6mm;margin-bottom:1.6mm;font:600 6.8pt/1 var(--fb);color:#1F1F3D">{t}{lk}</div>')
    out.append('<div style="font:500 5.8pt/1.35 var(--fb);color:#62627A;margin-top:1.4mm">Lock = permission-aware: answers follow who can see the document.</div></div>')
    return "".join(out) + sample(88, 3)

def ai_odoo():
    out = []
    out.append('<div class="win" style="left:6mm;top:9mm;width:44mm;height:62mm;transform:rotate(-2deg)"><div style="padding:3mm"><div style="font:800 8pt/1 var(--fd);color:#1F1F3D">INVOICE</div>'
               '<div style="font:500 5.6pt/1.4 var(--fb);color:#62627A;margin-top:1mm">Coastal Supplies Pte Ltd<br>INV-20931 · 14 Oct 2026</div><div style="margin-top:3mm">' + lines(6, 96) +
               '</div><div style="margin-top:3mm;border-top:.25mm solid #E7E4E9;padding-top:2mm;display:flex;justify-content:space-between;font:700 6.4pt/1 var(--fb);color:#1F1F3D">Total<span>S$4,280.00</span></div>'
               '<div style="position:absolute;inset:0;border:.6mm solid #3167CA;border-radius:2.4mm;box-shadow:inset 0 0 0 30mm rgba(49,103,202,.05)"></div></div></div>')
    out.append(wires(["M52 40 L62 40"], dash=False, w=.5, arrow=True))
    out.append('<div class="win" style="left:64mm;top:7mm;width:106mm;height:70mm"><div class="bar odoo"><i></i><i></i><i></i><span style="margin-left:2mm">Accounting · Vendor bill (draft)</span></div><div style="padding:3mm">'
               '<div style="display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm;font:500 6.4pt/1.3 var(--fb)">' + "".join(
                   f'<div style="border-bottom:.25mm solid #E7E4E9;padding-bottom:1.4mm"><div style="color:#62627A;font-size:5.6pt">{k}</div><div style="color:#1F1F3D;font-weight:600;display:flex;justify-content:space-between">{v}<span class="tag ok" style="height:3.2mm;font-size:4.8pt">AI</span></div></div>'
                   for k, v in [("Vendor", "Coastal Supplies Pte Ltd"), ("Bill reference", "INV-20931"), ("Matched PO", "P00412 · 3 lines"), ("Total", "S$4,280.00")]) + '</div>'
               '<div style="margin-top:3mm;background:#F6F8FD;border-radius:2mm;padding:2.4mm 3mm;font:500 6.2pt/1.45 var(--fb);color:#1F1F3D">'
               '<b style="color:#1E4691">AI note</b> · Quantities match receipt WH/IN/00318. Unit price on line 2 is 3% above the PO.</div>'
               '<div style="display:flex;gap:2mm;margin-top:3mm;align-items:center"><span style="height:6mm;padding:0 3mm;border-radius:1.6mm;background:#714B67;color:#fff;font:600 6.4pt/6mm var(--fb)">Approve &amp; post</span>'
               '<span style="height:6mm;padding:0 3mm;border-radius:1.6mm;border:.25mm solid #E7E4E9;font:600 6.4pt/6mm var(--fb);color:#1F1F3D">Edit</span><span class="tag am" style="margin-left:auto">Awaiting approval</span></div>'
               '<div style="margin-top:3mm;border-top:.25mm solid #E7E4E9;padding-top:2mm;font:500 5.8pt/1.6 var(--fb);color:#62627A">'
               '10:42 · AI read document, matched PO and receipt<br>10:42 · AI drafted bill · waiting for a person to post</div></div></div>')
    return "".join(out) + sample(146, 3)

def automation():
    st = [("Email in", "Supplier sends a quote", "mail", ""), ("Read", "Extracts items and prices", None, ""), ("Classify", "Matches vendor and project", None, ""),
          ("Prepare", "Drafts an RFQ in Odoo", "purchase", ""), ("Approve", "A person releases it", None, "gate"), ("Hand over", "Logged on the record", "account", "")]
    out, paths = [], []
    icons = {"Read": '<svg class="ico" viewBox="0 0 24 24"><path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h5"/></svg>',
             "Classify": '<svg class="ico" viewBox="0 0 24 24"><path d="M4 6h7v5H4zM13 13h7v5h-7zM11 8.5h4v4.5"/></svg>',
             "Approve": '<svg class="ico" viewBox="0 0 24 24" style="stroke:#fff"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/></svg>'}
    for i, (t, s, ic, g) in enumerate(st):
        x = 6 + i * 28
        gate = g == "gate"
        ico = oi(ic, 7) if ic else icons[t]
        out.append(f'<div style="position:absolute;left:{x}mm;top:16mm;width:24mm;height:34mm;border-radius:2.6mm;background:{"#0F2350" if gate else "#fff"};'
                   f'box-shadow:0 6mm 12mm -8mm rgba(31,31,61,.35);padding:3mm;display:flex;flex-direction:column;gap:1.8mm">'
                   f'<div style="font:700 5.4pt/1 var(--fb);color:{"#9DB3DD" if gate else "#9DB3DD"};letter-spacing:.12em">0{i + 1}</div>{ico}'
                   f'<div class="h4" style="font-size:8pt;color:{"#fff" if gate else "#1F1F3D"}">{t}</div><div style="font:500 6pt/1.35 var(--fb);color:{"#9DB3DD" if gate else "#62627A"}">{s}</div></div>')
        if i < 5:
            paths.append(f"M{x + 24.3} 33 L{x + 27.6} 33")
    out.append('<div style="position:absolute;left:6mm;right:6mm;top:58mm;display:flex;gap:3mm;align-items:center">'
               '<span class="chip"><span style="width:2mm;height:2mm;border-radius:50%;background:#137A4A"></span>Running</span>'
               '<span class="chip">Pause workflow</span><span class="chip" style="border-color:#D93A30;color:#D93A30">Kill switch</span>'
               '<span style="margin-left:auto;font:500 6.4pt/1.3 var(--fb);color:#62627A">Every action logged · any step can be replayed or rolled back</span></div>')
    return wires(paths, dash=False, w=.5, arrow=True) + "".join(out) + sample(6, 6)

def chatbot():
    out = ['<div style="position:absolute;left:14mm;top:3mm;width:44mm;height:78mm;border-radius:7mm;background:#1F1F3D;padding:2mm;box-shadow:0 12mm 24mm -12mm rgba(15,35,80,.6)">'
           '<div style="width:100%;height:100%;border-radius:5.4mm;background:#fff;overflow:hidden"><div style="background:#1E4691;color:#fff;padding:5mm 3mm 2.4mm;font:700 7pt/1 var(--fd)">Your company<div style="font:500 5.4pt/1 var(--fb);color:#9DB3DD;margin-top:1mm">Assistant · replies instantly</div></div>'
           '<div style="padding:2.4mm;display:flex;flex-direction:column;gap:1.8mm;font:500 6pt/1.4 var(--fb)">'
           '<div style="align-self:flex-end;background:#3167CA;color:#fff;border-radius:2.4mm 2.4mm .6mm 2.4mm;padding:1.8mm 2.2mm;max-width:34mm">Where is order SO1187?</div>'
           '<div style="background:#F1F4FA;border-radius:2.4mm 2.4mm 2.4mm .6mm;padding:1.8mm 2.2mm;max-width:36mm;color:#1F1F3D">It shipped on 16 Oct and is due on 18 Oct. Tracking: <b>SG4482</b></div>'
           '<div style="align-self:flex-end;background:#3167CA;color:#fff;border-radius:2.4mm 2.4mm .6mm 2.4mm;padding:1.8mm 2.2mm;max-width:34mm">Can I get a bulk quote?</div>'
           '<div style="background:#F1F4FA;border-radius:2.4mm 2.4mm 2.4mm .6mm;padding:1.8mm 2.2mm;max-width:36mm;color:#1F1F3D">Happy to help. How many units, and by when?</div>'
           '<div style="align-self:center;font:600 5.2pt/1 var(--fb);color:#62627A;margin-top:1mm">Passing you to our sales team</div></div></div></div>']
    out.append(wires(["M62 42 C80 42 80 26 96 26", "M62 42 C80 42 80 60 96 60"], dash=True, w=.4))
    out.append(f'<div class="win" style="left:96mm;top:12mm;width:72mm;height:28mm"><div class="bar odoo"><i></i><i></i><i></i><span style="margin-left:2mm">CRM · New lead</span></div>'
               '<div style="padding:2.4mm 3mm;font:500 6.2pt/1.5 var(--fb);color:#1F1F3D"><b>Bulk quote · 200 units</b><br><span style="color:#62627A">Source: Website chat · transcript attached</span>'
               '<div style="margin-top:1.4mm;display:flex;gap:1.4mm"><span class="tag bl">Qualified</span><span class="tag pl">Assigned by rule</span></div></div></div>')
    out.append(f'<div class="win" style="left:96mm;top:46mm;width:72mm;height:28mm"><div class="bar odoo"><i></i><i></i><i></i><span style="margin-left:2mm">Live Chat · Hand-off</span></div>'
               '<div style="padding:2.4mm 3mm;font:500 6.2pt/1.5 var(--fb);color:#1F1F3D"><b>Conversation passed to a person</b><br><span style="color:#62627A">With context and the customer record</span>'
               '<div style="margin-top:1.4mm;display:flex;gap:1.4mm"><span class="tag am">On request</span><span class="tag am">Sentiment</span><span class="tag am">Uncertainty</span></div></div></div>')
    return "".join(out) + sample(146, 3)

# ------------------------------------------------------------------ Marketing
def website():
    out = ['<div class="win" style="left:6mm;top:6mm;width:116mm;height:74mm"><div class="bar"><i></i><i></i><i></i><span class="url">yourcompany.com</span></div>'
           '<div style="display:flex;justify-content:space-between;align-items:center;padding:2.4mm 4mm;border-bottom:.25mm solid #F0EEF2"><div style="width:16mm;height:2.6mm;border-radius:99px;background:#1F1F3D"></div>'
           '<div style="display:flex;gap:3mm">' + "".join('<div class="line" style="width:8mm"></div>' for _ in range(4)) + '<div style="width:12mm;height:3.6mm;border-radius:99px;background:#3167CA;margin-top:-1mm"></div></div></div>'
           '<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:4mm;padding:5mm 4mm"><div><div style="font:800 11pt/1.1 var(--fd);color:#1F1F3D;letter-spacing:-.02em">Clear about what<br>you do, in one line.</div>'
           '<div style="margin-top:2.4mm">' + lines(3, 92) + '</div><div style="display:flex;gap:2mm;margin-top:3mm"><div style="width:18mm;height:5mm;border-radius:99px;background:#3167CA"></div><div style="width:16mm;height:5mm;border-radius:99px;border:.25mm solid #DDE7F8"></div></div></div>'
           '<div style="border-radius:2mm;background:linear-gradient(140deg,#DDE7F8,#EAF0FB);position:relative"><div style="position:absolute;left:4mm;right:4mm;bottom:4mm;height:12mm;border-radius:1.6mm;background:#fff;padding:2mm">' + lines(2, 80) + '</div></div></div>'
           '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;padding:0 4mm">' + "".join(
               '<div style="border:.25mm solid #E7E4E9;border-radius:1.8mm;padding:2.4mm"><div style="width:5mm;height:5mm;border-radius:1.2mm;background:#EAF0FB"></div><div style="margin-top:2mm">' + lines(2, 90, 1.8, True) + '</div></div>' for _ in range(3)) + '</div></div>']
    out.append('<div style="position:absolute;left:112mm;top:30mm;width:24mm;height:48mm;border-radius:3.6mm;background:#1F1F3D;padding:1.2mm;box-shadow:0 10mm 20mm -10mm rgba(15,35,80,.6)">'
               '<div style="width:100%;height:100%;border-radius:2.6mm;background:#fff;padding:2.4mm 2mm"><div style="font:800 5.6pt/1.15 var(--fd);color:#1F1F3D">Clear about what you do.</div>'
               '<div style="margin-top:1.6mm">' + lines(3, 92, 1.4) + '</div><div style="width:12mm;height:3mm;border-radius:99px;background:#3167CA;margin-top:2mm"></div>'
               '<div style="margin-top:2mm;height:12mm;border-radius:1.4mm;background:#EAF0FB"></div></div></div>')
    ck = ["Titles and descriptions", "Sitemap", "Structured data", "Fast, accessible pages", "Forms to your inbox or CRM"]
    out.append('<div style="position:absolute;left:142mm;top:8mm;width:30mm"><div style="font:700 5.6pt/1.3 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:#1E4691;margin-bottom:2.4mm">Built in</div>' + "".join(
        f'<div style="display:flex;gap:1.6mm;align-items:flex-start;font:600 6.2pt/1.3 var(--fb);color:#1F1F3D;margin-bottom:2.2mm"><svg viewBox="0 0 12 12" style="width:3mm;height:3mm;flex:none;margin-top:.2mm"><circle cx="6" cy="6" r="6" fill="#3167CA"/><path d="M3.4 6.2l1.8 1.8 3.4-3.8" stroke="#fff" stroke-width="1.4" fill="none"/></svg>{c}</div>' for c in ck) + '</div>')
    return "".join(out)

def social():
    tiles = [("linear-gradient(140deg,#3167CA,#1E4691)", "#fff", "New in Odoo 20"), ("#fff", "#1F1F3D", "Client story"), ("linear-gradient(140deg,#EAF0FB,#DDE7F8)", "#1E4691", "Quick tip"),
             ("linear-gradient(140deg,#0F2350,#1E4691)", "#fff", "Event recap"), ("#fff", "#1F1F3D", "Team update"), ("linear-gradient(140deg,#DDE7F8,#fff)", "#1E4691", "How-to")]
    out = ['<div style="position:absolute;left:6mm;top:7mm;width:82mm;display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm">']
    for bg, fg, t in tiles:
        out.append(f'<div style="aspect-ratio:3/4;border-radius:2mm;background:{bg};border:.25mm solid #E7E4E9;padding:2.2mm;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 5mm 10mm -8mm rgba(31,31,61,.35)">'
                   f'<div style="width:7mm;height:1.6mm;border-radius:99px;background:{fg};opacity:.35"></div><div style="font:800 7pt/1.1 var(--fd);color:{fg}">{t}</div></div>')
    out.append("</div>")
    days = [("Mon", "LinkedIn", "Approved", "ok"), ("Tue", "Instagram", "Approved", "ok"), ("Wed", "Facebook", "For sign-off", "am"),
            ("Thu", "LinkedIn", "For sign-off", "am"), ("Fri", "Instagram", "Drafting", "bl")]
    out.append('<div class="win" style="left:94mm;top:7mm;width:76mm;height:52mm"><div class="bar"><i></i><i></i><i></i><span style="margin-left:2mm">Content plan · week 43</span></div><div style="padding:1.6mm 3mm">')
    for d, ch, st, c in days:
        out.append(f'<div style="display:grid;grid-template-columns:9mm 1fr auto;align-items:center;padding:1.9mm 0;border-bottom:.25mm solid #F0EEF2;font:600 6.4pt/1 var(--fb);color:#1F1F3D">'
                   f'<span style="color:#62627A">{d}</span><span>{ch}</span><span class="tag {c}">{st}</span></div>')
    out.append("</div></div>")
    out.append('<div class="win" style="left:94mm;top:62mm;width:76mm;height:16mm;display:flex;align-items:center;gap:3mm;padding:0 3mm">'
               '<svg class="ico" viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg><div style="font:600 6.4pt/1.35 var(--fb);color:#1F1F3D">One-page monthly report<br><span style="color:#62627A;font-weight:500">Reach, engagement, leads passed to sales</span></div></div>')
    return "".join(out) + sample(68, 2.6)

def brand():
    out = ['<div class="win" style="left:6mm;top:6mm;width:108mm;height:72mm;display:grid;grid-template-columns:1fr 1fr">'
           '<div style="padding:4mm;border-right:.25mm solid #F0EEF2"><div style="font:700 5.4pt/1 var(--fb);letter-spacing:.14em;color:#62627A">01 · LOGO</div>'
           '<div style="height:24mm;border-radius:1.6mm;background:#F6F8FD;margin-top:2.4mm;display:flex;align-items:center;justify-content:center;gap:2mm">'
           '<div style="width:7mm;height:7mm;border-radius:50% 50% 50% 0;background:#1F1F3D"></div><div style="font:800 9pt/1 var(--fd);color:#1F1F3D;letter-spacing:-.02em">yourbrand</div></div>'
           '<div style="font:700 5.4pt/1 var(--fb);letter-spacing:.14em;color:#62627A;margin-top:4mm">02 · COLOUR</div><div style="display:flex;gap:1.6mm;margin-top:2.4mm">' + "".join(
               f'<div style="flex:1"><div style="height:10mm;border-radius:1.4mm;background:{c};border:.25mm solid #E7E4E9"></div><div style="font:600 4.8pt/1 var(--fb);color:#62627A;margin-top:1mm">{c}</div></div>'
               for c in ["#1F1F3D", "#E4572E", "#F3EDE4", "#FFFFFF"]) + '</div></div>'
           '<div style="padding:4mm"><div style="font:700 5.4pt/1 var(--fb);letter-spacing:.14em;color:#62627A">03 · TYPE</div>'
           '<div style="font:800 22pt/1 var(--fd);color:#1F1F3D;margin-top:2mm;letter-spacing:-.03em">Aa</div><div style="font:500 6pt/1.4 var(--fb);color:#62627A">Headline · Body · Caption</div>'
           '<div style="font:700 5.4pt/1 var(--fb);letter-spacing:.14em;color:#62627A;margin-top:4mm">04 · TEMPLATES</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:1.6mm;margin-top:2.4mm">'
           + "".join(f'<div style="height:10mm;border-radius:1.2mm;background:{b};border:.25mm solid #E7E4E9"></div>' for b in ["#1F1F3D", "#F3EDE4", "#fff", "#E4572E"]) + '</div></div></div>']
    files = [("PowerPoint", "Decks"), ("Canva", "Social"), ("Figma", "Digital"), ("InDesign", "Print")]
    out.append('<div style="position:absolute;left:120mm;top:6mm;width:50mm"><div style="font:700 5.8pt/1 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:#1E4691;margin-bottom:2.6mm">Editable masters</div>')
    for t, s in files:
        out.append(f'<div style="display:flex;align-items:center;gap:2.4mm;background:#fff;border-radius:2mm;padding:2.2mm 2.6mm;margin-bottom:1.8mm;box-shadow:0 5mm 10mm -8mm rgba(31,31,61,.3)">'
                   '<svg class="ico" viewBox="0 0 24 24" style="width:5mm;height:5mm"><path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5"/></svg>'
                   f'<div style="font:700 6.8pt/1.2 var(--fb);color:#1F1F3D">{t}<div style="font:500 5.6pt/1 var(--fb);color:#62627A;margin-top:.6mm">{s}</div></div></div>')
    out.append('<div style="font:500 6pt/1.4 var(--fb);color:#62627A;margin-top:2mm">Plus PDFs for sharing. You own every file delivered.</div></div>')
    return "".join(out) + '<span class="sample" style="left:88mm;top:2.6mm">Fictional brand</span>'

# ------------------------------------------------------------------ BIR
CAP = "font:700 6pt/1 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:#62627A"

def tick(on=True):
    return (f'<span style="width:3.6mm;height:3.6mm;border-radius:1mm;flex:none;display:inline-flex;align-items:center;justify-content:center;'
            f'background:{"#137A4A" if on else "#fff"};border:.3mm solid {"#137A4A" if on else "#B9C6E2"};color:#fff;font:800 5pt/1 var(--fb)">{"&#10003;" if on else ""}</span>')

def bir_einv():
    lines_ = [("Service retainer, October", "1", "&#8369; 80,000.00"), ("Implementation hours", "12", "&#8369; 42,000.00")]
    out = ['<div class="win" style="left:6mm;top:7mm;width:86mm;height:70mm"><div class="bar odoo"><i></i><i></i><i></i><span style="margin-left:2mm">Accounting · Customer invoice</span></div>'
           '<div style="padding:3mm 3.6mm"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div class="h4" style="font-size:9pt">INV/2026/00184</div>'
           '<div style="font:500 6pt/1.4 var(--fb);color:#62627A;margin-top:.8mm">Sample Trading Corp. · Head office · Branch 00000</div></div><span class="tag ok">Posted</span></div>'
           f'<div style="display:grid;grid-template-columns:1fr 8mm 22mm;gap:2mm;margin-top:3.4mm;padding:1.4mm 0;border-bottom:.25mm solid #E7E4E9;{CAP};font-size:5.2pt"><span>ITEM</span><span>QTY</span><span style="text-align:right">AMOUNT</span></div>']
    for t, q, a in lines_:
        out.append(f'<div style="display:grid;grid-template-columns:1fr 8mm 22mm;gap:2mm;padding:2.2mm 0;border-bottom:.25mm solid #F0EEF2;font:500 6.4pt/1.3 var(--fb);color:#1F1F3D"><span>{t}</span><span>{q}</span><span style="text-align:right">{a}</span></div>')
    out.append('<div style="display:flex;justify-content:space-between;padding:2.4mm 0;font:800 7.4pt/1 var(--fd);color:#1F1F3D"><span>Total (VAT inclusive)</span><span>&#8369; 122,000.00</span></div>'
               '<div style="display:flex;gap:1.6mm;flex-wrap:wrap;margin-top:1.4mm"><span class="tag bl">PTI on file</span><span class="tag bl">EIS route: to be scoped</span><span class="tag am">No edits after issue</span></div>'
               '<div style="margin-top:3mm;padding:2mm 2.6mm;border-radius:1.6mm;background:#FAF9FB;font:500 6pt/1.4 var(--fb);color:#62627A">Correction? A credit note for a decrease, a new e-invoice for an increase.</div></div></div>')
    st = [("Draft", "Entered in Odoo", "#3167CA"), ("Posted", "Validated in Odoo", "#3167CA"), ("Locked", "No edits; a credit note corrects", "#0F2350"), ("EIS transmission", "Not in standard Odoo; to be scoped", "#9AA3B8")]
    out.append(f'<div style="position:absolute;left:100mm;top:7mm;width:70mm"><div style="{CAP};color:#1E4691;margin-bottom:3mm">From draft to locked invoice</div>')
    for i, (t, s, c) in enumerate(st):
        out.append(f'<div style="display:flex;gap:2.6mm;align-items:center;margin-bottom:2.2mm"><div style="width:6mm;height:6mm;border-radius:50%;background:{c};color:#fff;font:800 6.4pt/6mm var(--fd);text-align:center;flex:none">{i + 1}</div>'
                   f'<div style="background:#fff;border-radius:2mm;padding:1.8mm 2.6mm;flex:1;box-shadow:0 5mm 10mm -8mm rgba(31,31,61,.3)"><div class="h4" style="font-size:7.6pt">{t}</div><div style="font:500 6pt/1.3 var(--fb);color:#62627A;margin-top:.5mm">{s}</div></div></div>')
    out.append('<div style="margin-top:1mm;background:#0F2350;border-radius:2mm;padding:2.2mm 3mm;display:flex;justify-content:space-between;align-items:center">'
               '<span style="font:700 5.6pt/1 var(--fb);letter-spacing:.14em;color:#9DB3DD">DEADLINE</span><span style="font:800 9pt/1 var(--fd);color:#fff">31 Dec 2026</span></div></div>')
    return "".join(out) + sample(72, 3)

def bir_cas():
    flow = [("Set up Odoo", "Books, invoices", ""), ("Annex B check", "RMC 5-2021", ""), ("Build the pack", "From your Odoo", ""),
            ("File at RDO", "You file", ""), ("RDO decision", "By the BIR", ""), ("ORUS", "You, every year", "")]
    out, paths = [f'<div style="position:absolute;left:6mm;top:6mm;{CAP}">Preparing your CAS or CBA application</div>'], []
    for i, (t, s, ic) in enumerate(flow):
        x = 6 + i * 27.6
        cls = "dark" if i == 3 else ("blue" if i == 0 else "")
        num = f'<span style="width:5.4mm;height:5.4mm;border-radius:50%;flex:none;background:{"#fff" if cls else "#EAF0FB"};color:#1E4691;font:800 6pt/5.4mm var(--fd);text-align:center">{i + 1}</span>'
        out.append(node(x, 11, t, s, ic or num, cls, w=24.6, extra="height:15mm;padding:2mm 2.2mm;font-size:6.8pt"))
        if i < 5:
            paths.append(f"M{x + 24.8} 18.5 L{x + 27.4} 18.5")
    checks = [("Audit trail of all activity, printable and protected", 1), ("Posted entries voided, not modified", 1), ("System-controlled invoice numbering", 1),
              ("Exports of books in CSV or DAT", 1), ("2306, 2307 and 2316 from the system", 1), ("Backups kept for ten years", 0)]
    out.append('<div class="win" style="left:6mm;top:33mm;width:96mm;height:46mm"><div class="bar"><i></i><i></i><i></i><span style="margin-left:2mm">Example check · before you apply</span></div><div style="padding:2mm 3mm">')
    for t, on in checks:
        out.append(f'<div style="display:flex;gap:2.2mm;align-items:center;padding:1.15mm 0;font:500 6.2pt/1.25 var(--fb);color:#1F1F3D">{tick(on)}<span>{t}</span>'
                   f'{"" if on else "<span class=\"tag am\" style=\"margin-left:auto\">Hosting decides</span>"}</div>')
    out.append('</div></div>')
    pack = ["Sworn statement and system description", "Sample invoices and documents", "Sample books and reports", "Printed audit trail", "Signed requirements checklist"]
    out.append('<div class="win" style="left:108mm;top:33mm;width:62mm;height:46mm"><div class="bar odoo"><i></i><i></i><i></i><span style="margin-left:2mm">Application pack</span></div><div style="padding:2.4mm 3mm">')
    out += [f'<div style="display:flex;gap:2mm;align-items:center;padding:1.3mm 0;border-bottom:.25mm solid #F0EEF2;font:500 6.1pt/1.25 var(--fb);color:#1F1F3D">'
            f'<span style="font:800 6pt/1 var(--fd);color:#3167CA;width:3mm">{i + 1}</span>{t}</div>' for i, t in enumerate(pack)]
    out.append('<div style="font:500 5.6pt/1.35 var(--fb);color:#62627A;margin-top:2mm">Cloud set-up: plus a joint sworn statement with the provider.</div></div></div>')
    return wires(paths) + "".join(out) + sample(146, 5)

def bir_forms():
    src = [("purchase", "Vendor bills", "Withholding with ATC"), ("account", "Customer invoices", "Sales and VAT"), ("hr_payroll", "Payroll runs", "Compensation tax")]
    out, paths = [f'<div style="position:absolute;left:6mm;top:6mm;{CAP}">One set of entries</div>'], []
    for i, (ic, t, s) in enumerate(src):
        y = 12 + i * 22
        out.append(node(6, y, t, s, ic, w=46, extra="height:16mm"))
        paths.append(f"M52.5 {y + 8} C60 {y + 8} 60 42 66 42")
    rows = [("2307 / 2306", "Per payee, per quarter", "Generated", "ok"), ("SLSP", "1,284 lines · DAT", "Exported", "ok"), ("SAWT", "52 certificates · DAT", "Exported", "ok"),
            ("QAP", "38 payees · DAT", "Validating", "am"), ("2550Q", "Q3 VAT summary", "Draft", "bl"), ("1601-C", "September payroll", "For review", "bl"), ("2316 · 1604-C", "Yearly, Alphalist DAT", "Planned", "pl")]
    out.append('<div class="win" style="left:66mm;top:6mm;width:104mm;height:73mm"><div class="bar odoo"><i></i><i></i><i></i><span style="margin-left:2mm">Accounting · BIR reports</span></div>'
               f'<div style="padding:1.6mm 3mm"><div style="display:grid;grid-template-columns:22mm 1fr 18mm;gap:2mm;padding:1.6mm 0;border-bottom:.25mm solid #E7E4E9;{CAP};font-size:5.2pt"><span>FORM</span><span>FROM YOUR ENTRIES</span><span>STATUS</span></div>')
    for f, d, s, c in rows:
        out.append(f'<div style="display:grid;grid-template-columns:22mm 1fr 18mm;gap:2mm;align-items:center;padding:2.05mm 0;border-bottom:.25mm solid #F0EEF2;font:500 6.4pt/1.25 var(--fb);color:#1F1F3D">'
                   f'<b style="font:700 6.8pt/1 var(--fd)">{f}</b><span style="color:#62627A">{d}</span><span class="tag {c}">{s}</span></div>')
    out.append('</div></div>')
    return wires(paths) + "".join(out) + sample(146, 1.2)

def bir_audit():
    out = [f'<div style="position:absolute;left:6mm;top:6mm;{CAP}">eLA document request · 10 calendar days</div>']
    out.append('<div style="position:absolute;left:6mm;top:12mm;width:80mm;height:6mm;display:grid;grid-template-columns:repeat(10,1fr);gap:.8mm">'
               + "".join(f'<div style="border-radius:1mm;background:{"#3167CA" if d < 3 else "#DDE7F8"};font:700 5pt/6mm var(--fb);color:{"#fff" if d < 3 else "#1E4691"};text-align:center">{d + 1}</div>' for d in range(10)) + '</div>')
    req = ["Returns and proof of payment", "Registered books and general ledger", "Invoices, bills and supporting documents", "SLSP, 2307s and alphalists", "Audited financial statements"]
    out.append('<div class="win" style="left:6mm;top:23mm;width:80mm;height:56mm"><div class="bar"><i></i><i></i><i></i><span style="margin-left:2mm">Request checklist · Day 3</span></div><div style="padding:2.4mm 3mm">')
    out += [f'<div style="display:flex;gap:2.2mm;align-items:center;padding:1.7mm 0;border-bottom:.25mm solid #F0EEF2;font:500 6.3pt/1.25 var(--fb);color:#1F1F3D">{tick()}<span>{t}</span>'
            f'<span style="margin-left:auto;font:600 5.6pt/1 var(--fb);color:#62627A">Attached</span></div>' for t in req]
    out.append('<div style="margin-top:2.6mm;font:500 6pt/1.4 var(--fb);color:#62627A">Books and lists come from Odoo; returns and audited statements are attached.</div></div></div>')
    trail = [("BILL/2026/0944", "Amount changed by user finance.clerk", "4,200 &#8594; 4,480"), ("INV/2026/00179", "Credit note linked", "Reversal, not an edit"), ("JE/2026/0611", "Change on a posted entry", "Blocked by lock date")]
    out.append('<div class="win" style="left:92mm;top:6mm;width:78mm;height:46mm"><div class="bar odoo"><i></i><i></i><i></i><span style="margin-left:2mm">Accounting · Audit trail</span></div><div style="padding:1.6mm 3mm">')
    out += [f'<div style="padding:2mm 0;border-bottom:.25mm solid #F0EEF2"><div style="display:flex;justify-content:space-between;font:700 6.4pt/1.2 var(--fd);color:#1F1F3D"><span>{r}</span><span style="font:500 5.6pt/1.2 var(--fb);color:#62627A">{v}</span></div>'
            f'<div style="font:500 5.8pt/1.3 var(--fb);color:#62627A;margin-top:.6mm">{t}</div></div>' for r, t, v in trail]
    out.append('</div></div>')
    for i, (t, s) in enumerate([("Hash chain", "Inalterability check passed"), ("Hard lock", "Up to 30 Sep 2026")]):
        out.append(node(92 + i * 40, 57, t, s, '<span style="width:5mm;height:5mm;border-radius:50%;flex:none;background:#E3F4EA;color:#137A4A;font:800 6pt/5mm var(--fb);text-align:center">&#10003;</span>', w=38, extra="height:14mm"))
    return "".join(out) + sample(146, 1.2)

VIS = dict(bir_einv=bir_einv, bir_cas=bir_cas, bir_forms=bir_forms, bir_audit=bir_audit, erp_impl=erp_impl,discovery=discovery, customisation=customisation, integration=integration, crm=crm, training=training, support=support,
           enterprise=enterprise, rag=rag, ai_odoo=ai_odoo, automation=automation, chatbot=chatbot, website=website, social=social, brand=brand)
