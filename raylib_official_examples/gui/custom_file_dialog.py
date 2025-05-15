"""raygui - custom file dialog to load image
DEPENDENCIES:
    raylib 4.0  - Windowing/input management and drawing.
    raygui 3.0  - Immediate-mode GUI controls.
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99
LICENSE: zlib/libpng
Copyright (c) 2016-2024 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import os
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# This is a simplified version since the full custom GUI file dialog implementation
# would require porting the C header file to Python as well.
# For this example, we'll simulate a basic file dialog using PyRay

def main():
    # Initialization
    #---------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 560

    rl.init_window(screen_width, screen_height, "raygui - custom modal dialog")
    rl.set_exit_key(0)

    # Variables for our custom file dialog
    file_dialog_active = False
    selected_file = ""
    current_directory = os.getcwd()

    # File list for the current directory
    file_list = []
    file_count = 0
    file_scroll_index = 0
    file_selected = -1

    # Button to open the dialog
    dialog_button_rect = rl.Rectangle(20, 20, 140, 30)
    
    # Dialog rectangle
    dialog_rect = rl.Rectangle(screen_width/2 - 200, screen_height/2 - 150, 400, 300)
    
    # Image texture to display
    texture = rl.Texture2D()
    file_name_to_load = ""

    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():
        # Update
        #----------------------------------------------------------------------------------
        
        # Update file list if dialog is activated
        if file_dialog_active and len(file_list) == 0:
            try:
                # Get all files in the current directory
                files = [f for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f))]
                # Filter just PNG files for this example
                files = [f for f in files if f.endswith('.png')]
                file_list = files
                file_count = len(file_list)
            except:
                file_list = []
                file_count = 0
        
        # Check if image selection is made
        if file_selected >= 0 and file_selected < file_count and file_dialog_active:
            selected_file = file_list[file_selected]
            file_name_to_load = os.path.join(current_directory, selected_file)
            
            # Load the selected image
            if rl.is_file_extension(selected_file, ".png"):
                if texture.id != 0:
                    rl.unload_texture(texture)
                texture = rl.load_texture(file_name_to_load)
                file_dialog_active = False
                file_selected = -1
                file_list = []
                file_count = 0
        
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.get_color(rl.gui_get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))

        # Draw the loaded texture if any
        if texture.id != 0:
            rl.draw_texture(texture, int(screen_width/2 - texture.width/2), 
                          int(screen_height/2 - texture.height/2 - 5), rl.WHITE)
            rl.draw_rectangle_lines(int(screen_width/2 - texture.width/2), 
                                  int(screen_height/2 - texture.height/2 - 5), 
                                  texture.width, texture.height, rl.BLACK)
        
        # Draw file name
        rl.draw_text(file_name_to_load, 208, screen_height - 20, 10, rl.GRAY)

        # raygui: controls drawing
        #----------------------------------------------------------------------------------
        if file_dialog_active:
            rl.gui_lock()

        if rl.gui_button(dialog_button_rect, rl.gui_icon_text(rl.ICON_FILE_OPEN, "Open Image")):
            file_dialog_active = True
            file_list = []  # Reset file list
            file_selected = -1

        rl.gui_unlock()

        # Draw our custom file dialog
        if file_dialog_active:
            # Dialog background
            rl.draw_rectangle_rounded(dialog_rect, 0.2, 8, rl.fade(rl.LIGHTGRAY, 0.9))
            rl.draw_rectangle_rounded_lines(dialog_rect, 0.2, 8, 2, rl.BLACK)
            
            # Dialog title
            rl.gui_label(rl.Rectangle(dialog_rect.x + 10, dialog_rect.y + 10, 
                                    dialog_rect.width - 20, 30), "Select PNG Image")
            
            # File list area
            file_list_rect = rl.Rectangle(dialog_rect.x + 10, dialog_rect.y + 50, 
                                        dialog_rect.width - 20, dialog_rect.height - 100)
            rl.gui_panel(file_list_rect, "")
            
            # Draw file list
            for i in range(file_count):
                file_item_rect = rl.Rectangle(file_list_rect.x + 5, file_list_rect.y + 5 + i*30, 
                                            file_list_rect.width - 10, 25)
                
                if i == file_selected:
                    rl.draw_rectangle_rec(file_item_rect, rl.SKYBLUE)
                
                if rl.gui_button(file_item_rect, file_list[i]):
                    file_selected = i
            
            # Close button
            close_btn_rect = rl.Rectangle(dialog_rect.x + dialog_rect.width - 90, 
                                        dialog_rect.y + dialog_rect.height - 40, 80, 30)
            if rl.gui_button(close_btn_rect, "Close"):
                file_dialog_active = False
                file_list = []
                file_selected = -1

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    if texture.id != 0:
        rl.unload_texture(texture)  # Unload texture

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

# Execute the main function
if __name__ == '__main__':
    main()
