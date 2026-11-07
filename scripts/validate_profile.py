"""Validate the published README surfaces and generated image assets."""
from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Images(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert tag not in {'script', 'iframe', 'style', 'table'}, tag
        assert 'style' not in attrs
        if tag == 'img':
            assert 'alt' in attrs
        for attr in ('src', 'srcset'):
            if attr in attrs:
                assert not attrs[attr].startswith('http'), 'External image dependency'
                assert (ROOT / attrs[attr]).is_file(), attrs[attr]

for filename in ('README.md', 'README-static.md'):
    content = (ROOT / filename).read_text()
    Images().feed(content)
    assert not re.search(r'3\.5|92\+|300\+|1\.2k\+|EchoJobPilot|real.time developer telemetry', content, re.I)
    for link in re.findall(r'\]\(([^)]+)\)', content):
        if not link.startswith(('http', '#', 'mailto:')):
            assert (ROOT / link).is_file(), link
    if filename == 'README-static.md':
        assert '.gif' not in content

dirs=['monarch','hero','cards','projects','stats','footer','background']
for file in (f for d in dirs for f in (ROOT/'assets'/d).glob('*.svg')):
    root = ET.parse(file).getroot()
    assert root.tag.endswith('svg')
    assert '<script' not in file.read_text()
static=(ROOT/'README-static.md').read_text()
for asset in re.findall(r'(?:src|srcset)="(assets/[^"]+)"',static):
    if asset.endswith('.svg'):
        assert '<animate' not in (ROOT/asset).read_text(), asset
print('PASS: local assets, alt text, static fallback, SVG XML and README constraints')
