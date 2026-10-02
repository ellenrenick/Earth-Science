"""Create the Volcanic Materials ID Lab as a Canvas New Quiz (unpublished).

Usage: python3 build_quiz.py COURSE_ID [SITE_URL]
Canvas auth is injected by the session proxy; outside it, set CANVAS_TOKEN.
"""
import html, json, os, sys, uuid, urllib.request

COURSE = sys.argv[1]
SITE = sys.argv[2] if len(sys.argv) > 2 else "https://claude.ai/artifact/KmmQFBXnyRKrP3og5uFHp7"
HOST = "https://kernhigh.instructure.com"
DATA = json.load(open(os.path.join(os.path.dirname(__file__), "quiz_key.json")))


def call(method, path, body=None):
    req = urllib.request.Request(HOST + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"})
    if os.environ.get("CANVAS_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["CANVAS_TOKEN"])
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read() or "null")


INSTRUCTIONS = f"""<p><strong>Open the <a href="{SITE}" target="_blank" rel="noopener">Volcanic Materials ID Lab</a> in a new tab.</strong></p>
<ol>
<li>For each of the 15 specimens, read the specimen tag, look through the hand lens, and measure the specimen on the grid.</li>
<li>Use the <strong>ID Guide</strong> tab to make all 7 choices in the specimen's notebook.</li>
<li>When you finish, open <strong>My Lab Sheet</strong> and copy each row into the matching question below.</li>
</ol>
<p>Each specimen is worth 1 point, with partial credit for each correct choice.</p>"""


def item_for(pos, sid, answers):
    blanks, scoring, lines, working = [], [], [], []
    for (key, label, opts), ans in zip(DATA["fields"], answers):
        bid = str(uuid.uuid4())
        choices = [{"id": str(uuid.uuid4()), "position": i + 1, "item_body": o} for i, o in enumerate(opts)]
        correct = next(c for c in choices if c["item_body"] == ans)
        blanks.append({"id": bid, "answer_type": "dropdown", "choices": choices})
        scoring.append({"id": bid, "scoring_algorithm": "Equivalence",
                        "scoring_data": {"value": correct["id"], "blank_text": ans}})
        lines.append(f'<p>{label}: <span id="blank_{bid}"></span></p>')
        working.append(f"<p>{label}: `{html.escape(ans)}`</p>")
    return {"item": {
        "position": pos, "points_possible": 1, "entry_type": "Item",
        "entry": {
            "title": f"Specimen {sid}",
            "item_body": f"<p><strong>Specimen {sid}</strong></p>" + "".join(lines),
            "interaction_type_slug": "rich-fill-blank",
            "interaction_data": {"blanks": blanks},
            "scoring_data": {"value": scoring, "working_item_body": f"<p><strong>Specimen {sid}</strong></p>" + "".join(working)},
            "scoring_algorithm": "MultipleMethods",
            "properties": {"shuffle_rules": {"blanks": {"children": {str(i): {"children": None} for i in range(len(blanks))}}}},
            "calculator_type": "none",
        }}}


if __name__ == "__main__":
    only = int(os.environ.get("ONLY", "0"))
    quiz_id = os.environ.get("QUIZ_ID")
    if not quiz_id:
        q = call("POST", f"/api/quiz/v1/courses/{COURSE}/quizzes", {"quiz": {
            "title": "LAB Volcanic Materials Identification (New)",
            "instructions": INSTRUCTIONS,
            "points_possible": 15,
            "assignment_group_id": os.environ.get("GROUP_ID"),
            "published": False,
            "quiz_settings": {"one_at_a_time_type": "none", "allow_backtracking": True,
                              "multiple_attempts": {"multiple_attempts_enabled": False}},
        }})
        quiz_id = q["id"]
        print("quiz", quiz_id)
    for pos, (sid, ans) in enumerate(DATA["key"].items(), 1):
        if only and pos != only:
            continue
        r = call("POST", f"/api/quiz/v1/courses/{COURSE}/quizzes/{quiz_id}/items", item_for(pos, sid, ans))
        print("item", pos, sid, r.get("id"))
