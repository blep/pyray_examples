"""raylib [core] example - window scale letterbox (and virtual mouse)
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 4.0
Example contributed by Anata (@anatagawa) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Anata (@anatagawa) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import random

# clamp is not directly in pyray, but Vector2Clamp is. We can use that or implement a simple clamp.
def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def main():
    window_width = 800
    window_height = 450

    rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE | rl.FLAG_VSYNC_HINT)
    rl.init_window(window_width, window_height, "raylib [core] example - window scale letterbox")
    rl.set_window_min_size(320, 240)

    game_screen_width = 640
    game_screen_height = 480

    target = rl.load_render_texture(game_screen_width, game_screen_height)
    rl.set_texture_filter(target.texture, rl.TEXTURE_FILTER_BILINEAR)

    colors = [rl.Color(random.randint(100, 250), random.randint(50, 150), random.randint(10, 100), 255) for _ in range(10)]

    rl.set_target_fps(60)

    while not rl.window_should_close():
        scale = min(float(rl.get_screen_width()) / game_screen_width, float(rl.get_screen_height()) / game_screen_height)

        if rl.is_key_pressed(rl.KEY_SPACE):
            colors = [rl.Color(random.randint(100, 250), random.randint(50, 150), random.randint(10, 100), 255) for _ in range(10)]

        mouse = rl.get_mouse_position()
        virtual_mouse = rl.Vector2(0, 0)
        virtual_mouse.x = (mouse.x - (rl.get_screen_width() - (game_screen_width * scale)) * 0.5) / scale
        virtual_mouse.y = (mouse.y - (rl.get_screen_height() - (game_screen_height * scale)) * 0.5) / scale
        virtual_mouse = rl.vector2_clamp(virtual_mouse, rl.Vector2(0, 0), rl.Vector2(float(game_screen_width), float(game_screen_height)))

        rl.begin_texture_mode(target)
        rl.clear_background(rl.RAYWHITE)
        for i in range(10):
            rl.draw_rectangle(0, (game_screen_height // 10) * i, game_screen_width, game_screen_height // 10, colors[i])
        rl.draw_text("If executed inside a window,\nyou can resize the window,\nand see the screen scaling!", 10, 25, 20, rl.WHITE)
        rl.draw_text(f"Default Mouse: [{int(mouse.x)}, {int(mouse.y)}]", 350, 25, 20, rl.GREEN)
        rl.draw_text(f"Virtual Mouse: [{int(virtual_mouse.x)}, {int(virtual_mouse.y)}]", 350, 55, 20, rl.YELLOW)
        rl.end_texture_mode()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_texture_pro(target.texture,
                            rl.Rectangle(0.0, 0.0, float(target.texture.width), -float(target.texture.height)),
                            rl.Rectangle((rl.get_screen_width() - (game_screen_width * scale)) * 0.5,
                                         (rl.get_screen_height() - (game_screen_height * scale)) * 0.5,
                                         game_screen_width * scale, game_screen_height * scale),
                            rl.Vector2(0, 0), 0.0, rl.WHITE)
        rl.end_drawing()

    rl.unload_render_texture(target)
    rl.close_window()

if __name__ == '__main__':
    main()
