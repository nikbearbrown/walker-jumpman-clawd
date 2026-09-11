extends RefCounted
## Clawd's 18 code-driven animations, adapted from Brutalist's ClaudeMascotScene.
## Drawing only: never writes a body's position, velocity, input, or collision shape.
const ANIMATIONS := ["idle", "bounce", "wave", "look", "walk", "run", "think", "type", "sleep", "error", "nod", "shake", "dance", "stretch", "crouch", "jump", "spin", "celebrate"]
const BODY := Color("dd775b")
const EYE := Color.BLACK

static func sample(animation: String, seconds: float) -> Dictionary:
	assert(animation in ANIMATIONS, "Unknown Clawd animation")
	var t := seconds * TAU
	var frame := seconds * 30.0 # Original library's 30-fps blink clock.
	var s := {"x": 0.0, "y": 0.0, "sx": 1.0, "sy": 1.0, "left_arm": 0.0, "right_arm": 0.0, "eye_x": 0.0, "eye_h": 10.0, "legs": [0.0, 0.0, 0.0, 0.0]}
	match animation:
		"idle":
			s.y = sin(t * 1.2) * 2
			var phase := fmod(frame, 80.0)
			if phase < 4: s.eye_h = absf(phase - 2.0) * 5.0
		"bounce":
			var arc := absf(sin(t * 3))
			s.sy = 1 - (1 - arc) * 0.15
			s.sx = 1 + (1 - arc) * 0.10
			s.y = 86 * (1 - s.sy) - arc * 28
			s.x = 48 * (1 - s.sx)
		"wave":
			s.right_arm = sin(t * 3) * -12
			s.y = sin(t * 1.5) * 2
		"look":
			s.eye_x = sin(t * 1.8) * 8
			s.y = sin(t * 0.8) * 2
		"walk", "run":
			var fast := animation == "run"
			var phase := sin(t * (6 if fast else 4))
			var lift := 14 if fast else 8
			s.legs = [-maxf(0, phase) * lift, -maxf(0, -phase) * lift, -maxf(0, phase) * lift, -maxf(0, -phase) * lift]
			s.x = phase * (6 if fast else 3)
			s.y = -absf(sin(t * (12 if fast else 8))) * (4 if fast else 2)
		"think":
			s.eye_x = sin(t * 1.5) * 6
			s.left_arm = sin(t * 1.5) * -10
			s.y = sin(t * 0.8) * 2
		"type":
			s.left_arm = 8.0
			s.right_arm = 8.0
			s.y = sin(t * 12) * 1.5
		"sleep":
			s.eye_h = lerpf(10, 2, clampf(seconds, 0, 1))
			s.y = sin(t * 0.6) * 3
		"error": s.x = sin(t * 15) * 10
		"nod":
			s.sy = 1 - absf(sin(t * 3)) * 0.12
			s.y = 86 * (1 - s.sy)
		"shake": s.x = sin(t * 8) * 12
		"dance":
			var arc := absf(sin(t * 4))
			s.sy = 1 - (1 - arc) * 0.08
			s.y = 86 * (1 - s.sy) - arc * 15
			s.left_arm = sin(t * 3) * -12
			s.right_arm = sin(t * 3 + PI) * -12
			s.x = sin(t * 2) * 8
		"stretch":
			s.sy = sin(t * 1.5) * 0.25 + 1
			s.y = 86 * (1 - s.sy)
		"crouch":
			s.sy = 1 - (sin(t * 2) + 1) / 2 * 0.25
			s.y = 86 * (1 - s.sy)
		"jump":
			var arc := maxf(0, sin(t * 2.5))
			s.sy = 1 - (1 - arc) * 0.15
			s.sx = 1 + (1 - arc) * 0.08
			s.y = 86 * (1 - s.sy) - arc * 35
			s.x = 48 * (1 - s.sx)
		"spin":
			s.sx = cos(t * 1.5)
			s.x = 48 * (1 - s.sx)
		"celebrate":
			var arc := maxf(0, sin(t * 2.5))
			s.sy = 1 - (1 - arc) * 0.12
			s.y = 86 * (1 - s.sy) - arc * 35
			s.left_arm = -arc * 20 - 10
			s.right_arm = -arc * 20 - 10
			s.x = sin(t * 4) * 10
	return s

static func paint(canvas: CanvasItem, animation: String, seconds: float, feet: Vector2, size: float = 0.32, facing: float = 1.0, airborne: bool = false) -> void:
	# Airborne physics owns the jump arc. Hold the library's apex pose; do not
	# add its display-only jump offset to the moving CharacterBody2D.
	var s := sample("jump" if airborne else animation, 0.1 if airborne else seconds)
	if airborne: s.y = 86 * (1 - s.sy)
	var rectangles := [Rect2(0, 0, 96, 60), Rect2(-20, 20 + s.left_arm, 20, 20), Rect2(96, 20 + s.right_arm, 20, 20)]
	for i in range(4): rectangles.append(Rect2([11, 32, 64, 85][i], 60 + s.legs[i], 11, 26))
	rectangles.append(Rect2(11 + s.eye_x, 10, 11, s.eye_h))
	rectangles.append(Rect2(74 + s.eye_x, 10, 11, s.eye_h))
	# Transform corners, then normalize: horizontal flips never need rotation.
	for i in range(rectangles.size()):
		var r: Rect2 = rectangles[i]
		var a := feet + Vector2((s.x + r.position.x * s.sx - 48) * facing, s.y + r.position.y * s.sy - 86) * size
		var b := feet + Vector2((s.x + r.end.x * s.sx - 48) * facing, s.y + r.end.y * s.sy - 86) * size
		canvas.draw_rect(Rect2(a, b - a).abs(), EYE if i >= 7 else BODY)
