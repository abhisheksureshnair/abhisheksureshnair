import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def build_currently_card():
    print("Rebuilding Currently Working On Card with Boy Anime Developer...")
    W, H = 900, 520
    card = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    
    # Load boy workspace art
    ws_art_path = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a/cyberpunk_anime_developer_v2_1794038301178.jpg'
    ws_art = Image.open(ws_art_path).convert('RGBA')
    art_h = H
    art_w = int(ws_art.width * (art_h / ws_art.height))
    ws_art = ws_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
    
    card.paste(ws_art, (W - art_w, 0))
    
    # Left dark glass gradient for text readability
    grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(grad)
    for x in range(W):
        if x < W * 0.45:
            alpha = 245
        elif x < W * 0.80:
            frac = (x - W * 0.45) / (W * 0.35)
            alpha = int(245 * (1.0 - frac * 0.9))
        else:
            alpha = 15
        grad_draw.line([(x, 0), (x, H)], fill=(10, 16, 32, alpha))
    card = Image.alpha_composite(card, grad)
    
    draw = ImageDraw.Draw(card)
    # Border & brackets
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 180), width=2)
    bracket_len = 20
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=2)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=2)
        
    # Title
    draw.text((45, 40), "ACTIVE QUEST // CURRENT FOCUS", fill=(34, 211, 238), font=get_font(18, bold=True))
    draw.text((45, 75), "Dungeon In Progress", fill=(248, 250, 252), font=get_font(32, bold=True))
    draw.text((45, 120), "PRIORITY SYSTEM EXPANSIONS & WORKFLOWS", fill=(168, 85, 247), font=get_font(13, bold=True))
    
    # Body text
    body = [
        "1. FlowSync Architecture Expansion",
        "   Scaling real-time collaborative task boards and team messaging",
        "   using optimized WebSocket conduits and MongoDB event streaming.",
        "",
        "2. LiveSync Telemetry & Geolocation Prototype",
        "   Refining cross-platform location simulation, map rendering,",
        "   and responsive location tracking across React Native and Web.",
        "",
        "3. AlphaPulse Stock AI Intelligence Bot",
        "   Building automated stock analytics, algorithmic portfolio tooling,",
        "   and market signals powered by Python & FastAPI."
    ]
    font_body = get_font(14, bold=False)
    y = 155
    for line in body:
        draw.text((45, y), line, fill=(226, 232, 240) if line.startswith("   ") else (196, 181, 253), font=font_body)
        y += 22
        
    # Badges
    pills = ["⚡ FlowSync v2", "📍 LiveSync Map", "📈 AlphaPulse AI"]
    px = 45
    py = 430
    for p in pills:
        pw = len(p) * 8 + 26
        draw.rounded_rectangle([px, py, px + pw, py + 32], radius=6, fill=(34, 211, 238, 50), outline=(34, 211, 238, 180), width=1)
        draw.text((px + 12, py + 7), p, fill=(248, 250, 252), font=get_font(13, bold=True))
        px += pw + 12
        
    card = card.convert('RGB')
    card.save('assets/currently-card.png', quality=95)
    print("Updated Currently Working On Card saved!")

if __name__ == '__main__':
    build_currently_card()
