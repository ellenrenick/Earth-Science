// Builds one .pptx per Unit 3 lesson from lessons.json. Run: node build_slides.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const L = JSON.parse(fs.readFileSync("lessons.json", "utf8"));
const OUT = "../decks";
fs.mkdirSync(OUT, { recursive: true });

const C = { dark: "1C1917", text: "292524", muted: "78716C", accent: "C2410C", amber: "D97706",
  sand: "FEF3E2", line: "E7E5E4", white: "FFFFFF", crust: "57534E", mantle: "D97706", outer: "EA580C", inner: "FDE68A" };
const HF = "Cambria", BF = "Calibri";
const W = 13.333, H = 7.5, M = 0.6;

function badge(slide, x, y, d) {
  [[1, C.crust], [0.86, C.mantle], [0.5, C.outer], [0.24, C.inner]].forEach(([f, col]) => {
    const s = d * f;
    slide.addShape("ellipse", { x: x + (d - s) / 2, y: y + (d - s) / 2, w: s, h: s, fill: { color: col }, line: { color: col, width: 0 } });
  });
}

function runs(rs, base) {
  return rs.map((r, i) => {
    const o = { ...base };
    if (r.b) o.bold = true;
    if (r.i) o.italic = true;
    if (r.href) { o.hyperlink = { url: r.href }; o.color = C.accent; }
    return { text: r.text, options: o };
  });
}

// Turn blocks into a pptxgenjs paragraph array
function paras(blocks, size) {
  const out = [];
  blocks.forEach((b, bi) => {
    if (b.t === "table") return;
    const rs = runs(b.runs, { fontSize: size, color: C.text, fontFace: BF });
    const first = rs[0].options;
    const box = b.t === "li" && b.runs[0].text.startsWith("☐");
    if (b.t === "li" && !box) first.bullet = b.ordered ? { type: "number", numberStartAt: b.n } : true;
    if (b.t === "li") first.indentLevel = 0;
    first.paraSpaceAfter = Math.round(size * 0.45);
    rs[rs.length - 1].options.breakLine = true;
    out.push(...rs);
  });
  if (out.length) delete out[out.length - 1].options.breakLine;
  return out;
}

const textLen = bs => bs.filter(b => b.t !== "table").map(b => b.runs.map(r => r.text).join("").length + 8);
function linesFor(bs, size, width) {
  const cpl = width / (size * 0.0072);
  return textLen(bs).reduce((n, len) => n + Math.max(1, Math.ceil(len / cpl)), 0);
}
function textHeight(bs, size, width) {
  const n = bs.filter(b => b.t !== "table").length;
  return linesFor(bs, size, width) * size * 1.22 / 72 + n * size * 0.45 / 72 + 0.15;
}

function tableRows(tb, size) {
  return tb.rows.map((row, ri) => row.map(c => ({
    text: c.runs.length ? runs(c.runs, { fontSize: size, fontFace: BF, color: c.h ? C.white : C.text, bold: c.h }) : " ",
    options: { fill: { color: c.h ? C.dark : (ri % 2 ? "FAFAF9" : C.white) }, valign: "middle" },
  })));
}
function tableHeight(tb, size, width) {
  const cols = tb.rows[0].length, cw = width / cols, cpl = cw / (size * 0.0072);
  return tb.rows.reduce((h, row) => {
    const lines = Math.max(...row.map(c => Math.max(1, Math.ceil(c.runs.map(r => r.text).join("").length / cpl))));
    return h + lines * size * 1.2 / 72 + 0.14;
  }, 0);
}

function header(slide, title, lesson) {
  slide.background = { color: C.white };
  badge(slide, M, 0.42, 0.55);
  slide.addText(title, { x: M + 0.75, y: 0.3, w: W - 2 * M - 0.75, h: 0.8, fontFace: HF, fontSize: 32, bold: true, color: C.dark, margin: 0, valign: "middle", isTextBox: true });
  slide.addText([{ text: `Unit 3 · Lesson ${lesson.num} · ${lesson.days}   `, options: { color: C.muted } },
    { text: "Open the lesson webpage", options: { color: C.accent, hyperlink: { url: lesson.student_url } } }],
    { x: M, y: H - 0.5, w: W - 2 * M, h: 0.3, fontFace: BF, fontSize: 11, align: "right", margin: 0, isTextBox: true });
}

function contentSlide(pres, lesson, s) {
  const slide = pres.addSlide();
  header(slide, s.h, lesson);
  const top = 1.35, bottom = H - 0.75, avail = bottom - top;
  const tb = s.blocks.find(b => b.t === "table");
  const text = s.blocks.filter(b => b.t !== "table");
  const twoCol = tb && tb.rows[0].length <= 4 && text.length > 0 && text.length <= 3;
  if (twoCol) {
    const lw = 4.6, rw = W - 2 * M - lw - 0.4;
    let ts = 20; while (ts > 13 && textHeight(text, ts, lw) > avail) ts -= 1;
    slide.addText(paras(text, ts), { x: M, y: top, w: lw, h: avail, valign: "top", margin: 0, isTextBox: true });
    let fs = 16; while (fs > 10 && tableHeight(tb, fs, rw) > avail) fs -= 1;
    slide.addTable(tableRows(tb, fs), { x: M + lw + 0.4, y: top, w: rw, colW: Array(tb.rows[0].length).fill(rw / tb.rows[0].length), border: { type: "solid", pt: 0.75, color: C.line }, margin: 0.06 });
    return slide;
  }
  const w = W - 2 * M;
  let ts = 24, fs = 16;
  const fits = () => (text.length ? textHeight(text, ts, w) : 0) + (tb ? tableHeight(tb, fs, w) + 0.2 : 0) <= avail;
  while (!fits() && (ts > 14 || fs > 10)) { if (ts > 14) ts -= 1; if (!fits() && fs > 10) fs -= 1; }
  let y = top;
  if (text.length) {
    const th = Math.min(avail, textHeight(text, ts, w));
    slide.addText(paras(text, ts), { x: M, y, w, h: th, valign: "top", margin: 0, isTextBox: true });
    y += th + 0.2;
  }
  if (tb) slide.addTable(tableRows(tb, fs), { x: M, y, w, colW: Array(tb.rows[0].length).fill(w / tb.rows[0].length), border: { type: "solid", pt: 0.75, color: C.line }, margin: 0.06 });
  return slide;
}

function promptSlide(pres, lesson, s, label) {
  // Do Now / Exit ticket: one big question in a tinted card with a round label
  const slide = pres.addSlide();
  header(slide, s.h, lesson);
  slide.addShape("roundRect", { x: M, y: 1.5, w: W - 2 * M, h: 4.9, fill: { color: C.sand }, line: { color: C.sand }, rectRadius: 0.15 });
  slide.addShape("ellipse", { x: M + 0.45, y: 1.95, w: 1.3, h: 1.3, fill: { color: C.accent }, line: { color: C.accent } });
  slide.addText(label, { x: M + 0.45, y: 1.95, w: 1.3, h: 1.3, fontFace: HF, fontSize: 40, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
  const tw = W - 2 * M - 2.6;
  let ts = 30; while (ts > 16 && textHeight(s.blocks, ts, tw) > 4.2) ts -= 1;
  slide.addText(paras(s.blocks, ts), { x: M + 2.15, y: 1.95, w: tw, h: 4.2, valign: "top", margin: 0, isTextBox: true });
  return slide;
}

function cfaSlide(pres, lesson, s) {
  const slide = pres.addSlide();
  slide.background = { color: C.dark };
  badge(slide, W - M - 2.6, 2.2, 2.6);
  slide.addText("Show what you know", { x: M, y: 1.2, w: 8.5, h: 0.6, fontFace: BF, fontSize: 16, bold: true, color: C.amber, charSpacing: 3, margin: 0, isTextBox: true });
  slide.addText(s.h.replace("Show what you know: ", ""), { x: M, y: 1.85, w: 8.5, h: 1.2, fontFace: HF, fontSize: 44, bold: true, color: C.white, margin: 0, isTextBox: true });
  slide.addText(s.blocks.flatMap(b => b.runs).map(r => r.text).join(""), { x: M, y: 3.3, w: 8.3, h: 2.2, fontFace: BF, fontSize: 22, color: "E7E5E4", margin: 0, valign: "top", isTextBox: true });
  slide.addText([{ text: "Open the lesson webpage", options: { hyperlink: { url: lesson.student_url }, color: C.amber } }],
    { x: M, y: H - 0.9, w: 6, h: 0.4, fontFace: BF, fontSize: 14, margin: 0, isTextBox: true });
  return slide;
}

const isTargetSlide = s => /^Learning target|^Today's targets/.test(s.h);

function targetsSlide(pres, lesson, ti) {
  {
    const s = pres.addSlide();
    header(s, (ti >= 0 ? `${ti + 1}. ` : "") + (lesson.targets.length > 1 ? "Learning targets" : "Learning target"), lesson);
    const n = lesson.targets.length, gap = 0.25, ch = Math.min(1.4, (H - 2.2 - gap * (n - 1)) / n);
    lesson.targets.forEach((tg, i) => {
      const y = 1.45 + i * (ch + gap);
      s.addShape("roundRect", { x: M, y, w: W - 2 * M, h: ch, fill: { color: C.sand }, line: { color: C.sand }, rectRadius: 0.1 });
      const d = Math.min(0.95, ch - 0.25);
      s.addShape("ellipse", { x: M + 0.25, y: y + (ch - d) / 2, w: d, h: d, fill: { color: C.accent }, line: { color: C.accent } });
      s.addText(tg.code, { x: M + 0.25, y: y + (ch - d) / 2, w: d, h: d, fontFace: HF, fontSize: d > 0.8 ? 22 : 16, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
      s.addText(tg.text, { x: M + 0.25 + d + 0.35, y, w: W - 2 * M - d - 1.0, h: ch, fontFace: BF, fontSize: n > 3 ? 18 : 24, color: C.text, valign: "middle", margin: 0, isTextBox: true });
    });
  }

}

function notesText(lesson) {
  const t = lesson.teacher;
  const flat = bs => bs.map(b => b.t === "table" ? "" : (b.t === "li" ? "- " : "") + b.runs.map(r => r.text).join("")).filter(Boolean).join("\n");
  return { open: `AT A GLANCE: ${t.glance}\n\nMATERIALS: ${flat(t.materials)}\n\nAGENDA (minutes):\n` +
      t.agenda.map(([m, w]) => `${m}: ${w}`).join("\n") + `\n\nTeacher page: ${lesson.teacher_url}`,
    key: `ANSWER KEY:\n${flat(t.key)}\n\nTEACHING NOTES:\n${flat(t.notes)}\n\nSUPPORTS: ${t.supports}` };
}

for (const lesson of L) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = `Unit 3 Lesson ${lesson.num}: ${lesson.title}`;
  const notes = notesText(lesson);

  // Title
  const t = pres.addSlide();
  t.background = { color: C.dark };
  badge(t, W - 5.2, 1.15, 5.2);
  t.addText(`UNIT 3 · LESSON ${lesson.num} · ${lesson.days.toUpperCase()}`, { x: M, y: 1.3, w: 7.2, h: 0.5, fontFace: BF, fontSize: 16, bold: true, color: C.amber, charSpacing: 3, margin: 0, isTextBox: true });
  t.addText(lesson.title, { x: M, y: 1.9, w: 7.2, h: 2.2, fontFace: HF, fontSize: 48, bold: true, color: C.white, margin: 0, valign: "top", isTextBox: true });
  t.addText([{ text: "Driving question: ", options: { bold: true } }, { text: "What is inside Earth, and why does it move?", options: { italic: true } }],
    { x: M, y: 4.4, w: 7.2, h: 0.9, fontFace: BF, fontSize: 18, color: "E7E5E4", margin: 0, valign: "top", isTextBox: true });
  t.addShape("roundRect", { x: M, y: 5.6, w: 3.6, h: 0.65, fill: { color: C.accent }, line: { color: C.accent }, rectRadius: 0.1 });
  t.addText([{ text: "Open the lesson webpage", options: { hyperlink: { url: lesson.student_url }, color: C.white } }],
    { x: M, y: 5.6, w: 3.6, h: 0.65, fontFace: BF, fontSize: 16, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true });
  t.addNotes(notes.open);

  // Notebook setup
  {
    const s = pres.addSlide();
    header(s, "Notebook setup", lesson);
    const lw = W - 2 * M - 3.5;
    let ts = 22; while (ts > 13 && textHeight(lesson.notebook, ts, lw) > 5.3) ts -= 1;
    s.addText(paras(lesson.notebook, ts), { x: M, y: 1.4, w: lw, h: 5.3, valign: "top", margin: 0, isTextBox: true });
    s.addShape("roundRect", { x: W - M - 3.1, y: 1.6, w: 3.1, h: 3.6, fill: { color: C.sand }, line: { color: C.sand }, rectRadius: 0.12 });
    s.addText([{ text: "Your notebook is your answer sheet.", options: { bold: true, breakLine: true, fontSize: 20, color: C.accent } },
      { text: "Title, date, and a table of contents entry on every page. Keep it neat; your teacher will check it.", options: { fontSize: 16, color: C.text } }],
      { x: W - M - 2.85, y: 1.85, w: 2.6, h: 3.1, fontFace: BF, valign: "top", margin: 0, isTextBox: true });
  }

  // Lesson slides (skip the learning-target slide; it has its own slide above)
  lesson.slides.forEach((s0, i) => {
    if (isTargetSlide(s0) && lesson.targets.length) return targetsSlide(pres, lesson, i);
    const s = { ...s0, h: s0.h.startsWith("Show what you know") ? s0.h : `${i + 1}. ${s0.h}` };
    if (s.h.startsWith("Show what you know")) cfaSlide(pres, lesson, s);
    else if (s0.h === "Do Now") promptSlide(pres, lesson, s, "?");
    else if (/Exit|Before you start/.test(s0.h)) promptSlide(pres, lesson, s, "!");
    else contentSlide(pres, lesson, s);
  });
  pres.slides[pres.slides.length - 1].addNotes(notes.key);

  const name = `${OUT}/Unit3-Lesson${String(lesson.num).padStart(2, "0")}-${lesson.title.replace(/[^A-Za-z0-9]+/g, "-").replace(/-+$/, "")}.pptx`;
  pres.writeFile({ fileName: name }).then(f => console.log("wrote", f));
}
