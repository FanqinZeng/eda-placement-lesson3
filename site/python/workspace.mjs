import {EXAMPLES, RUN_TIMEOUT_MS, LIVE_DEBOUNCE_MS} from './examples.mjs';
const $ = id => document.getElementById(id);
const copy = {
 zh:{back:'返回课程',language:'语言',title:'实时 Python 实验室',intro:'亲手修改三种线网模型，用真正的 Python 立即验证结果。',runtime:'CPython 在浏览器的独立 Worker 中运行。首次加载约 12 MB 本地运行时；无需安装 Python。',expected:'黄金样例：BBox = 4，Clique = 16，Star = 8。坐标使用曼哈顿距离，Star 默认以第一个引脚为中心。',example:'代码样例',reference:'参考实现 · 黄金样例',asymmetric:'非对称引脚',exercise:'练习模板',run:'运行',stop:'停止 / 重启',reset:'恢复所选样例',live:'实时运行',editor:'Python 编辑器',help:'可修改任意代码；Tab 插入四个空格。实时运行会在停止输入 0.7 秒后执行。每次执行使用新的变量空间。',output:'运行结果',stdout:'标准输出',errors:'错误与诊断',limits:'单次运行限时 5 秒。停止或超时会重启解释器，并保留代码和已有输出。支持 Python 标准库；不预装第三方包。',privacy:'代码只在当前浏览器执行；编辑内容保存在本机浏览器。选择其他样例或恢复样例会替换编辑器内容。',loading:'正在加载 Python…',ready:'Python 就绪',running:'正在执行…',done:'执行完成',error:'执行出错',failed:'加载失败：请重启重试',stopped:'已停止；正在重启…',timeout:'执行超过 5 秒，已停止并重启解释器。',stopMessage:'已停止运行。代码与已有输出已保留。',loadTimeout:'Python 加载超时，请检查网络或重新加载页面。'},
 en:{back:'Back to lesson',language:'Language',title:'Live Python Lab',intro:'Edit three net models and verify the results with real Python.',runtime:'CPython runs in a separate browser Worker. The first load fetches about 12 MB of bundled runtime files; no Python installation is required.',expected:'Golden example: BBox = 4, Clique = 16, Star = 8. All distances are Manhattan; Star uses the first pin as its hub by default.',example:'Example',reference:'Reference · Golden pins',asymmetric:'Asymmetric pins',exercise:'Exercise template',run:'Run',stop:'Stop / Restart',reset:'Reset selected example',live:'Live run',editor:'Python editor',help:'Edit any code; Tab inserts four spaces. Live run executes 0.7 seconds after typing stops. Each run gets a fresh variable namespace.',output:'Results',stdout:'Standard output',errors:'Errors & diagnostics',limits:'Each run has a 5-second limit. Stop or timeout restarts the interpreter and keeps your code and existing output. Python standard library is available; third-party packages are not preinstalled.',privacy:'Code executes only in this browser; edits are saved in this browser on your device. Selecting or resetting an example replaces the editor contents.',loading:'Loading Python…',ready:'Python ready',running:'Running…',done:'Finished',error:'Execution error',failed:'Loading failed: restart to retry',stopped:'Stopped; restarting…',timeout:'Execution exceeded 5 seconds. The interpreter was stopped and restarted.',stopMessage:'Execution stopped. Code and existing output were retained.',loadTimeout:'Python loading timed out. Check your connection or reload the page.'}
};
function readSaved(key) {try{return localStorage.getItem(key)}catch{return null}}
function save(key,value) {try{localStorage.setItem(key,value)}catch{/* Storage can be disabled. */}}
let language = new URLSearchParams(location.search).get('lang') || readSaved('lesson3-language') || 'zh';
let statusKey = 'loading';
let version = '';
function translate() {
 const t=copy[language];
 document.documentElement.lang=language === 'zh' ? 'zh-CN' : 'en';
 document.title=`${t.title} · Placement Lesson 3`;
 for(const node of document.querySelectorAll('[data-i18n]')) node.textContent=t[node.dataset.i18n];
 $('language').value=language;
 $('back').href=`../?lang=${language}`;
 $('status').textContent=t[statusKey]+(version && statusKey==='ready' ? ` · CPython ${version}` : '');
}
function setStatus(key) {statusKey=key;translate()}
function setLanguage(value) {
 language=value === 'en' ? 'en' : 'zh';save('lesson3-language',language);
 const url=new URL(location.href);url.searchParams.set('lang',language);history.replaceState(null,'',url);translate();
}
setLanguage(language);
$('language').addEventListener('change',e=>setLanguage(e.target.value));
$('code').value=readSaved('lesson3-python-code') ?? EXAMPLES.reference;
let worker=null, ready=false, running=false, runId=0, activeId=null;
let executionTimer=null, startupTimer=null, debounceTimer=null, pendingRun=false;
function appendError(message) {$('errors').textContent+=($('errors').textContent ? '\n' : '')+message}
function updateButtons() {$('run').disabled=!ready || running;$('code').setAttribute('aria-busy',String(running))}
function clearTimers() {clearTimeout(executionTimer);clearTimeout(startupTimer)}
function launch() {
 clearTimers();worker?.terminate();ready=false;running=false;activeId=null;updateButtons();
 setStatus('loading');
 const current = new Worker(new URL('./worker.mjs',import.meta.url),{type:'module'});worker=current;
 startupTimer=setTimeout(()=>{if(worker!==current)return;current.terminate();pendingRun=false;appendError(copy[language].loadTimeout);setStatus('failed')},60000);
 current.onmessage=({data})=>{
  if(worker!==current)return;
  if(data.type==='ready') {clearTimeout(startupTimer);version=data.version;ready=true;setStatus('ready');updateButtons();if(pendingRun){pendingRun=false;run()}return}
  if(data.type==='init-error'){clearTimeout(startupTimer);pendingRun=false;appendError(data.error);setStatus('failed');return}
  if(data.id!==activeId)return;
  if(data.type==='output') {const target=$(data.kind==='stderr'?'errors':'output');target.textContent+=data.text;return}
  if(data.type==='done'||data.type==='error'){
   clearTimeout(executionTimer);running=false;activeId=null;
   if(data.type==='error')appendError(data.error);
   setStatus(data.type==='error'?'error':'done');updateButtons();
  }
 };
 current.onerror=(event)=>{if(worker!==current)return;event.preventDefault();clearTimers();current.terminate();ready=false;running=false;pendingRun=false;appendError(event.message);setStatus('failed');updateButtons()};
}
function stop(reason='stopMessage') {
 clearTimeout(debounceTimer);pendingRun=false;appendError(copy[language][reason]);launch();
}
function run() {
 clearTimeout(debounceTimer);
 if(!ready){pendingRun=true;return}
 if(running){pendingRun=true;launch();return}
 running=true;activeId=++runId;$('output').textContent='';$('errors').textContent='';setStatus('running');updateButtons();
 executionTimer=setTimeout(()=>stop('timeout'),RUN_TIMEOUT_MS);
 worker.postMessage({type:'run',id:activeId,code:$('code').value});
}
function edited() {save('lesson3-python-code',$('code').value);clearTimeout(debounceTimer);if($('live').checked)debounceTimer=setTimeout(run,LIVE_DEBOUNCE_MS)}
$('run').addEventListener('click',run);
$('stop').addEventListener('click',()=>stop());
$('code').addEventListener('input',edited);
$('code').addEventListener('keydown',event=>{
 if((event.ctrlKey||event.metaKey)&&event.key==='Enter'){event.preventDefault();run()}
 if(event.key==='Tab'&&!event.shiftKey){event.preventDefault();const e=event.target;const start=e.selectionStart;e.setRangeText('    ',start,e.selectionEnd,'end');edited()}
});
function exampleChanged() {$('code').value=EXAMPLES[$('example').value];edited()}
$('example').addEventListener('change',exampleChanged);
$('reset').addEventListener('click',exampleChanged);
$('live').addEventListener('change',()=>{clearTimeout(debounceTimer);if($('live').checked)run()});
window.addEventListener('pagehide',()=>{clearTimeout(debounceTimer);clearTimers();worker?.terminate()});
launch();
