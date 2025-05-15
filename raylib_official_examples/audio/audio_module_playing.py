"""raylib [audio] example - Module playing (streaming)
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.5, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2016-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import random
from pathlib import Path

MAX_CIRCLES = 64

THIS_DIR = Path(__file__).resolve().parent

class CircleWave:
    def __init__(self):
        self.position = rl.Vector2(0, 0)
        self.radius = 0.0
        self.alpha = 0.0
        self.speed = 0.0
        self.color = rl.BLANK

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)  # NOTE: Try to enable MSAA 4X
    rl.init_window(screen_width, screen_height, "raylib [audio] example - module playing (streaming)")
    rl.init_audio_device()  # Initialize audio device

    colors = [rl.ORANGE, rl.RED, rl.GOLD, rl.LIME, rl.BLUE, rl.VIOLET, rl.BROWN, rl.LIGHTGRAY, rl.PINK,
              rl.YELLOW, rl.GREEN, rl.SKYBLUE, rl.PURPLE, rl.BEIGE]

    # Creates some circles for visual effect
    circles = [CircleWave() for _ in range(MAX_CIRCLES)]

    for i in range(MAX_CIRCLES - 1, -1, -1):
        circles[i].alpha = 0.0
        circles[i].radius = float(random.randint(10, 40))
        circles[i].position.x = float(random.randint(int(circles[i].radius), int(screen_width - circles[i].radius)))
        circles[i].position.y = float(random.randint(int(circles[i].radius), int(screen_height - circles[i].radius)))
        circles[i].speed = float(random.randint(1, 100)) / 2000.0
        circles[i].color = colors[random.randint(0, 13)]

    music = rl.load_music_stream(str(THIS_DIR/"resources/mini1111.xm"))
    music.looping = False
    pitch = 1.0

    rl.play_music_stream(music)

    time_played = 0.0
    pause = False

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        rl.update_music_stream(music)  # Update music buffer with new stream data

        # Restart music playing (stop and play)
        if rl.is_key_pressed(rl.KEY_SPACE):
            rl.stop_music_stream(music)
            rl.play_music_stream(music)
            pause = False

        # Pause/Resume music playing
        if rl.is_key_pressed(rl.KEY_P):
            pause = not pause
            if pause:
                rl.pause_music_stream(music)
            else:
                rl.resume_music_stream(music)

        if rl.is_key_down(rl.KEY_DOWN):
            pitch -= 0.01
        elif rl.is_key_down(rl.KEY_UP):
            pitch += 0.01

        rl.set_music_pitch(music, pitch)

        # Get timePlayed scaled to bar dimensions
        if rl.get_music_time_length(music) > 0: # Avoid division by zero
            time_played = rl.get_music_time_played(music) / rl.get_music_time_length(music) * (screen_width - 40)
        else:
            time_played = 0


        # Color circles animation
        for i in range(MAX_CIRCLES - 1, -1, -1):
            if not pause:
                circles[i].alpha += circles[i].speed
                circles[i].radius += circles[i].speed * 10.0

                if circles[i].alpha > 1.0:
                    circles[i].speed *= -1

                if circles[i].alpha <= 0.0:
                    circles[i].alpha = 0.0
                    circles[i].radius = float(random.randint(10, 40))
                    circles[i].position.x = float(random.randint(int(circles[i].radius), int(screen_width - circles[i].radius)))
                    circles[i].position.y = float(random.randint(int(circles[i].radius), int(screen_height - circles[i].radius)))
                    circles[i].color = colors[random.randint(0, 13)]
                    circles[i].speed = float(random.randint(1, 100)) / 2000.0

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        for i in range(MAX_CIRCLES - 1, -1, -1):
            rl.draw_circle_v(circles[i].position, circles[i].radius, rl.fade(circles[i].color, circles[i].alpha))

        # Draw time bar
        rl.draw_rectangle(20, screen_height - 20 - 12, screen_width - 40, 12, rl.LIGHTGRAY)
        rl.draw_rectangle(20, screen_height - 20 - 12, int(time_played), 12, rl.MAROON)
        rl.draw_rectangle_lines(20, screen_height - 20 - 12, screen_width - 40, 12, rl.GRAY)

        # Draw help instructions
        rl.draw_rectangle(20, 20, 425, 145, rl.WHITE)
        rl.draw_rectangle_lines(20, 20, 425, 145, rl.GRAY)
        rl.draw_text("PRESS SPACE TO RESTART MUSIC", 40, 40, 20, rl.BLACK)
        rl.draw_text("PRESS P TO PAUSE/RESUME", 40, 70, 20, rl.BLACK)
        rl.draw_text("PRESS UP/DOWN TO CHANGE SPEED", 40, 100, 20, rl.BLACK)
        rl.draw_text(f"SPEED: {pitch:.2f}", 40, 130, 20, rl.MAROON)

        rl.end_drawing()

    # De-Initialization
    rl.unload_music_stream(music)  # Unload music stream buffers from RAM
    rl.close_audio_device()  # Close audio device (music streaming is automatically stopped)
    rl.close_window()  # Close window and OpenGL context

if __name__ == '__main__':
    main()
