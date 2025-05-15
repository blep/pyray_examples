"""raylib [textures] example - Procedural images generation
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.8, last time updated with raylib 1.8
Example contributed by Wilhem Barbier (@nounoursheureux) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Wilhem Barbier (@nounoursheureux) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

NUM_TEXTURES = 9  # Currently we have 8 generation algorithms but some have multiple purposes (Linear and Square Gradients)

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - procedural images generation")

# Generate procedural images
verticalGradient = rl.gen_image_gradient_linear(screenWidth, screenHeight, 0, rl.RED, rl.BLUE)
horizontalGradient = rl.gen_image_gradient_linear(screenWidth, screenHeight, 90, rl.RED, rl.BLUE)
diagonalGradient = rl.gen_image_gradient_linear(screenWidth, screenHeight, 45, rl.RED, rl.BLUE)
radialGradient = rl.gen_image_gradient_radial(screenWidth, screenHeight, 0.0, rl.WHITE, rl.BLACK)
squareGradient = rl.gen_image_gradient_square(screenWidth, screenHeight, 0.0, rl.WHITE, rl.BLACK)
checked = rl.gen_image_checked(screenWidth, screenHeight, 32, 32, rl.RED, rl.BLUE)
whiteNoise = rl.gen_image_white_noise(screenWidth, screenHeight, 0.5)
perlinNoise = rl.gen_image_perlin_noise(screenWidth, screenHeight, 50, 50, 4.0)
cellular = rl.gen_image_cellular(screenWidth, screenHeight, 32)

# Load textures from generated images
textures = [
    rl.load_texture_from_image(verticalGradient),
    rl.load_texture_from_image(horizontalGradient),
    rl.load_texture_from_image(diagonalGradient),
    rl.load_texture_from_image(radialGradient),
    rl.load_texture_from_image(squareGradient),
    rl.load_texture_from_image(checked),
    rl.load_texture_from_image(whiteNoise),
    rl.load_texture_from_image(perlinNoise),
    rl.load_texture_from_image(cellular)
]

# Unload image data (CPU RAM)
rl.unload_image(verticalGradient)
rl.unload_image(horizontalGradient)
rl.unload_image(diagonalGradient)
rl.unload_image(radialGradient)
rl.unload_image(squareGradient)
rl.unload_image(checked)
rl.unload_image(whiteNoise)
rl.unload_image(perlinNoise)
rl.unload_image(cellular)

currentTexture = 0

rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT) or rl.is_key_pressed(rl.KEY_RIGHT):
        currentTexture = (currentTexture + 1) % NUM_TEXTURES  # Cycle between the textures
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_texture(textures[currentTexture], 0, 0, rl.WHITE)
    
    rl.draw_rectangle(30, 400, 325, 30, rl.fade(rl.SKYBLUE, 0.5))
    rl.draw_rectangle_lines(30, 400, 325, 30, rl.fade(rl.WHITE, 0.5))
    rl.draw_text("MOUSE LEFT BUTTON to CYCLE PROCEDURAL TEXTURES", 40, 410, 10, rl.WHITE)
    
    texture_names = [
        "VERTICAL GRADIENT",
        "HORIZONTAL GRADIENT",
        "DIAGONAL GRADIENT",
        "RADIAL GRADIENT",
        "SQUARE GRADIENT",
        "CHECKED",
        "WHITE NOISE",
        "PERLIN NOISE",
        "CELLULAR"
    ]
    
    texture_positions = [
        (560, 10), (540, 10), (540, 10), (580, 10), (580, 10), 
        (680, 10), (640, 10), (640, 10), (670, 10)
    ]
    
    texture_colors = [
        rl.RAYWHITE, rl.RAYWHITE, rl.RAYWHITE, rl.LIGHTGRAY, rl.LIGHTGRAY,
        rl.RAYWHITE, rl.RED, rl.RED, rl.RAYWHITE
    ]
    
    # Draw the name of the current texture
    pos = texture_positions[currentTexture]
    rl.draw_text(texture_names[currentTexture], pos[0], pos[1], 20, texture_colors[currentTexture])
    
    rl.end_drawing()

# De-Initialization
# Unload textures data (GPU VRAM)
for texture in textures:
    rl.unload_texture(texture)

rl.close_window()  # Close window and OpenGL context