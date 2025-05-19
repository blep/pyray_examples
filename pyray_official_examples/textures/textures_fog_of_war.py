"""raylib [textures] example - Fog of war
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 4.2, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2018-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import ctypes

THIS_DIR = Path(__file__).resolve().parent

MAP_TILE_SIZE = 32         # Tiles size 32x32 pixels
PLAYER_SIZE = 16           # Player size
PLAYER_TILE_VISIBILITY = 2  # Player can see 2 tiles around its position

# Map data type
class Map:
    def __init__(self, tiles_x, tiles_y):
        self.tilesX = tiles_x
        self.tilesY = tiles_y
        # Initialize arrays of unsigned chars (bytes)
        self.tileIds = bytearray(tiles_x * tiles_y)
        self.tileFog = bytearray(tiles_x * tiles_y)

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - fog of war")

# Initialize map
map_data = Map(25, 15)

# Load map tiles (generating 2 random tile ids for testing)
# NOTE: Map tile ids should be probably loaded from an external map file
for i in range(map_data.tilesY * map_data.tilesX):
    map_data.tileIds[i] = rl.get_random_value(0, 1)

# Player position on the screen (pixel coordinates, not tile coordinates)
playerPosition = rl.Vector2(180, 130)
playerTileX = 0
playerTileY = 0

# Render texture to render fog of war
# NOTE: To get an automatic smooth-fog effect we use a render texture to render fog
# at a smaller size (one pixel per tile) and scale it on drawing with bilinear filtering
fogOfWar = rl.load_render_texture(map_data.tilesX, map_data.tilesY)
rl.set_texture_filter(fogOfWar.texture, rl.TEXTURE_FILTER_BILINEAR)

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    # Move player around
    if rl.is_key_down(rl.KEY_RIGHT):
        playerPosition.x += 5
    if rl.is_key_down(rl.KEY_LEFT):
        playerPosition.x -= 5
    if rl.is_key_down(rl.KEY_DOWN):
        playerPosition.y += 5
    if rl.is_key_down(rl.KEY_UP):
        playerPosition.y -= 5

    # Check player position to avoid moving outside tilemap limits
    if playerPosition.x < 0:
        playerPosition.x = 0
    elif (playerPosition.x + PLAYER_SIZE) > (map_data.tilesX * MAP_TILE_SIZE):
        playerPosition.x = map_data.tilesX * MAP_TILE_SIZE - PLAYER_SIZE
    
    if playerPosition.y < 0:
        playerPosition.y = 0
    elif (playerPosition.y + PLAYER_SIZE) > (map_data.tilesY * MAP_TILE_SIZE):
        playerPosition.y = map_data.tilesY * MAP_TILE_SIZE - PLAYER_SIZE

    # Previous visited tiles are set to partial fog
    for i in range(map_data.tilesX * map_data.tilesY):
        if map_data.tileFog[i] == 1:
            map_data.tileFog[i] = 2

    # Get current tile position from player pixel position
    playerTileX = int((playerPosition.x + MAP_TILE_SIZE/2) / MAP_TILE_SIZE)
    playerTileY = int((playerPosition.y + MAP_TILE_SIZE/2) / MAP_TILE_SIZE)

    # Check visibility and update fog
    # NOTE: We check tilemap limits to avoid processing tiles out-of-array-bounds (it could crash program)
    for y in range(playerTileY - PLAYER_TILE_VISIBILITY, playerTileY + PLAYER_TILE_VISIBILITY):
        for x in range(playerTileX - PLAYER_TILE_VISIBILITY, playerTileX + PLAYER_TILE_VISIBILITY):
            if (x >= 0) and (x < map_data.tilesX) and (y >= 0) and (y < map_data.tilesY):
                map_data.tileFog[y * map_data.tilesX + x] = 1

    # Draw
    # Draw fog of war to a small render texture for automatic smoothing on scaling
    rl.begin_texture_mode(fogOfWar)
    rl.clear_background(rl.BLANK)
    
    for y in range(map_data.tilesY):
        for x in range(map_data.tilesX):
            if map_data.tileFog[y * map_data.tilesX + x] == 0:
                rl.draw_rectangle(x, y, 1, 1, rl.BLACK)
            elif map_data.tileFog[y * map_data.tilesX + x] == 2:
                rl.draw_rectangle(x, y, 1, 1, rl.fade(rl.BLACK, 0.8))
    
    rl.end_texture_mode()

    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)

    for y in range(map_data.tilesY):
        for x in range(map_data.tilesX):
            # Draw tiles from id (and tile borders)
            if map_data.tileIds[y * map_data.tilesX + x] == 0:
                tile_color = rl.BLUE
            else:
                tile_color = rl.fade(rl.BLUE, 0.9)
                
            rl.draw_rectangle(
                x * MAP_TILE_SIZE, 
                y * MAP_TILE_SIZE, 
                MAP_TILE_SIZE, 
                MAP_TILE_SIZE, 
                tile_color
            )
            
            rl.draw_rectangle_lines(
                x * MAP_TILE_SIZE, 
                y * MAP_TILE_SIZE, 
                MAP_TILE_SIZE, 
                MAP_TILE_SIZE, 
                rl.fade(rl.DARKBLUE, 0.5)
            )

    # Draw player
    rl.draw_rectangle_v(playerPosition, rl.Vector2(PLAYER_SIZE, PLAYER_SIZE), rl.RED)

    # Draw fog of war (scaled to full map, bilinear filtering)
    rl.draw_texture_pro(
        fogOfWar.texture, 
        rl.Rectangle(0, 0, fogOfWar.texture.width, -fogOfWar.texture.height),
        rl.Rectangle(0, 0, map_data.tilesX * MAP_TILE_SIZE, map_data.tilesY * MAP_TILE_SIZE),
        rl.Vector2(0, 0), 
        0.0, 
        rl.WHITE
    )

    # Draw player current tile
    rl.draw_text(f"Current tile: [{playerTileX},{playerTileY}]", 10, 10, 20, rl.RAYWHITE)
    rl.draw_text("ARROW KEYS to move", 10, screenHeight - 25, 20, rl.RAYWHITE)

    rl.end_drawing()

# De-Initialization
rl.unload_render_texture(fogOfWar)  # Unload render texture
rl.close_window()  # Close window and OpenGL context