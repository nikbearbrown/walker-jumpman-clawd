extends SceneTree
const Art = preload("res://features/player/clawd_art.gd")
const Game = preload("res://game/session.gd")
var failures := 0
var checks := 0
func check(passed: bool, label: String) -> void:
	checks += 1
	if not passed:
		failures += 1
		push_error(label)
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var reference = JSON.parse_string(FileAccess.get_file_as_string("res://tests/clawd-reference.json"))
	for row in reference.rows:
		var actual := Art.sample(row.name, row.seconds)
		for key in row.expected:
			if key == "legs":
				for i in range(4): check(absf(actual.legs[i] - row.expected.legs[i]) < 0.00001, row.name + " leg " + str(i))
			else: check(absf(actual[key] - row.expected[key]) < 0.00001, row.name + " " + key)
	var game := Game.new()
	game.test_mode = true
	root.add_child(game)
	await process_frame
	game.start_session()
	for i in range(4):
		await physics_frame
		await process_frame
	check(game.player.visual_animation() == "idle", "Stationary grounded idle")
	game.player.velocity.x = 30
	check(game.player.visual_animation() == "walk", "Low speed walk")
	game.player.velocity.x = 160
	check(game.player.visual_animation() == "run", "High speed run")
	game.resolve_contacts(false, true)
	check(game.player.visual_animation() == "celebrate", "Finish celebration")
	game.restart_attempt()
	game.resolve_contacts(true, false)
	check(game.player.visual_animation() == "error", "Failure presentation")
	game.restart_attempt()
	game.set_paused(true)
	var old_seconds: float = game.player.animation_seconds
	for i in range(10): await process_frame
	check(game.player.animation_seconds == old_seconds, "Pause freezes presentation")
	var report := {"checks": checks, "failures": failures, "animation_samples": reference.rows.size(), "reference_sha256": reference.source_sha256, "scope": "Numeric animation parity and staged presentation checks, not human playtesting"}
	var dest := ProjectSettings.globalize_path("res://../evidence/clawd")
	DirAccess.make_dir_recursive_absolute(dest)
	FileAccess.open(dest + "/animation-" + str(Time.get_unix_time_from_system()) + ".json", FileAccess.WRITE).store_string(JSON.stringify(report, "  "))
	print(JSON.stringify(report))
	game.queue_free()
	await process_frame
	quit(1 if failures else 0)
