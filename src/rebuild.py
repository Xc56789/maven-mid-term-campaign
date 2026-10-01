from pathlib import Path
import argparse, json, subprocess, shutil, sys, os
from reportlab.pdfgen import canvas
from build_html import REPO, ROOT, DATA, campaign

def main():
    parser=argparse.ArgumentParser(description='Rebuild campaign materials and standalone HTML.')
    parser.add_argument('--html-only',action='store_true',help='Re-embed existing PDF/PNG files without rendering.')
    args=parser.parse_args()
    if not args.html_only:
        renderer=os.environ.get('PDFTOPPM') or shutil.which('pdftoppm')
        if not renderer:raise SystemExit('Install Poppler and place pdftoppm on PATH, or set PDFTOPPM to its absolute path.')
        print('Font mode:',campaign.register_fonts())
        for s in campaign.STYLES:
            pdf=ROOT/(s['id']+'-campaign.pdf')
            c=canvas.Canvas(str(pdf),pagesize=(540,720));c.setTitle(campaign.TITLE+' · '+s['name']);c.setAuthor('Maven')
            campaign.poster(c,s);campaign.card(c,s);c.save()
            prefix=ROOT/(s['id']+'-render')
            subprocess.run([renderer,'-png','-scale-to-x','1080','-scale-to-y','1440',str(pdf),str(prefix)],check=True)
            for n,kind in [(1,'poster'),(2,'task-card')]:
                (ROOT/(s['id']+f'-render-{n}.png')).replace(ROOT/(s['id']+'-'+kind+'.png'))
    from build_html import build_html
    build_html()

if __name__=='__main__':main()
