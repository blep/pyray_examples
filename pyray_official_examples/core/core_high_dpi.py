"""raylib [core] example - HighDPI
Example complexity rating: [★☆☆☆] e/4
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2013-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def draw_text_center(text: str, x: int, y: int, font_size: int, color: rl.Color):
    size = rl.measure_text_ex(rl.get_font_default(), text, float(font_size), 3)
    pos = rl.Vector2(x - size.x / 2, y - size.y / 2)
    rl.draw_text_ex(rl.get_font_default(), text, pos, float(font_size), 3, color)

def main():
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_WINDOW_HIGHDPI | rl.FLAG_WINDOW_RESIZABLE)

    rl.init_window(screen_width, screen_height, "raylib [core] example - highdpi")
    rl.set_window_min_size(450, 450)

    rl.set_target_fps(60)

    while not rl.window_should_close():
        monitor_count = rl.get_monitor_count()
        if monitor_count > 1 and rl.is_key_pressed(rl.KEY_N):
            rl.set_window_monitor((rl.get_current_monitor() + 1) % monitor_count)
        
        current_monitor = rl.get_current_monitor()

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        dpi_scale = rl.get_window_scale_dpi()
        window_center = rl.get_screen_width() // 2

        draw_text_center(f"Dpi Scale: {dpi_scale.x:.2f}", window_center, 30, 40, rl.DARKGRAY)
        draw_text_center(f"Monitor: {current_monitor + 1}/{monitor_count} ([N] next monitor)", window_center, 70, 16, rl.LIGHTGRAY)

        logical_grid_desc_y = 120
        logical_grid_label_y = logical_grid_desc_y + 30
        logical_grid_top = logical_grid_label_y + 30
        logical_grid_bottom = logical_grid_top + 80
        pixel_grid_top = logical_grid_bottom - 20
        pixel_grid_bottom = pixel_grid_top + 80
        pixel_grid_label_y = pixel_grid_bottom + 30
        pixel_grid_desc_y = pixel_grid_label_y + 30

        cell_size = 50
        cell_size_px = float(cell_size) / dpi_scale.x

        draw_text_center(f'Window is {rl.get_screen_width()} "logical points" wide', window_center, logical_grid_desc_y, 20, rl.ORANGE)
        odd = True
        i = cell_size
        while i < rl.get_screen_width():
            if odd:
                rl.draw_rectangle(i, logical_grid_top, cell_size, logical_grid_bottom - logical_grid_top, rl.ORANGE)
            draw_text_center(f"{i}", i, logical_grid_label_y, 12, rl.LIGHTGRAY)
            rl.draw_line(i, logical_grid_label_y + 10, i, logical_grid_bottom, rl.GRAY)
            i += cell_size
            odd = not odd

        odd = True
        min_text_space = 30
        last_text_x = -min_text_space
        i = cell_size
        while i < rl.get_render_width():
            x = int(float(i) / dpi_scale.x)
            if odd:
                rl.draw_rectangle(x, pixel_grid_top, int(cell_size_px), pixel_grid_bottom - pixel_grid_top, rl.Color(0, 121, 241, 100))
            rl.draw_line(x, pixel_grid_top, int(float(i) / dpi_scale.x), pixel_grid_label_y - 10, rl.GRAY)
            if x - last_text_x >= min_text_space:
                draw_text_center(f"{i}", x, pixel_grid_label_y, 12, rl.LIGHTGRAY)
                last_text_x = x
            i += cell_size
            odd = not odd
        
        draw_text_center(f'Window is {rl.get_render_width()} "physical pixels" wide', window_center, pixel_grid_desc_y, 20, rl.BLUE)

        text = "Can you see this?"
        size = rl.measure_text_ex(rl.get_font_default(), text, 16, 3)
        pos = rl.Vector2(rl.get_screen_width() - size.x - 5, rl.get_screen_height() - size.y - 5)
        rl.draw_text_ex(rl.get_font_default(), text, pos, 16, 3, rl.LIGHTGRAY)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
