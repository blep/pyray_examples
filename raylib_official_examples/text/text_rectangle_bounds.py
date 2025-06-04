"""raylib [text] example - Rectangle bounds
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 2.5, last time updated with raylib 4.0
Example contributed by Vlad Adrian (@demizdor) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2018-2025 Vlad Adrian (@demizdor) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

# Implement draw_text_boxed to render text within a rectangle
def draw_text_boxed(font, text, rec, font_size, spacing, word_wrap, tint):
    draw_text_boxed_selectable(font, text, rec, font_size, spacing, word_wrap, tint, 0, 0, rl.WHITE, rl.WHITE)

# Implement draw_text_boxed_selectable to support text selection
def draw_text_boxed_selectable(font, text, rec, font_size, spacing, word_wrap, tint, select_start, select_length, select_tint, select_back_tint):
    scale_factor = font_size / font.baseSize

    text_offset_x = 0.0
    text_offset_y = 0.0

    for i, char in enumerate(text):
        if char == '\n':
            text_offset_x = 0.0
            text_offset_y += font_size + spacing
            continue

        glyph_index = rl.get_glyph_index(font, ord(char))
        glyph = font.glyphs[glyph_index]

        glyph_width = glyph.advanceX * scale_factor

        if word_wrap and (text_offset_x + glyph_width > rec.width):
            text_offset_x = 0.0
            text_offset_y += font_size + spacing

        if text_offset_y + font_size > rec.height:
            break

        position = rl.Vector2(rec.x + text_offset_x, rec.y + text_offset_y)

        rl.draw_text_ex(font, char, position, font_size, spacing, tint)

        text_offset_x += glyph_width

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - draw text inside a rectangle")

    text = ("Text cannot escape\tthis container\t...word wrap also works when active so here's "
           "a long text for testing.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
           "tempor incididunt ut labore et dolore magna aliqua. Nec ullamcorper sit amet risus nullam eget felis eget.")

    resizing = False
    word_wrap = True

    container = rl.Rectangle(25.0, 25.0, screen_width - 50.0, screen_height - 250.0)
    resizer = rl.Rectangle(container.x + container.width - 17, container.y + container.height - 17, 14, 14)

    # Minimum width and height for the container rectangle
    min_width = 60
    min_height = 60
    max_width = screen_width - 50.0
    max_height = screen_height - 160.0

    last_mouse = rl.Vector2(0.0, 0.0)  # Stores last mouse coordinates
    border_color = rl.MAROON         # Container border color
    font = rl.get_font_default()       # Get default system font

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        if rl.is_key_pressed(rl.KEY_SPACE):
            word_wrap = not word_wrap

        mouse = rl.get_mouse_position()

        # Check if the mouse is inside the container and toggle border color
        if rl.check_collision_point_rec(mouse, container):
            border_color = rl.fade(rl.MAROON, 0.4)
        elif not resizing:
            border_color = rl.MAROON

        # Container resizing logic
        if resizing:
            if rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT):
                resizing = False

            width = container.width + (mouse.x - last_mouse.x)
            container.width = width if width > min_width and width < max_width else (min_width if width <= min_width else max_width)

            height = container.height + (mouse.y - last_mouse.y)
            container.height = height if height > min_height and height < max_height else (min_height if height <= min_height else max_height)
        else:
            # Check if we're resizing
            if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT) and rl.check_collision_point_rec(mouse, resizer):
                resizing = True

        # Move resizer rectangle properly
        resizer.x = container.x + container.width - 17
        resizer.y = container.y + container.height - 17

        last_mouse = mouse  # Update mouse

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_rectangle_lines_ex(container, 3, border_color)  # Draw container border

        # Draw text in container (add some padding)
        draw_text_boxed(
            font, text, 
            rl.Rectangle(container.x + 4, container.y + 4, container.width - 4, container.height - 4),
            20.0, 2.0, word_wrap, rl.GRAY
        )

        rl.draw_rectangle_rec(resizer, border_color)  # Draw the resize box

        # Draw bottom info
        rl.draw_rectangle(0, screen_height - 54, screen_width, 54, rl.GRAY)
        rl.draw_rectangle_rec(rl.Rectangle(382.0, screen_height - 34.0, 12.0, 12.0), rl.MAROON)

        rl.draw_text("Word Wrap: ", 313, screen_height-115, 20, rl.BLACK)
        if word_wrap:
            rl.draw_text("ON", 447, screen_height - 115, 20, rl.RED)
        else:
            rl.draw_text("OFF", 447, screen_height - 115, 20, rl.BLACK)

        rl.draw_text("Press [SPACE] to toggle word wrap", 218, screen_height - 86, 20, rl.GRAY)
        rl.draw_text("Click hold & drag the    to resize the container", 155, screen_height - 38, 20, rl.RAYWHITE)

        rl.end_drawing()

    # De-Initialization
    rl.close_window()  # Close window and OpenGL context

if __name__ == "__main__":
    main()