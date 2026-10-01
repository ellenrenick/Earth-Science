"""Converts content.py (HTML snippets) into structured JSON blocks for the slide and doc builders."""
import json, sys, html
from html.parser import HTMLParser
sys.path.insert(0, "..")
from content import LESSONS, LT

PAGES = json.load(open("../canvas_ids.json"))["pages"]
BASE = "https://kernhigh.instructure.com/courses/300209/pages/"


class Blocks(HTMLParser):
    """Blocks: {"t":"p","runs":[...]}, {"t":"li","ordered":bool,"n":int,"runs":[...]}, {"t":"table","rows":[[{"h":bool,"runs":[...]}]]}"""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.runs, self.fmt, self.lists, self.table, self.cell = [], None, [], [], None, None
        self.href = None
        self.in_li = False

    def _start(self):
        self.runs = []

    def _end(self, block):
        if self.runs is not None and any(r["text"].strip() for r in self.runs):
            block["runs"] = self._clean(self.runs)
            self.out.append(block)
        self.runs = None

    @staticmethod
    def _clean(runs):
        merged = []
        for r in runs:
            r["text"] = " ".join(r["text"].split()) if r["text"].strip() else " "
            if merged and {k: v for k, v in merged[-1].items() if k != "text"} == {k: v for k, v in r.items() if k != "text"}:
                merged[-1]["text"] += r["text"] if r["text"].startswith((" ", ".", ",", ":", ";", ")")) or merged[-1]["text"].endswith(" ") else " " + r["text"]
            else:
                merged.append(r)
        # fix spacing between runs
        for i in range(1, len(merged)):
            a, b = merged[i - 1]["text"], merged[i]["text"]
            if not a.endswith(" ") and not b.startswith((" ", ".", ",", ":", ";", ")", "?", "!")) and not a.endswith(("(", "\"")):
                merged[i]["text"] = " " + b
        merged[0]["text"] = merged[0]["text"].lstrip()
        merged[-1]["text"] = merged[-1]["text"].rstrip()
        return [m for m in merged if m["text"]]

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in ("strong", "b"): self.fmt.append("b")
        elif tag in ("em", "i"): self.fmt.append("i")
        elif tag == "a": self.href = a.get("href")
        elif tag == "br" and self.runs is not None and self.cell is None and not self.in_li:
            self._end({"t": "p"}); self._start()
        elif tag in ("ul", "ol"): self.lists.append([tag == "ol", 0])
        elif tag == "li":
            self.lists[-1][1] += 1; self._start(); self.in_li = True
        elif tag == "p" and self.cell is None: self._start()
        elif tag == "table": self.table = []
        elif tag == "tr": self.table.append([])
        elif tag in ("td", "th"): self.cell = {"h": tag == "th"}; self._start()

    def handle_endtag(self, tag):
        if tag in ("strong", "b", "em", "i") and self.fmt: self.fmt.pop()
        elif tag == "a": self.href = None
        elif tag in ("ul", "ol"): self.lists.pop()
        elif tag == "li":
            self.in_li = False
            self._end({"t": "li", "ordered": self.lists[-1][0], "n": self.lists[-1][1]})
        elif tag == "p" and self.cell is None: self._end({"t": "p"})
        elif tag in ("td", "th"):
            runs = self._clean(self.runs) if self.runs and any(r["text"].strip() for r in self.runs) else []
            self.cell["runs"] = runs; self.table[-1].append(self.cell); self.cell, self.runs = None, None
        elif tag == "table": self.out.append({"t": "table", "rows": self.table}); self.table = None

    def handle_data(self, d):
        if self.runs is None:
            if d.strip(): self._start()
            else: return
        r = {"text": d}
        if "b" in self.fmt: r["b"] = True
        if "i" in self.fmt: r["i"] = True
        if self.href: r["href"] = self.href if self.href.startswith("http") else "https://kernhigh.instructure.com" + self.href
        self.runs.append(r)

    def close(self):
        super().close()
        if self.runs: self._end({"t": "p"})
        return self.out


def blocks(h):
    p = Blocks(); p.feed(h); return p.close()


out = []
for L, pg in zip(LESSONS, PAGES):
    t = L["teacher"]
    out.append({
        "num": L["num"], "days": L["days"], "title": L["title"],
        "targets": [{"code": k, "text": LT[k]} for k in L["targets"]],
        "cfa": L.get("cfa"),
        "student_url": BASE + pg["student"], "teacher_url": BASE + pg["teacher"],
        "notebook": blocks(L["notebook"]),
        "slides": [{"h": h, "blocks": blocks(b)} for h, b in L["slides"]],
        "teacher": {"glance": t["glance"], "materials": blocks("<p>" + t["materials"] + "</p>"),
                    "agenda": [[m, html.unescape(w)] for m, w in t["agenda"]],
                    "notes": blocks(t["notes"]), "key": blocks(t["key"]), "supports": t["supports"]},
    })
json.dump(out, open("lessons.json", "w"), indent=1, ensure_ascii=False)
print("lessons", len(out), "slides", sum(len(l["slides"]) for l in out))
