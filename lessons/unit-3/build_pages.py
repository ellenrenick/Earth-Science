"""Creates Unit 3 student and teacher lesson pages in the Canvas sandbox and places them in modules.

Run from this folder. Requires network access to kernhigh.instructure.com with a Canvas token
(injected by the session proxy). Everything is created unpublished.
"""
import json, sys, urllib.request, urllib.error
from content import LESSONS, LT

COURSE = 300209
H = f"https://kernhigh.instructure.com/api/v1/courses/{COURSE}"
UNIT_MODULE = 1637025
CFA_IDS = {"3.1": 13882130, "3.2": 13882132, "3.3": 13882134, "3.4": 13882136, "3.5": 13882138}
BOX = 'style="background:#eef5fb;border-left:5px solid #2b6cb0;padding:10px 14px;margin:12px 0"'
TBOX = 'style="background:#fff7e6;border-left:5px solid #c05621;padding:10px 14px;margin:12px 0"'


def call(m, p, body=None):
    r = urllib.request.Request(H + p, method=m, data=json.dumps(body).encode() if body else None,
                               headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as x:
            return json.load(x)
    except urllib.error.HTTPError as e:
        sys.exit(f"{m} {p} -> {e.code}: {e.read().decode()[:800]}")


def student_title(L):
    return f"Unit 3 Lesson {L['num']} ({L['days']}): {L['title']}"


def teacher_title(L):
    return f"TEACHER: Unit 3 Lesson {L['num']} ({L['days']}): {L['title']}"


def student_html(L):
    tg = "".join(f"<li><strong>{k}</strong> {LT[k]}</li>" for k in L["targets"])
    head = f"<div {BOX}><p><strong>{L['days']}</strong> &middot; Unit 3: Forces Beneath Our Feet (HS-ESS2-3)</p>"
    head += f"<p><strong>Driving question:</strong> What is inside Earth, and why does it move?</p>"
    head += (f"<p><strong>Learning target{'s' if len(L['targets']) > 1 else ''}:</strong></p><ul>{tg}</ul>" if tg else "") + "</div>"
    nb = f"<h2>Notebook setup</h2><div {BOX}>{L['notebook']}<p><em>Your notebook is your answer sheet for this lesson. Keep it neat; your teacher will check it.</em></p></div>"
    slides = "".join(f"<hr><h2>Slide {i}: {h}</h2>{body}" for i, (h, body) in enumerate(L["slides"], 1))
    return head + nb + slides


def teacher_html(L, student_url):
    t = L["teacher"]
    rows = "".join(f"<tr><td>{mins}</td><td>{what}</td></tr>" for mins, what in t["agenda"])
    tg = ", ".join(L["targets"]) or "none (launch)"
    cfa = f"<p><strong>CFA:</strong> Unit 3 CFA {L['cfa']} (Mastery Path opens Review {L['cfa']} for scores under 67.5%).</p>" if L.get("cfa") else ""
    return (f"<div {TBOX}><p><strong>Teacher page &middot; keep unpublished.</strong> Students never see this page.</p>"
            f"<p><strong>{L['days']}</strong> &middot; Targets: {tg} &middot; "
            f"<a href=\"/courses/{COURSE}/pages/{student_url}\">Student page</a></p>{cfa}</div>"
            f"<h2>At a glance</h2><p>{t['glance']}</p>"
            f"<h2>Materials and prep</h2><p>{t['materials']}</p>"
            f"<h2>Agenda (minutes)</h2><table border=\"1\" cellpadding=\"6\" style=\"border-collapse:collapse\">"
            f"<tr><th>Min</th><th>What happens</th></tr>{rows}</table>"
            f"<h2>Teaching notes</h2>{t['notes']}"
            f"<h2>Answer key</h2>{t['key']}"
            f"<h2>Supports</h2><p>{t['supports']}</p>")


# 1. Pages
made = []
for L in LESSONS:
    sp = call("POST", "/pages", {"wiki_page": {"title": student_title(L), "body": student_html(L), "published": False,
                                               "editing_roles": "teachers"}})
    tp = call("POST", "/pages", {"wiki_page": {"title": teacher_title(L), "body": teacher_html(L, sp["url"]),
                                               "published": False, "editing_roles": "teachers"}})
    made.append({"num": L["num"], "student": sp["url"], "teacher": tp["url"]})
    print(L["num"], sp["url"], "|", tp["url"])

# 2. Teacher module (separate, unpublished)
tm = call("POST", "/modules", {"module": {"name": "Unit 3 TEACHER PAGES (keep unpublished)", "position": 13}})
for i, m in enumerate(made, 1):
    call("POST", f"/modules/{tm['id']}/items", {"module_item": {"type": "Page", "page_url": m["teacher"], "position": i}})
print("teacher module", tm["id"])

# 3. Student pages into the Unit 3 module, each lesson under its own header
items = call("GET", f"/modules/{UNIT_MODULE}/items?per_page=100")
by_content = {i.get("content_id"): i for i in items}
headers = [i for i in items if i["type"] == "SubHeader"]
lt_header = {h["title"].split(":")[0].replace("Learning target ", ""): h for h in headers if h["title"].startswith("Learning target")}
pt_header = next(h for h in headers if h["title"] == "Practice test")
csa_header = next(h for h in headers if h["title"].startswith("Common summative"))


def header_for(L):
    title = f"Lesson {L['num']} ({L['days']}): {L['title']}"
    existing = {2: lt_header.get("3.1"), 3: lt_header.get("3.2"), 4: lt_header.get("3.3"), 6: lt_header.get("3.4"),
                7: lt_header.get("3.5"), 9: pt_header, 10: csa_header}.get(L["num"])
    if existing:
        call("PUT", f"/modules/{UNIT_MODULE}/items/{existing['id']}", {"module_item": {"title": title}})
        return existing["id"]
    return call("POST", f"/modules/{UNIT_MODULE}/items", {"module_item": {"type": "SubHeader", "title": title}})["id"]


tail = {2: [CFA_IDS["3.1"]], 3: [CFA_IDS["3.2"]], 4: [CFA_IDS["3.3"]], 6: [CFA_IDS["3.4"]], 7: [CFA_IDS["3.5"]],
        9: [13882096], 10: [13881975]}
followers = {CFA_IDS["3.1"]: [13882129], CFA_IDS["3.2"]: [13882131], CFA_IDS["3.3"]: [13882133],
             CFA_IDS["3.4"]: [13882135], CFA_IDS["3.5"]: [13882137], 13882096: [13882099, 13882100]}
order = []
for L, m in zip(LESSONS, made):
    order.append(header_for(L))
    order.append(call("POST", f"/modules/{UNIT_MODULE}/items",
                      {"module_item": {"type": "Page", "page_url": m["student"]}})["id"])
    for cid in tail.get(L["num"], []):
        order.append(by_content[cid]["id"])
        order += [by_content[f]["id"] for f in followers.get(cid, [])]
for pos, item_id in enumerate(order, 1):
    call("PUT", f"/modules/{UNIT_MODULE}/items/{item_id}", {"module_item": {"position": pos}})
json.dump({"pages": made, "teacher_module": tm["id"], "order": order}, open("canvas_ids.json", "w"), indent=1)
print("unit module items placed:", len(order))
