from PIL import Image, ImageDraw, ImageFilter

def build_tech_stack():
    print("Building Tech Stack Galaxy from reference image 4...")
    ref_path = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a/.user_uploaded/media_1794038166166_14b170df.jpg'
    ref_img = Image.open(ref_path).convert('RGBA')
    
    # Target size: 900 x 520
    W, H = 900, 520
    card = Image.new('RGBA', (W, H), (10, 16, 32, 255))
    
    # Scale ref_img to fit within W, H
    # ref is 1024 x 444 (ratio 2.30)
    # We can fit ref_img centered or resize it smoothly
    scale = min(W / ref_img.width, H / ref_img.height)
    new_w = int(ref_img.width * scale)
    new_h = int(ref_img.height * scale)
    resized_ref = ref_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Paste centered
    offset_x = (W - new_w) // 2
    offset_y = (H - new_h) // 2
    card.paste(resized_ref, (offset_x, offset_y))
    
    # Outer theme border & brackets
    draw = ImageDraw.Draw(card)
    draw.rectangle([4, 4, W - 5, H - 5], outline=(124, 58, 237, 200), width=2)
    bracket_len = 22
    for cx, cy, dx, dy in [(6, 6, 1, 1), (W - 7, 6, -1, 1), (6, H - 7, 1, -1), (W - 7, H - 7, -1, -1)]:
        draw.line([(cx, cy), (cx + dx * bracket_len, cy)], fill=(34, 211, 238, 255), width=3)
        draw.line([(cx, cy), (cx, cy + dy * bracket_len)], fill=(34, 211, 238, 255), width=3)
        
    card = card.convert('RGB')
    card.save('assets/tech-stack-galaxy.png', quality=95)
    print("Tech Stack Galaxy updated to match Image 4!")

if __name__ == '__main__':
    build_tech_stack()
