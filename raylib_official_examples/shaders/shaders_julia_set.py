"""raylib [shaders] example - Julia sets
Example complexity rating: [★★★☆] 3/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3).
Example originally created with raylib 2.5, last time updated with raylib 4.0
Example contributed by Josh Colclough (@joshcol9232) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Josh Colclough (@joshcol9232) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 100
else:
    GLSL_VERSION = 330

# A few good julia sets
points_of_interest = [
    [-0.348827, 0.607167],
    [-0.786268, 0.169728],
    [-0.8, 0.156],
    [0.285, 0.0],
    [-0.835, -0.2321],
    [-0.70176, -0.3842],
]

screen_width = 800
screen_height = 450
zoom_speed = 1.01
offset_speed_mul = 2.0

starting_zoom = 0.75

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - julia sets")    # Load julia set shader
    # NOTE: Defining empty string ("") for vertex shader forces usage of internal default vertex shader
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/julia_set.fs"))

    # Create a RenderTexture2D to be used for render to texture
    target = rl.load_render_texture(rl.get_screen_width(), rl.get_screen_height())

    # c constant to use in z^2 + c
    c = rl.ffi.new("float[2]", [points_of_interest[0][0], points_of_interest[0][1]])

    # Offset and zoom to draw the julia set at. (centered on screen and default size)
    offset = rl.ffi.new("float[2]", [0.0, 0.0])
    zoom = starting_zoom

    # Get variable (uniform) locations on the shader to connect with the program
    # NOTE: If uniform variable could not be found in the shader, function returns -1
    c_loc = rl.get_shader_location(shader, "c")
    zoom_loc = rl.get_shader_location(shader, "zoom")
    offset_loc = rl.get_shader_location(shader, "offset")

    # Upload the shader uniform values!
    rl.set_shader_value(shader, c_loc, c, rl.SHADER_UNIFORM_VEC2)
    rl.set_shader_value(shader, zoom_loc, rl.ffi.new("float *", zoom), rl.SHADER_UNIFORM_FLOAT)
    rl.set_shader_value(shader, offset_loc, offset, rl.SHADER_UNIFORM_VEC2)

    increment_speed = 0             # Multiplier of speed to change c value
    show_controls = True            # Show controls

    rl.set_target_fps(60)           # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():        # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # Press [1 - 6] to reset c to a point of interest
        if (rl.is_key_pressed(rl.KEY_ONE) or
            rl.is_key_pressed(rl.KEY_TWO) or
            rl.is_key_pressed(rl.KEY_THREE) or
            rl.is_key_pressed(rl.KEY_FOUR) or
            rl.is_key_pressed(rl.KEY_FIVE) or
            rl.is_key_pressed(rl.KEY_SIX)):

            if rl.is_key_pressed(rl.KEY_ONE):
                c[0], c[1] = points_of_interest[0][0], points_of_interest[0][1]
            elif rl.is_key_pressed(rl.KEY_TWO):
                c[0], c[1] = points_of_interest[1][0], points_of_interest[1][1]
            elif rl.is_key_pressed(rl.KEY_THREE):
                c[0], c[1] = points_of_interest[2][0], points_of_interest[2][1]
            elif rl.is_key_pressed(rl.KEY_FOUR):
                c[0], c[1] = points_of_interest[3][0], points_of_interest[3][1]
            elif rl.is_key_pressed(rl.KEY_FIVE):
                c[0], c[1] = points_of_interest[4][0], points_of_interest[4][1]
            elif rl.is_key_pressed(rl.KEY_SIX):
                c[0], c[1] = points_of_interest[5][0], points_of_interest[5][1]

            rl.set_shader_value(shader, c_loc, c, rl.SHADER_UNIFORM_VEC2)

        # If "R" is pressed, reset zoom and offset.
        if rl.is_key_pressed(rl.KEY_R):
            zoom = starting_zoom
            offset[0] = 0.0
            offset[1] = 0.0
            rl.set_shader_value(shader, zoom_loc, rl.ffi.new("float *", zoom), rl.SHADER_UNIFORM_FLOAT)
            rl.set_shader_value(shader, offset_loc, offset, rl.SHADER_UNIFORM_VEC2)

        if rl.is_key_pressed(rl.KEY_SPACE): 
            increment_speed = 0         # Pause animation (c change)
            
        if rl.is_key_pressed(rl.KEY_F1): 
            show_controls = not show_controls  # Toggle whether or not to show controls

        if rl.is_key_pressed(rl.KEY_RIGHT): 
            increment_speed += 1
        elif rl.is_key_pressed(rl.KEY_LEFT): 
            increment_speed -= 1

        # If either left or right button is pressed, zoom in/out.
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT) or rl.is_mouse_button_down(rl.MOUSE_BUTTON_RIGHT):
            # Change zoom. If Mouse left -> zoom in. Mouse right -> zoom out.
            if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
                zoom *= zoom_speed
            else:
                zoom *= 1.0/zoom_speed

            mouse_pos = rl.get_mouse_position()
            # Find the velocity at which to change the camera. Take the distance of the mouse
            # from the center of the screen as the direction, and adjust magnitude based on
            # the current zoom.
            offset_velocity_x = (mouse_pos.x/screen_width - 0.5)*offset_speed_mul/zoom
            offset_velocity_y = (mouse_pos.y/screen_height - 0.5)*offset_speed_mul/zoom

            # Apply move velocity to camera
            offset[0] += rl.get_frame_time()*offset_velocity_x
            offset[1] += rl.get_frame_time()*offset_velocity_y

            # Update the shader uniform values!
            rl.set_shader_value(shader, zoom_loc, rl.ffi.new("float *", zoom), rl.SHADER_UNIFORM_FLOAT)
            rl.set_shader_value(shader, offset_loc, offset, rl.SHADER_UNIFORM_VEC2)

        # Increment c value with time
        dc = rl.get_frame_time()*increment_speed*0.0005
        c[0] += dc
        c[1] += dc
        rl.set_shader_value(shader, c_loc, c, rl.SHADER_UNIFORM_VEC2)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        # Using a render texture to draw Julia set
        rl.begin_texture_mode(target)       # Enable drawing to texture
        rl.clear_background(rl.BLACK)       # Clear the render texture

        # Draw a rectangle in shader mode to be used as shader canvas
        # NOTE: Rectangle uses font white character texture coordinates,
        # so shader cannot be applied here directly because input vertexTexCoord
        # do not represent full screen coordinates (space where we want to apply shader)
        rl.draw_rectangle(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.BLACK)
        rl.end_texture_mode()
            
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)     # Clear screen background

        # Draw the saved texture and rendered julia set with shader
        # NOTE: We do not invert texture on Y, already considered inside shader
        rl.begin_shader_mode(shader)
        # WARNING: If FLAG_WINDOW_HIGHDPI is enabled, HighDPI monitor scaling should be considered
        # when rendering the RenderTexture2D to fit in the HighDPI scaled Window
        rl.draw_texture_ex(target.texture, rl.Vector2(0.0, 0.0), 0.0, 1.0, rl.WHITE)
        rl.end_shader_mode()

        if show_controls:
            rl.draw_text("Press Mouse buttons right/left to zoom in/out and move", 10, 15, 10, rl.RAYWHITE)
            rl.draw_text("Press KEY_F1 to toggle these controls", 10, 30, 10, rl.RAYWHITE)
            rl.draw_text("Press KEYS [1 - 6] to change point of interest", 10, 45, 10, rl.RAYWHITE)
            rl.draw_text("Press KEY_LEFT | KEY_RIGHT to change speed", 10, 60, 10, rl.RAYWHITE)
            rl.draw_text("Press KEY_SPACE to stop movement animation", 10, 75, 10, rl.RAYWHITE)
            rl.draw_text("Press KEY_R to recenter the camera", 10, 90, 10, rl.RAYWHITE)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)               # Unload shader
    rl.unload_render_texture(target)       # Unload render texture

    rl.close_window()                      # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()