"""raygui - style selector
DEPENDENCIES:
    raylib 4.5          - Windowing/input management and drawing
    raygui 3.5          - Immediate-mode GUI controls with custom styling and icons
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99
LICENSE: zlib/libpng
Copyright (c) 2016-2024 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #-------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 480
    
    rl.init_window(screen_width, screen_height, "raygui - styles selector")
    rl.set_exit_key(0)
    
    # Custom GUI font loading
    # font = rl.load_font_ex(str(THIS_DIR/"fonts/custom_font.ttf"), 12, None, 0)
    # rl.gui_set_font(font)
    
    exit_window = False
    show_message_box = False
    
    # Load default style
    rl.gui_load_style_bluish()
    visual_style_active_ptr = rl.ffi.new('int *', 4)
    prev_visual_style_active = 4
    
    rl.set_target_fps(60)
    #-------------------------------------------------------------------------------------
    
    # Main game loop
    while not exit_window:
        # Update
        #---------------------------------------------------------------------------------
        exit_window = rl.window_should_close()
        
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            show_message_box = not show_message_box
        
        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()
            
            if (dropped_files.count > 0) and rl.is_file_extension(dropped_files.paths[0], ".rgs"):
                rl.gui_load_style(dropped_files.paths[0])
            
            rl.unload_dropped_files(dropped_files)  # Clear internal buffers
        
        if visual_style_active_ptr[0] != prev_visual_style_active:
            # Reset to default internal style
            # NOTE: Required to unload any previously loaded font texture
            rl.gui_load_style_default()
            
            if visual_style_active_ptr[0] == 1:
                rl.gui_load_style_jungle()
            elif visual_style_active_ptr[0] == 2:
                rl.gui_load_style_candy()
            elif visual_style_active_ptr[0] == 3:
                rl.gui_load_style_lavanda()
            elif visual_style_active_ptr[0] == 4:
                rl.gui_load_style_cyber()
            elif visual_style_active_ptr[0] == 5:
                rl.gui_load_style_terminal()
            elif visual_style_active_ptr[0] == 6:
                rl.gui_load_style_ashes()
            elif visual_style_active_ptr[0] == 7:
                rl.gui_load_style_bluish()
            elif visual_style_active_ptr[0] == 8:
                rl.gui_load_style_dark()
            elif visual_style_active_ptr[0] == 9:
                rl.gui_load_style_cherry()
            elif visual_style_active_ptr[0] == 10:
                rl.gui_load_style_sunny()
            elif visual_style_active_ptr[0] == 11:
                rl.gui_load_style_enefete()
            
            prev_visual_style_active = visual_style_active_ptr[0]
        #---------------------------------------------------------------------------------
        
        # Draw
        #---------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.get_color(rl.get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))
        
        # Visuals options
        rl.gui_label(rl.Rectangle(10, 10, 60, 24), "Style:")
        rl.gui_combo_box(rl.Rectangle(60, 10, 120, 24), "default;Jungle;Candy;Lavanda;Cyber;Terminal;Ashes;Bluish;Dark;Cherry;Sunny;Enefete", visual_style_active_ptr)
        
        font = rl.gui_get_font()
        rl.draw_rectangle(10, 44, font.texture.width, font.texture.height, rl.BLACK)
        rl.draw_texture(font.texture, 10, 44, rl.WHITE)
        rl.draw_rectangle_lines(10, 44, font.texture.width, font.texture.height,
                               rl.get_color(rl.get_style(rl.DEFAULT, rl.LINE_COLOR)))
        
        # GuiSetIconScale(2)
        # GuiSetStyle(BUTTON, TEXT_ALIGNMENT, TEXT_ALIGN_RIGHT)
        # GuiButton((Rectangle){ 25, 255, 300, 30 }, GuiIconText(ICON_FILE_SAVE, "Save File"))
        # GuiSetStyle(BUTTON, TEXT_ALIGNMENT, TEXT_ALIGN_CENTER)
        #---------------------------------------------------------------------------------
        
        rl.end_drawing()
        #---------------------------------------------------------------------------------
    
    # De-Initialization
    #---------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    #---------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
