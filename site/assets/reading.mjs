let timer;
document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
 const code=document.getElementById(button.dataset.copy),status=document.getElementById('copy-status');
 try{await navigator.clipboard.writeText(code.textContent);status.textContent='已复制，可粘贴到编辑器中。';}
 catch{const range=document.createRange();range.selectNodeContents(code);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);status.textContent='代码已选中，可使用 Ctrl/Cmd + C 复制。';}
 clearTimeout(timer);timer=setTimeout(()=>{status.textContent='';},4500);
}));
