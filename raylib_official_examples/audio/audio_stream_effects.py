"""raylib [audio] example - Music stream processing effects
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 4.2, last time updated with raylib 5.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2022-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import ctypes
from pathlib import Path

# Get the directory where this script is located
THIS_DIR = Path(__file__).resolve().parent

# Required delay effect variables
delay_buffer = None
delay_buffer_size = 0
delay_read_index = 2
delay_write_index = 0

low = [0.0, 0.0]

# Audio effect: lowpass filter
@ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint)
def audio_process_effect_lpf(buffer, frames):
    global low

    cutoff = 70.0 / 44100.0  # 70 Hz lowpass filter
    k = cutoff / (cutoff + 0.1591549431)  # RC filter formula

    # Converts the buffer data before using it
    buffer_data = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_float))
    
    for i in range(0, frames * 2, 2):
        l = buffer_data[i]
        r = buffer_data[i + 1]

        low[0] += k * (l - low[0])
        low[1] += k * (r - low[1])
        
        buffer_data[i] = low[0]
        buffer_data[i + 1] = low[1]

# Audio effect: delay
@ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint)
def audio_process_effect_delay(buffer, frames):
    global delay_buffer, delay_buffer_size, delay_read_index, delay_write_index
    
    buffer_data = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_float))
    
    for i in range(0, frames * 2, 2):
        left_delay = delay_buffer[delay_read_index]
        delay_read_index += 1
        right_delay = delay_buffer[delay_read_index]
        delay_read_index += 1

        if delay_read_index == delay_buffer_size:
            delay_read_index = 0

        buffer_data[i] = 0.5 * buffer_data[i] + 0.5 * left_delay
        buffer_data[i + 1] = 0.5 * buffer_data[i + 1] + 0.5 * right_delay

        delay_buffer[delay_write_index] = buffer_data[i]
        delay_write_index += 1
        delay_buffer[delay_write_index] = buffer_data[i + 1]
        delay_write_index += 1
        
        if delay_write_index == delay_buffer_size:
            delay_write_index = 0

# Initialization
#--------------------------------------------------------------------------------------
screen_width = 800
screen_height = 450

rl.init_window(screen_width, screen_height, "raylib [audio] example - stream effects")

rl.init_audio_device()              # Initialize audio device

music = rl.load_music_stream(str(THIS_DIR/"resources/country.mp3"))

# Allocate buffer for the delay effect
delay_buffer_size = 48000 * 2      # 1 second delay (device sampleRate*channels)
delay_buffer = (ctypes.c_float * delay_buffer_size)()  # Create ctypes array of floats

rl.play_music_stream(music)

time_played = 0.0        # Time played normalized [0.0..1.0]
pause = False            # Music playing paused

enable_effect_lpf = False    # Enable effect low-pass-filter
enable_effect_delay = False  # Enable effect delay (1 second)

rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
#--------------------------------------------------------------------------------------

# Main game loop
while not rl.window_should_close():    # Detect window close button or ESC key
    # Update
    #----------------------------------------------------------------------------------
    rl.update_music_stream(music)   # Update music buffer with new stream data

    # Restart music playing (stop and play)
    if rl.is_key_pressed(rl.KEY_SPACE):
        rl.stop_music_stream(music)
        rl.play_music_stream(music)

    # Pause/Resume music playing
    if rl.is_key_pressed(rl.KEY_P):
        pause = not pause

        if pause:
            rl.pause_music_stream(music)
        else:
            rl.resume_music_stream(music)

    # Add/Remove effect: lowpass filter
    if rl.is_key_pressed(rl.KEY_F):
        enable_effect_lpf = not enable_effect_lpf
        if enable_effect_lpf:
            rl.attach_audio_stream_processor(music.stream, audio_process_effect_lpf)
        else:
            rl.detach_audio_stream_processor(music.stream, audio_process_effect_lpf)

    # Add/Remove effect: delay
    if rl.is_key_pressed(rl.KEY_D):
        enable_effect_delay = not enable_effect_delay
        if enable_effect_delay:
            rl.attach_audio_stream_processor(music.stream, audio_process_effect_delay)
        else:
            rl.detach_audio_stream_processor(music.stream, audio_process_effect_delay)
    
    # Get normalized time played for current music stream
    time_played = rl.get_music_time_played(music) / rl.get_music_time_length(music)

    if time_played > 1.0:
        time_played = 1.0   # Make sure time played is no longer than music
    #----------------------------------------------------------------------------------

    # Draw
    #----------------------------------------------------------------------------------
    rl.begin_drawing()

    rl.clear_background(rl.RAYWHITE)

    rl.draw_text("MUSIC SHOULD BE PLAYING!", 245, 150, 20, rl.LIGHTGRAY)

    rl.draw_rectangle(200, 180, 400, 12, rl.LIGHTGRAY)
    rl.draw_rectangle(200, 180, int(time_played * 400.0), 12, rl.MAROON)
    rl.draw_rectangle_lines(200, 180, 400, 12, rl.GRAY)

    rl.draw_text("PRESS SPACE TO RESTART MUSIC", 215, 230, 20, rl.LIGHTGRAY)
    rl.draw_text("PRESS P TO PAUSE/RESUME MUSIC", 208, 260, 20, rl.LIGHTGRAY)
    
    rl.draw_text(f"PRESS F TO TOGGLE LPF EFFECT: {'ON' if enable_effect_lpf else 'OFF'}", 200, 320, 20, rl.GRAY)
    rl.draw_text(f"PRESS D TO TOGGLE DELAY EFFECT: {'ON' if enable_effect_delay else 'OFF'}", 180, 350, 20, rl.GRAY)

    rl.end_drawing()
    #----------------------------------------------------------------------------------

# De-Initialization
#--------------------------------------------------------------------------------------
rl.unload_music_stream(music)   # Unload music stream buffers from RAM

rl.close_audio_device()         # Close audio device (music streaming is automatically stopped)

# No need to free delay_buffer in Python as garbage collection will handle it

rl.close_window()               # Close window and OpenGL context
#--------------------------------------------------------------------------------------