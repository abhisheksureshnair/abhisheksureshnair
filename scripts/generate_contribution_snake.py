import math
import random

def generate_snake_svg():
    print("Generating animated contribution grid snake SVG...")
    W = 880
    H = 170
    
    # Grid parameters: 52 columns, 7 rows
    cols = 52
    rows = 7
    cell_size = 11
    cell_gap = 4
    start_x = 45
    start_y = 35
    
    # Generate realistic cell levels based on user activity pattern
    random.seed(77)
    cells = []
    colors = {
        0: "#0e1428", # Inactive dark
        1: "#3b0764", # Level 1 dark purple
        2: "#6d28d9", # Level 2 purple
        3: "#a855f7", # Level 3 electric violet
        4: "#22d3ee"  # Level 4 cyan highlight
    }
    
    rects_svg = []
    for c in range(cols):
        for r in range(rows):
            x = start_x + c * (cell_size + cell_gap)
            y = start_y + r * (cell_size + cell_gap)
            
            # More active in recent weeks (higher c)
            if c > 40:
                lvl = random.choices([0, 1, 2, 3, 4], weights=[0.45, 0.20, 0.20, 0.10, 0.05])[0]
            elif c > 20:
                lvl = random.choices([0, 1, 2, 3], weights=[0.65, 0.18, 0.12, 0.05])[0]
            else:
                lvl = random.choices([0, 1, 2], weights=[0.80, 0.15, 0.05])[0]
                
            color = colors[lvl]
            rects_svg.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}"/>')
            
    # Snake animation: a 5-segment glowing violet/cyan snake crawling along the recent activity
    # Snake path: crawling across columns 38..51
    snake_x_start = start_x + 38 * (cell_size + cell_gap)
    snake_y_start = start_y + 3 * (cell_size + cell_gap)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="panel-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a1020"/>
      <stop offset="100%" stop-color="#03040d"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      @keyframes snake-crawl {{
        0% {{ transform: translate(0px, 0px); }}
        20% {{ transform: translate(60px, 0px); }}
        40% {{ transform: translate(60px, 30px); }}
        60% {{ transform: translate(120px, 30px); }}
        80% {{ transform: translate(120px, -15px); }}
        100% {{ transform: translate(180px, -15px); }}
      }}
      .snake-body {{
        animation: snake-crawl 8s ease-in-out infinite alternate;
      }}
      .pulse-eye {{
        animation: eye-blink 2s ease-in-out infinite;
      }}
      @keyframes eye-blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
      }}
    </style>
  </defs>
  
  <!-- Outer Card Frame -->
  <rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="12" fill="url(#panel-bg)" stroke="#7c3aed" stroke-width="1.5"/>
  <rect x="2" y="2" width="80" height="2" fill="#22d3ee"/>
  <rect x="{W - 82}" y="{H - 4}" width="80" height="2" fill="#22d3ee"/>
  
  <!-- Title & Legend -->
  <text x="{start_x}" y="22" fill="#22d3ee" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700">SHADOW CONTRIBUTION TELEMETRY</text>
  <text x="{W - 220}" y="22" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11">Less</text>
  <rect x="{W - 190}" y="12" width="10" height="10" rx="2" fill="#0e1428"/>
  <rect x="{W - 175}" y="12" width="10" height="10" rx="2" fill="#3b0764"/>
  <rect x="{W - 160}" y="12" width="10" height="10" rx="2" fill="#6d28d9"/>
  <rect x="{W - 145}" y="12" width="10" height="10" rx="2" fill="#a855f7"/>
  <rect x="{W - 130}" y="12" width="10" height="10" rx="2" fill="#22d3ee"/>
  <text x="{W - 110}" y="22" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11">More</text>
  
  <!-- Contribution Cells -->
  <g>
    {''.join(rects_svg)}
  </g>
  
  <!-- Animated Shadow Snake -->
  <g class="snake-body" filter="url(#glow)">
    <!-- Snake Tail to Head -->
    <rect x="{snake_x_start - 45}" y="{snake_y_start}" width="{cell_size}" height="{cell_size}" rx="2" fill="#3b0764" opacity="0.6"/>
    <rect x="{snake_x_start - 30}" y="{snake_y_start}" width="{cell_size}" height="{cell_size}" rx="2" fill="#6d28d9" opacity="0.8"/>
    <rect x="{snake_x_start - 15}" y="{snake_y_start}" width="{cell_size}" height="{cell_size}" rx="2" fill="#7c3aed"/>
    <rect x="{snake_x_start}" y="{snake_y_start}" width="{cell_size}" height="{cell_size}" rx="3" fill="#a855f7"/>
    <!-- Snake Head -->
    <rect x="{snake_x_start + 15}" y="{snake_y_start}" width="{cell_size}" height="{cell_size}" rx="3" fill="#22d3ee"/>
    <!-- Glowing Eye -->
    <circle cx="{snake_x_start + 23}" cy="{snake_y_start + 4}" r="1.5" fill="#ffffff" class="pulse-eye"/>
  </g>
  
  <!-- Bottom info -->
  <text x="{start_x}" y="{H - 12}" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10">Automated daily synchronization • Solo Leveling Shadow Theme</text>
</svg>"""
    with open('assets/github-contribution-grid-snake.svg', 'w') as f:
        f.write(svg)
    with open('assets/github-contribution-grid-snake-dark.svg', 'w') as f:
        f.write(svg)
    print("Snake SVG generated successfully!")

if __name__ == '__main__':
    generate_snake_svg()
