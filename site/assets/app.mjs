import {evaluate,PRESETS} from './models.mjs';
import {diagram} from './draw.mjs';
const $=s=>document.querySelector(s),copy=p=>p.map(x=>({...x})),fmt=n=>Number(n.toFixed(2)).toString();
const KEY='placement03-progress-v1';let progress={},storage=true;
try{const p=JSON.parse(localStorage.getItem(KEY)||'{}');if(p&&typeof p==='object'&&!Array.isArray(p))progress=p;}catch{storage=false;}
function save(){try{localStorage.setItem(KEY,JSON.stringify(progress));}catch{storage=false;}updateProgress();}
function updateProgress(){$('#progress').textContent=`学习记录 · ${Object.values(progress).filter(v=>v===true).length} / 12 已完成`;$('#storage-status').textContent=storage?'记录只保存在此浏览器，不上传个人数据。':'浏览器存储不可用，本次学习仍可继续；关闭页面后记录可能丢失。';}
let reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function motion(){document.body.classList.toggle('reduced',reduced);$('#motion').setAttribute('aria-pressed',String(reduced));$('#motion').textContent=reduced?'减少动态：开':'减少动态';stopSteps();}
$('#motion').addEventListener('click',()=>{reduced=!reduced;motion();});
let step=0,timer=null;function stopSteps(){clearInterval(timer);timer=null;$('#step-play').textContent='自动演示';$('#step-play').setAttribute('aria-pressed','false');}
function renderStep(){const r=evaluate(PRESETS.golden,'A'),shown=r.pairs.slice(0,step),sum=shown.reduce((s,e)=>s+e.value,0);$('#step-diagram').innerHTML=diagram(PRESETS.golden,'clique','A',step);$('#step-copy').textContent=step?`第 ${step}/6 对：${shown.at(-1).from}–${shown.at(-1).to} = ${shown.at(-1).value}。当前累计 ${shown.map(e=>e.value).join(' + ')} = ${sum}。`:'从 0 开始。每次只加入一对引脚，不要把 A–B 和 B–A 算两次。';$('#trace-list').innerHTML=r.pairs.map((e,i)=>`<li class="${i<step?'active':''}">${e.from}–${e.to} : ${i<step?e.value:'待计算'}</li>`).join('');$('#step-back').disabled=step===0;$('#step-next').disabled=step===6;}
$('#step-next').onclick=()=>{stopSteps();step=Math.min(6,step+1);renderStep();};$('#step-back').onclick=()=>{stopSteps();step=Math.max(0,step-1);renderStep();};$('#step-reset').onclick=()=>{stopSteps();step=0;renderStep();};
$('#step-play').onclick=()=>{if(timer){stopSteps();return;}if(reduced){step=Math.min(6,step+1);renderStep();return;}if(step===6)step=0;$('#step-play').textContent='暂停';$('#step-play').setAttribute('aria-pressed','true');timer=setInterval(()=>{step++;renderStep();if(step===6)stopSteps();},1300);};
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopSteps();});
$('#hero-diagram').innerHTML=diagram(PRESETS.golden,'bbox');
let preset='golden',pins=copy(PRESETS.golden),hub='A',drag=null;
$('#coordinates').innerHTML=`<table><thead><tr><th>引脚</th><th>x</th><th>y</th></tr></thead><tbody>${pins.map(p=>`<tr><th scope="row">${p.id}</th>${['x','y'].map(axis=>`<td><input type="number" min="0" max="8" step="1" data-id="${p.id}" data-axis="${axis}" aria-label="${p.id} 的 ${axis} 坐标" value="${p[axis]}"></td>`).join('')}</tr>`).join('')}</tbody></table>`;
function renderLab(){const r=evaluate(pins,hub);$('#boards').innerHTML=[['bbox','BBox / HPWL','半周长 · 宽 + 高','gold'],['clique','Clique','6 对引脚 · 每对一次','blue'],['star',`Star / ${hub}`,'3 条辐条 · 现有引脚中心','teal']].map(([kind,name,sub,color])=>`<article class="board"><div class="board-head"><h3 class="${color}">${name}</h3><output class="readout ${color}">${fmt(r[kind])}</output></div><small>${sub}</small>${diagram(pins,kind,hub,Infinity,true)}</article>`).join('');
 $('#contributions').innerHTML=`<p><strong>BBox</strong>　(${r.box.maxX}−${r.box.minX}) + (${r.box.maxY}−${r.box.minY}) = ${fmt(r.bbox)}</p><p><strong>Clique</strong>　${r.pairs.map(e=>`${e.from}${e.to}:${fmt(e.value)}`).join(' / ')} → ${fmt(r.clique)}</p><p><strong>Star ${hub}</strong>　${r.spokes.map(e=>`${e.from}${e.to}:${fmt(e.value)}`).join(' / ')} → ${fmt(r.star)}</p>`;
 for(const input of $('#coordinates').querySelectorAll('input'))input.value=pins.find(p=>p.id===input.dataset.id)[input.dataset.axis];
 $('#lab-summary').textContent=`当前单个 ABCD net：HPWL ${fmt(r.bbox)}，Clique ${fmt(r.clique)}，Star-from-${hub} ${fmt(r.star)}。${r.bbox===0?'所有点重叠；数值为零不说明布局合法。':'它们的数值口径不同，不能直接据此给模型排名。'}`;
}
function load(key,scroll=false){preset=key;pins=copy(PRESETS[key]);hub='A';$('#preset').value=key;$('#hub').value='A';$('#input-status').textContent='';renderLab();if(scroll)$('#lab').scrollIntoView({behavior:reduced?'instant':'smooth'});}
$('#preset').onchange=e=>load(e.target.value);$('#hub').onchange=e=>{hub=e.target.value;renderLab();};$('#reset-lab').onclick=()=>load(preset);
$('#coordinates').addEventListener('change',e=>{const i=e.target;if(!i.matches('input'))return;const v=Number(i.value);if(i.value.trim()===''||!Number.isInteger(v)||v<0||v>8){$('#input-status').textContent='请输入 0–8 的整数；本次无效输入未应用。';i.setAttribute('aria-invalid','true');return;}i.removeAttribute('aria-invalid');pins.find(p=>p.id===i.dataset.id)[i.dataset.axis]=v;$('#input-status').textContent='坐标已更新，三幅图已同步。';renderLab();});
$('#boards').addEventListener('pointerdown',e=>{const el=e.target.closest('[data-pin]');if(!el)return;const svg=el.closest('svg'),rect=svg.getBoundingClientRect();drag={id:el.dataset.pin,rect,pointer:e.pointerId};e.preventDefault();});
window.addEventListener('pointermove',e=>{if(!drag||drag.pointer!==e.pointerId)return;const x=(e.clientX-drag.rect.left)/drag.rect.width*330,y=(e.clientY-drag.rect.top)/drag.rect.height*335,p=pins.find(p=>p.id===drag.id);p.x=Math.max(0,Math.min(8,Math.round((x-40)/30)));p.y=Math.max(0,Math.min(8,Math.round((290-y)/30)));renderLab();});
for(const event of ['pointerup','pointercancel','blur'])window.addEventListener(event,()=>{drag=null;});
$('#boards').addEventListener('keydown',e=>{const el=e.target.closest('[data-pin]');if(!el||!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key))return;e.preventDefault();const index=[...$('#boards').children].indexOf(el.closest('.board')),p=pins.find(p=>p.id===el.dataset.pin),axis=['ArrowLeft','ArrowRight'].includes(e.key)?'x':'y',delta=['ArrowRight','ArrowUp'].includes(e.key)?1:-1;p[axis]=Math.max(0,Math.min(8,p[axis]+delta));const id=p.id;renderLab();$('#boards').children[index].querySelector(`[data-pin="${id}"]`).focus({preventScroll:true});});
document.querySelectorAll('[data-load]').forEach(b=>b.onclick=()=>load(b.dataset.load,true));$('#collapse').onclick=()=>{pins=pins.map(p=>({...p,x:4,y:4}));renderLab();$('#lab').scrollIntoView({behavior:reduced?'instant':'smooth'});};
const tasks=[
 ['标准图的半周长','载入标准正方形。预测宽加高，而不是整圈周长。','golden',()=>evaluate(pins,hub).bbox,4,'宽 2 加高 2，HPWL = 4。'],
 ['不重复的六对引脚','载入标准正方形。预测 Clique 的总和。','golden',()=>evaluate(pins,hub).clique,16,'六项为 2、2、4、4、2、2，总和 16。'],
 ['把中心换成 B','载入非对称图，再将 Star 中心设成 B。预测三条辐条的总和。','asymmetric',()=>hub==='B'?evaluate(pins,hub).star:null,22,'BA = 6，BC = 7，BD = 9，所以是 22。'],
 ['移动内部点','载入内部点预设，再把 D 改成 (2,2)。预测此时的 HPWL。','interior',()=>{const d=pins.find(p=>p.id==='D');return d.x===2&&d.y===2?evaluate(pins,hub).bbox:null;},16,'A、B、C 仍支撑 8×8 包围盒，HPWL 仍是 16。'],
 ['四个引脚有几对？','不区分方向，AB 与 BA 视作同一对。共有几对？','golden',()=>evaluate(pins,hub).pairs.length,6,'组合数 4×3÷2 = 6。'],
 ['哪个中心更省？','载入非对称图，分别更换四个 Star 中心。四个读数中的最小值是多少？','asymmetric',()=>Math.min(...pins.map(p=>evaluate(pins,p.id).star)),14,'A/B/C/D 分别为 16/22/14/20；本例中心 C 最小，为 14。']
];
$('#challenges').innerHTML=tasks.map(([title,prompt,key],i)=>`<form class="exercise" data-task="${i}"><h4>${String(i+1).padStart(2,'0')} / ${title}</h4><p>${prompt}</p><button type="button" data-task-load="${i}">载入题目情境</button><label for="answer-${i}">我的预测数值</label><div class="answer-row"><input id="answer-${i}" type="number" step="any" required><button type="submit">提交检查</button></div><p class="feedback" role="status"></p></form>`).join('');
document.querySelectorAll('[data-task-load]').forEach(b=>b.onclick=()=>{load(tasks[Number(b.dataset.taskLoad)][2],true);});
function feedback(el,ok,text){el.textContent=(ok?'✓ ':'再想一想：')+text;el.className='feedback '+(ok?'good':'bad');}
document.querySelectorAll('[data-task]').forEach(form=>form.onsubmit=e=>{e.preventDefault();const i=Number(form.dataset.task),t=tasks[i],actual=t[3](),prediction=Number(form.querySelector('input').value),expected=t[4];const ids=PRESETS[t[2]],context=t[0]==='移动内部点'?pins.every(p=>p.id==='D'||ids.some(q=>q.id===p.id&&q.x===p.x&&q.y===p.y)):pins.every(p=>ids.some(q=>q.id===p.id&&q.x===p.x&&q.y===p.y));const ok=context&&actual!==null&&Math.abs(actual-expected)<1e-8&&Math.abs(prediction-actual)<1e-8;feedback(form.querySelector('.feedback'),ok,ok?t[5]:!context||actual===null?'请先设置题目要求的坐标或中心，再提交。':`当前模型值是 ${fmt(actual)}。${t[5]}`);if(ok){progress['task'+i]=true;save();}});
const quiz=[
 ['HPWL 的“半”是什么意思？',['包围盒宽加高','包围盒的面积','四条边的总长'],0,'包围盒周长是 2(宽+高)，HPWL 只取宽+高。'],
 ['为什么 Clique 只算 i<j？',['忽略短边','每个无序引脚对只计一次','为了选出中心'],1,'AB 与 BA 是同一无向引脚对，不重复计数。'],
 ['标准图四个 Star 中心的值相同，能推出什么？',['任何图换中心都不变','Star 总是最优布线','本例对称，不能推广到所有输入'],2,'对称性只解释当前图；非对称反例中各中心的值不同。'],
 ['所有引脚重叠，三模型为零，说明什么？',['连接测量为零，但未验证布局合法性','真实芯片布局已完成','时序一定最优'],0,'线长模型未检查单元面积、重叠、密度和时序。'],
 ['同图得到 4、16、8，能直接断言哪把尺子更好？',['4 最小所以 BBox 最好','16 最大所以 Clique 最差','不能，它们测量口径不同'],2,'应先对齐模型、权重和约束，再比较布局候选。'],
 ['本课 Star-from-A 的中心在哪里？',['任意虚拟中心','现有引脚 A','包围盒几何中心'],1,'本课固定使用现有 pin 作 hub。虚拟中心是另一个模型约定。']
];
$('#quiz').innerHTML=quiz.map(([q,options],i)=>`<form class="exercise" data-quiz="${i}"><h4>${i+1}. ${q}</h4>${options.map((o,j)=>`<label><input type="radio" name="q${i}" value="${j}" required style="width:auto;margin-right:8px">${o}</label>`).join('')}<button type="submit">检查与解释</button><p class="feedback" role="status"></p></form>`).join('');
document.querySelectorAll('[data-quiz]').forEach(f=>f.onsubmit=e=>{e.preventDefault();const i=Number(f.dataset.quiz),v=Number(new FormData(f).get('q'+i)),ok=v===quiz[i][2];feedback(f.querySelector('.feedback'),ok,quiz[i][3]);if(ok){progress['quiz'+i]=true;save();}});
$('#clear-progress').onclick=()=>{progress={};save();document.querySelectorAll('.feedback').forEach(p=>{p.textContent='';});document.querySelectorAll('.exercise').forEach(f=>f.reset());};
const video=$('#lesson-video');$('#video-speed').onchange=e=>{video.playbackRate=Number(e.target.value);};video.addEventListener('error',()=>{$('#video-status').textContent='播放器暂时无法载入。可以下载 MP4，或阅读完整文字稿继续学习。';});
fetch('media/chapters.json').then(r=>{if(!r.ok)throw Error('chapters');return r.json();}).then(chapters=>{$('#chapters').innerHTML=chapters.map((c,i)=>`<button data-chapter="${i}"><span>${Math.floor(c.start/60)}:${String(Math.floor(c.start%60)).padStart(2,'0')}</span>${c.title}</button>`).join('');$('#chapters').querySelectorAll('button').forEach((b,i)=>b.onclick=()=>{video.currentTime=chapters[i].start;video.play().catch(()=>{$('#video-status').textContent='章节已定位，点击播放器开始。';});});}).catch(()=>{$('#chapters').textContent='章节暂时无法读取，请使用播放器进度条。';});
motion();renderStep();renderLab();updateProgress();
