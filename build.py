# -*- coding: utf-8 -*-
"""Собирает data/section_*.json в один самодостаточный index.html."""
import json, glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data')

sections = []
missing = []
for i in range(18):
    p = os.path.join(DATA, f'section_{i}.json')
    if not os.path.exists(p):
        missing.append(i); continue
    with open(p, encoding='utf-8') as f:
        s = json.load(f)
    s['id'] = i
    sections.append(s)

if missing:
    print('MISSING sections:', missing)

PHASE_META = [
    ('Phase 1', 'Linux + Bash + Git', '#2e7d46'),
    ('Phase 2', 'Docker + Kubernetes', '#1f5fa8'),
    ('Phase 3', 'CI/CD + Terraform + Ansible', '#c07716'),
    ('Phase 4', 'Cloud + Monitoring + Security', '#b23a3a'),
    ('Phase 5', 'SRE Practices', '#6d4fa3'),
]

def phase_idx(name):
    m = re.search(r'Phase (\d)', name)
    return int(m.group(1)) - 1 if m else 0

for s in sections:
    s['pi'] = phase_idx(s.get('phase',''))

payload = json.dumps(sections, ensure_ascii=False).replace('</', '<\\/')

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DevOps / SRE — Учебник</title>
<style>
:root{
  --paper:#f7f5f0; --ink:#23241f; --muted:#6b6a62; --line:#dedbd2;
  --card:#ffffff; --code-bg:#2b2d2a; --code-ink:#e8e6da;
  --p0:#2e7d46; --p1:#1f5fa8; --p2:#c07716; --p3:#b23a3a; --p4:#6d4fa3;
}
*{box-sizing:border-box}
body{margin:0;font-family:Georgia,'Times New Roman',serif;background:var(--paper);color:var(--ink);line-height:1.65}
code,pre,.mono{font-family:Consolas,'JetBrains Mono',Menlo,monospace}
a{color:inherit}
#layout{display:flex;min-height:100vh}
/* Sidebar */
#nav{width:300px;flex-shrink:0;border-right:1px solid var(--line);background:#f0ede5;padding:20px 0;position:sticky;top:0;height:100vh;overflow-y:auto}
#nav h1{font-size:17px;margin:0 20px 4px;letter-spacing:.02em}
#nav .sub{font-size:12px;color:var(--muted);margin:0 20px 18px;font-family:Consolas,monospace}
.phase-group{margin-bottom:6px}
.phase-label{display:flex;align-items:center;gap:8px;padding:8px 20px 4px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-family:Consolas,monospace}
.phase-label .spine{width:14px;height:4px;border-radius:2px}
.nav-item{display:flex;align-items:center;gap:8px;width:100%;text-align:left;border:none;background:none;font:inherit;font-size:14.5px;padding:7px 20px 7px 34px;cursor:pointer;color:var(--ink);border-left:4px solid transparent}
.nav-item:hover{background:#e8e4d8}
.nav-item.active{background:#fff;border-left-color:var(--pc);font-weight:bold}
.nav-item .done-mark{margin-left:auto;font-size:11px;color:var(--muted);font-family:Consolas,monospace}
/* Main */
#main{flex:1;min-width:0;padding:40px 56px 120px;max-width:960px}
.eyebrow{font-family:Consolas,monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--pc)}
h2.section-title{font-size:34px;margin:6px 0 4px;line-height:1.2}
.section-meta{color:var(--muted);font-size:14px;margin-bottom:28px}
/* Topic accordion */
.topic{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--pc);border-radius:4px;margin-bottom:10px;overflow:hidden}
.topic-head{display:flex;align-items:center;gap:12px;padding:13px 18px;cursor:pointer;user-select:none}
.topic-head:hover{background:#fbfaf6}
.topic-num{font-family:Consolas,monospace;font-size:12px;color:var(--muted);min-width:26px}
.topic-title{flex:1;font-size:16.5px}
.topic-level{font-size:11px;font-family:Consolas,monospace;color:var(--muted);white-space:nowrap}
.topic-check{width:18px;height:18px;flex-shrink:0;accent-color:var(--pc)}
.topic-body{display:none;padding:4px 22px 20px 56px;border-top:1px dashed var(--line);font-size:15.5px}
.topic.open .topic-body{display:block}
.topic-body p{margin:.7em 0}
.topic-body code{background:#eceade;padding:1px 5px;border-radius:3px;font-size:.88em}
.topic-body pre{background:var(--code-bg);color:var(--code-ink);padding:14px 16px;border-radius:6px;overflow-x:auto;font-size:13px;line-height:1.5}
.topic-body pre code{background:none;padding:0;color:inherit}
.topic-body table{border-collapse:collapse;margin:.8em 0;font-size:14px}
.topic-body td,.topic-body th{border:1px solid var(--line);padding:5px 10px;text-align:left}
.topic-body th{background:#f0ede5}
/* Quiz */
#quiz-block{margin-top:48px;border-top:3px double var(--line);padding-top:28px}
#quiz-block h3{font-size:24px;margin:0 0 4px}
.q-card{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:18px 22px;margin:14px 0}
.q-text{font-weight:bold;margin-bottom:12px}
.q-num{font-family:Consolas,monospace;color:var(--muted);font-weight:normal;margin-right:8px}
.opt{display:block;padding:8px 12px;margin:6px 0;border:1px solid var(--line);border-radius:4px;cursor:pointer;font-size:15px}
.opt:hover{background:#fbfaf6}
.opt input{margin-right:10px;accent-color:var(--pc)}
.opt.correct{border-color:#2e7d46;background:#eef6ef}
.opt.wrong{border-color:#b23a3a;background:#faeeee}
.q-explain{display:none;margin-top:10px;font-size:14px;color:var(--muted);border-left:3px solid var(--pc);padding-left:12px}
.q-card.answered .q-explain{display:block}
#quiz-actions{margin-top:24px;display:flex;gap:14px;align-items:center}
button.primary{font:inherit;font-size:15px;background:var(--ink);color:#fff;border:none;padding:11px 26px;border-radius:4px;cursor:pointer}
button.primary:hover{opacity:.88}
button.ghost{font:inherit;font-size:14px;background:none;border:1px solid var(--line);padding:10px 20px;border-radius:4px;cursor:pointer;color:var(--muted)}
#quiz-result{font-size:17px;font-weight:bold}
/* Dashboard */
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-top:28px}
.book{background:var(--card);border:1px solid var(--line);border-left:10px solid var(--pc);border-radius:4px;padding:16px 18px;cursor:pointer}
.book:hover{box-shadow:0 2px 10px rgba(0,0,0,.08)}
.book .bp{font-family:Consolas,monospace;font-size:11px;color:var(--pc);letter-spacing:.12em;text-transform:uppercase}
.book h4{margin:6px 0 8px;font-size:17px}
.bar{height:6px;background:#eceade;border-radius:3px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--pc)}
.book .stats{font-size:12px;color:var(--muted);font-family:Consolas,monospace;margin-top:7px}
.hero-eyebrow{font-family:Consolas,monospace;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
h2.hero{font-size:40px;margin:8px 0 10px;line-height:1.15}
.hero-sub{color:var(--muted);font-size:16px;max-width:620px}
#menu-btn{display:none}
@media(max-width:860px){
  #nav{position:fixed;z-index:20;transform:translateX(-100%);transition:transform .2s}
  #nav.open{transform:none}
  #menu-btn{display:block;position:fixed;top:12px;left:12px;z-index:30;font:inherit;background:var(--ink);color:#fff;border:none;border-radius:4px;padding:8px 14px}
  #main{padding:64px 20px 100px}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<button id="menu-btn" onclick="document.getElementById('nav').classList.toggle('open')">☰ Разделы</button>
<div id="layout">
  <nav id="nav"></nav>
  <main id="main"></main>
</div>
<script>
const DATA = __PAYLOAD__;
const PHASES = __PHASES__;
const LS = 'devops-learn-v1';
let state = JSON.parse(localStorage.getItem(LS) || '{"read":{},"quiz":{}}');
function save(){ localStorage.setItem(LS, JSON.stringify(state)); }
function esc(s){ const d=document.createElement('div'); d.textContent=s; return d.innerHTML; }

function sectionProgress(s){
  const read = s.topics.filter((_,ti)=>state.read[s.id+':'+ti]).length;
  return {read, total:s.topics.length, quiz: state.quiz[s.id]};
}

function renderNav(active){
  const nav = document.getElementById('nav');
  let h = '<h1>DevOps / SRE</h1><p class="sub">учебник · '+DATA.length+' разделов</p>';
  h += '<button class="nav-item" style="--pc:#555" onclick="showDash()"'+(active===-1?' aria-current="page"':'')+'>🏠 Обзор</button>';
  PHASES.forEach((ph,pi)=>{
    const secs = DATA.filter(s=>s.pi===pi);
    if(!secs.length) return;
    h += '<div class="phase-group"><div class="phase-label"><span class="spine" style="background:'+ph[2]+'"></span>'+ph[0]+' · '+ph[1]+'</div>';
    secs.forEach(s=>{
      const p = sectionProgress(s);
      const mark = p.read===p.total ? '✓' : p.read+'/'+p.total;
      h += '<button class="nav-item'+(active===s.id?' active':'')+'" style="--pc:'+ph[2]+'" onclick="showSection('+s.id+')">'+esc(s.section)+'<span class="done-mark">'+mark+'</span></button>';
    });
    h += '</div>';
  });
  nav.innerHTML = h;
}

function showDash(){
  renderNav(-1);
  const total = DATA.reduce((a,s)=>a+s.topics.length,0);
  const read = Object.keys(state.read).filter(k=>state.read[k]).length;
  let h = '<p class="hero-eyebrow">трекер обучения · '+total+' тем · 5 фаз</p>';
  h += '<h2 class="hero">Путь DevOps / SRE инженера</h2>';
  h += '<p class="hero-sub">От файловой системы Linux до chaos engineering. Читайте темы, отмечайте изученное и закрепляйте тестом в конце каждого раздела. Прогресс сохраняется в браузере.</p>';
  h += '<p class="mono" style="color:var(--muted)">Изучено тем: '+read+' / '+total+'</p>';
  h += '<div class="shelf">';
  DATA.forEach(s=>{
    const ph = PHASES[s.pi], p = sectionProgress(s);
    const pct = Math.round(100*p.read/p.total);
    const qz = p.quiz ? 'тест: '+p.quiz.score+'/'+p.quiz.total : 'тест не пройден';
    h += '<div class="book" style="--pc:'+ph[2]+'" onclick="showSection('+s.id+')"><div class="bp">'+ph[0]+'</div><h4>'+esc(s.section)+'</h4><div class="bar"><i style="width:'+pct+'%"></i></div><div class="stats">'+p.read+'/'+p.total+' тем · '+qz+'</div></div>';
  });
  h += '</div>';
  document.getElementById('main').innerHTML = h;
  window.scrollTo(0,0);
  document.getElementById('nav').classList.remove('open');
}

function showSection(id){
  const s = DATA.find(x=>x.id===id); if(!s) return;
  renderNav(id);
  const ph = PHASES[s.pi];
  let h = '<p class="eyebrow" style="--pc:'+ph[2]+'">'+ph[0]+' — '+ph[1]+'</p>';
  h += '<h2 class="section-title">'+esc(s.section)+'</h2>';
  h += '<p class="section-meta">'+s.topics.length+' тем · тест из '+s.quiz.length+' вопросов в конце</p>';
  s.topics.forEach((t,ti)=>{
    const key = s.id+':'+ti, checked = state.read[key] ? 'checked' : '';
    h += '<div class="topic" style="--pc:'+ph[2]+'" id="t'+ti+'">'
      + '<div class="topic-head" onclick="toggleTopic('+ti+')">'
      + '<span class="topic-num">'+String(ti+1).padStart(2,'0')+'</span>'
      + '<span class="topic-title">'+esc(t.title)+'</span>'
      + '<span class="topic-level">'+esc(t.level)+'</span>'
      + '<input type="checkbox" class="topic-check" '+checked+' onclick="event.stopPropagation();markRead('+s.id+','+ti+',this.checked)" title="отметить изученным">'
      + '</div><div class="topic-body">'+t.explanation+'</div></div>';
  });
  h += '<div id="quiz-block" style="--pc:'+ph[2]+'"><h3>Проверьте себя</h3><p class="section-meta">Выберите ответы и нажмите «Проверить».</p>';
  s.quiz.forEach((q,qi)=>{
    h += '<div class="q-card" data-a="'+q.answer+'" id="q'+qi+'"><div class="q-text"><span class="q-num">'+(qi+1)+'.</span>'+esc(q.q)+'</div>';
    q.options.forEach((o,oi)=>{
      h += '<label class="opt"><input type="radio" name="q'+qi+'" value="'+oi+'">'+esc(o)+'</label>';
    });
    h += '<div class="q-explain">'+esc(q.explain)+'</div></div>';
  });
  h += '<div id="quiz-actions"><button class="primary" onclick="gradeQuiz('+s.id+')">Проверить</button>'
    + '<button class="ghost" onclick="showSection('+s.id+')">Сбросить тест</button>'
    + '<span id="quiz-result"></span></div></div>';
  document.getElementById('main').innerHTML = h;
  window.scrollTo(0,0);
  document.getElementById('nav').classList.remove('open');
}

function toggleTopic(ti){ document.getElementById('t'+ti).classList.toggle('open'); }
function markRead(sid,ti,v){ state.read[sid+':'+ti]=v; save(); renderNav(sid); }

function gradeQuiz(sid){
  const s = DATA.find(x=>x.id===sid);
  let score=0;
  s.quiz.forEach((q,qi)=>{
    const card = document.getElementById('q'+qi);
    card.classList.add('answered');
    const sel = card.querySelector('input:checked');
    const opts = card.querySelectorAll('.opt');
    opts[q.answer].classList.add('correct');
    if(sel){
      const v = +sel.value;
      if(v===q.answer) score++;
      else opts[v].classList.add('wrong');
    }
  });
  state.quiz[sid] = {score, total:s.quiz.length}; save();
  const pct = Math.round(100*score/s.quiz.length);
  document.getElementById('quiz-result').textContent =
    'Результат: '+score+' / '+s.quiz.length+' ('+pct+'%)'+(pct>=80?' — отлично!':pct>=60?' — неплохо, повторите слабые темы':' — стоит перечитать раздел');
  renderNav(sid);
}

showDash();
</script>
</body>
</html>
"""

phases_js = json.dumps(PHASE_META, ensure_ascii=False)
html = html.replace('__PAYLOAD__', payload).replace('__PHASES__', phases_js)

out = os.path.join(ROOT, 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print('Wrote', out, len(html)//1024, 'KB,', len(sections), 'sections')
