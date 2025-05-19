"""raylib [textures] example - Retrive image channel (mask)
NOTE: Images are loaded in CPU memory (RAM); textures are loaded in GPU memory (VRAM)
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 5.1-dev, last time updated with raylib 5.1-dev
Example contributed by Bruno Cabral (@brccabral) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2024-2025 Bruno Cabral (@brccabral) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - extract channel from image")

fudesumiImage = rl.load_image(str(THIS_DIR/"resources/fudesumi.png"))

imageAlpha = rl.image_from_channel(fudesumiImage, 3)  # Alpha channel (3)
rl.image_alpha_mask(imageAlpha, imageAlpha)

imageRed = rl.image_from_channel(fudesumiImage, 0)    # Red channel (0)
rl.image_alpha_mask(imageRed, imageAlpha)

imageGreen = rl.image_from_channel(fudesumiImage, 1)  # Green channel (1)
rl.image_alpha_mask(imageGreen, imageAlpha)

imageBlue = rl.image_from_channel(fudesumiImage, 2)   # Blue channel (2)
rl.image_alpha_mask(imageBlue, imageAlpha)

backgroundImage = rl.gen_image_checked(
    screenWidth, screenHeight, 
    screenWidth//20, screenHeight//20, 
    rl.ORANGE, rl.YELLOW
)

fudesumiTexture = rl.load_texture_from_image(fudesumiImage)
textureAlpha = rl.load_texture_from_image(imageAlpha)
textureRed = rl.load_texture_from_image(imageRed)
textureGreen = rl.load_texture_from_image(imageGreen)
textureBlue = rl.load_texture_from_image(imageBlue)
backgroundTexture = rl.load_texture_from_image(backgroundImage)

rl.unload_image(fudesumiImage)
rl.unload_image(imageAlpha)
rl.unload_image(imageRed)
rl.unload_image(imageGreen)
rl.unload_image(imageBlue)
rl.unload_image(backgroundImage)

# Define rectangle for the source image
fudesumiRec = rl.Rectangle(0, 0, fudesumiTexture.width, fudesumiTexture.height)

# Define position rectangles for all textures
fudesumiPos = rl.Rectangle(50, 10, fudesumiTexture.width*0.8, fudesumiTexture.height*0.8)
redPos = rl.Rectangle(410, 10, fudesumiPos.width / 2, fudesumiPos.height / 2)
greenPos = rl.Rectangle(600, 10, fudesumiPos.width / 2, fudesumiPos.height / 2)
bluePos = rl.Rectangle(410, 230, fudesumiPos.width / 2, fudesumiPos.height / 2)
alphaPos = rl.Rectangle(600, 230, fudesumiPos.width / 2, fudesumiPos.height / 2)

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Draw
    rl.begin_drawing()
    
    rl.draw_texture(backgroundTexture, 0, 0, rl.WHITE)
    rl.draw_texture_pro(
        fudesumiTexture, fudesumiRec, fudesumiPos, 
        rl.Vector2(0, 0), 0, rl.WHITE
    )
    
    rl.draw_texture_pro(
        textureRed, fudesumiRec, redPos,
        rl.Vector2(0, 0), 0, rl.RED
    )
    rl.draw_texture_pro(
        textureGreen, fudesumiRec, greenPos,
        rl.Vector2(0, 0), 0, rl.GREEN
    )
    rl.draw_texture_pro(
        textureBlue, fudesumiRec, bluePos,
        rl.Vector2(0, 0), 0, rl.BLUE
    )
    rl.draw_texture_pro(
        textureAlpha, fudesumiRec, alphaPos,
        rl.Vector2(0, 0), 0, rl.WHITE
    )
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(backgroundTexture)
rl.unload_texture(fudesumiTexture)
rl.unload_texture(textureRed)
rl.unload_texture(textureGreen)
rl.unload_texture(textureBlue)
rl.unload_texture(textureAlpha)
rl.close_window()  # Close window and OpenGL context