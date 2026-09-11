# Clawd — iteration-one films

Both Liam films are public in the [CSYE 7270 course playlist](https://www.youtube.com/playlist?list=PLMhsxBEsgHFU), following the course introduction:

1. [Clawd in Walker Jumpman: First Playthrough](https://www.youtube.com/watch?v=0yXF1BMiokc) — native 3840 × 2160, 30 fps; master 6:16. Brutalist `godot-waikthrough walker` and `riff` connect narration to the running game.
2. [Building Clawd: Code to Gameplay, One Change at a Time](https://www.youtube.com/watch?v=azoGEpdrcqo) — native 3840 × 2160, 30 fps; master 7:41. `godot-gamedev walker` pairs seven exact code excerpts with their immediate visible results.

Both show all 18 animation previews, keep the regular outro, and include optional English closed captions. Playlist thumbnail durations may round upward by a second. YouTube's quality controls were checked for 2160p; this is not a claim of an uninterrupted end-to-end streaming benchmark.

## Local masters

```sh
open "/Users/bear/Documents/CoWork/bear-textbooks/books/walker-jumpman-clawd/youtube/claude-liam-walker-jumpman-clawd-walkthrough/exports/landscape/claude-liam-walker-jumpman-clawd-walkthrough.mp4"
open "/Users/bear/Documents/CoWork/bear-textbooks/books/walker-jumpman-clawd/youtube/claude-liam-walker-jumpman-clawd-gamedev/exports/landscape/claude-liam-walker-jumpman-clawd-gamedev.mp4"
```

These are local author-machine paths, not files shipped in a Git clone. Video, audio, generated frames, fonts, dependency directories, and private upload-session records are excluded from Git. Text recipes, code, aligned SRT copies, and small evidence records are included.

## Source and review trail

Each reel contains `SCRIPT.md`, `beat_sheet.json`, `CAPTURE.md`, `FACTCHECK.md`, `QC.md`, source/capture hashes and input/state logs under `evidence/`, and render/QC scripts. `evidence/publication.json` records the confirmed video, playlist position, caption track, and 4K observation. These records do not contain credentials.

The walkthrough's `coverage.json` separates implemented and planned features. The development film's `gamedev-evidence.json` maps source files and the seven code/result pairs. Both use the exact build identified in `evidence/source-build.json`. Film evidence copies of Frictional and the brief are production-time snapshots; the root files carry subsequent entries.

The initial render recipe's authorization was local-only. Bear subsequently explicitly requested publication of both 4K films to this course playlist; the publication record captures that later authorization. Rebuilding a future revision does **not** authorize publishing it.

## Rebuilding / revising

This is film-as-code tied to the author's existing Brutalist installation, not a standalone video SDK. Dependencies include Godot 4.7.2 regular/GDScript, FFmpeg/FFprobe, Node, Python, Brutalist's Remotion dependencies and browser, local Kokoro/Whisper models, and the fonts referenced by the compositions. Some scripts import `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art` explicitly; adapt paths and provision those dependencies on another machine before running.

1. Check the root game manifest and preserve the current masters/receipts. `scripts/author-films.py` is a one-time initializer and refuses existing recipes; do not rerun it over edited films.
2. The walkthrough's `scripts/capture.cjs` records actual Godot takes. Existing named takes are refused to preserve evidence. Successful diagnostic takes used `gallery-one-v2`, `gallery-two-v2`, `gallery-three-v2`, and `inspector-v3`; normal takes used `controls`, `jump`, `spike`, `fall`, `pause`, `coyote`, `buffer`, `finish`, and `mouse`. Read `CAPTURE.md` before recapturing. `scripts/prepare-films.py` binds verified captures and hashes to both reels; it requires the capture MP4s omitted from Git.
3. Narration uses Brutalist `runtime/scripts/generate_audio_kokoro.py`, voice `am_onyx`. Preserve the locked original audio or make a separate revision and remeasure it. Each reel's `scripts/build.py lock` adds measured lead/tail silence and intentionally refuses an already locked recipe. Do not clear that guard merely to rerun a command.
4. Align words with Brutalist `runtime/scripts/align.py`; use the reel's `scripts/build.py cues`, then `footage` and `render`. Existing recipes are audio-locked. Restoring only the text checkout is insufficient: excluded audio, fonts, models and captured media must be regenerated or restored first. `scripts/reuse-film-scenes.py` only reuses scenes after checking matching inputs.
5. Compile with Brutalist's canonical `runtime/scripts/compile.py REEL --height 2160 --fps 30 --out REEL/exports/landscape`. Run the relevant `art godot-waikthrough --check REEL` or `art godot-gamedev --check REEL --game GAME/godot` validator. Run the reel's `scripts/qc.py contacts`, `audio`, `subtitles`, `sweep`, and `report`, then actually inspect the frames. A generated contact sheet is not itself a completed visual review.

`scripts/publish-clawd.py` is scoped to these two authorized films and this existing playlist. It uploads privately, prevents blind duplicate attempts, and requires source hashes, review, captions and a browser 4K observation before final publication. Credentials are supplied outside the repository. Do not reuse the existing authorization for new content.

## What this iteration does not prove

This is one character pass, not completed Assignment 1. The original level, collision and physics remain unchanged. Wider arms can clip the world boundary and overlap world labels. Mini-goals, a full agentic-loop finish, new hazards, and the level extension are later work. Scripted captures and sampled math checks are not human playtests. Start early, make one change, test it, and record failures honestly in [Frictional](../FRICTIONAL.md).
