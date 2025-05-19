"""raylib [core] example - 2D Camera platformer
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 2.5, last time updated with raylib 3.0
Example contributed by arvyy (@arvyy) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 arvyy (@arvyy)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math

G = 400
PLAYER_JUMP_SPD = 350.0
PLAYER_HOR_SPD = 200.0

class Player:
    def __init__(self, position: rl.Vector2, speed: float, can_jump: bool):
        self.position = position
        self.speed = speed
        self.can_jump = can_jump

class EnvItem:
    def __init__(self, rect: rl.Rectangle, blocking: int, color: rl.Color):
        self.rect = rect
        self.blocking = blocking
        self.color = color

def update_player(player: Player, env_items: list[EnvItem], delta: float):
    if rl.is_key_down(rl.KEY_LEFT):
        player.position.x -= PLAYER_HOR_SPD * delta
    if rl.is_key_down(rl.KEY_RIGHT):
        player.position.x += PLAYER_HOR_SPD * delta
    if rl.is_key_down(rl.KEY_SPACE) and player.can_jump:
        player.speed = -PLAYER_JUMP_SPD
        player.can_jump = False

    hit_obstacle = False
    for ei in env_items:
        if ei.blocking and \
           ei.rect.x <= player.position.x and \
           ei.rect.x + ei.rect.width >= player.position.x and \
           ei.rect.y >= player.position.y and \
           ei.rect.y <= player.position.y + player.speed * delta:
            hit_obstacle = True
            player.speed = 0.0
            player.position.y = ei.rect.y
            break
    
    if not hit_obstacle:
        player.position.y += player.speed * delta
        player.speed += G * delta
        player.can_jump = False
    else:
        player.can_jump = True

def update_camera_center(camera: rl.Camera2D, player: Player, env_items: list[EnvItem], delta: float, width: int, height: int):
    camera.offset = rl.Vector2(width / 2.0, height / 2.0)
    camera.target = player.position

def update_camera_center_inside_map(camera: rl.Camera2D, player: Player, env_items: list[EnvItem], delta: float, width: int, height: int):
    camera.target = player.position
    camera.offset = rl.Vector2(width / 2.0, height / 2.0)
    min_x, min_y = 10000.0, 10000.0  # Use large float values
    max_x, max_y = -10000.0, -10000.0 # Use small float values

    for ei in env_items:
        min_x = min(ei.rect.x, min_x)
        max_x = max(ei.rect.x + ei.rect.width, max_x)
        min_y = min(ei.rect.y, min_y)
        max_y = max(ei.rect.y + ei.rect.height, max_y)

    max_world = rl.get_world_to_screen_2d(rl.Vector2(max_x, max_y), camera)
    min_world = rl.get_world_to_screen_2d(rl.Vector2(min_x, min_y), camera)

    if max_world.x < width:
        camera.offset.x = width - (max_world.x - width / 2.0)
    if max_world.y < height:
        camera.offset.y = height - (max_world.y - height / 2.0)
    if min_world.x > 0:
        camera.offset.x = width / 2.0 - min_world.x
    if min_world.y > 0:
        camera.offset.y = height / 2.0 - min_world.y
        
def update_camera_center_smooth_follow(camera: rl.Camera2D, player: Player, env_items: list[EnvItem], delta: float, width: int, height: int):
    min_speed = 30.0
    min_effect_length = 10.0
    fraction_speed = 0.8

    camera.offset = rl.Vector2(width / 2.0, height / 2.0)
    diff = rl.vector2_subtract(player.position, camera.target)
    length = rl.vector2_length(diff)

    if length > min_effect_length:
        speed = max(fraction_speed * length, min_speed)
        camera.target = rl.vector2_add(camera.target, rl.vector2_scale(diff, speed * delta / length))

# Need to store these as global or pass them around if they need to persist across calls for this camera mode
evening_out_state = {"evening_out": False, "even_out_target": 0.0}

def update_camera_even_out_on_landing(camera: rl.Camera2D, player: Player, env_items: list[EnvItem], delta: float, width: int, height: int):
    even_out_speed = 700.0
    
    camera.offset = rl.Vector2(width / 2.0, height / 2.0)
    camera.target.x = player.position.x

    if evening_out_state["evening_out"]:
        if evening_out_state["even_out_target"] > camera.target.y:
            camera.target.y += even_out_speed * delta
            if camera.target.y > evening_out_state["even_out_target"]:
                camera.target.y = evening_out_state["even_out_target"]
                evening_out_state["evening_out"] = False
        else:
            camera.target.y -= even_out_speed * delta
            if camera.target.y < evening_out_state["even_out_target"]:
                camera.target.y = evening_out_state["even_out_target"]
                evening_out_state["evening_out"] = False
    else:
        if player.can_jump and player.speed == 0 and player.position.y != camera.target.y:
            evening_out_state["evening_out"] = True
            evening_out_state["even_out_target"] = player.position.y

def update_camera_player_bounds_push(camera: rl.Camera2D, player: Player, env_items: list[EnvItem], delta: float, width: int, height: int):
    bbox = rl.Vector2(0.2, 0.2) # Percentage of screen size

    bbox_world_min = rl.get_screen_to_world_2d(rl.Vector2((1 - bbox.x) * 0.5 * width, (1 - bbox.y) * 0.5 * height), camera)
    bbox_world_max = rl.get_screen_to_world_2d(rl.Vector2((1 + bbox.x) * 0.5 * width, (1 + bbox.y) * 0.5 * height), camera)
    camera.offset = rl.Vector2((1 - bbox.x) * 0.5 * width, (1 - bbox.y) * 0.5 * height)

    if player.position.x < bbox_world_min.x:
        camera.target.x = player.position.x
    if player.position.y < bbox_world_min.y:
        camera.target.y = player.position.y
    if player.position.x > bbox_world_max.x:
        camera.target.x = bbox_world_min.x + (player.position.x - bbox_world_max.x)
    if player.position.y > bbox_world_max.y:
        camera.target.y = bbox_world_min.y + (player.position.y - bbox_world_max.y)


def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - 2d camera platformer")

    player = Player(rl.Vector2(400, 280), 0, False)
    
    env_items = [
        EnvItem(rl.Rectangle(0, 0, 1000, 400), 0, rl.LIGHTGRAY),
        EnvItem(rl.Rectangle(0, 400, 1000, 200), 1, rl.GRAY),
        EnvItem(rl.Rectangle(300, 200, 400, 10), 1, rl.GRAY),
        EnvItem(rl.Rectangle(250, 300, 100, 10), 1, rl.GRAY),
        EnvItem(rl.Rectangle(650, 300, 100, 10), 1, rl.GRAY)
    ]

    camera = rl.Camera2D()
    camera.target = player.position
    camera.offset = rl.Vector2(screen_width / 2.0, screen_height / 2.0)
    camera.rotation = 0.0
    camera.zoom = 1.0

    camera_updaters = [
        update_camera_center,
        update_camera_center_inside_map,
        update_camera_center_smooth_follow,
        update_camera_even_out_on_landing,
        update_camera_player_bounds_push
    ]
    
    camera_option = 0
    
    camera_descriptions = [
        "Follow player center",
        "Follow player center, but clamp to map edges",
        "Follow player center; smoothed",
        "Follow player center horizontally; update player center vertically after landing",
        "Player push camera on getting too close to screen edge"
    ]

    rl.set_target_fps(60)

    while not rl.window_should_close():
        delta_time = rl.get_frame_time()

        update_player(player, env_items, delta_time)

        mouse_wheel_move = rl.get_mouse_wheel_move()
        camera.zoom += mouse_wheel_move * 0.05
        camera.zoom = rl.clamp(camera.zoom, 0.25, 3.0)

        if rl.is_key_pressed(rl.KEY_R):
            camera.zoom = 1.0
            player.position = rl.Vector2(400, 280)
        
        if rl.is_key_pressed(rl.KEY_C):
            camera_option = (camera_option + 1) % len(camera_updaters)

        camera_updaters[camera_option](camera, player, env_items, delta_time, screen_width, screen_height)

        rl.begin_drawing()
        rl.clear_background(rl.LIGHTGRAY)

        rl.begin_mode_2d(camera)
        for item in env_items:
            rl.draw_rectangle_rec(item.rect, item.color)

        player_rect = rl.Rectangle(player.position.x - 20, player.position.y - 40, 40, 40)
        rl.draw_rectangle_rec(player_rect, rl.RED)
        # Draw a small circle at player's actual position for reference
        rl.draw_circle_v(player.position, 5, rl.GOLD)


        rl.end_mode_2d()

        rl.draw_text("Controls:", 20, 20, 10, rl.BLACK)
        rl.draw_text("- Right/Left to move", 40, 40, 10, rl.DARKGRAY)
        rl.draw_text("- Space to jump", 40, 60, 10, rl.DARKGRAY)
        rl.draw_text("- Mouse Wheel to Zoom in-out, R to reset zoom", 40, 80, 10, rl.DARKGRAY)
        rl.draw_text("- C to change camera mode", 40, 100, 10, rl.DARKGRAY)
        rl.draw_text("Current camera mode:", 20, 120, 10, rl.BLACK)
        rl.draw_text(camera_descriptions[camera_option], 40, 140, 10, rl.DARKGRAY)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
