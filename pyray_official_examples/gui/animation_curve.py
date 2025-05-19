"""Animation curves - An example demo for animation curves
DEPENDENCIES:
    raylib 4.0  - Windowing/input management and drawing.
    raygui 3.0  - Immediate-mode GUI controls.
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99
LICENSE: zlib/libpng
Copyright (c) 2023 Pierre Jaffuer (@smallcluster)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Define a simplified Curve class to replace the C implementation
class CurvePoint:
    def __init__(self, x, y, tangent_left=0.0, tangent_right=0.0):
        self.position = rl.Vector2(x, y)
        self.tangent_left = tangent_left
        self.tangent_right = tangent_right

class AnimationCurve:
    def __init__(self, start_value=0.0, end_value=1.0):
        self.start_value = start_value
        self.end_value = end_value
        self.points = []
        self.selected_index = -1
    
    def add_point(self, x, y, tangent_left=0.0, tangent_right=0.0):
        self.points.append(CurvePoint(x, y, tangent_left, tangent_right))
        self.sort_points()
    
    def sort_points(self):
        self.points.sort(key=lambda p: p.position.x)
    
    def evaluate(self, t):
        """Simplified curve evaluation using linear interpolation"""
        # Handle edge cases
        if not self.points:
            return self.start_value + (self.end_value - self.start_value) * t
        
        if t <= 0.0:
            return self.start_value + self.points[0].position.y * (self.end_value - self.start_value)
            
        if t >= 1.0:
            return self.start_value + self.points[-1].position.y * (self.end_value - self.start_value)
        
        # Find the two points to interpolate between
        p1 = None
        p2 = None
        
        for i in range(len(self.points)):
            if self.points[i].position.x > t:
                if i > 0:
                    p1 = self.points[i-1]
                    p2 = self.points[i]
                else:
                    p1 = CurvePoint(0.0, self.points[0].position.y)
                    p2 = self.points[i]
                break
        
        # If we reached the end without finding p2, use the last point
        if p2 is None:
            p1 = self.points[-1]
            p2 = CurvePoint(1.0, p1.position.y)
        
        # Simple linear interpolation
        t_segment = (t - p1.position.x) / (p2.position.x - p1.position.x) if p2.position.x != p1.position.x else 0
        y = p1.position.y + t_segment * (p2.position.y - p1.position.y)
        
        return self.start_value + y * (self.end_value - self.start_value)
    
    def draw(self, bounds, color=rl.RED):
        """Draw the curve in the given bounds"""
        # Draw background
        rl.draw_rectangle_rec(bounds, rl.get_color(rl.get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))
        rl.draw_rectangle_lines_ex(bounds, 1, rl.get_color(rl.get_style(rl.DEFAULT, rl.BORDER_COLOR)))
        
        # Draw grid
        grid_color = rl.ColorAlpha(rl.get_color(rl.get_style(rl.DEFAULT, rl.LINE_COLOR)), 0.15)
        for i in range(1, 4):
            x = bounds.x + bounds.width * 0.25 * i
            y = bounds.y + bounds.height * 0.25 * i
            rl.draw_line(int(x), int(bounds.y), int(x), int(bounds.y + bounds.height), grid_color)
            rl.draw_line(int(bounds.x), int(y), int(bounds.x + bounds.width), int(y), grid_color)
        
        # Draw curve
        if len(self.points) > 0:
            old_x = bounds.x
            old_y = bounds.y + bounds.height * (1.0 - self.points[0].position.y)
            
            # Draw curve with many small line segments
            for i in range(1, 101):
                t = i / 100.0
                normalized_y = self.evaluate(t) / (self.end_value - self.start_value)
                
                x = bounds.x + t * bounds.width
                y = bounds.y + bounds.height * (1.0 - normalized_y)
                
                rl.draw_line(int(old_x), int(old_y), int(x), int(y), color)
                
                old_x = x
                old_y = y
        
        # Draw points
        for i, point in enumerate(self.points):
            x = bounds.x + point.position.x * bounds.width
            y = bounds.y + bounds.height * (1.0 - point.position.y)
            
            # Draw point
            if i == self.selected_index:
                rl.draw_circle(int(x), int(y), 6, rl.YELLOW)
            else:
                rl.draw_circle(int(x), int(y), 5, rl.WHITE)
            
            rl.draw_circle_lines(int(x), int(y), 5, rl.BLACK)

def load_curve_defaults():
    """Create default animation curves"""
    curves = []
    
    # X position curve
    curve_x = AnimationCurve(100.0, 650.0)
    curve_x.add_point(0.0, 0.0)
    curve_x.add_point(0.2, 0.2)
    curve_x.add_point(0.4, 0.4)
    curve_x.add_point(0.6, 0.6)
    curve_x.add_point(0.8, 0.8)
    curve_x.add_point(1.0, 1.0)
    curves.append(curve_x)
    
    # Y position curve - Bounce effect
    curve_y = AnimationCurve(400.0, 100.0)
    curve_y.add_point(0.0, 0.0)
    curve_y.add_point(0.2, 0.8)
    curve_y.add_point(0.4, 0.2)
    curve_y.add_point(0.6, 0.6)
    curve_y.add_point(0.8, 0.1)
    curve_y.add_point(1.0, 0.5)
    curves.append(curve_y)
    
    # Width curve - Pulse effect
    curve_w = AnimationCurve(20.0, 50.0)
    curve_w.add_point(0.0, 0.0)
    curve_w.add_point(0.2, 1.0)
    curve_w.add_point(0.4, 0.2)
    curve_w.add_point(0.6, 0.8)
    curve_w.add_point(0.8, 0.5)
    curve_w.add_point(1.0, 1.0)
    curves.append(curve_w)
    
    # Height curve - Same as width for aspect ratio
    curve_h = AnimationCurve(20.0, 50.0)
    curve_h.add_point(0.0, 0.0)
    curve_h.add_point(0.2, 1.0)
    curve_h.add_point(0.4, 0.2)
    curve_h.add_point(0.6, 0.8)
    curve_h.add_point(0.8, 0.5)
    curve_h.add_point(1.0, 1.0)
    curves.append(curve_h)
    
    # Rotation curve
    curve_r = AnimationCurve(0.0, 360.0)
    curve_r.add_point(0.0, 0.0)
    curve_r.add_point(0.5, 0.5)
    curve_r.add_point(1.0, 1.0)
    curves.append(curve_r)
    
    return curves

def main():
    # Initialization
    #---------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 540
    
    rl.init_window(screen_width, screen_height, "raygui - animation curves (simplified)")
    rl.set_target_fps(60)
    
    # GUI style
    rl.gui_load_style_default()
    visual_style_active_ptr = rl.ffi.new('int *', 0)
    prev_visual_style_active = 0
    
    # GUI states
    section_active = [True, False, False, False, False]
    section_names = ["X Position", "Y Position", "Width", "Height", "Rotation"]
    play_animation = True
    show_help = True
    
    settings_rect = rl.Rectangle(screen_width - screen_width/3, 0, screen_width/3, screen_height)
    move_slider = False
    
    # Animation curves
    # 0 -> Ball X position
    # 1 -> Ball Y position
    # 2 -> Ball Width
    # 3 -> Ball Height
    # 4 -> Ball rotation
    curves = load_curve_defaults()
    
    # Animation time
    time_val = 0.0
    animation_time = 4.0
    
    # Main game loop
    while not rl.window_should_close():
        # Update
        #----------------------------------------------------------------------------------
        if play_animation:
            time_val += rl.get_frame_time()
        
        # Reset timer
        if time_val > animation_time:
            time_val = 0
        
        # Ball animation
        t = time_val / animation_time
        ball_pos = rl.Vector2(curves[0].evaluate(t), curves[1].evaluate(t))
        ball_size = rl.Vector2(curves[2].evaluate(t), curves[3].evaluate(t))
        ball_rotation = curves[4].evaluate(t)
        
        # Update style
        if visual_style_active_ptr[0] != prev_visual_style_active:
            if visual_style_active_ptr[0] == 0:
                rl.gui_load_style_default()
            elif visual_style_active_ptr[0] == 1:
                rl.gui_load_style_jungle()
            elif visual_style_active_ptr[0] == 2:
                rl.gui_load_style_lavanda()
            elif visual_style_active_ptr[0] == 3:
                rl.gui_load_style_dark()
            elif visual_style_active_ptr[0] == 4:
                rl.gui_load_style_bluish()
            elif visual_style_active_ptr[0] == 5:
                rl.gui_load_style_cyber()
            elif visual_style_active_ptr[0] == 6:
                rl.gui_load_style_terminal()
            
            prev_visual_style_active = visual_style_active_ptr[0]
        
        # Update settings panel rect
        slider_rect = rl.Rectangle(settings_rect.x - 4, settings_rect.y, 4, settings_rect.height)
        if (rl.check_collision_point_rec(rl.get_mouse_position(), slider_rect) and 
            rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON)):
            move_slider = True
        if rl.is_mouse_button_up(rl.MOUSE_LEFT_BUTTON):
            move_slider = False
        
        if move_slider:
            settings_rect.x = rl.get_mouse_x()
            
            # Minimum-Maximum size
            if settings_rect.x > (screen_width - 4):
                settings_rect.x = screen_width - 4
            elif settings_rect.x < 4:
                settings_rect.x = 4
                
            settings_rect.width = screen_width - settings_rect.x
        
        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        # PORT: "0xffff_ffff &" is a work-around for converting the negative int32 to uint32
        rl.clear_background(rl.get_color(0xffff_ffff & rl.gui_get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))
        
        # Draw ball
        rl.draw_rectangle_pro(
            rl.Rectangle(ball_pos.x, ball_pos.y, ball_size.x, ball_size.y),
            rl.Vector2(ball_size.x/2, ball_size.y/2),
            ball_rotation,
            rl.ColorAlpha(rl.RED, 0.9)
        )
        
        # Bottom info
        rl.gui_panel(rl.Rectangle(0, screen_height - 30, screen_width - settings_rect.width, 30), None)
        rl.draw_text(
            f"Time: {time_val:.2f} / {animation_time:.2f} (SPACE to play/pause)",
            10, screen_height - 25, 10, rl.get_color(rl.get_style(rl.DEFAULT, rl.TEXT_COLOR_NORMAL))
        )
        
        # Drawing settings and curve editor
        rl.gui_panel(settings_rect, "Settings")
        
        # Style selector
        rl.gui_label(rl.Rectangle(settings_rect.x + 8, settings_rect.y + 30, 60, 20), "Style:")
        rl.gui_combo_box(
            rl.Rectangle(settings_rect.x + 50, settings_rect.y + 30, 140, 20),
            "Default;Jungle;Lavanda;Dark;Bluish;Cyber;Terminal",
            visual_style_active_ptr
        )
        
        # Settings
        rl.gui_check_box(rl.Rectangle(settings_rect.x + 10, settings_rect.y + 60, 20, 20), "Play animation", rl.ffi.new('bool *', play_animation))
        play_animation = rl.gui_check_box(rl.Rectangle(settings_rect.x + 10, settings_rect.y + 60, 20, 20), "Play animation", rl.ffi.new('bool *', play_animation))[0]
        
        # Draw curve editors
        curve_height = 80
        total_curves_height = len(curves) * curve_height
        
        for i in range(len(curves)):
            section_active[i] = rl.gui_check_box(
                rl.Rectangle(settings_rect.x + 10, settings_rect.y + 100 + i * 20, 20, 20),
                section_names[i],
                rl.ffi.new('bool *', section_active[i])
            )[0]
            
            if section_active[i]:
                curve_bounds = rl.Rectangle(
                    settings_rect.x + 10,
                    settings_rect.y + 122 + i * 20,
                    settings_rect.width - 20,
                    curve_height
                )
                curves[i].draw(curve_bounds, rl.get_color(rl.get_style(rl.DEFAULT, rl.TEXT_COLOR_PRESSED)))
        
        # Draw time marker on active curves
        for i in range(len(curves)):
            if section_active[i]:
                curve_bounds = rl.Rectangle(
                    settings_rect.x + 10,
                    settings_rect.y + 122 + i * 20,
                    settings_rect.width - 20,
                    curve_height
                )
                marker_x = curve_bounds.x + t * curve_bounds.width
                rl.draw_line_ex(
                    rl.Vector2(marker_x, curve_bounds.y),
                    rl.Vector2(marker_x, curve_bounds.y + curve_bounds.height),
                    2,
                    rl.ColorAlpha(rl.YELLOW, 0.8)
                )
        
        # Handle key presses
        if rl.is_key_pressed(rl.KEY_SPACE):
            play_animation = not play_animation
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------
    
    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
