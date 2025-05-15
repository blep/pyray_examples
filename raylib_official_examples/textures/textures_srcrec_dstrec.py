"""raylib [textures] example - Texture source and destination rectangles
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 1.3, last time updated with raylib 1.3
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

rl.init_window(screenWidth, screenHeight, "raylib [textures] examples - texture source and destination rectangles")

# NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)

scarfy = rl.load_texture(str(THIS_DIR/"resources/scarfy.png"))  # Texture loading

frameWidth = scarfy.width//6
frameHeight = scarfy.height

# Source rectangle (part of the texture to use for drawing)
sourceRec = rl.Rectangle(0.0, 0.0, frameWidth, frameHeight)

# Destination rectangle (screen rectangle where drawing part of texture)
destRec = rl.Rectangle(screenWidth/2.0, screenHeight/2.0, frameWidth*2.0, frameHeight*2.0)

# Origin of the texture (rotation/scale point), it's relative to destination rectangle size
origin = rl.Vector2(frameWidth, frameHeight)

rotation = 0

rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    rotation += 1
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    # NOTE: Using DrawTexturePro() we can easily rotate and scale the part of the texture we draw
    # sourceRec defines the part of the texture we use for drawing
    # destRec defines the rectangle where our texture part will fit (scaling it to fit)
    # origin defines the point of the texture used as reference for rotation and scaling
    # rotation defines the texture rotation (using origin as rotation point)
    rl.draw_texture_pro(scarfy, sourceRec, destRec, origin, float(rotation), rl.WHITE)
    
    rl.draw_line(int(destRec.x), 0, int(destRec.x), screenHeight, rl.GRAY)
    rl.draw_line(0, int(destRec.y), screenWidth, int(destRec.y), rl.GRAY)
    
    rl.draw_text("(c) Scarfy sprite by Eiden Marsal", screenWidth - 200, screenHeight - 20, 10, rl.GRAY)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(scarfy)  # Texture unloading
rl.close_window()  # Close window and OpenGL context