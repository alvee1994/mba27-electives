# Handover – MBA27 Electives Navigator

## Summary
- The app was refactored to add programme-aware planning (MBA / GEMBA / EMBA), calendar conflict detection, sidebar warnings, and full-month calendar rendering.
- While restructuring the data and UI, several breaking regressions slipped in: invalid course objects, stale function calls, and UI wiring that doesn’t yet honour programme rules.
- Do **not** push to production until the issues below are resolved and the JS smoke test (`new Function(script)`) passes.

## Blocking Issues
1. **Broken JS (runtime failure)**
   - `detectConflicts()` was removed but is still referenced (e.g. in `renderSidebar`). This throws an "Unexpected token" error before any UI renders.
   - Must replace those references with the new `detectOverlaps()` pipeline and ensure the function returns the shape the sidebar/calendar expect.

2. **Corrupted course objects**
   - Many course entries now read `notes:"", restriction:"", , href:"…"` (note the double comma). That breaks the COURSES array and prevents rendering entirely.
   - Need to regenerate/reformat the course array so every object is valid JS. Consider rebuilding via `build.py` or a small script.

3. **Programme logic incomplete**
   - Programme selector value isn’t passed into the cards/calendar filters yet – all courses show regardless of restriction.
   - Sidebar warnings about required course counts and overlaps are wired, but they rely on the broken conflict detector above.

4. **Modal/card regressions**
   - LEVET’s “sessions in The Hague” note never displays (conditional filters it out).
   - Modal string building mixes template literals and concatenation, making further editing error-prone; also dedupe the badges vs. notes copy.

## Next Steps
1. **Repair COURSES array**
   - Easiest path: re-run `build.py` or write a quick formatter to ensure `restriction` is always present (e.g. `restriction:null` when unrestricted) and no stray commas.

2. **Replace `detectConflicts` usage**
   - Update `renderSidebar`, `renderCalendar`, etc. to consume the new `detectOverlaps` output (`{code1, code2, sharedDates, hardConflict}`) and remove the old function entirely.

3. **Wire programme filter + warnings**
   - Apply programme restrictions when computing `filteredCourses()` (skip MBA-only courses for EMBA/GEMBA unless explicitly allowed, and vice versa).
   - Ensure the sidebar course count (3 vs 4) is enforced before enabling the “My Picks” filter/summary.

4. **Clean up modal/card rendering**
   - Reintroduce a consistent component for restriction/exam badges so both cards and modal share the same markup.
   - Always show notes (after escaping), even if a badge also displays, so contextual info like “sessions in The Hague” isn’t lost.

5. **Smoke test before push**
   - Run `node -e "const fs = require('fs'); const script = fs.readFileSync('index.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1]; new Function(script);"`
   - Open `index.html` locally to confirm calendar renders, programme selector works, and sidebar warnings behave.

## Files to Inspect First
- `index.html` (all work is here; no bundler)
- `build.py` (for regenerating course JSON if needed)

## Reminder
After fixes, re-run `git status`, stage, commit, and push to `main`. Enable GitHub Pages (Main branch / root) once the build is stable.
