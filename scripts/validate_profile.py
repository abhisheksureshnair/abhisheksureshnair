"""
Validation suite for Shadow Monarch V3 GitHub Profile.
Verifies all assets, animations, links, Markdown constraints, and image integrity.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]

class ProfileHTMLParser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        assert tag not in {'script', 'iframe', 'object', 'embed'}, f"Forbidden unsafe tag <{tag}> in {self.filename}"
        if tag == 'img':
            assert 'alt' in attrs_dict, f"Missing alt attribute on <img> in {self.filename}: {attrs_dict}"
            src = attrs_dict.get('src', '')
            if not src.startswith(('http://', 'https://')):
                local_path = ROOT / src
                assert local_path.is_file(), f"Missing local image referenced in {self.filename}: {src}"

def validate_markdown_files():
    print("Checking README.md and README-static.md...")
    for filename in ('README.md', 'README-static.md'):
        content = (ROOT / filename).read_text()
        parser = ProfileHTMLParser(filename)
        parser.feed(content)
        
        # Check no fictional experience or metric claims
        assert not re.search(r'3\.5\s*years|92\+\s*repos|1\.2k\+\s*stars', content, re.I), f"Unverified claim in {filename}"
        
        # Check markdown links
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if not link.startswith(('http://', 'https://', '#', 'mailto:')):
                assert (ROOT / link).is_file(), f"Broken markdown link in {filename}: {link}"
                
        if filename == 'README-static.md':
            assert '.gif' not in content, f"GIF animation found in static fallback {filename}"
    print("✓ Markdown files and links validated.")

def validate_gif_animations():
    print("Checking animated GIF assets for genuine motion...")
    expected_gifs = [
        'assets/animations/chibi-idle.gif',
        'assets/animations/chibi-typing.gif',
        'assets/animations/chibi-dancing.gif',
        'assets/animations/shadow-soldier.gif',
        'assets/animations/shadow-particles.gif',
    ]
    for rel_path in expected_gifs:
        full_path = ROOT / rel_path
        assert full_path.is_file(), f"Missing animation: {rel_path}"
        im = Image.open(full_path)
        assert im.n_frames >= 12, f"Insufficient frames ({im.n_frames}) in {rel_path}"
        assert im.info.get('loop') == 0, f"GIF not set to infinite loop in {rel_path}"
        
        # Verify genuine motion across frames
        diff_count = 0
        for i in range(1, min(im.n_frames, 10)):
            im.seek(i)
            f1 = im.convert('RGBA')
            im.seek(i - 1)
            f0 = im.convert('RGBA')
            if ImageChops.difference(f1, f0).getbbox() is not None:
                diff_count += 1
        assert diff_count >= 8, f"Static frames detected in {rel_path}; visible motion required!"
        print(f"  ✓ {rel_path}: {im.n_frames} frames, {im.size}, verified active motion.")

def validate_svg_assets():
    print("Checking SVG assets for XML integrity...")
    svg_files = list((ROOT / 'assets').rglob('*.svg'))
    assert len(svg_files) > 0, "No SVG assets found"
    for svg_file in svg_files:
        root = ET.parse(svg_file).getroot()
        assert root.tag.endswith('svg'), f"Not an SVG element: {svg_file}"
        assert '<script' not in svg_file.read_text(), f"Script tag found in SVG: {svg_file}"
    print(f"✓ Validated {len(svg_files)} SVG assets.")

def validate_card_artwork():
    print("Checking card and banner image assets...")
    required_cards = [
        'assets/hero-banner.png',
        'assets/about-card.png',
        'assets/currently-card.png',
        'assets/tech-stack-galaxy.png',
        'assets/hunter-id-card.png',
        'assets/stats-ribbon.png',
        'assets/featured-repositories-showcase.png',
        'assets/contribution-city-cinematic.png',
        'assets/connect-card.png',
        'assets/shadow-monarch-footer.png',
    ]
    for card in required_cards:
        p = ROOT / card
        assert p.is_file(), f"Missing card asset: {card}"
        im = Image.open(p)
        assert im.width >= 800, f"Card width too small: {card} ({im.size})"
        print(f"  ✓ {card}: {im.size}")

if __name__ == '__main__':
    validate_markdown_files()
    validate_gif_animations()
    validate_svg_assets()
    validate_card_artwork()
    print("\n🎉 ALL TESTS PASSED: Shadow Monarch V3 profile is fully verified!")
