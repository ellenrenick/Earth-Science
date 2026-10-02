import json, subprocess, sys
BASE = 'https://kernhigh.instructure.com/api/v1/courses/300209'
def call(method, path, body):
    r = subprocess.run(['curl', '-sS', '-X', method, BASE + path, '-H', 'Content-Type: application/json',
                        '-d', json.dumps(body)], capture_output=True, text=True, check=True).stdout
    d = json.loads(r)
    if 'id' not in d: sys.exit(f'{path}: {r}')
    return d
mod = call('POST', '/modules', {'module': {'name': 'Unit 2: Cosmic Clues: How Earth Began (HS-ESS1-6)', 'position': 11}})
items = [
 {'type': 'SubHeader', 'title': 'Practice Test Day'},
 {'type': 'Quiz', 'content_id': 1565265},
 {'type': 'SubHeader', 'title': 'After the practice test: Review (below 80%) or Extension (80% or higher)'},
 {'type': 'Assignment', 'content_id': 13884096},
 {'type': 'Assignment', 'content_id': 13884097},
 {'type': 'SubHeader', 'title': 'CSA Day'},
 {'type': 'Quiz', 'content_id': 1565266},
]
for pos, it in enumerate(items, 1):
    it = dict(it, position=pos, indent=0 if it['type'] == 'SubHeader' else 1)
    d = call('POST', f"/modules/{mod['id']}/items", {'module_item': it})
    print(pos, d['type'], d['title'], d['published'])
print('module', mod['id'], mod['position'], mod['published'])
