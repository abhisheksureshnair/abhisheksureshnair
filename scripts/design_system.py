"""GitHub-safe, self-contained SVG composition. No JavaScript or external fonts."""
import base64
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def text(x,y,value,size=20,color='#C4B5FD',weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>'

def image(path,x,y,w,h,opacity=1,fit='xMidYMid slice'):
    p=ROOT/path
    mime='image/webp' if p.suffix=='.webp' else 'image/png'
    data=base64.b64encode(p.read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" opacity="{opacity}" preserveAspectRatio="{fit}" href="data:{mime};base64,{data}"/>'

def energy(w,h,animated=False):
    s=''
    for i in range(14):
        x=20+(i*137)%(w-40);y=12+(i*59)%(h-24)
        motion=f'<animate attributeName="opacity" values=".15;.65;.15" dur="6s" begin="-{i%6}s" repeatCount="indefinite"/><animate attributeName="cy" values="{y+6};{y-6};{y+6}" dur="6s" begin="-{i%6}s" repeatCount="indefinite"/>' if animated else ''
        s+=f'<circle cx="{x}" cy="{y}" r="{1+i%2}" fill="#A855F7" opacity=".35">{motion}</circle>'
    return s

def write(path,body,w,h,title,animated=False):
    out=ROOT/path;out.parent.mkdir(parents=True,exist_ok=True)
    defs='''<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#080D21"/><stop offset="1" stop-color="#03040D"/></linearGradient><linearGradient id="fade"><stop stop-color="#03040D" stop-opacity=".9"/><stop offset=".65" stop-color="#03040D" stop-opacity=".2"/><stop offset="1" stop-color="#03040D" stop-opacity="0"/></linearGradient><radialGradient id="glow"><stop stop-color="#7C3AED" stop-opacity=".35"/><stop offset="1" stop-color="#7C3AED" stop-opacity="0"/></radialGradient><clipPath id="frame"><rect x="1" y="1" width="W" height="H" rx="16"/></clipPath></defs>'''.replace('W',str(w-2)).replace('H',str(h-2))
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{defs}<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="url(#bg)"/><ellipse cx="{w*.72}" cy="{h*.48}" rx="{w*.5}" ry="{h*.8}" fill="url(#glow)"/>{body}{energy(w,h,animated)}</g><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="none" stroke="#69409B"/><path d="M24 1 H110" stroke="#C4B5FD" stroke-width="2"/></svg>')

def pair(path,body,w,h,title):
    write(path+'-static.svg',body,w,h,title)
    write(path+'.svg',body,w,h,title,True)
