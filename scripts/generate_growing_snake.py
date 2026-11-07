import math
import random

def generate_growing_snake_svg():
    print("Generating Snake Game Growing SVG (Eating dots & increasing size)...")
    W = 880
    H = 185
    
    cols = 52
    rows = 7
    cell_size = 11
    cell_gap = 4
    start_x = 45
    start_y = 42
    
    # Deterministic seed for realistic activity pattern
    random.seed(88)
    
    colors = {
        0: "#0e1428", # Inactive dark
        1: "#3b0764", # Level 1
        2: "#6d28d9", # Level 2
        3: "#a855f7", # Level 3
        4: "#22d3ee"  # Level 4 cyan
    }
    
    # Food dots that the snake will eat:
    # Let's place food dots at specific column/row coordinates
    # Path of the snake:
    # Starts at col 36, row 3
    # Moves right: eats food at (col 39, row 3) -> grows
    # Moves down: eats food at (col 39, row 5) -> grows
    # Moves right: eats food at (col 44, row 5) -> grows
    # Moves up: eats food at (col 44, row 2) -> grows
    # Moves right: eats food at (col 48, row 2) -> grows
    food_coords = [
        (39, 3),
        (39, 5),
        (44, 5),
        (44, 2),
        (48, 2),
    ]
    food_set = set(food_coords)
    
    rects_svg = []
    food_svg = []
    
    for c in range(cols):
        for r in range(rows):
            x = start_x + c * (cell_size + cell_gap)
            y = start_y + r * (cell_size + cell_gap)
            
            if (c, r) in food_set:
                # This is an active food dot!
                # It will disappear when eaten
                idx = food_coords.index((c, r))
                eat_times = ["0.18", "0.36", "0.54", "0.72", "0.90"]
                eat_t = eat_times[idx]
                # Keyframe animation: visible until eaten, then flashes and vanishes, resets at end
                food_svg.append(f'''
    <rect id="food_{idx}" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="#22d3ee">
      <animate attributeName="fill" values="#22d3ee;#ffffff;#22d3ee;#0e1428;#0e1428" keyTimes="0;{float(eat_t)-0.02:.2f};{eat_t};{float(eat_t)+0.04:.2f};1" dur="10s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;1;1;0.2;0.2" keyTimes="0;{float(eat_t)-0.02:.2f};{eat_t};{float(eat_t)+0.04:.2f};1" dur="10s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="scale" values="1;1.4;0.2;0.2" keyTimes="0;{eat_t};{float(eat_t)+0.04:.2f};1" transform-origin="{x + cell_size/2} {y + cell_size/2}" dur="10s" repeatCount="indefinite"/>
    </rect>''')
            else:
                if c > 40:
                    lvl = random.choices([0, 1, 2, 3, 4], weights=[0.45, 0.20, 0.20, 0.10, 0.05])[0]
                elif c > 20:
                    lvl = random.choices([0, 1, 2, 3], weights=[0.65, 0.18, 0.12, 0.05])[0]
                else:
                    lvl = random.choices([0, 1, 2], weights=[0.80, 0.15, 0.05])[0]
                color = colors[lvl]
                rects_svg.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}"/>')

    # Base coordinates for the snake
    # Column 36, Row 3
    bx = start_x + 36 * (cell_size + cell_gap)
    by = start_y + 3 * (cell_size + cell_gap)
    
    # Path movement offsets in px:
    # Step 0 (0s, 0%): (0, 0)
    # Step 1 (1.8s, 18%): hits food 0 at (39, 3) -> dx = 3 * 15 = 45, dy = 0
    # Step 2 (3.6s, 36%): hits food 1 at (39, 5) -> dx = 45, dy = 2 * 15 = 30
    # Step 3 (5.4s, 54%): hits food 2 at (44, 5) -> dx = 8 * 15 = 120, dy = 30
    # Step 4 (7.2s, 72%): hits food 3 at (44, 2) -> dx = 120, dy = -1 * 15 = -15
    # Step 5 (9.0s, 90%): hits food 4 at (48, 2) -> dx = 12 * 15 = 180, dy = -15
    # Step 6 (10.0s, 100%): loops smoothly
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="panel-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a1020"/>
      <stop offset="100%" stop-color="#03040d"/>
    </linearGradient>
    <filter id="neon-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      /* Snake path keyframes */
      @keyframes crawl-head {{
        0%   {{ transform: translate(0px, 0px); }}
        18%  {{ transform: translate(45px, 0px); }}
        20%  {{ transform: translate(45px, 0px); }}
        36%  {{ transform: translate(45px, 30px); }}
        38%  {{ transform: translate(45px, 30px); }}
        54%  {{ transform: translate(120px, 30px); }}
        56%  {{ transform: translate(120px, 30px); }}
        72%  {{ transform: translate(120px, -15px); }}
        74%  {{ transform: translate(120px, -15px); }}
        90%  {{ transform: translate(180px, -15px); }}
        100% {{ transform: translate(0px, 0px); }}
      }}
      @keyframes chomp-head {{
        0%, 16%, 22%, 34%, 40%, 52%, 58%, 70%, 76%, 88%, 94%, 100% {{
          transform: scale(1);
        }}
        18%, 36%, 54%, 72%, 90% {{
          transform: scale(1.45);
        }}
      }}
      @keyframes crawl-body1 {{
        0%   {{ transform: translate(-15px, 0px); }}
        18%  {{ transform: translate(30px, 0px); }}
        36%  {{ transform: translate(45px, 15px); }}
        54%  {{ transform: translate(105px, 30px); }}
        72%  {{ transform: translate(120px, 0px); }}
        90%  {{ transform: translate(165px, -15px); }}
        100% {{ transform: translate(-15px, 0px); }}
      }}
      @keyframes crawl-body2 {{
        0%   {{ transform: translate(-30px, 0px); }}
        18%  {{ transform: translate(15px, 0px); }}
        36%  {{ transform: translate(45px, 0px); }}
        54%  {{ transform: translate(90px, 30px); }}
        72%  {{ transform: translate(120px, 15px); }}
        90%  {{ transform: translate(150px, -15px); }}
        100% {{ transform: translate(-30px, 0px); }}
      }}
      @keyframes crawl-body3 {{
        0%   {{ transform: translate(-45px, 0px); }}
        18%  {{ transform: translate(0px, 0px); }}
        36%  {{ transform: translate(30px, 0px); }}
        54%  {{ transform: translate(75px, 30px); }}
        72%  {{ transform: translate(120px, 30px); }}
        90%  {{ transform: translate(135px, -15px); }}
        100% {{ transform: translate(-45px, 0px); }}
      }}
      /* Segments 4, 5, 6, 7 grow as snake eats food */
      @keyframes grow-seg4 {{
        0%, 17%  {{ opacity: 0; transform: translate(-60px, 0px) scale(0); }}
        18%, 100% {{ opacity: 1; transform: translate(0px, 0px) scale(1); }}
      }}
      @keyframes grow-seg5 {{
        0%, 35%  {{ opacity: 0; transform: translate(-60px, 0px) scale(0); }}
        36%, 100% {{ opacity: 1; transform: translate(15px, 0px) scale(1); }}
      }}
      @keyframes grow-seg6 {{
        0%, 53%  {{ opacity: 0; transform: translate(-60px, 0px) scale(0); }}
        54%, 100% {{ opacity: 1; transform: translate(45px, 15px) scale(1); }}
      }}
      @keyframes grow-seg7 {{
        0%, 71%  {{ opacity: 0; transform: translate(-60px, 0px) scale(0); }}
        72%, 100% {{ opacity: 1; transform: translate(90px, 30px) scale(1); }}
      }}

      .snake-head-move {{
        animation: crawl-head 10s ease-in-out infinite;
      }}
      .snake-head-chomp {{
        animation: chomp-head 10s ease-in-out infinite;
        transform-origin: center;
      }}
      .snake-b1 {{ animation: crawl-body1 10s ease-in-out infinite; }}
      .snake-b2 {{ animation: crawl-body2 10s ease-in-out infinite; }}
      .snake-b3 {{ animation: crawl-body3 10s ease-in-out infinite; }}
      .snake-b4 {{ animation: grow-seg4 10s ease-in-out infinite; }}
      .snake-b5 {{ animation: grow-seg5 10s ease-in-out infinite; }}
      .snake-b6 {{ animation: grow-seg6 10s ease-in-out infinite; }}
      .snake-b7 {{ animation: grow-seg7 10s ease-in-out infinite; }}
      
      .score-counter {{
        font-family: monospace;
        font-weight: 700;
        fill: #22d3ee;
      }}
    </style>
  </defs>
  
  <!-- Outer Card Frame -->
  <rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="12" fill="url(#panel-bg)" stroke="#7c3aed" stroke-width="1.5"/>
  <rect x="2" y="2" width="90" height="2" fill="#22d3ee"/>
  <rect x="{W - 92}" y="{H - 4}" width="90" height="2" fill="#22d3ee"/>
  
  <!-- Title, Status & Game Score -->
  <text x="{start_x}" y="24" fill="#22d3ee" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700">🐍 SHADOW CONTRIBUTION MATRIX // SNAKE GAME LEVEL UP</text>
  <text x="{start_x + 480}" y="24" fill="#c084fc" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600">LENGTH: 4 → 8 SEGMENTS (EATING)</text>

  <!-- Legend -->
  <text x="{W - 195}" y="24" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11">Less</text>
  <rect x="{W - 165}" y="14" width="10" height="10" rx="2" fill="#0e1428"/>
  <rect x="{W - 150}" y="14" width="10" height="10" rx="2" fill="#3b0764"/>
  <rect x="{W - 135}" y="14" width="10" height="10" rx="2" fill="#6d28d9"/>
  <rect x="{W - 120}" y="14" width="10" height="10" rx="2" fill="#a855f7"/>
  <rect x="{W - 105}" y="14" width="10" height="10" rx="2" fill="#22d3ee"/>
  <text x="{W - 88}" y="24" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11">More</text>
  
  <!-- Contribution Cells -->
  <g>
    {''.join(rects_svg)}
  </g>
  
  <!-- Animated Food Dots -->
  <g filter="url(#neon-glow)">
    {''.join(food_svg)}
  </g>
  
  <!-- Growing Snake Entity -->
  <g filter="url(#neon-glow)">
    <!-- Base Body Segments -->
    <rect class="snake-b3" x="{bx}" y="{by}" width="{cell_size}" height="{cell_size}" rx="2" fill="#4c1d95" opacity="0.8"/>
    <rect class="snake-b2" x="{bx}" y="{by}" width="{cell_size}" height="{cell_size}" rx="2" fill="#6d28d9"/>
    <rect class="snake-b1" x="{bx}" y="{by}" width="{cell_size}" height="{cell_size}" rx="3" fill="#a855f7"/>

    <!-- Dynamic Growth Segments (Added as food is consumed) -->
    <rect class="snake-b4" x="{bx}" y="{by}" width="{cell_size}" height="{cell_size}" rx="2" fill="#3b0764"/>
    <rect class="snake-b5" x="{bx}" y="{by}" width="{cell_size}" height="{cell_size}" rx="2" fill="#311042"/>
    <rect class="snake-b6" x="{bx}" y="{by}" width="{cell_size}" height="{cell_size}" rx="2" fill="#240b33"/>
    <rect class="snake-b7" x="{bx}" y="{by}" width="{cell_size}" height="{cell_size}" rx="2" fill="#1c0729"/>

    <!-- Snake Head (Chomping & Moving) -->
    <g class="snake-head-move">
      <g class="snake-head-chomp">
        <rect x="{bx}" y="{by}" width="{cell_size + 2}" height="{cell_size + 2}" rx="3" fill="#22d3ee"/>
        <!-- Glowing eye on snake head -->
        <circle cx="{bx + 8}" cy="{by + 4}" r="1.8" fill="#ffffff"/>
        <circle cx="{bx + 8}" cy="{by + 4}" r="0.8" fill="#03040d"/>
      </g>
    </g>
  </g>
  
  <!-- Bottom info bar -->
  <text x="{start_x}" y="{H - 12}" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10">🎮 Live Arcade Telemetry • Snake eats contribution dots &amp; increases body length • Solo Leveling Engine</text>
</svg>"""

    with open('assets/github-contribution-grid-snake.svg', 'w') as f:
        f.write(svg)
    with open('assets/github-contribution-grid-snake-dark.svg', 'w') as f:
        f.write(svg)
    print("Growing Snake SVG generated successfully!")

if __name__ == '__main__':
    generate_growing_snake_svg()
