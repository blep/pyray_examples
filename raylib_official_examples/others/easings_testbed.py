"""raylib [easings] example - Easings Testbed
Example originally created with raylib 2.5, last time updated with raylib 2.5
Example complexity rating: [★★★☆] 3/4
Example contributed by Juan Miguel López (@flashback-fx) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Juan Miguel López (@flashback-fx) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Constants
FONT_SIZE = 20

D_STEP = 20.0
D_STEP_FINE = 2.0
D_MIN = 1.0
D_MAX = 10000.0

# Easing types
EASE_LINEAR_NONE = 0
EASE_LINEAR_IN = 1
EASE_LINEAR_OUT = 2
EASE_LINEAR_IN_OUT = 3
EASE_SINE_IN = 4
EASE_SINE_OUT = 5
EASE_SINE_IN_OUT = 6
EASE_CIRC_IN = 7
EASE_CIRC_OUT = 8
EASE_CIRC_IN_OUT = 9
EASE_CUBIC_IN = 10
EASE_CUBIC_OUT = 11
EASE_CUBIC_IN_OUT = 12
EASE_QUAD_IN = 13
EASE_QUAD_OUT = 14
EASE_QUAD_IN_OUT = 15
EASE_EXPO_IN = 16
EASE_EXPO_OUT = 17
EASE_EXPO_IN_OUT = 18
EASE_BACK_IN = 19
EASE_BACK_OUT = 20
EASE_BACK_IN_OUT = 21
EASE_BOUNCE_OUT = 22
EASE_BOUNCE_IN = 23
EASE_BOUNCE_IN_OUT = 24
EASE_ELASTIC_IN = 25
EASE_ELASTIC_OUT = 26
EASE_ELASTIC_IN_OUT = 27
NUM_EASING_TYPES = 28
EASING_NONE = NUM_EASING_TYPES

def no_ease(t, b, c, d):
    """NoEase function, used when "no easing" is selected for any axis. It just returns the base value."""
    # Burn unused parameters to avoid compiler warnings
    burn = t + b + c + d
    d += burn
    return b

# Define a list of easing functions and their names
easings = [
    {"name": "EaseLinearNone", "func": rl.ease_linear_none},
    {"name": "EaseLinearIn", "func": rl.ease_linear_in},
    {"name": "EaseLinearOut", "func": rl.ease_linear_out},
    {"name": "EaseLinearInOut", "func": rl.ease_linear_in_out},
    {"name": "EaseSineIn", "func": rl.ease_sine_in},
    {"name": "EaseSineOut", "func": rl.ease_sine_out},
    {"name": "EaseSineInOut", "func": rl.ease_sine_in_out},
    {"name": "EaseCircIn", "func": rl.ease_circ_in},
    {"name": "EaseCircOut", "func": rl.ease_circ_out},
    {"name": "EaseCircInOut", "func": rl.ease_circ_in_out},
    {"name": "EaseCubicIn", "func": rl.ease_cubic_in},
    {"name": "EaseCubicOut", "func": rl.ease_cubic_out},
    {"name": "EaseCubicInOut", "func": rl.ease_cubic_in_out},
    {"name": "EaseQuadIn", "func": rl.ease_quad_in},
    {"name": "EaseQuadOut", "func": rl.ease_quad_out},
    {"name": "EaseQuadInOut", "func": rl.ease_quad_in_out},
    {"name": "EaseExpoIn", "func": rl.ease_expo_in},
    {"name": "EaseExpoOut", "func": rl.ease_expo_out},
    {"name": "EaseExpoInOut", "func": rl.ease_expo_in_out},
    {"name": "EaseBackIn", "func": rl.ease_back_in},
    {"name": "EaseBackOut", "func": rl.ease_back_out},
    {"name": "EaseBackInOut", "func": rl.ease_back_in_out},
    {"name": "EaseBounceOut", "func": rl.ease_bounce_out},
    {"name": "EaseBounceIn", "func": rl.ease_bounce_in},
    {"name": "EaseBounceInOut", "func": rl.ease_bounce_in_out},
    {"name": "EaseElasticIn", "func": rl.ease_elastic_in},
    {"name": "EaseElasticOut", "func": rl.ease_elastic_out},
    {"name": "EaseElasticInOut", "func": rl.ease_elastic_in_out},
    {"name": "None", "func": no_ease}
]

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [easings] example - easings testbed")

    ball_position = rl.Vector2(100.0, 100.0)

    t = 0.0        # Current time (in any unit measure, but same unit as duration)
    d = 300.0      # Total time it should take to complete (duration)
    paused = True
    bounded_t = True  # If true, t will stop when d >= td, otherwise t will keep adding td to its value every loop

    easing_x = EASING_NONE  # Easing selected for x axis
    easing_y = EASING_NONE  # Easing selected for y axis

    rl.set_target_fps(60)

    # Main game loop
    while not rl.window_should_close():
        # Update
        if rl.is_key_pressed(rl.KEY_T):
            bounded_t = not bounded_t

        # Choose easing for the X axis
        if rl.is_key_pressed(rl.KEY_RIGHT):
            easing_x += 1
            if easing_x > EASING_NONE:
                easing_x = 0
        elif rl.is_key_pressed(rl.KEY_LEFT):
            if easing_x == 0:
                easing_x = EASING_NONE
            else:
                easing_x -= 1

        # Choose easing for the Y axis
        if rl.is_key_pressed(rl.KEY_DOWN):
            easing_y += 1
            if easing_y > EASING_NONE:
                easing_y = 0
        elif rl.is_key_pressed(rl.KEY_UP):
            if easing_y == 0:
                easing_y = EASING_NONE
            else:
                easing_y -= 1

        # Change d (duration) value
        if rl.is_key_pressed(rl.KEY_W) and d < D_MAX - D_STEP:
            d += D_STEP
        elif rl.is_key_pressed(rl.KEY_Q) and d > D_MIN + D_STEP:
            d -= D_STEP

        if rl.is_key_down(rl.KEY_S) and d < D_MAX - D_STEP_FINE:
            d += D_STEP_FINE
        elif rl.is_key_down(rl.KEY_A) and d > D_MIN + D_STEP_FINE:
            d -= D_STEP_FINE

        # Play, pause and restart controls
        if (rl.is_key_pressed(rl.KEY_SPACE) or rl.is_key_pressed(rl.KEY_T) or
            rl.is_key_pressed(rl.KEY_RIGHT) or rl.is_key_pressed(rl.KEY_LEFT) or
            rl.is_key_pressed(rl.KEY_DOWN) or rl.is_key_pressed(rl.KEY_UP) or
            rl.is_key_pressed(rl.KEY_W) or rl.is_key_pressed(rl.KEY_Q) or
            rl.is_key_down(rl.KEY_S) or rl.is_key_down(rl.KEY_A) or
            (rl.is_key_pressed(rl.KEY_ENTER) and bounded_t and t >= d)):
            
            t = 0.0
            ball_position.x = 100.0
            ball_position.y = 100.0
            paused = True

        if rl.is_key_pressed(rl.KEY_ENTER):
            paused = not paused

        # Movement computation
        if not paused and ((bounded_t and t < d) or not bounded_t):
            ball_position.x = easings[easing_x]["func"](t, 100.0, 700.0 - 170.0, d)
            ball_position.y = easings[easing_y]["func"](t, 100.0, 400.0 - 170.0, d)
            t += 1.0

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # Draw information text
        rl.draw_text(f"Easing x: {easings[easing_x]['name']}", 20, FONT_SIZE, FONT_SIZE, rl.LIGHTGRAY)
        rl.draw_text(f"Easing y: {easings[easing_y]['name']}", 20, FONT_SIZE*2, FONT_SIZE, rl.LIGHTGRAY)
        rl.draw_text(f"t ({'b' if bounded_t else 'u'}) = {t:.2f} d = {d:.2f}", 20, FONT_SIZE*3, FONT_SIZE, rl.LIGHTGRAY)

        # Draw instructions text
        rl.draw_text("Use ENTER to play or pause movement, use SPACE to restart", 20, 
                  rl.get_screen_height() - FONT_SIZE*2, FONT_SIZE, rl.LIGHTGRAY)
        rl.draw_text("Use Q and W or A and S keys to change duration", 20, 
                  rl.get_screen_height() - FONT_SIZE*3, FONT_SIZE, rl.LIGHTGRAY)
        rl.draw_text("Use LEFT or RIGHT keys to choose easing for the x axis", 20, 
                  rl.get_screen_height() - FONT_SIZE*4, FONT_SIZE, rl.LIGHTGRAY)
        rl.draw_text("Use UP or DOWN keys to choose easing for the y axis", 20, 
                  rl.get_screen_height() - FONT_SIZE*5, FONT_SIZE, rl.LIGHTGRAY)

        # Draw ball
        rl.draw_circle_v(ball_position, 16.0, rl.MAROON)

        rl.end_drawing()

    # De-Initialization
    rl.close_window()

if __name__ == "__main__":
    main()
