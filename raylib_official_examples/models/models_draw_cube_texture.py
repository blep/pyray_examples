"""raylib [models] example - Draw textured cube
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2022-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

#------------------------------------------------------------------------------------
# Custom Functions Declaration
#------------------------------------------------------------------------------------
def draw_cube_texture(texture, position, width, height, length, color):
    """Draw cube textured
    NOTE: Cube position is the center position"""
    x = position.x
    y = position.y
    z = position.z

    # Set desired texture to be enabled while drawing following vertex data
    rl.rl_set_texture(texture.id)

    # Vertex data transformation can be defined with the commented lines,
    # but in this example we calculate the transformed vertex data directly when calling rl_vertex3f()
    #rl.rl_push_matrix()
        # NOTE: Transformation is applied in inverse order (scale -> rotate -> translate)
        #rl.rl_translate_f(2.0, 0.0, 0.0)
        #rl.rl_rotate_f(45, 0, 1, 0)
        #rl.rl_scale_f(2.0, 2.0, 2.0)

    rl.rl_begin(rl.RL_QUADS)
    rl.rl_color4ub(color[0], color[1], color[2], color[3])
    # Front Face
    rl.rl_normal3f(0.0, 0.0, 1.0)       # Normal Pointing Towards Viewer
    rl.rl_tex_coord2f(0.0, 0.0); rl.rl_vertex3f(x - width/2, y - height/2, z + length/2)  # Bottom Left Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 0.0); rl.rl_vertex3f(x + width/2, y - height/2, z + length/2)  # Bottom Right Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 1.0); rl.rl_vertex3f(x + width/2, y + height/2, z + length/2)  # Top Right Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 1.0); rl.rl_vertex3f(x - width/2, y + height/2, z + length/2)  # Top Left Of The Texture and Quad
    # Back Face
    rl.rl_normal3f(0.0, 0.0, -1.0)     # Normal Pointing Away From Viewer
    rl.rl_tex_coord2f(1.0, 0.0); rl.rl_vertex3f(x - width/2, y - height/2, z - length/2)  # Bottom Right Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 1.0); rl.rl_vertex3f(x - width/2, y + height/2, z - length/2)  # Top Right Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 1.0); rl.rl_vertex3f(x + width/2, y + height/2, z - length/2)  # Top Left Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 0.0); rl.rl_vertex3f(x + width/2, y - height/2, z - length/2)  # Bottom Left Of The Texture and Quad
    # Top Face
    rl.rl_normal3f(0.0, 1.0, 0.0)       # Normal Pointing Up
    rl.rl_tex_coord2f(0.0, 1.0); rl.rl_vertex3f(x - width/2, y + height/2, z - length/2)  # Top Left Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 0.0); rl.rl_vertex3f(x - width/2, y + height/2, z + length/2)  # Bottom Left Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 0.0); rl.rl_vertex3f(x + width/2, y + height/2, z + length/2)  # Bottom Right Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 1.0); rl.rl_vertex3f(x + width/2, y + height/2, z - length/2)  # Top Right Of The Texture and Quad
    # Bottom Face
    rl.rl_normal3f(0.0, -1.0, 0.0)     # Normal Pointing Down
    rl.rl_tex_coord2f(1.0, 1.0); rl.rl_vertex3f(x - width/2, y - height/2, z - length/2)  # Top Right Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 1.0); rl.rl_vertex3f(x + width/2, y - height/2, z - length/2)  # Top Left Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 0.0); rl.rl_vertex3f(x + width/2, y - height/2, z + length/2)  # Bottom Left Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 0.0); rl.rl_vertex3f(x - width/2, y - height/2, z + length/2)  # Bottom Right Of The Texture and Quad
    # Right face
    rl.rl_normal3f(1.0, 0.0, 0.0)       # Normal Pointing Right
    rl.rl_tex_coord2f(1.0, 0.0); rl.rl_vertex3f(x + width/2, y - height/2, z - length/2)  # Bottom Right Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 1.0); rl.rl_vertex3f(x + width/2, y + height/2, z - length/2)  # Top Right Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 1.0); rl.rl_vertex3f(x + width/2, y + height/2, z + length/2)  # Top Left Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 0.0); rl.rl_vertex3f(x + width/2, y - height/2, z + length/2)  # Bottom Left Of The Texture and Quad
    # Left Face
    rl.rl_normal3f(-1.0, 0.0, 0.0)    # Normal Pointing Left
    rl.rl_tex_coord2f(0.0, 0.0); rl.rl_vertex3f(x - width/2, y - height/2, z - length/2)  # Bottom Left Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 0.0); rl.rl_vertex3f(x - width/2, y - height/2, z + length/2)  # Bottom Right Of The Texture and Quad
    rl.rl_tex_coord2f(1.0, 1.0); rl.rl_vertex3f(x - width/2, y + height/2, z + length/2)  # Top Right Of The Texture and Quad
    rl.rl_tex_coord2f(0.0, 1.0); rl.rl_vertex3f(x - width/2, y + height/2, z - length/2)  # Top Left Of The Texture and Quad
    rl.rl_end()
    #rl.rl_pop_matrix()

    rl.rl_set_texture(0)


def draw_cube_texture_rec(texture, source, position, width, height, length, color):
    """Draw cube with texture piece applied to all faces"""
    x = position.x
    y = position.y
    z = position.z
    tex_width = float(texture.width)
    tex_height = float(texture.height)

    # Set desired texture to be enabled while drawing following vertex data
    rl.rl_set_texture(texture.id)

    # We calculate the normalized texture coordinates for the desired texture-source-rectangle
    # It means converting from (tex.width, tex.height) coordinates to [0.0f, 1.0f] equivalent 
    rl.rl_begin(rl.RL_QUADS)
    rl.rl_color4ub(color[0], color[1], color[2], color[3])

    # Front face
    rl.rl_normal3f(0.0, 0.0, 1.0)
    rl.rl_tex_coord2f(source.x/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x - width/2, y - height/2, z + length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x + width/2, y - height/2, z + length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x + width/2, y + height/2, z + length/2)
    rl.rl_tex_coord2f(source.x/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x - width/2, y + height/2, z + length/2)

    # Back face
    rl.rl_normal3f(0.0, 0.0, -1.0)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x - width/2, y - height/2, z - length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x - width/2, y + height/2, z - length/2)
    rl.rl_tex_coord2f(source.x/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x + width/2, y + height/2, z - length/2)
    rl.rl_tex_coord2f(source.x/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x + width/2, y - height/2, z - length/2)

    # Top face
    rl.rl_normal3f(0.0, 1.0, 0.0)
    rl.rl_tex_coord2f(source.x/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x - width/2, y + height/2, z - length/2)
    rl.rl_tex_coord2f(source.x/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x - width/2, y + height/2, z + length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x + width/2, y + height/2, z + length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x + width/2, y + height/2, z - length/2)

    # Bottom face
    rl.rl_normal3f(0.0, -1.0, 0.0)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x - width/2, y - height/2, z - length/2)
    rl.rl_tex_coord2f(source.x/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x + width/2, y - height/2, z - length/2)
    rl.rl_tex_coord2f(source.x/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x + width/2, y - height/2, z + length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x - width/2, y - height/2, z + length/2)

    # Right face
    rl.rl_normal3f(1.0, 0.0, 0.0)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x + width/2, y - height/2, z - length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x + width/2, y + height/2, z - length/2)
    rl.rl_tex_coord2f(source.x/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x + width/2, y + height/2, z + length/2)
    rl.rl_tex_coord2f(source.x/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x + width/2, y - height/2, z + length/2)

    # Left face
    rl.rl_normal3f(-1.0, 0.0, 0.0)
    rl.rl_tex_coord2f(source.x/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x - width/2, y - height/2, z - length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, (source.y + source.height)/tex_height)
    rl.rl_vertex3f(x - width/2, y - height/2, z + length/2)
    rl.rl_tex_coord2f((source.x + source.width)/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x - width/2, y + height/2, z + length/2)
    rl.rl_tex_coord2f(source.x/tex_width, source.y/tex_height)
    rl.rl_vertex3f(x - width/2, y + height/2, z - length/2)

    rl.rl_end()

    rl.rl_set_texture(0)


#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - draw cube texture")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.0, 10.0, 10.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE
    
    # Load texture to be applied to the cubes sides
    texture = rl.load_texture(str(THIS_DIR/"resources/cubicmap_atlas.png"))

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # TODO: Update your variables here
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

            # Draw cube with an applied texture
        draw_cube_texture(texture, rl.Vector3(-2.0, 2.0, 0.0), 2.0, 4.0, 2.0, rl.WHITE)

            # Draw cube with an applied texture, but only a defined rectangle piece of the texture
        draw_cube_texture_rec(texture, rl.Rectangle(0.0, texture.height/2.0, texture.width/2.0, texture.height/2.0), 
                              rl.Vector3(2.0, 1.0, 0.0), 2.0, 2.0, 2.0, rl.WHITE)

        rl.draw_grid(10, 1.0)        # Draw a grid

        rl.end_mode_3d()

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(texture) # Unload texture
    
    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
