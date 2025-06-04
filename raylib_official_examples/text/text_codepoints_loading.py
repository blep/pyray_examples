"""raylib [text] example - Codepoints loading
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 4.2, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2022-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Text to be displayed, must be UTF-8
# NOTE: It can contain all the required text for the game,
# this text will be scanned to get all the required codepoints
text = "いろはにほへと　ちりぬるを\nわかよたれそ　つねならむ\nうゐのおくやま　けふこえて\nあさきゆめみし　ゑひもせす"

# Remove codepoint duplicates if requested
def codepoint_remove_duplicates(codepoints, codepoint_count):
    """
    Remove codepoint duplicates
    WARNING: This process could be a bit slow if the text to process is very long
    """
    codepoints_no_dups = list(codepoints)
    
    # Remove duplicates (using Python's set capabilities)
    codepoints_no_dups = list(dict.fromkeys(codepoints_no_dups))
    
    return codepoints_no_dups, len(codepoints_no_dups)

# Main program
def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - codepoints loading")

    # Convert each utf-8 character into its
    # corresponding codepoint in the font file.
    codepoint_count = rl.ffi.new("int *")
    codepoints = rl.load_codepoints(text, codepoint_count)
    codepoint_count = codepoint_count[0]

    # Remove duplicate codepoints to generate smaller font atlas
    codepoints_list = [codepoints[i] for i in range(codepoint_count)]
    codepoints_no_dups, codepoints_no_dups_count = codepoint_remove_duplicates(codepoints_list, codepoint_count)

    # Create a C array of ints for the codepoints
    codepoints_array = rl.ffi.new("int[]", codepoints_no_dups)
    
    rl.unload_codepoints(codepoints)

    # Load font containing all the provided codepoint glyphs
    # A texture font atlas is automatically generated
    font = rl.load_font_ex(str(THIS_DIR/"resources/DotGothic16-Regular.ttf"), 36,
                           rl.ffi.cast("int *", codepoints_array), codepoints_no_dups_count)

    # Set bilinear scale filter for better font scaling
    rl.set_texture_filter(font.texture, rl.TEXTURE_FILTER_BILINEAR)

    rl.set_text_line_spacing(20)         # Set line spacing for multiline text (when line breaks are included '\n')

    show_font_atlas = False

    codepoint_size = rl.ffi.new("int *")
    ptr = text

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        if rl.is_key_pressed(rl.KEY_SPACE):
            show_font_atlas = not show_font_atlas

        # Testing code: getting next and previous codepoints on provided text
        if rl.is_key_pressed(rl.KEY_RIGHT):
            # Get next codepoint in string and move pointer
            # Note: This part might not work perfectly in Python due to string handling differences
            pass
        elif rl.is_key_pressed(rl.KEY_LEFT):
            # Get previous codepoint in string and move pointer
            # Note: This part might not work perfectly in Python due to string handling differences
            pass

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_rectangle(0, 0, rl.get_screen_width(), 70, rl.BLACK)
        rl.draw_text(f"Total codepoints contained in provided text: {codepoint_count}", 10, 10, 20, rl.GREEN)
        rl.draw_text(f"Total codepoints required for font atlas (duplicates excluded): {codepoints_no_dups_count}", 10, 40, 20, rl.GREEN)

        if show_font_atlas:
            # Draw generated font texture atlas containing provided codepoints
            rl.draw_texture(font.texture, 150, 100, rl.BLACK)
            rl.draw_rectangle_lines(150, 100, font.texture.width, font.texture.height, rl.BLACK)
        else:
            # Draw provided text with loaded font, containing all required codepoint glyphs
            rl.draw_text_ex(font, text, rl.Vector2(160, 110), 48, 5, rl.BLACK)

        rl.draw_text("Press SPACE to toggle font atlas view!", 10, rl.get_screen_height() - 30, 20, rl.GRAY)

        rl.end_drawing()

    # De-Initialization
    rl.unload_font(font)     # Unload font
    rl.close_window()        # Close window and OpenGL context

if __name__ == "__main__":
    main()