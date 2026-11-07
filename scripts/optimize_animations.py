"""Resize existing loops, unify their canvases and save static alternatives.

Maintenance only: requires Pillow. No image-generation or runtime dependency.
Original GIFs are preserved in assets/animations.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageSequence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'monarch'
OUT.mkdir(parents=True, exist_ok=True)
for slug in ['chibi-idle', 'chibi-dancing', 'shadow-soldier']:
    source = Image.open(ROOT / 'assets' / 'animations' / f'{slug}.gif')
    frames, durations = [], []
    for frame in ImageSequence.Iterator(source):
        durations.append(frame.info.get('duration', 100))
        art = frame.convert('RGB')
        art.thumbnail((218, 258), Image.Resampling.LANCZOS)
        canvas = Image.new('RGB', (240, 284), '#080A18')
        canvas.paste(art, ((240-art.width)//2, (284-art.height)//2))
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((1,1,238,282), radius=14, outline='#7C3AED', width=2)
        draw.line((24,1,76,1),fill='#C4B5FD',width=2)
        frames.append(canvas)
    frames[0].save(OUT / f'{slug}.png', optimize=True)
    palette = frames[0].quantize(colors=128)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT / f'{slug}.gif', save_all=True, append_images=indexed[1:], duration=durations, loop=0, optimize=True, disposal=2)
source = Image.open(ROOT / 'assets' / 'animations' / 'shadow-particles.gif')
source.convert('RGB').save(OUT / 'energy-static.png', optimize=True)
