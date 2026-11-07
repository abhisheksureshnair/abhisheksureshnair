import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from scipy.ndimage import label, gaussian_filter

def extract_character(img_path):
    img = Image.open(img_path).convert('RGBA')
    arr = np.array(img, dtype=np.float32)
    rgb = arr[:, :, :3]
    brightness = np.mean(rgb, axis=2)
    max_c = np.max(rgb, axis=2)
    min_c = np.min(rgb, axis=2)
    saturation = np.where(max_c > 0, (max_c - min_c) / np.maximum(max_c, 1), 0)
    is_white = (brightness > 225) & (saturation < 0.18)
    labeled, _ = label(is_white)
    border_labels = set(labeled[0, :]).union(labeled[-1, :]).union(labeled[:, 0]).union(labeled[:, -1])
    border_labels.discard(0)
    is_outer_bg = np.isin(labeled, list(border_labels))
    alpha = np.ones((arr.shape[0], arr.shape[1]), dtype=np.uint8) * 255
    alpha[is_outer_bg] = 0
    alpha_smooth = gaussian_filter(alpha.astype(np.float32), sigma=0.8)
    alpha_final = np.clip(alpha_smooth, 0, 255).astype(np.uint8)
    res = Image.fromarray(np.dstack([arr[:, :, :3].astype(np.uint8), alpha_final]), mode='RGBA')
    bbox = res.getbbox()
    return res.crop(bbox)

def make_transparent_gif(frames, output_path, duration=90):
    """
    Saves an animated GIF with crisp transparency and 0 trail artifacts.
    Uses adaptive palette with index 0 reserved for pure transparency.
    """
    processed = []
    for frame in frames:
        # Convert RGBA to palette with transparent background
        alpha = frame.split()[3]
        # Create a mask of fully transparent pixels
        mask = Image.eval(alpha, lambda a: 255 if a < 128 else 0)
        
        # Color quantize RGB to 255 colors
        rgb = frame.convert('RGB')
        p_frame = rgb.convert('P', palette=Image.ADAPTIVE, colors=255)
        
        # Shift palette indices by 1 to make index 0 transparent
        p_arr = np.array(p_frame, dtype=np.uint8)
        p_arr = np.clip(p_arr + 1, 1, 255)
        
        # Where mask is 255, set to index 0
        mask_arr = np.array(mask, dtype=bool)
        p_arr[mask_arr] = 0
        
        # Create output image
        out_img = Image.fromarray(p_arr, mode='P')
        
        # Build palette
        pal = p_frame.getpalette()
        # Prepend transparent color (black or dark purple) at index 0
        new_pal = [10, 16, 32] + pal[:255*3]
        out_img.putpalette(new_pal)
        
        out_img.info['transparency'] = 0
        out_img.info['duration'] = duration
        out_img.info['disposal'] = 2
        processed.append(out_img)
        
    processed[0].save(
        output_path,
        save_all=True,
        append_images=processed[1:],
        duration=duration,
        loop=0,
        transparency=0,
        disposal=2,
        optimize=False
    )
    print(f"Saved {output_path}: {len(processed)} frames, {os.path.getsize(output_path)} bytes")

# =========================================================================
# MASCOT 1: IDLE SHADOW MONARCH (User Referral Image)
# =========================================================================
def generate_mascot1():
    print("Generating Mascot 1: Idle Shadow Monarch...")
    ref_path = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a/.user_uploaded/media_1794036534386_8294df51.jpg'
    char = extract_character(ref_path)
    
    # Target canvas
    CANVAS_W, CANVAS_H = 320, 340
    # Scale character to fit nicely
    target_h = 270
    target_w = int(char.width * (target_h / char.height))
    char = char.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Locate face/eye region on resized character
    # Original eyes were at y: 101..118, x: 253..308 on 610x610 (char crop was ~ 564x549)
    # Scaled to target_w, target_h:
    scale_y = target_h / 549.0
    scale_x = target_w / 564.0
    eye_y1 = int(95 * scale_y)
    eye_y2 = int(115 * scale_y)
    eye_lx = int(248 * scale_x)
    eye_rx = int(295 * scale_x)
    
    N_FRAMES = 18
    frames = []
    
    # Pre-generate floating soul particles (looping smoothly)
    random.seed(42)
    particles = []
    for _ in range(12):
        particles.append({
            'base_x': random.uniform(20, CANVAS_W - 20),
            'start_y': random.uniform(CANVAS_H - 70, CANVAS_H + 20),
            'speed': random.uniform(40, 70),
            'radius': random.uniform(1.8, 3.5),
            'wobble_freq': random.uniform(1, 3),
            'phase': random.uniform(0, math.pi * 2)
        })
    
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        angle = 2 * math.pi * t
        
        # Breathing: subtle vertical expansion of torso
        # Sine wave breathing offset
        breath_dy = math.sin(angle) * 2.2
        breath_scale_y = 1.0 + 0.012 * math.sin(angle)
        
        # Rescale character slightly for breathing
        cur_h = int(target_h * breath_scale_y)
        frame_char = char.resize((target_w, cur_h), Image.Resampling.BILINEAR)
        
        # Position on canvas
        char_x = (CANVAS_W - target_w) // 2
        char_y = int(CANVAS_H - cur_h - 15 - breath_dy)
        
        # Create RGBA canvas
        frame = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # 1. Background violet aura pulse
        aura_intensity = 0.5 + 0.5 * math.sin(angle)
        aura_radius_x = target_w * 0.48 + 8 * aura_intensity
        aura_radius_y = target_h * 0.50 + 10 * aura_intensity
        aura_center_x = CANVAS_W // 2
        aura_center_y = char_y + int(cur_h * 0.5)
        
        # Draw soft glowing ellipse aura behind
        aura_layer = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        aura_draw = ImageDraw.Draw(aura_layer)
        for r_step in range(4):
            frac = (4 - r_step) / 4.0
            rx = int(aura_radius_x * (1.0 + frac * 0.25))
            ry = int(aura_radius_y * (1.0 + frac * 0.25))
            alpha = int(45 * aura_intensity * (1.0 - frac * 0.6))
            aura_draw.ellipse(
                [aura_center_x - rx, aura_center_y - ry, aura_center_x + rx, aura_center_y + ry],
                fill=(124, 58, 237, alpha)
            )
        aura_layer = aura_layer.filter(ImageFilter.GaussianBlur(10))
        frame.paste(aura_layer, (0, 0), aura_layer)
        
        # 2. Floating soul particles rising upward
        for p in particles:
            # Loop particle position
            py = (p['start_y'] - p['speed'] * t) % (CANVAS_H - 30) + 30
            px = p['base_x'] + math.sin(angle * p['wobble_freq'] + p['phase']) * 6
            p_alpha = int(220 * math.sin(math.pi * ((py - 30) / (CANVAS_H - 60))))
            p_alpha = max(0, min(255, p_alpha))
            
            # Particle color: electric violet #A855F7 and cyan highlights
            p_color = (168, 85, 247, p_alpha) if p['base_x'] % 2 == 0 else (34, 211, 238, p_alpha)
            pr = p['radius']
            draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=p_color)
            draw.ellipse([px - pr*0.5, py - pr*0.5, px + pr*0.5, py + pr*0.5], fill=(255, 255, 255, p_alpha))
        
        # 3. Paste character
        # Modify eyes for blinking:
        # Blink happens around frame 13, 14, 15
        char_copy = frame_char.copy()
        if i in (13, 14, 15):
            # Eye blink overlay: draw closed eyelids (dark skin/shadow line)
            char_draw = ImageDraw.Draw(char_copy)
            ey = int(eye_y1 * breath_scale_y)
            # Left eye
            char_draw.rectangle([eye_lx - 12, ey - 2, eye_lx + 14, ey + 10], fill=(210, 160, 130, 255))
            char_draw.line([eye_lx - 10, ey + 4, eye_lx + 12, ey + 4], fill=(50, 30, 60, 255), width=2)
            # Right eye
            char_draw.rectangle([eye_rx - 12, ey - 4, eye_rx + 14, ey + 8], fill=(210, 160, 130, 255))
            char_draw.line([eye_rx - 10, ey + 2, eye_rx + 12, ey + 2], fill=(50, 30, 60, 255), width=2)
        elif i in (12, 16):
            # Eye glow pulse flare!
            char_draw = ImageDraw.Draw(char_copy)
            ey = int(eye_y1 * breath_scale_y)
            # Luminous eye glow flare
            char_draw.ellipse([eye_lx - 5, ey - 2, eye_lx + 7, ey + 10], fill=(230, 180, 255, 200))
            char_draw.ellipse([eye_rx - 5, ey - 4, eye_rx + 7, ey + 8], fill=(230, 180, 255, 200))
        
        frame.paste(char_copy, (char_x, char_y), char_copy)
        
        # 4. Foreground swirling shadow mist at feet
        mist_layer = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        mist_draw = ImageDraw.Draw(mist_layer)
        for m in range(5):
            mx = char_x + int(target_w * (0.2 + 0.15 * m)) + int(math.sin(angle + m) * 8)
            my = char_y + cur_h - 10 + int(math.cos(angle * 1.5 + m) * 4)
            m_rad = 12 + 4 * math.sin(angle + m)
            mist_draw.ellipse([mx - m_rad, my - m_rad*0.5, mx + m_rad, my + m_rad*0.5], fill=(168, 85, 247, 80))
        mist_layer = mist_layer.filter(ImageFilter.GaussianBlur(5))
        frame.paste(mist_layer, (0, 0), mist_layer)
        
        frames.append(frame)
        
    make_transparent_gif(frames, 'assets/animations/chibi-idle.gif', duration=90)
    make_transparent_gif(frames, 'assets/monarch/chibi-idle.gif', duration=90)
    # Also save static png companion
    frames[0].save('assets/monarch/chibi-idle.png')
    print("Mascot 1 completed successfully!")

if __name__ == '__main__':
    generate_mascot1()

# =========================================================================
# MASCOT 2: CODING CHIBI
# =========================================================================
def generate_mascot2():
    print("Generating Mascot 2: Coding Chibi...")
    coder_path = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a/chibi_jinwoo_coder_1794036895375.jpg'
    char = extract_character(coder_path)
    
    CANVAS_W, CANVAS_H = 340, 340
    target_h = 270
    target_w = int(char.width * (target_h / char.height))
    char = char.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    N_FRAMES = 18
    frames = []
    
    # Floating code runes
    code_symbols = ['{ }', '< >', '0 1', 'λ', '⚡', '/*', '*/', 'fn()', '=>']
    random.seed(101)
    runes = []
    for _ in range(8):
        runes.append({
            'symbol': random.choice(code_symbols),
            'start_x': random.uniform(CANVAS_W * 0.4, CANVAS_W * 0.7),
            'start_y': CANVAS_H * 0.65,
            'speed': random.uniform(45, 75),
            'drift': random.uniform(-15, 15),
            'phase': random.uniform(0, math.pi * 2)
        })
        
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        angle = 2 * math.pi * t
        
        # Typing bounce: fast rhythm (3 cycles per loop)
        typing_cycle = math.sin(angle * 3)
        ty_offset = typing_cycle * 1.5
        
        char_x = (CANVAS_W - target_w) // 2
        char_y = int(CANVAS_H - target_h - 15 + ty_offset)
        
        frame = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # 1. Screen glow pulse
        glow_pulse = 0.5 + 0.5 * math.sin(angle * 2)
        glow_layer = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        glow_color = (34, 211, 238, int(80 * glow_pulse)) if i % 2 == 0 else (168, 85, 247, int(90 * glow_pulse))
        glow_draw.ellipse([CANVAS_W * 0.35, CANVAS_H * 0.5, CANVAS_W * 0.75, CANVAS_H * 0.85], fill=glow_color)
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(15))
        frame.paste(glow_layer, (0, 0), glow_layer)
        
        # 2. Paste character
        frame.paste(char, (char_x, char_y), char)
        
        # 3. Dynamic typing hands effect: alternating keystroke sparks
        spark_x = char_x + int(target_w * 0.52) + (5 if typing_cycle > 0 else -5)
        spark_y = char_y + int(target_h * 0.72)
        draw.ellipse([spark_x - 3, spark_y - 2, spark_x + 3, spark_y + 2], fill=(255, 255, 255, 220))
        draw.ellipse([spark_x - 5, spark_y - 3, spark_x + 5, spark_y + 3], fill=(34, 211, 238, 140))
        
        # 4. Floating code runes
        for r in runes:
            ry = (r['start_y'] - r['speed'] * t) % (CANVAS_H * 0.55) + (CANVAS_H * 0.15)
            rx = r['start_x'] + math.sin(angle * 2 + r['phase']) * r['drift']
            r_alpha = int(240 * math.sin(math.pi * ((ry - CANVAS_H * 0.15) / (CANVAS_H * 0.55))))
            r_alpha = max(0, min(255, r_alpha))
            draw.text((rx, ry), r['symbol'], fill=(196, 181, 253, r_alpha))
            
        frames.append(frame)
        
    make_transparent_gif(frames, 'assets/animations/chibi-typing.gif', duration=85)
    print("Mascot 2 completed successfully!")

# =========================================================================
# MASCOT 3: VICTORY DANCE CHIBI
# =========================================================================
def generate_mascot3():
    print("Generating Mascot 3: Victory Dance Chibi...")
    victory_path = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a/chibi_jinwoo_victory_1794036900512.jpg'
    char = extract_character(victory_path)
    
    CANVAS_W, CANVAS_H = 320, 360
    target_h = 265
    target_w = int(char.width * (target_h / char.height))
    char = char.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    N_FRAMES = 18
    frames = []
    
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        angle = 2 * math.pi * t
        
        # Victory dance: energetic jump + side tilt
        jump_dy = -abs(math.sin(angle * 2)) * 14.0
        tilt_deg = math.sin(angle) * 3.5
        
        # Rotate character
        rotated = char.rotate(tilt_deg, resample=Image.Resampling.BICUBIC, expand=True)
        
        frame = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        char_x = (CANVAS_W - rotated.width) // 2
        char_y = int(CANVAS_H - rotated.height - 25 + jump_dy)
        
        # 1. Dance ground shadow (shrinks when jumping)
        shadow_w = int(target_w * 0.55 * (1.0 - abs(jump_dy) / 28.0))
        shadow_h = int(12 * (1.0 - abs(jump_dy) / 28.0))
        shadow_x = CANVAS_W // 2
        shadow_y = CANVAS_H - 18
        draw.ellipse([shadow_x - shadow_w, shadow_y - shadow_h, shadow_x + shadow_w, shadow_y + shadow_h], fill=(124, 58, 237, 70))
        
        # 2. Victory energy sparks around character
        for s in range(8):
            s_ang = angle * 2 + s * (math.pi / 4)
            dist = 50 + 15 * math.sin(angle * 3 + s)
            sx = CANVAS_W // 2 + math.cos(s_ang) * dist
            sy = char_y + target_h * 0.45 + math.sin(s_ang) * dist
            draw.line([sx - 3, sy, sx + 3, sy], fill=(248, 250, 252, 220), width=2)
            draw.line([sx, sy - 3, sx, sy + 3], fill=(168, 85, 247, 220), width=2)
            
        # 3. Paste character
        frame.paste(rotated, (char_x, char_y), rotated)
        
        frames.append(frame)
        
    make_transparent_gif(frames, 'assets/animations/chibi-dancing.gif', duration=80)
    make_transparent_gif(frames, 'assets/monarch/chibi-dancing.gif', duration=80)
    frames[0].save('assets/monarch/chibi-dancing.png')
    print("Mascot 3 completed successfully!")

# =========================================================================
# MASCOT 4: SHADOW SOLDIER CHIBI
# =========================================================================
def generate_mascot4():
    print("Generating Mascot 4: Shadow Soldier Chibi...")
    soldier_path = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a/chibi_shadow_knight_1794036917440.jpg'
    char = extract_character(soldier_path)
    
    CANVAS_W, CANVAS_H = 320, 360
    target_h = 280
    target_w = int(char.width * (target_h / char.height))
    char = char.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    N_FRAMES = 18
    frames = []
    
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        angle = 2 * math.pi * t
        
        # Gentle armor breathing
        breath_scale = 1.0 + 0.015 * math.sin(angle)
        cur_h = int(target_h * breath_scale)
        scaled_char = char.resize((target_w, cur_h), Image.Resampling.BILINEAR)
        
        char_x = (CANVAS_W - target_w) // 2
        char_y = int(CANVAS_H - cur_h - 12)
        
        frame = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # 1. Swirling violet flame aura behind soldier
        flame_layer = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        flame_draw = ImageDraw.Draw(flame_layer)
        for f in range(6):
            fx = char_x + int(target_w * (0.2 + 0.12 * f)) + int(math.sin(angle * 2 + f) * 10)
            fy = char_y + int(cur_h * (0.3 + 0.1 * f)) + int(math.cos(angle * 2 + f) * 8)
            fr = 20 + 8 * math.sin(angle + f)
            flame_draw.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=(124, 58, 237, 75))
            flame_draw.ellipse([fx - fr*0.5, fy - fr*0.5, fx + fr*0.5, fy + fr*0.5], fill=(168, 85, 247, 95))
        flame_layer = flame_layer.filter(ImageFilter.GaussianBlur(8))
        frame.paste(flame_layer, (0, 0), flame_layer)
        
        # 2. Paste character
        frame.paste(scaled_char, (char_x, char_y), scaled_char)
        
        # 3. Pulsing violet eye glow flare
        eye_pulse = 0.5 + 0.5 * math.sin(angle * 2)
        eye_alpha = int(140 + 115 * eye_pulse)
        # Eye locations on knight helmet
        ex1, ey1 = char_x + int(target_w * 0.44), char_y + int(cur_h * 0.28)
        ex2, ey2 = char_x + int(target_w * 0.56), char_y + int(cur_h * 0.28)
        draw.ellipse([ex1 - 4, ey1 - 4, ex1 + 4, ey1 + 4], fill=(220, 160, 255, eye_alpha))
        draw.ellipse([ex2 - 4, ey2 - 4, ex2 + 4, ey2 + 4], fill=(220, 160, 255, eye_alpha))
        draw.ellipse([ex1 - 1, ey1 - 1, ex1 + 1, ey1 + 1], fill=(255, 255, 255, eye_alpha))
        draw.ellipse([ex2 - 1, ey2 - 1, ex2 + 1, ey2 + 1], fill=(255, 255, 255, eye_alpha))
        
        frames.append(frame)
        
    make_transparent_gif(frames, 'assets/animations/shadow-soldier.gif', duration=90)
    make_transparent_gif(frames, 'assets/monarch/shadow-soldier.gif', duration=90)
    frames[0].save('assets/monarch/shadow-soldier.png')
    print("Mascot 4 completed successfully!")

