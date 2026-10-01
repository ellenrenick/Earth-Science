"""Unit 3 lesson content: student pages (projectable "slides" + notebook setup) and teacher pages.

Pacing follows the Scope & Sequence doc, Unit 3, Days 37-50.
"""

REPO = "https://github.com/ellenrenick/Earth-Science/blob/claude/vibrant-cerf-kl0bt9/lessons/unit-3/files"
T = 'border="1" cellpadding="6" style="border-collapse:collapse"'

LT = {
    "3.1": "I can describe how P-waves and S-waves travel differently through solids and liquids.",
    "3.2": "I can use seismic wave data, including the shadow zone, to identify Earth's layers and which one is liquid.",
    "3.3": "I can describe Earth's layers by composition, density, temperature, and state (solid or liquid).",
    "3.4": "I can identify the two sources of Earth's internal heat: heat left from formation and radioactive decay.",
    "3.5": "I can model how mantle convection moves heat and cycles rock between Earth's interior and surface.",
}

# Each lesson: num, days, title, targets, student slides [(heading, html)], notebook html, teacher dict.
LESSONS = [
    {
        "num": 1, "days": "Day 37", "title": "The Shadow Zone Mystery", "targets": [],
        "notebook": """<p><strong>Set up your Unit 3 section.</strong></p>
<ol>
<li><strong>Cover page:</strong> "Unit 3: Forces Beneath Our Feet." Write the driving question: <em>What is inside Earth, and why does it move?</em> Draw a picture of what you <em>think</em> is inside Earth (it's OK to be wrong).</li>
<li><strong>Learning targets page:</strong> copy targets 3.1-3.5 from Slide 2. Leave a box next to each one to rate yourself 1-4 later.</li>
<li><strong>Table of contents:</strong> add "Unit 3 cover," "Unit 3 targets," and "L1 Shadow Zone Mystery."</li>
<li><strong>L1 page:</strong> title "The Shadow Zone Mystery." Make a two-column chart: <em>I notice</em> | <em>I wonder</em>. Below it, the vocabulary chart from Slide 5.</li>
</ol>""",
        "slides": [
            ("Do Now", """<p>Think of a watermelon. How could you figure out what's inside it <strong>without cutting it open</strong>? List 2 ideas in your notebook.</p>"""),
            ("Unit 3 learning targets", "<ul>" + "".join(f"<li><strong>{k}</strong> {v}</li>" for k, v in LT.items()) + "</ul>"),
            ("The phenomenon", """<p>The deepest hole humans have ever drilled is about <strong>12 km</strong> deep. Earth is about <strong>6,371 km</strong> to the center. We have never seen Earth's inside.</p>
<p>But in 1914, a scientist named Beno Gutenberg noticed something strange. When a big earthquake happens, seismographs all over the world record the shaking. But <strong>some stations on the far side of Earth record nothing at all</strong>. This "quiet" ring around the planet is called the <strong>shadow zone</strong>.</p>
<p><strong>Your teacher will show a picture of the shadow zone.</strong> Fill in your <em>I notice / I wonder</em> chart.</p>"""),
            ("Driving question", """<p style="font-size:1.3em"><strong>What is inside Earth, and why does it move?</strong></p>
<p>Turn and talk: Why might earthquake waves NOT reach some places? Write your best guess under your chart. We will come back to it at the end of the unit.</p>"""),
            ("Unit 3 vocabulary", f"""<p>Copy this chart. Draw a small picture for each word.</p>
<table {T}>
<tr><th>Word</th><th>What it means</th><th>Picture</th></tr>
<tr><td>crust</td><td>Thin, solid, rocky outer layer we live on</td><td></td></tr>
<tr><td>mantle</td><td>Thick layer of hot solid rock that flows very slowly</td><td></td></tr>
<tr><td>outer core</td><td>Layer of liquid iron and nickel</td><td></td></tr>
<tr><td>inner core</td><td>Solid ball of iron and nickel at the center</td><td></td></tr>
<tr><td>seismic wave</td><td>Wave of energy that travels through Earth after an earthquake</td><td></td></tr>
<tr><td>P-wave</td><td>Fastest seismic wave; push-pull motion; goes through solids and liquids</td><td></td></tr>
<tr><td>S-wave</td><td>Slower seismic wave; side-to-side motion; goes through solids only</td><td></td></tr>
<tr><td>density</td><td>How much matter is packed into a space (how "heavy for its size")</td><td></td></tr>
<tr><td>convection</td><td>Hot material rises, cool material sinks, making a loop</td><td></td></tr>
<tr><td>radioactive decay</td><td>Unstable elements breaking down and giving off heat</td><td></td></tr>
</table>"""),
            ("Exit ticket", """<p>In your notebook: <em>One thing I think is inside Earth is ______ because ______.</em></p>"""),
        ],
        "teacher": {
            "glance": "Launch day. Hook with the shadow zone, set up the Unit 3 notebook section, pre-teach the 10 vocabulary words with pictures (per the course support plan). No CFA today.",
            "materials": "Projector; a shadow zone diagram (textbook Module 15, Lesson 2 figure of seismic wave paths, or any labeled shadow zone image); optional: a watermelon or a wrapped box to shake for the Do Now.",
            "agenda": [("5", "Do Now: watermelon question. Take 3-4 ideas (thump it, weigh it, X-ray, shake it). Connect: scientists 'thump' Earth with earthquakes."),
                       ("8", "Notebook setup: cover page with driving question + initial model drawing, targets page, table of contents."),
                       ("10", "Phenomenon: 12 km deepest hole vs 6,371 km radius. Show the shadow zone image with no labels first. Notice/Wonder chart; share out."),
                       ("5", "Driving question turn-and-talk. Record class ideas on chart paper to revisit on Day 49."),
                       ("17", "Vocabulary chart with pictures. Model 2-3 pictures; students finish in pairs. Quick gesture for P-wave (push-pull) and S-wave (side-to-side)."),
                       ("5", "Exit ticket.")],
            "notes": """<ul>
<li>The deepest hole is the Kola Superdeep Borehole (about 12 km). Gutenberg (1914) located the core boundary at about 2,900 km depth; Inge Lehmann (1936) found the solid inner core.</li>
<li>Don't explain the shadow zone today. Students should leave with the question, not the answer. Lessons 2-3 resolve it.</li>
<li>Expected wonders to collect: Why don't the waves reach? Is something blocking them? Is part of Earth hollow or liquid?</li>
</ul>""",
            "key": "<p>No key. Look for exit tickets that name a layer or a material; note students who draw Earth as hollow or all lava, since these misconceptions come up again in Lessons 3-4.</p>",
            "supports": "Sentence frames are on the slides. Pair students for the vocabulary pictures. Let students who are new to English label pictures in their home language too.",
        },
    },
    {
        "num": 2, "days": "Days 38-39", "title": "Seismic Waves: P-waves vs S-waves", "targets": ["3.1"], "cfa": "3.1",
        "notebook": f"""<p><strong>Title:</strong> L2 Seismic Waves. Add it to your table of contents.</p>
<ol>
<li>Draw a long Slinky twice. On the first, show a <strong>P-wave</strong> (bunched-up and spread-out coils). On the second, show an <strong>S-wave</strong> (wavy, side to side). Add arrows for the direction the wave travels and the direction the coils move.</li>
<li>Copy and fill in the comparison chart from Slide 4.</li>
<li>Day 39: write answers to the reading questions (Slide 5) under the chart.</li>
</ol>""",
        "slides": [
            ("Do Now", "<p>When an earthquake happens, does everyone feel it at the same time? Why or why not?</p>"),
            ("Learning target 3.1", f"<p>{LT['3.1']}</p>"),
            ("Slinky demo", """<p>Watch the demo, then try it with a partner.</p>
<ol>
<li><strong>P-wave:</strong> Stretch the Slinky on the floor. Push one end forward quickly. The coils <em>squeeze and stretch</em> in the same direction the wave moves.</li>
<li><strong>S-wave:</strong> Shake one end <em>side to side</em>. The coils move across the direction the wave moves.</li>
<li><strong>Race:</strong> Which wave reached the other end first?</li>
</ol>"""),
            ("Compare the two waves", f"""<table {T}>
<tr><th></th><th>P-wave (primary)</th><th>S-wave (secondary)</th></tr>
<tr><td>Motion</td><td>______</td><td>______</td></tr>
<tr><td>Speed</td><td>______ (arrives first)</td><td>______ (arrives second)</td></tr>
<tr><td>Travels through solids?</td><td>______</td><td>______</td></tr>
<tr><td>Travels through liquids?</td><td>______</td><td>______</td></tr>
</table>
<p><strong>Memory tricks:</strong> P = Primary = first. S-waves Stop at liquids.</p>
<p><strong>Why do S-waves stop?</strong> Side-to-side shaking only works in stiff material that springs back. A liquid just flows out of the way.</p>"""),
            ("Day 39: Reading", """<p>Read <strong>Module 15, Lesson 2: Seismic Waves and Earth's Interior (pp. 399-403)</strong>. Answer in your notebook:</p>
<ol>
<li>What is a seismograph?</li>
<li>Which wave arrives first at a seismograph, and why?</li>
<li>What happens to an S-wave when it reaches liquid?</li>
<li>Why do seismic waves change speed and direction inside Earth?</li>
</ol>"""),
            ("Show what you know: CFA 3.1", "<p>Take <strong>Unit 3 CFA 3.1: P-waves vs S-waves</strong> (5 questions). If you score below a B, a review page for this target will open for you.</p>"),
        ],
        "teacher": {
            "glance": "Two days. Day 38: Slinky demo and comparison chart. Day 39: textbook reading + questions, then CFA 3.1 (Mastery Path opens Review 3.1 for scores under 67.5%).",
            "materials": "Metal or plastic Slinkys (1 per pair, or a few for demo stations); open floor or long tables; textbooks (Module 15, Lesson 2, pp. 399-403); Chromebooks for CFA 3.1.",
            "agenda": [("Day 38: 5", "Do Now. Answer: no, people closer feel it first, because waves take time to travel."),
                       ("10", "Teacher Slinky demo: P-wave push, S-wave shake. Students describe motion in their own words."),
                       ("15", "Pairs try both waves. Race: P-wave arrives first."),
                       ("15", "Comparison chart and notebook drawings. Introduce 'S-waves Stop at liquids' with the 'liquid can't spring back' explanation."),
                       ("5", "Exit: show P or S with your hand (push vs side-to-side) as you call out descriptions."),
                       ("Day 39: 5", "Review the chart with hand gestures."),
                       ("25", "Reading pp. 399-403 with questions; read aloud the first section together."),
                       ("15", "CFA 3.1 on Canvas."),
                       ("5", "Students who finish early: start the Earthquakes 1 - Recording Station Gizmo (optional).")],
            "notes": """<ul>
<li>P-waves are compressional (longitudinal); S-waves are shear (transverse). In the crust, P-waves travel about 6 km/s, S-waves about 3.5 km/s.</li>
<li>P-waves slow down and bend when they enter the liquid outer core; they do not stop. Watch for students who think P-waves stop in liquid.</li>
<li>In a Slinky, you can't truly show the liquid case. Use the 'liquid can't spring back' explanation, or a tray of water: pushing it makes ripples spread, but side-to-side 'shear' just slides the water.</li>
</ul>""",
            "key": f"""<p><strong>Chart:</strong> P = push-pull / squeeze-stretch, faster, solids yes, liquids yes. S = side to side, slower, solids yes, liquids <strong>no</strong>.</p>
<p><strong>Reading:</strong> (1) An instrument that records ground shaking from seismic waves. (2) The P-wave, because it is the fastest. (3) It stops; S-waves cannot travel through liquid. (4) The layers have different materials, densities, and states (solid or liquid), which changes how fast waves travel and bends their paths.</p>
<p><strong>CFA 3.1 key:</strong> A, B, C, D, False.</p>""",
            "supports": "Gestures for each wave. Partner reading for pp. 399-403. Students who score under 67.5% on CFA 3.1 get Review 3.1 automatically; check it before Lesson 3.",
        },
    },
    {
        "num": 3, "days": "Days 40-41", "title": "Reading the Shadow Zone", "targets": ["3.2"], "cfa": "3.2",
        "notebook": """<p><strong>Title:</strong> L3 Reading the Shadow Zone. Add it to your table of contents.</p>
<ol>
<li>Glue or tape your colored <strong>Shadow Zone Map</strong> on the page.</li>
<li>Next to it, copy the station data table (Slide 3) and the 3 rules from Slide 4.</li>
<li>Write your CER (Slide 5) at the bottom of the page.</li>
</ol>""",
        "slides": [
            ("Do Now", "<p>A station gets P-waves but no S-waves. Based on Lesson 2, what kind of material did the waves go through? How do you know?</p>"),
            ("Learning target 3.2", f"<p>{LT['3.2']}</p>"),
            ("Station data", f"""<p>One earthquake was recorded by stations all around the world. Distance is in degrees around Earth from the earthquake (0&deg; = right at the earthquake, 180&deg; = the exact opposite side).</p>
<table {T}>
<tr><th>Distance</th><th>P-waves?</th><th>S-waves?</th><th>Color</th></tr>
<tr><td>20&deg;</td><td>Yes</td><td>Yes</td><td>green</td></tr>
<tr><td>50&deg;</td><td>Yes</td><td>Yes</td><td>green</td></tr>
<tr><td>80&deg;</td><td>Yes</td><td>Yes</td><td>green</td></tr>
<tr><td>100&deg;</td><td>Yes</td><td>Yes</td><td>green</td></tr>
<tr><td>110&deg;</td><td>No</td><td>No</td><td>red</td></tr>
<tr><td>120&deg;</td><td>No</td><td>No</td><td>red</td></tr>
<tr><td>135&deg;</td><td>No</td><td>No</td><td>red</td></tr>
<tr><td>150&deg;</td><td>Yes</td><td>No</td><td>yellow</td></tr>
<tr><td>165&deg;</td><td>Yes</td><td>No</td><td>yellow</td></tr>
<tr><td>180&deg;</td><td>Yes</td><td>No</td><td>yellow</td></tr>
</table>
<p>On your Shadow Zone Map, color a dot at each distance on <strong>both</strong> sides of the circle. Then shade in each color zone.</p>"""),
            ("Make sense of the map", """<p><strong>3 rules:</strong></p>
<ol>
<li><strong>Green</strong> (P and S): the waves only went through solid rock.</li>
<li><strong>Yellow</strong> (P only): the waves went through a <strong>liquid</strong>. S-waves were stopped.</li>
<li><strong>Red</strong> (nothing): the <strong>shadow zone</strong>. P-waves bent (refracted) at the core and missed this area; S-waves were stopped.</li>
</ol>
<p><strong>Now draw:</strong> a circle inside Earth that would block S-waves from reaching every yellow station. Label it "liquid outer core."</p>"""),
            ("CER: Which layer is liquid?", """<p><strong>Claim:</strong> The ______ is liquid.<br>
<strong>Evidence:</strong> Stations at ______ recorded P-waves but no S-waves. Stations at ______ recorded no waves at all.<br>
<strong>Reasoning:</strong> S-waves cannot travel through ______, so ______. P-waves bend when they enter the core, so ______.</p>"""),
            ("Show what you know: CFA 3.2", "<p>Take <strong>Unit 3 CFA 3.2: Seismic data reveals layers</strong> (5 questions). If you score below a B, a review page for this target will open for you.</p>"),
        ],
        "teacher": {
            "glance": "Two days. Day 40: color the shadow zone map from station data. Day 41: interpret the map, draw the core, write a CER, then CFA 3.2.",
            "materials": f"""Printed <a href="{REPO}/shadow-zone-map.pdf">Shadow Zone Map</a> (1 per student) and the <a href="{REPO}/shadow-zone-map-KEY.pdf">teacher key</a> (these are in the course GitHub repo; print from there); green, yellow, and red colored pencils; glue sticks; Chromebooks for CFA 3.2.""",
            "agenda": [("Day 40: 5", "Do Now: liquid, because S-waves can't travel through liquid."),
                       ("10", "Model how to read degrees on the map: 0&deg; at the earthquake, both sides count up to 180&deg;. Plot the 20&deg; station together."),
                       ("25", "Pairs plot and color all stations on both sides, then shade the zones."),
                       ("10", "Gallery walk: does everyone's map look the same? Why is it symmetrical?"),
                       ("Day 41: 10", "Go over the 3 rules. Ask: what would have to be inside Earth to make the yellow zone?"),
                       ("10", "Students draw the liquid outer core. Show the key; discuss why the P-waves bending creates the red ring."),
                       ("15", "CER with frames."),
                       ("15", "CFA 3.2 on Canvas.")],
            "notes": """<ul>
<li>Real values: the P-wave shadow zone is about 104&deg;-140&deg; from the earthquake. S-waves are missing everywhere beyond about 104&deg;.</li>
<li>The core-mantle boundary is about 2,900 km deep. The key draws it to scale.</li>
<li>Common misconception: "the earthquake wasn't strong enough to reach." Counter: the farthest stations (180&deg;) still get P-waves.</li>
<li>Inner core is solid (found by Lehmann in 1936 from faint P-waves inside the shadow zone). Mention it as an extension; it's not needed for the CER.</li>
</ul>""",
            "key": """<p><strong>Map:</strong> green 0&deg;-100&deg;, red 110&deg;-135&deg;, yellow 150&deg;-180&deg;, on both sides. The drawn core should block straight-line paths to the yellow zone.</p>
<p><strong>CER:</strong> Claim: the outer core is liquid. Evidence: stations at 150&deg;, 165&deg;, 180&deg; got P-waves but no S-waves; stations at 110&deg;-135&deg; got no waves. Reasoning: S-waves cannot travel through liquid, so they were stopped by the outer core; P-waves bend when they enter the core, so they miss the 110&deg;-135&deg; stations and make the shadow zone.</p>
<p><strong>CFA 3.2 key:</strong> C and D (multi-select), D, C, B, A.</p>""",
            "supports": "Pre-color the 20&deg; dot on student maps. CER frames on the slide. Pair a strong reader with each student who needs support for the CER.",
        },
    },
    {
        "num": 4, "days": "Day 42", "title": "Earth's Layers and the Density Lab", "targets": ["3.3"], "cfa": "3.3",
        "notebook": """<p><strong>Title:</strong> L4 Density Lab and Earth's Layers. Add it to your table of contents.</p>
<ol>
<li><strong>Lab section:</strong> question, prediction, a labeled drawing of your density column, and your observations.</li>
<li><strong>Layers section:</strong> draw a large circle cut in half (like a cut peach). Draw and label the 4 layers.</li>
<li>Copy and fill in the layers chart from Slide 5.</li>
</ol>""",
        "slides": [
            ("Do Now", "<p>If you pour honey, water, and oil into one cup, what do you think will happen? Draw your prediction.</p>"),
            ("Learning target 3.3", f"<p>{LT['3.3']}</p>"),
            ("Density lab", """<p><strong>Question:</strong> What happens when liquids with different densities are put together?</p>
<ol>
<li>Pour a small amount of <strong>honey</strong> into the cup. Let it settle.</li>
<li>Slowly pour <strong>dish soap</strong> down the side of the cup.</li>
<li>Slowly pour <strong>colored water</strong> down the side.</li>
<li>Slowly pour <strong>vegetable oil</strong> down the side.</li>
<li>Gently drop in a <strong>penny</strong>, a <strong>grape</strong>, and a <strong>plastic bead</strong>. Where does each one stop?</li>
<li>Draw and label your column.</li>
</ol>
<p><strong>Safety:</strong> No tasting. Clean spills right away (soap and oil are slippery).</p>"""),
            ("Connect the lab to Earth", """<p>In the cup, the <strong>densest</strong> material sank to the bottom and the <strong>least dense</strong> floated on top.</p>
<p>When Earth was young and very hot, the same thing happened. Heavy metals (iron and nickel) sank to the center. Lighter rock rose to the top. That's why Earth has <strong>layers</strong>.</p>"""),
            ("Earth's layers", f"""<table {T}>
<tr><th>Layer</th><th>Made of</th><th>Solid or liquid</th><th>Density</th><th>Temperature</th><th>Depth</th></tr>
<tr><td>Crust</td><td>______</td><td>______</td><td>least dense</td><td>coolest</td><td>0 to about 5-70 km</td></tr>
<tr><td>Mantle</td><td>______</td><td>______</td><td>______</td><td>______</td><td>to about 2,900 km</td></tr>
<tr><td>Outer core</td><td>______</td><td>______</td><td>______</td><td>______</td><td>to about 5,150 km</td></tr>
<tr><td>Inner core</td><td>______</td><td>______</td><td>most dense</td><td>hottest</td><td>to 6,371 km (center)</td></tr>
</table>
<p><strong>Pattern:</strong> As you go deeper, Earth gets ______ and ______.</p>
<p><strong>Puzzle:</strong> The inner core is the hottest layer. Why is it solid? (Hint: think about the weight of everything above it.)</p>"""),
            ("Show what you know: CFA 3.3", "<p>Take <strong>Unit 3 CFA 3.3: Describe Earth's layers</strong> (5 questions). If you score below a B, a review page for this target will open for you.</p>"),
        ],
        "teacher": {
            "glance": "One day. Density column lab, connect to Earth's layering, fill in the layers chart, then CFA 3.3.",
            "materials": "Per group (3-4 students): clear plastic cup; about 2 tbsp each of honey (or corn syrup), dish soap, water with food coloring, vegetable oil; a penny, a grape, a small plastic bead; paper towels. Chromebooks for CFA 3.3.",
            "agenda": [("5", "Do Now prediction."),
                       ("15", "Density lab in groups. Circulate; remind students to pour slowly down the side."),
                       ("5", "Debrief: densest on the bottom. Where did the penny, grape, and bead stop, and why?"),
                       ("12", "Connect to Earth: differentiation. Fill in the layers chart together; discuss the inner core puzzle."),
                       ("13", "CFA 3.3 on Canvas; groups clean up in rotation.")],
            "notes": """<ul>
<li>Typical densities (g/mL): honey about 1.4, dish soap about 1.06, water 1.0, vegetable oil about 0.92. The penny sinks to the bottom; the grape usually rests on the honey or soap; a plastic bead usually floats in or on the oil (depends on the plastic).</li>
<li>Earth layers: crust 5-70 km thick (oceanic thin, continental thick); mantle to about 2,900 km; outer core 2,900-5,150 km; inner core 5,150-6,371 km. Inner core temperature is about 5,000-6,000 &deg;C, similar to the sun's surface.</li>
<li>The mantle is solid but flows over millions of years (plastic behavior). Some students will call it "magma"; correct this here, because Lesson 7 depends on it.</li>
<li>Limitation to discuss: Earth's layers aren't liquids poured in a cup, and the mantle and crust are solid.</li>
</ul>""",
            "key": """<p><strong>Layers chart:</strong> Crust: rock, solid. Mantle: rock, solid that flows slowly, denser than crust, hot. Outer core: iron and nickel, liquid, denser, very hot. Inner core: iron and nickel, solid, most dense, hottest. Pattern: hotter and denser. Puzzle: the pressure is so great that the metal is squeezed into a solid.</p>
<p><strong>CFA 3.3 key:</strong> A, B, C, D, B.</p>""",
            "supports": "Pre-measure liquids into labeled cups for each group. Provide a word bank for the layers chart (rock, iron and nickel, solid, liquid, solid that flows slowly).",
        },
    },
    {
        "num": 5, "days": "Day 43", "title": "Mid-Unit Check: Reteach and Extend", "targets": ["3.1", "3.2", "3.3"],
        "notebook": """<p><strong>Title:</strong> L5 Mid-Unit Check. Add it to your table of contents.</p>
<ol>
<li>Go to your Unit 3 targets page. Rate yourself 1-4 on targets 3.1, 3.2, and 3.3, using your CFA scores.</li>
<li>Write the station you are assigned to and what you worked on.</li>
<li>Finish with the exit ticket (Slide 5).</li>
</ol>""",
        "slides": [
            ("Do Now", "<p>Open Canvas and look at your scores on CFAs 3.1, 3.2, and 3.3. Rate yourself on each target on your targets page.</p>"),
            ("Today's targets", "<ul>" + "".join(f"<li><strong>{k}</strong> {LT[k]}</li>" for k in ("3.1", "3.2", "3.3")) + "</ul>"),
            ("Where do I go?", """<p><strong>If a review opened for you on Canvas</strong> (Review 3.1, 3.2, or 3.3): go to the <strong>reteach table</strong> and work through it. Your teacher will work with you.</p>
<p><strong>If no review opened:</strong> go to the <strong>extension table</strong> (Slide 4).</p>"""),
            ("Extension table: Design an Earth", """<p>Imagine a planet that is the same as Earth, except its outer core is <strong>solid</strong>.</p>
<ol>
<li>Draw what the shadow zone map would look like for this planet. Would there still be a shadow zone? Would yellow stations still exist?</li>
<li>Explain how a scientist on that planet would know the core is solid.</li>
<li>Try the Earthquakes 1 - Recording Station Gizmo if you finish.</li>
</ol>"""),
            ("Exit ticket", "<p>Which target (3.1, 3.2, or 3.3) do you feel best about? Which one do you still need help with? Why?</p>"),
        ],
        "teacher": {
            "glance": "Mid-unit check (per the course support plan): use CFA 3.1-3.3 results to split the room into a reteach group and an extension group.",
            "materials": "CFA 3.1-3.3 results (Canvas gradebook or the U3 tab of the Learning Target Tracker); small whiteboards; Slinky; extra Shadow Zone Maps; Chromebooks.",
            "agenda": [("10", "Do Now and self-rating. Pull up scores; quickly confirm group lists."),
                       ("35", "Reteach table: work Reviews 3.1-3.3 with students, focusing on the target each one missed. Extension table: the solid-core thought experiment."),
                       ("5", "Exit ticket.")],
            "notes": """<ul>
<li>The Mastery Paths already opened the right review for each student. Students who got a review should finish it today; mark it complete in SpeedGrader.</li>
<li>Re-check: have reteach students redo 2-3 questions orally or on whiteboards. Record re-check scores in the tracker's Re-check column.</li>
<li>Most-missed items to reteach (predict): S-waves vs liquids (3.1), reading the yellow zone as 'liquid' (3.2), the inner core being solid (3.3).</li>
</ul>""",
            "key": """<p><strong>Extension:</strong> With a solid outer core, S-waves would pass through, so there would be no 'P-only' (yellow) zone. P-waves (and S-waves) would still bend at the boundary because the core is denser, so a smaller shadow zone could still appear. Evidence of a solid core: S-waves arriving on the far side of the planet.</p>""",
            "supports": "Keep reteach groups to 4-6. Use the 'Try it' checks on the review pages as warm-ups.",
        },
    },
    {
        "num": 6, "days": "Day 44", "title": "Where Does Earth's Heat Come From?", "targets": ["3.4"], "cfa": "3.4",
        "notebook": """<p><strong>Title:</strong> L6 Earth's Heat. Add it to your table of contents.</p>
<ol>
<li>Draw a big T-chart: <em>Real sources of Earth's internal heat</em> | <em>NOT sources</em>. Sort the cards from Slide 4.</li>
<li>Under the T-chart, write the two sources in a box with a picture for each.</li>
<li>Answer the exit question (Slide 5).</li>
</ol>""",
        "slides": [
            ("Do Now", "<p>Rub your hands together fast for 10 seconds. What happens? Where did that heat come from?</p>"),
            ("Learning target 3.4", f"<p>{LT['3.4']}</p>"),
            ("Two sources of heat", """<p><strong>1. Heat left from formation.</strong> About 4.6 billion years ago, Earth formed as rocks smashed together. Each crash turned energy of motion into heat, like rubbing your hands. Heavy metals sinking to the center made more heat. Earth is still slowly cooling off.</p>
<p><strong>2. Radioactive decay.</strong> Some elements in rock, like <strong>uranium</strong>, <strong>thorium</strong>, and <strong>potassium</strong>, are unstable. They slowly break down and give off energy as heat. This is still happening today.</p>
<p>Heat always flows from hot to cold: from Earth's hot center <strong>outward</strong> toward the cooler surface.</p>"""),
            ("Card sort: source or not?", """<p>Sort these into <em>Real source</em> or <em>NOT a source</em>:</p>
<ul>
<li>Rocks crashing together when Earth formed</li>
<li>Sunlight</li>
<li>Uranium breaking down in rocks</li>
<li>Volcanoes</li>
<li>Iron sinking to the center of early Earth</li>
<li>Earthquakes</li>
<li>Potassium breaking down in rocks</li>
<li>Ocean tides</li>
</ul>"""),
            ("Exit question", "<p>A classmate says, \"The sun heats Earth's core.\" Explain why they are wrong. Use the two real sources in your answer.</p>"),
            ("Show what you know: CFA 3.4", "<p>Take <strong>Unit 3 CFA 3.4: Sources of Earth's heat</strong> (5 questions). If you score below a B, a review page for this target will open for you.</p>"),
        ],
        "teacher": {
            "glance": "One day. Hand-rubbing hook, two heat sources, card sort, then CFA 3.4.",
            "materials": "Card sort sets (print the 8 items from Slide 4 and cut, 1 set per pair) or students sort in their notebooks; Chromebooks for CFA 3.4.",
            "agenda": [("5", "Do Now: friction turns motion energy into heat."),
                       ("15", "Mini-lesson on the two sources (Slide 3). Act out accretion: students 'collide' fists gently to show motion becoming heat."),
                       ("12", "Card sort in pairs; whole-class check."),
                       ("5", "Exit question in notebooks."),
                       ("13", "CFA 3.4 on Canvas.")],
            "notes": """<ul>
<li>Radioactive decay supplies roughly half of Earth's heat flow today; the rest is primordial heat from accretion and core formation. (Exact split is still debated; 'about half' is a safe classroom statement.)</li>
<li>Volcanoes and earthquakes are effects of internal heat, not sources. The sun drives surface processes (weather, water cycle) but not the interior.</li>
<li>Bridge to Lesson 7: heat flowing outward is what drives mantle convection.</li>
</ul>""",
            "key": """<p><strong>Card sort:</strong> Real sources: rocks crashing together when Earth formed; uranium breaking down; iron sinking to the center of early Earth; potassium breaking down. NOT sources: sunlight; volcanoes; earthquakes; ocean tides.</p>
<p><strong>Exit:</strong> The sun only heats the surface. The heat inside comes from heat left over from Earth's formation and from radioactive decay of elements like uranium.</p>
<p><strong>CFA 3.4 key:</strong> C, A, B, True, D.</p>""",
            "supports": "Picture icons on cards. Sentence frame for the exit: 'The sun only heats ______. The heat inside Earth comes from ______ and ______.'",
        },
    },
    {
        "num": 7, "days": "Days 45-46", "title": "Convection Lab: Heat on the Move", "targets": ["3.5"], "cfa": "3.5",
        "notebook": """<p><strong>Title:</strong> L7 Convection Lab. Add it to your table of contents.</p>
<ol>
<li><strong>Lab:</strong> question, prediction, a side-view drawing of the container with arrows showing how the color moved, and observations.</li>
<li><strong>Model:</strong> draw the mantle as a ring around the core. Add one convection loop with arrows: rise, sideways, cool, sink.</li>
<li>Day 46: reading questions (Slide 5).</li>
</ol>""",
        "slides": [
            ("Do Now", "<p>Hot air balloons rise. Why? What do you think happens to hot rock deep in the mantle?</p>"),
            ("Learning target 3.5", f"<p>{LT['3.5']}</p>"),
            ("Convection lab", """<p><strong>Question:</strong> How does heat make a liquid move?</p>
<ol>
<li>Fill the clear container with room-temperature water. Let it sit still for 1 minute.</li>
<li>Set it so one end sits over a cup of <strong>hot water</strong> and the other end over a cup of <strong>ice water</strong>.</li>
<li>Using the dropper, put 2 drops of <strong>red</strong> food coloring at the bottom over the hot cup, and 2 drops of <strong>blue</strong> at the bottom over the ice cup.</li>
<li>Watch for 5 minutes without bumping the table. Draw what you see every minute.</li>
</ol>
<p><strong>Safety:</strong> Hot water can burn. Don't move the cups once they are set.</p>"""),
            ("Make sense of it", """<p><strong>Hot</strong> water is <strong>less dense</strong>, so it <strong>rises</strong>. At the top it moves sideways and <strong>cools</strong>. <strong>Cool</strong> water is <strong>denser</strong>, so it <strong>sinks</strong>. This loop is a <strong>convection current</strong>.</p>
<p>The mantle does the same thing, but much, much slower (a few centimeters per year) because it is solid rock that flows like putty.</p>
<table border="1" cellpadding="6" style="border-collapse:collapse">
<tr><th>In the lab</th><th>In Earth</th></tr>
<tr><td>Hot water cup</td><td>______</td></tr>
<tr><td>Water in the container</td><td>______</td></tr>
<tr><td>Ice water cup / cool top</td><td>______</td></tr>
</table>"""),
            ("Day 46: Reading", """<p>Read <strong>Module 13, Lesson 4: Causes of Plate Motions (pp. 362-364)</strong>. Answer in your notebook:</p>
<ol>
<li>What is a convection current?</li>
<li>Where does the energy for mantle convection come from?</li>
<li>How does mantle convection affect the plates of the crust?</li>
</ol>"""),
            ("Show what you know: CFA 3.5", "<p>Take <strong>Unit 3 CFA 3.5: Model mantle convection</strong> (5 questions). If you score below a B, a review page for this target will open for you.</p>"),
        ],
        "teacher": {
            "glance": "Two days. Day 45: convection lab and lab-to-Earth model. Day 46: textbook reading + questions, then CFA 3.5.",
            "materials": "Per group: clear plastic shoebox or loaf-pan-size container; 2 small cups (one hot tap water, one ice water) to set under the ends; red and blue food coloring; dropper or pipette; paper towels. Hot water from a kettle or tap (no boiling water at tables). Textbooks (Module 13, Lesson 4, pp. 362-364); Chromebooks.",
            "agenda": [("Day 45: 5", "Do Now: hot air is less dense, so it rises."),
                       ("10", "Set up; teacher demo of dropping coloring at the bottom slowly."),
                       ("15", "Observe and draw at 1-minute intervals."),
                       ("15", "Debrief; complete the lab-to-Earth table; draw the mantle convection loop."),
                       ("5", "Exit: show the loop with your finger in the air."),
                       ("Day 46: 5", "Review the loop: heated, rises, sideways, cools, sinks."),
                       ("25", "Reading pp. 362-364 with questions."),
                       ("15", "CFA 3.5 on Canvas."),
                       ("5", "Preview Lesson 8: you will build a full model.")],
            "notes": """<ul>
<li>Red should rise over the hot cup, spread across the top, and drift down at the cold end; blue should stay low and spread along the bottom toward the hot side. Results improve if the water sits still first.</li>
<li>Stress the limitation: the lab uses fast-moving liquid; the mantle is solid rock moving a few cm per year (about as fast as fingernails grow).</li>
<li>Mantle convection is one driver of plate motion (with slab pull and ridge push in the textbook). Keep the focus on convection for this unit; Unit 4 picks up plate motion.</li>
</ul>""",
            "key": """<p><strong>Lab-to-Earth table:</strong> hot cup = the core (heat source); water = the mantle; ice cup / cool top = the cooler region near the crust.</p>
<p><strong>Reading:</strong> (1) A loop where heated material rises, cools, and sinks. (2) Earth's internal heat: heat from formation and radioactive decay, flowing out from the core. (3) The slowly moving mantle drags or pushes the plates, so they move a few cm per year.</p>
<p><strong>CFA 3.5 key:</strong> B, A, C, D, A.</p>""",
            "supports": "Assign roles (dropper, timer, artist, reporter). Provide a partially drawn convection loop for students who need it.",
        },
    },
    {
        "num": 8, "days": "Days 47-48", "title": "Build Your Earth Interior Model", "targets": ["3.2", "3.3", "3.4", "3.5"],
        "notebook": """<p><strong>Title:</strong> L8 Earth Interior Model. Add it to your table of contents.</p>
<ol>
<li>Day 47: sketch a rough draft of your model here first.</li>
<li>Day 48: tape your peer feedback (Slide 4) here, and list 2 changes you made.</li>
</ol>""",
        "slides": [
            ("Do Now", "<p>Look back at the drawing on your Unit 3 cover page from Day 37. What would you change now?</p>"),
            ("Your task", """<p>Build a labeled model (poster or full notebook page) of Earth's interior that answers the driving question: <strong>What is inside Earth, and why does it move?</strong></p>"""),
            ("Model checklist", """<ul>
<li>&#9744; All 4 layers, drawn in the right order, labeled</li>
<li>&#9744; For each layer: solid or liquid, and what it's made of</li>
<li>&#9744; Arrows showing heat flowing <strong>outward</strong> from the core</li>
<li>&#9744; The 2 sources of Earth's heat, labeled</li>
<li>&#9744; At least one <strong>convection loop</strong> in the mantle (rise, sideways, cool, sink)</li>
<li>&#9744; One seismic wave path: an S-wave stopping at the outer core, and a P-wave passing through</li>
<li>&#9744; A short written explanation (3-5 sentences): how we know what's inside Earth, and how heat makes the mantle move</li>
</ul>"""),
            ("Day 48: Peer review", """<p>Trade models with a partner. Use the checklist. Write on a sticky note:</p>
<p><strong>Glow:</strong> One thing your model shows really well is ______.<br>
<strong>Grow:</strong> Your model would be clearer if you ______.</p>
<p>Then revise your model using the feedback.</p>"""),
            ("Exit ticket", "<p>What is one change you made to your model after peer review, and why?</p>"),
        ],
        "teacher": {
            "glance": "Two days. Students build the unit summative model (scope & sequence summative: labeled model of Earth's interior showing heat flow and convection, with a short written explanation). Day 48 is peer review and revision.",
            "materials": "Poster paper or 11x17 paper; colored pencils/markers; rulers; compasses or lids to trace circles; sticky notes.",
            "agenda": [("Day 47: 5", "Do Now: revisit the Day 37 drawing."),
                       ("10", "Go over the checklist; show a quick teacher sketch (layers only) as a starting point."),
                       ("35", "Draft and start the final model."),
                       ("Day 48: 20", "Finish the model."),
                       ("15", "Peer review with glow/grow."),
                       ("10", "Revise; exit ticket."),
                       ("5", "Collect or photograph models.")],
            "notes": """<ul>
<li>Score the model on targets 3.2-3.5 (0-4 each) using the checklist, or use it as evidence alongside the CSA.</li>
<li>If you want students to submit a photo on Canvas, add an assignment to the module (not created yet).</li>
</ul>""",
            "key": """<p><strong>Strong model:</strong> crust, mantle, liquid outer core, solid inner core in order; iron and nickel cores; arrows outward; 'heat from formation' and 'radioactive decay' labeled; a mantle loop rising near the core and sinking near the crust; an S-wave stopping at the outer core and a P-wave bending through it. Explanation mentions seismic waves as evidence and density differences driving convection.</p>""",
            "supports": "Offer a pre-drawn circle template with layer boundaries for students who need it. Checklist doubles as a scoring guide.",
        },
    },
    {
        "num": 9, "days": "Day 49", "title": "Review Day and Practice Test", "targets": ["3.1", "3.2", "3.3", "3.4", "3.5"],
        "notebook": """<p><strong>Title:</strong> L9 Review. Add it to your table of contents.</p>
<ol>
<li>Re-rate yourself on all 5 targets on your targets page.</li>
<li>For each review station, write 1 thing you learned or fixed.</li>
<li>Revisit the driving question on your cover page: answer it in 2-3 sentences.</li>
</ol>""",
        "slides": [
            ("Do Now", "<p>Rate yourself 1-4 on each Unit 3 target. Circle the one you'll focus on today.</p>"),
            ("Practice test", "<p>Take the <strong>Unit 3 Practice Test</strong> on Canvas. It looks just like the real CSA: 13 questions, including 2 written answers. After your teacher grades it, a review (C, D, or F) or an extension (A or B) will open for you.</p>"),
            ("Review stations", """<ol>
<li><strong>Waves:</strong> Slinky and hand-gesture quiz. P or S?</li>
<li><strong>Shadow zone:</strong> color a new station table and write a CER.</li>
<li><strong>Layers:</strong> put layer cards in order and match properties.</li>
<li><strong>Heat and convection:</strong> sequence the convection loop cards; name the 2 heat sources.</li>
</ol>"""),
            ("Driving question, revisited", "<p><strong>What is inside Earth, and why does it move?</strong> Answer it on your cover page using at least 4 vocabulary words.</p>"),
        ],
        "teacher": {
            "glance": "Review day before the CSA (per the support plan): practice test in the same format, then stations. The practice test's Mastery Path opens the review (below a B) or the extension (A or B) once essays are graded.",
            "materials": "Chromebooks; Slinkys; extra Shadow Zone Maps; layer and convection-step cards; the class chart of Day 37 driving-question ideas.",
            "agenda": [("5", "Do Now self-rating."),
                       ("25", "Practice test. Grade the two essays (P5, P13) during stations so the Mastery Path opens before Day 50."),
                       ("15", "Review stations (rotate by need, using CFA and practice results)."),
                       ("5", "Driving question revisited; compare with the Day 37 class chart.")],
            "notes": """<ul>
<li>Mastery Paths wait for the full practice-test score, so the two essays must be graded before students see their review/extension.</li>
<li>If grading can't finish today, students work on the path assignment as a warm-up on Day 50 or as homework.</li>
</ul>""",
            "key": "<p>Practice test key and rubrics: see <em>assessments/unit-3-practice-and-mastery-paths.md</em> in the course repo.</p>",
            "supports": "Send students to the station for their lowest target first.",
        },
    },
    {
        "num": 10, "days": "Day 50", "title": "Unit 3 CSA", "targets": ["3.1", "3.2", "3.3", "3.4", "3.5"],
        "notebook": """<p><strong>Title:</strong> L10 CSA reflection. Add it to your table of contents.</p>
<p>After the test: rate yourself on all 5 targets one last time. Which target improved the most since Day 37?</p>""",
        "slides": [
            ("Before you start", "<p>Clear your desk except for your Chromebook and a pencil. You may sketch on scratch paper. Read every question twice. Questions 5 and 13 need written answers: use claim, evidence, and reasoning.</p>"),
            ("Unit 3 CSA", "<p>Open <strong>Unit 3 CSA: Forces Beneath Our Feet (HS-ESS2-3)</strong> on Canvas.</p>"),
            ("When you finish", "<p>Do your notebook reflection. Then work quietly on your review or extension assignment from the practice test, or a Gizmo.</p>"),
        ],
        "teacher": {
            "glance": "Summative day: Unit 3 CSA (13 questions; 11 self-graded, 2 teacher-graded free responses).",
            "materials": "Chromebooks; scratch paper.",
            "agenda": [("5", "Directions; students open the CSA."),
                       ("40", "CSA."),
                       ("5", "Notebook reflection.")],
            "notes": """<ul>
<li>Score Q5 and Q13 with the rubrics; record per-target scores in the U3 tab of the Learning Target Tracker (CSA columns).</li>
<li>Students under 1.8 on a target get an intervention pick in the tracker.</li>
</ul>""",
            "key": "<p>CSA key and rubrics: see <em>assessments/unit-3-csa-mastery-connect.md</em> in the course repo.</p>",
            "supports": "Extended time and read-aloud per IEP/504. Small-group setting as needed.",
        },
    },
]
