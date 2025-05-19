"""raylib [shaders] example - Rounded Rectangle
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 5.5, last time updated with raylib 5.5
Example contributed by Anstro Pleuton (@anstropleuton) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2025-2025 Anstro Pleuton (@anstropleuton)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
from dataclasses import dataclass
THIS_DIR = Path(__file__).resolve().parent

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 100
else:
    GLSL_VERSION = 330

# Rounded rectangle data
@dataclass
class RoundedRectangle:
    corner_radius: rl.Vector4  # Individual corner radius (top-left, top-right, bottom-left, bottom-right)
    
    # Shadow variables
    shadow_radius: float
    shadow_offset: rl.Vector2
    shadow_scale: float
    
    # Border variables
    border_thickness: float  # Inner-border thickness
    
    # Shader locations
    rectangle_loc: int = 0
    radius_loc: int = 0
    color_loc: int = 0
    shadow_radius_loc: int = 0
    shadow_offset_loc: int = 0
    shadow_scale_loc: int = 0
    shadow_color_loc: int = 0
    border_thickness_loc: int = 0
    border_color_loc: int = 0

# Create a rounded rectangle and set uniform locations
def create_rounded_rectangle(corner_radius, shadow_radius, shadow_offset, shadow_scale, border_thickness, shader):
    rec = RoundedRectangle(
        corner_radius=corner_radius,
        shadow_radius=shadow_radius,
        shadow_offset=shadow_offset,
        shadow_scale=shadow_scale,
        border_thickness=border_thickness
    )
    
    # Get shader uniform locations
    rec.rectangle_loc = rl.get_shader_location(shader, "rectangle")
    rec.radius_loc = rl.get_shader_location(shader, "radius")
    rec.color_loc = rl.get_shader_location(shader, "color")
    rec.shadow_radius_loc = rl.get_shader_location(shader, "shadowRadius")
    rec.shadow_offset_loc = rl.get_shader_location(shader, "shadowOffset")
    rec.shadow_scale_loc = rl.get_shader_location(shader, "shadowScale")
    rec.shadow_color_loc = rl.get_shader_location(shader, "shadowColor")
    rec.border_thickness_loc = rl.get_shader_location(shader, "borderThickness")
    rec.border_color_loc = rl.get_shader_location(shader, "borderColor")
    
    update_rounded_rectangle(rec, shader)
    
    return rec

# Update rounded rectangle uniforms
def update_rounded_rectangle(rec, shader):
    corner_radius = rl.ffi.new("float[4]", [rec.corner_radius.x, rec.corner_radius.y, rec.corner_radius.z, rec.corner_radius.w])
    rl.set_shader_value(shader, rec.radius_loc, corner_radius, rl.SHADER_UNIFORM_VEC4)
    
    rl.set_shader_value(shader, rec.shadow_radius_loc, rl.ffi.new("float *", rec.shadow_radius), rl.SHADER_UNIFORM_FLOAT)
    
    shadow_offset = rl.ffi.new("float[2]", [rec.shadow_offset.x, rec.shadow_offset.y])
    rl.set_shader_value(shader, rec.shadow_offset_loc, shadow_offset, rl.SHADER_UNIFORM_VEC2)
    
    rl.set_shader_value(shader, rec.shadow_scale_loc, rl.ffi.new("float *", rec.shadow_scale), rl.SHADER_UNIFORM_FLOAT)
    rl.set_shader_value(shader, rec.border_thickness_loc, rl.ffi.new("float *", rec.border_thickness), rl.SHADER_UNIFORM_FLOAT)

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450
    
    rectangle_color = rl.BLUE
    shadow_color = rl.DARKBLUE
    border_color = rl.SKYBLUE
    
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - Rounded Rectangle")
    
    # Load the shader
    shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/base.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/rounded_rectangle.fs")
    )
    
    # Create a rounded rectangle
    rounded_rectangle = create_rounded_rectangle(
        rl.Vector4(5.0, 10.0, 15.0, 20.0),  # Corner radius
        20.0,                               # Shadow radius
        rl.Vector2(0.0, -5.0),              # Shadow offset
        0.95,                               # Shadow scale
        5.0,                                # Border thickness
        shader                              # Shader
    )
    
    # Update shader uniforms
    update_rounded_rectangle(rounded_rectangle, shader)
    
    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------
    
    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.RAYWHITE)
        
        # Draw rectangle box with rounded corners using shader
        rec = rl.Rectangle(50, 70, 110, 60)
        rl.draw_rectangle_lines(int(rec.x - 20), int(rec.y - 20), int(rec.width + 40), int(rec.height + 40), rl.DARKGRAY)
        rl.draw_text("Rounded rectangle", int(rec.x - 20), int(rec.y - 35), 10, rl.DARKGRAY)
        
        # Flip Y axis to match shader coordinate system
        rec.y = screen_height - rec.y - rec.height
        rect_values = rl.ffi.new("float[4]", [rec.x, rec.y, rec.width, rec.height])
        rl.set_shader_value(shader, rounded_rectangle.rectangle_loc, rect_values, rl.SHADER_UNIFORM_VEC4)
        
        # Only rectangle color
        rect_color = rl.ffi.new("float[4]", [rectangle_color[0]/255.0, rectangle_color[1]/255.0, rectangle_color[2]/255.0, rectangle_color[3]/255.0])
        shadow_color_0 = rl.ffi.new("float[4]", [0.0, 0.0, 0.0, 0.0])
        border_color_0 = rl.ffi.new("float[4]", [0.0, 0.0, 0.0, 0.0])
        
        rl.set_shader_value(shader, rounded_rectangle.color_loc, rect_color, rl.SHADER_UNIFORM_VEC4)
        rl.set_shader_value(shader, rounded_rectangle.shadow_color_loc, shadow_color_0, rl.SHADER_UNIFORM_VEC4)
        rl.set_shader_value(shader, rounded_rectangle.border_color_loc, border_color_0, rl.SHADER_UNIFORM_VEC4)
        
        rl.begin_shader_mode(shader)
        rl.draw_rectangle(0, 0, screen_width, screen_height, rl.WHITE)
        rl.end_shader_mode()
        
        
        # Draw rectangle shadow using shader
        rec = rl.Rectangle(50, 200, 110, 60)
        rl.draw_rectangle_lines(int(rec.x - 20), int(rec.y - 20), int(rec.width + 40), int(rec.height + 40), rl.DARKGRAY)
        rl.draw_text("Rounded rectangle shadow", int(rec.x - 20), int(rec.y - 35), 10, rl.DARKGRAY)
        
        rec.y = screen_height - rec.y - rec.height
        rect_values = rl.ffi.new("float[4]", [rec.x, rec.y, rec.width, rec.height])
        rl.set_shader_value(shader, rounded_rectangle.rectangle_loc, rect_values, rl.SHADER_UNIFORM_VEC4)
        
        # Only shadow color
        rect_color_0 = rl.ffi.new("float[4]", [0.0, 0.0, 0.0, 0.0]) 
        shadow_color_val = rl.ffi.new("float[4]", [shadow_color[0]/255.0, shadow_color[1]/255.0, shadow_color[2]/255.0, shadow_color[3]/255.0])
        
        rl.set_shader_value(shader, rounded_rectangle.color_loc, rect_color_0, rl.SHADER_UNIFORM_VEC4)
        rl.set_shader_value(shader, rounded_rectangle.shadow_color_loc, shadow_color_val, rl.SHADER_UNIFORM_VEC4)
        rl.set_shader_value(shader, rounded_rectangle.border_color_loc, border_color_0, rl.SHADER_UNIFORM_VEC4)
        
        rl.begin_shader_mode(shader)
        rl.draw_rectangle(0, 0, screen_width, screen_height, rl.WHITE)
        rl.end_shader_mode()
        
        
        # Draw rectangle's border using shader
        rec = rl.Rectangle(50, 330, 110, 60)
        rl.draw_rectangle_lines(int(rec.x - 20), int(rec.y - 20), int(rec.width + 40), int(rec.height + 40), rl.DARKGRAY)
        rl.draw_text("Rounded rectangle border", int(rec.x - 20), int(rec.y - 35), 10, rl.DARKGRAY)
        
        rec.y = screen_height - rec.y - rec.height
        rect_values = rl.ffi.new("float[4]", [rec.x, rec.y, rec.width, rec.height])
        rl.set_shader_value(shader, rounded_rectangle.rectangle_loc, rect_values, rl.SHADER_UNIFORM_VEC4)
        
        # Only border color
        border_color_val = rl.ffi.new("float[4]", [border_color[0]/255.0, border_color[1]/255.0, border_color[2]/255.0, border_color[3]/255.0])
        
        rl.set_shader_value(shader, rounded_rectangle.color_loc, rect_color_0, rl.SHADER_UNIFORM_VEC4)
        rl.set_shader_value(shader, rounded_rectangle.shadow_color_loc, shadow_color_0, rl.SHADER_UNIFORM_VEC4)
        rl.set_shader_value(shader, rounded_rectangle.border_color_loc, border_color_val, rl.SHADER_UNIFORM_VEC4)
        
        rl.begin_shader_mode(shader)
        rl.draw_rectangle(0, 0, screen_width, screen_height, rl.WHITE)
        rl.end_shader_mode()
        
        
        # Draw one more rectangle with all three colors
        rec = rl.Rectangle(240, 80, 500, 300)
        rl.draw_rectangle_lines(int(rec.x - 30), int(rec.y - 30), int(rec.width + 60), int(rec.height + 60), rl.DARKGRAY)
        rl.draw_text("Rectangle with all three combined", int(rec.x - 30), int(rec.y - 45), 10, rl.DARKGRAY)
        
        rec.y = screen_height - rec.y - rec.height
        rect_values = rl.ffi.new("float[4]", [rec.x, rec.y, rec.width, rec.height])
        rl.set_shader_value(shader, rounded_rectangle.rectangle_loc, rect_values, rl.SHADER_UNIFORM_VEC4)
        
        # All three colors
        rl.set_shader_value(shader, rounded_rectangle.color_loc, rect_color, rl.SHADER_UNIFORM_VEC4)
        rl.set_shader_value(shader, rounded_rectangle.shadow_color_loc, shadow_color_val, rl.SHADER_UNIFORM_VEC4)
        rl.set_shader_value(shader, rounded_rectangle.border_color_loc, border_color_val, rl.SHADER_UNIFORM_VEC4)
        
        rl.begin_shader_mode(shader)
        rl.draw_rectangle(0, 0, screen_width, screen_height, rl.WHITE)
        rl.end_shader_mode()
        
        rl.draw_text("(c) Rounded rectangle SDF by Iñigo Quilez. MIT License.", screen_width - 300, screen_height - 20, 10, rl.BLACK)
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------
    
    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)  # Unload shader
    
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()