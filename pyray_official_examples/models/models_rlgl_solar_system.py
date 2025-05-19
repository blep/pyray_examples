"""raylib [models] example - rlgl module usage with push/pop matrix transformations
Example complexity rating: [★★★★] 4/4
NOTE: This example uses [rlgl] module functionality (pseudo-OpenGL 1.1 style coding)
Example originally created with raylib 2.5, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2018-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

#------------------------------------------------------------------------------------
# Module Functions Declaration
#------------------------------------------------------------------------------------
def draw_sphere_basic(color):
    """Draw sphere without any matrix transformation"""
    rl.draw_sphere(rl.Vector3(0, 0, 0), 1.0, color)

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    sun_radius = 4.0
    earth_radius = 0.6
    earth_orbit_radius = 8.0
    moon_radius = 0.16
    moon_orbit_radius = 1.5

    rl.init_window(screen_width, screen_height, "raylib [models] example - rlgl module usage with push/pop matrix transformations")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(16.0, 16.0, 16.0)  # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)       # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)           # Camera up vector (rotation towards target)
    camera.fovy = 45.0                              # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE       # Camera projection type

    rl.set_target_fps(60)                           # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    rotation_speed = 0.2                            # General system rotation speed

    earth_rotation = 0.0                            # Rotation of earth around itself (days) in degrees
    earth_orbit_rotation = 0.0                      # Rotation of earth around the sun (years) in degrees
    moon_rotation = 0.0                             # Rotation of moon around itself
    moon_orbit_rotation = 0.0                       # Rotation of moon around earth in degrees

    # Main game loop
    while not rl.window_should_close():             # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        earth_rotation += (5.0 * rotation_speed)
        earth_orbit_rotation += (365/360.0 * rotation_speed * 5.0)
        moon_rotation += (2.0 * rotation_speed)
        moon_orbit_rotation += (8.0 * rotation_speed)
        
        rl.update_camera(camera, rl.CAMERA_FREE)    # Update camera with free camera mode
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        # Draw sun
        rl.rl_push_matrix()
        rl.rl_scalef(sun_radius, sun_radius, sun_radius)    # Scale sphere to sun size
        draw_sphere_basic(rl.GOLD)
        rl.rl_pop_matrix()

        # Draw earth
        rl.rl_push_matrix()
        rl.rl_rotatef(earth_orbit_rotation, 0.0, 1.0, 0.0)  # Rotation for earth orbit around sun
        rl.rl_translatef(earth_orbit_radius, 0.0, 0.0)      # Translation for earth orbit

        rl.rl_push_matrix()
        rl.rl_rotatef(earth_rotation, 0.25, 1.0, 0.0)       # Rotation for earth itself
        rl.rl_scalef(earth_radius, earth_radius, earth_radius)  # Scale sphere to earth size
        draw_sphere_basic(rl.BLUE)
        rl.rl_pop_matrix()

        # Draw moon
        rl.rl_rotatef(moon_orbit_rotation, 0.0, 1.0, 0.0)  # Rotation for moon orbit around earth
        rl.rl_translatef(moon_orbit_radius, 0.0, 0.0)      # Translation for moon orbit
        rl.rl_rotatef(moon_rotation, 0.0, 1.0, 0.0)        # Rotation for moon itself
        rl.rl_scalef(moon_radius, moon_radius, moon_radius) # Scale sphere to moon size
                
        draw_sphere_basic(rl.LIGHTGRAY)
        
        rl.rl_pop_matrix()

        # Draw some reference elements (small cubes)
        rl.draw_cube(rl.Vector3(0.0, 0.0, 0.0), 0.5, 0.5, 0.5, rl.RED)
        rl.draw_cube(rl.Vector3(0.0, 6.0, 0.0), 0.5, 0.5, 0.5, rl.RED)
        rl.draw_cube(rl.Vector3(0.0, 0.0, 6.0), 0.5, 0.5, 0.5, rl.RED)

        # Draw grid reference
        rl.draw_grid(20, 1.0)

        rl.end_mode_3d()
        
        rl.draw_text("EARTH ORBITING AROUND THE SUN!", 400, 10, 20, rl.MAROON)
        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()      # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
