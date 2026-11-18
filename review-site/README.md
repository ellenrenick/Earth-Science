# Personalized CFA review site

Students type their name and get a review plan built from their own CFA scores.
Covers every published "Unit N CFA ..." assignment in the live course (342899);
review content is reused from the matching "Unit N Review ... (Mastery Path)"
assignment, so editing a review page in Canvas and rebuilding updates the site.

## Rebuild (re-run after each CFA is graded)

    python3 review-site/build.py        # writes review-site/dist/index.html

- Status per target: **Not taken** / **Needs review** (< 2.7) / **Proficient** (2.7-3.4) / **Mastered** (3.5+).
- A CFA no one has submitted yet (currently Unit 4 ESS1-5.5 and 5.6) is left out automatically and appears once scores exist.
- Names are stored only as salted SHA-256 hashes (new salt each build). "First Last", "Last, First" and "First Middle Last" all match.

## Privacy: read before sharing

`dist/index.html` contains every student's scores (keyed by hashed name). It is gitignored; do not commit it
or put it on a public host (e.g. public GitHub Pages). A name is not a password, so a student who knows a
classmate's name can look that classmate up. Host it only behind your school login (Canvas file / Google
Drive restricted to the domain), or ask for an added check such as a student-ID last four.
