"""raygui - basic calculator app with custom input box for float values
DEPENDENCIES:
    raylib 4.5  - Windowing/input management and drawing.
    raygui 3.5  - Immediate-mode GUI controls.
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Global variable shared by all gui_float_box()
gui_floating_point_index = 0

def gui_float_box(bounds, text, value_ptr, min_value, max_value, edit_mode):
    """
    Custom input box that works with float values. Basically gui_value_box(), but with some changes
    """
    RAYGUI_VALUEBOX_MAX_CHARS = 32
    
    result = 0
    state = rl.gui_get_state()
    
    text_value = ""
    
    text_bounds = rl.Rectangle(0, 0, 0, 0)
    if text is not None:
        text_bounds.width = float(rl.measure_text(text, 10) + 2)
        text_bounds.height = float(rl.get_style(rl.DEFAULT, rl.TEXT_SIZE))
        text_bounds.x = bounds.x + bounds.width + 2
        text_bounds.y = bounds.y + bounds.height/2 - text_bounds.height/2
        
    if not edit_mode:
        text_value = f"{value_ptr[0]}"
    
    pressed = rl.gui_text_box_ex(bounds, text_value, RAYGUI_VALUEBOX_MAX_CHARS, edit_mode)
    
    if pressed:
        result = 1
        if not edit_mode:
            global gui_floating_point_index
            gui_floating_point_index = 0
    
    if edit_mode:
        value_text = rl.gui_text_box_get_text()
        
        try:
            new_value = float(value_text)
            value_ptr[0] = new_value
        except:
            # Skip parsing if the value is invalid
            pass
            
        if rl.is_key_pressed(rl.KEY_COMMA) or rl.is_key_pressed(rl.KEY_KP_DECIMAL):
            digit = rl.get_char_pressed()
            if digit == 44 or digit == 46:  # Check for ',' or '.'
                rl.gui_text_box_set_cursor_index(gui_floating_point_index)
        
    # Draw text label if provided
    if text is not None:
        rl.gui_draw_text(text, text_bounds, rl.TEXT_ALIGN_LEFT, rl.get_color(rl.get_style(rl.DEFAULT, rl.TEXT + (state * 3))))
        
    return result

def main():
    # Initialization
    rl.init_window(250, 100, "Basic calculator")
    
    # General variables
    rl.set_target_fps(60)
    
    variable_a_ptr = rl.ffi.new('float *', 0.0)
    variable_b_ptr = rl.ffi.new('float *', 0.0)
    result_ptr = rl.ffi.new('float *', 0.0)
    operation = '+'
    
    variable_a_mode = False
    variable_b_mode = False
    
    # Main game loop
    while not rl.window_should_close():
        # Draw
        rl.begin_drawing()
        
        rl.clear_background(rl.RAYWHITE)
        
        if gui_float_box(rl.Rectangle(10, 10, 100, 20), None, variable_a_ptr, -1000000.0, 1000000.0, variable_a_mode):
            variable_a_mode = not variable_a_mode
        if gui_float_box(rl.Rectangle(140, 10, 100, 20), None, variable_b_ptr, -1000000.0, 1000000.0, variable_b_mode):
            variable_b_mode = not variable_b_mode
        
        if rl.gui_button(rl.Rectangle(10, 70, 50, 20), "+"):
            result_ptr[0] = variable_a_ptr[0] + variable_b_ptr[0]
            operation = '+'
        if rl.gui_button(rl.Rectangle(70, 70, 50, 20), "-"):
            result_ptr[0] = variable_a_ptr[0] - variable_b_ptr[0]
            operation = '-'
        if rl.gui_button(rl.Rectangle(130, 70, 50, 20), "*"):
            result_ptr[0] = variable_a_ptr[0] * variable_b_ptr[0]
            operation = '*'
        if rl.gui_button(rl.Rectangle(190, 70, 50, 20), "/"):
            result_ptr[0] = variable_a_ptr[0] / variable_b_ptr[0]
            operation = '/'
            
        rl.draw_text(operation, 123, 15, 10, rl.DARKGRAY)
        
        gui_float_box(rl.Rectangle(55, 40, 135, 20), "= ", result_ptr, -2000000.0, 2000000.0, False)
        
        rl.end_drawing()
        
    rl.close_window()

if __name__ == "__main__":
    main()
