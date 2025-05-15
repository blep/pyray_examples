"""raylib [shaders] example - Sieve of Eratosthenes
Example complexity rating: [★★★☆] 3/4
NOTE: Sieve of Eratosthenes, the earliest known (ancient Greek) prime number sieve.
    "Sift the twos and sift the threes,
     The Sieve of Eratosthenes.
     When the multiples sublime,
     the numbers that are left are prime."
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3).
Example originally created with raylib 2.5, last time updated with raylib 4.0
Example contributed by ProfJski (@ProfJski) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 ProfJski (@ProfJski) and Ramon Santamaria (@raysan5)

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

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - Sieve of Eratosthenes")

    target = rl.load_render_texture(screen_width, screen_height)

    # Load Eratosthenes shader
    # NOTE: Defining "" (empty string) for vertex shader forces usage of internal default vertex shader
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/eratosthenes.fs"))

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():     # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # Nothing to do here, everything is happening in the shader
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_texture_mode(target)       # Enable drawing to texture
        rl.clear_background(rl.BLACK)       # Clear the render texture

        # Draw a rectangle in shader mode to be used as shader canvas
        # NOTE: Rectangle uses font white character texture coordinates,
        # so shader can not be applied here directly because input vertexTexCoord
        # do not represent full screen coordinates (space where want to apply shader)
        rl.draw_rectangle(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.BLACK)
        rl.end_texture_mode()               # End drawing to texture (now we have a blank texture available for the shader)

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)    # Clear screen background

        rl.begin_shader_mode(shader)
        # NOTE: Render texture must be y-flipped due to default OpenGL coordinates (left-bottom)
        rl.draw_texture_rec(
            target.texture,
            rl.Rectangle(0, 0, float(target.texture.width), float(-target.texture.height)),
            rl.Vector2(0.0, 0.0),
            rl.WHITE
        )
        rl.end_shader_mode()
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