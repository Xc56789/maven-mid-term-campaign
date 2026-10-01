from pathlib import Path
import json, base64, hashlib, html
import layout as campaign

REPO=Path(__file__).resolve().parent.parent
ROOT=REPO/'materials'
ROOT.mkdir(exist_ok=True)
DATA=json.loads((REPO/'content/campaign.json').read_text(encoding='utf-8'))
for attribute,key in [('TITLE','title'),('INTRO','intro'),('TASKS','tasks'),('STYLES','styles'),('REWARDS','poster_rewards'),('CARDTEXT','card_text')]:
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
  steps.append(f'''<details class="step" {'open' if t['n']==1 else ''}><summary><span class="number">{t['n']:02}</span><span><span class="steptitle">{t['title']}</span><span class="short">{t['short']}</span></span></summary><div class="stepbody"><span class="channel">{t['channel']}</span><p>{t['body']}</p><p class="help">{t['help']}</p>{extra}<p class="done">完成就好：{t['done']}</p><label class="tick"><input type="checkbox" aria-label="完成第{t['n']}项任务">这条线索，我查过了</label></div></details>''')
 variants={s['id']:{'name':s['name'],'headline':''.join(s['headline']),'colors':{**{k:s[k] for k in ['bg','ink','muted','accent','line','panel','secondary']},'buttonink':'#081b30' if s['id']=='night' else '#ffffff'}} for s in campaign.STYLES}
 toggles=''.join(f'<button class="edition" type="button" data-edition="{s["id"]}" aria-pressed="{str(s["id"]=="archive").lower()}">{s["name"]}</button>' for s in campaign.STYLES)
 gifts=''
 for group in ['每日随机礼','结案大奖']:
  rows=''.join(f'<li><span>{g["name"]}</span><span class="qty">{g["count"]} {g["unit"]}</span></li>' for g in GIFTS if g['group']==group)
  gifts+=f'<article class="giftgroup"><h3>{group}</h3><p>{"每通过一项，增加一次每日抽奖机会。" if group=="每日随机礼" else "六项全完成，活动结束额外抽出 6 位获奖者。"}</p><ul>{rows}</ul></article>'
 initial=';'.join('--'+k+':'+v for k,v in variants['archive']['colors'].items())
 dump=lambda value:json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
 page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="Maven 概念侦探社：六条线索，一桩小案。查课件、试一题、画小图，答错也能结案。"><title>Maven 概念侦探社</title><style>:root{{{initial}}}{CSS}</style></head><body><header><a class="brand" href="#top">Maven 概念侦探社</a><nav aria-label="页面导航"><a href="#clues">任务</a><a href="#gifts">礼物</a><a href="#downloads">下载</a></nav></header><main id="top"><section class="hero"><div><p class="audience">香港中文大学（深圳） · 营销课程期中复习</p><h1>概念侦探社</h1><p class="hook" id="hook">这两个概念，到底差在哪？</p><p class="intro">{campaign.INTRO}</p><p class="note">六条线索，一桩小案。答错、需要提示，都算完成。</p><div class="editions" role="group" aria-label="切换三版视觉">{toggles}</div><a class="primary" href="#clues">接下这桩小案</a><p class="note">用自己的学校账号参加，已有账号直接登录。</p></div><details class="poster" id="poster" open><summary>查看活动海报</summary><img id="poster-image" alt="Maven 概念侦探社活动海报" width="1080" height="1440"></details></section><section class="rewardstrip" aria-label="参与奖励"><div><small>任意一项通过审核</small><strong>领取贴纸 1 张</strong></div><div><small>每一项通过审核</small><strong>每日抽奖机会 +1</strong></div><div><small>六项全部完成</small><strong>额外参加 6 份大奖抽奖</strong></div></section><section id="clues"><div class="headingline"><h2>一桩小案，六条线索</h2><span class="counter" id="progress" aria-live="polite">已勾选 0 / 6</span></div><div class="case"><div class="inputs"><label>概念 A<input type="text" id="concept-a" maxlength="80" placeholder="一个容易混淆的概念" autocomplete="off"></label><label>概念 B<input type="text" id="concept-b" maxlength="80" placeholder="另一个概念" autocomplete="off"></label><label>想用什么场景举例？<input type="text" id="scene" maxlength="100" placeholder="校园咖啡店 / 社团招新 / 虚构小案件" autocomplete="off"></label></div><p class="note">填好后，各步的提问句会一起更新。复制到自己的 Maven 课程中使用。</p></div><div class="tasks">{''.join(steps)}</div><p class="note">勾选仅用来记进度，刷新会重置；任务与领奖资格按活动通知核验。</p></section><section class="gifts" id="gifts"><h2>查线索，也有小礼物</h2><div class="giftgroups">{gifts}</div><div class="sticker"><strong>入社小礼 · Maven Sticker ×300</strong><br>任意一项通过审核，领取贴纸 1 张。数量有限，先到先得。</div><ul class="rules"><li>每完成一项并通过审核，获得一次每日抽奖机会；同一任务每人只计一次。</li><li>每天随机开奖，不用自己选礼物。六项全完成，额外获得一次结案抽奖资格。</li><li>保存学习结果截图，按课程群通知提交与核验。请勿提交密码、二维码或微信配对码。</li><li>答错、需要提示，都算完成。礼品数量按原活动方案列示，最终名额、活动时间及领取安排见课程群通知。</li></ul></section><section class="downloads" id="downloads"><h2>把这份小案卷带走</h2><p class="note">当前：<strong id="download-edition">线索档案版</strong>。切换上方视觉版本，可下载另外两版。</p><div class="downloadbuttons"><button class="secondary" data-download="poster" type="button">下载海报 PNG</button><button class="secondary" data-download="task-card" type="button">下载任务卡 PNG</button><button class="secondary" data-download="campaign" type="button">下载海报与任务卡 PDF</button><button class="secondary" data-download="poster" data-preview="true" type="button">查看／保存海报</button><button class="secondary" data-download="notice" type="button">下载群公告文案</button><button class="secondary" data-download="prompts" type="button">下载提问句</button></div><p id="download-status" class="downloadstatus" role="status" aria-live="polite"></p><p class="note">所有材料都在这一个文件里，无需其他附件。微信内若不能打开或下载，请先保存文件，再用浏览器打开。</p></section><section class="closing"><h2>不用一次全懂。能说出哪里不懂，也是进展。</h2><p>把概念对照、小图和一句话理解留下来。下次复习，先回到这份小案卷。</p><a class="primary" href="https://ask-maven.com/" target="_blank" rel="noopener">去 Maven 开始</a></section></main><footer>Missing course files? Please contact your TA.<br>活动时间、任务提交、开奖与领取安排见课程群通知。</footer><noscript><p style="padding:20px">请使用支持 JavaScript 的浏览器打开，以显示海报、复制提问句和下载内置材料。任务与活动规则可直接阅读。</p></noscript><script type="application/json" id="material-data">{dump(assets)}</script><script type="application/json" id="variant-data">{dump(variants)}</script><script type="application/json" id="prompt-data">{dump(prompts)}</script><script>{JS}</script></body></html>'''
 output=REPO/'index.html';output.write_text(page,encoding='utf-8')
 
 manifest={k:{a:b for a,b in v.items() if a!='base64'} for k,v in assets.items()}
 (REPO/'docs'/'embedded-materials.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Standalone HTML bytes:',output.stat().st_size)
 print('Embedded downloads:',len(assets))

if __name__=="__main__":
 build_html()
