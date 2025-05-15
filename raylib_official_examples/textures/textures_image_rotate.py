"""raylib [textures] example - Image Rotation
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.0, last time updated with raylib 1.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

NUM_TEXTURES = 3

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - texture rotation")

# NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)
image45 = rl.load_image(str(THIS_DIR/"resources/raylib_logo.png"))
image90 = rl.load_image(str(THIS_DIR/"resources/raylib_logo.png"))
imageNeg90 = rl.load_image(str(THIS_DIR/"resources/raylib_logo.png"))

rl.image_rotate(image45, 45)
rl.image_rotate(image90, 90)
rl.image_rotate(imageNeg90, -90)

textures = [None] * NUM_TEXTURES

textures[0] = rl.load_texture_from_image(image45)
textures[1] = rl.load_texture_from_image(image90)
textures[2] = rl.load_texture_from_image(imageNeg90)

# Unload images now that we have the textures
rl.unload_image(image45)
rl.unload_image(image90)
rl.unload_image(imageNeg90)

currentTexture = 0

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT) or rl.is_key_pressed(rl.KEY_RIGHT):
        currentTexture = (currentTexture + 1) % NUM_TEXTURES  # Cycle between the textures
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_texture(
        textures[currentTexture], 
        screenWidth//2 - textures[currentTexture].width//2, 
        screenHeight//2 - textures[currentTexture].height//2, 
        rl.WHITE
    )
    
    rl.draw_text("Press LEFT MOUSE BUTTON to rotate the image clockwise", 250, 420, 10, rl.DARKGRAY)
    
    rl.end_drawing()

# De-Initialization
for i in range(NUM_TEXTURES):
    rl.unload_texture(textures[i])

rl.close_window()  # Close window and OpenGL context