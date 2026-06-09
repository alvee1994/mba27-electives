# Implementation Plan: Elective Overlap + Instructor Profiles

**Date:** 2026-06-09  
**Branch:** `feature/overlap-instructor-profiles` (from `main` at `8839d6c`)  
**Scope:** Two features — (1) Identify topic/schedule overlap between different electives, (2) Instructor profile cards with academic vs. practical experience

---

## Feature 1: Elective Overlap Identification

### Problem
Students currently see **schedule** overlap (same date/time clashes) via the calendar conflict detector, but have no way to see **topical** overlap between courses. Two electives might cover the same domain (e.g., both "Finance + Strategy") without any scheduling conflict. Students want to avoid picking redundant courses and instead build a diverse skill set.

### What "overlap" means here
1. **Category overlap** — courses sharing one or more `categories[]` tags (e.g., MA and MCT both span "Finance" + "Strategy")
2. **Schedule overlap** — already implemented via `detectOverlaps()`, but currently only surfaced when courses are *selected*. We'll add a proactive overlap explorer.
3. **Cross-reference overlap** — the same instructor teaching multiple electives (e.g., Caroline Witte teaches both DGBS and ADVSTR; Christopher Sabel teaches HPCsC and ADVSTR; Vareska van de Vrande teaches LEVET and HPCsC)

### Implementation steps

#### 1A. New data: `TOPIC_OVERLAPS` map (computed at runtime)
No new data structure needed — we compute overlap from existing `COURSES` and `ADVANCED_COURSES` at render time.

**Logic** (`computeTopicOverlaps()`):
```
For each pair of courses:
  - sharedCats = intersection of categories[]
  - sharedFaculty = intersection of parsed faculty names
  - sharedDates = countSharedDates() + timesOverlap check (reuse existing)
If any of sharedCats, sharedFaculty, or sharedDates > 0:
  add to overlaps array with { code1, code2, name1, name2, sharedCats, sharedFaculty, sharedDates }
```

#### 1B. New view tab: "Overlap Explorer"
Add a 4th tab to the view switcher (Calendar | Course Cards | Preference Ranking | **Overlap**).

**Layout:**
- **Subject overlap matrix** — a visual heatmap/grid. Rows = courses, columns = categories. Cells are colored when a course belongs to a category. Overlapping cells (courses sharing a category) are highlighted with connecting lines or grouped visually.
- **Overlap pairs list** — for each pair with shared categories/faculty/dates, show:
  - Course A ↔ Course B
  - Shared categories (colored pills)
  - Shared faculty (if any)
  - Shared session dates (if any, with time overlap indicator)
  - A recommendation badge: "⚠️ High topic overlap — consider diversifying" if they share 2+ categories; "💡 Partial overlap" if 1 category; "📅 Schedule conflict" if only date overlap
- **Filter by category** — chips to filter overlap pairs to a specific category

#### 1C. Overlap badges on existing Course Cards
- On each course card (in the Course Cards view), add a small **overlap indicator** next to the category pills, e.g., "↔ 3 overlaps" that opens the overlap detail when clicked.
- In the course modal (openModal), add a new section: **"Related Courses"** showing courses with shared categories, faculty, or dates.

#### 1D. Overlap warnings in Calendar sidebar
- When a student selects courses that have high topical overlap (2+ shared categories), show a **soft warning** (yellow, not red like schedule conflicts): "⚠️ MA and MCT share Finance + Strategy — you may cover similar ground."

---

## Feature 2: Instructor Profile Cards

### Problem
Students know almost nothing about who teaches each course beyond a name string. They want to know: *Is this instructor purely academic, or do they have real industry experience? Will I learn current practices or only theory?*

### Data model

Add a new `INSTRUCTORS` object (keyed by normalized name) inline in `index.html`:

```js
const INSTRUCTORS = {
  "Maartje Schouten": {
    title: "Dr.",
    role: "Assistant Professor, RSM",
    education: "PhD in Organizational Psychology, EUR",
    experience: [
      { type: "academic", desc: "Asst. Professor at RSM since 2019" },
      { type: "practical", desc: "Consultant at KPMG Advisory (2014–2018)" }
    ],
    experienceType: "mixed",  // "academic", "practical", "mixed"
    profileUrl: "https://www.rsm.nl/people/maartje-schouten/"
  },
  // ... one entry per instructor
};
```

**`experienceType` values (strict classification):**
- `"academic"` — career is entirely in academia (PhD → postdoc → professor). Advisory work, executive education, or consulting done alongside a professor role does NOT qualify as industry experience.
- `"practical"` — career is primarily industry (came to teaching later, teaching is secondary to their practice)
- `"mixed"` — has held **substantive industry positions** (employed at companies, ran businesses, worked in banking/PE/consulting firms) before or alongside their academic career. Mere advisory roles, executive education, or research collaborations with industry do NOT qualify. The "mixed" badge reads "Industry + Academic" (industry first) to emphasize this distinction.

**Current counts:** academic: 37, mixed: 2, practical: 6

**Mixed qualifiers (strict):**
- Maartje Schouten — Consultant at KPMG Advisory (2014–2018), actual corporate consulting employment
- Erik Roelofsen — Worked in investment banking and PE before entering academia

**Badge on cards:**
- 🎓 Academic-only → blue badge "Academic"
- 💼 Industry → amber badge "Practical Experience"  
- 🔄 Mixed → green badge "Academic + Industry"

### Implementation steps

#### 2A. Instructor data collection
This is the **largest manual effort**. We need to research each of the ~35 unique instructors. Sources:
- RSM faculty directory (rsm.nl/people/)
- LinkedIn profiles
- Google Scholar
- Course outline PDFs (may have bio sections)

**Research template per instructor:**
| Field | Source | Notes |
|-------|--------|-------|
| title | RSM page | Dr., Prof. Dr., etc. |
| role | RSM page | Asst. Prof, Assoc. Prof, etc. |
| education | RSM page / LinkedIn | Highest degree + institution |
| experience | LinkedIn / RSM page | 2–4 bullet points covering career |
| experienceType | Derived | academic / practical / mixed |
| profileUrl | RSM page | Link to official profile |

**Phased approach:**
1. **Phase 1 (ship fast):** Research all RSM faculty via rsm.nl/people/ — most have structured profiles already. For instructors with no RSM page, use LinkedIn or leave minimal data with a "Profile not found" note.
2. **Phase 2 (polish):** Fill gaps for "et al" instructors and non-RSM adjuncts.

#### 2B. Instructor card in Course Cards view
Extend each course card's faculty line:

**Before:**
```
👤 Maartje Schouten & Dimitrios Tsekouras
```

**After:**
```
👤 Maartje Schouten [🔄 Mixed] & Dimitrios Tsekouras [🎓 Academic]
```

Each instructor name becomes a **clickable link** that opens an instructor profile popover/modal.

#### 2C. Instructor profile modal
A new modal (or reuse the existing `#modal` overlay) showing:

```
┌─────────────────────────────────────────┐
│  Dr. Maartje Schouten            [✕]    │
│  🔄 Academic + Industry Experience      │
│  Assistant Professor, RSM               │
│─────────────────────────────────────────│
│  📚 Education                           │
│  PhD Organizational Psychology, EUR     │
│  MSc Psychology, University of Amsterdam│
│─────────────────────────────────────────│
│  💼 Experience                           │
│  • Asst. Professor, RSM (2019–present)  │
│  • Consultant, KPMG Advisory (2014–18)  │
│─────────────────────────────────────────│
│  📖 Teaches                             │
│  • Business Negotiations (Bneg)          │
│                                         │
│  [🔗 RSM Profile ↗]                    │
└─────────────────────────────────────────┘
```

#### 2D. Instructor index section
Add a collapsible **"Browse by Instructor"** section in the Course Cards view showing all instructors as small cards, filterable by experience type. Clicking an instructor filters courses to those they teach.

#### 2E. Faculty name normalization
Current `faculty` field is a free-text string like `"Caroline Witte & Marijn Faling"` or `"Steffen Giessner, Antonie Knoppers et al"`. We need a parser:

```js
function parseFaculty(facultyStr) {
  // Split on " & " or ", "
  // Strip titles: "Dr.", "Prof. Dr.", "Prof. dr"
  // Flag "et al" as incomplete
  // Return array of { name, title, normalizedName }
}
```

Then match `normalizedName` against `INSTRUCTORS` keys. For "et al" entries, show the named instructors plus an "+ more faculty" note.

---

## File changes summary

| File | Change |
|------|--------|
| `index.html` | All changes — this is a single-file app |
| `plan.md` | This file (new) |

### Inside `index.html`:

1. **`INSTRUCTORS` data object** (~35 entries, after `ADVANCED_COURSES`)
2. **`parseFaculty()` helper** — normalize faculty strings
3. **`computeTopicOverlaps()` function** — compute all pairwise overlaps
4. **Overlap Explorer view** — new tab + rendering functions
5. **Overlap badges on course cards** — in `renderCards()`
6. **Overlap section in course modal** — in `openModal()`
7. **Topic overlap warnings in sidebar** — in `renderSidebar()`
8. **Instructor badges on course cards** — experience type pills next to faculty names
9. **Instructor profile modal** — new `openInstructorModal(name)` function
10. **Instructor index section** — collapsible grid in Course Cards view
11. **CSS additions** — overlap heatmap, instructor card, experience badge styles

---

## Execution order

### Step 1: Data foundations (non-visual, no risk of regression)
1. Add `INSTRUCTORS` object with placeholder data for all ~35 instructors
2. Add `parseFaculty()` helper
3. Add `computeTopicOverlaps()` function
4. Verify smoke test still passes

### Step 2: Overlap Explorer (new view, isolated)
1. Add "Overlap" tab to view switcher
2. Implement overlap pairs list rendering
3. Add category filter chips
4. Test in isolation

### Step 3: Overlap integration into existing views
1. Add overlap badges to course cards
2. Add "Related Courses" section to course modal
3. Add topical overlap warnings to calendar sidebar
4. Regression test all views

### Step 4: Instructor profiles
1. Populate `INSTRUCTORS` with real data (research phase — longest step)
2. Add experience type badges to course card faculty lines
3. Implement instructor profile modal
4. Add instructor index section
5. Link instructor names to profiles
6. Final regression test

### Step 5: Polish & deploy
1. Mobile responsive checks for new components
2. Update `HANDOVER.md`
3. Commit & push to `main`

---

## Risks & mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Instructor data unavailable for some faculty | Gaps in profile cards | Show "Profile not yet available" with a link to search RSM directory; don't block shipping |
| `parseFaculty()` misparses names with titles like "Prof. Dr." | Wrong instructor lookup | Careful regex testing against all 35 faculty strings; unit test with actual values |
| Overlap Explorer too slow with N² pairs | Sluggish UI | 35 courses → only ~600 pairs; trivial. Cache result. |
| Overlap badges clutter course cards | Card UI too busy | Use small icons/pills; only show count, expand on click |
| Experience classification subjective | Students misinterpret | Use explicit labels: "Academic career" vs "Industry experience" vs "Both"; let students decide |

---

## Open questions (to resolve before implementation)

1. **Should overlap explorer include advanced courses?** — Recommend yes (students may want to see how an advanced course overlaps with electives they're considering).
2. **How deep should instructor research go?** — Recommend: title, role, education (1–2 lines), and 2–4 career highlights. Not a full CV. Link to RSM profile for more.
3. **Should instructor data be editable by students?** — Recommend no for v1. Could add a "Suggest edit" link in v2.
