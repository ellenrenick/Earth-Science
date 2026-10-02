import json, subprocess, sys
BASE = 'https://kernhigh.instructure.com/api/v1/courses/300209'
def call(method, path, body):
    r = subprocess.run(['curl', '-sS', '-X', method, BASE + path, '-H', 'Content-Type: application/json',
                        '-d', json.dumps(body)], capture_output=True, text=True, check=True).stdout
    d = json.loads(r)
    if not isinstance(d, dict) or ('id' not in d and 'outcome' not in d): sys.exit(f'{path}: {r}')
    return d
# Same layout and rating scale as the Unit 3 (HS-ESS2-3) group
grp = call('POST', '/outcome_groups/116859/subgroups', {
    'title': 'HS-ESS1-6 · Unit 2: Cosmic Clues: How Earth Began',
    'description': '<p><strong>HS-ESS1-6 (priority standard):</strong> Apply scientific reasoning and evidence from ancient '
                   'Earth materials, meteorites, and other planetary surfaces to construct an account of Earth\'s formation and early history.</p>'})
LTS = [
 ('2.1', 'Earth formed by accretion', 'I can describe how Earth formed by accretion from the solar nebula.'),
 ('2.2', 'Radiometric dating', 'I can explain how radiometric dating uses half-life to find the age of a rock.'),
 ('2.3', "Why Earth's oldest rocks are gone", "I can explain why most of Earth's oldest rocks are gone (plate tectonics and erosion), while moon rocks and meteorites are not."),
 ('2.4', "Evidence for Earth's age", "I can use the ages of meteorites, moon rocks, and Earth's oldest minerals as evidence that Earth is about 4.6 billion years old."),
 ('2.5', 'Craters as evidence', "I can use craters on the moon and other planets as evidence of Earth's early impact history."),
 ('2.6', "CER on Earth's early history", "I can write a CER explaining Earth's formation and early history using more than one line of evidence."),
]
RATINGS = [{'description': d, 'points': p} for d, p in
           (('Mastered', 4), ('Proficient', 3), ('Approaching', 2), ('Not yet meeting', 1), ('Insufficient evidence', 0))]
for n, short, text in LTS:
    d = call('POST', f"/outcome_groups/{grp['id']}/outcomes", {
        'title': f'ESS1-6 LT {n}: {short}', 'display_name': f'LT {n} {short}',
        'description': f'<p>{text}</p>', 'ratings': RATINGS, 'mastery_points': 3, 'calculation_method': 'highest'})
    o = d['outcome']; print(o['id'], o['title'])
print('group', grp['id'], grp['title'])
