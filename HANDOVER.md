# Handover – MBA27 Electives Navigator

**Last updated:** 9 June 2026  
**Repo:** `github.com:alvee1994/mba27-electives.git` (branch `feature/overlap`, local)  
**Latest commit:** `8839d6c` on `main` — advanced courses overlap UI. Overlap explorer + instructor profiles on `feature/overlap` (uncommitted).

---

## Summary

Single-file app (`index.html`) — no bundler, no framework. Students browse 2026 MBA electives, plan around schedule conflicts, rank up to 6 preferences (mirroring EPRS), and optionally overlay their **advanced course** to spot timetable clashes.

All blocking regressions from the earlier refactor are **resolved**. The JS smoke test passes. Advanced course PDFs and overlap UI are on `main`.

---

## Current Features

### Four views (tabs in header)

| View | Purpose |
|------|---------|
| **Calendar** | Sep–Dec 2026 full-month grid. Click events to toggle selection. Sidebar shows programme, electives, advanced course, warnings, conflict checks, and **topical overlap** warnings when 2+ categories overlap among selected electives. |
| **Course Cards** | Filterable card grid (weekday / weekend / all tabs). Electives only. Click card to select; **Details** opens modal with **Related Courses**; **Draft outline** links to Canvas. Faculty names are clickable with experience badges (🎓 Academic / 💼 Industry / 🔄 Mixed). **Browse by Instructor** collapsible index filters courses by teacher. Overlap count pill (↔ N overlaps) links to Overlap view. |
| **Preference Ranking** | Drag-and-drop EPRS-style ranking. Up to **6** ordered slots. Electives only — advanced courses are excluded. **SAVE** persists locally and syncs calendar selection. |
| **Overlap** | Proactive overlap explorer: category heatmap matrix, filterable overlap pairs list (shared categories, faculty, schedule). Includes electives **and** advanced courses. |

### Programme awareness

- Selector in calendar sidebar: **MBA** (3 electives), **GEMBA** (3), **EMBA** (4).
- `filteredCourses()` hides programme-ineligible courses from chips/cards.
- Calendar still shows restricted courses with dashed styling (`restricted-mba` / `restricted-emba`).
- Banner at top reflects programme rules.

### Selection model

**Electives** (multi-select):
- **Course chips** (toolbar): full name + code, e.g. `Business Negotiations (Bneg)`. Click to toggle.
- **Calendar events**: abbreviation + time only, e.g. `SPM 13:30–16:30`. Click to toggle.
- **Preference ranking**: ordered list of up to 6; SAVE copies rankings into chip/calendar selection.

**Advanced course** (single-select, overlap check only):
- Separate picker below elective chips, gold **dashed** styling (`advanced-chip`).
- Only one advanced course at a time (`selectedAdvanced` / `mba_advanced`).
- Shown on calendar with dashed border + stripe pattern; selected state uses gold dashed outline (electives use solid white).
- **Not** included in preference ranking, course cards, or elective count.
- Sidebar panel: **My Advanced Course** (separate from **My Electives**).
- Conflict detection includes advanced + selected electives together.

### Conflict detection

- `detectOverlaps()` – pairwise overlaps among selected electives **and** advanced course; hard conflict if >2 shared session dates.
- `getCalendarConflicts()` – per-date highlights on calendar for time overlaps.
- Sidebar banners: programme restrictions, weekday/weekend priority notes, exam reminders, weekend course rules.

### Shared helpers

- `findCourse(code)` – looks up `COURSES` then `ADVANCED_COURSES`.
- `isAdvancedCourse(code)`, `selectedAdvancedCourse()`, `plannerSelectionCount()`.
- `buildBadges()`, `noteTextForDisplay()`, `formatNotesHtml()`, `escapeHtml()` – used by cards and modal.
- `parseFaculty(str)` – splits faculty strings, strips titles, flags `et al`.
- `computeTopicOverlaps()` – cached pairwise overlaps (categories, faculty, schedule) across electives + advanced courses.
- `overlapsForCourse(code)`, `detectTopicOverlapWarnings(courses)` – overlap integration helpers.
- `buildFacultyHtml(str)` – clickable instructor links with experience badges.
- `openInstructorModal(name)` – instructor profile modal (reuses `#modal` overlay).
- LEVET Hague note and exam notes display correctly (badge + deduped notes text).

---

## Data

### Electives — `COURSES` array

Inline in `index.html`. Each course: `code`, `name`, `faculty`, `period` (`weekday`|`weekend`), `categories[]`, `notes`, `restriction` (`null`|`"mba"`|`"emba"`), `href`, `sessions[]`.

### Instructor profiles — `INSTRUCTORS` object

Inline in `index.html`, after `ADVANCED_COURSES`. Keyed by normalized faculty name. Fields: `title`, `role`, `education`, `experience[]` (type + desc), `experienceType` (`academic` | `practical` | `mixed`), `profileUrl`. ~45 entries covering all named faculty from course data. Adjuncts without RSM pages have minimal data; modal shows “Profile not yet available” fallback.

### Advanced courses — `ADVANCED_COURSES` array

Inline in `index.html`, immediately after `COURSES`. Same shape plus `isAdvanced: true`. PDF outlines live in `advanced/`.

| Code | Name | Sessions in app |
|------|------|-----------------|
| `ADVFIN` | Advanced Finance | 10 (Sep 3 – Oct 5, 13:30–16:30) |
| `ADVMKT` | Advanced Marketing: Marketing & AI | 10 (Sep 3 – Sep 24; paired AM/PM on same days) |
| `ADVSCM` | Advanced Supply Chain Management | 10 (Sep 3 – Oct 19; S6 is Tue 09:30–12:30) |
| `ADVSTR` | Advanced Strategy | 10 (Sep 14 – Sep 29; paired AM/PM) |
| `ADVSUS` | Advanced Sustainability | **0** — draft outline has no session dates |

**ADVSUS gap:** Included in picker and sidebar with “dates TBA” messaging. Add `sessions[]` once dates are confirmed (Canvas/MyTimetable).

### Legacy

- **`build.py`** – generator from `weekday_electives.html` / `weekend_electives.html`. **Do not run** without care: it overwrites `index.html` with an old simple layout and wipes the interactive app.

---

## localStorage keys

| Key | Content |
|-----|---------|
| `mba_programme` | `"MBA"` \| `"GEMBA"` \| `"EMBA"` |
| `mba_selected` | JSON array of selected elective codes |
| `mba_rankings` | JSON array of up to 6 elective codes, ordered (rank 1 first) |
| `mba_advanced` | Single advanced course code, or absent when none selected |
| `mba_stars` | Legacy; migrated to `mba_selected` on load if present |

---

## Smoke test

```bash
node -e "const fs = require('fs'); const script = fs.readFileSync('index.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1]; new Function(script);"
```

Open `index.html` locally (or GitHub Pages once enabled) and verify:

1. Calendar renders all four months (Sep–Dec 2026).
2. Programme selector filters chips/cards and updates sidebar count (3 vs 4).
3. Elective chip + calendar selection highlights events; conflict warnings appear when overlaps exist.
4. Advanced picker: select one course; calendar shows dashed events; overlaps with electives surface in sidebar.
5. Preference Ranking: drag between panels, reorder slots, SAVE shows toast and updates calendar (electives only).
6. Overlap tab: heatmap renders; pairs list filters by category; clicking overlap pill on a card jumps to filtered pairs.
7. Course Cards: instructor names open profile modal; Browse by Instructor filters cards; topical overlap warning in sidebar when MA + MCT (or similar) both selected.

---

## Files

| File | Role |
|------|------|
| `index.html` | **All app code** (HTML, CSS, JS, course data) |
| `advanced/*.pdf` | Draft advanced course outlines (linked from `ADVANCED_COURSES[].href`) |
| `build.py` | Legacy static page generator — not the source of truth |
| `weekday_electives.html`, `weekend_electives.html` | Source tables for `build.py` only |
| `Electives Overview 2026_UPDATED 1 June.pdf` | Linked from resource cards |
| `Electives Schedule_2026_1 JUNE.pdf` | Linked from resource cards |
| `FAQ Elective General Requirements_2026_v 7 May.pdf` | **Untracked** — not linked in app yet |
| `screencapture-electives-myrsm-nl-preferences-*.png` | **Untracked** — reference screenshot for ranking UI |

---

## Git / deploy

```bash
git status
git add index.html HANDOVER.md advanced/   # add others as needed
git commit -m "…"
git push origin main
```

**GitHub Pages:** not confirmed enabled. To publish: repo **Settings → Pages → Deploy from branch `main` / root**.

---

## Possible next work

1. **ADVSUS session dates** — add to `ADVANCED_COURSES` once available from Canvas/MyTimetable.
2. **Link FAQ PDF** in resource cards (file exists locally, untracked).
3. **Export ranking** — copy ranked list as text/CSV for pasting into EPRS.
4. **Ranking validation** — warn if fewer than 6 ranked before SAVE (EPRS requires 6; app allows 1–6).
5. **Mobile ranking UX** — drag-and-drop is awkward on touch; consider tap-to-add + move up/down buttons.
6. **Course data updates** — edit `COURSES` / `ADVANCED_COURSES` in `index.html` directly (or extend `build.py` to emit JSON without replacing the whole page).
7. **Instructor data polish** — verify RSM profile URLs and fill gaps for adjunct / `et al` faculty (Phase 2 from plan).

---

## Commit history (recent)

```
8839d6c Add advanced courses to calendar for elective overlap checking.
8db66e1 Add drag-and-drop preference ranking for up to 6 electives.
e9a86d7 Show full course names on selection chips.
cb37b9f Replace star bookmarks with clickable course chip selection.
1a57b88 Fix electives navigator regressions from programme refactor.
4de4646 Initial commit
```

---

## Quick orientation for a new session

1. Read `index.html` `<script>`: `COURSES` → `ADVANCED_COURSES` → helpers → view/render functions.
2. Run smoke test (above).
3. Test calendar (elective + advanced selection), cards, and preference ranking SAVE.
4. Do **not** run `build.py` unless rebuilding the data pipeline intentionally.

---

## Session notes (clear for next agent)

**Last session completed:**
- Implemented **Overlap Explorer** (4th tab): category heatmap, filterable overlap pairs, integration with course cards/modal/sidebar.
- Implemented **Instructor profiles**: `INSTRUCTORS` data, experience badges, profile modal, Browse by Instructor index.
- Branch: `feature/overlap`. Changes uncommitted at session end.

**Untracked local files (not on remote):**
- `FAQ Elective General Requirements_2026_v 7 May.pdf`
- `screencapture-electives-myrsm-nl-preferences-2026-06-08-12_32_56.png`
- `plan.md`
