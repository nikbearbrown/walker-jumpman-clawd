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

## Session 1 — capture recovery and finished-film checks

- **Second capture failure:** the first revised inspector stopped at its process
  limit without a completion receipt. Exit code zero did not establish success.
  Rejected that take and retained its partial frames/logs. Increased only the
  diagnostic harness's bounded process allowance; normal gameplay capture was
  unchanged. The three gallery `-v2` takes and inspector `-v3` each completed
  600 native 4K frames, giving 20 seconds at 30 fps.
- **Visual pilot failure:** the title-card correction used a multi-word trigger
  that the existing component's word matcher did not recognize. The first
  render left the wrong sentence on screen. Changed the trigger to one word,
  forced a fresh render, and inspected the correction from “Build everything
  today” to “Build one change today.”
- **Observed tradeoffs, not hidden fixes:** the broad arms can extend beyond the
  left world boundary, and the character can pass in front of world labels.
  These are visible in real gameplay. The original collider and level remain
  unchanged for this character-only iteration; readability and collision
  fairness are questions for Bear's next play session.
- The two completed masters are 3840 × 2160 at 30 fps: walkthrough 376.133 seconds
  and game-development explainer 461.467 seconds. Every section's narration or
  stock outro was compared with its source and passed preservation/alignment
  checks. This is not a human listening or pronunciation approval.
- The footage uses scripted normal input, not human playtesting. Repeated
  footage is labelled as the same take, not additional evidence. Gallery and
  collider-inspection scenes are explicitly diagnostic.
- **Human/AI boundary:** Bear supplied the intent and constraints. AI implemented,
  captured, tested, wrote and rendered this iteration. Human play-feel judgments,
  film approval and the next design decision remain pending. No YouTube
  publication has been performed. Final per-film review evidence lives under
  `youtube/`; this log does not claim future days of work.

## Session 1 — publication authorized and verified

- Bear subsequently requested both 4K films be published to the CSYE 7270
  playlist. That authorizes publication; it does not invent a human playtest or
  a claim that Bear watched and approved every frame.
- AI completed final visual review: 68 walkthrough contact pages and 79
  development-film pages, supplementing per-beat and native-resolution checks.
  Both were uploaded once with their aligned English caption tracks.
- The first immediate playlist verification did not yet see the new entry.
  Retained the returned insertion ID, inspected the server state, and reconciled
  it without a duplicate upload or playlist insertion. Added bounded read-only
  verification retries and an insertion-attempt guard to the publisher.
- Confirmed both videos public, positions 2 and 3 after the course introduction.
  The walkthrough quality menu offers 2160p 4K; the development player reports
  Auto (2160p 4K). These are availability observations, not continuous streaming
  performance tests. Publication records live with each reel's evidence.

## Next-entry template (copy for the next actual session)

Date/session · intention · prediction · actual attempt · what failed or surprised
me · evidence/command/commit · what I changed or rejected · retest and limits ·
human versus AI contributions · one next step.

An unsuccessful test is useful when it says what did not work and informs the
next decision. Do not invent a failure just to fill this log.
