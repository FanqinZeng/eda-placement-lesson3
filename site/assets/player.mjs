/** Keep the same authored scene and its relative progress across voice timelines. */
export function mapPlaybackTime(time,from,to){
 if(!Number.isFinite(time)||time<=0||!from?.length||!to?.length)return 0;
 if(time>=from.at(-1).end)return to.at(-1).end;
 const i=from.findIndex(s=>time<s.end);if(i<0||!to[i])return 0;
 const a=from[i],b=to[i],fraction=Math.max(0,Math.min(1,(time-a.start)/(a.end-a.start)));
 return b.start+(b.end-b.start)*fraction;
}
export async function initLessonPlayer(root=document){
 const $=s=>root.querySelector(s),video=$('#lesson-video'),select=$('#voice-language'),track=$('#lesson-captions');
 let versions,active='zh',request=0,pending=null,captionChoice='bilingual';
 const captionSelect=$('#caption-mode');
 function captionSource(lang){return versions[lang].captionTracks[captionChoice==='off'?'bilingual':captionChoice];}
 function applyCaption(lang){
  track.src=captionSource(lang);track.srclang=captionChoice==='bilingual'?'mul':captionChoice==='en'?'en-US':'zh-CN';
  track.label=captionChoice==='bilingual'?'中英双语 / Chinese + English':captionChoice==='en'?'English captions':'中文字幕';
  track.track.mode=captionChoice==='off'?'disabled':'showing';
 }
 const status=$('#video-language-status');select.disabled=true;
 $('#video-speed').onchange=e=>{video.playbackRate=Number(e.target.value);if(pending)pending.speed=video.playbackRate;};
 video.addEventListener('error',()=>{$('#video-status').textContent='播放器暂时无法载入。可以下载当前语言 MP4，或阅读文字稿继续学习。';});
 function resources(lang){
  const v=versions[lang];$('#download-video').href=v.video;$('#download-video').textContent=`下载 ${v.label} MP4 ↓`;
  $('#download-captions').href=captionSource(lang);$('#download-captions').textContent=`${captionChoice==='zh'?'中文字幕':captionChoice==='en'?'English captions':v.trackLabel} VTT ↓`;
  $('#video-transcript').href=v.transcript;$('#video-transcript').textContent=`${v.label}文字稿 / Transcript ↗`;
  $('#chapters').innerHTML=v.chapters.map((c,i)=>`<button data-chapter="${i}"><span>${Math.floor(c.start/60)}:${String(Math.floor(c.start%60)).padStart(2,'0')}</span>${c.title}</button>`).join('');
  $('#chapters').querySelectorAll('button').forEach((button,i)=>button.onclick=()=>{
   const t=v.chapters[i].start;if(pending){pending.time=t;pending.resume=true;return;}
   video.currentTime=t;const chapterRequest=request;video.play().catch(()=>{if(chapterRequest!==request)return;$('#video-status').textContent='章节已定位，点击播放器开始。';});
  });
 }
 function switchVoice(lang){
  if(!versions[lang])return;
  const token=++request,from=pending?.lang||active,time=pending?.time??video.currentTime;
  const state={lang,time:mapPlaybackTime(time,versions[from].scenes,versions[lang].scenes),resume:pending?.resume??!video.paused,speed:pending?.speed??video.playbackRate,captionMode:pending?.captionMode??track.track?.mode??'showing'};
  pending=state;video.pause();resources(lang);status.textContent=`正在载入 ${versions[lang].label} 配音…`;$('#video-status').textContent='';
  for(const t of video.textTracks)t.mode='disabled';
  applyCaption(lang);
  video.poster=versions[lang].poster;
  video.addEventListener('loadedmetadata',()=>{
   if(token!==request)return;
   active=lang;video.dataset.language=lang;video.currentTime=Math.min(state.time,Math.max(0,video.duration-.01));video.playbackRate=state.speed;
   if(track.track)track.track.mode=state.captionMode;select.value=lang;status.textContent=`当前配音：${versions[lang].label} · ${versions[lang].voice}`;pending=null;
   if(state.resume)video.play().catch(()=>{if(token!==request)return;$('#video-status').textContent='语言已切换，点击播放器继续播放。';});
  },{once:true});
  video.src=versions[lang].video;video.load();
 }
 try{
  const r=await fetch('media/versions.json');if(!r.ok)throw Error('versions');versions=await r.json();
  resources('zh');applyCaption('zh');video.dataset.language='zh';status.textContent=`当前配音：中文 · ${versions.zh.voice}`;select.disabled=false;
  select.onchange=e=>switchVoice(e.target.value);
  if(captionSelect)captionSelect.onchange=e=>{captionChoice=e.target.value;applyCaption(pending?.lang||active);resources(pending?.lang||active);if(pending)pending.captionMode=captionChoice==='off'?'disabled':'showing';};
  // Interface changes select the matching rendered film, including its pictures.
  // The voice picker can still override that choice independently afterwards.
  root.addEventListener('lessonlanguagechange',e=>{
   const lang=e.detail.language;if(versions[lang]&&lang!==(pending?.lang||active))switchVoice(lang);
  });
  if(root.documentElement.lang.startsWith('en'))switchVoice('en');
 }catch{status.textContent='双语切换资料暂时无法载入；下方可分别下载中文和英文成片。';}
}
