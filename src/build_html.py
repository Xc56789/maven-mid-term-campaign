from pathlib import Path
import json, base64, hashlib, html
import layout as campaign

REPO=Path(__file__).resolve().parent.parent
ROOT=REPO/'materials'
ROOT.mkdir(exist_ok=True)
DATA=json.loads((REPO/'content/campaign.json').read_text(encoding='utf-8'))
for attribute,key in [('TITLE','title'),('TASKS','tasks'),('STYLES','styles'),('REWARDS','poster_rewards'),('CARDTEXT','card_text')]:
    setattr(campaign,attribute,DATA[key])
GIFTS=DATA['gifts']
ANNOUNCEMENT=DATA['announcement']
CSS=(REPO/'src/campaign.css').read_text(encoding='utf-8')
JS=(REPO/'src/interactions.js').read_text(encoding='utf-8')

def file_asset(path,mime,filename=None):
 raw=path.read_bytes();return {'mime':mime,'filename':filename or path.name,'base64':base64.b64encode(raw).decode(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def build_html():
 assets={}
 for s in campaign.STYLES:
  for kind,ext,mime in [('poster','png','image/png'),('task-card','png','image/png'),('campaign','pdf','application/pdf')]:
   assets[s['id']+'-'+kind]=file_asset(ROOT/(s['id']+'-'+kind+'.'+ext),mime,'Maven-概念侦探社-'+s['name']+'-'+{'poster':'海报','task-card':'任务卡','campaign':'海报与任务卡'}[kind]+'.'+ext)
 (ROOT/'群公告-定稿.txt').write_text(ANNOUNCEMENT,encoding='utf-8-sig')
 promptdoc='Maven 概念侦探社｜提问句\n\n'+ '\n\n'.join(f"{t['n']:02} {t['title']}\n"+'\n\n'.join(t[k] for k in ['prompt','extra'] if t.get(k)) for t in campaign.TASKS if t.get('prompt'))
 (ROOT/'提问句-定稿.txt').write_text(promptdoc,encoding='utf-8-sig')
 assets['notice']=file_asset(ROOT/'群公告-定稿.txt','text/plain;charset=utf-8')
 assets['prompts']=file_asset(ROOT/'提问句-定稿.txt','text/plain;charset=utf-8')
 prompts={};steps=[]
 for t in campaign.TASKS:
  extra=''
  for key in ['prompt','extra']:
   if t.get(key):
    pid=f"p{t['n']}-{key}";prompts[pid]=t[key];extra+=f'<div class="promptbox"><p id="{pid}" data-prompt="{pid}">{html.escape(t[key])}</p><button class="copy" type="button" data-copy="{pid}">复制这句</button></div>'
  steps.append(f'''<details class="step" {'open' if t['n']==1 else ''}><summary><span class="number">{t['n']:02}</span><span><span class="steptitle">{t['title']}</span><span class="short">{t['short']}</span></span></summary><div class="stepbody"><span class="channel">{t['channel']}</span><p>{t['body']}</p><p class="help">{t['help']}</p>{extra}<p class="done">完成：{t['done']}</p></div></details>''')
 variants={s['id']:{'name':s['name'],'colors':{**{k:s[k] for k in ['bg','ink','muted','accent','line','panel','secondary']},'buttonink':'#081b30' if s['id']=='night' else '#ffffff'}} for s in campaign.STYLES}
 toggles=''.join(f'<button class="edition" type="button" data-edition="{s["id"]}" aria-pressed="{str(s["id"]=="archive").lower()}">{s["name"]}</button>' for s in campaign.STYLES)
 gifts=''
 for group in ['每日随机礼','结案大奖']:
<section class="rewardstrip" aria-label="参与奖励"><div><small>每一项通过审核</small><strong>每日抽奖机会 +1</strong></div><div><small>六项全部完成</small><strong>额外参加 6 份大奖抽奖</strong></div></section>  gifts+=f'<article class="giftgroup"><h3>{group}</h3><p>{"每通过一项，增加一次每日抽奖机会。" if group=="每日随机礼" else "六项全完成，活动结束额外抽出 6 位获奖者。"}</p><ul>{rows}</ul></article>'
 initial=';'.join('--'+k+':'+v for k,v in variants['archive']['colors'].items())
 dump=lambda value:json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
<div class="rewardstrip" aria-label="参与奖励"><div><small>每一项通过审核</small><strong>每日抽奖机会 +1</strong></div><div><small>六项全部完成</small><strong>额外参加 6 份大奖抽奖</strong></div></section> output=REPO/'index.html';output.write_text(page,encoding='utf-8')
 
 manifest={k:{a:b for a,b in v.items() if a!='base64'} for k,v in assets.items()}
 (REPO/'docs'/'embedded-materials.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Standalone HTML bytes:',output.stat().st_size)
 print('Embedded downloads:',len(assets))

if __name__=="__main__":
 build_html()
