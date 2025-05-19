"""raylib [textures] example - Retrieve image data from texture: LoadImageFromTexture()
Example complexity rating: [★☆☆☆] 1/4
NOTE: Images are loaded in CPU memory (RAM); textures are loaded in GPU memory (VRAM)
Example originally created with raylib 1.3, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - texture to image")

# NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)

image = rl.load_image(str(THIS_DIR/"resources/raylib_logo.png"))  # Load image data into CPU memory (RAM)
texture = rl.load_texture_from_image(image)          # Image converted to texture, GPU memory (RAM -> VRAM)
rl.unload_image(image)                             # Unload image data from CPU memory (RAM)

image = rl.load_image_from_texture(texture)          # Load image from GPU texture (VRAM -> RAM)
rl.unload_texture(texture)                         # Unload texture from GPU memory (VRAM)

texture = rl.load_texture_from_image(image)          # Recreate texture from retrieved image data (RAM -> VRAM)
rl.unload_image(image)                             # Unload retrieved image data from CPU memory (RAM)

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_texture(
        texture, 
        screenWidth//2 - texture.width//2, 
        screenHeight//2 - texture.height//2, 
        rl.WHITE
    )
    
    rl.draw_text("this IS a texture loaded from an image!", 300, 370, 10, rl.GRAY)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texture)  # Texture unloading
rl.close_window()  # Close window and OpenGL context