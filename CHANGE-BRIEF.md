# Iteration 1 — Clawd first, one change at a time

September 11, 2026. Project: **walker-jumpman-clawd**. Professor Bear's evolving
CSYE 7270 Assignment 1 example, forked from walker-jumpman. This iteration is
not a completed Assignment 1 submission: the required level extension is later.

## Human intent

Bear wants the player to be a coding agent, represented by Clawd. Eventually,
mini-goals will represent completed tasks and the final goal a full agentic loop.
**Those task goals, new hazards, and the level extension are not implemented now.**
First inspect the character in the existing level, then decide the next change.

## Predict

1. The wide Clawd silhouette may overhang the unchanged collision box. An arm
   can overlap a hazard without contact; inspect rather than silently retune.
2. Playing a decorative jump loop on a physically jumping body could create
   two apparent jump arcs. The airborne pose must not add a second displacement.
3. A library of 18 animations might be mistaken for 18 implemented abilities.
   Separate the gallery from actual gameplay and label the difference.

## Build → Playtest → Inspect → Revise

Change drawing and presentation selection only. Preserve the player physics
function, tuning, collision shape, level JSON, hazards, camera, input bindings,
and recovery. Reuse Brutalist's rectangle-based animation library in GDScript.
Keep a separate gallery to inspect every animation without inventing new moves.

Rerun starter mechanical/keyboard checks; compare source invariants. Capture real
Godot output with scripted normal input, separately from diagnostic previews.
Record failures as they occur in [FRICTIONAL.md](FRICTIONAL.md). Machine checks
cannot decide whether the new silhouette feels fair or whether the game is fun.

## Next session, not a fabricated day's work

Bear plays and chooses one improvement or test. A later iteration can implement
one mini-goal, then test its completion/reset behavior before adding another.
Start early: short repeated sessions leave time to discover what does not work.
No minimum hours, artificial struggle, or invented dates are expected.

AI: code, inspection, test execution, documentation, narrated film production.
Human: intent, scope, art judgment, play-feel review, and the next decision.
