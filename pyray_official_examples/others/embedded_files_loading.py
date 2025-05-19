"""raylib [others] example - Embedded files loading (Wave and Image)
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 3.0, last time updated with raylib 2.5
Example contributed by Kristian Holmgren (@defutura) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2020-2025 Kristian Holmgren (@defutura) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Note: In Python version, we're not using embedded files in the same way as the C version
# Instead we'll load from the resources directory

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [others] example - embedded files loading")

    rl.init_audio_device()  # Initialize audio device

    # In the C version, these are loaded from header files
    # In our Python version, we'll load from actual files instead
    audio_path = THIS_DIR / "../resources/country.mp3"
    image_path = THIS_DIR / "../resources/raylib_logo.png"
    
    # Load sound and image
    sound = rl.load_sound(str(audio_path))
    texture = rl.load_texture(str(image_path))
    
    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    
    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        if rl.is_key_pressed(rl.KEY_SPACE):
            rl.play_sound(sound)  # Play sound
            
        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        
        rl.draw_texture(texture, screen_width//2 - texture.width//2, 40, rl.WHITE)
        
        rl.draw_text("raylib logo and sound loaded from files", 150, 320, 20, rl.LIGHTGRAY)
        rl.draw_text("Press SPACE to PLAY the sound!", 220, 370, 20, rl.LIGHTGRAY)
        
        rl.end_drawing()
        
    # De-Initialization
    rl.unload_sound(sound)     # Unload sound
    rl.unload_texture(texture)  # Unload texture
    
    rl.close_audio_device()    # Close audio device
    rl.close_window()          # Close window and OpenGL context

if __name__ == "__main__":
    main()
