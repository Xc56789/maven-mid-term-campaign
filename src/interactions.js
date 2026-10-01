
const materials=JSON.parse(document.getElementById('material-data').textContent);
const variants=JSON.parse(document.getElementById('variant-data').textContent);
const prompts=JSON.parse(document.getElementById('prompt-data').textContent);
let edition='archive';
function changeEdition(id){edition=id;const v=variants[id];for(const [key,value] of Object.entries(v.colors)){document.documentElement.style.setProperty('--'+key,value)}document.getElementById('hook').textContent=v.headline;document.getElementById('poster-image').src='data:image/png;base64,'+materials[id+'-poster'].base64;document.getElementById('download-edition').textContent=v.name;document.querySelectorAll('[data-edition]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.edition===id)))}
document.querySelectorAll('[data-edition]').forEach(b=>b.addEventListener('click',()=>changeEdition(b.dataset.edition)));changeEdition('archive');
if(window.matchMedia('(max-width:760px)').matches)document.getElementById('poster').open=false;
function fill(t){const a=document.getElementById('concept-a').value.trim()||'【概念 A】';const b=document.getElementById('concept-b').value.trim()||'【概念 B】';const s=document.getElementById('scene').value.trim()||'学校咖啡店';return t.replaceAll('【概念 A】',a).replaceAll('【概念 B】',b).replaceAll('【场景】',s)}
function refresh(){document.querySelectorAll('[data-prompt]').forEach(e=>e.textContent=fill(prompts[e.dataset.prompt]))}
document.querySelectorAll('.inputs input').forEach(e=>e.addEventListener('input',refresh));refresh();
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{const el=document.getElementById(b.dataset.copy);try{await navigator.clipboard.writeText(el.textContent);b.textContent='已复制'}catch(e){const r=document.createRange();r.selectNodeContents(el);const s=window.getSelection();s.removeAllRanges();s.addRange(r);b.textContent='已选中，请复制'}setTimeout(()=>b.textContent='复制这句',2200)}));
document.querySelectorAll('.tick input').forEach(e=>e.addEventListener('change',()=>{document.getElementById('progress').textContent='已勾选 '+document.querySelectorAll('.tick input:checked').length+' / 6'}));
function blobFor(id){const m=materials[id];const binary=atob(m.base64);const bytes=new Uint8Array(binary.length);for(let i=0;i<binary.length;i++)bytes[i]=binary.charCodeAt(i);return new Blob([bytes],{type:m.mime})}
function download(id,preview=false){const status=document.getElementById('download-status');try{const m=materials[id];const url=URL.createObjectURL(blobFor(id));const a=document.createElement('a');a.href=url;if(preview){a.target='_blank';a.rel='noopener'}else a.download=m.filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),120000);status.textContent=preview?'已打开预览；图片可长按保存。':'已准备下载：'+m.filename+'。若没有出现保存提示，请用“查看海报”或浏览器打开本文件。'}catch(e){status.textContent='暂时无法保存，请用系统浏览器打开本文件后重试。'}}
document.querySelectorAll('[data-download]').forEach(b=>b.addEventListener('click',()=>{const kind=b.dataset.download;download(['notice','prompts'].includes(kind)?kind:edition+'-'+kind,b.dataset.preview==='true')}));
