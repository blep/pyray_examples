#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
raygui - gui value box float extension

DEPENDENCIES:
    pyray - Python wrapper for raylib
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

def gui_value_box_float(bounds, text, text_value, value_ptr, edit_mode):
    """
    ValueBox control for float values, inspired by GuiValueBox
    
    Parameters:
        bounds (Rectangle): Rectangle defining the bounds of the control
        text (str): Text to display alongside the value box (can be None)
        text_value (str): Current text value displayed in the box
        value_ptr (float*): Pointer to float value to be modified
        edit_mode (bool): Whether the control is in edit mode
    
    Returns:
        bool: True if value changed or enter/key pressed
    """
    state = rl.gui_get_state()
    result = False
    
    text_bounds = rl.Rectangle(0, 0, 0, 0)
    if text is not None:
        text_bounds.width = float(rl.measure_text(text, rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)))
        text_bounds.height = bounds.height
        text_bounds.x = bounds.x + bounds.width + 5
        text_bounds.y = bounds.y + bounds.height/2 - text_bounds.height/2
        
    if not edit_mode:
        # Format float value with 2 decimal places
        text_value = f"{value_ptr[0]:.2f}"
        
    pressed = rl.gui_text_box_ex(bounds, text_value, 64, edit_mode)
    
    if pressed:
        result = True
        
    if edit_mode:
        value_text = rl.gui_text_box_get_text()
        try:
            new_value = float(value_text)
            value_ptr[0] = new_value
        except:
            # Skip parsing if the value is invalid
            pass
    
    # Draw text label if provided
    if text is not None:
        rl.gui_draw_text(text, text_bounds, rl.TEXT_ALIGN_LEFT, rl.get_color(rl.get_style(rl.DEFAULT, rl.TEXT + (state * 3))))
    
    return result

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450
    
    rl.init_window(screen_width, screen_height, "raygui - value box float test")
    
    value_box_value_ptr = rl.ffi.new('float *', 0.0)
    value_box_edit_mode = False
    value_box_text_value = ""
    
    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------
    
    # Main game loop
    while not rl.window_should_close():
        # Update
        #----------------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------------
        
        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        # PORT: "0xffff_ffff &" is a work-around for converting the negative int32 to uint32
        rl.clear_background(rl.get_color(0xffff_ffff & rl.gui_get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))
        
        if gui_value_box_float(rl.Rectangle(25, 175, 125, 30), None, value_box_text_value, value_box_value_ptr, value_box_edit_mode):
            value_box_edit_mode = not value_box_edit_mode
            print(f"Value: {value_box_value_ptr[0]:.2f}")
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------
    
    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
