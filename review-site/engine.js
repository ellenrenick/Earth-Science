// ===== Animations =====
const RM=matchMedia("(prefers-reduced-motion: reduce)").matches;
const ANIM={};
const sq=(svg,k)=>svg.querySelector(`[data-k="${k}"]`);

function mountAnim(kind,el,o={}){
  const A=ANIM[kind];if(!A){return}
  el.classList.add("anim");
  if(A.custom){A.custom(el,o);return}
  el.innerHTML=`<svg viewBox="${A.vb}" role="img" aria-label="${A.alt}">${A.svg}</svg>
  <div class="actl"><button type="button" class="play">▶ Play</button>
  <label class="sl"><span>${A.slider}</span><input type="range" min="0" max="100" value="0"></label></div>
  <p class="cap" aria-live="polite"></p>`;
  const svg=el.querySelector("svg"),btn=el.querySelector(".play"),rng=el.querySelector("input"),cap=el.querySelector(".cap");
  let t=0,raf=0;
  const set=v=>{t=Math.max(0,Math.min(1,v));rng.value=Math.round(t*100);A.draw(svg,t,cap)};
  const stop=()=>{cancelAnimationFrame(raf);raf=0;btn.textContent="▶ Play"};
  const run=to=>{
    stop();
    if(RM){set(to);return}
    const from=t>=to-0.01?0:t,t0=performance.now(),dur=Math.max(400,A.dur*Math.abs(to-from));
    btn.textContent="❚❚ Pause";
    const step=now=>{
      if(!el.isConnected){return}
      const k=Math.min(1,(now-t0)/dur);set(from+(to-from)*k);
      if(k<1)raf=requestAnimationFrame(step);else stop();
    };
    raf=requestAnimationFrame(step);
  };
  btn.onclick=()=>raf?stop():run(1);
  rng.oninput=()=>{stop();set(rng.value/100)};
  set(o.from||0);
  if(o.autoplay)setTimeout(()=>run(o.to==null?1:o.to),250);
}

// --- 5.1 Continents fit ---
(()=>{
  const cy=y=>200+22*Math.sin((y-30)/150*Math.PI);
  const pts=[];for(let y=30;y<=180;y+=10)pts.push([+cy(y).toFixed(1),y]);
  const edge=pts.map(p=>p.join(",")).join(" L");
  const sa=`M110,30 L${edge} L120,180 L100,110 Z`;
  const af=`M${edge} L300,180 L325,110 L310,30 Z`;
  const mk=(y,dx)=>`<circle cx="${cy(y)+dx}" cy="${y}" r="6" class="s-fossil"/>`;
  const tri=(y,dx)=>`<path d="M${cy(y)+dx-6},${y+6} L${cy(y)+dx},${y-6} L${cy(y)+dx+6},${y+6} Z" class="s-fossil2"/>`;
  ANIM.fit={vb:"0 0 400 215",dur:6000,slider:"Rewind time",
    alt:"South America and Africa drifting together, with fossils and a rock band that line up when the continents are joined.",
    svg:`<rect x="0" y="0" width="400" height="215" class="s-water"/>
    <g data-k="sa"><path d="${sa}" class="s-cont"/>
      <line x1="112" y1="82" x2="${cy(82)}" y2="82" class="s-band"/>${tri(60,-16)}${mk(110,-16)}${tri(150,-16)}
      <text x="150" y="205" class="t" text-anchor="middle">South America</text></g>
    <g data-k="af"><path d="${af}" class="s-cont"/>
      <line x1="${cy(82)}" y1="82" x2="316" y2="82" class="s-band"/>${tri(60,16)}${mk(110,16)}${tri(150,16)}
      <text x="270" y="205" class="t" text-anchor="middle">Africa</text></g>
    <text x="200" y="16" class="t" text-anchor="middle" data-k="lbl"></text>
    <g class="t" font-size="10"><circle cx="14" cy="14" r="5" class="s-fossil"/><text x="24" y="18">Mesosaurus</text>
    <path d="M10,32 L14,24 L18,32 Z" class="s-fossil2"/><text x="24" y="31">Glossopteris</text>
    <line x1="8" y1="42" x2="20" y2="42" class="s-band"/><text x="24" y="45">Matching rock</text></g>`,
    draw(svg,t,cap){
      const g=70*(1-t);
      sq(svg,"sa").setAttribute("transform",`translate(${-g},0)`);
      sq(svg,"af").setAttribute("transform",`translate(${g},0)`);
      const joined=t>0.97;
      cap.textContent=t<0.03?"Today: an ocean separates them. Press play or drag to rewind time."
        :joined?"About 280 million years ago: the coasts fit, the fossils sit side by side, and the rock band is one line."
        :`${Math.round(280*t)} million years ago: the continents are moving back together.`;
      cap.classList.toggle("hi",joined);
    }};
})();

// --- 5.2 Seafloor ages and stripes ---
(()=>{
  let b="";
  for(let i=0;i<12;i++){
    const f=`hsl(${10+i*22},70%,${60-i*2}%)`;
    b+=`<rect x="${200+i*15}" y="22" width="15" height="48" fill="${f}"/><rect x="${200-(i+1)*15}" y="22" width="15" height="48" fill="${f}"/>`;
  }
  const bd=[0,18,40,52,86,100,130,150,180];let st="";
  for(let k=0;k<bd.length-1;k++){
    const c=k%2?"s-cr":"s-cn";
    st+=`<rect x="${200+bd[k]}" y="84" width="${bd[k+1]-bd[k]}" height="20" class="${c}"/><rect x="${200-bd[k+1]}" y="84" width="${bd[k+1]-bd[k]}" height="20" class="${c}"/>`;
  }
  const ticks=[0,500,1000,1500].map(v=>{const d=v/1500*180;return `<text x="${200+d}" y="134" class="t" text-anchor="middle" font-size="10">${v?v+" km":"0 km (ridge)"}</text>`+(v?`<text x="${200-d}" y="134" class="t" text-anchor="middle" font-size="10">${v} km</text>`:"")}).join("");
  ANIM.ages={vb:"0 0 400 145",dur:5000,slider:"Distance from the ridge",
    alt:"Cross-section of the seafloor: rock gets older away from a mid-ocean ridge, and magnetic stripes mirror each other on both sides.",
    svg:`${b}${st}
    <text x="200" y="14" class="t" text-anchor="middle" font-size="10">Rock age (red = youngest, blue = oldest)</text>
    <text x="200" y="118" class="t" text-anchor="middle" font-size="10">Magnetic stripes (dark = normal, light = reversed)</text>${ticks}
    <line data-k="mr" y1="18" y2="108" class="s-mark"/><line data-k="ml" y1="18" y2="108" class="s-mark"/>`,
    draw(svg,t,cap){
      const x=180*t,km=Math.round(1500*t),age=Math.round(km/25);
      sq(svg,"mr").setAttribute("x1",200+x);sq(svg,"mr").setAttribute("x2",200+x);
      sq(svg,"ml").setAttribute("x1",200-x);sq(svg,"ml").setAttribute("x2",200-x);
      cap.textContent=km===0?"At the ridge (0 km) the rock is brand new, 0 million years old."
        :`${km.toLocaleString()} km from the ridge, on either side: the rock is about ${age} million years old.`;
    }};
})();

// --- 5.3 Seafloor spreading ---
(()=>{
  const starts=[0,.14,.3,.46,.64,.82];
  ANIM.spread={vb:"0 0 400 175",dur:9000,slider:"Time passing",
    alt:"Magma rises at a mid-ocean ridge, cools into new crust, and pushes older crust away on both sides. Each magnetic flip adds a new stripe.",
    svg:`<rect x="0" y="0" width="400" height="50" class="s-water"/><rect x="0" y="90" width="400" height="85" class="s-mantle"/>
    <g data-k="b"></g><path data-k="mg" class="s-magma"/>
    <g data-k="ar" class="s-arrow"><path d="M240,70 H275 M270,65 L277,70 L270,75"/><path d="M160,70 H125 M130,65 L123,70 L130,75"/></g>
    <text x="200" y="30" class="t" text-anchor="middle" font-size="11">Mid-ocean ridge</text>
    <text x="8" y="138" class="t" font-size="10">Hot mantle</text>
    <text x="392" y="168" class="t" text-anchor="end" font-size="10">Spreading rate here: 25 km per million years (2.5 cm/yr)</text>`,
    draw(svg,t,cap){
      let h="";
      starts.forEach((s0,i)=>{
        const s1=starts[i+1]??9;if(t<=s0)return;
        const far=(t-s0)*170,near=Math.max(0,(t-s1)*170),c=i%2?"s-cr":"s-cn";
        h+=`<rect x="${200+near}" y="50" width="${far-near}" height="40" class="${c}"/><rect x="${200-far}" y="50" width="${far-near}" height="40" class="${c}"/>`;
      });
      sq(svg,"b").innerHTML=h;
      const top=50+40*(1-Math.min(1,t*6));
      sq(svg,"mg").setAttribute("d",`M188,175 L212,175 L206,${top} L194,${top} Z`);
      sq(svg,"ar").style.opacity=t>0.28?1:0;
      cap.textContent=t<0.14?"1. Rise: magma rises at the ridge."
        :t<0.38?"2. Cool: it cools and hardens into new crust, locking in Earth's magnetic direction."
        :t<0.78?"3. Push: new crust pushes older crust away on both sides. Each field flip adds a new stripe."
        :"4. Older: the farther from the ridge, the older the crust. The stripes mirror each other.";
    }};
})();

// --- 5.5 Subduction (also used in 5.4) ---
ANIM.subduct={vb:"0 0 400 175",dur:7000,slider:"Plates colliding",
  alt:"A dense oceanic plate bends down and sinks beneath lighter continental crust, forming a trench. Magma rises to a volcano.",
  svg:`<rect x="0" y="62" width="400" height="113" class="s-mantle"/><rect x="0" y="40" width="172" height="25" class="s-water"/>
  <path data-k="sl" class="s-slab" fill="none" stroke-width="14"/>
  <path d="M165,22 L400,22 L400,62 L165,62 Z" class="s-cont"/>
  <path d="M285,22 L300,2 L315,22 Z" class="s-oc"/>
  <line data-k="mg" x1="272" y1="150" x2="298" y2="24" class="s-magmaline"/>
  <g class="s-arrow"><path d="M12,30 H48 M42,25 L49,30 L42,35"/></g>
  <text x="10" y="100" class="t" font-size="11">Oceanic crust: dense, 3.0 g/cm³</text>
  <text x="232" y="48" class="t" font-size="11" text-anchor="middle">Continental crust: light, 2.7 g/cm³</text>
  <text data-k="tr" x="104" y="57" class="t" font-size="11" font-weight="700">trench</text>`,
  draw(svg,t,cap){
    sq(svg,"sl").setAttribute("d",`M0,69 L130,69 Q175,69 ${175+95*t},${69+90*t}`);
    sq(svg,"mg").style.opacity=t>0.7?1:0;
    sq(svg,"tr").style.opacity=t>0.35?1:0;
    cap.textContent=t<0.3?"Two plates move toward each other."
      :t<0.7?"The dense oceanic plate bends down and sinks. That is subduction, and a trench forms."
      :"The light continental crust is too buoyant to sink. Magma rises to feed volcanoes.";
  }};

// --- 5.4 pieces: divergent, continent collision, transform ---
ANIM.divergent={vb:"0 0 400 140",dur:5000,slider:"Plates pulling apart",
  alt:"Two plates move apart and magma rises between them, forming a mid-ocean ridge or rift valley.",
  svg:`<rect x="0" y="90" width="400" height="50" class="s-mantle"/>
  <rect data-k="l" y="50" height="40" class="s-oc"/><rect data-k="r" y="50" height="40" class="s-oc"/>
  <rect data-k="m" y="50" height="45" class="s-magma"/>
  <g class="s-arrow"><path d="M150,30 H110 M116,25 L109,30 L116,35"/><path d="M250,30 H290 M284,25 L291,30 L284,35"/></g>
  <text x="200" y="125" class="t" text-anchor="middle" font-size="11">Mid-ocean ridge or rift valley</text>`,
  draw(svg,t,cap){
    const s=8+55*t;
    sq(svg,"l").setAttribute("x",-10);sq(svg,"l").setAttribute("width",210-s);
    sq(svg,"r").setAttribute("x",200+s);sq(svg,"r").setAttribute("width",210-s);
    sq(svg,"m").setAttribute("x",200-s);sq(svg,"m").setAttribute("width",2*s);
    cap.textContent="Divergent (Divide): plates move apart and magma fills the gap. Landforms: mid-ocean ridge, rift valley. Examples: Mid-Atlantic Ridge, East African Rift.";
  }};
ANIM.collide={vb:"0 0 400 140",dur:5000,slider:"Continents colliding",
  alt:"Two continents move together; neither sinks, so the crust crumples into a tall mountain range.",
  svg:`<rect x="0" y="110" width="400" height="30" class="s-mantle"/>
  <rect data-k="l" y="70" width="175" height="40" class="s-cont"/><rect data-k="r" y="70" width="175" height="40" class="s-cont"/>
  <path data-k="mt" class="s-cont2"/>
  <g class="s-arrow"><path d="M40,45 H80 M74,40 L81,45 L74,50"/><path d="M360,45 H320 M326,40 L319,45 L326,50"/></g>
  <text x="200" y="130" class="t" text-anchor="middle" font-size="11">Neither continent sinks</text>`,
  draw(svg,t,cap){
    sq(svg,"l").setAttribute("x",30*t);sq(svg,"r").setAttribute("x",195-30*t);
    const w=40+90*t,h=70*t;
    sq(svg,"mt").setAttribute("d",`M${200-w},70 L${200-w*0.3},${70-h*0.8} L200,${70-h} L${200+w*0.4},${70-h*0.7} L${200+w},70 Z`);
    cap.textContent="Convergent (Come together): two continents collide. Neither sinks, so the crust crumples into tall mountains. Example: the Himalayas.";
  }};
ANIM.transform={vb:"0 0 400 165",dur:5000,slider:"Plates sliding",
  alt:"Seen from above, two plates slide past each other along a fault and offset a stream.",
  svg:`<rect data-k="a" x="0" y="20" width="400" height="55" class="s-oc"/><rect data-k="b" x="0" y="90" width="400" height="55" class="s-oc"/>
  <line x1="0" y1="82" x2="400" y2="82" class="s-fault"/><path data-k="st" class="s-stream" fill="none"/>
  <g class="s-arrow"><path d="M320,47 H360 M354,42 L361,47 L354,52"/><path d="M80,118 H40 M46,113 L39,118 L46,123"/></g>
  <text x="200" y="12" class="t" text-anchor="middle" font-size="10">View from above</text>
  <text x="200" y="160" class="t" text-anchor="middle" font-size="11">Fault: the stream is offset</text>`,
  draw(svg,t,cap){
    const d=50*t;
    sq(svg,"a").setAttribute("x",d-50);sq(svg,"b").setAttribute("x",50-d);
    sq(svg,"st").setAttribute("d",`M${200+d},20 L${200+d},75 L${200-d},90 L${200-d},145`);
    cap.textContent="Transform (slide): plates slide past each other. Landforms: faults and offset streams. Example: the San Andreas Fault.";
  }};

ANIM.bound={custom(el,o){
  const tabs=[["div","Divergent","divergent"],["subduct","Convergent: ocean + continent","subduct"],["cc","Convergent: two continents","collide"],["tr","Transform","transform"]];
  el.innerHTML=`<div class="tabs" role="tablist">${tabs.map(x=>`<button type="button" role="tab" data-t="${x[0]}">${x[1]}</button>`).join("")}</div><div class="stage"></div>`;
  const stage=el.querySelector(".stage"),bs=[...el.querySelectorAll(".tabs button")];
  const show=(k,auto)=>{bs.forEach(b=>b.setAttribute("aria-selected",b.dataset.t===k));
    mountAnim(tabs.find(x=>x[0]===k)[2],stage,{autoplay:auto});};
  bs.forEach(b=>b.onclick=()=>show(b.dataset.t,true));
  show(o.tab||"div",!!o.autoplay);
}};

// --- 5.6 Claim / Evidence / Reasoning sorter ---
ANIM.cer={custom(el){
  const cats={c:["Claim","It answers the question."],e:["Evidence","It is data or an observation."],r:["Reasoning","It explains why the evidence supports the claim."],x:["Not strong evidence","It is an opinion or a guess, not data."]};
  const items=[
    ["The seafloor is younger than the continents because it is made at ridges and destroyed at trenches.","c"],
    ["Seafloor rock is 0 years old at the ridge and no older than about 200 million years.","e"],
    ["Dense oceanic crust sinks at trenches, while light continental crust is too buoyant to sink.","r"],
    ["I think the ocean looks young.","x"],
    ["Some continental rocks are nearly 4 billion years old.","e"],
    ["Rock ages increase with distance from the ridge on both sides.","e"]];
  el.innerHTML=`<p class="cap"><strong>Sort the statements.</strong> Tap the part of an argument each one is.</p>`+
    items.map((it,i)=>`<div class="cs" data-i="${i}"><p>${it[0]}</p><div class="row">${Object.entries(cats).map(([k,v])=>`<button type="button" data-c="${k}">${v[0]}</button>`).join("")}</div><p class="res" aria-live="polite"></p></div>`).join("")+
    `<p class="done" hidden>All sorted. You can now build an argument: a claim, two or more pieces of evidence, and reasoning that connects them.</p>`;
  el.querySelectorAll(".cs").forEach(box=>{
    const it=items[box.dataset.i],res=box.querySelector(".res");
    box.querySelectorAll("button").forEach(b=>b.onclick=()=>{
      const c=b.dataset.c;
      if(c===it[1]){
        box.classList.add("ok");box.querySelectorAll("button").forEach(x=>x.disabled=true);b.classList.add("right");
        res.className="res g";res.textContent=`✓ ${cats[c][0]}. ${cats[c][1]}`;
        if(el.querySelectorAll(".cs.ok").length===items.length)el.querySelector(".done").hidden=false;
      }else{
        box.classList.remove("shake");void box.offsetWidth;box.classList.add("shake");
        b.disabled=true;res.className="res a";
        res.textContent=`Not quite. ${cats[c][0]}: ${cats[c][1].toLowerCase()} Does this statement do that?`;
      }
    });
  });
}};

// ===== Practice questions with reteach =====
function mountPractice(el,t,P,st,save,onChange){
  const N=P.qs.length;
  let queue=[],cur=-1,tries=0,done=false,rq=new Set();
  const ok=i=>st.p[i]==="first"||st.p[i]==="later";
  const dots=()=>P.qs.map((_,i)=>`<i class="d ${ok(i)?(st.p[i]==="first"?"f":"l"):st.p[i]==="missed"?"m":""}"></i>`).join("");
  function start(){queue=P.qs.map((_,i)=>i).filter(i=>!ok(i));rq=new Set();next()}
  function next(){
    if(!queue.length){summary();return}
    cur=queue.shift();tries=0;question();
  }
  function question(){
    const q=P.qs[cur];
    el.innerHTML=`<h3>Quick practice</h3><div class="dots" aria-label="Progress">${dots()}</div>
    <p class="pq">${cur+1}. ${q.q}</p><div class="opts" role="group" aria-label="Answer choices">${q.o.map((o,k)=>`<button type="button" class="opt" data-k="${k}">${o}</button>`).join("")}</div>
    <div class="fb" aria-live="polite"></div><div class="reteach" hidden></div><div class="row nxt" hidden><button type="button" class="nb">Next</button></div>`;
    const fb=el.querySelector(".fb"),rt=el.querySelector(".reteach"),nx=el.querySelector(".nxt");
    el.querySelector(".nb").onclick=next;
    el.querySelectorAll(".opt").forEach(b=>b.onclick=()=>{
      const k=+b.dataset.k;
      if(k===q.a){
        b.classList.add("right");el.querySelectorAll(".opt").forEach(x=>x.disabled=true);
        st.p[cur]=(tries===0&&!rq.has(cur))?"first":"later";save();
        fb.className="fb g";fb.textContent="✓ "+(tries===0?"Right! ":"There it is. ")+q.why;
        nx.hidden=false;el.querySelector(".dots").innerHTML=dots();onChange();
      }else{
        tries++;b.disabled=true;b.classList.remove("shake");void b.offsetWidth;b.classList.add("wrong","shake");
        fb.className="fb a";
        if(tries>=2){
          el.querySelectorAll(".opt").forEach(x=>{x.disabled=true;if(+x.dataset.k===q.a)x.classList.add("reveal")});
          st.p[cur]="missed";save();
          fb.textContent=`Not quite. The answer is "${q.o[q.a]}". ${q.why}`;
          if(!rq.has(cur)){rq.add(cur);queue.push(cur);fb.textContent+=" We'll ask this one again in a moment."}
          nx.hidden=false;el.querySelector(".dots").innerHTML=dots();
        }else fb.textContent="Not quite. "+q.f[k]+" Try again.";
        rt.hidden=false;
        rt.innerHTML=`<p class="rth">Let's look at it again</p><p class="tip"><strong>Remember:</strong> ${q.tip}</p><div class="mini"></div>`;
        if(P.anim!=="cer")mountAnim(P.anim,rt.querySelector(".mini"),{from:q.from||0,to:q.to==null?1:q.to,autoplay:true,tab:q.tab});
        else rt.querySelector(".mini").remove();
      }
    });
  }
  function summary(){
    const f=P.qs.filter((_,i)=>st.p[i]==="first").length;
    const miss=P.qs.map((q,i)=>st.p[i]==="missed"?q.q:null).filter(Boolean);
    el.innerHTML=`<h3>Quick practice</h3><div class="dots">${dots()}</div>
    <p class="pq">${f===N?"Perfect run! ":"Practice finished. "}You got ${f} of ${N} on the first try.</p>
    ${miss.length?`<p class="fb a">Ask Ms. Renick about: ${miss.join(" · ")}</p>`:""}
    <div class="row"><button type="button" class="ghost again2">Practice again</button></div>`;
    el.querySelector(".again2").onclick=()=>{st.p={};save();onChange();start()};
    onChange();
  }
  st.p=st.p||{};
  start();
}
