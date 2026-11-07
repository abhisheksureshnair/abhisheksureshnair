import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def make_particles_gif():
    print("Generating Shadow Particles GIF (480 x 140)...")
    W, H = 480, 140
    N_FRAMES = 20
    
    random.seed(999)
    particles = []
    for _ in range(35):
        particles.append({
            'base_x': random.uniform(10, W - 10),
            'start_y': random.uniform(H * 0.4, H + 20),
            'speed': random.uniform(30, 60),
            'radius': random.uniform(1.5, 3.5),
            'freq': random.uniform(1, 3),
            'phase': random.uniform(0, math.pi * 2),
            'color_type': random.choice(['purple', 'violet', 'cyan'])
        })
        
    frames = []
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        angle = 2 * math.pi * t
        
        frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # Soft ambient purple mist at bottom
        mist = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        m_draw = ImageDraw.Draw(mist)
        for m in range(4):
            mx = int(W * (0.2 + 0.2 * m)) + int(math.sin(angle + m) * 15)
            my = H - 15 + int(math.cos(angle + m) * 5)
            m_draw.ellipse([mx - 60, my - 25, mx + 60, my + 25], fill=(124, 58, 237, 45))
        mist = mist.filter(ImageFilter.GaussianBlur(12))
        frame.paste(mist, (0, 0), mist)
        
        # Draw rising particles
        for p in particles:
            py = (p['start_y'] - p['speed'] * t) % H
            px = p['base_x'] + math.sin(angle * p['freq'] + p['phase']) * 12
            
            # Opacity fades near top and bottom
            fade = math.sin(math.pi * (py / H))
            alpha = int(230 * max(0, min(1, fade)))
            
            if p['color_type'] == 'purple':
                col = (124, 58, 237, alpha)
            elif p['color_type'] == 'violet':
                col = (168, 85, 247, alpha)
            else:
                col = (34, 211, 238, alpha)
                
            r = p['radius']
            draw.ellipse([px - r, py - r, px + r, py + r], fill=col)
            draw.ellipse([px - r*0.5, py - r*0.5, px + r*0.5, py + r*0.5], fill=(255, 255, 255, alpha))
            
        # Convert to palette with transparency
        alpha_channel = frame.split()[3]
        mask = Image.eval(alpha_channel, lambda a: 255 if a < 40 else 0)
        p_frame = frame.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        p_arr = np.array(p_frame, dtype=np.uint8)
        p_arr = np.clip(p_arr + 1, 1, 255)
        p_arr[np.array(mask, dtype=bool)] = 0
        out_img = Image.fromarray(p_arr, mode='P')
        pal = p_frame.getpalette()
        out_img.putpalette([10, 16, 32] + pal[:255*3])
        out_img.info['transparency'] = 0
        out_img.info['duration'] = 80
        out_img.info['disposal'] = 2
        frames.append(out_img)
        
    frames[0].save(
        'assets/animations/shadow-particles.gif',
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        transparency=0,
        disposal=2
    )
    print("Shadow Particles GIF saved successfully!")

if __name__ == '__main__':
    make_particles_gif()
