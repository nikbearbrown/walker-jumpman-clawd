extends CharacterBody2D

const Tuning = preload("res://features/player/tuning.gd")
const ClawdArt = preload("res://features/player/clawd_art.gd")
var animation_seconds: float = 0.0
var animation_name: String = "idle"
var tuning = Tuning.new()
var enabled: bool = false
var tick: int = 0
var last_floor_tick: int = -1000
var jump_request_tick: int = -1000
var opportunity_consumed: bool = false
var require_jump_release: bool = true
var facing: float = 1.0
var jumps: int = 0
var test_control: bool = false
var test_axis: float = 0.0
var test_jump_pressed: bool = false
var test_jump_held: bool = false

func _ready() -> void:
	name = "Player"
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = 1.0
	var shape := RectangleShape2D.new()
	shape.size = Vector2(18, 28)
	var collider := CollisionShape2D.new()
	collider.shape = shape
	collider.position = Vector2(0, -14)
	add_child(collider)

func reset_at(spawn: Vector2) -> void:
	position = spawn
	velocity = Vector2.ZERO
	last_floor_tick = -1000
	jump_request_tick = -1000
	opportunity_consumed = false
	require_jump_release = true
	test_jump_pressed = false
	jumps = 0
	queue_redraw()

func _physics_process(delta: float) -> void:
	if not enabled:
		return
	tick += 1
	var axis := test_axis if test_control else Input.get_axis("move_left", "move_right")
	var held := test_jump_held if test_control else Input.is_action_pressed("jump")
	var pressed := test_jump_pressed if test_control else Input.is_action_just_pressed("jump")
	test_jump_pressed = false
	if not held:
		require_jump_release = false
	if is_on_floor() and velocity.y >= 0.0:
		last_floor_tick = tick
		opportunity_consumed = false
	if pressed and not require_jump_release:
		jump_request_tick = tick
	var rate: float = tuning.acceleration if not is_zero_approx(axis) else tuning.deceleration
	velocity.x = move_toward(velocity.x, axis * tuning.speed, rate * delta)
	if not is_zero_approx(axis):
		facing = signf(axis)
	velocity.y = minf(velocity.y + tuning.gravity * delta, tuning.terminal_velocity)
	if not opportunity_consumed and tick - last_floor_tick <= tuning.coyote_ticks and tick - jump_request_tick <= tuning.buffer_ticks:
		velocity.y = tuning.jump_velocity
		opportunity_consumed = true
		jump_request_tick = -1000
		jumps += 1
	move_and_slide()
	position.x = maxf(position.x, 10.0)
	queue_redraw()

func visual_animation() -> String:
	var context: String = get_parent().player_animation_context()
	if context == "complete": return "celebrate"
	if context == "failed": return "error"
	if not enabled: return "idle"
	if not is_on_floor(): return "jump"
	if absf(velocity.x) >= 100: return "run"
	if absf(velocity.x) > 8: return "walk"
	return "idle"

func _process(delta: float) -> void:
	if get_parent().player_animation_context() == "paused": return
	var next_animation := visual_animation()
	if next_animation != animation_name:
		animation_seconds = 0.0
		animation_name = next_animation
	animation_seconds += delta
	queue_redraw()

func _draw() -> void:
	ClawdArt.paint(self, animation_name, animation_seconds, Vector2.ZERO, 0.32, facing, animation_name == "jump")
