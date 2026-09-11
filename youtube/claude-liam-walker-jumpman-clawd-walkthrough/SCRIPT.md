# Clawd Takes the First Step

## B00 — Professor Bear starts Assignment 1

Please use Walker to convert my game design document about a coding-agent platformer into one small revision: put Clawd in the existing level. Preserve the mechanics. I'm Liam, in for Professor Bear. His project is Walker Jumpman Clawd. The opening prompt is a suggested handoff, not a saved conversation.

## B01 — One character, the same level

We have changed the character, not completed the assignment. Clawd now moves through the existing First Steps level. The physics and layout remain the starter's. A separate gallery contains eighteen animations. Task mini-goals, new hazards, and the required level extension are later decisions. This is the first revision of a semester-long example.

## B02 — The loop is one inspectable change

Predict what might break. Build one change. Play it, inspect the evidence, revise, then record the version. Here the prediction is specific: Clawd's wide arms might make the unchanged collision box misleading. A small experiment gives us a question to answer. Changing the character, level, and physics together would make that answer harder to isolate.

## B03 — Meet Clawd in the original course

Here is the actual Godot level. Enter starts, left and right move, and the character stops after release. Clawd's legs now animate with movement; the ground and controls have not been redesigned. These are scripted normal-input captures, not Professor Bear's playtest. The first visual question is simple: can you read this character at game size?

## B04 — One body, one physical jump

Watch the feet leave the ground and return. Holding Space does not bounce again on landing, and another press in the air does not create a double jump. The airborne drawing holds a pose while physics supplies the trajectory. An animation named jump must not secretly add another movement mechanic.

## B05 — The arm is not the collision box

This enlarged view uses the actual Godot drawing routine. The blue rectangle marks the unchanged eighteen by twenty-eight collision reference. Clawd's arms extend beyond it. That is a real first-pass tradeoff, not a solved design problem. Bear should test whether the mismatch feels forgiving or confusing before deciding on a second change.

## B06 — A mistake still returns control

Into the spikes: failure, a brief error animation, one retry, then control returns at the start. We did not invent a new hazard system. The character's reaction is presentation, while the session still owns the reset. Watch the result before deciding whether that visual reaction explains enough.

## B07 — Falling is a separate failure route

Missing the gap still ends the attempt and starts another. This is not the same test as touching spikes. Both need checking after a visual change because a new silhouette can change what a landing appears to mean. The observed retry works; whether the failure reads clearly is still a human judgment.

## B08 — Keep the small forgiveness windows

Here the jump input arrives just after leaving a ledge, and the character still rises. This is the starter's coyote window, not a new Clawd power. The recording demonstrates this particular late jump. Boundary tests separately check the accepted and expired tick ages; one attractive replay does not prove every timing case.

## B09 — An early press can be remembered

Now Space arrives before landing, and the buffered request produces the next jump. The controller consumes that request once. This is different from holding a key forever. Keeping the original input behavior gives us a stable baseline while we inspect the new character. The art is the experiment; the jump rules are not.

## B10 — Pause is not another animation

Escape pauses the jump, Enter resumes, and R restarts. The capture also sends a labelled simulated focus-loss event, returns to the menu, and starts again. Pause freezes the animation clock as well as the player's motion. These scripted checks demonstrate the recorded controls, not an unstated human usability test.

## B11 — The mouse path still works

The menu's button also resumes and starts the game with mouse input. It is easy to check only the keyboard path you usually use. A small revision deserves a small but deliberate regression pass: does the rest of the existing interface still do what it did before?

## B12 — Finish this course, then replay

Clawd clears the original steps and gaps, reaches the same finish, and celebrates. Enter starts a fresh run. This recorded route completes without a death. It is not yet the proposed agentic-loop game: the flag is still the original flag. Keeping that distinction visible is part of explaining what we actually built.

## B13 — Start early; keep the honest trail

A first scene can appear quickly. Refinement is where the work continues. Make an improvement today; come back for another improvement or test in the next session. If an attempt does not work, record what you tried, observed, and learned in Frictional. Do not manufacture struggle or pretend these changes happened across several days. This iteration's entries are from one actual session.

## B14 — The larger idea stays on the roadmap

Bear's longer-term idea is a coding agent crossing mini-goals: a task completed, another task checked, and eventually a full agentic loop finished. Those are design notes, not features in today's build. The level extension is still required for Assignment One. Starting with Clawd's appearance lets Bear decide the next step from something he can actually play.

## B15 — Gallery 1: idle through run

Idle, bounce, wave, look, walk, and run. Watch the four legs alternate and the eyes scan. These are actual Godot gallery previews of the ported library. Bounce and wave are available artwork, not player commands in this level. The gallery lets us judge options before choosing more behavior.

## B16 — Gallery 2: thought and reaction

Think, type, sleep, error, nod, and shake. Their names suggest possible future coding-agent moments, but naming an animation does not implement a task system. Error currently reacts to failure; the others remain catalogue options. Choose a future state for a reason, then test whether the animation communicates it.

## B17 — Gallery 3: motion and celebration

Dance, stretch, crouch, jump, spin, and celebrate. Spin flips horizontally instead of rotating the pixel rectangles. The gallery jump is decorative; gameplay uses its held pose while physics moves the body. Celebrate is connected to the current finish. All eighteen are here to inspect, not a promise of eighteen powers.

## B18 — The verdict

The verdict: one recognizable character change, preserved mechanics, and a visible question about collision. The A I wrote and tested the implementation; Bear supplied the intent and chooses what deserves another iteration. Start early enough to inspect the result. A test that reveals a problem can move the project forward without making the feature complete.

## B19 — Your turn

Your turn. Please inspect Walker Jumpman Clawd. Propose one visual improvement and one test. Preserve the mechanics and log the result in Frictional. Before accepting the change, check that it answers a specific observation, leaves the existing controls intact, and names what the test does not establish. Then let a human play. Liam, in for Professor Bear.

## B20 — Regular outro

[Stock outro music only.]
