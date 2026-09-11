# Frictional — an honest effort log

This records actual effort, including uncertainty and failed attempts. It is not
a success story retroactively spread across several days. All entries below are
from September 11, 2026 unless another actual date is recorded.

## Session 1 — scope and first implementation

- **Human contribution:** Bear chose Clawd, named the separate project
  walker-jumpman-clawd, supplied its GitHub destination, and asked for one change
  at a time. Task mini-goals and a full agentic loop are future design intent.
- **AI contribution:** inspected the starter and Brutalist's 18 animations;
  cloned the starter with history into a separate checkout; implemented a
  drawing-only GDScript port and a separate animation gallery.
- **Prediction:** wide art may miscommunicate collision. Preserve the 18 × 28
  collider first, expose the difference, and ask the human to judge it in play.
- **Design decision:** physics supplies the airborne trajectory. Hold the
  mascot's apex pose instead of adding the gallery animation's second jump arc.
- **Status at this entry:** implementation written; tests and visual inspection
  pending. No human playtest or completed Assignment 1 claimed.

## Session 1 — checks and a production error

- The 25 original mechanics checks and 9 synthetic-keyboard checks passed.
  The original physics function, tuning resource, level JSON, and HUD were
  compared with the starter commit and are byte-identical.
- The independent TypeScript reference supplied 162 animation samples. The
  GDScript test passed 1,944 scalar comparisons and six staged presentation
  checks. This establishes sampled parity, not that every possible frame is right.
- Native 4K pilot inspection: Clawd is recognizable in the existing level;
  the wide arms and unchanged collision box remain an explicit review question.
  Gallery page 1 renders all six labelled motions clearly.
- **Actual AI error:** the film-authoring script initially had two malformed
  dictionary entries for editor notes. Python's syntax check rejected it before
  execution. Added the missing `value` keys and reran successfully. This was a
  production-script error, not a game mechanics failure.
- Human play-feel and film approval remain pending. No future day of work is
  claimed and no new task-goal behavior is represented as implemented.
- **Actual capture failure:** one 18-second gallery take contained 343 saved
  frames instead of the expected 540. Its driver counted process updates while
  render callbacks could be throttled. The early receipt's PASS is insufficient;
  the take is rejected for the film and retained. Revised the diagnostic-only
  harness to advance the display clock per rendered frame and require 600 saved
  frames for 20 seconds. Re-recording uses `-v2` names, preserving original takes.

## Next-entry template (copy for the next actual session)

Date/session · intention · prediction · actual attempt · what failed or surprised
me · evidence/command/commit · what I changed or rejected · retest and limits ·
human versus AI contributions · one next step.

An unsuccessful test is useful when it says what did not work and informs the
next decision. Do not invent a failure just to fill this log.
