# Personalized CFA review site

Students enter their student ID and get a review plan built from their own CFA scores.
Covers the published "Unit N CFA ..." assignments for Unit 4 only (change with `--units 3,4`) in the live course (342899);
review content is reused from the matching "Unit N Review ... (Mastery Path)"
assignment, so editing a review page in Canvas and rebuilding updates the site.

## Rebuild (re-run after each CFA is graded)

    python3 review-site/build.py        # writes review-site/dist/index.html

- Status per target: **Not taken** / **Needs review** (< 2.67) / **Proficient** (2.67-3.4) / **Mastered** (3.5+).
- A CFA no one has submitted yet (e.g. a Unit 4 CFA not yet taken by anyone) is left out automatically and appears once scores exist.
- Each student's scores are AES-GCM encrypted with a key derived (PBKDF2, 600k rounds) from their own student ID (the Canvas SIS ID, the 6-digit number in the school email). The file has no names or IDs, and a student cannot read a classmate's row without that classmate's ID. Dashes/spaces in the typed ID are ignored.

## Privacy: read before sharing

`dist/index.html` contains every student's scores (keyed by hashed student ID). It is gitignored; do not commit it
or put it on a public host (e.g. public GitHub Pages). A student who knows a classmate's ID can still look that classmate up. Host it only behind your school login (Canvas file / Google
Drive restricted to the domain).

## Interactive pieces

- `practice.json`: multiple-choice practice per target, with a specific explanation for every wrong choice and a memory trick. Edit this file to change questions, then rebuild.
- `engine.js`: the animations (continent fit, seafloor ages, spreading, plate boundaries, subduction, claim/evidence/reasoning sorter) and the practice flow (a wrong answer shows an explanation plus the animation replaying; two misses reveal the answer and the question comes back once).
- Progress and written answers are saved only in the student's browser (not sent to anyone).

## Live course

The built file is uploaded to the live course (342899) as `Unit4_Personalized_Review.html` and linked from the Unit 4 module under "Today's Work!". To refresh: rebuild, then upload over the same file name (on_duplicate=overwrite keeps the link working).
