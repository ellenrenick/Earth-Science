import json, re, subprocess, sys
BASE = 'https://kernhigh.instructure.com/api/v1/courses/300209'
def call(method, path, body=None):
    cmd = ['curl', '-sS', '-X', method, BASE + path, '-H', 'Content-Type: application/json']
    if body is not None: cmd += ['-d', json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    d = json.loads(r)
    if isinstance(d, dict) and d.get('errors'): sys.exit(f'{path}: {d}')
    return d

data = json.load(open('quizzes.json'))
WB = '<p><strong>Word bank:</strong> radiometric dating · half-life · meteorite · composition · impact crater · surface processes</p>'
DESC = {
 'csa': ('Unit 2 CSA: Cosmic Clues – How Earth Began',
   '<p><strong>HS-ESS1-6 · 16 questions · 22 points</strong></p>'
   '<p><strong>Directions:</strong> Read every question twice. For multiple choice, choose the best answer. '
   'Questions 14a, 14b and 16 are written answers: use complete sentences. Question 16 is a CER (claim, evidence, reasoning). '
   'You may sketch or do math on scratch paper.</p>' + WB +
   '<p><strong>Before you submit:</strong> Did you answer every question? In #16, make sure your claim is clear and you used at least 4 word bank words.</p>',
   False),
 'pt': ('Unit 2 Practice Test: Cosmic Clues – How Earth Began',
   '<p><strong>HS-ESS1-6 · 16 questions · 22 points · Set up just like the CSA</strong></p>'
   '<p><strong>Directions:</strong> Read every question twice. For multiple choice, choose the best answer. '
   'Questions 14a, 14b and 16 are written answers: use complete sentences. Question 16 is a CER. '
   'After this is graded, you will get a <strong>review</strong> assignment (below 80%) or an <strong>extension</strong> assignment (80% or higher).</p>' + WB +
   '<p><strong>Self-check after you finish:</strong> Which target felt hardest? 2.1 · 2.2 · 2.3 · 2.4 · 2.5 · 2.6</p>',
   True),
}
out = {}
for name in ('pt', 'csa'):
    title, desc, show = DESC[name]
    quiz = call('POST', '/quizzes', {'quiz': {
        'title': title, 'description': desc, 'quiz_type': 'assignment',
        'assignment_group_id': 555333, 'shuffle_answers': False,
        'show_correct_answers': show, 'allowed_attempts': 1,
        'one_question_at_a_time': False, 'published': False}})
    qid = quiz['id']
    for i, q in enumerate(data[name]['questions'], 1):
        q = dict(q, position=i)
        q['question_text'] = re.sub(r'<p>Use this table for questions [^<]*</p>', '<p>Use this table to answer the question.</p>', q['question_text'])
        if q['question_name'].startswith('Q16'): q['question_text'] += WB
        call('POST', f'/quizzes/{qid}/questions', {'question': q})
    q = call('GET', f'/quizzes/{qid}')
    print(name, qid, q['question_count'], q['points_possible'], q['html_url'])
    out[name] = qid
json.dump(out, open('created.json', 'w'))
