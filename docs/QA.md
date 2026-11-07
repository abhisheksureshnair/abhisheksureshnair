# Cinematic redesign validation — 2026-11-07

Baseline: `1168134c65e63da6a4a2d0ed22b72c9dab4ca647`. Feature branch: `feat/shadow-monarch-profile-redesign`.

## Rendering and accessibility

- GitHub's Markdown API returned HTTP 200 for the actual README. Its sanitized output was used for browser previews.
- Chromium/Brave previews at 1200×900 (766px content column) and 375×900, in both light and dark modes, reported zero broken images and no horizontal overflow.
- Full desktop light/dark and mobile light screenshots were visually inspected. Project cards form three columns at the desktop profile width and stack on mobile. The hero and section headings have separate mobile compositions.
- Pixel comparisons 1.8 seconds apart confirmed motion in the hero, technology galaxy and footer SVGs. The artwork and text stay stationary while sparse particles pulse and drift.
- Reduced-motion media switched those SVGs to their `-static.svg` versions; the reduced-motion mobile check loaded zero GIFs. The separate static README references no GIFs or SVG animation elements.
- All generated SVGs parse as XML. The validator checks image existence, alternative text, local document links, no external image providers, no scripts/iframes/CSS injection, and the static surface.
- The existing three optimized character GIFs retain their original 16 frames, timings and infinite loops. Their combined size remains about 1.16 MB.
- All 47 distinct referenced assets, including alternate sources, total about 3.19 MB. Browsers load only their selected picture sources. The two original generated raster artworks total about 160 KB; SVG compositions embed optimized versions to avoid cross-origin image dependencies.

## Data and links

Five standard-library regression tests pass:

1. Owned/public/fork scopes and repositories without a language.
2. No content or timestamp changes when metric values remain identical, even on another date.
3. A network failure retains every prior output.
4. Repository pagination and all-null language results.
5. Private events are excluded from the public activity field.

Public repository evidence was refreshed through GitHub's REST API. Project descriptions and stacks retain the source audit in [PROFILE.md](PROFILE.md). The portfolio's prior HTTP 200 result and LinkedIn's HTTP 999 restriction are recorded there. Mailbox delivery is not tested. No imaginary count, streak, professional ranking or experience duration was introduced.

## Screenshots and remaining limits

- [Before — desktop](previews/before-desktop.webp)
- [Before — mobile](previews/before-mobile.webp)

The baseline captures are from the actual public profile. Post-publication captures will be added after the feature branch is published. No reference images, PDF or resume were supplied, so exact reference matching and resume cross-checking cannot be certified. Native GitHub mobile-app behavior is not covered by browser tests.

## Reproduce

```sh
python3 scripts/validate_profile.py
python3 -m unittest discover -s scripts -p test_activity.py -v
```

The daily workflow uses only public API data and publishes when metric values change. Its timestamp identifies the last changed snapshot, not the last successful unchanged check. Workflow registration is checked after publication; a scheduled execution is a separate operational check.
