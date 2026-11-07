# Profile sources and maintenance

Audit date: **2026-11-07**. The cinematic redesign started from `1168134c65e63da6a4a2d0ed22b72c9dab4ca647`; the working tree was clean. The existing checkout was reused. GitHub confirmed `main` as the default branch. The existing daily snapshot workflow was retained and updated. Work is on `feat/shadow-monarch-profile-redesign`.

## Identity and factual boundaries

- The [public account](https://github.com/abhisheksureshnair) describes the owner as a Full Stack Developer. The [portfolio README](https://github.com/abhisheksureshnair/abhishek-portfolio) supplies the full name, email and LinkedIn URL.
- No resume, reference images or reference PDF accompanied either text brief. Exact visual reference matching could not be verified. Years of experience, employers, certifications, availability and current-work assertions are therefore omitted. Project focus describes repository contents, not an assertion of ongoing work or professional employment.
- The original artwork and original asset files are retained. Older, unused graphics contain unverified statistics and experience claims and **must not be treated as factual sources or reused without review**. Neither profile README references them. The GitHub account photo was not changed.

## Project and technology evidence

All seven featured repositories were public and owned by this account at audit time. Repository descriptions, READMEs and recursive trees were inspected. FlowSync backend, LiveSync mobile and portfolio dependency manifests were also inspected; versions in README badges sometimes differed from manifests, so the profile does not advertise versions.

| Project | Source | Conservative description |
| --- | --- | --- |
| FlowSync | [Repository and README](https://github.com/abhisheksureshnair/flowsync), [backend manifest](https://github.com/abhisheksureshnair/flowsync/blob/main/backend/package.json) | React task boards/chat; Node.js, Express, MongoDB |
| LiveSync | [Repository and README](https://github.com/abhisheksureshnair/LiveSync), [mobile manifest](https://github.com/abhisheksureshnair/LiveSync/blob/main/mobile/package.json) | React Native and web location prototype; README documents simulated backend data |
| AlphaPulse Stock AI | [Repository and README](https://github.com/abhisheksureshnair/AlphaPulse-Stock-AI) | Python/FastAPI backend; Flutter and React Native clients; stock analysis/portfolio tooling |
| Echo Desktop AI | [Repository and README](https://github.com/abhisheksureshnair/echo-desktop-ai) | Electron/React assistant with browser page sidebar |
| Abhishek Portfolio | [Repository and README](https://github.com/abhisheksureshnair/abhishek-portfolio), [manifest](https://github.com/abhisheksureshnair/abhishek-portfolio/blob/master/package.json) | Next.js/React/TypeScript portfolio |
| Luxentia E-commerce | [Repository and README](https://github.com/abhisheksureshnair/ecommerce-app-flutter) | Flutter fashion shopping application and Node.js backend |
| Vehicle Tracking | [Repository and README](https://github.com/abhisheksureshnair/vehicle-tracking-app-flutter) | Neon Kinetic Flutter vehicle maps and route history interface; Express backend |

Technology labels indicate project usage, not years of professional experience. Firebase was omitted because evidence was insufficient. No deployments, adoption figures, production readiness or sole authorship are asserted. Each project uses an individually clickable card with an original vector concept illustration. No actual application screenshots were available in the inspected public trees; the illustrations are explicitly labelled and are not represented as product screenshots.

## Links and metrics

- Both old statistics providers returned **503** during the audit. The profile now uses a committed SVG generated from public GitHub REST responses, with a dated [text snapshot](activity.md) and machine-readable `assets/stats/activity.json`.
- Removed the unavailable EchoJobPilot link and the duplicated TraqInn/vehicle link; use the actual `flowsync` repository slug.
- Retained `https://abhisheksnair.vercel.app/`: HTTP **200**, page title “Abhishek S Nair | Software Developer”. The alternative deployment in the portfolio README returned **404** and was excluded.
- LinkedIn matches the public portfolio README but returned **999**, preventing automated availability verification. Email provenance is verified; mailbox deliverability was not tested.
- No fixed contribution counts, streak, fictional city heatmap, “live” metrics or “verified technical domains” remain in either displayed README.

## Rendering and accessibility

The profile uses Markdown, supported HTML and standalone SVG/PNG/GIF images. It does not require JavaScript, injected CSS, iframes or hover behavior. Cards have opaque dark backgrounds for both GitHub themes, and fixed natural widths constrained by GitHub’s responsive image rules allow wrapping.

Each meaningful visual has alternative text. The three original 16-frame loops preserve their original timing and infinite looping, use consistent 240×284 canvases and a shared 128-color palette per animation. Their combined size decreased from 2,288,418 to 1,155,006 bytes (about 50%). Original GIFs remain untouched. New self-contained SVG animations supply six-second ambient particles in the hero, cards, city and footer; their text and artwork stay stationary. `prefers-reduced-motion` picture sources and [README-static.md](../README-static.md) provide static alternatives; support depends on the GitHub client.

## Updating

```sh
python3 scripts/build_profile.py
python3 scripts/update_activity.py
python3 scripts/validate_profile.py
```

The SVG/README generators and activity updater use only Python's standard library. The original raster background and character were created using the built-in image-generation tool; prompts and saved paths are in [ARTWORK.md](ARTWORK.md). To regenerate optimized animation assets, install Pillow in a maintenance environment and run `python3 scripts/optimize_animations.py`. No frontend framework or app build system is needed.

The daily/manual workflow fetches only public owned repositories, paginates them, and excludes forks from star/language aggregation. It uses the workflow token from the environment; tokens are never written into generated files. API errors stop the refresh before files are changed. Branch protection or disabled Actions may prevent automated commits; the dated existing snapshot stays available. Only changed metric values trigger updated files; unchanged checks retain the last changed timestamp, which is documented in the snapshot. A maintainer can run the refresh locally and submit `assets/stats/` and `docs/activity.md` through a PR.

## New visual composition

A 3:1 original violet-moon cityscape forms the precomposited hero, with separate mobile typography. About and Project Focus are paired, followed by a character-centered technology orbit and decorative Hunter ID. Three compact factual tiles precede seven project cards in a three-column desktop gallery. The city scene is explicitly decorative and links to real GitHub activity. Contact cards are actual image links. No fictional rank, location or availability is displayed. The user’s original character GIFs remain visible.
