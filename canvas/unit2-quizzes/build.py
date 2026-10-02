import re, json, html, sys

def inline(s):
    s = s.replace('\\~', '~').replace('\\_', '_')
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    return s

def table(lines):
    rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines]
    head, body = rows[0], rows[2:]
    h = '<table style="border-collapse:collapse;margin:8px 0" border="1" cellpadding="6"><thead><tr>'
    h += ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>'
    for r in body:
        h += '<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
    return h + '</tbody></table>'

def blocks(text):
    """Split markdown into blocks: ('p', text) | ('table', html) | ('li', text) | ('h', text)"""
    out, lines, i = [], text.split('\n'), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith('|'):
            t = []
            while i < len(lines) and lines[i].startswith('|'):
                t.append(lines[i]); i += 1
            out.append(('table', table(t))); continue
        if l.startswith('## '): out.append(('h', l[3:]))
        elif l.startswith('- '): out.append(('li', l[2:]))
        elif l.strip() and l.strip() != '---' and not l.startswith('# '): out.append(('p', l))
        i += 1
    return out

def parse(md, key):
    bl = blocks(md)
    intro, qs, cur, shared, pending_shared = [], [], None, None, None
    for kind, val in bl:
        m = re.match(r'\*\*(\d+)\.(.*?)\*\*\s*(.*)', val) if kind == 'p' else None
        if m:
            n = int(m.group(1))
            cur = {'n': n, 'stem': [], 'choices': [], 'target': target}
            label = m.group(2).strip()
            if label: cur['label'] = label
            if m.group(3): cur['stem'].append('<p>' + inline(m.group(3)) + '</p>')
            if shared and n in shared[0]:
                cur['stem'].insert(0, shared[1])
            qs.append(cur); continue
        if kind == 'h':
            mt = re.search(r'Target (\d\.\d)', val); target = mt.group(1) if mt else None
            cur = None; continue
        if kind == 'p' and val.startswith('Use this table for questions'):
            cur = None
        if cur is None:
            if kind == 'p' and val.startswith('Use this table for questions'):
                nums = [int(x) for x in re.findall(r'\d+', val)]
                pending_shared = (nums, '<p>' + inline(val) + '</p>'); continue
            if kind == 'table' and pending_shared:
                shared = (pending_shared[0], pending_shared[1] + val); pending_shared = None; continue
            intro.append((kind, val)); continue
        if kind == 'li' and re.match(r'[A-D]\. ', val) and not cur.get('label'):
            cur['choices'].append(inline(val[3:]))
        elif kind == 'li':
            cur['stem'].append('<li>' + inline(val) + '</li>')
        elif kind == 'table':
            cur['stem'].append(val)
        elif kind == 'p' and (val.startswith('**Before') or val.startswith('**Self-check')):
            cur = None; intro.append(('end', val))
        else:
            cur['stem'].append('<p>' + inline(val) + '</p>')
        # the "Use this table" line can appear right after a question's choices
    return intro, qs

def wrap_li(parts):
    out, inlist = [], False
    for p in parts:
        if p.startswith('<li>') and not inlist: out.append('<ul>'); inlist = True
        if not p.startswith('<li>') and inlist: out.append('</ul>'); inlist = False
        out.append(p)
    if inlist: out.append('</ul>')
    return ''.join(out)

def to_canvas(qs, key):
    out = []
    for q in qs:
        n, t = q['n'], q['target']
        tag = f'<p style="color:#666;font-size:0.85em">Question {n} · Target {t}</p>'
        if q['choices']:
            letter = key[n]
            out.append({'question_name': f'Q{n} (Target {t})', 'question_type': 'multiple_choice_question',
                'question_text': tag + wrap_li(q['stem']), 'points_possible': 1,
                'answers': [{'answer_html': c, 'answer_weight': 100 if 'ABCD'[i] == letter else 0}
                            for i, c in enumerate(q['choices'])]})
        elif n == 14:
            # split a/b into two essay questions, each carrying the shared intro + data table
            stem = q['stem']
            ia = next(i for i, s in enumerate(stem) if s.startswith('<p>a. '))
            ib = next(i for i, s in enumerate(stem) if s.startswith('<p>b. '))
            common = stem[:ia]
            for part, seg in (('a', stem[ia:ib]), ('b', stem[ib:])):
                out.append({'question_name': f'Q14{part} (Target {t})', 'question_type': 'essay_question',
                    'question_text': f'<p style="color:#666;font-size:0.85em">Question 14{part} · Target {t} · 2 points</p>'
                        + wrap_li(common + seg), 'points_possible': 2})
        else:
            out.append({'question_name': f'Q{n} CER (Target {t})', 'question_type': 'essay_question',
                'question_text': tag + wrap_li(q['stem']), 'points_possible': 4})
    return out

KEYS = {
 'csa': dict(zip([1,2,3,4,5,6,7,8,9,10,11,12,13,15], 'BCACDCDCDADCBA')),
 'pt':  dict(zip([1,2,3,4,5,6,7,8,9,10,11,12,13,15], 'CBADCADCBCDABC')),
}
if __name__ == '__main__':
    res = {}
    for name in ('csa', 'pt'):
        md = open(f'{name}.md').read()
        intro, qs = parse(md, KEYS[name])
        assert [q['n'] for q in qs] == list(range(1, 17)), [q['n'] for q in qs]
        for q in qs:
            if q['n'] not in (14, 16): assert len(q['choices']) == 4, q
        res[name] = {'intro': intro, 'questions': to_canvas(qs, KEYS[name])}
    json.dump(res, open('quizzes.json', 'w'), indent=1)
    for name in res:
        print(name, len(res[name]['questions']), sum(q['points_possible'] for q in res[name]['questions']))
        print(res[name]['intro'])
