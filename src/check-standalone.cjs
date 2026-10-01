const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const readData=id=>JSON.parse(html.match(new RegExp('id="'+id+'">([\\s\\S]*?)<\\/script>'))[1]);
const materials=readData('material-data'),variants=readData('variant-data'),prompts=readData('prompt-data');
const checks=[];
function pass(name){checks.push(name)}
for(const [id,m] of Object.entries(materials)){
 const bytes=Buffer.from(m.base64,'base64');assert.equal(bytes.length,m.bytes);assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),m.sha256);
 if(m.mime==='application/pdf')assert(bytes.subarray(0,5).equals(Buffer.from('%PDF-')));
 if(m.mime==='image/png')assert(bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])));
 pass('Embedded material integrity: '+id);
}
assert.equal(Object.keys(materials).length,11);
assert(!/<(?:script|link)[^>]+(?:src|href)=/i.test(html));
for(const href of [...html.matchAll(/href="([^"]+)"/g)].map(m=>m[1]))assert(href.startsWith('#')||href==='https://ask-maven.com/');
assert(html.includes('@media(max-width:760px)')&&html.includes('@media(max-width:360px)'));
pass('No sibling files or remote asset dependencies; responsive breakpoints present');
for(const count of ['300','120','50','30'])assert(html.includes(count));
for(const gift of ['Maven Sticker','Maven 定制帆布袋','会饮／一瓯茶代金券','攀岩／健身握力环','Tangle','一次性胶片相机','影视飓风复古相机充电宝','abib 防晒'])assert(html.includes(gift));
assert(!html.includes('01＋02：贴纸')&&!html.includes('03＋04：帆布袋'));
pass('Original gift inventory and drawing rules; no prior guaranteed pair rewards');
function el(extra={}){return {textContent:'',value:'',dataset:{},attrs:{},listeners:{},addEventListener(t,f){this.listeners[t]=f},setAttribute(k,v){this.attrs[k]=v},...extra}}
const displays=Object.entries(prompts).map(([id,textContent])=>el({id,textContent,dataset:{prompt:id}}));
const copy=displays.map(d=>el({dataset:{copy:d.id}}));
const tabs=Object.keys(variants).map(id=>el({dataset:{edition:id}}));
const downs=['poster','task-card','campaign','poster','notice','prompts'].map((kind,i)=>el({dataset:{download:kind,preview:i===3?'true':'false'}}));
const ids=Object.fromEntries(displays.map(e=>[e.id,e]));
for(const id of ['poster-image','download-edition','download-status','poster'])ids[id]=el({open:true});
for(const [id,data] of [['material-data',materials],['variant-data',variants],['prompt-data',prompts]])ids[id]=el({textContent:JSON.stringify(data)});
const colors={},blobs=[],links=[];let selected=false,copied='';
const doc={documentElement:{style:{setProperty(k,v){colors[k]=v}}},getElementById(id){return ids[id]},querySelectorAll(q){return q==='[data-edition]'?tabs:q==='[data-copy]'?copy:q==='[data-download]'?downs:[]},createRange(){return {selectNodeContents(){selected=true}}},body:{appendChild(){}},createElement(){const a={click(){links.push({href:a.href,download:a.download,target:a.target})},remove(){}};return a}};
const navigator={clipboard:{async writeText(value){copied=value}}};
const context={document:doc,navigator,window:{matchMedia(){return {matches:true}},getSelection(){return {removeAllRanges(){},addRange(){}}}},setTimeout(){},URL:{createObjectURL(blob){blobs.push(blob);return 'blob:test-'+blobs.length},revokeObjectURL(){}},Blob,Uint8Array,atob:s=>Buffer.from(s,'base64').toString('binary')};
vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(root,'src','interactions.js'),'utf8'),context);
(async()=>{
 assert.equal(Object.keys(prompts).length,5);assert(!('p4-extra' in prompts));for(const field of ['考试时间','地点','考试范围','题型','未说明'])assert(prompts['p2-prompt'].includes(field));assert(ids['p4-prompt'].textContent.includes('学校咖啡店'));for(const phrase of ['3 道基础判断或选择题','先给题目','等我回答后再讲解'])assert(prompts['p4-prompt'].includes(phrase));assert(!html.includes('不要为连线编造因果关系'));for(const phrase of ['Quiz','Diagram','请给我举个例子','保留关键英文术语'])assert(prompts['p6-prompt'].includes(phrase));pass('Revised exam background, concept comparison, one case-and-quiz task, diagram and artifact follow-up');assert(!ids.poster.open);assert.equal(ids['download-edition'].textContent,'线索档案版');pass('Mobile poster collapses; default edition initializes');
 for(const id of Object.keys(variants)){context.changeEdition(id);assert.equal(ids['poster-image'].src,'data:image/png;base64,'+materials[id+'-poster'].base64);assert.equal(colors['--accent'],variants[id].colors.accent);assert.equal(tabs.filter(t=>t.attrs['aria-pressed']==='true').length,1)}pass('Three themes synchronize poster, palette and download edition');
 for(const removed of ['id="concept-a"','id="concept-b"','id="scene"','id="progress"','id="hook"','type="checkbox"','填好后，各步','答错','都算完成','【概念 A】','【概念 B】','【场景】'])assert(!html.includes(removed),removed);
 assert(prompts['p3-prompt'].includes('这节课的两个核心概念'));assert(prompts['p4-prompt'].includes('刚才这两个概念'));assert(prompts['p5-prompt'].includes('刚才这两个概念'));
 for(const display of displays)assert(html.includes('data-prompt="'+display.id+'">'+display.textContent+'</p>'));
 pass('Concise page without inputs, progress or correctness slogans; prompts use step-three concepts');
 await copy[0].listeners.click();assert.equal(copied,displays[0].textContent);navigator.clipboard.writeText=async()=>{throw Error()};await copy[0].listeners.click();assert(selected);pass('Copy and selection fallback');
 for(const [id,preview] of [['archive-poster',false],['night-campaign',false],['club-task-card',false],['notice',false],['prompts',false],['club-poster',true]]){context.download(id,preview);const actual=Buffer.from(await blobs.at(-1).arrayBuffer());assert.equal(crypto.createHash('sha256').update(actual).digest('hex'),materials[id].sha256);if(preview)assert.equal(links.at(-1).target,'_blank');else assert.equal(links.at(-1).download,materials[id].filename)}pass('PNG/PDF/TXT download bytes and preview target');
 context.changeEdition('night');downs[0].listeners.click();assert.equal(links.at(-1).download,materials['night-poster'].filename);pass('Download button follows selected edition');
 fs.writeFileSync(path.join(root,'docs','validation.json'),JSON.stringify({method:'Static HTML checks plus Node VM with DOM stubs; no browser or real phone execution',passed:checks,htmlBytes:Buffer.byteLength(html)},null,2));
 console.log(checks.length+' checks passed. All 11 embedded files match their SHA-256 hashes.');
})().catch(e=>{console.error(e);process.exit(1)});
