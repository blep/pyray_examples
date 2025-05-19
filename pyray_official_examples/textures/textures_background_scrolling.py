"""raylib [textures] example - Background scrolling
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 2.0, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - background scrolling")

# NOTE: Be careful, background width must be equal or bigger than screen width
# if not, texture should be draw more than two times for scrolling effect
background = rl.load_texture(str(THIS_DIR/"resources/cyberpunk_street_background.png"))
midground = rl.load_texture(str(THIS_DIR/"resources/cyberpunk_street_midground.png"))
foreground = rl.load_texture(str(THIS_DIR/"resources/cyberpunk_street_foreground.png"))

scrollingBack = 0.0
scrollingMid = 0.0
scrollingFore = 0.0

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    scrollingBack -= 0.1
    scrollingMid -= 0.5
    scrollingFore -= 1.0

    # NOTE: Texture is scaled twice its size, so it should be considered on scrolling
    if scrollingBack <= -background.width*2:
        scrollingBack = 0
    if scrollingMid <= -midground.width*2:
        scrollingMid = 0
    if scrollingFore <= -foreground.width*2:
        scrollingFore = 0

    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.get_color(0x052c46ff))
    
    # Draw background image twice
    # NOTE: Texture is scaled twice its size
    rl.draw_texture_ex(background, rl.Vector2(scrollingBack, 20), 0.0, 2.0, rl.WHITE)
    rl.draw_texture_ex(background, rl.Vector2(background.width*2 + scrollingBack, 20), 0.0, 2.0, rl.WHITE)
    
    # Draw midground image twice
    rl.draw_texture_ex(midground, rl.Vector2(scrollingMid, 20), 0.0, 2.0, rl.WHITE)
    rl.draw_texture_ex(midground, rl.Vector2(midground.width*2 + scrollingMid, 20), 0.0, 2.0, rl.WHITE)
    
    # Draw foreground image twice
    rl.draw_texture_ex(foreground, rl.Vector2(scrollingFore, 70), 0.0, 2.0, rl.WHITE)
    rl.draw_texture_ex(foreground, rl.Vector2(foreground.width*2 + scrollingFore, 70), 0.0, 2.0, rl.WHITE)
    
    rl.draw_text("BACKGROUND SCROLLING & PARALLAX", 10, 10, 20, rl.RED)
    rl.draw_text("(c) Cyberpunk Street Environment by Luis Zuno (@ansimuz)", 
               screenWidth - 330, screenHeight - 20, 10, rl.RAYWHITE)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(background)  # Unload background texture
rl.unload_texture(midground)   # Unload midground texture
rl.unload_texture(foreground)  # Unload foreground texture

rl.close_window()  # Close window and OpenGL context