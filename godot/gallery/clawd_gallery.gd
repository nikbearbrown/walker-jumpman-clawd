extends Node2D
## Separate preview scene: all 18 library animations, NOT 18 gameplay abilities.
const Art = preload("res://features/player/clawd_art.gd")
var seconds: float = 0.0
var page: int = 0
var autoplay: bool = true
var show_collider: bool = false
var font: Font = ThemeDB.fallback_font

func _process(delta: float) -> void:
	seconds += delta
	if autoplay: page = int(seconds / 9.0) % 3
	queue_redraw()

func _unhandled_key_input(event: InputEvent) -> void:
	if not event.is_pressed() or event.is_echo(): return
	if event.keycode == KEY_SPACE: autoplay = not autoplay
	if event.keycode == KEY_RIGHT:
		autoplay = false
		page = (page + 1) % 3
	if event.keycode == KEY_LEFT:
		autoplay = false
		page = (page + 2) % 3
	if event.keycode == KEY_C: show_collider = not show_collider
	if event.keycode == KEY_ESCAPE: get_tree().quit()

func _draw() -> void:
	draw_rect(Rect2(0, 0, 640, 360), Color("faf9f5"))
	draw_string(font, Vector2(32, 32), "CLAWD / ANIMATION LIBRARY", HORIZONTAL_ALIGNMENT_LEFT, -1, 19, Color("3d3929"))
	draw_string(font, Vector2(32, 53), "Gallery %d/3: display previews, not additional game mechanics" % (page + 1), HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color("3d3929"))
	for i in range(6):
		var x := 122.0 + (i % 3) * 196
		var y := 153.0 + (i / 3) * 125
		var animation: String = Art.ANIMATIONS[page * 6 + i]
		draw_line(Vector2(x - 60, y + 2), Vector2(x + 60, y + 2), Color("ddd8d0"))
		Art.paint(self, animation, fmod(seconds, 9.0), Vector2(x, y), 0.55)
		draw_string(font, Vector2(x - 70, y + 23), animation, HORIZONTAL_ALIGNMENT_CENTER, 140, 15, Color("3d3929"))
		if show_collider:
			# Same reference shape at the gallery scale; the game uses scale 0.32.
			var ratio := 0.55 / 0.32
			draw_rect(Rect2(Vector2(x, y) + Vector2(-9, -28) * ratio, Vector2(18, 28) * ratio), Color("287baf"), false, 1)
	draw_string(font, Vector2(32, 333), "Arrows: page   Space: auto/manual   C: collision reference   Esc: close", HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color("3d3929"))
