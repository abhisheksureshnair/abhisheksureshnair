import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from scipy.ndimage import label, gaussian_filter

def extract_clean_coder(img_path):
    img = Image.open(img_path).convert('RGBA')
    arr = np.array(img, dtype=np.float32)
    rgb = arr[:, :, :3]
    
    # 1. Clean the knee/pant region where the old misplaced dot was:
    # On 644x596, the knee area is y: 385..405, x: 345..375
    knee_crop = rgb[385:405, 345:375]
    # Replace any stray cyan/light pixels with the surrounding dark pant color
    pant_mask = np.mean(knee_crop, axis=2) > 65
    arr[385:405, 345:375][pant_mask] = [18, 20, 28, 255]
    
    # 2. Extract transparent background:
    # Outer background is dark: RGB around [13, 16, 21]
    diff = np.max(np.abs(arr[:, :, :3] - np.array([13, 16, 21])), axis=2)
    is_bg = diff < 14
    
    labeled, _ = label(is_bg)
    border_labels = set(labeled[0, :]).union(labeled[-1, :]).union(labeled[:, 0]).union(labeled[:, -1])
    border_labels.discard(0)
    is_outer_bg = np.isin(labeled, list(border_labels))
    
    alpha = np.ones((arr.shape[0], arr.shape[1]), dtype=np.uint8) * 255
    alpha[is_outer_bg] = 0
    
    alpha_smooth = gaussian_filter(alpha.astype(np.float32), sigma=0.8)
    alpha_final = np.clip(alpha_smooth, 0, 255).astype(np.uint8)
    
    return Image.fromarray(np.dstack([arr[:, :, :3].astype(np.uint8), alpha_final]), mode='RGBA')

def build_perfect_coder_gif():
    print("Generating perfected Solo Coder typing animation...")
    src_path = '/Users/innsparksolutions/.gemini/antigravity/brain/fedc8984-56d5-42c1-9f49-84e428da5c7a/.user_uploaded/media_1794038279433_17c36036.jpg'
    char_raw = extract_clean_coder(src_path)
    
    CANVAS_W, CANVAS_H = 340, 340
    target_w = 340
    target_h = int(char_raw.height * (target_w / char_raw.width)) # ~314
    char = char_raw.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    char_x = 0
    char_y = (CANVAS_H - target_h) // 2 # 13
    
    s = target_w / char_raw.width
    # Verified keyboard landmarks:
    # Center of keyboard keys: x = 181, y = 183
    # Left hand typing area: x = 173, y = 182
    # Right hand typing area: x = 189, y = 182
    kbd_x = char_x + int(343 * s) # 181
    kbd_y = char_y + int(323 * s) # 183
    
    # Holographic code panel bounds:
    holo_x1 = char_x + int(150 * s) # 79
    holo_y1 = char_y + int(190 * s) # 113
    holo_x2 = char_x + int(310 * s) # 164
    holo_y2 = char_y + int(270 * s) # 155
    
    # Eye coordinates:
    leye_x = char_x + int(321 * s) # 169
    leye_y = char_y + int(195 * s) # 115
    reye_x = char_x + int(387 * s) # 204
    reye_y = char_y + int(192 * s) # 114
    
    N_FRAMES = 18
    frames = []
    
    # Code spark particles strictly floating upward from keyboard
    random.seed(555)
    particles = []
    for _ in range(8):
        particles.append({
            'base_x': random.uniform(kbd_x - 14, kbd_x + 14),
            'start_y': kbd_y - 4,
            'max_h': random.uniform(40, 75),
            'speed': random.uniform(45, 75),
            'radius': random.uniform(1.0, 2.0),
            'drift': random.uniform(-6, 6),
            'color': random.choice([(168, 85, 247), (196, 181, 253), (34, 211, 238), (255, 255, 255)])
        })
        
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        angle = 2 * math.pi * t
        
        # Subtle posture breathing
        breath_dy = math.sin(angle) * 1.0
        cur_y = int(char_y + breath_dy)
        
        frame = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # Background screen glow behind laptop
        screen_glow_pulse = 0.5 + 0.5 * math.sin(angle * 2)
        glow_layer = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        glow_draw.ellipse(
            [kbd_x - 45, kbd_y - 50, kbd_x + 45, kbd_y + 5],
            fill=(124, 58, 237, int(45 * screen_glow_pulse))
        )
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(10))
        frame.paste(glow_layer, (0, 0), glow_layer)
        
        # Character copy
        char_copy = char.copy()
        
        # Natural blinking at frames 12, 13, 14
        if i in (12, 13, 14):
            char_draw = ImageDraw.Draw(char_copy)
            char_draw.rectangle([leye_x - 7, leye_y - 2, leye_x + 7, leye_y + 5], fill=(225, 180, 155, 255))
            char_draw.line([leye_x - 6, leye_y + 2, leye_x + 6, leye_y + 2], fill=(45, 25, 60, 255), width=2)
            char_draw.rectangle([reye_x - 7, reye_y - 2, reye_x + 7, reye_y + 5], fill=(225, 180, 155, 255))
            char_draw.line([reye_x - 6, reye_y + 2, reye_x + 6, reye_y + 2], fill=(45, 25, 60, 255), width=2)
        elif i in (11, 15):
            char_draw = ImageDraw.Draw(char_copy)
            char_draw.ellipse([leye_x - 2, leye_y, leye_x + 4, leye_y + 6], fill=(240, 210, 255, 190))
            char_draw.ellipse([reye_x - 2, reye_y, reye_x + 4, reye_y + 6], fill=(240, 210, 255, 190))
            
        frame.paste(char_copy, (char_x, cur_y), char_copy)
        
        # KEYSTROKE TYPING MOTION:
        # Fast typing rhythm: 4 keystroke cycles per loop
        type_cycle = math.sin(angle * 4)
        
        # Correctly position keystroke hits directly on the keyboard keys!
        # Left hand key tap: x = 173, y = 182
        # Right hand key tap: x = 189, y = 182
        if type_cycle > 0.25:
            # Right hand key tap!
            rx = kbd_x + 8
            ry = kbd_y - 1
            draw.ellipse([rx - 2.5, ry - 1.5, rx + 2.5, ry + 1.5], fill=(255, 255, 255, 255))
            draw.ellipse([rx - 5, ry - 3, rx + 5, ry + 3], fill=(168, 85, 247, 160))
        elif type_cycle < -0.25:
            # Left hand key tap!
            lx = kbd_x - 8
            ly = kbd_y - 1
            draw.ellipse([lx - 2.5, ly - 1.5, lx + 2.5, ly + 1.5], fill=(255, 255, 255, 255))
            draw.ellipse([lx - 5, ly - 3, lx + 5, ly + 3], fill=(34, 211, 238, 160))
            
        # Holographic code scan line
        scan_y = holo_y1 + int(((i * 3.2) % (holo_y2 - holo_y1)))
        draw.line([(holo_x1 + 6, scan_y), (holo_x2 - 6, scan_y)], fill=(220, 180, 255, 110), width=1)
        
        # Rising code particles (only from keyboard moving up)
        for p in particles:
            dist_up = (p['speed'] * t) % p['max_h']
            py = p['start_y'] - dist_up
            px = p['base_x'] + math.sin(angle * 2 + dist_up * 0.1) * p['drift']
            alpha = int(240 * (1.0 - (dist_up / p['max_h'])))
            r = p['radius']
            draw.ellipse([px - r, py - r, px + r, py + r], fill=p['color'] + (alpha,))
            draw.ellipse([px - r*0.5, py - r*0.5, px + r*0.5, py + r*0.5], fill=(255, 255, 255, alpha))
            
        frames.append(frame)
        
    # Save as animated transparent GIF
    processed = []
    for frame in frames:
        alpha = frame.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a < 128 else 0)
        rgb = frame.convert('RGB')
        p_frame = rgb.convert('P', palette=Image.ADAPTIVE, colors=255)
        p_arr = np.array(p_frame, dtype=np.uint8)
        p_arr = np.clip(p_arr + 1, 1, 255)
        p_arr[np.array(mask, dtype=bool)] = 0
        out_img = Image.fromarray(p_arr, mode='P')
        pal = p_frame.getpalette()
        out_img.putpalette([13, 16, 21] + pal[:255*3])
        out_img.info['transparency'] = 0
        out_img.info['duration'] = 85
        out_img.info['disposal'] = 2
        processed.append(out_img)
        
    for path in ['assets/animations/chibi-typing.gif', 'assets/monarch/chibi-typing.gif']:
        processed[0].save(
            path,
            save_all=True,
            append_images=processed[1:],
            duration=85,
            loop=0,
            transparency=0,
            disposal=2
        )
        print(f"Saved {path} successfully!")
        
    frames[0].save('assets/chibi-laptop.png')
    print("Saved assets/chibi-laptop.png!")

if __name__ == '__main__':
    build_perfect_coder_gif()
