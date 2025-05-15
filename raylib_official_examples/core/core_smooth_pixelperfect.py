"""raylib [core] example - Smooth Pixel-perfect camera
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 3.7, last time updated with raylib 4.0
Example contributed by Giancamillo Alessandroni (@NotManyIdeasDev) and
reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Giancamillo Alessandroni (@NotManyIdeasDev) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math

def main():
    screen_width = 800
    screen_height = 450

    virtual_screen_width = 160
    virtual_screen_height = 90

    virtual_ratio = float(screen_width) / float(virtual_screen_width)

    rl.init_window(screen_width, screen_height, "raylib [core] example - smooth pixel-perfect camera")

    world_space_camera = rl.Camera2D()
    world_space_camera.zoom = 1.0

    screen_space_camera = rl.Camera2D()
    screen_space_camera.zoom = 1.0

    target = rl.load_render_texture(virtual_screen_width, virtual_screen_height)

    rec01 = rl.Rectangle(70.0, 35.0, 20.0, 20.0)
    rec02 = rl.Rectangle(90.0, 55.0, 30.0, 10.0)
    rec03 = rl.Rectangle(80.0, 65.0, 15.0, 25.0)

    source_rec = rl.Rectangle(0.0, 0.0, float(target.texture.width), -float(target.texture.height))
    dest_rec = rl.Rectangle(-virtual_ratio, -virtual_ratio, screen_width + (virtual_ratio * 2), screen_height + (virtual_ratio * 2))

    origin = rl.Vector2(0.0, 0.0)

    rotation = 0.0

    camera_x = 0.0
    camera_y = 0.0

    rl.set_target_fps(60)

    while not rl.window_should_close():
        rotation += 60.0 * rl.get_frame_time()

        camera_x = (math.sin(rl.get_time()) * 50.0) - 10.0
        camera_y = math.cos(rl.get_time()) * 30.0

        screen_space_camera.target = rl.Vector2(camera_x, camera_y)

        world_space_camera.target.x = math.trunc(screen_space_camera.target.x)
        screen_space_camera.target.x -= world_space_camera.target.x
        screen_space_camera.target.x *= virtual_ratio

        world_space_camera.target.y = math.trunc(screen_space_camera.target.y)
        screen_space_camera.target.y -= world_space_camera.target.y
        screen_space_camera.target.y *= virtual_ratio

        rl.begin_texture_mode(target)
        rl.clear_background(rl.RAYWHITE)
        rl.begin_mode_2d(world_space_camera)
        rl.draw_rectangle_pro(rec01, origin, rotation, rl.BLACK)
        rl.draw_rectangle_pro(rec02, origin, -rotation, rl.RED)
        rl.draw_rectangle_pro(rec03, origin, rotation + 45.0, rl.BLUE)
        rl.end_mode_2d()
        rl.end_texture_mode()

        rl.begin_drawing()
        rl.clear_background(rl.RED)
        rl.begin_mode_2d(screen_space_camera)
        rl.draw_texture_pro(target.texture, source_rec, dest_rec, origin, 0.0, rl.WHITE)
        rl.end_mode_2d()

        rl.draw_text(f"Screen resolution: {screen_width}x{screen_height}", 10, 10, 20, rl.DARKBLUE)
        rl.draw_text(f"World resolution: {virtual_screen_width}x{virtual_screen_height}", 10, 40, 20, rl.DARKGREEN)
        rl.draw_fps(rl.get_screen_width() - 95, 10)
        rl.end_drawing()

    rl.unload_render_texture(target)
    rl.close_window()

if __name__ == '__main__':
    main()
