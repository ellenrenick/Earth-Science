# Unit 2 (HS-ESS1-6) quizzes and assignments in Canvas

Source: the "Unit 2 CSA" and "Unit 2 Practice Test" Claude docs, exported as `csa.md` and `pt.md`.
Answer keys come from the "Unit 2 Cosmic Clues Assessments – TEACHER KEYS" doc (`KEYS` in `build.py`).

- `python3 build.py` parses both files into `quizzes.json` (Canvas Classic Quiz questions).
- `python3 upload.py` creates both quizzes, unpublished, in the sandbox (300209). It does not touch the live course.

Created in the sandbox on 2026-10-02:

| Quiz | Canvas quiz ID |
| --- | --- |
| Unit 2 Practice Test: Cosmic Clues – How Earth Began | 1565265 |
| Unit 2 CSA: Cosmic Clues – How Earth Began | 1565266 |

Multiple choice is auto-graded (1 point each). Q14 is split into 14a and 14b (2 points each), and Q16 is the CER (4 points). These are essay questions that you grade by hand with the rubrics in the teacher keys doc.

## Review and enrichment assignments

`python3 assignments.py` posts `review.md` and `enrichment.md` as unpublished assignments in the sandbox. They are graded complete/incomplete (10 points), and students can submit by text entry or file upload.

| Assignment | Canvas assignment ID |
| --- | --- |
| Unit 2 Review & Intervention: Cosmic Clues – How Earth Began | 13884096 |
| Unit 2 Enrichment & Extension: Cosmic Clues – Going Deeper | 13884097 |
