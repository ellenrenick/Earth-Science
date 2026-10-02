import json, re, subprocess, sys
from build import inline, table

def md_to_html(md):
    lines = [l for l in md.split('\n') if not l.startswith('# ') and not l.startswith('Name:')]
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if l.startswith('|'):
            t = []
            while i < len(lines) and lines[i].startswith('|'): t.append(lines[i]); i += 1
            out.append(table(t)); continue
        for tag, pat in (('ul', r'- '), ('ol', r'\d+\. ')):
            if re.match(pat, l):
                items = []
                while i < len(lines) and re.match(pat, lines[i]):
                    items.append(re.sub('^' + pat, '', lines[i])); i += 1
                out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
                break
        else:
            if l.startswith('## '): out.append(f'<h3>{inline(l[3:])}</h3>')
            elif l.strip() and l.strip() != '---': out.append(f'<p>{inline(l)}</p>')
            i += 1
    h = '\n'.join(out)
    return re.sub(r'_{6,}', '__________', h)  # shorten long write-on lines

TURN_IN = ('<div style="border:2px solid #2d6cdf;border-radius:6px;padding:8px 12px;margin-bottom:12px">'
           '<p><strong>How to turn this in:</strong> {}</p></div>')
ITEMS = {
 'review': ('Unit 2 Review & Intervention: Cosmic Clues – How Earth Began', 'review.md',
   TURN_IN.format('Type your answers in the text box, numbered by station (for example "2.2 #1: ..."), '
                  'or do the work on paper and upload a photo. Do the vocabulary warm-up, every station for a target you missed, and the exit check.'),
   [('Circle every question you missed in the table below.', 'Find every question you missed in the table below.')]),
 'enrichment': ('Unit 2 Enrichment & Extension: Cosmic Clues – Going Deeper', 'enrichment.md',
   TURN_IN.format('Type your answers in the text box, labeled by challenge and question (for example "B #2: ..."), '
                  'or do the work on paper and upload a photo. If you choose Challenge B, upload a photo of your graph.'),
   [('in your notebook or below each challenge', 'in the text box or on paper')]),
}
BASE = 'https://kernhigh.instructure.com/api/v1/courses/300209'
for key, (title, src, box, fixes) in ITEMS.items():
    md = open(src).read()
    for a, b in fixes:
        assert a in md, a; md = md.replace(a, b)
    desc = box + md_to_html(md)
    open(f'{key}.html', 'w').write(desc)
    body = {'assignment': {'name': title, 'description': desc, 'assignment_group_id': 555333,
        'submission_types': ['online_text_entry', 'online_upload'], 'allowed_extensions': [],
        'grading_type': 'pass_fail', 'points_possible': 10, 'published': False}}
    r = subprocess.run(['curl', '-sS', '-X', 'POST', BASE + '/assignments', '-H', 'Content-Type: application/json',
                        '-d', json.dumps(body)], capture_output=True, text=True, check=True).stdout
    d = json.loads(r)
    if 'id' not in d: sys.exit(r)
    print(key, d['id'], d['points_possible'], d['grading_type'], d['published'], d['html_url'])
