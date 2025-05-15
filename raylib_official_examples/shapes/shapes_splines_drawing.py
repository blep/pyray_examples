"""raylib [shapes] example - splines drawing
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 5.0, last time updated with raylib 5.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

MAX_SPLINE_POINTS = 32

# Spline types
SPLINE_LINEAR = 0       # Linear
SPLINE_BASIS = 1        # B-Spline
SPLINE_CATMULLROM = 2   # Catmull-Rom
SPLINE_BEZIER = 3       # Cubic Bezier

# Cubic Bezier spline control points
# NOTE: Every segment has two control points 
class ControlPoint:
    def __init__(self, start=None, end=None):
        self.start = start if start else rl.Vector2(0, 0)
        self.end = end if end else rl.Vector2(0, 0)

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "raylib [shapes] example - splines drawing")

    # Initialize points for splines
    points = [
        rl.Vector2(50.0, 400.0),
        rl.Vector2(160.0, 220.0),
        rl.Vector2(340.0, 380.0),
        rl.Vector2(520.0, 60.0),
        rl.Vector2(710.0, 260.0)
    ]
    
    # Fill the rest of the array with zeros
    for i in range(len(points), MAX_SPLINE_POINTS):
        points.append(rl.Vector2(0, 0))
    
    # Array required for spline bezier-cubic, 
    # including control points interleaved with start-end segment points
    points_interleaved = [rl.Vector2(0, 0) for _ in range(3*(MAX_SPLINE_POINTS - 1) + 1)]
    
    point_count = 5
    selected_point = -1
    focused_point = -1
    selected_control_point = None
    focused_control_point = None
    
    # Cubic Bezier control points initialization
    control = [ControlPoint() for _ in range(MAX_SPLINE_POINTS-1)]
    for i in range(point_count - 1):
        control[i].start = rl.Vector2(points[i].x + 50, points[i].y)
        control[i].end = rl.Vector2(points[i + 1].x - 50, points[i + 1].y)

    # Spline config variables
    spline_thickness = 8.0
    spline_type_active = SPLINE_LINEAR  # 0-Linear, 1-BSpline, 2-CatmullRom, 3-Bezier
    spline_type_edit_mode = False 
    spline_helpers_active = True
    
    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # Spline points creation logic (at the end of spline)
        if rl.is_mouse_button_pressed(rl.MOUSE_RIGHT_BUTTON) and (point_count < MAX_SPLINE_POINTS):
            points[point_count] = rl.get_mouse_position()
            i = point_count - 1
            control[i].start = rl.Vector2(points[i].x + 50, points[i].y)
            control[i].end = rl.Vector2(points[i + 1].x - 50, points[i + 1].y)
            point_count += 1

        # Spline point focus and selection logic
        if (selected_point == -1) and ((spline_type_active != SPLINE_BEZIER) or (selected_control_point is None)):
            focused_point = -1
            for i in range(point_count):
                if rl.check_collision_point_circle(rl.get_mouse_position(), points[i], 8.0):
                    focused_point = i
                    break
            if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
                selected_point = focused_point
        
        # Spline point movement logic
        if selected_point >= 0:
            points[selected_point] = rl.get_mouse_position()
            if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON):
                selected_point = -1
        
        # Cubic Bezier spline control points logic
        if (spline_type_active == SPLINE_BEZIER) and (focused_point == -1):
            # Spline control point focus and selection logic
            if selected_control_point is None:
                focused_control_point = None
                for i in range(point_count - 1):
                    if rl.check_collision_point_circle(rl.get_mouse_position(), control[i].start, 6.0):
                        focused_control_point = (i, "start")
                        break
                    elif rl.check_collision_point_circle(rl.get_mouse_position(), control[i].end, 6.0):
                        focused_control_point = (i, "end")
                        break
                if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
                    selected_control_point = focused_control_point
            
            # Spline control point movement logic
            if selected_control_point is not None:
                idx, point_type = selected_control_point
                if point_type == "start":
                    control[idx].start = rl.get_mouse_position()
                else:  # "end"
                    control[idx].end = rl.get_mouse_position()
                    
                if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON):
                    selected_control_point = None
        
        # Spline selection logic
        if rl.is_key_pressed(rl.KEY_ONE):
            spline_type_active = 0
        elif rl.is_key_pressed(rl.KEY_TWO):
            spline_type_active = 1
        elif rl.is_key_pressed(rl.KEY_THREE):
            spline_type_active = 2
        elif rl.is_key_pressed(rl.KEY_FOUR):
            spline_type_active = 3

        # Clear selection when changing to a spline without control points
        if rl.is_key_pressed(rl.KEY_ONE) or rl.is_key_pressed(rl.KEY_TWO) or rl.is_key_pressed(rl.KEY_THREE):
            selected_control_point = None
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)
    
        # Convert python list of Vector2 to a format raylib C API expects
        # For this we need to copy our points to a contiguous array
        points_array = points[:point_count]
        
        if spline_type_active == SPLINE_LINEAR:
            # Draw spline: linear
            rl.draw_spline_linear(points_array, point_count, spline_thickness, rl.RED)
            
        elif spline_type_active == SPLINE_BASIS:
            # Draw spline: basis
            rl.draw_spline_basis(points_array, point_count, spline_thickness, rl.RED)
            
        elif spline_type_active == SPLINE_CATMULLROM:
            # Draw spline: catmull-rom
            rl.draw_spline_catmull_rom(points_array, point_count, spline_thickness, rl.RED)
            
        elif spline_type_active == SPLINE_BEZIER:
            # NOTE: Cubic-bezier spline requires the 2 control points of each segment to be 
            # provided interleaved with the start and end point of every segment
            for i in range(point_count - 1):
                points_interleaved[3*i] = points[i]
                points_interleaved[3*i + 1] = control[i].start
                points_interleaved[3*i + 2] = control[i].end
            
            points_interleaved[3*(point_count - 1)] = points[point_count - 1]

            # Convert to contiguous array for raylib C API
            interleaved_count = 3*(point_count - 1) + 1
            points_interleaved_array = points_interleaved[:interleaved_count]
            
            # Draw spline: cubic-bezier (with control points)
            rl.draw_spline_bezier_cubic(points_interleaved_array, interleaved_count, spline_thickness, rl.RED)

            # Draw spline control points
            for i in range(point_count - 1):
                # Every cubic bezier point have two control points
                rl.draw_circle_v(control[i].start, 6, rl.GOLD)
                rl.draw_circle_v(control[i].end, 6, rl.GOLD)
                
                # Highlight focused control point
                if focused_control_point is not None:
                    idx, point_type = focused_control_point
                    if idx == i and point_type == "start":
                        rl.draw_circle_v(control[i].start, 8, rl.GREEN)
                    elif idx == i and point_type == "end":
                        rl.draw_circle_v(control[i].end, 8, rl.GREEN)
                        
                rl.draw_line_ex(points[i], control[i].start, 1.0, rl.LIGHTGRAY)
                rl.draw_line_ex(points[i + 1], control[i].end, 1.0, rl.LIGHTGRAY)
            
                # Draw spline control lines
                rl.draw_line_v(points[i], control[i].start, rl.GRAY)
                rl.draw_line_v(control[i].end, points[i + 1], rl.GRAY)

        if spline_helpers_active:
            # Draw spline point helpers
            for i in range(point_count):
                rl.draw_circle_lines_v(points[i], 12.0 if focused_point == i else 8.0, 
                                     rl.BLUE if focused_point == i else rl.DARKBLUE)
                                     
                if ((spline_type_active != SPLINE_LINEAR) and
                    (spline_type_active != SPLINE_BEZIER) and
                    (i < point_count - 1)):
                    rl.draw_line_v(points[i], points[i + 1], rl.GRAY)

                rl.draw_text(f"[{int(points[i].x)}, {int(points[i].y)}]", int(points[i].x), int(points[i].y) + 10, 10, rl.BLACK)        # Check all possible UI states that require controls lock
        if spline_type_edit_mode or (selected_point != -1) or (selected_control_point is not None):
            rl.gui_lock()
            
        # Draw spline config
        spline_thickness_ptr = rl.ffi.new('float *', spline_thickness)
        rl.gui_label(rl.Rectangle(12, 62, 140, 24), f"Spline thickness: {int(spline_thickness_ptr[0])}")
        rl.gui_slider_bar(rl.Rectangle(12, 60 + 24, 140, 16), "", "", spline_thickness_ptr, 1.0, 40.0)
        spline_thickness = spline_thickness_ptr[0]

        spline_helpers_active_ptr = rl.ffi.new('bool *', spline_helpers_active)
        rl.gui_check_box(rl.Rectangle(12, 110, 20, 20), "Show point helpers", spline_helpers_active_ptr)
        spline_helpers_active = spline_helpers_active_ptr[0]

        if spline_type_edit_mode:
            rl.gui_unlock()
            rl.gui_label(rl.Rectangle(12, 10, 140, 24), "Spline type:")
        spline_type_active_ptr = rl.ffi.new('int *', spline_type_active)
        spline_type_edit_mode_ptr = rl.ffi.new('int *', spline_type_edit_mode)
        if rl.gui_dropdown_box(rl.Rectangle(12, 8 + 24, 140, 28), "LINEAR;BSPLINE;CATMULLROM;BEZIER", spline_type_active_ptr, spline_type_edit_mode_ptr[0]):
            spline_type_edit_mode = not spline_type_edit_mode
            spline_type_active = spline_type_active_ptr[0]

        rl.gui_unlock()

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()