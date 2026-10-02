"""Create the Ch 4 Quiz (unpublished) with a real-sample pumice ID question.

Usage: python3 pumice_question.py COURSE_ID [QUIZ_ID]
Students hold a real pumice sample; the card gives only what they cannot observe themselves.
Same 7 dropdowns as the Volcanic Materials ID Lab, with no ID guide.
"""
import html, json, os, sys, uuid, urllib.request

COURSE = sys.argv[1]
HOST = "https://kernhigh.instructure.com"
FIELDS = json.load(open(os.path.join(os.path.dirname(__file__), "quiz_key.json")))["fields"]
# Tephra size assumes a sample under 6.4 cm. Change "2–64 mm" if your sample is bigger.
KEY = ["glassy", "vesicular", "felsic", "rhyolite", "pyroclastic (tephra)", "2–64 mm", "pumice"]


def call(method, path, body=None):
    req = urllib.request.Request(HOST + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"})
    if os.environ.get("CANVAS_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["CANVAS_TOKEN"])
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read() or "null")


TD = 'style="padding:6px 10px;border-bottom:1px solid #d3d8d8;vertical-align:top"'
TH = 'style="padding:6px 10px;border-bottom:1px solid #d3d8d8;vertical-align:top;text-align:left;width:11em;font-size:0.85em;text-transform:uppercase;letter-spacing:0.05em;color:#59626a"'
CARD = f"""<p><strong>Rock identification: real sample</strong></p>
<p>Use the pumice sample your teacher gives you <strong>and</strong> the specimen card below. Look closely at the sample (use a hand lens if one is available) and measure its longest side with a ruler. Then choose an answer from each dropdown.</p>
<table style="border-collapse:collapse;background:#f7f5ec;border:1px solid #d3d8d8;max-width:640px;width:100%">
<tbody>
<tr><th {TH}>Specimen</th><td {TD}><strong>Sample P-1</strong> (your real sample)</td></tr>
<tr><th {TH}>Collected from</th><td {TD}>Loose fragments from a thick, pale layer that covers hills and valleys downwind of a volcano.</td></tr>
<tr><th {TH}>How it got there</th><td {TD}>It fell out of the sky from a tall eruption column. The layer gets thinner the farther you go from the volcano.</td></tr>
<tr><th {TH}>SiO₂ (silica)</th><td {TD}><strong>71.5%</strong></td></tr>
<tr><th {TH}>Float test</th><td {TD}>Floats</td></tr>
<tr><th {TH}>Size</th><td {TD}>Measure the longest side of your sample with a ruler.</td></tr>
</tbody></table>"""


def item(pos):
    blanks, scoring, lines, working = [], [], [], []
    for (key, label, opts), ans in zip(FIELDS, KEY):
        bid = str(uuid.uuid4())
        choices = [{"id": str(uuid.uuid4()), "position": i + 1, "item_body": o} for i, o in enumerate(opts)]
        correct = next(c for c in choices if c["item_body"] == ans)
        blanks.append({"id": bid, "answer_type": "dropdown", "choices": choices})
        scoring.append({"id": bid, "scoring_algorithm": "Equivalence", "scoring_data": {"value": correct["id"], "blank_text": ans}})
        lines.append(f'<p>{label}: <span id="blank_{bid}"></span></p>')
        working.append(f"<p>{label}: `{html.escape(ans)}`</p>")
    return {"item": {"position": pos, "points_possible": 7, "entry_type": "Item", "entry": {
        "title": "Volcanic material ID: pumice (real sample)",
        "item_body": CARD + "".join(lines),
        "interaction_type_slug": "rich-fill-blank",
        "interaction_data": {"blanks": blanks},
        "scoring_data": {"value": scoring, "working_item_body": CARD + "".join(working)},
        "scoring_algorithm": "MultipleMethods",
        "properties": {"shuffle_rules": {"blanks": {"children": {str(i): {"children": None} for i in range(len(blanks))}}}},
        "calculator_type": "none"}}}


if __name__ == "__main__":
    quiz_id = sys.argv[2] if len(sys.argv) > 2 else None
    if not quiz_id:
        q = call("POST", f"/api/quiz/v1/courses/{COURSE}/quizzes", {"quiz": {
            "title": "Ch 4 Quiz", "assignment_group_id": "647930", "published": False,
            "instructions": "<p>Chapter 4: Volcanism &amp; Extrusive Rocks.</p>"}})
        quiz_id = q["id"]
        print("quiz", quiz_id)
    r = call("POST", f"/api/quiz/v1/courses/{COURSE}/quizzes/{quiz_id}/items", item(1))
    print("item", r.get("id"))
