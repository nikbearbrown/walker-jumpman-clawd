extends SceneTree
## Actual engine capture with input-only traversal. No game state writes.
var game: Node2D
var stage: SubViewport
var preview: TextureRect
var output: String
var take: String = "pilot"
var frame: int = 0
var written: int = 0
var log_file: FileAccess
var states: FileAccess
var flags: Array[String] = []

func _initialize() -> void:
	call_deferred("run")

func fail(message: String) -> void:
	push_error(message)
	if log_file: log_file.flush()
	if states: states.flush()
	quit(1)

func check(ok: bool, message: String) -> void:
	if not ok:
		fail(message)
		assert(ok, message)

func record(kind: String, detail: String) -> void:
	log_file.store_line(JSON.stringify({"frame60": frame, "time_s": float(frame)/60.0, "kind": kind, "detail": detail}))

func mark(label: String) -> void:
	flags.append(label)
	record("marker", label)
	print("CAPTURE %s %.3fs %s" % [take, float(frame)/60.0, label])

func step(count: int = 1) -> void:
	for i in range(count):
		await process_frame

func capture_frame() -> void:
	states.store_line(JSON.stringify({"frame60":frame,"state":game.state,"x":game.player.position.x,"y":game.player.position.y,"vx":game.player.velocity.x,"vy":game.player.velocity.y,"grounded":game.player.is_on_floor(),"jumps":game.player.jumps,"retries":game.deaths,"elapsed":game.elapsed,"camera_x":game.camera.position.x,"player_tick":game.player.tick,"animation":game.player.animation_name,"animation_seconds":game.player.animation_seconds}))
	if frame % 2 == 0:
		var img := stage.get_texture().get_image()
		check(img.get_size() == Vector2i(3840,2160), "Not native 4K viewport")
		check(img.save_png(output + "/frames/" + take + "/%06d.png" % written) == OK, "PNG save failed")
		written += 1
	frame += 1

func key(code: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)
	stage.push_input(event)
	record("key_down" if pressed else "key_up", OS.get_keycode_string(code))
	await step(2)

func tap(code: Key) -> void:
	await key(code, true)
	await key(code, false)

func click_button() -> void:
	var motion := InputEventMouseMotion.new()
	motion.position = Vector2(320,230)
	stage.push_input(motion, true)
	await step(3)
	for down in [true,false]:
		var event := InputEventMouseButton.new()
		event.position = Vector2(320,230)
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = down
		stage.push_input(event, true)
		record("mouse_down" if down else "mouse_up", "button at logical 320,230")
		await step(3)

func to_x(target: float, max_steps: int = 600) -> void:
	await key(KEY_D, true)
	for i in range(max_steps):
		if game.player.position.x >= target: return
		await step()
	fail("Route failed to reach x=" + str(target))

func route(until_x: float = 914.0) -> void:
	var marks := [138.0,292.0,424.0,548.0,712.0]
	var next_jump := 0
	await key(KEY_D,true)
	for i in range(1000):
		if game.state == game.State.COMPLETE:
			await key(KEY_D,false)
			return
		if game.player.position.x >= until_x:
			await key(KEY_D,false)
			return
		check(game.state == game.State.PLAYING, "Unexpected route state")
		if next_jump < marks.size() and game.player.position.x >= marks[next_jump] and game.player.is_on_floor():
			await tap(KEY_SPACE)
			next_jump += 1
		else:
			await step()
	fail("Route timed out")

func run() -> void:
	var args := OS.get_cmdline_user_args()
	check(args.size() == 2, "Need output and take")
	output = args[0]
	check(output.is_absolute_path(), "Capture output must be absolute")
	take = args[1]
	DirAccess.make_dir_recursive_absolute(output + "/frames/" + take)
	log_file = FileAccess.open(output + "/" + take + "-inputs.jsonl", FileAccess.WRITE)
	states = FileAccess.open(output + "/" + take + "-states.jsonl", FileAccess.WRITE)
	stage = SubViewport.new()
	stage.size = Vector2i(3840,2160)
	stage.size_2d_override = Vector2i(640,360)
	stage.size_2d_override_stretch = true
	stage.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	stage.handle_input_locally = true
	root.add_child(stage)
	preview = TextureRect.new()
	preview.texture = stage.get_texture()
	preview.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	root.add_child(preview)
	game = load("res://game/main.tscn").instantiate()
	stage.add_child(game)
	RenderingServer.frame_post_draw.connect(capture_frame)
	await step(60)
	mark("menu")
	if take == "pilot":
		await tap(KEY_ENTER)
		await step(60)
	else:
		await tap(KEY_ENTER)
		check(game.state == game.State.PLAYING,"Enter did not start game")
		mark("start")
		await step(30)
		match take:
			"mouse":
				await tap(KEY_ESCAPE)
				await step(30)
				await click_button()
				check(game.state==game.State.PLAYING,"Mouse resume failed")
				mark("mouse-resume")
				await step(30)
				await tap(KEY_P)
				await tap(KEY_M)
				await step(30)
				await click_button()
				check(game.state==game.State.PLAYING,"Mouse start failed")
				mark("mouse-start")
			"controls":
				await key(KEY_A,true)
				await step(45)
				await key(KEY_A,false)
				mark("left-boundary")
				check(game.player.position.x <= 11,"Boundary not reached")
				await step(30)
				await key(KEY_RIGHT,true)
				await step(29)
				await key(KEY_RIGHT,false)
				await step(25)
				mark("accelerate-stop")
				await key(KEY_A,true)
				await key(KEY_D,true)
				await step(25)
				mark("opposing-inputs")
				await key(KEY_A,false)
				await key(KEY_D,false)
				await step(25)
			"jump":
				await key(KEY_SPACE,true)
				mark("jump-held")
				await step(85)
				check(game.player.jumps==1,"Held key bounced")
				mark("landed-no-bounce")
				await key(KEY_SPACE,false)
				await step(30)
				await tap(KEY_SPACE)
				await step(7)
				await tap(KEY_SPACE)
				mark("air-press-no-double")
				await step(65)
				check(game.player.jumps==2,"Unexpected double jump")
			"spike":
				await to_x(138)
				await tap(KEY_SPACE)
				for i in range(180):
					await step()
					if game.state==game.State.DYING: break
				check(game.state==game.State.DYING,"Did not hit spike")
				mark("spike-contact")
				await key(KEY_D,false)
				await step(45)
				check(game.state==game.State.PLAYING and game.deaths==1,"Retry failed")
				mark("automatic-retry")
			"fall":
				await to_x(138)
				await tap(KEY_SPACE)
				await to_x(292)
				await tap(KEY_SPACE)
				for i in range(200):
					await step()
					if game.state==game.State.DYING: break
				check(game.state==game.State.DYING,"Did not fall")
				mark("fall-contact")
				await key(KEY_D,false)
				await step(45)
				mark("fall-retry")
			"pause":
				await tap(KEY_SPACE)
				await step(10)
				await tap(KEY_ESCAPE)
				check(game.state==game.State.PAUSED,"Pause failed")
				mark("pause-mid-jump")
				await step(90)
				await tap(KEY_ENTER)
				mark("resume")
				await step(65)
				await key(KEY_D,true)
				await step(15)
				await key(KEY_D,false)
				await tap(KEY_R)
				mark("manual-retry")
				await step(40)
				# Deliver the normal Window event; explicit simulation, not human focus evidence.
				root.focus_exited.emit()
				mark("simulated-focus-loss")
				check(game.state==game.State.PAUSED,"Focus safety failed")
				await step(75)
				await tap(KEY_M)
				mark("main-menu")
				await step(45)
				await tap(KEY_ENTER)
				mark("menu-restart")
			"coyote":
				await to_x(138)
				await tap(KEY_SPACE)
				await to_x(292)
				await tap(KEY_SPACE)
				await to_x(449)
				for i in range(40):
					await step()
					if not game.player.is_on_floor(): break
				check(not game.player.is_on_floor(),"No ledge departure")
				mark("left-edge")
				await step(2)
				await tap(KEY_SPACE)
				mark("late-jump")
				check(game.player.velocity.y<0,"Coyote jump failed")
				await step(25)
				await key(KEY_D,false)
				await step(45)
				check(game.deaths==0,"Coyote landing failed")
				mark("coyote-landed")
			"buffer":
				await tap(KEY_SPACE)
				for i in range(70):
					await step()
					if game.player.velocity.y>150 and game.player.position.y>306: break
				check(not game.player.is_on_floor(),"Buffer input too late")
				mark("early-input-before-landing")
				await tap(KEY_SPACE)
				await step(15)
				check(game.player.jumps==2,"Buffered jump failed")
				mark("buffered-jump")
				await step(70)
			"finish":
				mark("route-begins")
				await route()
				check(game.state==game.State.COMPLETE and game.deaths==0,"Route not complete")
				mark("complete")
				await step(90)
				await tap(KEY_ENTER)
				mark("replay")
				check(game.state==game.State.PLAYING and game.deaths==0,"Replay failed")
			_: fail("Unknown take")
	await step(90)
	mark("end")
	RenderingServer.frame_post_draw.disconnect(capture_frame)
	var receipt := {"take":take,"frames":written,"fps":30,"width":3840,"height":2160,"engine":Engine.get_version_info().string,"game_source":"unmodified main.tscn and dependencies","input_method":"synthetic InputEventKey through Input plus SubViewport delivery","simulation_fps":60,"test_mode":game.test_mode,"test_control":game.player.test_control,"markers":flags,"status":"PASS"}
	FileAccess.open(output+"/"+take+"-receipt.json",FileAccess.WRITE).store_string(JSON.stringify(receipt,"  "))
	log_file.close()
	states.close()
	print(JSON.stringify(receipt))
	quit()
