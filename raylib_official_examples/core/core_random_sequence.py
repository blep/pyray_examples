"""raylib [core] example - Generates a random sequence
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 5.0, last time updated with raylib 5.0
Example contributed by Dalton Overmyer (@REDl3east) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Dalton Overmyer (@REDl3east)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import random

class ColorRect:
    def __init__(self, c, r):
        self.c = c
        self.r = r

def generate_random_color():
    return rl.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

def generate_random_color_rect_sequence(rect_count, rect_width, screen_width, screen_height):
    rectangles = []
    # In Python, LoadRandomSequence is not directly available in pyray.
    # We can achieve a similar effect for heights by shuffling a list of possible heights.
    # For this example, we'll generate random heights directly for simplicity, similar to original logic's remapping effect.
    
    # The original C code uses LoadRandomSequence to determine the height of each rectangle.
    # seq = rl.load_random_sequence(rect_count, 0, rect_count - 1) # This function does not exist in pyray
    # For a Pythonic equivalent, we can shuffle a list of indices or generate random heights.
    # Let's generate random heights based on a sequence for a similar visual effect.
    
    possible_height_indices = list(range(rect_count))
    random.shuffle(possible_height_indices)

    rect_seq_width = rect_count * rect_width
    start_x = (screen_width - rect_seq_width) * 0.5

    for i in range(rect_count):
        # rect_height = int(rl.remap(float(seq[i]), 0, float(rect_count - 1), 0, float(screen_height)))
        # Simulating the remapping of a shuffled sequence for height:
        # We'll use the shuffled index to determine the height proportion.
        # A simpler approach for random heights within a range:
        # rect_height = random.randint(int(screen_height * 0.1), int(screen_height * 0.9))
        # To mimic the C example's distribution more closely (using shuffled indices for height steps):
        rect_height = int(rl.remap(float(possible_height_indices[i]), 0, float(rect_count -1), 0, float(screen_height)))
        if rect_height < 1: rect_height = 1 # Ensure minimum height

        color = generate_random_color()
        rect = rl.Rectangle(start_x + i * rect_width, screen_height - rect_height, rect_width, float(rect_height))
        rectangles.append(ColorRect(color, rect))
    
    # UnloadRandomSequence is not needed as we are managing the list in Python
    return rectangles

def shuffle_color_rect_sequence(rectangles, rect_count):
    # Similar to C, LoadRandomSequence is not in pyray.
    # We can shuffle indices to swap elements.
    indices = list(range(rect_count))
    random.shuffle(indices)

    # Create a temporary copy of relevant attributes (color and height aspects of rect)
    temp_rect_attrs = [(rect.c, rect.r.height, rect.r.y) for rect in rectangles]

    for i1 in range(rect_count):
        idx2 = indices[i1]
        
        # Get attributes from the target shuffle position
        original_c1, original_h1, original_y1 = temp_rect_attrs[i1]
        target_c2, target_h2, target_y2 = temp_rect_attrs[idx2]

        # Swap color and height-related properties
        rectangles[i1].c = target_c2
        rectangles[i1].r.height = target_h2
        rectangles[i1].r.y = target_y2

        # If i1 and idx2 are different, apply the original i1's properties to the target idx2's original position
        # This needs careful handling to ensure a correct shuffle. A simpler way is to create a new shuffled list.
        # However, to stick to the C example's in-place shuffle idea:
        # The C code swaps r1 and r2 (rectangles[i1] and rectangles[seq[i1]])
        # Let's try a direct swap of the ColorRect objects' relevant fields

    # A more Pythonic way to shuffle, keeping rectangle positions fixed but shuffling color and height:
    shuffled_colors_heights = [(rect.c, rect.r.height, rect.r.y) for rect in rectangles]
    random.shuffle(shuffled_colors_heights)

    for i in range(rect_count):
        rectangles[i].c = shuffled_colors_heights[i][0]
        rectangles[i].r.height = shuffled_colors_heights[i][1]
        rectangles[i].r.y = shuffled_colors_heights[i][2]

def draw_text_center_key_help(key, text, pos_x, pos_y, font_size, color):
    space_size = rl.measure_text(" ", font_size)
    press_size = rl.measure_text("Press ", font_size) # Added space for better look
    key_size = rl.measure_text(key, font_size)
    
    current_x = pos_x
    rl.draw_text("Press ", current_x, pos_y, font_size, color)
    current_x += press_size
    rl.draw_text(key, current_x, pos_y, font_size, rl.RED)
    rl.draw_rectangle(current_x, pos_y + font_size, key_size, 3, rl.RED)
    current_x += key_size + space_size # Added one space_size
    rl.draw_text(text, current_x, pos_y, font_size, color)

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - Generates a random sequence")

    rect_count = 20
    rect_size = float(screen_width) / rect_count
    rectangles = generate_random_color_rect_sequence(rect_count, rect_size, float(screen_width), 0.75 * screen_height)

    rl.set_target_fps(60)
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
            shuffle_color_rect_sequence(rectangles, rect_count)

        if rl.is_key_pressed(rl.KeyboardKey.KEY_UP):
            rect_count += 1
            rect_size = float(screen_width) / rect_count
            rectangles = generate_random_color_rect_sequence(rect_count, rect_size, float(screen_width), 0.75 * screen_height)

        if rl.is_key_pressed(rl.KeyboardKey.KEY_DOWN):
            if rect_count >= 4:
                rect_count -= 1
                rect_size = float(screen_width) / rect_count
                rectangles = generate_random_color_rect_sequence(rect_count, rect_size, float(screen_width), 0.75 * screen_height)
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        font_size = 20
        for i in range(rect_count):
            rl.draw_rectangle_rec(rectangles[i].r, rectangles[i].c)
        
        draw_text_center_key_help("SPACE", "to shuffle the sequence.", 10, screen_height - 96, font_size, rl.BLACK)
        draw_text_center_key_help("UP", "to add a rectangle and generate a new sequence.", 10, screen_height - 64, font_size, rl.BLACK)
        draw_text_center_key_help("DOWN", "to remove a rectangle and generate a new sequence.", 10, screen_height - 32, font_size, rl.BLACK)

        rect_count_text = f"{rect_count} rectangles"
        rect_count_text_size = rl.measure_text(rect_count_text, font_size)
        rl.draw_text(rect_count_text, screen_width - rect_count_text_size - 10, 10, font_size, rl.BLACK)

        rl.draw_fps(10, 10)
        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    # Python's garbage collector handles memory for `rectangles` list and objects
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
