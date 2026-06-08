# MBA27 Electives Navigator

An interactive schedule browser for the RSM MBA 2026 electives.

## What's here

- **[index.html](index.html)** — the main app. Open it in any browser (or serve it via GitHub Pages).
- **Electives Overview 2026_UPDATED 1 June.pdf** — official course overview from Erasmus
- **Electives Schedule_2026_1 JUNE.pdf** — official schedule with dates/times

## How to use

### For classmates (via GitHub Pages)
Your repo is published at:
```
https://alvee1994.github.io/mba27-electives/
```

Just open that URL — no server needed. Your starred courses are saved in your browser's localStorage.

### Features
- **Interactive Calendar** — all 4 months (Sep–Dec 2026) shown at once, color-coded by subject
- **Conflict detection** — if two starred courses overlap on the same day, both are flagged in red
- **Course Cards** — browse weekday vs. weekend electives separately
- **Search & Filter** — search by name, code, or faculty; filter by subject category
- **My Picks (★)** — star courses from the card view or modal to plan your personal schedule
- **My Picks Toggle** — filter to show only your starred courses
- **Bookmarks persist** — saved in browser localStorage across sessions

## Developing / rebuilding

If you update the PDFs, rebuild `index.html` with:

```bash
python3 build.py
```

This regenerates the card view from `weekday_electives.html` and `weekend_electives.html`.

## Publishing updates to GitHub Pages

```bash
git add .
git commit -m "Update description"
git push origin main
```

GitHub Pages serves the `main` branch root automatically.
