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

def build_showcase():
    print("Building Featured Repositories Showcase (1840 x 840)...")
    W, H = 1840, 840
    img = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    draw = ImageDraw.Draw(img)
    
    # Outer border and corner brackets
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 200), width=2)
    bracket_len = 24
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=3)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=3)
        
    # Top Section Header
    draw.text((60, 32), "⚔️ SHADOW ARSENAL // FEATURED REPOSITORIES", fill=(34, 211, 238), font=get_font(22, bold=True))
    draw.text((60, 68), "Curated collection of public projects across full-stack web, cross-platform mobile, and AI tooling.", fill=(226, 232, 240), font=get_font(15, bold=False))
    
    # 6 Major Grid Cards (3 columns x 2 rows)
    projects = [
        {
            "name": "⚡ FlowSync",
            "desc": "Real-time task boards & team messaging with live collaboration sync.",
            "tech": "React • Node.js • Express • MongoDB",
            "accent": (168, 85, 247),
            "mockup_type": "kanban"
        },
        {
            "name": "📱 LiveSync",
            "desc": "Cross-platform location-sharing prototype with simulated tracking telemetry.",
            "tech": "React Native • React • Node.js • Express",
            "accent": (34, 211, 238),
            "mockup_type": "map"
        },
        {
            "name": "📈 AlphaPulse Stock AI",
            "desc": "Algorithmic market analytics, technical stock indicators & portfolio tooling.",
            "tech": "Flutter • React Native • Python • FastAPI",
            "accent": (124, 58, 237),
            "mockup_type": "chart"
        },
        {
            "name": "🤖 Echo Desktop AI",
            "desc": "Intelligent desktop assistant & browser co-pilot for developer productivity.",
            "tech": "Electron • React • JavaScript",
            "accent": (196, 181, 253),
            "mockup_type": "ai"
        },
        {
            "name": "📍 Vehicle Tracking (TraqInn)",
            "desc": "Fleet tracking mobile interface with real-time GPS routes & telemetry history.",
            "tech": "Flutter • Dart • Node.js • Express",
            "accent": (34, 211, 238),
            "mockup_type": "fleet"
        },
        {
            "name": "🛍️ Luxentia E-commerce",
            "desc": "Modern luxury fashion mobile boutique application with catalogue & cart.",
            "tech": "Flutter • Dart • Node.js",
            "accent": (168, 85, 247),
            "mockup_type": "store"
        }
    ]
    
    card_w = 540
    card_h = 320
    gap_x = 45
    gap_y = 35
    start_x = 60
    start_y = 115
    
    for idx, p in enumerate(projects):
        row = idx // 3
        col = idx % 3
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)
        
        # Project card container
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=10, fill=(15, 22, 45, 230), outline=p["accent"], width=1)
        
        # Inner Mockup Area (110px height)
        mx, my, mw, mh = cx + 18, cy + 18, card_w - 36, 110
        draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=6, fill=(8, 12, 26, 255), outline=(124, 58, 237, 100), width=1)
        
        # Draw distinctive visual mockup inside
        if p["mockup_type"] == "kanban":
            # 3 kanban columns
            for ki in range(3):
                kx = mx + 15 + ki * 165
                draw.rounded_rectangle([kx, my + 10, kx + 145, my + mh - 10], radius=4, fill=(18, 24, 50, 255))
                draw.rectangle([kx + 10, my + 18, kx + 70, my + 24], fill=(168, 85, 247, 255))
                draw.rounded_rectangle([kx + 10, my + 32, kx + 135, my + 54], radius=3, fill=(28, 38, 75, 255))
                draw.rounded_rectangle([kx + 10, my + 60, kx + 135, my + 82], radius=3, fill=(28, 38, 75, 255))
        elif p["mockup_type"] == "map":
            # Map grid and path
            for gx in range(mx + 20, mx + mw - 20, 45):
                draw.line([(gx, my + 10), (gx, my + mh - 10)], fill=(20, 30, 60, 150))
            for gy in range(my + 15, my + mh - 15, 25):
                draw.line([(mx + 10, gy), (mx + mw - 10, gy)], fill=(20, 30, 60, 150))
            # GPS path
            pts = [(mx + 40, my + 80), (mx + 140, my + 35), (mx + 260, my + 70), (mx + 380, my + 30), (mx + 460, my + 60)]
            draw.line(pts, fill=(34, 211, 238, 255), width=3)
            for px, py in pts:
                draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(248, 250, 252, 255), outline=(34, 211, 238, 255), width=2)
        elif p["mockup_type"] == "chart":
            # Stock line chart
            pts = [(mx + 20, my + 85), (mx + 100, my + 65), (mx + 180, my + 80), (mx + 270, my + 35), (mx + 360, my + 50), (mx + 470, my + 20)]
            draw.line(pts, fill=(168, 85, 247, 255), width=3)
            # Area glow
            for pt in pts:
                draw.ellipse([pt[0] - 3, pt[1] - 3, pt[0] + 3, pt[1] + 3], fill=(34, 211, 238, 255))
            draw.text((mx + mw - 120, my + 12), "+24.8% AI SIGNAL", fill=(34, 211, 238), font=get_font(11, bold=True))
        elif p["mockup_type"] == "ai":
            # AI chat prompt & response
            draw.rounded_rectangle([mx + 15, my + 15, mx + 280, my + 45], radius=4, fill=(25, 35, 70, 255))
            draw.text((mx + 25, my + 22), "> analyze_repo_ast --mode=fast", fill=(196, 181, 253), font=get_font(12, bold=False))
            draw.rounded_rectangle([mx + 150, my + 55, mx + mw - 15, my + 95], radius=4, fill=(35, 25, 65, 255), outline=(168, 85, 247, 150))
            draw.text((mx + 165, my + 65), "⚡ Co-pilot: 0 bottlenecks found. Ready.", fill=(34, 211, 238), font=get_font(12, bold=True))
        elif p["mockup_type"] == "fleet":
            # Fleet vehicle dots & speed
            draw.text((mx + 20, my + 15), "FLEET TELEMETRY: 12 VEHICLES ACTIVE", fill=(34, 211, 238), font=get_font(11, bold=True))
            for fx in range(mx + 30, mx + mw - 40, 80):
                draw.rounded_rectangle([fx, my + 40, fx + 65, my + 95], radius=4, fill=(20, 30, 60, 255))
                draw.text((fx + 10, my + 50), "SPEED", fill=(148, 163, 184), font=get_font(9, bold=False))
                draw.text((fx + 10, my + 68), "64 km/h", fill=(248, 250, 252), font=get_font(11, bold=True))
        elif p["mockup_type"] == "store":
            # Product cards
            for si in range(4):
                sx = mx + 20 + si * 115
                draw.rounded_rectangle([sx, my + 12, sx + 100, my + mh - 12], radius=4, fill=(22, 28, 55, 255))
                draw.rectangle([sx + 10, my + 22, sx + 90, my + 65], fill=(35, 45, 80, 255))
                draw.text((sx + 10, my + 72), "Collection", fill=(196, 181, 253), font=get_font(10, bold=False))
                
        # Project Title
        draw.text((cx + 18, cy + 142), p["name"], fill=(248, 250, 252), font=get_font(18, bold=True))
        
        # Project Description
        draw.text((cx + 18, cy + 172), p["desc"], fill=(226, 232, 240), font=get_font(13, bold=False))
        
        # Tech Stack Tag
        draw.text((cx + 18, cy + 228), "TECH STACK:", fill=(148, 163, 184), font=get_font(11, bold=True))
        draw.text((cx + 18, cy + 248), p["tech"], fill=p["accent"], font=get_font(13, bold=True))
        
        # Explore Link Button
        bx, by, bw, bh = cx + 18, cy + 276, 175, 30
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=5, fill=(10, 16, 32, 240), outline=p["accent"], width=1)
        draw.text((bx + 16, by + 7), "EXPLORE REPOSITORY →", fill=(248, 250, 252), font=get_font(11, bold=True))
        
    img = img.convert('RGB')
    img.save('assets/featured-repositories-showcase.png', quality=95)
    print("Featured Repositories Showcase saved!")

if __name__ == '__main__':
    build_showcase()
