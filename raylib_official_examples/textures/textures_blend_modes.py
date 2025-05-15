"""raylib [textures] example - blend modes
Example complexity rating: [★☆☆☆] 1/4
NOTE: Images are loaded in CPU memory (RAM); textures are loaded in GPU memory (VRAM)
Example originally created with raylib 3.5, last time updated with raylib 3.5
Example contributed by Karlo Licudine (@accidentalrebel) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2020-2025 Karlo Licudine (@accidentalrebel)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - blend modes")

# NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)
bgImage = rl.load_image(str(THIS_DIR/"resources/cyberpunk_street_background.png"))  # Loaded in CPU memory (RAM)
bgTexture = rl.load_texture_from_image(bgImage)  # Image converted to texture, GPU memory (VRAM)

fgImage = rl.load_image(str(THIS_DIR/"resources/cyberpunk_street_foreground.png"))  # Loaded in CPU memory (RAM)
fgTexture = rl.load_texture_from_image(fgImage)  # Image converted to texture, GPU memory (VRAM)

# Once image has been converted to texture and uploaded to VRAM, it can be unloaded from RAM
rl.unload_image(bgImage)
rl.unload_image(fgImage)

blendCountMax = 4
blendMode = 0

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    if rl.is_key_pressed(rl.KEY_SPACE):
        if blendMode >= (blendCountMax - 1):
            blendMode = 0
        else:
            blendMode += 1

    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_texture(bgTexture, screenWidth//2 - bgTexture.width//2, 
                   screenHeight//2 - bgTexture.height//2, rl.WHITE)
    
    # Apply the blend mode and then draw the foreground texture
    rl.begin_blend_mode(blendMode)
    rl.draw_texture(fgTexture, screenWidth//2 - fgTexture.width//2, 
                   screenHeight//2 - fgTexture.height//2, rl.WHITE)
    rl.end_blend_mode()
    
    # Draw the texts
    rl.draw_text("Press SPACE to change blend modes.", 310, 350, 10, rl.GRAY)
    
    if blendMode == rl.BLEND_ALPHA:
        rl.draw_text("Current: BLEND_ALPHA", (screenWidth // 2) - 60, 370, 10, rl.GRAY)
    elif blendMode == rl.BLEND_ADDITIVE:
        rl.draw_text("Current: BLEND_ADDITIVE", (screenWidth // 2) - 60, 370, 10, rl.GRAY)
    elif blendMode == rl.BLEND_MULTIPLIED:
        rl.draw_text("Current: BLEND_MULTIPLIED", (screenWidth // 2) - 60, 370, 10, rl.GRAY)
    elif blendMode == rl.BLEND_ADD_COLORS:
        rl.draw_text("Current: BLEND_ADD_COLORS", (screenWidth // 2) - 60, 370, 10, rl.GRAY)
    
    rl.draw_text("(c) Cyberpunk Street Environment by Luis Zuno (@ansimuz)", 
               screenWidth - 330, screenHeight - 20, 10, rl.GRAY)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(fgTexture)  # Unload foreground texture
rl.unload_texture(bgTexture)  # Unload background texture

rl.close_window()  # Close window and OpenGL context