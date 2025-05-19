"""raylib [rlgl] example - Using rlgl module as standalone module
rlgl library is an abstraction layer for multiple OpenGL versions (1.1, 2.1, 3.3 Core, ES 2.0)
that provides a pseudo-OpenGL 1.1 immediate-mode style API (rlVertex, rlTranslate, rlRotate...)
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 1.6, last time updated with raylib 4.0
WARNING: This example is intended only for PLATFORM_DESKTOP and OpenGL 3.3 Core profile.
    It could work on other platforms if redesigned for those platforms (out-of-scope)
DEPENDENCIES:
    glfw3     - Windows and context initialization library
    rlgl.h    - OpenGL abstraction layer to OpenGL 1.1, 3.3 or ES2
    glad.h    - OpenGL extensions initialization library (required by rlgl)
    raymath.h - 3D math library
WINDOWS COMPILATION:
    gcc -o rlgl_standalone.exe rlgl_standalone.c -s -Iexternal\include -I..\..\src  \
        -L. -Lexternal\lib -lglfw3 -lopengl32 -lgdi32 -Wall -std=c99 -DGRAPHICS_API_OPENGL_33
APPLE COMPILATION:
    gcc -o rlgl_standalone rlgl_standalone.c -I../../src -Iexternal/include -Lexternal/lib \
        -lglfw3 -framework CoreVideo -framework OpenGL -framework IOKit -framework Cocoa
        -Wno-deprecated-declarations -std=c99 -DGRAPHICS_API_OPENGL_33
LICENSE: zlib/libpng
This example is licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software:
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)
This software is provided "as-is", without any express or implied warranty. In no event
will the authors be held liable for any damages arising from the use of this software.
Permission is granted to anyone to use this software for any purpose, including commercial
applications, and to alter it and redistribute it freely, subject to the following restrictions:
  1. The origin of this software must not be misrepresented; you must not claim that you
  wrote the original software. If you use this software in a product, an acknowledgment
  in the product documentation would be appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be misrepresented
  as being the original software.
  3. This notice may not be removed or altered from any source distribution.

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Camera type (defines a camera position/orientation in 3d space)
class Camera:
    def __init__(self):
        self.position = rl.Vector3(0.0, 0.0, 0.0)  # Camera position
        self.target = rl.Vector3(0.0, 0.0, 0.0)    # Camera target it looks-at
        self.up = rl.Vector3(0.0, 0.0, 0.0)        # Camera up vector (rotation over its axis)
        self.fovy = 0.0                            # Camera field-of-view apperture in Y (degrees)
        self.projection = 0                        # Camera projection: CAMERA_PERSPECTIVE or CAMERA_ORTHOGRAPHIC

# These are color constants to match the original example
RED = rl.Color(230, 41, 55, 255)
RAYWHITE = rl.Color(245, 245, 245, 255)
DARKGRAY = rl.Color(80, 80, 80, 255)

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    # GLFW3 Initialization + OpenGL 3.3 Context + Extensions
    rl.init_window(screen_width, screen_height, "raylib [rlgl] example - rlgl standalone")

    # Define our custom camera to look into our 3d world
    camera = Camera()
    camera.position = rl.Vector3(5.0, 5.0, 5.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Using rlgl we can access raylib internal matrix stack
    # Useful to define custom views and projections
    # After that we have full control of matrix handling

    # Set drawing position to center, middle with some offset
    position = rl.Vector3(0.0, 0.0, 0.0)
    rotation = rl.Quaternion(0.0, 0.0, 0.0, 1.0)
    scale = rl.Vector3(1.0, 1.0, 1.0)

    # Model transformation matrix (rotation -> scale -> translation)
    transform = rl.matrix_identity()

    angle = 0.0  # Global transformation angle

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    
    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # Change camera rotation
        angle += 1.0

        # Use our custom camera to look into our 3d world
        # Set custom model transform (translate + rotate)
        transform = rl.matrix_identity()
        transform = rl.matrix_multiply(transform, rl.matrix_rotate_z(angle * rl.DEG2RAD))
        transform = rl.matrix_multiply(transform, rl.matrix_rotate_x(angle * rl.DEG2RAD))
        transform = rl.matrix_multiply(transform, rl.matrix_translate(position.x, position.y, position.z))

        # Draw
        rl.begin_drawing()
        rl.clear_background(RAYWHITE)

        # Using directly OpenGL 3.3 functions
        rl.begin_mode_3d_custom(camera, camera.fovy, camera.projection)

        # Grid of lines
        rl.rl_push_matrix()
        rl.rl_translatef(0.0, 0.0, 0.0)
        rl.rl_begin(rl.RL_LINES)
        for i in range(-10, 11):
            if i == 0:
                rl.rl_color4ub(5, 5, 5, 255)
            else:
                rl.rl_color4ub(40, 40, 40, 255)

            rl.rl_vertex3f(i, 0.0, -10.0)
            rl.rl_vertex3f(i, 0.0, 10.0)
            
            rl.rl_vertex3f(-10.0, 0.0, i)
            rl.rl_vertex3f(10.0, 0.0, i)
        rl.rl_end()
        rl.rl_pop_matrix()

        # Using rlpushMatrix/rlPopMatrix we can store multiple matrix transformations
        # This allows to work in different coordinate systems
        rl.rl_push_matrix()
        rl.rl_translatef(0.0, 0.5, 0.0)
        rl.rl_rotatef(angle, 0.0, 1.0, 0.0)
        rl.rl_scalef(0.5, 0.5, 0.5)

        # Draw 3d cube
        rl.rl_begin(rl.RL_TRIANGLES)
        rl.rl_color4ub(255, 0, 0, 255)
        rl.rl_normal3f(0.0, 1.0, 0.0)
        # Top face
        rl.rl_vertex3f(-1.0, 1.0, -1.0)
        rl.rl_vertex3f(-1.0, 1.0, 1.0)
        rl.rl_vertex3f(1.0, 1.0, 1.0)

        rl.rl_vertex3f(1.0, 1.0, 1.0)
        rl.rl_vertex3f(1.0, 1.0, -1.0)
        rl.rl_vertex3f(-1.0, 1.0, -1.0)
        # Bottom face
        rl.rl_normal3f(0.0, -1.0, 0.0)
        rl.rl_vertex3f(-1.0, -1.0, -1.0)
        rl.rl_vertex3f(1.0, -1.0, -1.0)
        rl.rl_vertex3f(1.0, -1.0, 1.0)

        rl.rl_vertex3f(1.0, -1.0, 1.0)
        rl.rl_vertex3f(-1.0, -1.0, 1.0)
        rl.rl_vertex3f(-1.0, -1.0, -1.0)
        # Front face
        rl.rl_normal3f(0.0, 0.0, 1.0)
        rl.rl_vertex3f(-1.0, -1.0, 1.0)
        rl.rl_vertex3f(1.0, -1.0, 1.0)
        rl.rl_vertex3f(1.0, 1.0, 1.0)

        rl.rl_vertex3f(1.0, 1.0, 1.0)
        rl.rl_vertex3f(-1.0, 1.0, 1.0)
        rl.rl_vertex3f(-1.0, -1.0, 1.0)
        # Back face
        rl.rl_normal3f(0.0, 0.0, -1.0)
        rl.rl_vertex3f(-1.0, -1.0, -1.0)
        rl.rl_vertex3f(-1.0, 1.0, -1.0)
        rl.rl_vertex3f(1.0, 1.0, -1.0)

        rl.rl_vertex3f(1.0, 1.0, -1.0)
        rl.rl_vertex3f(1.0, -1.0, -1.0)
        rl.rl_vertex3f(-1.0, -1.0, -1.0)
        # Right face
        rl.rl_normal3f(1.0, 0.0, 0.0)
        rl.rl_vertex3f(1.0, -1.0, -1.0)
        rl.rl_vertex3f(1.0, 1.0, -1.0)
        rl.rl_vertex3f(1.0, 1.0, 1.0)

        rl.rl_vertex3f(1.0, 1.0, 1.0)
        rl.rl_vertex3f(1.0, -1.0, 1.0)
        rl.rl_vertex3f(1.0, -1.0, -1.0)
        # Left face
        rl.rl_normal3f(-1.0, 0.0, 0.0)
        rl.rl_vertex3f(-1.0, -1.0, -1.0)
        rl.rl_vertex3f(-1.0, -1.0, 1.0)
        rl.rl_vertex3f(-1.0, 1.0, 1.0)

        rl.rl_vertex3f(-1.0, 1.0, 1.0)
        rl.rl_vertex3f(-1.0, 1.0, -1.0)
        rl.rl_vertex3f(-1.0, -1.0, -1.0)
        rl.rl_end()

        rl.rl_pop_matrix()

        # Draw some cubes around
        for i in range(8):
            rl.rl_push_matrix()
            rl.rl_translatef(
                math.sin(angle * rl.DEG2RAD) * 4.0, 0.0,
                math.cos(angle * rl.DEG2RAD) * 4.0
            )
            rl.rl_rotatef(angle, 0.0, 1.0, 0.0)
            rl.rl_scalef(0.5, 0.5, 0.5)

            rl.draw_cube_wires(rl.Vector3(0, 0, 0), 1.0, 1.0, 1.0, DARKGRAY)

            rl.rl_pop_matrix()
        
        rl.end_mode_3d()

        # Draw info in 2d
        rl.draw_text("Following this guide:", 10, 50, 10, DARKGRAY)
        rl.draw_text("https://learnopengl.com/Getting-started/Coordinate-Systems", 10, 70, 10, DARKGRAY)
        rl.draw_text("Example shows how to:", 10, 110, 10, DARKGRAY)
        rl.draw_text("- Use rlgl matrix stack functions", 10, 130, 10, DARKGRAY)
        rl.draw_text("- Define position, rotation, scale of elements", 10, 150, 10, DARKGRAY)
        rl.draw_text("- Work with diferent coordinate systems", 10, 170, 10, DARKGRAY)
        rl.draw_text("Note: Using rlgl you can combine raylib with OpenGL code", 10, 210, 10, DARKGRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()

    # De-Initialization
    rl.close_window()  # Close window and OpenGL context

if __name__ == "__main__":
    main()
