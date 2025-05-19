"""raylib [textures] example - particles blending
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.7, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from dataclasses import dataclass
from pathlib import Path
import random

THIS_DIR = Path(__file__).resolve().parent

MAX_PARTICLES = 200

@dataclass
class Particle:
    """Particle structure with basic data"""
    position: rl.Vector2
    color: rl.Color
    alpha: float
    size: float
    rotation: float
    active: bool  # NOTE: Use it to activate/deactivate particle

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - particles blending")

# Particles pool, reuse them!
mouseTail = []

# Initialize particles
for i in range(MAX_PARTICLES):
    mouseTail.append(Particle(
        position=rl.Vector2(0, 0),
        color=rl.Color(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            255
        ),
        alpha=1.0,
        size=random.randint(1, 30) / 20.0,
        rotation=random.randint(0, 360),
        active=False
    ))

gravity = 3.0

smoke = rl.load_texture(str(THIS_DIR/"resources/spark_flame.png"))

blending = rl.BLEND_ALPHA

rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    
    # Activate one particle every frame and Update active particles
    # NOTE: Particles initial position should be mouse position when activated
    # NOTE: Particles fall down with gravity and rotation... and disappear after 2 seconds (alpha = 0)
    # NOTE: When a particle disappears, active = false and it can be reused.
    for i in range(MAX_PARTICLES):
        if not mouseTail[i].active:
            mouseTail[i].active = True
            mouseTail[i].alpha = 1.0
            mouseTail[i].position = rl.get_mouse_position()
            break
    
    for i in range(MAX_PARTICLES):
        if mouseTail[i].active:
            mouseTail[i].position.y += gravity / 2
            mouseTail[i].alpha -= 0.005
            
            if mouseTail[i].alpha <= 0.0:
                mouseTail[i].active = False
            
            mouseTail[i].rotation += 2.0
    
    if rl.is_key_pressed(rl.KEY_SPACE):
        if blending == rl.BLEND_ALPHA:
            blending = rl.BLEND_ADDITIVE
        else:
            blending = rl.BLEND_ALPHA
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.DARKGRAY)
    
    rl.begin_blend_mode(blending)
    
    # Draw active particles
    for i in range(MAX_PARTICLES):
        if mouseTail[i].active:
            rl.draw_texture_pro(
                smoke, 
                rl.Rectangle(0.0, 0.0, smoke.width, smoke.height),
                rl.Rectangle(
                    mouseTail[i].position.x, 
                    mouseTail[i].position.y, 
                    smoke.width * mouseTail[i].size, 
                    smoke.height * mouseTail[i].size
                ),
                rl.Vector2(
                    smoke.width * mouseTail[i].size / 2.0, 
                    smoke.height * mouseTail[i].size / 2.0
                ), 
                mouseTail[i].rotation,
                rl.fade(mouseTail[i].color, mouseTail[i].alpha)
            )
    
    rl.end_blend_mode()
    
    rl.draw_text("PRESS SPACE to CHANGE BLENDING MODE", 180, 20, 20, rl.BLACK)
    
    if blending == rl.BLEND_ALPHA:
        rl.draw_text("ALPHA BLENDING", 290, screenHeight - 40, 20, rl.BLACK)
    else:
        rl.draw_text("ADDITIVE BLENDING", 280, screenHeight - 40, 20, rl.RAYWHITE)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(smoke)
rl.close_window()  # Close window and OpenGL context