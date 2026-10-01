"""Writes compact HTML for each student/teacher doc; Drive converts text/html uploads into Google Docs."""
import json, html, os
L = json.load(open("lessons.json"))
os.makedirs("gdoc_html", exist_ok=True)
A = "#C2410C"

def runs(rs):
    out = ""
    for r in rs:
        t = html.escape(r["text"])
        if r.get("b"): t = f"<b>{t}</b>"
        if r.get("i"): t = f"<i>{t}</i>"
        if r.get("href"): t = f'<a href="{r["href"]}">{t}</a>'
        out += t
    return out

def blocks(bs):
    out, lst = "", None
    for b in bs:
        kind = ("ol" if b.get("ordered") else "ul") if b["t"] == "li" else None
        if lst and (kind != lst or (kind == "ol" and b.get("n") == 1)):
            out += f"</{lst}>"; lst = None
        if b["t"] == "table":
            out += '<table border="1" cellpadding="4" style="border-collapse:collapse">' + "".join(
                "<tr>" + "".join(f'<{"th" if c["h"] else "td"}>{runs(c["runs"]) or "&nbsp;"}</{"th" if c["h"] else "td"}>' for c in row) + "</tr>"
                for row in b["rows"]) + "</table><p></p>"
        elif kind:
            if not lst: out += f"<{kind}>"; lst = kind
            out += f"<li>{runs(b['runs'])}</li>"
        else:
            out += f"<p>{runs(b['runs'])}</p>"
    if lst: out += f"</{lst}>"
    return out

def lines(n): return "".join("<p>______________________________________________________________________________</p>" for _ in range(n))

def need(s):
    txt = " ".join(r["text"] for b in s["blocks"] if b["t"] != "table" for r in b["runs"])
    h = s["h"]
    if h.startswith("Show what you know") or "vocabulary" in h.lower(): return 0
    if "Exit" in h or "Do Now" in h: return 3
    if "Reading" in h or "CER" in h: return 6
    return 4 if ("?" in txt or "______" in txt or any(w in txt for w in ("Draw", "Write", "Explain", "Finish", "Copy", "List", "Describe"))) else 0

for l in L:
    fn = f"Unit3-Lesson{l['num']:02d}"
    h = lambda t, lvl=2: f'<h{lvl} style="color:{A}">{html.escape(t)}</h{lvl}>'
    s = f"<h1>Lesson {l['num']}: {html.escape(l['title'])}</h1><p>Unit 3: Forces Beneath Our Feet &middot; {l['days']} &middot; Student notebook guide and answer sheet</p>"
    s += "<p>Name: ________________________ Period: ____ Date: __________</p>"
    s += f'<p><b>Lesson webpage:</b> <a href="{l["student_url"]}">open the lesson on Canvas</a></p>'
    if l["targets"]:
        s += h("Learning target" + ("s" if len(l["targets"]) > 1 else ""), 3) + "<ul>" + "".join(f"<li><b>{t['code']}</b> {html.escape(t['text'])}</li>" for t in l["targets"]) + "</ul>"
    s += h("Notebook setup") + blocks(l["notebook"]) + "<p><i>No notebook today? Use this sheet as your answer sheet and staple it into your notebook later.</i></p>"
    for i, sl in enumerate(l["slides"], 1):
        if sl["h"].startswith(("Learning target", "Today's targets")): continue
        s += h(f"Slide {i}: {sl['h']}") + blocks(sl["blocks"]) + lines(need(sl))
    open(f"gdoc_html/{fn}-STUDENT.html", "w").write(s)

    t = l["teacher"]
    s = f"<h1>TEACHER: Lesson {l['num']}: {html.escape(l['title'])}</h1><p>Unit 3: Forces Beneath Our Feet (HS-ESS2-3) &middot; {l['days']}</p>"
    s += f'<p><b>Teacher page (Canvas):</b> <a href="{l["teacher_url"]}">open</a><br><b>Student page (Canvas):</b> <a href="{l["student_url"]}">open</a><br><b>Slides:</b> {fn} slide deck (same folder)</p>'
    s += f"<p><b>Targets:</b> {', '.join(x['code'] for x in l['targets']) or 'none (launch)'}"
    s += (f" &middot; <b>CFA:</b> Unit 3 CFA {l['cfa']} (Mastery Path opens Review {l['cfa']} under 67.5%)" if l.get("cfa") else "") + "</p>"
    s += h("At a glance") + f"<p>{html.escape(t['glance'])}</p>" + h("Materials and prep") + blocks(t["materials"])
    s += h("Agenda") + '<table border="1" cellpadding="4" style="border-collapse:collapse"><tr><th>Minutes</th><th>What happens</th></tr>' + "".join(f"<tr><td>{html.escape(m)}</td><td>{html.escape(w)}</td></tr>" for m, w in t["agenda"]) + "</table>"
    s += h("Teaching notes") + blocks(t["notes"]) + h("Answer key") + blocks(t["key"]) + h("Supports") + f"<p>{html.escape(t['supports'])}</p>"
    open(f"gdoc_html/{fn}-TEACHER.html", "w").write(s)
