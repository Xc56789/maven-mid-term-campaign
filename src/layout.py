from pathlib import Path
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parent.parent
ASSETS=ROOT/'assets'/'illustrations'
W,H=540,720

def register_fonts():
    mode=os.environ.get('MAVEN_FONT','auto')
    windows=Path('C:/Windows/Fonts')
    legacy=(windows/'msyh.ttc').exists() and (windows/'msyhbd.ttc').exists()
    if mode=='windows' and not legacy:
        raise RuntimeError('Microsoft YaHei is unavailable; use MAVEN_FONT=licensed.')
    if legacy and mode!='licensed':
        pdfmetrics.registerFont(TTFont('Chinese',str(windows/'msyh.ttc'),subfontIndex=0))
        pdfmetrics.registerFont(TTFont('ChineseBold',str(windows/'msyhbd.ttc'),subfontIndex=0))
        font_mode='Microsoft YaHei (installed locally)'
    else:
        pdfmetrics.registerFont(TTFont('Chinese',str(ROOT/'assets/fonts/MavenCampaignSans-Regular.ttf')))
        pdfmetrics.registerFont(TTFont('ChineseBold',str(ROOT/'assets/fonts/MavenCampaignSans-Bold.ttf')))
        font_mode='Bundled OFL Noto Sans SC static instances'
    pdfmetrics.registerFont(TTFont('Brand',str(ROOT/'assets/fonts/BricolageGrotesque-Bold.ttf')))
    return font_mode


def color(c,h): c.setFillColor(HexColor(h))

def text(c,x,top,value,size=12,bold=False,fill='#173538',font=None):
    color(c,fill);c.setFont(font or ('ChineseBold' if bold else 'Chinese'),size);c.drawString(x,H-top-size,value)

def line(c,x,y,x2,y2,fill,width=.6):
    c.setStrokeColor(HexColor(fill));c.setLineWidth(width);c.line(x,H-y,x2,H-y2)

def wrap(value,width,size,font='Chinese'):
    lines=[];part=''
    for ch in value:
        if ch=='\n':lines.append(part);part='';continue
        if part and pdfmetrics.stringWidth(part+ch,font,size)>width:
            if ch in '，。；：！？、）】》」』':
                lines.append(part[:-1]);part=part[-1]+ch
            else:lines.append(part);part=ch
        else:part+=ch
    if part:lines.append(part)
    return lines

def para(c,x,top,value,width,size=12,leading=None,fill='#173538',bold=False):
    lines=wrap(value,width,size,'ChineseBold' if bold else 'Chinese')
    for n,s in enumerate(lines): text(c,x,top+n*(leading or size*1.6),s,size,bold,fill)
    return top+len(lines)*(leading or size*1.6)

def box(c,x,top,w,h,fill,border=None,r=8,alpha=1):
    c.saveState();c.setFillAlpha(alpha);color(c,fill)
    if border:c.setStrokeColor(HexColor(border));c.setLineWidth(.6)
    c.roundRect(x,H-top-h,w,h,r,stroke=1 if border else 0,fill=1);c.restoreState()

def poster(c,s):
    c.drawImage(ImageReader(str(ASSETS/s['hero'])),0,0,W,H)
    night=s['id']=='night';ink=s['postertext'];accent=s['accent'];panel=s['panel']
    text(c,30,25,'MAVEN',17,fill=ink,font='Brand')
    if s['id']=='archive':
        box(c,321,24,174,23,'#f7f5ed',r=4,alpha=.94)
    text(c,330,29,'期中复习 · 营销课程',9,fill=ink)
    text(c,31,67,'概念侦探社',43,True,ink)
    text(c,33,130,s['headline'][0],25,True,ink)
    text(c,33,164,s['headline'][1],22 if night else 25,True,ink)
    text(c,33,197 if s['id']=='club' else 208,'六条线索，一桩小案。',12,fill=ink)
    box(c,20,564,500,139,panel,s['line'],r=10,alpha=.96)
    text(c,35,577,'查考试背景 / 对照概念试一题 / 连线索找案卷',13,True,s['ink'])
    for i,(a,b,gift) in enumerate(REWARDS):
        x=35+i*166
        text(c,x,602,a,9,fill=s['muted'])
        text(c,x,619,gift,13,True,s['ink'])
        if i<2:line(c,x+151,607,x+151,638,s['line'])
    text(c,35,646,'ask-maven.com',18,fill=s['accent'],font='Brand')
    text(c,249,650,'用自己的学校账号参加',10,fill=s['ink'])
    text(c,35,680,'活动时间、礼物名额与领取安排见课程群通知。',9,fill=s['muted'])
    c.linkURL('https://ask-maven.com/',(35,H-670,220,H-642),relative=0)
    c.showPage()

def card(c,s):
    color(c,s['bg']);c.rect(0,0,W,H,stroke=0,fill=1)
    text(c,27,22,'MAVEN / 概念侦探社',17,True,s['ink'])
    text(c,27,57,'六条线索 · 任务卡',28,True,s['ink'])
    text(c,28,105,'先查清考试背景，再沿着概念线索走完这桩小案。',11,fill=s['muted'])
    for i,t in enumerate(TASKS):
        col=i%2;row=i//2;x=27+col*250;top=158+row*158;bw=236;bh=145
        box(c,x,top,bw,bh,s['panel'],s['line'],r=6 if s['id']=='archive' else 10)
        text(c,x+13,top+11,f'{i+1:02}',19,fill=s['accent'],font='Brand')
        text(c,x+47,top+13,t['title'],11,True,s['ink'])
        y=para(c,x+13,top+43,CARDTEXT[i][0],bw-26,10.2,15,s['ink'])
        line(c,x+13,y+6,x+bw-13,y+6,s['line'])
        para(c,x+13,y+13,CARDTEXT[i][1],bw-26,9.1,13,s['muted'])
        # Validate lower margin in the second text block.
        end=y+13+len(wrap(CARDTEXT[i][1],bw-26,9.1))*13
        assert end < top+bh-5,(s['id'],i,end,top+bh)
    text(c,28,646,'每项通过审核：每日抽奖 1 次 / 全部 6 项：额外参加结案抽奖',10.5,True,s['ink'])
    text(c,28,674,'任意 1 项通过可领贴纸 ×1，限量先到先得。',9,fill=s['muted'])
    text(c,28,695,'ask-maven.com  ·  考试安排以课程通知为准  ·  找不到课程请联系 TA',8.5,fill=s['muted'])
    c.showPage()
