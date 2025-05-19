"""raylib [audio] example - Mixed audio processing
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 4.2, last time updated with raylib 4.2
Example contributed by hkc (@hatkidchan) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 hkc (@hatkidchan)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math

exponent = 1.0  # Audio exponentiation value
average_volume = [0.0] * 400  # Average volume history

# Audio processing function
def process_audio(buffer, frames):
    samples = rl.ffi.cast("float *", buffer)  # Samples internally stored as <float>s
    average = 0.0  # Temporary average volume

    for frame in range(frames):
        left = samples[frame * 2 + 0]
        right = samples[frame * 2 + 1]

        samples[frame * 2 + 0] = math.pow(math.fabs(left), exponent) * (-1.0 if left < 0.0 else 1.0)
        samples[frame * 2 + 1] = math.pow(math.fabs(right), exponent) * (-1.0 if right < 0.0 else 1.0)

        average += math.fabs(left) / frames  # accumulating average volume
        average += math.fabs(right) / frames

    # Moving history to the left
    for i in range(399):
        average_volume[i] = average_volume[i + 1]

    average_volume[399] = average  # Adding last average value

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [audio] example - processing mixed output")

    rl.init_audio_device()  # Initialize audio device

    rl.attach_audio_mixed_processor(process_audio)

    music = rl.load_music_stream("raylib_c_examples/audio/resources/country.mp3") # Adjusted path
    sound = rl.load_sound("raylib_c_examples/audio/resources/coin.wav") # Adjusted path

    rl.play_music_stream(music)

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

    global exponent # Declare exponent as global to modify it

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        rl.update_music_stream(music)  # Update music buffer with new stream data

        # Modify processing variables
        if rl.is_key_pressed(rl.KEY_LEFT):
            exponent -= 0.05
        if rl.is_key_pressed(rl.KEY_RIGHT):
            exponent += 0.05

        if exponent <= 0.5:
            exponent = 0.5
        if exponent >= 3.0:
            exponent = 3.0

        if rl.is_key_pressed(rl.KEY_SPACE):
            rl.play_sound(sound)

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("MUSIC SHOULD BE PLAYING!", 255, 150, 20, rl.LIGHTGRAY)

        rl.draw_text(f"EXPONENT = {exponent:.2f}", 215, 180, 20, rl.LIGHTGRAY)

        rl.draw_rectangle(199, 199, 402, 34, rl.LIGHTGRAY)
        for i in range(400):
            rl.draw_line(201 + i, 232 - int(average_volume[i] * 32), 201 + i, 232, rl.MAROON)
        rl.draw_rectangle_lines(199, 199, 402, 34, rl.GRAY)

        rl.draw_text("PRESS SPACE TO PLAY OTHER SOUND", 200, 250, 20, rl.LIGHTGRAY)
        rl.draw_text("USE LEFT AND RIGHT ARROWS TO ALTER DISTORTION", 140, 280, 20, rl.LIGHTGRAY)

        rl.end_drawing()

    # De-Initialization
    rl.unload_music_stream(music)  # Unload music stream buffers from RAM

    rl.detach_audio_mixed_processor(process_audio)  # Disconnect audio processor

    rl.close_audio_device()  # Close audio device (music streaming is automatically stopped)

    rl.close_window()  # Close window and OpenGL context

if __name__ == '__main__':
    main()
