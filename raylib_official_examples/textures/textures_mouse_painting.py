"""raylib [textures] example - Mouse painting
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 3.0, last time updated with raylib 3.0
Example contributed by Chris Dill (@MysteriousSpace) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Chris Dill (@MysteriousSpace) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

MAX_COLORS_COUNT = 23          # Number of colors available

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - mouse painting")

# Colors to choose from
colors = [
    rl.RAYWHITE, rl.YELLOW, rl.GOLD, rl.ORANGE, rl.PINK, rl.RED, rl.MAROON, 
    rl.GREEN, rl.LIME, rl.DARKGREEN, rl.SKYBLUE, rl.BLUE, rl.DARKBLUE, 
    rl.PURPLE, rl.VIOLET, rl.DARKPURPLE, rl.BEIGE, rl.BROWN, rl.DARKBROWN,
    rl.LIGHTGRAY, rl.GRAY, rl.DARKGRAY, rl.BLACK
]

# Define colorsRecs data (for every rectangle)
colorsRecs = []

for i in range(MAX_COLORS_COUNT):
    rect = rl.Rectangle(10 + 30.0*i + 2*i, 10, 30, 30)
    colorsRecs.append(rect)

colorSelected = 0
colorSelectedPrev = colorSelected
colorMouseHover = 0
brushSize = 20.0
mouseWasPressed = False

btnSaveRec = rl.Rectangle(750, 10, 40, 30)
btnSaveMouseHover = False
showSaveMessage = False
saveMessageCounter = 0

# Create a RenderTexture2D to use as a canvas
target = rl.load_render_texture(screenWidth, screenHeight)

# Clear render texture before entering the game loop
rl.begin_texture_mode(target)
rl.clear_background(colors[0])
rl.end_texture_mode()

rl.set_target_fps(120)  # Set our game to run at 120 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    mousePos = rl.get_mouse_position()
    
    # Move between colors with keys
    if rl.is_key_pressed(rl.KEY_RIGHT):
        colorSelected += 1
    elif rl.is_key_pressed(rl.KEY_LEFT):
        colorSelected -= 1
    
    if colorSelected >= MAX_COLORS_COUNT:
        colorSelected = MAX_COLORS_COUNT - 1
    elif colorSelected < 0:
        colorSelected = 0
    
    # Choose color with mouse
    colorMouseHover = -1
    for i in range(MAX_COLORS_COUNT):
        if rl.check_collision_point_rec(mousePos, colorsRecs[i]):
            colorMouseHover = i
            break
    
    if (colorMouseHover >= 0) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        colorSelected = colorMouseHover
        colorSelectedPrev = colorSelected
    
    # Change brush size
    brushSize += rl.get_mouse_wheel_move() * 5
    if brushSize < 2:
        brushSize = 2
    if brushSize > 50:
        brushSize = 50
    
    if rl.is_key_pressed(rl.KEY_C):
        # Clear render texture to clear color
        rl.begin_texture_mode(target)
        rl.clear_background(colors[0])
        rl.end_texture_mode()
    
    if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT) or (rl.get_gesture_detected() == rl.GESTURE_DRAG):
        # Paint circle into render texture
        # NOTE: To avoid discontinuous circles, we could store
        # previous-next mouse points and just draw a line using brush size
        rl.begin_texture_mode(target)
        if mousePos.y > 50:
            rl.draw_circle(int(mousePos.x), int(mousePos.y), brushSize, colors[colorSelected])
        rl.end_texture_mode()
    
    if rl.is_mouse_button_down(rl.MOUSE_BUTTON_RIGHT):
        if not mouseWasPressed:
            colorSelectedPrev = colorSelected
            colorSelected = 0
        
        mouseWasPressed = True
        
        # Erase circle from render texture
        rl.begin_texture_mode(target)
        if mousePos.y > 50:
            rl.draw_circle(int(mousePos.x), int(mousePos.y), brushSize, colors[0])
        rl.end_texture_mode()
    elif rl.is_mouse_button_released(rl.MOUSE_BUTTON_RIGHT) and mouseWasPressed:
        colorSelected = colorSelectedPrev
        mouseWasPressed = False
    
    # Check mouse hover save button
    if rl.check_collision_point_rec(mousePos, btnSaveRec):
        btnSaveMouseHover = True
    else:
        btnSaveMouseHover = False
    
    # Image saving logic
    # NOTE: Saving painted texture to a default named image
    if (btnSaveMouseHover and rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT)) or rl.is_key_pressed(rl.KEY_S):
        image = rl.load_image_from_texture(target.texture)
        rl.image_flip_vertical(image)
        rl.export_image(image, "my_amazing_texture_painting.png")
        rl.unload_image(image)
        showSaveMessage = True
    
    if showSaveMessage:
        # On saving, show a full screen message for 2 seconds
        saveMessageCounter += 1
        if saveMessageCounter > 240:
            showSaveMessage = False
            saveMessageCounter = 0
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    # NOTE: Render texture must be y-flipped due to default OpenGL coordinates (left-bottom)
    rl.draw_texture_rec(
        target.texture,
        rl.Rectangle(0, 0, target.texture.width, -target.texture.height),
        rl.Vector2(0, 0),
        rl.WHITE
    )
    
    # Draw drawing circle for reference
    if mousePos.y > 50:
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_RIGHT):
            rl.draw_circle_lines(int(mousePos.x), int(mousePos.y), brushSize, rl.GRAY)
        else:
            rl.draw_circle(rl.get_mouse_x(), rl.get_mouse_y(), brushSize, colors[colorSelected])
    
    # Draw top panel
    rl.draw_rectangle(0, 0, rl.get_screen_width(), 50, rl.RAYWHITE)
    rl.draw_line(0, 50, rl.get_screen_width(), 50, rl.LIGHTGRAY)
    
    # Draw color selection rectangles
    for i in range(MAX_COLORS_COUNT):
        rl.draw_rectangle_rec(colorsRecs[i], colors[i])
    rl.draw_rectangle_lines(10, 10, 30, 30, rl.LIGHTGRAY)
    
    if colorMouseHover >= 0:
        rl.draw_rectangle_rec(colorsRecs[colorMouseHover], rl.fade(rl.WHITE, 0.6))
    
    rl.draw_rectangle_lines_ex(
        rl.Rectangle(
            colorsRecs[colorSelected].x - 2,
            colorsRecs[colorSelected].y - 2,
            colorsRecs[colorSelected].width + 4,
            colorsRecs[colorSelected].height + 4
        ),
        2,
        rl.BLACK
    )
    
    # Draw save image button
    rl.draw_rectangle_lines_ex(btnSaveRec, 2, rl.RED if btnSaveMouseHover else rl.BLACK)
    rl.draw_text("SAVE!", 755, 20, 10, rl.RED if btnSaveMouseHover else rl.BLACK)
    
    # Draw save image message
    if showSaveMessage:
        rl.draw_rectangle(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.fade(rl.RAYWHITE, 0.8))
        rl.draw_rectangle(0, 150, rl.get_screen_width(), 80, rl.BLACK)
        rl.draw_text("IMAGE SAVED:  my_amazing_texture_painting.png", 150, 180, 20, rl.RAYWHITE)
    
    rl.end_drawing()

# De-Initialization
rl.unload_render_texture(target)  # Unload render texture
rl.close_window()  # Close window and OpenGL context