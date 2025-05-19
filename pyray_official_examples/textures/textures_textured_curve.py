"""raylib [textures] example - Draw a texture along a segmented curve
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example contributed by Jeffery Myers (@JeffM2501) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2022-2025 Jeffery Myers (@JeffM2501) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import math

THIS_DIR = Path(__file__).resolve().parent

# Global Variables Definition
texRoad = None
showCurve = False
curveWidth = 50
curveSegments = 24

curveStartPosition = rl.Vector2(0, 0)
curveStartPositionTangent = rl.Vector2(0, 0)
curveEndPosition = rl.Vector2(0, 0)
curveEndPositionTangent = rl.Vector2(0, 0)

curveSelectedPoint = None

# Draw textured curve using Spline Cubic Bezier
def draw_textured_curve():
    global curveStartPosition, curveStartPositionTangent, curveEndPosition, curveEndPositionTangent
    global curveSegments, curveWidth, texRoad
    
    step = 1.0/curveSegments
    
    previous = rl.Vector2(curveStartPosition.x, curveStartPosition.y)
    previousTangent = rl.Vector2(0, 0)
    previousV = 0
    
    # We can't compute a tangent for the first point, so we need to reuse the tangent from the first segment
    tangentSet = False
    
    current = rl.Vector2(0, 0)
    
    for i in range(1, curveSegments + 1):
        t = step * i
        
        a = math.pow(1.0 - t, 3)
        b = 3.0 * math.pow(1.0 - t, 2) * t
        c = 3.0 * (1.0 - t) * math.pow(t, 2)
        d = math.pow(t, 3)
        
        # Compute the endpoint for this segment
        current.y = a * curveStartPosition.y + b * curveStartPositionTangent.y + c * curveEndPositionTangent.y + d * curveEndPosition.y
        current.x = a * curveStartPosition.x + b * curveStartPositionTangent.x + c * curveEndPositionTangent.x + d * curveEndPosition.x
        
        # Vector from previous to current
        delta = rl.Vector2(current.x - previous.x, current.y - previous.y)
        
        # The right hand normal to the delta vector
        normal = rl.vector2_normalize(rl.Vector2(-delta.y, delta.x))
        
        # The v texture coordinate of the segment (add up the length of all the segments so far)
        v = previousV + rl.vector2_length(delta)
        
        # Make sure the start point has a normal
        if not tangentSet:
            previousTangent = rl.Vector2(normal.x, normal.y)
            tangentSet = True
        
        # Extend out the normals from the previous and current points to get the quad for this segment
        prevPosNormal = rl.vector2_add(previous, rl.vector2_scale(previousTangent, curveWidth))
        prevNegNormal = rl.vector2_add(previous, rl.vector2_scale(previousTangent, -curveWidth))
        
        currentPosNormal = rl.vector2_add(current, rl.vector2_scale(normal, curveWidth))
        currentNegNormal = rl.vector2_add(current, rl.vector2_scale(normal, -curveWidth))
        
        # Draw the segment as a quad
        rl.rl_set_texture(texRoad.id)
        rl.rl_begin(rl.RL_QUADS)
        rl.rl_color4ub(255, 255, 255, 255)
        rl.rl_normal3f(0.0, 0.0, 1.0)
        
        rl.rl_tex_coord2f(0, previousV)
        rl.rl_vertex2f(prevNegNormal.x, prevNegNormal.y)
        
        rl.rl_tex_coord2f(1, previousV)
        rl.rl_vertex2f(prevPosNormal.x, prevPosNormal.y)
        
        rl.rl_tex_coord2f(1, v)
        rl.rl_vertex2f(currentPosNormal.x, currentPosNormal.y)
        
        rl.rl_tex_coord2f(0, v)
        rl.rl_vertex2f(currentNegNormal.x, currentNegNormal.y)
        rl.rl_end()
        
        # The current step is the start of the next step
        previous = rl.Vector2(current.x, current.y)
        previousTangent = rl.Vector2(normal.x, normal.y)
        previousV = v

# Initialization
screenWidth = 800
screenHeight = 450

rl.set_config_flags(rl.FLAG_VSYNC_HINT | rl.FLAG_MSAA_4X_HINT)
rl.init_window(screenWidth, screenHeight, "raylib [textures] examples - textured curve")

# Load the road texture
texRoad = rl.load_texture(str(THIS_DIR/"resources/road.png"))
rl.set_texture_filter(texRoad, rl.TEXTURE_FILTER_BILINEAR)

# Setup the curve
curveStartPosition = rl.Vector2(80, 100)
curveStartPositionTangent = rl.Vector2(100, 300)

curveEndPosition = rl.Vector2(700, 350)
curveEndPositionTangent = rl.Vector2(600, 100)

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    # Curve config options
    if rl.is_key_pressed(rl.KEY_SPACE):
        showCurve = not showCurve
    if rl.is_key_pressed(rl.KEY_EQUAL):
        curveWidth += 2
    if rl.is_key_pressed(rl.KEY_MINUS):
        curveWidth -= 2
    if curveWidth < 2:
        curveWidth = 2

    # Update segments
    if rl.is_key_pressed(rl.KEY_LEFT):
        curveSegments -= 2
    if rl.is_key_pressed(rl.KEY_RIGHT):
        curveSegments += 2

    if curveSegments < 2:
        curveSegments = 2

    # Update curve logic
    # If the mouse is not down, we are not editing the curve so clear the selection
    if not rl.is_mouse_button_down(rl.MOUSE_LEFT_BUTTON):
        curveSelectedPoint = None

    # If a point was selected, move it
    if curveSelectedPoint is not None:
        delta = rl.get_mouse_delta()
        curveSelectedPoint.x += delta.x
        curveSelectedPoint.y += delta.y

    # The mouse is down, and nothing was selected, so see if anything was picked
    if rl.is_mouse_button_down(rl.MOUSE_LEFT_BUTTON) and curveSelectedPoint is None:
        mouse = rl.get_mouse_position()
        if rl.check_collision_point_circle(mouse, curveStartPosition, 6):
            curveSelectedPoint = curveStartPosition
        elif rl.check_collision_point_circle(mouse, curveStartPositionTangent, 6):
            curveSelectedPoint = curveStartPositionTangent
        elif rl.check_collision_point_circle(mouse, curveEndPosition, 6):
            curveSelectedPoint = curveEndPosition
        elif rl.check_collision_point_circle(mouse, curveEndPositionTangent, 6):
            curveSelectedPoint = curveEndPositionTangent

    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    draw_textured_curve()  # Draw a textured Spline Cubic Bezier
    
    # Draw spline for reference
    if showCurve:
        rl.draw_spline_segment_bezier_cubic(
            curveStartPosition, curveEndPosition,
            curveStartPositionTangent, curveEndPositionTangent,
            2, rl.BLUE
        )
    
    # Draw the various control points and highlight where the mouse is
    rl.draw_line_v(curveStartPosition, curveStartPositionTangent, rl.SKYBLUE)
    rl.draw_line_v(curveStartPositionTangent, curveEndPositionTangent, rl.fade(rl.LIGHTGRAY, 0.4))
    rl.draw_line_v(curveEndPosition, curveEndPositionTangent, rl.PURPLE)
    
    mouse = rl.get_mouse_position()
    
    if rl.check_collision_point_circle(mouse, curveStartPosition, 6):
        rl.draw_circle_v(curveStartPosition, 7, rl.YELLOW)
    rl.draw_circle_v(curveStartPosition, 5, rl.RED)
    
    if rl.check_collision_point_circle(mouse, curveStartPositionTangent, 6):
        rl.draw_circle_v(curveStartPositionTangent, 7, rl.YELLOW)
    rl.draw_circle_v(curveStartPositionTangent, 5, rl.MAROON)
    
    if rl.check_collision_point_circle(mouse, curveEndPosition, 6):
        rl.draw_circle_v(curveEndPosition, 7, rl.YELLOW)
    rl.draw_circle_v(curveEndPosition, 5, rl.GREEN)
    
    if rl.check_collision_point_circle(mouse, curveEndPositionTangent, 6):
        rl.draw_circle_v(curveEndPositionTangent, 7, rl.YELLOW)
    rl.draw_circle_v(curveEndPositionTangent, 5, rl.DARKGREEN)
    
    # Draw usage info
    rl.draw_text("Drag points to move curve, press SPACE to show/hide base curve", 10, 10, 10, rl.DARKGRAY)
    rl.draw_text(f"Curve width: {int(curveWidth)} (Use + and - to adjust)", 10, 30, 10, rl.DARKGRAY)
    rl.draw_text(f"Curve segments: {curveSegments} (Use LEFT and RIGHT to adjust)", 10, 50, 10, rl.DARKGRAY)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texRoad)
rl.close_window()  # Close window and OpenGL context