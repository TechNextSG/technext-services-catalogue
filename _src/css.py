CSS = r"""
@font-face{font-family:"Jakarta";src:url(assets/fonts/plus-jakarta-sans-latin.woff2) format("woff2");font-weight:200 800;font-display:block}
@font-face{font-family:"Inter";src:url(assets/fonts/inter-latin.woff2) format("woff2");font-weight:100 900;font-display:block}
@font-face{font-family:"Caveat";src:url(assets/fonts/caveat-latin.woff2) format("woff2");font-weight:400 700;font-display:block}
:root{
  --blue:#3167CA;--navy:#1E4691;--deep:#0F2350;--ink:#1F1F3D;--body:#4C4C63;--muted:#62627A;
  --line:#E7E4E9;--wash:#EAF0FB;--mist:#DDE7F8;--sky:#6FA0F5;--alt:#FAF9FB;--ok:#137A4A;--amber:#A96B00;--red:#D93A30;--plum:#714B67;
  --fd:"Jakarta","Plus Jakarta Sans",Arial,sans-serif;--fb:"Inter",Arial,sans-serif;--fh:"Caveat",cursive;
  --mx:17mm;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#D9DEE8}
body{font-family:var(--fb);color:var(--body);font-size:9pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact;background:#D9DEE8}
img{display:block;max-width:100%}
a{color:inherit;text-decoration:none}
b,strong{color:var(--ink);font-weight:600}
@page{size:210mm 297mm;margin:0}
.book{display:flex;flex-direction:column;align-items:center;gap:10mm;padding:10mm 0 20mm}
.page{width:210mm;height:297mm;background:#fff;position:relative;overflow:hidden;box-shadow:0 2px 6px rgba(15,35,80,.10),0 30px 60px -30px rgba(15,35,80,.35);page-break-after:always;break-after:page}
@media print{html,body{background:#fff}.book{display:block;padding:0;gap:0}.page{box-shadow:none}}

/* ---------- running chrome ---------- */
.rh{position:absolute;left:var(--mx);right:var(--mx);top:10mm;height:8mm;display:flex;align-items:center;justify-content:space-between;border-bottom:.25mm solid var(--line);font:600 6.6pt/1 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.rh .l{display:flex;align-items:center;gap:2.6mm}
.rh .l img{height:3.6mm}
.rh .l i{width:.25mm;height:3.2mm;background:var(--line)}
.rh .r b{color:var(--blue);font-weight:700}
.rf{position:absolute;left:var(--mx);right:var(--mx);bottom:9mm;display:flex;align-items:center;justify-content:space-between;font:500 6.6pt/1 var(--fb);color:var(--muted);letter-spacing:.02em}
.rf .pn{font:800 11pt/1 var(--fd);color:var(--ink);letter-spacing:-.02em;display:flex;align-items:center;gap:2.5mm}
.rf .pn:before{content:"";width:6mm;height:.6mm;background:var(--blue)}
.page.even .rf{flex-direction:row-reverse}
.page.even .rf .pn{flex-direction:row-reverse}

/* thumb-index tabs */
.tabs{position:absolute;right:0;top:58mm;display:flex;flex-direction:column;gap:2mm}
.tab{width:6.5mm;height:36mm;background:#E3EAF7;border-radius:2mm 0 0 2mm;display:flex;align-items:center;justify-content:center}
.tab span{transform:rotate(90deg);white-space:nowrap;font:700 5.6pt/1 var(--fb);letter-spacing:.12em;text-transform:uppercase;color:#4A5F8C}
.tab.on{background:var(--blue);width:8.5mm}
.tab.on span{color:#fff}
.page.even .tabs{right:auto;left:0}
.page.even .tab{border-radius:0 2mm 2mm 0}
.page.even .tab span{transform:rotate(-90deg)}
.div .tab{background:rgba(255,255,255,.08)}.div .tab span{color:rgba(255,255,255,.75)}.div .tab.on{background:#fff}.div .tab.on span{color:#1E4691}

/* ---------- type ---------- */
.eyebrow{font:700 6.8pt/1 var(--fb);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.eyebrow.b{color:var(--blue)}
.h1{font:800 30pt/1.04 var(--fd);color:var(--ink);letter-spacing:-.03em}
.h2{font:800 21pt/1.08 var(--fd);color:var(--ink);letter-spacing:-.028em}
.h3{font:700 12pt/1.2 var(--fd);color:var(--ink);letter-spacing:-.015em}
.h4{font:700 9.2pt/1.25 var(--fd);color:var(--ink);letter-spacing:-.01em}
.mk{color:var(--blue);background:linear-gradient(transparent 64%,rgba(49,103,202,.16) 64%,rgba(49,103,202,.16) 92%,transparent 92%)}
.lead{font:400 10.6pt/1.55 var(--fb);color:var(--body)}
.kick{font:600 15pt/1 var(--fh);color:var(--blue);transform:rotate(-1.5deg);transform-origin:0 50%;display:inline-block}
.small{font-size:7.6pt;line-height:1.45;color:var(--muted)}
.ref{display:inline-flex;align-items:center;gap:1.6mm;height:5.2mm;padding:0 2.4mm;border-radius:99px;background:var(--wash);color:var(--navy);font:700 6.6pt/1 var(--fb);letter-spacing:.1em;text-transform:uppercase}
.ref i{width:1.4mm;height:1.4mm;border-radius:50%;background:var(--blue)}
.chip{display:inline-flex;align-items:center;gap:1.4mm;height:5mm;padding:0 2.2mm;border-radius:99px;border:.25mm solid var(--line);font:600 6.6pt/1 var(--fb);color:var(--ink);background:#fff;white-space:nowrap}
.chip img{width:3.4mm;height:3.4mm}
.sample{position:absolute;font:700 5.4pt/1 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:var(--amber);background:#FFF4DC;border-radius:99px;padding:1.1mm 2mm;z-index:5}

/* ---------- service page ---------- */
.sv{position:absolute;left:var(--mx);right:var(--mx);top:24mm;bottom:18.5mm;display:flex;flex-direction:column}
.sv-top{display:grid;grid-template-columns:1fr 58mm;gap:8mm;align-items:end}
.sv-top .ttl{display:flex;flex-direction:column;gap:3.4mm}
.sv-top .meta{display:flex;flex-direction:column;gap:2mm;padding-bottom:1mm}
.sv-top .meta .row{display:flex;justify-content:space-between;border-bottom:.25mm solid var(--line);padding-bottom:1.6mm;font-size:7.2pt}
.sv-top .meta .row span{color:var(--muted)}
.sv-top .meta .row b{font-weight:600;text-align:right}
.vis{position:relative;margin-top:5mm;height:84mm;border-radius:3.5mm;background:var(--wash);overflow:hidden;
  background-image:radial-gradient(rgba(49,103,202,.16) .3mm,transparent .35mm);background-size:4mm 4mm;background-position:2mm 2mm;flex:none}
.vis.white{background-color:#F6F8FD}
.vis .cap{position:absolute;left:5mm;bottom:4mm;font:600 6.4pt/1 var(--fb);letter-spacing:.12em;text-transform:uppercase;color:var(--navy);opacity:.75}
.sv-body{display:grid;grid-template-columns:1fr 1fr;gap:9mm;margin-top:6mm}
.inc{list-style:none;display:flex;flex-direction:column;gap:1.7mm}
.inc li{position:relative;padding-left:5.6mm;font-size:8.3pt;line-height:1.4}
.inc li:before{content:"";position:absolute;left:0;top:.6mm;width:3.4mm;height:3.4mm;border-radius:50%;background:var(--wash) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='M3 6.2l2 2 4-4.4' fill='none' stroke='%233167CA' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/100% no-repeat}
.inc li b{font-weight:600}
.sec-h{display:flex;align-items:center;gap:2.4mm;margin-bottom:3mm}
.sec-h .n{font:800 7pt/1 var(--fd);color:#fff;background:var(--blue);border-radius:1.2mm;padding:1mm 1.5mm}
.sec-h .t{font:700 6.8pt/1 var(--fb);letter-spacing:.16em;text-transform:uppercase;color:var(--ink)}
.spec{border-top:.5mm solid var(--ink)}
.spec .r{display:grid;grid-template-columns:24mm 1fr;gap:3mm;padding:1.8mm 0;border-bottom:.25mm solid var(--line);font-size:8pt;line-height:1.4}
.spec .r>span{font:600 6.4pt/1.5 var(--fb);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);padding-top:.3mm}
.spec .r div{color:var(--ink)}
.spec .apps{display:flex;flex-wrap:wrap;gap:1.4mm}
.faq{margin-top:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;padding-top:4mm}
.faq.two{grid-template-columns:1fr 1fr}
.qa{border-top:.25mm solid var(--line);padding-top:3mm}
.qa .q{font:700 8.4pt/1.3 var(--fd);color:var(--ink);margin-bottom:1.4mm;display:flex;gap:1.6mm}
.qa .q:before{content:"Q";color:var(--blue);font-weight:800}
.qa p{font-size:7.3pt;line-height:1.42;color:var(--body)}
.faq-h{grid-column:1/-1;margin-bottom:-1mm}

/* ---------- mock UI parts ---------- */
.win{position:absolute;background:#fff;border-radius:2.4mm;box-shadow:0 .4mm 1mm rgba(31,31,61,.08),0 8mm 16mm -8mm rgba(31,31,61,.28);overflow:hidden}
.win .bar{height:6mm;background:#fff;border-bottom:.25mm solid var(--line);display:flex;align-items:center;gap:1.2mm;padding:0 2.6mm;font:600 6pt/1 var(--fb);color:var(--ink)}
.win .bar i{width:1.6mm;height:1.6mm;border-radius:50%;background:#E3E1E8}
.win .bar .url{margin-left:3mm;flex:1;height:3.6mm;border-radius:99px;background:var(--alt);font:500 5.4pt/3.6mm var(--fb);color:var(--muted);padding:0 2mm}
.win .bar.odoo{background:var(--plum);color:#fff;border:0}
.win .bar.odoo i{background:rgba(255,255,255,.35)}
.tag{display:inline-flex;align-items:center;height:3.8mm;padding:0 1.6mm;border-radius:99px;font:700 5.2pt/1 var(--fb);letter-spacing:.04em;white-space:nowrap}
.tag.ok{background:#E3F4EA;color:var(--ok)}.tag.am{background:#FFF4DC;color:var(--amber)}.tag.bl{background:var(--wash);color:var(--navy)}.tag.rd{background:#FDE8E6;color:var(--red)}.tag.pl{background:#F3ECF1;color:var(--plum)}
.node{position:absolute;background:#fff;border-radius:2.4mm;border:.25mm solid var(--mist);box-shadow:0 6mm 12mm -8mm rgba(31,31,61,.3);display:flex;align-items:center;gap:2mm;padding:2mm 2.6mm;font:600 7pt/1.2 var(--fb);color:var(--ink)}
.node img{width:6mm;height:6mm;flex:none}
.node small{display:block;font:500 5.8pt/1.3 var(--fb);color:var(--muted)}
.node.dark{background:var(--deep);border-color:var(--deep);color:#fff}
.node.dark small{color:#9DB3DD}
.node.blue{background:var(--blue);border-color:var(--blue);color:#fff}
.node.blue small{color:#DDE7F8}
svg.wires{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.ico{width:6mm;height:6mm;stroke:var(--blue);fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.line{height:1.6mm;border-radius:99px;background:#E9ECF3}
.line.d{background:#D5DCEA}
.av{width:5mm;height:5mm;border-radius:50%;background:var(--mist);flex:none}

/* ---------- dividers ---------- */
.div{background:linear-gradient(150deg,#0F2350 0%,#1E4691 58%,#2D5DB8 100%);color:#fff}
.div .grid-bg{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) .25mm,transparent .25mm),linear-gradient(90deg,rgba(255,255,255,.06) .25mm,transparent .25mm);background-size:12mm 12mm;mask-image:linear-gradient(160deg,#000 10%,transparent 75%)}
.div .num{position:absolute;right:14mm;top:6mm;font:800 190pt/1 var(--fd);letter-spacing:-.06em;color:transparent;-webkit-text-stroke:.5mm rgba(255,255,255,.22)}
.div .in{position:absolute;left:var(--mx);right:var(--mx);top:92mm}
.div .eyebrow{color:#9DB3DD}
.div .h1{color:#fff;font-size:44pt;margin-top:4mm}
.div .h1 .mk{color:#fff;background:linear-gradient(transparent 66%,rgba(111,160,245,.45) 66%,rgba(111,160,245,.45) 90%,transparent 90%)}
.div .lead{color:#DDE7F8;max-width:128mm;margin-top:5mm}
.div .list{margin-top:10mm;border-top:.25mm solid rgba(255,255,255,.25)}
.div .list a{display:grid;grid-template-columns:20mm 1fr auto;align-items:center;padding:3.2mm 0;border-bottom:.25mm solid rgba(255,255,255,.18);font:700 11pt/1.2 var(--fd);color:#fff}
.div .list a span{font:700 6.8pt/1 var(--fb);letter-spacing:.14em;color:#9DB3DD}
.div .list a em{font:500 7.4pt/1 var(--fb);color:#9DB3DD;font-style:normal}
.div .art{position:absolute;right:var(--mx);bottom:22mm;width:76mm;border-radius:3mm;overflow:hidden;box-shadow:0 10mm 24mm -10mm rgba(0,0,0,.5);border:.6mm solid rgba(255,255,255,.18)}
.div .rf,.div .rf .pn{color:#fff}
.div .rf{color:#9DB3DD}
.div .rf .pn:before{background:#6FA0F5}
.div .foot-logo{position:absolute;left:var(--mx);top:12mm;height:5.5mm}

/* ---------- generic content pages ---------- */
.ct{position:absolute;left:var(--mx);right:var(--mx);top:24mm;bottom:20mm;display:flex;flex-direction:column}
.card{background:#fff;border:.25mm solid var(--line);border-radius:3mm;padding:5mm}
.card.w{background:var(--wash);border-color:var(--wash)}
.stat .v{font:800 26pt/1 var(--fd);color:var(--blue);letter-spacing:-.04em}
.stat .k{font:600 7pt/1.35 var(--fb);color:var(--ink);margin-top:1.6mm}
.tbl{width:100%;border-collapse:collapse;font-size:7.8pt}
.tbl th{font:700 6.6pt/1.3 var(--fb);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);text-align:left;padding:2.4mm 2.4mm;border-bottom:.5mm solid var(--ink);vertical-align:bottom}
.tbl td{padding:2.4mm;border-bottom:.25mm solid var(--line);vertical-align:top;color:var(--ink);line-height:1.42}
.tbl td:first-child{font-weight:600;color:var(--muted);font-size:7pt;letter-spacing:.02em}
.tbl tr td.hi,.tbl th.hi{background:var(--wash)}
"""
