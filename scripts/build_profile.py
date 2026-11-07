"""Rebuild the illustrated README dashboard with locally embedded artwork."""
from pathlib import Path
from html import escape
from design_system import ROOT, text as t, image, pair, write

CITY='assets/background/violet-citadel.webp'
CHAR='assets/characters/developer-monarch.webp'
body=image(CITY,0,0,1200,400)+ '<rect width="1200" height="400" fill="url(#fade)"/>'
body+=t(42,45,'SHADOW MONARCH / DEVELOPER',17,'#22D3EE',700)
body+=t(42,128,'ABHISHEK S NAIR',56,'#F8FAFC',700)
body+=t(44,177,'Full Stack Developer',27,'#C4B5FD',700)
body+=t(44,223,'Building web and mobile applications',23,'#F8FAFC')+t(44,254,'with modern technologies, while exploring',23,'#F8FAFC')+t(44,285,'AI-assisted software development.',23,'#F8FAFC')
body+=t(44,351,'REACT / REACT NATIVE / FLUTTER PROJECTS',17,'#22D3EE',700)
pair('assets/hero/shadow-monarch',body,1200,400,'Abhishek S Nair — Full Stack Developer')
body=image(CITY,-580,0,1080,360,.65)+'<rect width="500" height="360" fill="#03040D" opacity=".52"/>'
body+=t(24,38,'SHADOW MONARCH',16,'#22D3EE',700)+t(24,104,'ABHISHEK',44,'#F8FAFC',700)+t(24,155,'S NAIR',44,'#F8FAFC',700)+t(24,205,'Full Stack Developer',26,'#C4B5FD',700)
for y,line in [(250,'Building web and mobile applications,'),(278,'while exploring AI-assisted software'),(306,'development.')]:body+=t(24,y,line,20,'#F8FAFC')
pair('assets/hero/shadow-monarch-mobile',body,500,360,'Abhishek S Nair — mobile hero')

body=image(CHAR,288,44,210,315,.8)+t(25,37,'01 / ABOUT ME',16,'#22D3EE',700)+t(25,83,'Code across platforms.',27,'#F8FAFC',700)
for y,line in [(132,'My public projects span'),(161,'web, mobile and desktop.'),(210,'React / React Native / Flutter'),(242,'Full-stack applications'),(274,'AI-assisted tools')]:body+=t(25,y,line,19)
pair('assets/cards/about',body,500,330,'About — web, mobile and desktop projects')
body=image(CHAR,330,76,150,225,.6)+t(25,37,'02 / PROJECT FOCUS',16,'#22D3EE',700)+t(25,83,'Inside the code.',27,'#F8FAFC',700)
for y,name,detail in [(130,'FlowSync','Tasks and team messaging'),(198,'LiveSync','Location-sharing prototype'),(266,'Echo Desktop AI','Desktop and browser assistant')]:body+=t(25,y,name,21,'#F8FAFC',700)+t(25,y+27,detail,18)
pair('assets/cards/project-focus',body,500,330,'Project focus — repository contents, not current employment')

# Galaxy: figure, orbit paths and recognisable geometric technology symbols.
body=t(25,37,'03 / TECH STACK GALAXY',16,'#22D3EE',700)
body+='<ellipse cx="250" cy="225" rx="206" ry="115" fill="none" stroke="#7C3AED"/><ellipse cx="250" cy="225" rx="156" ry="81" fill="none" stroke="#22D3EE" opacity=".45"/>'
body+=image(CHAR,155,100,190,285)
icons=[(75,110,'React','atom'),(365,110,'React Native','atom'),(80,210,'Flutter','F'),(390,210,'TypeScript','TS'),(90,325,'JavaScript','JS'),(370,325,'Python','Py')]
for x,y,label,icon in icons:
    body+=f'<circle cx="{x}" cy="{y}" r="23" fill="#080D21" stroke="#A855F7"/>'
    if icon=='atom':
        for angle in [0,60,120]:body+=f'<ellipse cx="{x}" cy="{y}" rx="17" ry="6" transform="rotate({angle} {x} {y})" fill="none" stroke="#22D3EE"/>'
        body+=f'<circle cx="{x}" cy="{y}" r="3" fill="#22D3EE"/>'
    elif icon=='F':body+=f'<path d="M{x-14} {y+2} L{x+6} {y-18} H{x+20} L{x} {y+2} Z M{x-3} {y+8} L{x+7} {y-2} H{x+20} L{x+10} {y+8} L{x+20} {y+18} H{x+7} Z" fill="#22D3EE"/>'
    else:body+=t(x-12,y+6,icon,17,'#22D3EE',700)
    body+=t(x-len(label)*4.7,y+43,label,17,'#F8FAFC',700)
body+=t(35,408,'Node.js / Express / MongoDB',21,'#F8FAFC',700)+t(35,443,'FastAPI / Git',21,'#F8FAFC',700)+t(35,483,'Technologies used in public repositories',17)
pair('assets/cards/tech-galaxy',body,500,510,'Project technologies — React, React Native, Flutter, JavaScript, TypeScript, Python, Node.js, Express, MongoDB, FastAPI, Git')
body=t(25,37,'04 / HUNTER ID',16,'#22D3EE',700)+t(25,63,'DEVELOPER EDITION / THEME ONLY',12)
body+=image(CHAR,-20,88,235,353)
body+=t(202,123,'ABHISHEK',29,'#F8FAFC',700)+t(202,157,'S NAIR',29,'#F8FAFC',700)+t(202,197,'Full Stack Developer',19,'#22D3EE',700)
for y,label,value in [(241,'GITHUB','abhisheksureshnair'),(305,'CONTACT','nairsabhishek@gmail.com'),(369,'PORTFOLIO','abhisheksnair.vercel.app')]:body+=t(202,y,label,13,'#A855F7',700)+t(202,y+25,value,17)
body+=t(25,477,'Web / Mobile / AI-assisted projects',19,'#F8FAFC')
pair('assets/cards/hunter-id',body,500,510,'Abhishek S Nair — developer identity; decorative anime theme, not a credential')

PROJECTS=[
('flowsync','FlowSync',['Task boards and','team messaging.'],'React / Node.js','Express / MongoDB','boards'),
('LiveSync','LiveSync',['Location-sharing','prototype with','simulated backend data.'],'React Native / React','Node.js / Express','map'),
('AlphaPulse-Stock-AI','AlphaPulse Stock AI',['Stock analysis and','portfolio tooling.'],'Flutter / React Native','Python / FastAPI','chart'),
('echo-desktop-ai','Echo Desktop AI',['Desktop assistant','and browser co-pilot.'],'Electron / React','JavaScript','chat'),
('ecommerce-app-flutter','Luxentia',['Fashion shopping','application.'],'Flutter / Dart','Node.js','shop'),
('vehicle-tracking-app-flutter','Vehicle Tracking',['Vehicle maps and','route-history interface.'],'Flutter / Dart','Node.js / Express','map'),
('abhishek-portfolio','Abhishek Portfolio',['Professional and','cinematic portfolio.'],'Next.js / React','TypeScript','portfolio')]

def concept(kind):
    # Abstract original vector illustrations, deliberately not product screenshots.
    s='<rect x="18" y="18" width="284" height="128" rx="12" fill="#080D21" stroke="#49316D"/>'
    if kind in ['map','chart']:
        for x in range(40,290,40):s+=f'<path d="M{x} 30 V134" stroke="#1E1C3C"/>'
        for y in range(40,140,25):s+=f'<path d="M30 {y} H290" stroke="#1E1C3C"/>'
        s+='<path d="M38 112 L80 92 L116 101 L157 57 L205 74 L278 38" stroke="#22D3EE" stroke-width="4" fill="none"/>'
        if kind=='map':s+='<path d="M157 30 C133 30 131 58 157 80 C183 58 181 30 157 30" fill="#7C3AED"/><circle cx="157" cy="46" r="6" fill="#C4B5FD"/>'
    elif kind=='boards':
        for i in range(3):
            x=35+i*85;s+=f'<rect x="{x}" y="37" width="72" height="90" rx="7" fill="#17112E"/><path d="M{x+10} 51 H{x+57}" stroke="#22D3EE" stroke-width="3"/>'
            for j in range(2+i%2):s+=f'<rect x="{x+9}" y="{63+j*19}" width="54" height="12" rx="3" fill="#7C3AED" opacity="{.4+j*.2}"/>'
    elif kind=='chat':s+='<rect x="42" y="40" width="180" height="36" rx="12" fill="#30204D"/><rect x="98" y="87" width="178" height="36" rx="12" fill="#4B2383"/><path d="M61 57 H191 M116 105 H247" stroke="#C4B5FD" stroke-width="3"/>'
    elif kind=='shop':s+='<path d="M105 63 H215 L225 129 H95 Z" fill="#241139" stroke="#A855F7" stroke-width="3"/><path d="M134 66 V52 a26 26 0 0 1 52 0 V66" fill="none" stroke="#22D3EE" stroke-width="4"/>'
    else:s+='<circle cx="90" cy="77" r="26" fill="#7C3AED"/><path d="M139 60 H265 M139 82 H240 M55 120 H265" stroke="#C4B5FD" stroke-width="4"/>'
    return s+t(30,140,'PROJECT CONCEPT / ILLUSTRATION',9,'#C4B5FD')
for slug,name,lines,stack1,stack2,kind in PROJECTS:
    b=concept(kind)+t(22,184,name,24,'#F8FAFC',700)
    for i,line in enumerate(lines):b+=t(22,220+i*25,line,20)
    b+=t(22,312,stack1,17,'#22D3EE')+t(22,338,stack2,17,'#22D3EE')+t(22,380,'VIEW REPOSITORY →',16,'#F8FAFC',700)
    write('assets/projects/'+slug+'.svg',b,320,405,name+' — original project concept, not a screenshot')

body=image(CITY,0,0,1200,400)+t(35,45,'CONTRIBUTION CITY',22,'#F8FAFC',700)+t(35,83,'A world built one commit at a time.',22)+t(35,353,'DECORATIVE ARTWORK / EXPLORE REAL ACTIVITY ON GITHUB →',16,'#F8FAFC',700)
pair('assets/background/contribution-city',body,1200,400,'Decorative Shadow Monarch city — not a contribution heatmap')
body=image(CITY,0,-220,1200,400,.55)+'<rect width="1200" height="160" fill="#03040D" opacity=".3"/>'+t(42,79,'ARISE. BUILD. LEVEL UP.',46,'#F8FAFC',700)+t(44,125,'ABHISHEK S NAIR / SHADOW MONARCH',19,'#C4B5FD',700)
pair('assets/footer/shadow-energy',body,1200,160,'Arise. Build. Level up.')
for label in ['GitHub','LinkedIn','Portfolio','Email','Projects','Activity','Static']:
    write('assets/cards/link-'+label.lower()+'.svg',t(17,35,label,21,'#F8FAFC',700)+t(158,35,'↗',21,'#22D3EE'),195,58,label)
for slug,title in [('projects','FEATURED PROJECTS'),('activity','GITHUB TELEMETRY'),('connect',"LET’S CONNECT")]:
    write('assets/cards/heading-'+slug+'.svg',t(24,39,title,25,'#F8FAFC',700),900,64,title)
    write('assets/cards/heading-'+slug+'-mobile.svg',t(20,38,title,25,'#F8FAFC',700),440,62,title)

def motion(path,alt,width,mobile=None):
    source=f'<source media="(max-width: 600px) and (prefers-reduced-motion: reduce)" srcset="{mobile}-static.svg" /><source media="(max-width: 600px)" srcset="{mobile}.svg" />' if mobile else ''
    return f'<picture>{source}<source media="(prefers-reduced-motion: reduce)" srcset="{path}-static.svg" /><img src="{path}.svg" alt="{escape(alt,quote=True)}" width="{width}" /></picture>'

def link(label,url,width=170):return f'<a href="{url}"><img src="assets/cards/link-{label.lower()}.svg" alt="{label}" width="{width}" /></a>'

s='<div align="center">\n\n'+motion('assets/hero/shadow-monarch','Abhishek S Nair — Full Stack Developer. Building web and mobile applications while exploring AI-assisted software development.',1200,'assets/hero/shadow-monarch-mobile')+'\n\n<p>\n'
s+='\n'.join(link(a,b,140) for a,b in [('Projects','#featured-projects'),('Activity','#github-activity'),('Portfolio','https://abhisheksnair.vercel.app/'),('Static','README-static.md')])+'\n</p>\n\n<p>\n'
for slug,label in [('chibi-idle','Sung Jinwoo — idle aura'),('chibi-dancing','Sung Jinwoo — victory dance'),('shadow-soldier','Shadow soldier — violet summon')]:s+=f'<picture><source media="(prefers-reduced-motion: reduce)" srcset="assets/monarch/{slug}.png" /><img src="assets/monarch/{slug}.gif" alt="{label}" width="170" /></picture>\n'
s+='</p>\n\n<p>\n'+motion('assets/cards/about','About: My public projects span web, mobile and desktop, using React, React Native and Flutter.',360)+'\n'+motion('assets/cards/project-focus','Project focus: FlowSync tasks/chat, LiveSync location-sharing prototype, Echo desktop/browser assistant.',360)+'\n</p>\n\n<p>\n'
s+=motion('assets/cards/tech-galaxy','Technologies in public projects: React, React Native, Flutter, JavaScript, TypeScript, Python, Node.js, Express, MongoDB, FastAPI and Git.',360)+'\n'
s+='<a href="https://abhisheksnair.vercel.app/">'+motion('assets/cards/hunter-id','Developer identity: Abhishek S Nair; Full Stack Developer; GitHub abhisheksureshnair; nairsabhishek@gmail.com; abhisheksnair.vercel.app. Hunter ID is an anime theme only.',360)+'</a>\n</p>\n\n<p>\n'
for slug,alt in [('repositories','Public owned repositories, including forks'),('stars','Stars on owned non-fork public repositories'),('projects','Owned non-fork public repositories')]:s+=f'<a href="docs/activity.md"><img src="assets/stats/{slug}.svg" alt="{alt}. See dated snapshot for figures and methodology." width="230" /></a>\n'
s+='</p>\n\n<a name="featured-projects"></a>\n<picture><source media="(max-width: 600px)" srcset="assets/cards/heading-projects-mobile.svg" /><img src="assets/cards/heading-projects.svg" alt="Featured projects" width="900" /></picture>\n\n<p>\n'
for slug,name,lines,a,b,kind in PROJECTS:s+=f'<a href="https://github.com/abhisheksureshnair/{slug}"><img src="assets/projects/{slug}.svg" alt="{name}: {" ".join(lines)} {a}; {b}. Original illustration, not a screenshot. Open repository." width="230" /></a>\n'
s+='</p>\n\n<details>\n<summary>Project descriptions and technology sources</summary>\n\n'
for slug,name,lines,a,b,kind in PROJECTS:s+=f'- **[{name}](https://github.com/abhisheksureshnair/{slug})** — {" ".join(lines)} {a}; {b}.\n'
s+='\nThese are public project examples, not employment or commercial deployment claims. Project Focus describes repository contents rather than an assertion of current work.\n\n</details>\n\n<a name="github-activity"></a>\n<picture><source media="(max-width: 600px)" srcset="assets/cards/heading-activity-mobile.svg" /><img src="assets/cards/heading-activity.svg" alt="GitHub activity" width="900" /></picture>\n\n'
s+='<a href="docs/activity.md"><picture><source media="(max-width: 600px)" srcset="assets/stats/activity-mobile.svg" /><img src="assets/stats/activity.svg" alt="Dated public GitHub snapshot: repository statistics, primary-language counts and latest returned public event. Open the text snapshot for exact values and methodology." width="900" /></picture></a>\n\n'
s+='<a href="https://github.com/abhisheksureshnair?tab=overview">'+motion('assets/background/contribution-city','Decorative violet-moon cityscape. Open the real GitHub contribution history; this artwork does not encode contribution data.',1200)+'</a>\n\n<details>\n<summary>Statistics scope and update policy</summary>\n\n[Read the dated API snapshot](docs/activity.md). Languages count non-fork repositories by primary language, not lines of code or proficiency. A daily workflow checks public data and publishes only when values change. The timestamp identifies the last changed snapshot; failures retain it. Contribution totals and streaks are omitted.\n\n</details>\n\n<picture><source media="(max-width: 600px)" srcset="assets/cards/heading-connect-mobile.svg" /><img src="assets/cards/heading-connect.svg" alt="Let’s connect" width="900" /></picture>\n\n<p>\n'
s+='\n'.join(link(a,b) for a,b in [('GitHub','https://github.com/abhisheksureshnair'),('LinkedIn','https://www.linkedin.com/in/abhisheksnair/'),('Portfolio','https://abhisheksnair.vercel.app/'),('Email','mailto:nairsabhishek@gmail.com')])+'\n</p>\n\n'
s+=motion('assets/footer/shadow-energy','Arise. Build. Level up. Abhishek S Nair — Shadow Monarch.',1200)+'\n\n<details>\n<summary>Profile sources, accessibility and maintenance</summary>\n\n[Source audit](docs/PROFILE.md) · [Static version](README-static.md) · [Validation](docs/QA.md) · [Artwork provenance](docs/ARTWORK.md)\n\nEmail: [nairsabhishek@gmail.com](mailto:nairsabhishek@gmail.com). Title and contacts come from the existing public account and portfolio. No resume-dependent experience, education, location or availability claims are included.\n\n</details>\n\n</div>\n'
(ROOT/'README.md').write_text(s)
# Static version retains mobile art direction but replaces every animated source.
import re
static=s
for prefix in ['assets/hero/shadow-monarch','assets/cards/about','assets/cards/project-focus','assets/cards/tech-galaxy','assets/cards/hunter-id','assets/background/contribution-city','assets/footer/shadow-energy']:
    static=static.replace(prefix+'.svg',prefix+'-static.svg').replace(prefix+'-mobile.svg',prefix+'-mobile-static.svg')
for slug in ['chibi-idle','chibi-dancing','shadow-soldier']:static=static.replace(f'assets/monarch/{slug}.gif',f'assets/monarch/{slug}.png')
static=static.replace('href="README-static.md"','href="README.md"').replace('alt="Static"','alt="Animated version"')
(ROOT/'README-static.md').write_text(static)
