"""raylib [audio] example - Raw audio streaming
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 1.6, last time updated with raylib 4.2
Example created by Ramon Santamaria (@raysan5) and reviewed by James Hofmann (@triplefox)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5) and James Hofmann (@triplefox)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path
import ctypes

THIS_DIR = Path(__file__).resolve().parent

# Constants
MAX_SAMPLES = 512
MAX_SAMPLES_PER_UPDATE = 4096

# Cycles per second (hz)
frequency = 440.0

# Audio frequency, for smoothing
audio_frequency = 440.0

# Previous value, used to test if sine needs to be rewritten, and to smoothly modulate frequency
old_frequency = 1.0

# Index for audio rendering
sine_idx = 0.0

# Audio input processing callback
def audio_input_callback(buffer, frames):
    global audio_frequency, frequency, sine_idx
    
    audio_frequency = frequency + (audio_frequency - frequency) * 0.95
    
    incr = audio_frequency / 44100.0
    
    d = rl.ffi.cast("short *", buffer)
    
    for i in range(frames):
        d[i] = int(32000.0 * math.sin(2 * math.pi * sine_idx))
        sine_idx += incr
        if sine_idx > 1.0:
            sine_idx -= 1.0

# Main function
def main():
    global frequency, old_frequency
    
    # Initialization
    screen_width = 800
    screen_height = 450
    
    rl.init_window(screen_width, screen_height, "raylib [audio] example - raw audio streaming")
    
    rl.init_audio_device()  # Initialize audio device
    
    rl.set_audio_stream_buffer_size_default(MAX_SAMPLES_PER_UPDATE)
    
    # Init raw audio stream (sample rate: 44100, sample size: 16bit-short, channels: 1-mono)
    stream = rl.load_audio_stream(44100, 16, 1)
    
    # Set the callback using the correct function from PyRay
    # rl.ffi.callback() creates a trampoline to convert the C function call done by raylib to a python function call.
    c_audio_input_callback = rl.ffi.callback("void(void*, unsigned int)")(audio_input_callback)
    rl.set_audio_stream_callback(stream, c_audio_input_callback)
    
    # Buffer for the single cycle waveform we are synthesizing
    data = (ctypes.c_short * MAX_SAMPLES)()
    
    # Frame buffer, describing the waveform when repeated over the course of a frame
    write_buf = (ctypes.c_short * MAX_SAMPLES_PER_UPDATE)()
    
    rl.play_audio_stream(stream)  # Start processing stream buffer (no data loaded currently)
    
    # Position read in to determine next frequency
    mouse_position = rl.Vector2(-100.0, -100.0)
    
    # Computed size in samples of the sine wave
    wave_length = 1
    
    position = rl.Vector2(0, 0)
    
    rl.set_target_fps(30)  # Set our game to run at 30 frames-per-second
    
    # Main game loop
    while not rl.window_should_close():
        # Update
        mouse_position = rl.get_mouse_position()
        
        if rl.is_mouse_button_down(rl.MouseButton.MOUSE_BUTTON_LEFT):
            fp = float(mouse_position.y)
            frequency = 40.0 + float(fp)
            
            pan = float(mouse_position.x) / float(screen_width)
            rl.set_audio_stream_pan(stream, pan)
        
        # Rewrite the sine wave
        # Compute two cycles to allow the buffer padding, simplifying any modulation, resampling, etc.
        if frequency != old_frequency:
            # Compute wavelength. Limit size in both directions.
            wave_length = int(22050 / frequency)
            if wave_length > MAX_SAMPLES / 2:
                wave_length = MAX_SAMPLES // 2
            if wave_length < 1:
                wave_length = 1
            
            # Write sine wave
            for i in range(wave_length * 2):
                data[i] = int(math.sin(((2 * math.pi * float(i) / wave_length))) * 32000)
            
            # Make sure the rest of the line is flat
            for j in range(wave_length * 2, MAX_SAMPLES):
                data[j] = 0
            
            old_frequency = frequency
        
        # Draw
        rl.begin_drawing()
        
        rl.clear_background(rl.RAYWHITE)
        
        rl.draw_text(f"sine frequency: {int(frequency)}", screen_width - 220, 10, 20, rl.RED)
        rl.draw_text("click mouse button to change frequency or pan", 10, 10, 20, rl.DARKGRAY)
        
        # Draw the current buffer state proportionate to the screen
        for i in range(screen_width):
            position.x = float(i)
            position.y = 250 + 50 * data[i * MAX_SAMPLES // screen_width] / 32000.0
            
            rl.draw_pixel_v(position, rl.RED)
        
        rl.end_drawing()
    
    # De-Initialization
    rl.unload_audio_stream(stream)  # Close raw audio stream and delete buffers from RAM
    rl.close_audio_device()         # Close audio device
    
    rl.close_window()               # Close window and OpenGL context

if __name__ == "__main__":
    main()