"""raylib [textures] example - Bunnymark
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 1.6, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import random

THIS_DIR = Path(__file__).resolve().parent

MAX_BUNNIES = 50000  # 50K bunnies limit

# This is the maximum amount of elements (quads) per batch
# NOTE: This value is defined in [rlgl] module and can be changed there
MAX_BATCH_ELEMENTS = 8192

class Bunny:
    def __init__(self, pos, speed, color):
        self.position = pos
        self.speed = speed
        self.color = color

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - bunnymark")

# Load bunny texture
texBunny = rl.load_texture(str(THIS_DIR/"resources/wabbit_alpha.png"))

bunnies = []  # Bunnies list
bunniesCount = 0  # Bunnies counter

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
        # Create more bunnies
        for i in range(100):
            if bunniesCount < MAX_BUNNIES:
                pos = rl.get_mouse_position()
                speed = rl.Vector2(
                    random.uniform(-250, 250) / 60.0,
                    random.uniform(-250, 250) / 60.0
                )
                color = rl.Color(
                    random.randint(50, 240),
                    random.randint(80, 240),
                    random.randint(100, 240),
                    255
                )
                
                bunnies.append(Bunny(pos, speed, color))
                bunniesCount += 1

    # Update bunnies
    for i in range(bunniesCount):
        bunnies[i].position.x += bunnies[i].speed.x
        bunnies[i].position.y += bunnies[i].speed.y

        if ((bunnies[i].position.x + texBunny.width/2) > rl.get_screen_width() or
            (bunnies[i].position.x + texBunny.width/2) < 0):
            bunnies[i].speed.x *= -1

        if ((bunnies[i].position.y + texBunny.height/2) > rl.get_screen_height() or
            (bunnies[i].position.y + texBunny.height/2 - 40) < 0):
            bunnies[i].speed.y *= -1

    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    for i in range(bunniesCount):
        # NOTE: When internal batch buffer limit is reached (MAX_BATCH_ELEMENTS),
        # a draw call is launched and buffer starts being filled again;
        # before issuing a draw call, updated vertex data from internal CPU buffer is sent to GPU...
        # Process of sending data is costly and it could happen that GPU data has not been completely
        # processed for drawing while new data is tried to be sent (updating current in-use buffers)
        # it could generates a stall and consequently a frame drop, limiting the number of drawn bunnies
        rl.draw_texture(texBunny, int(bunnies[i].position.x), int(bunnies[i].position.y), bunnies[i].color)
    
    rl.draw_rectangle(0, 0, screenWidth, 40, rl.BLACK)
    rl.draw_text(f"bunnies: {bunniesCount}", 120, 10, 20, rl.GREEN)
    rl.draw_text(f"batched draw calls: {1 + bunniesCount // MAX_BATCH_ELEMENTS}", 320, 10, 20, rl.MAROON)
    
    rl.draw_fps(10, 10)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texBunny)  # Unload bunny texture
rl.close_window()  # Close window and OpenGL context