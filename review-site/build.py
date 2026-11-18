#!/usr/bin/env python3
"""Build the personalized CFA review site from live Canvas data.

Usage: python3 build.py [--units 4] [--course 342899] [--out dist/index.html]

Reads the roster, every "Unit N CFA <id>: <title>" assignment's scores, and the
matching "Unit N Review <id>: ..." assignment's page content. Writes ONE
self-contained HTML file. Student IDs are never stored in plaintext: the data
is keyed by a salted SHA-256 of the student ID.
"""
import argparse, hashlib, json, os, re, secrets, sys, unicodedata, urllib.request

BASE = "https://kernhigh.instructure.com/api/v1"
PROFICIENT = 2.67  # Proficient band is 2.7; 2.67 (e.g. 8/3) counts too. Below this = review
MASTERED = 3.5
HERE = os.path.dirname(os.path.abspath(__file__))


def get(path):
    """GET all pages of a Canvas list endpoint (token injected by the proxy)."""
    url, out = f"{BASE}{path}", []
    while url:
        with urllib.request.urlopen(urllib.request.Request(url)) as r:
            data = json.load(r)
            link = r.headers.get("Link", "")
        if isinstance(data, list):
            out += data
        else:
            return data
        m = re.search(r'<([^>]+)>; rel="next"', link)
        url = m.group(1) if m else None
    return out


def norm(sid):
    """Student ID -> digits only ('651-439 ' -> '651439')."""
    return re.sub(r"\D", "", str(sid))


def key(salt, sid):
    return hashlib.sha256((salt + norm(sid)).encode()).hexdigest()[:20]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", default="342899")
    ap.add_argument("--units", default="4", help="comma-separated unit numbers to include (default: 4)")
    ap.add_argument("--out", default=os.path.join(HERE, "dist", "index.html"))
    a = ap.parse_args()
    c = f"/courses/{a.course}"
    units = {u.strip() for u in a.units.split(",")}

    assigns = get(f"{c}/assignments?per_page=100")
    cfas, reviews = {}, {}
    for x in assigns:
        m = re.match(r"\s*Unit (\d+) CFA ([\w.\-]+):\s*(.+)", x["name"])
        if m and x["published"] and m[1] in units:
            cfas[(m[1], m[2])] = (x, m[3].strip())
        m = re.match(r"\s*Unit (\d+) Review ([\w.\-]+):", x["name"])
        if m:
            reviews[(m[1], m[2])] = x

    users = get(f"{c}/users?enrollment_type[]=student&per_page=100")
    uid = {u["id"]: u for u in users}

    targets = []
    for (unit, tid), (asg, title) in sorted(cfas.items(), key=lambda kv: (int(kv[0][0]), kv[0][1])):
        subs = {s["user_id"]: s for s in get(f"{c}/assignments/{asg['id']}/submissions?per_page=100")}
        # A CFA counts as "given" once anyone has actually submitted it.
        given = any(s.get("submitted_at") for s in subs.values())
        rev = reviews.get((unit, tid))
        html = rev["description"] if rev else ""
        html = re.sub(r"<p>Your CFA score was[^<]*</p>\s*", "", html)
        m = re.search(r"Learning target [^:]+:</strong>\s*(.*?)</p>", html, re.S)
        targets.append(dict(unit=unit, id=tid, title=title, given=given,
                            goal=re.sub(r"<[^>]+>", "", m[1]).strip() if m else title,
                            html=html, cfa_url=asg["html_url"], _subs=subs))

    salt = secrets.token_hex(8)
    students = {}
    for u in users:
        row = []
        for t in targets:
            s = t["_subs"].get(u["id"])
            if not t["given"]:
                row.append(None)            # CFA not given yet: leave out
            elif s is None or s.get("excused"):
                row.append("x")             # excused / no record
            elif not s.get("submitted_at"):
                row.append("n")             # not taken (auto-zero)
            else:
                row.append(round(s["score"] or 0, 2))
        sid = norm(u.get("sis_user_id") or "")
        if not sid:
            print(f"WARN: a student has no ID; skipped (user {u['id']})", file=sys.stderr); continue
        k = key(salt, sid)
        if k in students:
            print("WARN: duplicate student ID; dropping", file=sys.stderr); students.pop(k); continue
        students[k] = row

    for t in targets:
        t.pop("_subs")
    pr = json.load(open(os.path.join(HERE, "practice.json"), encoding="utf-8"))
    payload = dict(practice=pr, salt=salt, proficient=PROFICIENT, mastered=MASTERED,
                   built=__import__("datetime").date.today().isoformat(),
                   targets=targets, students=students)
    tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    tpl = tpl.replace("/*__ENGINE__*/", open(os.path.join(HERE, "engine.js"), encoding="utf-8").read())
    html = tpl.replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/"))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(html)
    print(f"{len(users)} students, {len(students)} name keys, "
          f"{sum(t['given'] for t in targets)}/{len(targets)} CFAs given -> {a.out}")


if __name__ == "__main__":
    main()
