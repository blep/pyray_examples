"""raylib [textures] example - sprite explosion
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

NUM_FRAMES_PER_LINE = 5
NUM_LINES = 5

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - sprite explosion")

rl.init_audio_device()

# Load explosion sound
fxBoom = rl.load_sound(str(THIS_DIR/"resources/boom.wav"))

# Load explosion texture
explosion = rl.load_texture(str(THIS_DIR/"resources/explosion.png"))

# Init variables for animation
frameWidth = float(explosion.width // NUM_FRAMES_PER_LINE)  # Sprite one frame rectangle width
frameHeight = float(explosion.height // NUM_LINES)          # Sprite one frame rectangle height
currentFrame = 0
currentLine = 0

frameRec = rl.Rectangle(0.0, 0.0, frameWidth, frameHeight)  # Ensure x, y are also float for consistency
position = rl.Vector2(0.0, 0.0)

active = False
framesCounter = 0

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
print('Click on the screen to generate an explosion')

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    
    # Check for mouse button pressed and activate explosion (if not active)
    if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT) and not active:
        position = rl.get_mouse_position()
        active = True
        
        position.x -= frameWidth / 2.0
        position.y -= frameHeight / 2.0
        
        rl.play_sound(fxBoom)
    
    # Compute explosion animation frames
    if active:
        framesCounter += 1
        
        if framesCounter > 2:
            currentFrame += 1
            
            if currentFrame >= NUM_FRAMES_PER_LINE:
                currentFrame = 0
                currentLine += 1
                
                if currentLine >= NUM_LINES:
                    currentLine = 0
                    active = False
            
            framesCounter = 0
    
    frameRec.x = frameWidth * currentFrame
    frameRec.y = frameHeight * currentLine
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    # Draw explosion required frame rectangle
    if active:
        rl.draw_texture_rec(explosion, frameRec, position, rl.WHITE)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(explosion)  # Unload texture
rl.unload_sound(fxBoom)      # Unload sound

rl.close_audio_device()
rl.close_window()  # Close window and OpenGL context