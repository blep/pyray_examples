"""raylib [core] example - 2D Camera system
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.5, last time updated with raylib 3.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2016-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
import random

MAX_BUILDINGS = 100

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

def main():
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 2d camera")

    player = rl.Rectangle(400, 280, 40, 40)
    buildings = [rl.Rectangle() for _ in range(MAX_BUILDINGS)]
    build_colors = [rl.Color() for _ in range(MAX_BUILDINGS)]

    spacing = 0

    for i in range(MAX_BUILDINGS):
        buildings[i].width = float(rl.get_random_value(50, 200))
        buildings[i].height = float(rl.get_random_value(100, 800))
        buildings[i].y = SCREEN_HEIGHT - 130.0 - buildings[i].height
        buildings[i].x = -6000.0 + spacing

        spacing += int(buildings[i].width)

        build_colors[i] = rl.Color(
            rl.get_random_value(200, 240),
            rl.get_random_value(200, 240),
            rl.get_random_value(200, 250),
            255
        )

    camera = rl.Camera2D()
    camera.target = rl.Vector2(player.x + 20.0, player.y + 20.0)
    camera.offset = rl.Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)
    camera.rotation = 0.0
    camera.zoom = 1.0

    rl.set_target_fps(60)

    while not rl.window_should_close():
        # Update
        if rl.is_key_down(rl.KEY_RIGHT):
            player.x += 2
        elif rl.is_key_down(rl.KEY_LEFT):
            player.x -= 2

        camera.target = rl.Vector2(player.x + 20, player.y + 20)

        if rl.is_key_down(rl.KEY_A):
            camera.rotation -= 1
        elif rl.is_key_down(rl.KEY_S):
            camera.rotation += 1

        if camera.rotation > 40:
            camera.rotation = 40
        elif camera.rotation < -40:
            camera.rotation = -40

        mouse_wheel_move = rl.get_mouse_wheel_move()
        if mouse_wheel_move != 0: # Check if there's any wheel movement to avoid log(0) or log(negative)
            new_zoom = camera.zoom * math.exp(mouse_wheel_move * 0.1)
            camera.zoom = rl.clamp(new_zoom, 0.1, 3.0)


        if rl.is_key_pressed(rl.KEY_R):
            camera.zoom = 1.0
            camera.rotation = 0.0

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_2d(camera)

        rl.draw_rectangle(-6000, 320, 13000, 8000, rl.DARKGRAY)

        for i in range(MAX_BUILDINGS):
            rl.draw_rectangle_rec(buildings[i], build_colors[i])

        rl.draw_rectangle_rec(player, rl.RED)

        rl.draw_line(int(camera.target.x), -SCREEN_HEIGHT * 10, int(camera.target.x), SCREEN_HEIGHT * 10, rl.GREEN)
        rl.draw_line(-SCREEN_WIDTH * 10, int(camera.target.y), SCREEN_WIDTH * 10, int(camera.target.y), rl.GREEN)

        rl.end_mode_2d()

        rl.draw_text("SCREEN AREA", 640, 10, 20, rl.RED)

        rl.draw_rectangle(0, 0, SCREEN_WIDTH, 5, rl.RED)
        rl.draw_rectangle(0, 5, 5, SCREEN_HEIGHT - 10, rl.RED)
        rl.draw_rectangle(SCREEN_WIDTH - 5, 5, 5, SCREEN_HEIGHT - 10, rl.RED)
        rl.draw_rectangle(0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5, rl.RED)

        rl.draw_rectangle(10, 10, 250, 113, rl.fade(rl.SKYBLUE, 0.5))
        rl.draw_rectangle_lines(10, 10, 250, 113, rl.BLUE)

        rl.draw_text("Free 2d camera controls:", 20, 20, 10, rl.BLACK)
        rl.draw_text("- Right/Left to move Offset", 40, 40, 10, rl.DARKGRAY) # Corrected text, C example says move player
        rl.draw_text("- Mouse Wheel to Zoom in-out", 40, 60, 10, rl.DARKGRAY)
        rl.draw_text("- A / S to Rotate", 40, 80, 10, rl.DARKGRAY)
        rl.draw_text("- R to reset Zoom and Rotation", 40, 100, 10, rl.DARKGRAY)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
