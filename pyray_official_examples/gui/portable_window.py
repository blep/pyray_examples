"""raygui - portable window
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
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #-------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 600
    
    rl.set_config_flags(rl.FLAG_WINDOW_UNDECORATED)
    rl.init_window(screen_width, screen_height, "raygui - portable window")
    
    # General variables
    mouse_position = rl.Vector2(0, 0)
    window_position = rl.Vector2(500, 200)
    pan_offset = rl.Vector2(0, 0)
    drag_window = False
    
    rl.set_window_position(int(window_position.x), int(window_position.y))
    
    exit_window = False
    
    rl.set_target_fps(60)
    #-------------------------------------------------------------------------------------
    
    # Main game loop
    while not exit_window and not rl.window_should_close():
        # Update
        #---------------------------------------------------------------------------------
        mouse_position = rl.get_mouse_position()
        
        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON) and not drag_window:
            if rl.check_collision_point_rec(mouse_position, rl.Rectangle(0, 0, screen_width, 20)):
                window_position = rl.get_window_position()
                drag_window = True
                pan_offset = mouse_position
        
        if drag_window:
            window_position.x += (mouse_position.x - pan_offset.x)
            window_position.y += (mouse_position.y - pan_offset.y)
            
            rl.set_window_position(int(window_position.x), int(window_position.y))
            
            if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON):
                drag_window = False
        #---------------------------------------------------------------------------------
        
        # Draw
        #---------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.RAYWHITE)
        
        exit_window = rl.gui_window_box(rl.Rectangle(0, 0, screen_width, screen_height), "#198# PORTABLE WINDOW")
        
        rl.draw_text(f"Mouse Position: [ {int(mouse_position.x)}, {int(mouse_position.y)} ]", 10, 40, 10, rl.DARKGRAY)
        rl.draw_text(f"Window Position: [ {int(window_position.x)}, {int(window_position.y)} ]", 10, 60, 10, rl.DARKGRAY)
        
        rl.end_drawing()
        #---------------------------------------------------------------------------------
    
    # De-Initialization
    #---------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    #---------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
