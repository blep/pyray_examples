"""raylib [textures] example - N-patch drawing
Example complexity rating: [★★★☆] 3/4
NOTE: Images are loaded in CPU memory (RAM); textures are loaded in GPU memory (VRAM)
Example originally created with raylib 2.0, last time updated with raylib 2.5
Example contributed by Jorge A. Gomes (@overdev) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2018-2025 Jorge A. Gomes (@overdev) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - N-patch drawing")

# NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)
nPatchTexture = rl.load_texture(str(THIS_DIR/"resources/ninepatch_button.png"))

mousePosition = rl.Vector2(0, 0)
origin = rl.Vector2(0.0, 0.0)

# Position and size of the n-patches
dstRec1 = rl.Rectangle(480.0, 160.0, 32.0, 32.0)
dstRec2 = rl.Rectangle(160.0, 160.0, 32.0, 32.0)
dstRecH = rl.Rectangle(160.0, 93.0, 32.0, 32.0)
dstRecV = rl.Rectangle(92.0, 160.0, 32.0, 32.0)

# A 9-patch (NPATCH_NINE_PATCH) changes its sizes in both axis
ninePatchInfo1 = rl.NPatchInfo(
    rl.Rectangle(0.0, 0.0, 64.0, 64.0),
    12, 40, 12, 12, 
    rl.NPATCH_NINE_PATCH
)

ninePatchInfo2 = rl.NPatchInfo(
    rl.Rectangle(0.0, 128.0, 64.0, 64.0),
    16, 16, 16, 16, 
    rl.NPATCH_NINE_PATCH
)

# A horizontal 3-patch (NPATCH_THREE_PATCH_HORIZONTAL) changes its sizes along the x axis only
h3PatchInfo = rl.NPatchInfo(
    rl.Rectangle(0.0, 64.0, 64.0, 64.0),
    8, 8, 8, 8, 
    rl.NPATCH_THREE_PATCH_HORIZONTAL
)

# A vertical 3-patch (NPATCH_THREE_PATCH_VERTICAL) changes its sizes along the y axis only
v3PatchInfo = rl.NPatchInfo(
    rl.Rectangle(0.0, 192.0, 64.0, 64.0),
    6, 6, 6, 6, 
    rl.NPATCH_THREE_PATCH_VERTICAL
)

rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    mousePosition = rl.get_mouse_position()
    
    # Resize the n-patches based on mouse position
    dstRec1.width = mousePosition.x - dstRec1.x
    dstRec1.height = mousePosition.y - dstRec1.y
    dstRec2.width = mousePosition.x - dstRec2.x
    dstRec2.height = mousePosition.y - dstRec2.y
    dstRecH.width = mousePosition.x - dstRecH.x
    dstRecV.height = mousePosition.y - dstRecV.y
    
    # Set a minimum width and/or height
    if dstRec1.width < 1.0:
        dstRec1.width = 1.0
    if dstRec1.width > 300.0:
        dstRec1.width = 300.0
    if dstRec1.height < 1.0:
        dstRec1.height = 1.0
    
    if dstRec2.width < 1.0:
        dstRec2.width = 1.0
    if dstRec2.width > 300.0:
        dstRec2.width = 300.0
    if dstRec2.height < 1.0:
        dstRec2.height = 1.0
    
    if dstRecH.width < 1.0:
        dstRecH.width = 1.0
    
    if dstRecV.height < 1.0:
        dstRecV.height = 1.0
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    # Draw the n-patches
    rl.draw_texture_n_patch(nPatchTexture, ninePatchInfo2, dstRec2, origin, 0.0, rl.WHITE)
    rl.draw_texture_n_patch(nPatchTexture, ninePatchInfo1, dstRec1, origin, 0.0, rl.WHITE)
    rl.draw_texture_n_patch(nPatchTexture, h3PatchInfo, dstRecH, origin, 0.0, rl.WHITE)
    rl.draw_texture_n_patch(nPatchTexture, v3PatchInfo, dstRecV, origin, 0.0, rl.WHITE)
    
    # Draw the source texture
    rl.draw_rectangle_lines(5, 88, 74, 266, rl.BLUE)
    rl.draw_texture(nPatchTexture, 10, 93, rl.WHITE)
    rl.draw_text("TEXTURE", 15, 360, 10, rl.DARKGRAY)
    
    rl.draw_text("Move the mouse to stretch or shrink the n-patches", 10, 20, 20, rl.DARKGRAY)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(nPatchTexture)  # Texture unloading
rl.close_window()  # Close window and OpenGL context