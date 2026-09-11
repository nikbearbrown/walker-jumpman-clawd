extends SceneTree
## Staged native-engine gallery/inspector, explicitly NOT a gameplay route.
var stage: SubViewport
var scene: Node2D
var output: String
var take: String
var frame := 0
var written := 0
var states: FileAccess
var inputs: FileAccess
func _initialize() -> void: call_deferred("run")
func capture() -> void:
	states.store_line(JSON.stringify({"frame60":frame,"page":scene.page if take.begins_with("gallery-") else -1,"kind":"staged animation preview"}))
	if frame % 2 == 0:
		var image := stage.get_texture().get_image()
		assert(image.get_size() == Vector2i(3840,2160))
		assert(image.save_png(output + "/frames/" + take + "/%06d.png" % written) == OK)
		written += 1
	frame += 1
	# Diagnostic preview only: advance its display clock exactly once per rendered
	# frame. Background-window process throttling must not speed up the movie.
	scene.seconds = float(frame) / 60.0
	scene.queue_redraw()
func tap(code: Key) -> void:
	for down in [true, false]:
		var e := InputEventKey.new()
		e.keycode = code
		e.physical_keycode = code
		e.pressed = down
		stage.push_input(e)
		inputs.store_line(JSON.stringify({"key":OS.get_keycode_string(code),"pressed":down,"kind":"gallery input"}))
		await process_frame
func run() -> void:
	var args := OS.get_cmdline_user_args()
	output = args[0]
	take = args[1]
	DirAccess.make_dir_recursive_absolute(output + "/frames/" + take)
	states = FileAccess.open(output + "/" + take + "-states.jsonl", FileAccess.WRITE)
	inputs = FileAccess.open(output + "/" + take + "-inputs.jsonl", FileAccess.WRITE)
	stage = SubViewport.new()
	stage.size = Vector2i(3840,2160)
	stage.size_2d_override = Vector2i(640,360)
	stage.size_2d_override_stretch = true
	stage.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(stage)
	var preview := TextureRect.new()
	preview.texture = stage.get_texture()
	preview.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	root.add_child(preview)
	if take.begins_with("gallery-"):
		scene = load("res://gallery/clawd_gallery.tscn").instantiate()
		stage.add_child(scene)
		await process_frame
		await tap(KEY_SPACE)
		for i in range({"gallery-one":0,"gallery-two":1,"gallery-three":2}[take.trim_suffix("-v2")]): await tap(KEY_RIGHT)
		assert(not scene.autoplay)
	else:
		scene = Inspector.new()
		stage.add_child(scene)
	scene.set_process(false)
	scene.seconds = 0.0
	scene.queue_redraw()
	RenderingServer.frame_post_draw.connect(capture)
	while written < 600: await process_frame
	RenderingServer.frame_post_draw.disconnect(capture)
	states.close()
	inputs.close()
	assert(written == 600, "Expected complete 20-second preview")
	var receipt := {"take":take,"frames":written,"fps":30,"width":3840,"height":2160,"engine":Engine.get_version_info().string,"status":"PASS","test_mode":false,"test_control":false,"method":"staged native Godot animation gallery; deterministic render-driven clock, not gameplay","page":scene.page if take.begins_with("gallery-") else -1}
	FileAccess.open(output+"/"+take+"-receipt.json",FileAccess.WRITE).store_string(JSON.stringify(receipt,"  "))
	print(JSON.stringify(receipt))
	quit()

class Inspector extends Node2D:
	const Art = preload("res://features/player/clawd_art.gd")
	var seconds := 0.0
	func _process(delta: float) -> void:
		seconds += delta
		queue_redraw()
	func _draw() -> void:
		var font: Font = ThemeDB.fallback_font
		draw_rect(Rect2(0,0,640,360),Color("faf9f5"))
		draw_string(font,Vector2(32,36),"CLAWD / ART AND COLLISION",HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color("3d3929"))
		draw_string(font,Vector2(32,61),"Staged Godot draw · the orange body is not the physics boundary",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("3d3929"))
		for i in range(2):
			var feet := Vector2(180 + i * 280,255)
			Art.paint(self,"walk",seconds,feet,1.3,1 if i == 0 else -1)
			var scale_factor := 1.3 / 0.32
			draw_rect(Rect2(feet + Vector2(-9,-28) * scale_factor,Vector2(18,28) * scale_factor),Color("287baf"),false,2)
			draw_string(font,Vector2(feet.x-65,292),"Right-facing" if i == 0 else "Left-facing",HORIZONTAL_ALIGNMENT_CENTER,130,15,Color("3d3929"))
		draw_string(font,Vector2(32,332),"Blue: unchanged 18 × 28 collider · feet at origin · enlarged for inspection",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("3d3929"))
