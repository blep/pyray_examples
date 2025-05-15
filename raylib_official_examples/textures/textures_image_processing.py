"""raylib [textures] example - Image processing
Example complexity rating: [★★★☆] 3/4
NOTE: Images are loaded in CPU memory (RAM); textures are loaded in GPU memory (VRAM)
Example originally created with raylib 1.4, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2016-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
from enum import IntEnum

THIS_DIR = Path(__file__).resolve().parent

NUM_PROCESSES = 9

# Define image processing options as an enum
class ImageProcess(IntEnum):
    NONE = 0
    COLOR_GRAYSCALE = 1
    COLOR_TINT = 2
    COLOR_INVERT = 3
    COLOR_CONTRAST = 4
    COLOR_BRIGHTNESS = 5
    GAUSSIAN_BLUR = 6
    FLIP_VERTICAL = 7
    FLIP_HORIZONTAL = 8

# Text descriptions for each process
processText = [
    "NO PROCESSING",
    "COLOR GRAYSCALE",
    "COLOR TINT",
    "COLOR INVERT",
    "COLOR CONTRAST",
    "COLOR BRIGHTNESS",
    "GAUSSIAN BLUR",
    "FLIP VERTICAL",
    "FLIP HORIZONTAL"
]

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - image processing")

# NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)
imOrigin = rl.load_image(str(THIS_DIR/"resources/parrots.png"))   # Loaded in CPU memory (RAM)
rl.image_format(imOrigin, rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)   # Format image to RGBA 32bit (required for texture update)
texture = rl.load_texture_from_image(imOrigin)    # Image converted to texture, GPU memory (VRAM)

imCopy = rl.image_copy(imOrigin)

currentProcess = ImageProcess.NONE
textureReload = False

toggleRecs = []
for i in range(NUM_PROCESSES):
    toggleRecs.append(rl.Rectangle(40.0, 50 + 32.0 * i, 150.0, 30.0))

mouseHoverRec = -1

rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    # Mouse toggle group logic
    for i in range(NUM_PROCESSES):
        if rl.check_collision_point_rec(rl.get_mouse_position(), toggleRecs[i]):
            mouseHoverRec = i

            if rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT):
                currentProcess = i
                textureReload = True
            break
        else:
            mouseHoverRec = -1

    # Keyboard toggle group logic
    if rl.is_key_pressed(rl.KEY_DOWN):
        currentProcess += 1
        if currentProcess > (NUM_PROCESSES - 1):
            currentProcess = 0
        textureReload = True
    elif rl.is_key_pressed(rl.KEY_UP):
        currentProcess -= 1
        if currentProcess < 0:
            currentProcess = NUM_PROCESSES - 1
        textureReload = True

    # Reload texture when required
    if textureReload:
        rl.unload_image(imCopy)           # Unload image-copy data
        imCopy = rl.image_copy(imOrigin)  # Restore image-copy from image-origin

        # NOTE: Image processing is a costly CPU process to be done every frame,
        # If image processing is required in a frame-basis, it should be done
        # with a texture and by shaders
        if currentProcess == ImageProcess.COLOR_GRAYSCALE:
            rl.image_color_grayscale(imCopy)
        elif currentProcess == ImageProcess.COLOR_TINT:
            rl.image_color_tint(imCopy, rl.GREEN)
        elif currentProcess == ImageProcess.COLOR_INVERT:
            rl.image_color_invert(imCopy)
        elif currentProcess == ImageProcess.COLOR_CONTRAST:
            rl.image_color_contrast(imCopy, -40)
        elif currentProcess == ImageProcess.COLOR_BRIGHTNESS:
            rl.image_color_brightness(imCopy, -80)
        elif currentProcess == ImageProcess.GAUSSIAN_BLUR:
            rl.image_blur_gaussian(imCopy, 10)
        elif currentProcess == ImageProcess.FLIP_VERTICAL:
            rl.image_flip_vertical(imCopy)
        elif currentProcess == ImageProcess.FLIP_HORIZONTAL:
            rl.image_flip_horizontal(imCopy)

        pixels = rl.load_image_colors(imCopy)    # Load pixel data from image (RGBA 32bit)
        rl.update_texture(texture, pixels)       # Update texture with new image data
        rl.unload_image_colors(pixels)           # Unload pixels data from RAM

        textureReload = False

    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_text("IMAGE PROCESSING:", 40, 30, 10, rl.DARKGRAY)

    # Draw rectangles
    for i in range(NUM_PROCESSES):
        if (i == currentProcess) or (i == mouseHoverRec):
            rect_color = rl.SKYBLUE
            lines_color = rl.BLUE
            text_color = rl.DARKBLUE
        else:
            rect_color = rl.LIGHTGRAY
            lines_color = rl.GRAY
            text_color = rl.DARKGRAY
            
        rl.draw_rectangle_rec(toggleRecs[i], rect_color)
        rl.draw_rectangle_lines(
            int(toggleRecs[i].x), 
            int(toggleRecs[i].y), 
            int(toggleRecs[i].width), 
            int(toggleRecs[i].height), 
            lines_color
        )
        
        text_width = rl.measure_text(processText[i], 10)
        text_x = int(toggleRecs[i].x + toggleRecs[i].width/2 - text_width/2)
        text_y = int(toggleRecs[i].y + 11)
        
        rl.draw_text(processText[i], text_x, text_y, 10, text_color)

    # Draw the processed image
    rl.draw_texture(
        texture, 
        screenWidth - texture.width - 60, 
        screenHeight//2 - texture.height//2, 
        rl.WHITE
    )
    
    rl.draw_rectangle_lines(
        screenWidth - texture.width - 60, 
        screenHeight//2 - texture.height//2, 
        texture.width, 
        texture.height, 
        rl.BLACK
    )
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texture)    # Unload texture from VRAM
rl.unload_image(imOrigin)     # Unload image-origin from RAM
rl.unload_image(imCopy)       # Unload image-copy from RAM

rl.close_window()             # Close window and OpenGL context