"""raylib [textures] example - Sprite animation
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.3, last time updated with raylib 1.3
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

MAX_FRAME_SPEED = 15
MIN_FRAME_SPEED = 1

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [texture] example - sprite anim")

# NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)
scarfy = rl.load_texture(str(THIS_DIR/"resources/scarfy.png"))  # Texture loading

position = rl.Vector2(350.0, 280.0)
frameRec = rl.Rectangle(0.0, 0.0, float(scarfy.width)/6, float(scarfy.height))
currentFrame = 0

framesCounter = 0
framesSpeed = 8  # Number of spritesheet frames shown by second

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    framesCounter += 1

    if framesCounter >= (60/framesSpeed):
        framesCounter = 0
        currentFrame += 1

        if currentFrame > 5:
            currentFrame = 0

        frameRec.x = float(currentFrame) * float(scarfy.width)/6

    # Control frames speed
    if rl.is_key_pressed(rl.KEY_RIGHT):
        framesSpeed += 1
    elif rl.is_key_pressed(rl.KEY_LEFT):
        framesSpeed -= 1

    if framesSpeed > MAX_FRAME_SPEED:
        framesSpeed = MAX_FRAME_SPEED
    elif framesSpeed < MIN_FRAME_SPEED:
        framesSpeed = MIN_FRAME_SPEED

    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_texture(scarfy, 15, 40, rl.WHITE)
    rl.draw_rectangle_lines(15, 40, scarfy.width, scarfy.height, rl.LIME)
    rl.draw_rectangle_lines(15 + int(frameRec.x), 40 + int(frameRec.y), 
                           int(frameRec.width), int(frameRec.height), rl.RED)
    
    rl.draw_text("FRAME SPEED: ", 165, 210, 10, rl.DARKGRAY)
    rl.draw_text(f"{framesSpeed:02d} FPS", 575, 210, 10, rl.DARKGRAY)
    rl.draw_text("PRESS RIGHT/LEFT KEYS to CHANGE SPEED!", 290, 240, 10, rl.DARKGRAY)
    
    for i in range(MAX_FRAME_SPEED):
        if i < framesSpeed:
            rl.draw_rectangle(250 + 21*i, 205, 20, 20, rl.RED)
        rl.draw_rectangle_lines(250 + 21*i, 205, 20, 20, rl.MAROON)
    
    rl.draw_texture_rec(scarfy, frameRec, position, rl.WHITE)  # Draw part of the texture
    
    rl.draw_text("(c) Scarfy sprite by Eiden Marsal", screenWidth - 200, screenHeight - 20, 10, rl.GRAY)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(scarfy)  # Texture unloading
rl.close_window()  # Close window and OpenGL context