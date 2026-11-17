import {english} from './translations.mjs';
const STORAGE_KEY='lesson3-language';
let language='zh';
if(typeof location!=='undefined'){
 const requested=new URL(location.href).searchParams.get('lang');
 if(requested==='en'||requested==='zh')language=requested;
 else try{language=localStorage.getItem(STORAGE_KEY)==='en'?'en':'zh';}catch{}
}
export const getLanguage=()=>language;
const entries=Object.entries(english).filter(([a,b])=>a!==b).sort((a,b)=>b[0].length-a[0].length);
export function translate(text,lang=language){
 if(lang!=='en'||!text)return text;
 const stripped=text.trim();if(english[stripped])return text.slice(0,text.indexOf(stripped))+english[stripped]+text.slice(text.indexOf(stripped)+stripped.length);
 let value=text
 .replace(/下载 (中文|English) MP4 ↓/g,(_,v)=>`Download ${v==='中文'?'Chinese':v} MP4 ↓`)
 .replace(/(中文|English)文字稿 \/ Transcript ↗/g,(_,v)=>`${v==='中文'?'Chinese':v} transcript ↗`)
 .replace(/正在载入 (中文|English) 配音…/g,(_,v)=>`Loading ${v==='中文'?'Chinese':v} narration…`)
 .replace(/当前配音：(中文|English)([^\n]*)/g,(_,v,extra)=>`Narration: ${v==='中文'?'Chinese':v}${extra}`)
 .replace(/学习记录 · (\d+) \/ 12 已完成/g,'Progress · $1 / 12 completed')
 .replace(/第 (\d+)\/6 对：([^。]+)。当前累计 ([^。]+)。/g,'Pair $1/6: $2. Running sum: $3.')
 .replace(/当前单个 ABCD net：HPWL ([^，]+)，Clique ([^，]+)，Star-from-([A-D]) ([^。]+)。/g,'Current ABCD net: HPWL $1, Clique $2, Star-from-$3 $4. ')
 .replace(/所有点重叠；数值为零不说明布局合法。/g,'All pins overlap; zero does not imply a legal placement.')
 .replace(/它们的数值口径不同，不能直接据此给模型排名。/g,'These models measure different quantities; their values cannot rank the models.')
 .replace(/当前模型值是 ([^。]+)。/g,'The current model value is $1. ')
 .replace(/([A-D]) 的 ([xy]) 坐标/g,'$1 $2 coordinate')
 .replace(/引脚 ([A-D])，坐标 ([^，]+)，方向键移动/g,'Pin $1, coordinates $2, move with arrow keys')
 .replace(/(bbox|clique|star)模型，原点左下，x和y范围0至8/g,'$1 model, origin bottom left, x and y range 0 to 8')
 .replace(/(bbox|clique|star) 网络模型；点坐标见下方输入表/g,'$1 net model; pin coordinates are in the input table below');
 // Longest-first, single-pass matching avoids recursively translating inserted copy.
 const matches=entries.filter(([key])=>value.includes(key));
 if(matches.length){const pattern=new RegExp(matches.map(([key])=>key.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|'),'g');value=value.replace(pattern,key=>english[key]);}
 return value;
}
const originals=new WeakMap(),attributes=new WeakMap();
let observer;
function isOriginal(node){return node.parentElement?.closest('pre,code,script,style,[data-original-language]');}
function textNode(node){
 if(isOriginal(node))return;
 const old=originals.get(node),current=node.nodeValue;
 const source=old&&old.output===current?old.source:current;
 const output=translate(source);originals.set(node,{source,output});if(current!==output)node.nodeValue=output;
}
function element(node){
 if(node.closest('pre,code,script,style,[data-original-language]'))return;
 let values=attributes.get(node);if(!values){values={};attributes.set(node,values);}
 for(const name of ['aria-label','title','placeholder','alt','content']){
  if(!node.hasAttribute(name)||(name==='content'&&!node.matches('meta[name="description"]')))continue;
  const current=node.getAttribute(name),old=values[name],source=old&&current===old.output?old.source:current,output=translate(source);values[name]={source,output};if(current!==output)node.setAttribute(name,output);
 }
}
function scan(root=document){
 if(root.nodeType===Node.TEXT_NODE){textNode(root);return;}
 if(root.nodeType===Node.ELEMENT_NODE)element(root);
 const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT|NodeFilter.SHOW_ELEMENT);
 while(walker.nextNode()){if(walker.currentNode.nodeType===Node.TEXT_NODE)textNode(walker.currentNode);else element(walker.currentNode);}
}
function update(){
 observer?.disconnect();document.documentElement.lang=language==='en'?'en':'zh-CN';
 document.querySelectorAll('[data-site-language]').forEach(el=>{el.hidden=el.dataset.siteLanguage!==language;});
 scan();document.querySelectorAll('[data-language-picker]').forEach(el=>{el.value=language;});
 observer?.observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['aria-label','title','placeholder','alt','content']});
}
export function setLanguage(value){
 if(value!=='zh'&&value!=='en')return;language=value;
 try{localStorage.setItem(STORAGE_KEY,language);}catch{}
 if(typeof history!=='undefined'){const url=new URL(location.href);url.searchParams.set('lang',language);try{history.replaceState(null,'',url);}catch{}}
 update();document.dispatchEvent(new CustomEvent('lessonlanguagechange',{detail:{language}}));
}
if(typeof document!=='undefined'){
 const host=document.querySelector('header .top');
 if(host&&!document.querySelector('[data-language-picker]')){
  const label=document.createElement('label');label.className='site-language';label.innerHTML='<span>界面 / UI</span> <select data-language-picker aria-label="界面语言 / Interface language"><option value="zh">中文</option><option value="en">English</option></select>';host.append(label);
  label.querySelector('select').addEventListener('change',event=>setLanguage(event.target.value));
 }
 observer=new MutationObserver(records=>{observer.disconnect();for(const record of records){if(record.type==='childList')record.addedNodes.forEach(node=>scan(node));else if(record.type==='characterData')textNode(record.target);else element(record.target);}observer.observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['aria-label','title','placeholder','alt','content']});});
 update();
 document.addEventListener('click',event=>{
  const anchor=event.target.closest('a[href]');if(!anchor||anchor.hasAttribute('download'))return;
  const url=new URL(anchor.href,location.href);if(url.origin!==location.origin||!url.pathname.endsWith('/')&&!url.pathname.endsWith('.html'))return;
  url.searchParams.set('lang',language);anchor.href=url.href;
 },{capture:true});
}
