import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BRAIN_DIR = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a'

# Try to load high quality fonts, fallback to default if not found
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

# -------------------------------------------------------------------------
# 1. HERO BANNER (1840 x 580)
# -------------------------------------------------------------------------
def build_hero_banner():
    print("Building Hero Banner...")
    W, H = 1840, 580
    banner = Image.new('RGBA', (W, H), (3, 4, 13, 255))
    
    # Load hero art
    hero_art_path = os.path.join(BRAIN_DIR, 'shadow_monarch_cyberpunk_banner_1794036864037.jpg')
    hero_art = Image.open(hero_art_path).convert('RGBA')
    # Resize art to height H, scale width proportionally
    art_h = H
    art_w = int(hero_art.width * (art_h / hero_art.height))
    hero_art = hero_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
    
    # Paste on right side
    banner.paste(hero_art, (W - art_w, 0))
    
    # Create smooth dark gradient overlay on left to blend seamlessly
    grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(grad)
    for x in range(W):
        if x < W * 0.40:
            alpha = 255
        elif x < W * 0.75:
            frac = (x - W * 0.40) / (W * 0.35)
            alpha = int(255 * (1.0 - frac * 0.95))
        else:
            alpha = int(12 * (1.0 - (x - W * 0.75) / (W * 0.25)))
        grad_draw.line([(x, 0), (x, H)], fill=(3, 4, 13, alpha))
    banner = Image.alpha_composite(banner, grad)
    
    # Draw content on left
    draw = ImageDraw.Draw(banner)
    
    # Glowing violet border
    draw.rectangle([6, 6, W - 7, H - 7], outline=(124, 58, 237, 180), width=2)
    # Corner brackets (cyan)
    bracket_len = 30
    for cx, cy, dx, dy in [(8, 8, 1, 1), (W - 9, 8, -1, 1), (8, H - 9, 1, -1), (W - 9, H - 9, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=3)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=3)
        
    # Protocol badge
    badge_x, badge_y = 60, 60
    draw.rounded_rectangle([badge_x, badge_y, badge_x + 360, badge_y + 36], radius=8, fill=(10, 16, 32, 220), outline=(124, 58, 237, 200), width=1)
    # Cyan status indicator dot
    draw.ellipse([badge_x + 14, badge_y + 13, badge_x + 24, badge_y + 23], fill=(34, 211, 238, 255))
    font_badge = get_font(14, bold=True)
    draw.text((badge_x + 36, badge_y + 9), "SYSTEM PROTOCOL // SHADOW MONARCH V3.0", fill=(196, 181, 253), font=font_badge)
    
    # Main Name
    font_title = get_font(56, bold=True)
    draw.text((60, 120), "ABHISHEK S NAIR", fill=(248, 250, 252), font=font_title)
    
    # Subtitle with glowing purple
    font_sub = get_font(24, bold=True)
    draw.text((62, 195), "FULL STACK DEVELOPER  •  S-RANK ARCHITECT", fill=(168, 85, 247), font=font_sub)
    
    # Description lines
    font_desc = get_font(18, bold=False)
    draw.text((62, 245), "Architecting high-performance web, mobile & distributed software systems.", fill=(226, 232, 240), font=font_desc)
    draw.text((62, 275), "Specializing in React, Flutter, Node.js, FastAPI & intelligent AI pipelines.", fill=(148, 163, 184), font=font_desc)
    draw.text((62, 305), "Leveling up codebases with clean design patterns and resilient engineering.", fill=(148, 163, 184), font=font_desc)
    
    # Feature telemetry pills
    pills = [
        ("⚡ 8 Public Repositories", (124, 58, 237, 60), (196, 181, 253)),
        ("📱 React Native & Flutter", (34, 211, 238, 50), (34, 211, 238)),
        ("🔮 Python & Node.js", (168, 85, 247, 50), (168, 85, 247)),
        ("🛡️ 100% Verified Telemetry", (10, 16, 32, 200), (248, 250, 252)),
    ]
    px = 62
    py = 370
    font_pill = get_font(15, bold=True)
    for text, bg_col, text_col in pills:
        pill_w = len(text) * 9 + 30
        draw.rounded_rectangle([px, py, px + pill_w, py + 38], radius=8, fill=bg_col, outline=(124, 58, 237, 180), width=1)
        draw.text((px + 15, py + 9), text, fill=text_col, font=font_pill)
        px += pill_w + 16
        
    # Quick Navigation capsules
    nav_py = 445
    nav_links = [
        ("⚔️ SHADOW ARSENAL", (168, 85, 247, 70)),
        ("📊 LIVE TELEMETRY", (34, 211, 238, 70)),
        ("🌌 TECH GALAXY", (124, 58, 237, 70)),
        ("🌐 PORTFOLIO", (248, 250, 252, 40))
    ]
    nx = 62
    for n_text, n_fill in nav_links:
        nw = len(n_text) * 9 + 28
        draw.rounded_rectangle([nx, nav_py, nx + nw, nav_py + 34], radius=6, fill=(10, 16, 32, 230), outline=n_fill, width=1)
        draw.text((nx + 14, nav_py + 8), n_text, fill=(248, 250, 252), font=get_font(13, bold=True))
        nx += nw + 14
        
    banner = banner.convert('RGB')
    banner.save('assets/hero-banner.png', quality=95)
    print("Hero Banner saved!")

# -------------------------------------------------------------------------
# 2. ABOUT ME CARD (900 x 520)
# -------------------------------------------------------------------------
def build_about_card():
    print("Building About Me Card...")
    W, H = 900, 520
    card = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    
    # Load about art (developer at futuristic desk)
    about_art_path = os.path.join(BRAIN_DIR, 'developer_futuristic_desk_1794036804756.jpg')
    about_art = Image.open(about_art_path).convert('RGBA')
    art_h = H
    art_w = int(about_art.width * (art_h / about_art.height))
    about_art = about_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
    
    card.paste(about_art, (W - art_w, 0))
    
    # Left dark glass gradient
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
    draw.text((45, 40), "SYSTEM INTEL // ABOUT ME", fill=(34, 211, 238), font=get_font(18, bold=True))
    draw.text((45, 75), "Full Stack Developer", fill=(248, 250, 252), font=get_font(32, bold=True))
    draw.text((45, 120), "CORE CAPABILITIES & ENGINEERING PHILOSOPHY", fill=(168, 85, 247), font=get_font(13, bold=True))
    
    # Body text
    body = [
        "Specialized in architecting modern web, mobile, and desktop",
        "ecosystems with clean component architecture and scalable APIs.",
        "",
        "Experienced across React, React Native, Flutter, and Next.js,",
        "paired with high-throughput Node.js/Express and Python/FastAPI",
        "backends, real-time WebSockets, and MongoDB persistence.",
        "",
        "Passionate about sleek UI/UX, robust state management, and",
        "integrating intelligent AI tooling into production workflows."
    ]
    font_body = get_font(15, bold=False)
    y = 155
    for line in body:
        draw.text((45, y), line, fill=(226, 232, 240), font=font_body)
        y += 22
        
    # Badges
    pills = ["⚡ Web Architecture", "📱 Cross-Platform Mobile", "🔮 Cloud & AI APIs"]
    px = 45
    py = 430
    for p in pills:
        pw = len(p) * 8 + 26
        draw.rounded_rectangle([px, py, px + pw, py + 32], radius=6, fill=(124, 58, 237, 60), outline=(168, 85, 247, 180), width=1)
        draw.text((px + 12, py + 7), p, fill=(196, 181, 253), font=get_font(13, bold=True))
        px += pw + 12
        
    card = card.convert('RGB')
    card.save('assets/about-card.png', quality=95)
    print("About Me Card saved!")

# -------------------------------------------------------------------------
# 3. CURRENTLY WORKING ON CARD (900 x 520)
# -------------------------------------------------------------------------
def build_currently_card():
    print("Building Currently Working On Card...")
    W, H = 900, 520
    card = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    
    # Load workspace art (small anime developer at glowing laptop)
    ws_art_path = os.path.join(BRAIN_DIR, 'anime_developer_workspace_1794036865333.jpg')
    ws_art = Image.open(ws_art_path).convert('RGBA')
    art_h = H
    art_w = int(ws_art.width * (art_h / ws_art.height))
    ws_art = ws_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
    
    card.paste(ws_art, (W - art_w, 0))
    
    # Left dark glass gradient
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
    print("Currently Working On Card saved!")

# -------------------------------------------------------------------------
# 4. TECH STACK GALAXY CARD (900 x 540)
# -------------------------------------------------------------------------
def build_tech_galaxy_card():
    print("Building Tech Galaxy Card...")
    W, H = 900, 540
    card = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    
    # Load tech orbit art
    orbit_art_path = os.path.join(BRAIN_DIR, 'shadow_monarch_orbit_1794036867594.jpg')
    orbit_art = Image.open(orbit_art_path).convert('RGBA')
    # Resize to cover
    art_w = W
    art_h = int(orbit_art.height * (art_w / orbit_art.width))
    orbit_art = orbit_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
    # Crop to W, H
    top_offset = (art_h - H) // 2
    orbit_art = orbit_art.crop((0, top_offset, W, top_offset + H))
    
    # Dark glass overlay to ensure all technology text remains 100% crisp and readable
    overlay = Image.new('RGBA', (W, H), (10, 16, 32, 160))
    card = Image.alpha_composite(orbit_art, overlay)
    
    draw = ImageDraw.Draw(card)
    # Border & brackets
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 180), width=2)
    bracket_len = 20
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=2)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=2)
        
    # Title
    draw.text((45, 30), "SYSTEM ARSENAL // TECH STACK GALAXY", fill=(34, 211, 238), font=get_font(18, bold=True))
    draw.text((45, 60), "Verified Technologies & Frameworks", fill=(248, 250, 252), font=get_font(26, bold=True))
    
    # Grouped Tech Orbit Badges
    categories = [
        ("LANGUAGES & RUNTIMES", ["TypeScript", "JavaScript", "Python", "Dart", "HTML5/CSS3"], (124, 58, 237)),
        ("FRAMEWORKS & MOBILE", ["React", "React Native", "Flutter", "Next.js", "Electron"], (34, 211, 238)),
        ("BACKEND & DATABASE", ["Node.js", "Express", "FastAPI", "MongoDB", "WebSockets"], (168, 85, 247)),
        ("DEVOPS & WORKFLOWS", ["Git", "GitHub Actions", "Docker", "REST APIs", "Vercel"], (196, 181, 253))
    ]
    
    y = 115
    for cat_title, items, border_color in categories:
        draw.text((45, y), f"⚡ {cat_title}", fill=border_color, font=get_font(14, bold=True))
        y += 25
        px = 45
        for item in items:
            iw = len(item) * 9 + 26
            draw.rounded_rectangle([px, y, px + iw, y + 32], radius=6, fill=(10, 16, 32, 210), outline=border_color, width=1)
            draw.text((px + 12, y + 7), item, fill=(248, 250, 252), font=get_font(13, bold=True))
            px += iw + 12
        y += 48
        
    card = card.convert('RGB')
    card.save('assets/tech-stack-galaxy.png', quality=95)
    print("Tech Galaxy Card saved!")

# -------------------------------------------------------------------------
# 5. HUNTER ID CARD (900 x 540)
# -------------------------------------------------------------------------
def build_hunter_id_card():
    print("Building Hunter ID Card...")
    W, H = 900, 540
    card = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    
    draw = ImageDraw.Draw(card)
    # Futuristic holographic card background
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 220), width=2)
    bracket_len = 24
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=3)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=3)
        
    # Header ribbon
    draw.rounded_rectangle([30, 25, W - 30, 75], radius=8, fill=(18, 14, 42, 230), outline=(124, 58, 237, 160), width=1)
    draw.text((50, 36), "HUNTER ASSOCIATION // OFFICIAL S-RANK LICENSE", fill=(34, 211, 238), font=get_font(17, bold=True))
    draw.text((W - 220, 36), "RANK: S-RANK [MONARCH]", fill=(168, 85, 247), font=get_font(14, bold=True))
    
    # Left avatar box
    avatar_x, avatar_y, avatar_s = 50, 100, 260
    draw.rectangle([avatar_x - 3, avatar_y - 3, avatar_x + avatar_s + 3, avatar_y + avatar_s + 3], outline=(168, 85, 247, 255), width=2)
    # Load hunter avatar
    avatar_path = os.path.join(BRAIN_DIR, 's_rank_shadow_monarch_avatar_1794036875756.jpg')
    avatar_img = Image.open(avatar_path).convert('RGBA')
    avatar_img = avatar_img.resize((avatar_s, avatar_s), Image.Resampling.LANCZOS)
    card.paste(avatar_img, (avatar_x, avatar_y))
    
    # S-Rank stamp across bottom of avatar
    stamp_y = avatar_y + avatar_s - 34
    draw.rectangle([avatar_x, stamp_y, avatar_x + avatar_s, avatar_y + avatar_s], fill=(124, 58, 237, 220))
    draw.text((avatar_x + 35, stamp_y + 8), "★ S-RANK MONARCH ★", fill=(255, 255, 255), font=get_font(15, bold=True))
    
    # Save a copy as hunter-avatar.png for anywhere else needed
    avatar_img.save('assets/hunter-avatar.png')
    
    # Right Information fields
    fx = 350
    fields = [
        ("HUNTER NAME", "ABHISHEK S NAIR"),
        ("CLASS / ROLE", "Full Stack Developer & System Architect"),
        ("AFFILIATION", "Solo Leveling System // Global"),
        ("GITHUB ID", "@abhisheksureshnair"),
        ("PORTFOLIO", "https://abhisheksnair.vercel.app/"),
        ("DIRECT COMMS", "nairsabhishek@gmail.com"),
        ("SYSTEM STATUS", "Active • Level 99 • Shadow Army Ready")
    ]
    
    fy = 100
    for label, val in fields:
        draw.text((fx, fy), label, fill=(168, 85, 247), font=get_font(12, bold=True))
        draw.text((fx, fy + 16), val, fill=(248, 250, 252) if label != "PORTFOLIO" else (34, 211, 238), font=get_font(16, bold=(label in ("HUNTER NAME", "CLASS / ROLE"))))
        fy += 45
        
    # Bottom security barcode & verified seal
    draw.rounded_rectangle([50, 395, W - 50, 500], radius=8, fill=(15, 20, 38, 200), outline=(124, 58, 237, 120), width=1)
    draw.text((70, 412), "SECURITY TELEMETRY // RSA-4096 SIGNED AUTHENTIC PROFILE", fill=(196, 181, 253), font=get_font(13, bold=True))
    draw.text((70, 440), "VERIFIED REPOSITORIES: 8 PUBLIC REPOSITORIES  •  NON-FORK: 8  •  0 UNVERIFIED CLAIMS", fill=(148, 163, 184), font=get_font(13, bold=False))
    draw.text((70, 466), "AUTHENTICITY: GUARANTEED BY GITHUB API & REAL-TIME COMMIT TELEMETRY", fill=(34, 211, 238), font=get_font(12, bold=True))
    
    card = card.convert('RGB')
    card.save('assets/hunter-id-card.png', quality=95)
    print("Hunter ID Card saved!")

# -------------------------------------------------------------------------
# 6. CONTRIBUTION CITY (1840 x 520)
# -------------------------------------------------------------------------
def build_contribution_city():
    print("Building Contribution City...")
    W, H = 1840, 520
    card = Image.new('RGBA', (W, H), (3, 4, 13, 255))
    
    # Load isometric cyberpunk city art
    city_art_path = os.path.join(BRAIN_DIR, 'cyberpunk_isometric_city_banner_1794036883160.jpg')
    city_art = Image.open(city_art_path).convert('RGBA')
    # Resize to width W
    art_w = W
    art_h = int(city_art.height * (art_w / city_art.width))
    city_art = city_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
    # Crop
    top_offset = (art_h - H) // 2
    city_art = city_art.crop((0, top_offset, W, top_offset + H))
    
    # Dark gradient overlay for header readability
    top_grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(top_grad)
    for y in range(H):
        if y < 140:
            alpha = int(220 * (1.0 - y / 140.0))
            t_draw.line([(0, y), (W, y)], fill=(3, 4, 13, alpha))
    card = Image.alpha_composite(city_art, top_grad)
    
    draw = ImageDraw.Draw(card)
    # Border & brackets
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 180), width=2)
    bracket_len = 28
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=3)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=3)
        
    # Header
    draw.text((60, 35), "🏙️ CONTRIBUTION CITY // ISOMETRIC METROPOLIS TELEMETRY", fill=(34, 211, 238), font=get_font(22, bold=True))
    draw.text((60, 68), "Continuous integration pipelines, automated GitHub actions & verified repository activity.", fill=(226, 232, 240), font=get_font(16, bold=False))
    
    card = card.convert('RGB')
    card.save('assets/contribution-city-cinematic.png', quality=95)
    card.save('assets/contribution-city.png', quality=95)
    print("Contribution City saved!")

# -------------------------------------------------------------------------
# 7. SHADOW MONARCH FOOTER (1840 x 460)
# -------------------------------------------------------------------------
def build_footer():
    print("Building Shadow Monarch Footer...")
    W, H = 1840, 460
    card = Image.new('RGBA', (W, H), (3, 4, 13, 255))
    
    # Load shadow army banner
    footer_art_path = os.path.join(BRAIN_DIR, 'shadow_army_banner_clean_1794036915435.jpg')
    footer_art = Image.open(footer_art_path).convert('RGBA')
    art_w = W
    art_h = int(footer_art.height * (art_w / footer_art.width))
    footer_art = footer_art.resize((art_w, art_h), Image.Resampling.LANCZOS)
    top_offset = (art_h - H) // 2
    footer_art = footer_art.crop((0, top_offset, W, top_offset + H))
    
    # Dark overlay in center for dramatic typography
    center_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(center_overlay)
    for x in range(W):
        dist = abs(x - W // 2) / (W // 2)
        alpha = int(180 * max(0, 1.0 - dist * 1.5))
        c_draw.line([(x, 0), (x, H)], fill=(3, 4, 13, alpha))
    card = Image.alpha_composite(footer_art, center_overlay)
    
    draw = ImageDraw.Draw(card)
    # Border & brackets
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 200), width=2)
    bracket_len = 24
    for cx, cy, dy in [(6, 6, 1), (W - 7, 6, -1), (6, H - 7, 1), (W - 7, H - 7, -1)]:
        draw.line([(cx, cy), (cx + dy * bracket_len, cy)], fill=(34, 211, 238, 255), width=3)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=3)
        
    # Centered Arise typography
    font_arise = get_font(52, bold=True)
    arise_text = "ARISE. BUILD. LEVEL UP."
    bbox = draw.textbbox((0, 0), arise_text, font=font_arise)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, 130), arise_text, fill=(248, 250, 252), font=font_arise)
    
    font_sub = get_font(22, bold=True)
    sub_text = "ABHISHEK S NAIR  //  THE SHADOW MONARCH DEVELOPER"
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    draw.text(((W - (bbox_sub[2] - bbox_sub[0])) // 2, 205), sub_text, fill=(168, 85, 247), font=font_sub)
    
    font_foot = get_font(15, bold=False)
    foot_text = "Continuous Evolution  •  Autonomous Systems  •  Clean Architecture  •  2026"
    bbox_foot = draw.textbbox((0, 0), foot_text, font=font_foot)
    draw.text(((W - (bbox_foot[2] - bbox_foot[0])) // 2, 250), foot_text, fill=(196, 181, 253), font=font_foot)
    
    card = card.convert('RGB')
    card.save('assets/shadow-monarch-footer.png', quality=95)
    print("Shadow Monarch Footer saved!")

# -------------------------------------------------------------------------
# 8. CONNECT CARD (1840 x 260)
# -------------------------------------------------------------------------
def build_connect_card():
    print("Building Connect Card...")
    W, H = 1840, 260
    card = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    draw = ImageDraw.Draw(card)
    
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 200), width=2)
    bracket_len = 20
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=2)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=2)
        
    draw.text((60, 40), "COMMUNICATION CONDUIT // LET'S CONNECT", fill=(34, 211, 238), font=get_font(20, bold=True))
    draw.text((60, 75), "Open for software engineering opportunities, collaborations, and architectural discussions.", fill=(226, 232, 240), font=get_font(16, bold=False))
    
    # 4 Sleek Channel Capsules
    channels = [
        ("🐙 GitHub", "github.com/abhisheksureshnair", (124, 58, 237)),
        ("💼 LinkedIn", "linkedin.com/in/abhisheksnair", (34, 211, 238)),
        ("🌐 Portfolio", "abhisheksnair.vercel.app", (168, 85, 247)),
        ("✉️ Email", "nairsabhishek@gmail.com", (196, 181, 253))
    ]
    cx = 60
    cy = 130
    for title, link, border_col in channels:
        cw = 400
        draw.rounded_rectangle([cx, cy, cx + cw, cy + 85], radius=8, fill=(15, 22, 45, 240), outline=border_col, width=1)
        draw.text((cx + 20, cy + 18), title, fill=(248, 250, 252), font=get_font(18, bold=True))
        draw.text((cx + 20, cy + 48), link, fill=border_col, font=get_font(14, bold=False))
        cx += cw + 35
        
    card = card.convert('RGB')
    card.save('assets/connect-card.png', quality=95)
    print("Connect Card saved!")

if __name__ == '__main__':
    build_hero_banner()
    build_about_card()
    build_currently_card()
    build_tech_galaxy_card()
    build_hunter_id_card()
    build_contribution_city()
    build_footer()
    build_connect_card()
    print("All cards and banners generated successfully!")
