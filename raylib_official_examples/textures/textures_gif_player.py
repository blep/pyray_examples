"""raylib [textures] example - gif playing
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 4.2, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import ctypes
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

MAX_FRAME_DELAY = 20
MIN_FRAME_DELAY = 1

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - gif playing")

# Create a pointer to store the number of animation frames
animFrames = rl.ffi.new("int *", 0)

# Load all GIF animation frames into a single Image
# NOTE: GIF data is always loaded as RGBA (32bit) by default
# NOTE: Frames are just appended one after another in image.data memory
imScarfyAnim = rl.load_image_anim(str(THIS_DIR/"resources/scarfy_run.gif"), animFrames)

# Extract the value from the pointer
animFrames_value = animFrames[0]

# Load texture from image
# NOTE: We will update this texture when required with next frame data
# WARNING: It's not recommended to use this technique for sprites animation,
# use spritesheets instead, like illustrated in textures_sprite_anim example
texScarfyAnim = rl.load_texture_from_image(imScarfyAnim)

nextFrameDataOffset = 0  # Current byte offset to next frame in image.data

currentAnimFrame = 0    # Current animation frame to load and draw
frameDelay = 8          # Frame delay to switch between animation frames
frameCounter = 0        # General frames counter

rl.set_target_fps(60)   # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    frameCounter += 1
    if frameCounter >= frameDelay:
        # Move to next frame
        # NOTE: If final frame is reached we return to first frame
        currentAnimFrame += 1
        if currentAnimFrame >= animFrames_value:
            currentAnimFrame = 0
        
        # Get memory offset position for next frame data in image.data
        nextFrameDataOffset = imScarfyAnim.width * imScarfyAnim.height * 4 * currentAnimFrame
        
        # Update GPU texture data with next frame image data
        # WARNING: Data size (frame size) and pixel format must match already created texture
        # We need to get a pointer to the image data, offset by the nextFrameDataOffset
        data_ptr = rl.ffi.cast("unsigned char *", imScarfyAnim.data)
        offset_ptr = rl.ffi.cast("void *", data_ptr + nextFrameDataOffset)
        rl.update_texture(texScarfyAnim, offset_ptr)
        
        frameCounter = 0
    
    # Control frames delay
    if rl.is_key_pressed(rl.KEY_RIGHT):
        frameDelay += 1
    elif rl.is_key_pressed(rl.KEY_LEFT):
        frameDelay -= 1
    
    if frameDelay > MAX_FRAME_DELAY:
        frameDelay = MAX_FRAME_DELAY
    elif frameDelay < MIN_FRAME_DELAY:
        frameDelay = MIN_FRAME_DELAY
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_text(f"TOTAL GIF FRAMES:  {animFrames_value:02d}", 50, 30, 20, rl.LIGHTGRAY)
    rl.draw_text(f"CURRENT FRAME: {currentAnimFrame:02d}", 50, 60, 20, rl.GRAY)
    rl.draw_text(f"CURRENT FRAME IMAGE.DATA OFFSET: {nextFrameDataOffset}", 50, 90, 20, rl.GRAY)
    
    rl.draw_text("FRAMES DELAY: ", 100, 305, 10, rl.DARKGRAY)
    rl.draw_text(f"{frameDelay:02d} frames", 620, 305, 10, rl.DARKGRAY)
    rl.draw_text("PRESS RIGHT/LEFT KEYS to CHANGE SPEED!", 290, 350, 10, rl.DARKGRAY)
    
    for i in range(MAX_FRAME_DELAY):
        if i < frameDelay:
            rl.draw_rectangle(190 + 21*i, 300, 20, 20, rl.RED)
        rl.draw_rectangle_lines(190 + 21*i, 300, 20, 20, rl.MAROON)
    
    rl.draw_texture(texScarfyAnim, rl.get_screen_width()//2 - texScarfyAnim.width//2, 140, rl.WHITE)
    
    rl.draw_text("(c) Scarfy sprite by Eiden Marsal", screenWidth - 200, screenHeight - 20, 10, rl.GRAY)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texScarfyAnim)  # Unload texture
rl.unload_image(imScarfyAnim)     # Unload image (contains all frames)
rl.close_window()                 # Close window and OpenGL context