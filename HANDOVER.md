# Handover – MBA27 Electives Navigator

**Last updated:** 8 June 2026  
**Repo:** `github.com:alvee1994/mba27-electives.git` (branch `main`, pushed)  
**Latest commit:** `8db66e1` – Add drag-and-drop preference ranking for up to 6 electives.

---

## Summary

Single-file app (`index.html`) — no bundler, no framework. Students browse 2026 MBA electives, plan around schedule conflicts, and rank up to 6 preferences (mirroring EPRS).

All blocking regressions from the earlier refactor are **resolved**. The JS smoke test passes. Changes are on `main`.

---

## Current Features

### Three views (tabs in header)

| View | Purpose |
|------|---------|
| **Calendar** | Sep–Dec 2026 full-month grid. Click events to toggle selection. Sidebar shows programme, warnings, conflict checks. |
| **Course Cards** | Filterable card grid (weekday / weekend / all tabs). Click card to select; **Details** opens modal; **Draft outline** links to Canvas. |
| **Preference Ranking** | Drag-and-drop EPRS-style ranking. Up to **6** ordered slots. Filter available courses by name / period. **SAVE** persists locally and syncs calendar selection. |

### Programme awareness

- Selector in calendar sidebar: **MBA** (3 electives), **GEMBA** (3), **EMBA** (4).
- `filteredCourses()` hides programme-ineligible courses from chips/cards.
- Calendar still shows restricted courses with dashed styling (`restricted-mba` / `restricted-emba`).
- Banner at top reflects programme rules.

### Selection model (no stars)

- **Course chips** (toolbar): full name + code, e.g. `Business Negotiations (Bneg)`. Click to toggle.
- **Calendar events**: abbreviation + time only, e.g. `SPM 13:30–16:30`. Click to toggle.
- **Preference ranking**: ordered list of up to 6; SAVE copies rankings into chip/calendar selection.

### Conflict detection

- `detectOverlaps()` – pairwise overlaps among selected/ranked courses; hard conflict if >2 shared session dates.
- `getCalendarConflicts()` – per-date highlights on calendar for time overlaps.
- Sidebar banners: programme restrictions, weekday/weekend priority notes, exam reminders, weekend course rules.

### Shared helpers

- `buildBadges()`, `noteTextForDisplay()`, `formatNotesHtml()`, `escapeHtml()` – used by cards and modal.
- LEVET Hague note and exam notes display correctly (badge + deduped notes text).

---

## Data

- **`COURSES` array** – inline in `index.html`. Each course: `code`, `name`, `faculty`, `period` (`weekday`|`weekend`), `categories[]`, `notes`, `restriction` (`null`|`"mba"`|`"emba"`), `href`, `sessions[]`.
- **`restriction:null`** for unrestricted courses (no stray commas).
- **`build.py`** – legacy generator from `weekday_electives.html` / `weekend_electives.html`. **Do not run** without care: it overwrites `index.html` with an old simple layout and wipes the interactive app.

---

## localStorage keys

| Key | Content |
|-----|---------|
| `mba_programme` | `"MBA"` \| `"GEMBA"` \| `"EMBA"` |
| `mba_selected` | JSON array of selected course codes (Set) |
| `mba_rankings` | JSON array of up to 6 codes, ordered (rank 1 first) |
| `mba_stars` | Legacy; migrated to `mba_selected` on load if present |

---

## Smoke test

```bash
node -e "const fs = require('fs'); const script = fs.readFileSync('index.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1]; new Function(script);"
```

Open `index.html` locally (or GitHub Pages once enabled) and verify:

1. Calendar renders all four months.
2. Programme selector filters chips/cards and updates sidebar count (3 vs 4).
3. Chip + calendar selection highlights events; conflict warnings appear when overlaps exist.
4. Preference Ranking: drag between panels, reorder slots, SAVE shows toast and updates calendar.

---

## Files

| File | Role |
|------|------|
| `index.html` | **All app code** (HTML, CSS, JS, course data) |
| `build.py` | Legacy static page generator — not the source of truth for the live app |
| `weekday_electives.html`, `weekend_electives.html` | Source tables for `build.py` only |
| `Electives Overview 2026_UPDATED 1 June.pdf` | Linked from resource cards |
| `Electives Schedule_2026_1 JUNE.pdf` | Linked from resource cards |
| `FAQ Elective General Requirements_2026_v 7 May.pdf` | **Untracked** — not linked in app yet |
| `screencapture-electives-myrsm-nl-preferences-*.png` | **Untracked** — reference screenshot for ranking UI |

---

## Git / deploy

```bash
git status
git add index.html HANDOVER.md   # add others as needed
git commit -m "…"
git push origin main
```

**GitHub Pages:** not confirmed enabled. To publish: repo **Settings → Pages → Deploy from branch `main` / root**.

---

## Possible next work

1. **Link FAQ PDF** in resource cards (file exists locally, untracked).
2. **Export ranking** – copy ranked list as text/CSV for pasting into EPRS.
3. **Ranking validation** – warn if fewer than 6 ranked before SAVE (EPRS requires 6; app allows 1–6).
4. **Mobile ranking UX** – drag-and-drop is awkward on touch; consider tap-to-add + move up/down buttons.
5. **Course data updates** – if schedule changes, edit `COURSES` in `index.html` directly (or extend `build.py` to emit course JSON without replacing the whole page).
6. **`advanced/` folder** – untracked; inspect before assuming it is part of the deploy.

---

## Commit history (recent)

```
8db66e1 Add drag-and-drop preference ranking for up to 6 electives.
e9a86d7 Show full course names on selection chips.
cb37b9f Replace star bookmarks with clickable course chip selection.
1a57b88 Fix electives navigator regressions from programme refactor.
4de4646 Initial commit
```

---

## Quick orientation for a new session

1. Read `index.html` `<script>` block from `COURSES` → helpers → view/render functions.
2. Run smoke test (above).
3. Test the three views and SAVE on Preference Ranking.
4. Do **not** run `build.py` unless rebuilding the data pipeline intentionally.
