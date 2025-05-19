#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
raygui - Standalone mode usage template

DEPENDENCIES:
    pyray - Python wrapper for raylib
"""

# In real standalone mode, you would need to implement a custom backend
# for raygui. Since we're using pyray which already includes raygui,
# this example is more of a template for how a standalone app would be structured.

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

def main():
    # TODO: Initialize your systems (window, graphics, inputs)
    # Example:
    screen_width = 800
    screen_height = 450
    rl.init_window(screen_width, screen_height, "raygui - standalone template")
    
    # TODO: Create your game loop
    while not rl.window_should_close():
        # Update
        # ----------------------------------------------------------------------------------
        
        # ----------------------------------------------------------------------------------
        
        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        
        # TODO: Use raygui API
        rl.gui_button(rl.Rectangle(10, 10, 140, 30), "This is a button")
        
        rl.end_drawing()
        # ----------------------------------------------------------------------------------
    
    # TODO: De-initialize all resources
    rl.close_window()

if __name__ == "__main__":
    main()
