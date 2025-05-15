"""raylib [shaders] example - OpenGL point particle system
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 3.8, last time updated with raylib 2.5
Example contributed by Stephan Soller (@arkanis) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Stephan Soller (@arkanis) and Ramon Santamaria (@raysan5)
Mixes raylib and plain OpenGL code to draw a GL_POINTS based particle system. The
primary point is to demonstrate raylib and OpenGL interop.
rlgl batched draw operations internally so we have to flush the current batch before
doing our own OpenGL work (rlDrawRenderBatchActive()).
The example also demonstrates how to get the current model view projection matrix of
raylib. That way raylib cameras and so on work as expected.

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import ctypes
import platform
import sys

THIS_DIR = Path(__file__).resolve().parent

# Determine GLSL version
if platform.system() == "Darwin":  # macOS
    GLSL_VERSION = "330"
elif platform.system() == "Windows":
    GLSL_VERSION = "330"
else:  # Linux or other
    GLSL_VERSION = "330"

MAX_PARTICLES = 1000

# For OpenGL interop, we need to access OpenGL functions
# This is done through pyray's FFI interface
# Note: This example requires PyOpenGL for proper OpenGL access

try:
    from OpenGL.GL import *
except ImportError:
    print("This example requires PyOpenGL. Please install it using: pip install PyOpenGL")
    sys.exit(1)

# Define a Particle class for our system
class Particle:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.period = 0.0

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib - point particles")

    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/point_particle.fs"))

    current_time_loc = rl.get_shader_location(shader, "currentTime")
    color_loc = rl.get_shader_location(shader, "color")

    # Initialize the vertex buffer for particles and assign each particle random values
    particles = []
    for i in range(MAX_PARTICLES):
        particle = Particle()
        particle.x = rl.get_random_value(20, screen_width - 20)
        particle.y = rl.get_random_value(50, screen_height - 20)
        # Give each particle a slightly different period. But don't spread it too much.
        # This way the particles line up every so often and you get a glimpse of what's going on.
        particle.period = rl.get_random_value(10, 30) / 10.0
        particles.append(particle)

    # Create a plain OpenGL vertex buffer with the data and an vertex array object
    # that feeds the data from the buffer into the vertexPosition shader attribute.
    # Set up OpenGL state for the particles
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    
    # Convert particle data to a continuous array for OpenGL
    particle_data = []
    for particle in particles:
        particle_data.extend([particle.x, particle.y, particle.period])
    
    # Load the data into the buffer (convert to ctypes array first)
    data_array = (ctypes.c_float * len(particle_data))(*particle_data)
    glBufferData(GL_ARRAY_BUFFER, len(particle_data) * ctypes.sizeof(ctypes.c_float), 
                 data_array, GL_STATIC_DRAW)
    
    # Set up the vertex attributes
    stride = 3 * ctypes.sizeof(ctypes.c_float)
    
    # Position attribute (x, y)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Period attribute
    glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, stride, 
                         ctypes.c_void_p(2 * ctypes.sizeof(ctypes.c_float)))
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0)

    # Set up a camera
    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.0, 0.0, 10.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    current_time = 0.0

    rl.set_target_fps(60)

    # Main game loop
    while not rl.window_should_close():
        # Update
        current_time += rl.get_frame_time()
        
        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.begin_mode_3d(camera)
        
        # The camera alone doesn't affect the particles because we use our own shader
        # that uses the raylib model-view-projection matrix. But raylib uses the camera
        # to set this matrix up. We can also change it.
        
        # Draw the coordinate system using ralyib lines
        rl.draw_line_3d(rl.Vector3(-2, 0, 0), rl.Vector3(2, 0, 0), rl.RED)
        rl.draw_line_3d(rl.Vector3(0, -2, 0), rl.Vector3(0, 2, 0), rl.GREEN)
        rl.draw_line_3d(rl.Vector3(0, 0, -2), rl.Vector3(0, 0, 2), rl.BLUE)
        
        # Raymaths quaternions make it easy to rotate a camera or any vector
        orbit_speed = rl.get_frame_time() * 30.0  # degrees per second
        rotation = rl.quaternion_from_axis_angle(rl.Vector3(0, 1, 0), orbit_speed)
        
        # If we update the camera every frame we can rotate the camera around the scene
        camera.position = rl.vector3_rotate_by_quaternion(camera.position, rotation)

        rl.update_camera(camera, rl.CAMERA_FREE)

        # Flush raylib's own drawing
        rl.rl_draw_render_batch_active()

        # Now use our own shader
        rl.begin_shader_mode(shader)

        # Setup the shader uniforms
        current_time_value = rl.ffi.new('float *', current_time)
        rl.set_shader_value(shader, current_time_loc, current_time_value, rl.SHADER_UNIFORM_FLOAT)
        
        color_value = rl.ffi.new('float[3]', [1.0, 0.0, 0.0])  # red color
        rl.set_shader_value(shader, color_loc, color_value, rl.SHADER_UNIFORM_VEC3)

        # The shader needs the model-view-projection matrix
        # Combine raylib's model, view and projection matrices to get the same
        # transformations for our manually drawn particles
        # Using RL functions to compose our modelviewprojection
        matModelView = rl.rl_get_matrix_modelview()
        matProjection = rl.rl_get_matrix_projection()
        
        # Use OpenGL to draw the particle system
        glBindVertexArray(vao)
        glDrawArrays(GL_POINTS, 0, MAX_PARTICLES)
        glBindVertexArray(0)

        # Restore raylib's own shader
        rl.end_shader_mode()
        
        rl.end_mode_3d()

        # Draw FPS info
        rl.draw_fps(10, 10)
        rl.draw_text("Particles move in sine wave based on their position", 10, 30, 20, rl.WHITE)

        rl.end_drawing()

    # De-Initialization
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    
    rl.unload_shader(shader)
    rl.close_window()

if __name__ == "__main__":
    main()
