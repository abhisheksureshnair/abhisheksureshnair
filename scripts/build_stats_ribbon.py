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

def build_stats_ribbon():
    print("Building Stats Ribbon (1840 x 160)...")
    W, H = 1840, 160
    img = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    draw = ImageDraw.Draw(img)
    
    # Outer border and corner brackets
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 200), width=2)
    bracket_len = 16
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=2)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=2)
        
    modules = [
        ("PUBLIC REPOSITORIES", "8 Repositories", "Owned & Fully Public", (168, 85, 247)),
        ("ORIGINAL NON-FORK", "8 Projects", "100% Original Codebases", (34, 211, 238)),
        ("PRIMARY LANGUAGES", "Dart • JS • TS • Python", "Cross-Platform Stack", (124, 58, 237)),
        ("TELEMETRY STATUS", "100% Operational", "Daily GitHub Verification", (196, 181, 253))
    ]
    
    col_w = W // 4
    for idx, (label, val, sub, col) in enumerate(modules):
        cx = idx * col_w + 35
        # Draw vertical separator except for first
        if idx > 0:
            draw.line([(idx * col_w, 20), (idx * col_w, H - 20)], fill=(124, 58, 237, 100), width=1)
            
        draw.text((cx, 28), f"⚡ {label}", fill=col, font=get_font(13, bold=True))
        draw.text((cx, 55), val, fill=(248, 250, 252), font=get_font(26, bold=True))
        draw.text((cx, 100), sub, fill=(148, 163, 184), font=get_font(14, bold=False))
        
    img = img.convert('RGB')
    img.save('assets/stats-ribbon.png', quality=95)
    print("Stats Ribbon saved!")

if __name__ == '__main__':
    build_stats_ribbon()
