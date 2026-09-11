# Building Clawd: One Change at a Time

## B00 — Professor Bear starts Assignment 1

Please use Walker to convert my game design document about a coding-agent platformer into one small revision: put Clawd in the existing level. Preserve the mechanics. I'm Liam, in for Professor Bear. His project is Walker Jumpman Clawd. The opening prompt is a suggested handoff, not a saved conversation.

## B01 — One character, the same level

We have changed the character, not completed the assignment. Clawd now moves through the existing First Steps level. The physics and layout remain the starter's. A separate gallery contains eighteen animations. Task mini-goals, new hazards, and the required level extension are later decisions. This is the first revision of a semester-long example.

## B02 — The loop is one inspectable change

Predict what might break. Build one change. Play it, inspect the evidence, revise, then record the version. Here the prediction is specific: Clawd's wide arms might make the unchanged collision box misleading. A small experiment gives us a question to answer. Changing the character, level, and physics together would make that answer harder to isolate.

## B03 — The same scene, a new presentation layer

The project still starts from main dot t s c n. The session constructs platforms, hazards, player, camera, and a separate interface layer. Clawd art is a drawing helper called by the player. There is no imported sprite sheet, AnimationPlayer node, or hidden agent service. The coding agent is the character's theme, not an autonomous player.

## B04 — Keep collision separate from the art

The rectangle shape is eighteen by twenty-eight, centered fourteen units above the player's origin. That places the reference at the feet. We preserved this code. Changing the picture does not change this collider, and testing the drawing alone cannot establish that the visual boundary feels fair.

## B05 — See the mismatch before fixing it

The blue outline is the collision reference; the orange arms extend beyond it. Both views are enlarged, staged Godot drawings, not gameplay. We have exposed the design question instead of quietly widening the collider. That would change which hazards and landings collide, so it deserves its own prediction and regression tests.

## B06 — Choose the pose from real state

This selector reads the session result, then grounded state and horizontal speed. Completion celebrates, failure uses error, air uses the jump pose, and speed chooses walk or run. These names do not add inputs. Run is an animation at the existing speed, not a new sprint button.

## B07 — The selected pose follows the movement

Watch Clawd start, move, brake, and stand still. The faster leg motion belongs to the existing velocity; it is not driving the body. The controller remains authoritative. The capture exercises both directions and opposing inputs. Judge the silhouette while it moves, not only when a character sheet looks tidy.

## B08 — Do not draw a second jump arc

The paint helper treats airborne rendering specially. It samples the library's apex pose, then removes the gallery's decorative vertical jump offset. The CharacterBody supplies the actual trajectory. Without that separation, the drawing could appear to hop independently of the collider, making a valid landing look wrong.

## B09 — Physics carries the visible jump

The character takes off and lands once. Holding the button does not cause another jump, and the midair press does not add a double jump. The new art stays attached to the body's trajectory. This is the visible consequence of separating display animation from the game's physical movement.

## B10 — Session state owns failure and success

This small read-only method translates the existing session state into presentation context. Complete, failed, and paused are descriptions for the drawing layer. The method does not change state, grant completion, or postpone a retry. Keeping ownership here prevents a missing or slow animation from deciding whether the game recovers.

## B11 — The error animation does not own retry

Clawd reaches the spike, reacts, and returns to the start on the existing timer. The brief error animation does not have to finish before the game can reset. This is a small example of a useful boundary: presentation describes the outcome; the session decides the outcome.

## B12 — Freeze the presentation clock on pause

The frame update returns immediately when the session says paused. Otherwise it chooses a pose, resets the animation clock on a pose change, advances time, and requests a redraw. None of those lines update velocity or collision. Pause therefore freezes the pose without replacing the original player physics function.

## B13 — Paused means the pose stops too

The jump and its pose hold during pause, then resume. The captured sequence also retries and returns to the menu, with focus loss explicitly simulated. Machine checks support these observations. A human still needs to judge whether the controls and feedback are understandable; a passing script is not that judgment.

## B14 — The level still comes from the same data

The solids, hazard, and finish coordinates are unchanged. The session builds their collision and drawing; its camera follows the player within the same bounds. The interface still displays the original progress and retry information. No task checkpoint was added just because the character now represents a coding agent.

## B15 — The old course still completes

Follow the unchanged route to the flag. The camera scrolls, the progress bar advances, and completion offers replay. Clawd celebrates, but this is the starter's finish condition. The future full-loop goal requires new state, reset rules, tests, and a design decision. Today we have evidence for this route only.

## B16 — Tests have different jobs

The original twenty-five mechanics checks and nine keyboard checks pass. A separate test compares a hundred sixty-two animation samples with Brutalist's TypeScript reference and checks presentation selection. These are machine checks, including staged fixtures. The recording driver uses normal input instead. Neither kind proves that Bear likes the character or that another player understands it.

## B17 — Start early; keep the honest trail

A first scene can appear quickly. Refinement is where the work continues. Make an improvement today; come back for another improvement or test in the next session. If an attempt does not work, record what you tried, observed, and learned in Frictional. Do not manufacture struggle or pretend these changes happened across several days. This iteration's entries are from one actual session.

## B18 — The larger idea stays on the roadmap

Bear's longer-term idea is a coding agent crossing mini-goals: a task completed, another task checked, and eventually a full agentic loop finished. Those are design notes, not features in today's build. The level extension is still required for Assignment One. Starting with Clawd's appearance lets Bear decide the next step from something he can actually play.

## B19 — One catalogue feeds a separate gallery

The gallery chooses six names for its current page and calls the same painting helper used by the player. This keeps the preview connected to the real implementation. The next three pages show all eighteen available animations. Only the smaller state-driven subset is connected to gameplay; a preview does not create an ability.

## B20 — Gallery 1: idle through run

Idle, bounce, wave, look, walk, and run. Watch the four legs alternate and the eyes scan. These are actual Godot gallery previews of the ported library. Bounce and wave are available artwork, not player commands in this level. The gallery lets us judge options before choosing more behavior.

## B21 — Gallery 2: thought and reaction

Think, type, sleep, error, nod, and shake. Their names suggest possible future coding-agent moments, but naming an animation does not implement a task system. Error currently reacts to failure; the others remain catalogue options. Choose a future state for a reason, then test whether the animation communicates it.

## B22 — Gallery 3: motion and celebration

Dance, stretch, crouch, jump, spin, and celebrate. Spin flips horizontally instead of rotating the pixel rectangles. The gallery jump is decorative; gameplay uses its held pose while physics moves the body. Celebrate is connected to the current finish. All eighteen are here to inspect, not a promise of eighteen powers.

## B23 — The verdict

The verdict: one recognizable character change, preserved mechanics, and a visible question about collision. The A I wrote and tested the implementation; Bear supplied the intent and chooses what deserves another iteration. Start early enough to inspect the result. A test that reveals a problem can move the project forward without making the feature complete.

## B24 — Your turn

Your turn. Please inspect Walker Jumpman Clawd. Propose one visual improvement and one test. Preserve the mechanics and log the result in Frictional. Before accepting the change, check that it answers a specific observation, leaves the existing controls intact, and names what the test does not establish. Then let a human play. Liam, in for Professor Bear.

## B25 — Regular outro

[Stock outro music only.]
