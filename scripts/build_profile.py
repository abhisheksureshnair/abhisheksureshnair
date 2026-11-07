"""Rebuild code-native graphics. Existing character illustrations remain intact."""
import base64
from pathlib import Path
from visuals import panel, text

ROOT = Path(__file__).resolve().parents[1]

def art(file, x, y, w, h):
    data = base64.b64encode((ROOT / 'assets' / file).read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:image/png;base64,{data}" preserveAspectRatio="xMidYMid slice"/>'

panel('hero', art('hero-character.png', 545, 0, 375, 340) +
      '<rect width="570" height="340" fill="url(#bg)"/>' +
      text(36, 48, 'SHADOW MONARCH  /  DEVELOPER PROFILE', 16, '#22D3EE', 700) +
      text(36, 121, 'ABHISHEK', 58, '#F8FAFC', 700) +
      text(36, 185, 'S NAIR', 58, '#F8FAFC', 700) +
      text(38, 239, 'Full Stack Developer', 26) +
      text(38, 284, 'WEB  /  MOBILE  /  AI PROJECTS', 17), 920, 340,
      'Abhishek S Nair — Full Stack Developer')
panel('hero-mobile', art('hero-character.png', 180, 0, 260, 290) +
      '<rect width="440" height="290" fill="#050510" opacity=".65"/>' +
      text(24, 38, 'SHADOW MONARCH', 15, '#22D3EE', 700) +
      text(24, 110, 'ABHISHEK', 46, '#F8FAFC', 700) +
      text(24, 165, 'S NAIR', 46, '#F8FAFC', 700) +
      text(24, 219, 'Full Stack Developer', 24) +
      text(24, 260, 'WEB / MOBILE / AI PROJECTS', 15),440,290)

panel('about', text(26, 39, '01 / THE DEVELOPER', 14, '#22D3EE', 700) +
      text(26, 82, 'Ideas into applications.', 27, '#F8FAFC', 700) +
      text(26, 123, 'My public projects span web, mobile') +
      text(26, 151, 'and AI-assisted applications.') +
      text(26, 201, 'Explore the code. Follow the progress.', 16))
panel('current', text(26, 39, '02 / PROJECT FOCUS', 14, '#22D3EE', 700) +
      text(26, 82, 'Inside the repositories.', 27, '#F8FAFC', 700) +
      text(26, 123, 'FlowSync — tasks and team chat') +
      text(26, 153, 'LiveSync — location-sharing prototype') +
      text(26, 183, 'Echo — desktop and browser assistant') +
      text(26, 213, 'Public projects, not employment claims.', 14))

body = text(32, 43, '03 / TECHNOLOGY CONSTELLATION', 18, '#22D3EE', 700)
body += '<ellipse cx="460" cy="205" rx="330" ry="112" fill="none" stroke="#7C3AED"/><ellipse cx="460" cy="205" rx="240" ry="75" fill="none" stroke="#22D3EE" stroke-opacity=".4"/>'
body += '<circle cx="460" cy="205" r="67" fill="#110D26" stroke="#A855F7"/>' + text(421, 201, 'BUILD', 23, '#F8FAFC', 700) + text(427, 228, 'LEVEL UP', 12)
for x,y,label in [(80,115,'React'),(370,100,'React Native'),(735,115,'Flutter'),(60,205,'JavaScript'),(700,205,'TypeScript'),(100,295,'Node.js / Express'),(370,320,'Python / FastAPI'),(720,295,'MongoDB')]:
    body += text(x,y,label,22,'#F8FAFC',700)
body += text(32,375,'Technologies used in public projects • see source links below',18)
panel('skills',body,920,410)
body=text(24,38,'03 / TECHNOLOGY',17,'#22D3EE',700)
for i,line in enumerate(['React / React Native / Flutter','JavaScript / TypeScript','Node.js / Express / MongoDB','Python / FastAPI']):
    body+=f'<circle cx="29" cy="{85+i*57}" r="4" fill="#A855F7"/>'+text(45,92+i*57,line,20,'#F8FAFC')
body+=text(24,320,'Technologies in my public projects',17)
panel('skills-mobile',body,440,350)

PROJECTS = [
 ('flowsync','FlowSync','REALTIME WORKSPACE',['Task boards and team messaging.','React frontend and a Node.js API.'],'React · Express · MongoDB'),
 ('LiveSync','LiveSync','MOBILE / WEB PROTOTYPE',['Location sharing and family dashboards.','Includes simulated backend data.'],'React Native · React · Express'),
 ('AlphaPulse-Stock-AI','AlphaPulse Stock AI','MARKET ANALYSIS PROJECT',['Stock analysis and portfolio tooling.','Flutter and React Native clients.'],'Python · FastAPI · Flutter'),
 ('echo-desktop-ai','Echo Desktop AI','DESKTOP / BROWSER',['Desktop assistant and page co-pilot.','Browser sidebar for contextual chat.'],'Electron · React · JavaScript'),
 ('abhishek-portfolio','Abhishek Portfolio','PERSONAL PORTFOLIO',['Professional and cinematic experiences.','A portfolio built with Next.js.'],'Next.js · React · TypeScript'),
 ('ecommerce-app-flutter','Luxentia E-commerce','SHOPPING APPLICATION',['Fashion shopping application.','Flutter frontend and backend project.'],'Flutter · Dart · Node.js'),
 ('vehicle-tracking-app-flutter','Vehicle Tracking','NEON KINETIC',['Vehicle maps and route history UI.','Flutter client with an Express backend.'],'Flutter · Dart · Express'),
]
for i,(slug,name,kind,lines,stack) in enumerate(PROJECTS,1):
    body=text(26,34,f'{i:02d} / {kind}',12,'#22D3EE',700)+text(26,78,name,27,'#F8FAFC',700)
    body+=''.join(text(26,118+j*27,line,17) for j,line in enumerate(lines))
    body+='<path d="M26 169 H414" stroke="#49316D"/>'+text(26,198,stack,15)+text(26,230,'EXPLORE REPOSITORY →',13,'#A855F7',700)
    panel('project-'+slug,body,height=252)

for label in ['GitHub','LinkedIn','Portfolio','Email']:
    panel('contact-'+label.lower(),text(22,37,label,20,'#F8FAFC',700)+text(164,37,'↗',22,'#22D3EE'),210,62)

panel('footer',text(35,56,'ARISE. BUILD. LEVEL UP.',32,'#F8FAFC',700)+text(35,91,'Abhishek S Nair  /  Shadow Monarch',18),920,125)

intro='''<div align="center">

<picture><source media="(max-width: 600px)" srcset="assets/monarch/hero-mobile.svg" /><img src="assets/monarch/hero.svg" alt="Abhishek S Nair — Full Stack Developer. Original Shadow Monarch character artwork." width="920" /></picture>

**Full Stack Developer · Web, mobile and AI projects**

[Projects](#featured-projects) · [Technology](#technology) · [Activity](#github-activity) · [Connect](#connect) · [Static version](README-static.md)

<picture><source media="(prefers-reduced-motion: reduce)" srcset="assets/monarch/energy-static.png" /><img src="assets/animations/shadow-particles.gif" alt="" width="460" height="36" /></picture>

### The shadow companions

<p>
'''
for slug,label in [('chibi-idle','Sung Jinwoo — idle aura'),('chibi-dancing','Sung Jinwoo — victory dance'),('shadow-soldier','Shadow soldier — violet summon')]:
    intro+=f'<picture><source media="(prefers-reduced-motion: reduce)" srcset="assets/monarch/{slug}.png" /><img src="assets/monarch/{slug}.gif" alt="{label}" width="220" /></picture>\n'
intro+='''
</p>
<p>Sung Jinwoo · Victory groove · Shadow soldier</p>

### About & project focus

<img src="assets/monarch/about.svg" alt="About: My public projects span web, mobile and AI-assisted applications." width="440" />
<img src="assets/monarch/current.svg" alt="Project focus: FlowSync task boards and chat, LiveSync location-sharing prototype, Echo desktop and browser assistant. Public projects, not employment claims." width="440" />

My public repositories explore team collaboration, location interfaces and AI-assisted tools. Browse [FlowSync](https://github.com/abhisheksureshnair/flowsync), [LiveSync](https://github.com/abhisheksureshnair/LiveSync) and [Echo](https://github.com/abhisheksureshnair/echo-desktop-ai) for their current implementation and setup.

### Technology

<picture><source media="(max-width: 600px)" srcset="assets/monarch/skills-mobile.svg" /><img src="assets/monarch/skills.svg" alt="Technology constellation: React, React Native, Flutter, JavaScript, TypeScript, Node.js, Express, Python, FastAPI and MongoDB. Project usage, not a professional experience rating." width="920" /></picture>

[React, Node.js, Express & MongoDB — FlowSync](https://github.com/abhisheksureshnair/flowsync) · [React Native — LiveSync](https://github.com/abhisheksureshnair/LiveSync) · [Python, FastAPI & Flutter — AlphaPulse](https://github.com/abhisheksureshnair/AlphaPulse-Stock-AI) · [TypeScript — Portfolio](https://github.com/abhisheksureshnair/abhishek-portfolio)

### Featured projects

Public code, with descriptions based on each repository. These are project examples, not claims of commercial deployment.

<p>
'''
for slug,name,kind,lines,stack in PROJECTS:
    intro+=f'<a href="https://github.com/abhisheksureshnair/{slug}"><img src="assets/monarch/project-{slug}.svg" alt="{name}: {" ".join(lines)} {stack}. Open repository." width="440" /></a>\n'
intro+='''
</p>

### GitHub activity

<a href="https://github.com/abhisheksureshnair?tab=repositories"><picture><source media="(max-width: 600px)" srcset="assets/monarch/activity-mobile.svg" /><img src="assets/monarch/activity.svg" alt="Dated public GitHub repository snapshot. Full figures, scope and source timestamps are available in the text snapshot below." width="920" /></picture></a>

[Read the snapshot and methodology](docs/activity.md) · [Contribution history on GitHub](https://github.com/abhisheksureshnair?tab=overview)

The dashboard is a dated API snapshot, refreshed by a daily workflow when available. Language counts describe repositories' primary languages, not proficiency or lines of code. Contribution totals and streaks are omitted.

### Connect

<p>
'''
for label,url in [('GitHub','https://github.com/abhisheksureshnair'),('LinkedIn','https://www.linkedin.com/in/abhisheksnair/'),('Portfolio','https://abhisheksnair.vercel.app/'),('Email','mailto:nairsabhishek@gmail.com')]:
    intro+=f'<a href="{url}"><img src="assets/monarch/contact-{label.lower()}.svg" alt="{label}" width="210" /></a>\n'
intro+='''
</p>
<p><a href="mailto:nairsabhishek@gmail.com">nairsabhishek@gmail.com</a></p>

<picture><source media="(prefers-reduced-motion: reduce)" srcset="assets/monarch/energy-static.png" /><img src="assets/animations/shadow-particles.gif" alt="" width="460" height="36" /></picture>

<img src="assets/monarch/footer.svg" alt="Arise. Build. Level up. Abhishek S Nair — Shadow Monarch." width="920" />

[Profile sources & maintenance](docs/PROFILE.md)

</div>
'''
(ROOT/'README.md').write_text(intro)
import re
static=re.sub(r'<picture><source media="\(prefers-reduced-motion: reduce\)"[^>]+srcset="([^"]+)"[^>]*\s*/><img([^>]+)src="[^"]+"([^>]*)/></picture>',lambda m:f'<img{m[2]}src="{m[1]}"{m[3]}/>',intro)
static=static.replace('[Static version](README-static.md)','[Animated version](README.md)')
(ROOT/'README-static.md').write_text(static)
