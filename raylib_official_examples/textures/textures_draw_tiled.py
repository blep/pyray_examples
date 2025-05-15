"""raylib [textures] example - Draw part of the texture tiled
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 3.0, last time updated with raylib 4.2
Example contributed by Vlad Adrian (@demizdor) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2020-2025 Vlad Adrian (@demizdor) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

OPT_WIDTH = 220       # Max width for the options container
MARGIN_SIZE = 8       # Size for the margins
COLOR_SIZE = 16       # Size of the color select buttons

# Draw part of a texture (defined by a rectangle) with rotation and scale tiled into dest.
def DrawTextureTiled(texture, source, dest, origin, rotation, scale, tint):
    if (texture.id <= 0) or (scale <= 0.0):
        return  # Prevent infinite loop
    
    if (source.width == 0) or (source.height == 0):
        return

    tileWidth = int(source.width * scale)
    tileHeight = int(source.height * scale)
    
    if (dest.width < tileWidth) and (dest.height < tileHeight):
        # Can fit only one tile
        rl.draw_texture_pro(
            texture, 
            rl.Rectangle(source.x, source.y, (dest.width/tileWidth)*source.width, (dest.height/tileHeight)*source.height),
            rl.Rectangle(dest.x, dest.y, dest.width, dest.height), 
            origin, rotation, tint
        )
    elif dest.width <= tileWidth:
        # Tiled vertically (one column)
        dy = 0
        while dy + tileHeight < dest.height:
            rl.draw_texture_pro(
                texture, 
                rl.Rectangle(source.x, source.y, (dest.width/tileWidth)*source.width, source.height),
                rl.Rectangle(dest.x, dest.y + dy, dest.width, tileHeight), 
                origin, rotation, tint
            )
            dy += tileHeight

        # Fit last tile
        if dy < dest.height:
            rl.draw_texture_pro(
                texture, 
                rl.Rectangle(source.x, source.y, (dest.width/tileWidth)*source.width, ((dest.height - dy)/tileHeight)*source.height),
                rl.Rectangle(dest.x, dest.y + dy, dest.width, dest.height - dy), 
                origin, rotation, tint
            )
    elif dest.height <= tileHeight:
        # Tiled horizontally (one row)
        dx = 0
        while dx + tileWidth < dest.width:
            rl.draw_texture_pro(
                texture, 
                rl.Rectangle(source.x, source.y, source.width, (dest.height/tileHeight)*source.height),
                rl.Rectangle(dest.x + dx, dest.y, tileWidth, dest.height), 
                origin, rotation, tint
            )
            dx += tileWidth

        # Fit last tile
        if dx < dest.width:
            rl.draw_texture_pro(
                texture, 
                rl.Rectangle(source.x, source.y, ((dest.width - dx)/tileWidth)*source.width, (dest.height/tileHeight)*source.height),
                rl.Rectangle(dest.x + dx, dest.y, dest.width - dx, dest.height), 
                origin, rotation, tint
            )
    else:
        # Tiled both horizontally and vertically (rows and columns)
        dx = 0
        while dx + tileWidth < dest.width:
            dy = 0
            while dy + tileHeight < dest.height:
                rl.draw_texture_pro(
                    texture, source,
                    rl.Rectangle(dest.x + dx, dest.y + dy, tileWidth, tileHeight), 
                    origin, rotation, tint
                )
                dy += tileHeight

            if dy < dest.height:
                rl.draw_texture_pro(
                    texture, 
                    rl.Rectangle(source.x, source.y, source.width, ((dest.height - dy)/tileHeight)*source.height),
                    rl.Rectangle(dest.x + dx, dest.y + dy, tileWidth, dest.height - dy), 
                    origin, rotation, tint
                )
            dx += tileWidth

        # Fit last column of tiles
        if dx < dest.width:
            dy = 0
            while dy + tileHeight < dest.height:
                rl.draw_texture_pro(
                    texture, 
                    rl.Rectangle(source.x, source.y, ((dest.width - dx)/tileWidth)*source.width, source.height),
                    rl.Rectangle(dest.x + dx, dest.y + dy, dest.width - dx, tileHeight), 
                    origin, rotation, tint
                )
                dy += tileHeight

            # Draw final tile in the bottom right corner
            if dy < dest.height:
                rl.draw_texture_pro(
                    texture, 
                    rl.Rectangle(source.x, source.y, ((dest.width - dx)/tileWidth)*source.width, ((dest.height - dy)/tileHeight)*source.height),
                    rl.Rectangle(dest.x + dx, dest.y + dy, dest.width - dx, dest.height - dy), 
                    origin, rotation, tint
                )

# Initialization
screenWidth = 800
screenHeight = 450

rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)  # Make the window resizable
rl.init_window(screenWidth, screenHeight, "raylib [textures] example - Draw part of a texture tiled")

# NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)
texPattern = rl.load_texture(str(THIS_DIR/"resources/patterns.png"))
rl.set_texture_filter(texPattern, rl.TEXTURE_FILTER_TRILINEAR)  # Makes the texture smoother when upscaled

# Coordinates for all patterns inside the texture
recPattern = [
    rl.Rectangle(3, 3, 66, 66),
    rl.Rectangle(75, 3, 100, 100),
    rl.Rectangle(3, 75, 66, 66),
    rl.Rectangle(7, 156, 50, 50),
    rl.Rectangle(85, 106, 90, 45),
    rl.Rectangle(75, 154, 100, 60)
]

# Setup colors
colors = [
    rl.BLACK, rl.MAROON, rl.ORANGE, rl.BLUE, rl.PURPLE, 
    rl.BEIGE, rl.LIME, rl.RED, rl.DARKGRAY, rl.SKYBLUE
]
MAX_COLORS = len(colors)
colorRec = []

# Calculate rectangle for each color
x, y = 0, 0
for i in range(MAX_COLORS):
    rect = rl.Rectangle(
        2.0 + MARGIN_SIZE + x,
        22.0 + 256.0 + MARGIN_SIZE + y,
        COLOR_SIZE * 2.0,
        COLOR_SIZE
    )
    colorRec.append(rect)
    
    if i == (MAX_COLORS // 2 - 1):
        x = 0
        y += COLOR_SIZE + MARGIN_SIZE
    else:
        x += (COLOR_SIZE * 2 + MARGIN_SIZE)

activePattern = 0
activeCol = 0
scale = 1.0
rotation = 0.0

rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    # Handle mouse
    if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        mouse = rl.get_mouse_position()

        # Check which pattern was clicked and set it as the active pattern
        for i in range(len(recPattern)):
            pattern_rect = rl.Rectangle(
                2 + MARGIN_SIZE + recPattern[i].x, 
                40 + MARGIN_SIZE + recPattern[i].y, 
                recPattern[i].width, 
                recPattern[i].height
            )
            if rl.check_collision_point_rec(mouse, pattern_rect):
                activePattern = i
                break

        # Check to see which color was clicked and set it as the active color
        for i in range(MAX_COLORS):
            if rl.check_collision_point_rec(mouse, colorRec[i]):
                activeCol = i
                break

    # Handle keys
    # Change scale
    if rl.is_key_pressed(rl.KEY_UP):
        scale += 0.25
    if rl.is_key_pressed(rl.KEY_DOWN):
        scale -= 0.25
    
    if scale > 10.0:
        scale = 10.0
    elif scale <= 0.0:
        scale = 0.25

    # Change rotation
    if rl.is_key_pressed(rl.KEY_LEFT):
        rotation -= 25.0
    if rl.is_key_pressed(rl.KEY_RIGHT):
        rotation += 25.0

    # Reset
    if rl.is_key_pressed(rl.KEY_SPACE):
        rotation = 0.0
        scale = 1.0

    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)

    # Draw the tiled area
    DrawTextureTiled(
        texPattern, 
        recPattern[activePattern], 
        rl.Rectangle(
            OPT_WIDTH + MARGIN_SIZE, 
            MARGIN_SIZE, 
            rl.get_screen_width() - OPT_WIDTH - 2.0 * MARGIN_SIZE, 
            rl.get_screen_height() - 2.0 * MARGIN_SIZE
        ),
        rl.Vector2(0.0, 0.0), 
        rotation, 
        scale, 
        colors[activeCol]
    )

    # Draw options
    rl.draw_rectangle(
        MARGIN_SIZE, 
        MARGIN_SIZE, 
        OPT_WIDTH - MARGIN_SIZE, 
        rl.get_screen_height() - 2 * MARGIN_SIZE, 
        rl.fade(rl.LIGHTGRAY, 0.5)
    )

    rl.draw_text("Select Pattern", 2 + MARGIN_SIZE, 30 + MARGIN_SIZE, 10, rl.BLACK)
    rl.draw_texture(texPattern, 2 + MARGIN_SIZE, 40 + MARGIN_SIZE, rl.BLACK)
    rl.draw_rectangle(
        2 + MARGIN_SIZE + int(recPattern[activePattern].x), 
        40 + MARGIN_SIZE + int(recPattern[activePattern].y), 
        int(recPattern[activePattern].width), 
        int(recPattern[activePattern].height), 
        rl.fade(rl.DARKBLUE, 0.3)
    )

    rl.draw_text("Select Color", 2 + MARGIN_SIZE, 10 + 256 + MARGIN_SIZE, 10, rl.BLACK)
    for i in range(MAX_COLORS):
        rl.draw_rectangle_rec(colorRec[i], colors[i])
        if activeCol == i:
            rl.draw_rectangle_lines_ex(colorRec[i], 3, rl.fade(rl.WHITE, 0.5))

    rl.draw_text("Scale (UP/DOWN to change)", 2 + MARGIN_SIZE, 80 + 256 + MARGIN_SIZE, 10, rl.BLACK)
    rl.draw_text(f"{scale:.2f}x", 2 + MARGIN_SIZE, 92 + 256 + MARGIN_SIZE, 20, rl.BLACK)

    rl.draw_text("Rotation (LEFT/RIGHT to change)", 2 + MARGIN_SIZE, 122 + 256 + MARGIN_SIZE, 10, rl.BLACK)
    rl.draw_text(f"{rotation:.0f} degrees", 2 + MARGIN_SIZE, 134 + 256 + MARGIN_SIZE, 20, rl.BLACK)

    rl.draw_text("Press [SPACE] to reset", 2 + MARGIN_SIZE, 164 + 256 + MARGIN_SIZE, 10, rl.DARKBLUE)

    # Draw FPS
    rl.draw_text(f"{rl.get_fps()} FPS", 2 + MARGIN_SIZE, 2 + MARGIN_SIZE, 20, rl.BLACK)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texPattern)  # Unload texture
rl.close_window()  # Close window and OpenGL context