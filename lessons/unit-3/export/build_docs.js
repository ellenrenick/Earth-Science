// Builds a student answer sheet and a teacher lesson plan (.docx) per Unit 3 lesson. Run: node build_docs.js
const fs = require("fs");
const d = require("docx");
const { Document, Packer, Paragraph, TextRun, ExternalHyperlink, Table, TableRow, TableCell, WidthType, ShadingType,
  HeadingLevel, AlignmentType, LevelFormat, BorderStyle } = d;

const L = JSON.parse(fs.readFileSync("lessons.json", "utf8"));
const OUT = "../docs";
fs.mkdirSync(OUT, { recursive: true });
const ACC = "C2410C", DARK = "1C1917", MUTED = "78716C", TW = 9360; // 6.5" text width

const styles = {
  default: { document: { run: { font: "Calibri", size: 22, color: "292524" } } },
  paragraphStyles: [
    { id: "Title", name: "Title", basedOn: "Normal", run: { font: "Cambria", size: 40, bold: true, color: DARK }, paragraph: { spacing: { after: 80 } } },
    { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Cambria", size: 28, bold: true, color: ACC }, paragraph: { spacing: { before: 280, after: 100 }, outlineLevel: 0 } },
    { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Cambria", size: 24, bold: true, color: DARK }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 1 } },
  ],
};
const numbering = { config: [
  { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
  ...Array.from({ length: 60 }, (_, k) => ({ reference: `num${k}`, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] })),
] };

function runsOf(rs, extra = {}) {
  return rs.map(r => {
    const t = new TextRun({ text: r.text, bold: r.b || extra.bold, italics: r.i, color: r.href ? ACC : extra.color, underline: r.href ? {} : undefined, size: extra.size });
    return r.href ? new ExternalHyperlink({ link: r.href, children: [new TextRun({ text: r.text, bold: r.b, color: ACC, underline: {} })] }) : t;
  });
}
const link = (text, url) => new ExternalHyperlink({ link: url, children: [new TextRun({ text, color: ACC, underline: {} })] });

function table(tb, widths) {
  const cols = tb.rows[0].length;
  const cw = widths || Array(cols).fill(Math.floor(TW / cols));
  const tw = cw.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: "D6D3D1" };
  return new Table({
    width: { size: tw, type: WidthType.DXA }, columnWidths: cw,
    rows: tb.rows.map(row => new TableRow({ tableHeader: row[0].h, children: row.map((c, i) => new TableCell({
      width: { size: cw[i], type: WidthType.DXA },
      borders: { top: border, bottom: border, left: border, right: border },
      shading: c.h ? { type: ShadingType.CLEAR, fill: DARK, color: "auto" } : undefined,
      margins: { top: 60, bottom: 60, left: 90, right: 90 },
      children: [new Paragraph({ children: c.runs.length ? runsOf(c.runs, c.h ? { bold: true, color: "FFFFFF" } : {}) : [new TextRun(" ")] })],
    })) })),
  });
}

// Renders blocks; each separate ordered list gets its own numbering reference so it restarts at 1
function render(blocks, ctx) {
  const out = [];
  let prevOrdered = false;
  blocks.forEach(b => {
    if (b.t === "table") { out.push(table(b)); out.push(new Paragraph({ text: "" })); prevOrdered = false; return; }
    if (b.t === "li" && b.ordered) {
      if (!prevOrdered || b.n === 1) ctx.n += 1;
      out.push(new Paragraph({ numbering: { reference: `num${ctx.n}`, level: 0 }, spacing: { after: 60 }, children: runsOf(b.runs) }));
      prevOrdered = true; return;
    }
    prevOrdered = false;
    if (b.t === "li") out.push(new Paragraph(b.runs[0].text.startsWith("☐") ? { spacing: { after: 60 }, indent: { left: 360 }, children: runsOf(b.runs) } : { numbering: { reference: "bul", level: 0 }, spacing: { after: 60 }, children: runsOf(b.runs) }));
    else out.push(new Paragraph({ spacing: { after: 100 }, children: runsOf(b.runs) }));
  });
  return out;
}

const writeLine = () => new Paragraph({ spacing: { before: 240 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "A8A29E", space: 1 } }, children: [new TextRun(" ")] });
const needsLines = s => {
  const txt = s.blocks.filter(b => b.t !== "table").flatMap(b => b.runs).map(r => r.text).join(" ");
  if (s.h.startsWith("Show what you know") || /learning target|^Today's targets/i.test(s.h)) return 0;
  if (/vocabulary/i.test(s.h)) return 0;
  const q = (txt.match(/\?/g) || []).length + (txt.match(/______/g) || []).length;
  if (/Exit|Do Now/.test(s.h)) return 4;
  if (/Reading/.test(s.h)) return 8;
  if (/CER|Claim/.test(s.h + txt)) return 8;
  return q > 0 || /\b(Draw|Write|Explain|Finish|Copy|List|Answer|Describe)\b/.test(txt) ? 5 : 0;
};

function header(title, sub) {
  return [new Paragraph({ style: "Title", children: [new TextRun(title)] }),
    new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: sub, color: MUTED })] })];
}

async function student(lesson, fname) {
  const ctx = { n: 0 };
  const kids = [
    ...header(`Lesson ${lesson.num}: ${lesson.title}`, `Unit 3: Forces Beneath Our Feet · ${lesson.days} · Student notebook guide and answer sheet`),
    new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Name: ________________________   Period: ____   Date: __________" })] }),
    new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: "Lesson webpage: ", bold: true }), link("open the lesson on Canvas", lesson.student_url)] }),
  ];
  if (lesson.targets.length) {
    kids.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(lesson.targets.length > 1 ? "Learning targets" : "Learning target")] }));
    lesson.targets.forEach(t => kids.push(new Paragraph({ numbering: { reference: "bul", level: 0 }, children: [new TextRun({ text: t.code + " ", bold: true }), new TextRun(t.text)] })));
  }
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Notebook setup")] }));
  kids.push(...render(lesson.notebook, ctx));
  kids.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "No notebook today? Use this sheet as your answer sheet and staple it into your notebook later.", italics: true, color: MUTED })] }));
  lesson.slides.forEach((s, i) => {
    if (/^Learning target|^Today's targets/.test(s.h)) return;
    kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(`Slide ${i + 1}: ${s.h}`)] }));
    kids.push(...render(s.blocks, ctx));
    for (let k = 0; k < needsLines(s); k++) kids.push(writeLine());
  });
  const doc = new Document({ styles, numbering, sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } }, children: kids }] });
  fs.writeFileSync(`${OUT}/${fname}-STUDENT.docx`, await Packer.toBuffer(doc));
}

async function teacher(lesson, fname, deck) {
  const ctx = { n: 0 }, t = lesson.teacher;
  const kids = [
    ...header(`TEACHER: Lesson ${lesson.num}: ${lesson.title}`, `Unit 3: Forces Beneath Our Feet (HS-ESS2-3) · ${lesson.days}`),
    new Paragraph({ children: [new TextRun({ text: "Teacher page (Canvas): ", bold: true }), link("open", lesson.teacher_url)] }),
    new Paragraph({ children: [new TextRun({ text: "Student page (Canvas): ", bold: true }), link("open", lesson.student_url)] }),
    new Paragraph({ children: [new TextRun({ text: "Slides: ", bold: true }), new TextRun(deck)] }),
    new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Targets: ", bold: true }), new TextRun(lesson.targets.map(x => x.code).join(", ") || "none (launch)"),
      ...(lesson.cfa ? [new TextRun({ text: "   CFA: ", bold: true }), new TextRun(`Unit 3 CFA ${lesson.cfa} (Mastery Path opens Review ${lesson.cfa} under 67.5%)`)] : [])] }),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("At a glance")] }),
    new Paragraph({ children: [new TextRun(t.glance)] }),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Materials and prep")] }),
    ...render(t.materials, ctx),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Agenda")] }),
    table({ rows: [[{ h: true, runs: [{ text: "Minutes" }] }, { h: true, runs: [{ text: "What happens" }] }],
      ...t.agenda.map(([m, w]) => [{ runs: [{ text: m }] }, { runs: [{ text: w }] }])] }, [1500, TW - 1500]),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Teaching notes")] }),
    ...render(t.notes, ctx),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Answer key")] }),
    ...render(t.key, ctx),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Supports")] }),
    new Paragraph({ children: [new TextRun(t.supports)] }),
  ];
  const doc = new Document({ styles, numbering, sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } }, children: kids }] });
  fs.writeFileSync(`${OUT}/${fname}-TEACHER.docx`, await Packer.toBuffer(doc));
}

(async () => {
  for (const lesson of L) {
    const fname = `Unit3-Lesson${String(lesson.num).padStart(2, "0")}-${lesson.title.replace(/[^A-Za-z0-9]+/g, "-").replace(/-+$/, "")}`;
    await student(lesson, fname);
    await teacher(lesson, fname, fname + ".pptx");
    console.log("wrote", fname);
  }
})();
