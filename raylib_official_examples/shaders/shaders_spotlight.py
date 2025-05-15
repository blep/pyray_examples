"""raylib [shaders] example - Simple shader mask
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 3.7
Example contributed by Chris Camacho (@chriscamacho) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Chris Camacho (@chriscamacho) and Ramon Santamaria (@raysan5)
The shader makes alpha holes in the forground to give the appearance of a top
down look at a spotlight casting a pool of light...
The right hand side of the screen there is just enough light to see whats
going on without the spot light, great for a stealth type game where you
have to avoid the spotlights.
The left hand side of the screen is in pitch dark except for where the spotlights are.
Although this example doesn't scale like the letterbox example, you could integrate
the two techniques, but by scaling the actual colour of the render texture rather
than using alpha as a mask.

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from dataclasses import dataclass
import math
import random
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 100
else:
    GLSL_VERSION = 330

MAX_SPOTS = 3        # NOTE: It must be the same as define in shader
MAX_STARS = 400

# Spot data
@dataclass
class Spot:
    position: rl.Vector2
    speed: rl.Vector2
    inner: float
    radius: float
    
    # Shader locations
    position_loc: int = 0
    inner_loc: int = 0
    radius_loc: int = 0

# Stars in the star field have a position and velocity
@dataclass
class Star:
    position: rl.Vector2
    speed: rl.Vector2

def reset_star(s):
    s.position = rl.Vector2(rl.get_screen_width()/2.0, rl.get_screen_height()/2.0)
    
    while True:
        s.speed.x = random.randint(-1000, 1000)/100.0
        s.speed.y = random.randint(-1000, 1000)/100.0
        
        if abs(s.speed.x) + abs(s.speed.y) > 1:
            break
    
    s.position = rl.vector2_add(s.position, rl.vector2_multiply(s.speed, rl.Vector2(8.0, 8.0)))

def update_star(s):
    s.position = rl.vector2_add(s.position, s.speed)
    
    if (s.position.x < 0 or s.position.x > rl.get_screen_width() or
        s.position.y < 0 or s.position.y > rl.get_screen_height()):
        reset_star(s)

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450
    
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - shader spotlight")
    rl.hide_cursor()
    
    tex_ray = rl.load_texture(str(THIS_DIR/"resources/raysan.png"))
    
    stars = [Star(rl.Vector2(0, 0), rl.Vector2(0, 0)) for _ in range(MAX_STARS)]
    
    for n in range(MAX_STARS):
        reset_star(stars[n])
    
    # Progress all the stars on, so they don't all start in the centre
    for m in range(int(screen_width/2.0)):
        for n in range(MAX_STARS):
            update_star(stars[n])
    
    frame_counter = 0
    
    # Use default vert shader
    shdr_spot = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/spotlight.fs"))
    
    # Get the locations of spots in the shader
    spots = []
    
    for i in range(MAX_SPOTS):
        pos_name = f"spots[{i}].pos"
        inner_name = f"spots[{i}].inner"
        radius_name = f"spots[{i}].radius"
        
        position_loc = rl.get_shader_location(shdr_spot, pos_name)
        inner_loc = rl.get_shader_location(shdr_spot, inner_name)
        radius_loc = rl.get_shader_location(shdr_spot, radius_name)
        
        spots.append(Spot(
            rl.Vector2(0, 0),
            rl.Vector2(0, 0),
            0.0,
            0.0,
            position_loc,
            inner_loc,
            radius_loc
        ))
    
    # Tell the shader how wide the screen is so we can have
    # a pitch black half and a dimly lit half.
    w_loc = rl.get_shader_location(shdr_spot, "screenWidth")
    sw = float(rl.get_screen_width())
    rl.set_shader_value(shdr_spot, w_loc, rl.ffi.new("float *", sw), rl.SHADER_UNIFORM_FLOAT)
    
    # Randomize the locations and velocities of the spotlights
    # and initialize the shader locations
    for i in range(MAX_SPOTS):
        spots[i].position.x = float(random.randint(64, screen_width - 64))
        spots[i].position.y = float(random.randint(64, screen_height - 64))
        
        while abs(spots[i].speed.x) + abs(spots[i].speed.y) < 2:
            spots[i].speed.x = random.randint(-400, 40) / 10.0
            spots[i].speed.y = random.randint(-400, 40) / 10.0
        
        spots[i].inner = 28.0 * (i + 1)
        spots[i].radius = 48.0 * (i + 1)
        
        position = rl.ffi.new("float[2]", [spots[i].position.x, spots[i].position.y])
        rl.set_shader_value(shdr_spot, spots[i].position_loc, position, rl.SHADER_UNIFORM_VEC2)
        rl.set_shader_value(shdr_spot, spots[i].inner_loc, rl.ffi.new("float *", spots[i].inner), rl.SHADER_UNIFORM_FLOAT)
        rl.set_shader_value(shdr_spot, spots[i].radius_loc, rl.ffi.new("float *", spots[i].radius), rl.SHADER_UNIFORM_FLOAT)
    
    rl.set_target_fps(60)               # Set to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------
    
    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        frame_counter += 1
        
        # Move the stars, resetting them if the go offscreen
        for n in range(MAX_STARS):
            update_star(stars[n])
        
        # Update the spots, send them to the shader
        for i in range(MAX_SPOTS):
            if i == 0:
                mp = rl.get_mouse_position()
                spots[i].position.x = mp.x
                spots[i].position.y = screen_height - mp.y
            else:
                spots[i].position.x += spots[i].speed.x
                spots[i].position.y += spots[i].speed.y
                
                if spots[i].position.x < 64:
                    spots[i].speed.x = -spots[i].speed.x
                if spots[i].position.x > (screen_width - 64):
                    spots[i].speed.x = -spots[i].speed.x
                if spots[i].position.y < 64:
                    spots[i].speed.y = -spots[i].speed.y
                if spots[i].position.y > (screen_height - 64):
                    spots[i].speed.y = -spots[i].speed.y
            
            position = rl.ffi.new("float[2]", [spots[i].position.x, spots[i].position.y])
            rl.set_shader_value(shdr_spot, spots[i].position_loc, position, rl.SHADER_UNIFORM_VEC2)
        
        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.DARKBLUE)
        
        # Draw stars and bobs
        for n in range(MAX_STARS):
            # Single pixel is just too small these days!
            rl.draw_rectangle(int(stars[n].position.x), int(stars[n].position.y), 2, 2, rl.WHITE)
        
        for i in range(16):
            rl.draw_texture(
                tex_ray,
                int((screen_width/2.0) + math.cos((frame_counter + i*8)/51.45)*(screen_width/2.2) - 32),
                int((screen_height/2.0) + math.sin((frame_counter + i*8)/17.87)*(screen_height/4.2)),
                rl.WHITE
            )
        
        # Draw spot lights
        rl.begin_shader_mode(shdr_spot)
        # Instead of a blank rectangle you could render here
        # a render texture of the full screen used to do screen
        # scaling (slight adjustment to shader would be required
        # to actually pay attention to the colour!)
        rl.draw_rectangle(0, 0, screen_width, screen_height, rl.WHITE)
        rl.end_shader_mode()
        
        rl.draw_fps(10, 10)
        
        rl.draw_text("Move the mouse!", 10, 30, 20, rl.GREEN)
        rl.draw_text("Pitch Black", int(screen_width*0.2), screen_height//2, 20, rl.GREEN)
        rl.draw_text("Dark", int(screen_width*.66), screen_height//2, 20, rl.GREEN)
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------
    
    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(tex_ray)
    rl.unload_shader(shdr_spot)
    
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()