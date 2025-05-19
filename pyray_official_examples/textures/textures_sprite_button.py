"""raylib [textures] example - sprite button
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

NUM_FRAMES = 3  # Number of frames (rectangles) for the button sprite texture

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - sprite button")

rl.init_audio_device()  # Initialize audio device

fxButton = rl.load_sound(str(THIS_DIR/"resources/buttonfx.wav"))  # Load button sound
button = rl.load_texture(str(THIS_DIR/"resources/button.png"))  # Load button texture

# Define frame rectangle for drawing
frameHeight = button.height / NUM_FRAMES
sourceRec = rl.Rectangle(0, 0, button.width, frameHeight)

# Define button bounds on screen
btnBounds = rl.Rectangle(
    screenWidth/2.0 - button.width/2.0,
    screenHeight/2.0 - button.height/NUM_FRAMES/2.0,
    button.width,
    frameHeight
)

btnState = 0        # Button state: 0-NORMAL, 1-MOUSE_HOVER, 2-PRESSED
btnAction = False   # Button action should be activated

mousePoint = rl.Vector2(0.0, 0.0)

rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    mousePoint = rl.get_mouse_position()
    btnAction = False
    
    # Check button state
    if rl.check_collision_point_rec(mousePoint, btnBounds):
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            btnState = 2
        else:
            btnState = 1
        
        if rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT):
            btnAction = True
    else:
        btnState = 0
    
    if btnAction:
        rl.play_sound(fxButton)
        
        # TODO: Any desired action
    
    # Calculate button frame rectangle to draw depending on button state
    sourceRec.y = btnState * frameHeight
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    # Draw button frame
    rl.draw_texture_rec(
        button, 
        sourceRec, 
        rl.Vector2(btnBounds.x, btnBounds.y), 
        rl.WHITE
    )
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(button)  # Unload button texture
rl.unload_sound(fxButton)  # Unload sound

rl.close_audio_device()  # Close audio device
rl.close_window()  # Close window and OpenGL context