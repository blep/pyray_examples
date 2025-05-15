"""raylib [textures] example - Image text drawing using TTF generated font
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.8, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [texture] example - image text drawing")

parrots = rl.load_image(str(THIS_DIR/"resources/parrots.png"))  # Load image in CPU memory (RAM)

# TTF Font loading with custom generation parameters
font = rl.load_font_ex(str(THIS_DIR/"resources/KAISG.ttf"), 64, None, 0)

# Draw over image using custom font
# Note the use of baseSize instead of base_size for property naming
rl.image_draw_text_ex(parrots, font, "[Parrots font drawing]", rl.Vector2(20.0, 20.0), 
                     float(font.baseSize), 0.0, rl.RED)

texture = rl.load_texture_from_image(parrots)  # Image converted to texture, uploaded to GPU memory (VRAM)
rl.unload_image(parrots)  # Once image has been converted to texture and uploaded to VRAM, it can be unloaded from RAM

position = rl.Vector2(float(screenWidth/2 - texture.width/2), 
                    float(screenHeight/2 - texture.height/2 - 20))

showFont = False

rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    if rl.is_key_down(rl.KEY_SPACE):
        showFont = True
    else:
        showFont = False

    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    if not showFont:
        # Draw texture with text already drawn inside
        rl.draw_texture_v(texture, position, rl.WHITE)
        
        # Draw text directly using sprite font
        rl.draw_text_ex(font, "[Parrots font drawing]", 
                       rl.Vector2(position.x + 20, position.y + 20 + 280), 
                       float(font.baseSize), 0.0, rl.WHITE)
    else:
        rl.draw_texture(font.texture, int(screenWidth/2 - font.texture.width/2), 50, rl.BLACK)
    
    rl.draw_text("PRESS SPACE to SHOW FONT ATLAS USED", 290, 420, 10, rl.DARKGRAY)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texture)  # Texture unloading
rl.unload_font(font)        # Unload custom font
rl.close_window()           # Close window and OpenGL context