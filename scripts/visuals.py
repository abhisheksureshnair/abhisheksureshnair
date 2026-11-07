"""Small, dependency-free SVG vocabulary for the profile's committed assets."""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'monarch'

def text(x, y, value, size=18, color='#C4B5FD', weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" font-family="Arial, sans-serif">{escape(str(value))}</text>'

def panel(name, body, width=440, height=230, title=None):
    OUT.mkdir(parents=True, exist_ok=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<title>{escape(title or name)}</title>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#15102C"/><stop offset="1" stop-color="#050510"/></linearGradient><radialGradient id="aura"><stop stop-color="#7C3AED" stop-opacity=".35"/><stop offset="1" stop-color="#050510" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18" fill="url(#bg)" stroke="#49316D"/>
<ellipse cx="{width*.8}" cy="{height*.4}" rx="{width*.45}" ry="{height*.8}" fill="url(#aura)"/>
<path d="M24 1 H108" stroke="#A855F7" stroke-width="3"/>
{body}</svg>'''
    (OUT / f'{name}.svg').write_text(svg)
    return svg
