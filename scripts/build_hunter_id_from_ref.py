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

def build_hunter_id():
    print("Building Hunter ID Card from reference image 5...")
    W, H = 900, 520
    card = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    draw = ImageDraw.Draw(card)
    
    # Outer frame and corner brackets
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 220), width=2)
    bracket_len = 24
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=3)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=3)
        
    # Header ribbon
    draw.rounded_rectangle([30, 20, W - 30, 70], radius=8, fill=(18, 14, 42, 230), outline=(124, 58, 237, 180), width=1)
    draw.text((50, 32), "HUNTER ASSOCIATION // OFFICIAL S-RANK LICENSE", fill=(34, 211, 238), font=get_font(17, bold=True))
    draw.text((W - 225, 32), "RANK: S-RANK [MONARCH]", fill=(168, 85, 247), font=get_font(14, bold=True))
    
    # Load Image 5 (Hunter Portrait with purple aura & glowing eyes)
    ref_avatar_path = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a/.user_uploaded/media_1794038191340_b5b4001a.jpg'
    avatar_src = Image.open(ref_avatar_path).convert('RGBA')
    
    # Save a clean copy as hunter-avatar.png
    avatar_src.save('assets/hunter-avatar.png')
    
    # Target avatar box dimensions
    av_x, av_y = 50, 90
    av_w, av_h = 240, 280
    
    # Scale avatar_src to cover av_w, av_h
    scale = max(av_w / avatar_src.width, av_h / avatar_src.height)
    scaled_w = int(avatar_src.width * scale)
    scaled_h = int(avatar_src.height * scale)
    scaled_avatar = avatar_src.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
    
    crop_x = (scaled_w - av_w) // 2
    crop_y = (scaled_h - av_h) // 2
    cropped_avatar = scaled_avatar.crop((crop_x, crop_y, crop_x + av_w, crop_y + av_h))
    
    # Paste avatar and draw neon border
    card.paste(cropped_avatar, (av_x, av_y))
    draw.rectangle([av_x - 2, av_y - 2, av_x + av_w + 2, av_y + av_h + 2], outline=(168, 85, 247, 255), width=2)
    
    # S-Rank stamp across bottom of avatar
    stamp_y = av_y + av_h - 32
    draw.rectangle([av_x, stamp_y, av_x + av_w, av_y + av_h], fill=(124, 58, 237, 230))
    draw.text((av_x + 30, stamp_y + 7), "★ S-RANK MONARCH ★", fill=(255, 255, 255), font=get_font(14, bold=True))
    
    # Right Information fields
    fx = 330
    fields = [
        ("HUNTER NAME", "ABHISHEK S NAIR"),
        ("CLASS / ROLE", "Full Stack Developer & System Architect"),
        ("AFFILIATION", "Solo Leveling System // Global"),
        ("GITHUB ID", "@abhisheksureshnair"),
        ("PORTFOLIO", "https://abhisheksnair.vercel.app/"),
        ("DIRECT COMMS", "nairsabhishek@gmail.com"),
        ("SYSTEM STATUS", "Active • Level 99 • Shadow Army Ready")
    ]
    
    fy = 90
    for label, val in fields:
        draw.text((fx, fy), label, fill=(168, 85, 247), font=get_font(11, bold=True))
        draw.text((fx, fy + 15), val, fill=(248, 250, 252) if label != "PORTFOLIO" else (34, 211, 238), font=get_font(15, bold=(label in ("HUNTER NAME", "CLASS / ROLE"))))
        fy += 42
        
    # Bottom security barcode & verified seal
    draw.rounded_rectangle([50, 395, W - 50, 495], radius=8, fill=(15, 20, 38, 200), outline=(124, 58, 237, 120), width=1)
    draw.text((70, 410), "SECURITY TELEMETRY // RSA-4096 SIGNED AUTHENTIC LICENSE", fill=(196, 181, 253), font=get_font(13, bold=True))
    draw.text((70, 436), "VERIFIED REPOSITORIES: 8 PUBLIC REPOSITORIES  •  NON-FORK: 8  •  0 UNVERIFIED CLAIMS", fill=(148, 163, 184), font=get_font(13, bold=False))
    draw.text((70, 462), "AUTHENTICITY: GUARANTEED BY GITHUB API & REAL-TIME COMMIT TELEMETRY", fill=(34, 211, 238), font=get_font(12, bold=True))
    
    card = card.convert('RGB')
    card.save('assets/hunter-id-card.png', quality=95)
    print("Hunter ID Card updated with Image 5 avatar!")

if __name__ == '__main__':
    build_hunter_id()
