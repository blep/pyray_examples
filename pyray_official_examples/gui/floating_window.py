"""
raygui - floating window example

DEPENDENCIES:
   pyray - Python wrapper for raylib
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Window states
window_position = rl.Vector2(10, 10)
window_size = rl.Vector2(200, 400)
minimized = False
moving = False
resizing = False
scroll = rl.Vector2(0, 0)

window2_position = rl.Vector2(250, 10)
window2_size = rl.Vector2(200, 400)
minimized2 = False
moving2 = False
resizing2 = False
scroll2 = rl.Vector2(0, 0)

def gui_window_floating(position, size, minimized, moving, resizing, draw_content, content_size, scroll, title):
    """
    Custom function to create a floating, resizable window
    
    Parameters:
    position - Vector2 with window position
    size - Vector2 with window size
    minimized - Boolean reference (in Python we'll need to use a list to pass by reference)
    moving - Boolean reference
    resizing - Boolean reference
    draw_content - Callback function that draws content
    content_size - Vector2 with content size
    scroll - Vector2 reference for scroll position
    title - Window title string
    """
    # Define constants that might be missing
    RAYGUI_WINDOWBOX_STATUSBAR_HEIGHT = 24
    RAYGUI_WINDOW_CLOSEBUTTON_SIZE = 18

    close_title_size_delta_half = (RAYGUI_WINDOWBOX_STATUSBAR_HEIGHT - RAYGUI_WINDOW_CLOSEBUTTON_SIZE) // 2

    # Window movement and resize input and collision check
    if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON) and not moving[0] and not resizing[0]:
        mouse_position = rl.get_mouse_position()

        title_collision_rect = rl.Rectangle(position.x, position.y, 
                                           size.x - (RAYGUI_WINDOW_CLOSEBUTTON_SIZE + close_title_size_delta_half), 
                                           RAYGUI_WINDOWBOX_STATUSBAR_HEIGHT)
        resize_collision_rect = rl.Rectangle(position.x + size.x - 20, position.y + size.y - 20, 20, 20)

        if rl.check_collision_point_rec(mouse_position, title_collision_rect):
            moving[0] = True
        elif not minimized[0] and rl.check_collision_point_rec(mouse_position, resize_collision_rect):
            resizing[0] = True

    # Window movement and resize update
    if moving[0]:
        mouse_delta = rl.get_mouse_delta()
        position.x += mouse_delta.x
        position.y += mouse_delta.y

        if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON):
            moving[0] = False

            # Clamp window position to keep it inside the application area
            if position.x < 0:
                position.x = 0
            elif position.x > rl.get_screen_width() - size.x:
                position.x = rl.get_screen_width() - size.x
            if position.y < 0:
                position.y = 0
            elif position.y > rl.get_screen_height():
                position.y = rl.get_screen_height() - RAYGUI_WINDOWBOX_STATUSBAR_HEIGHT

    elif resizing[0]:
        mouse = rl.get_mouse_position()
        if mouse.x > position.x:
            size.x = mouse.x - position.x
        if mouse.y > position.y:
            size.y = mouse.y - position.y

        # Clamp window size to an arbitrary minimum value and the window size as the maximum
        if size.x < 100:
            size.x = 100
        elif size.x > rl.get_screen_width():
            size.x = rl.get_screen_width()
        if size.y < 100:
            size.y = 100
        elif size.y > rl.get_screen_height():
            size.y = rl.get_screen_height()

        if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON):
            resizing[0] = False

    # Window and content drawing with scissor and scroll area
    if minimized[0]:
        rl.gui_status_bar(rl.Rectangle(position.x, position.y, size.x, RAYGUI_WINDOWBOX_STATUSBAR_HEIGHT), title)

        if rl.gui_button(rl.Rectangle(position.x + size.x - RAYGUI_WINDOW_CLOSEBUTTON_SIZE - close_title_size_delta_half,
                                    position.y + close_title_size_delta_half,
                                    RAYGUI_WINDOW_CLOSEBUTTON_SIZE,
                                    RAYGUI_WINDOW_CLOSEBUTTON_SIZE),
                                    "#120#"):
            minimized[0] = False

    else:
        minimized[0] = rl.gui_window_box(rl.Rectangle(position.x, position.y, size.x, size.y), title)

        # Scissor and draw content within a scroll panel
        if draw_content is not None:
            scissor = rl.Rectangle(0, 0, 0, 0)
            rl.gui_scroll_panel(rl.Rectangle(position.x, position.y + RAYGUI_WINDOWBOX_STATUSBAR_HEIGHT, 
                                           size.x, size.y - RAYGUI_WINDOWBOX_STATUSBAR_HEIGHT),
                              "",
                              rl.Rectangle(position.x, position.y, content_size.x, content_size.y),
                              scroll,
                              scissor)

            require_scissor = size.x < content_size.x or size.y < content_size.y

            if require_scissor:
                rl.begin_scissor_mode(int(scissor.x), int(scissor.y), int(scissor.width), int(scissor.height))

            draw_content(position, scroll)

            if require_scissor:
                rl.end_scissor_mode()

        # Draw the resize button/icon
        rl.gui_draw_icon(71, int(position.x + size.x - 20), int(position.y + size.y - 20), 1, rl.WHITE)

def draw_content(position, scroll):
    """Draw content inside the window"""
    rl.gui_button(rl.Rectangle(position.x + 20 + scroll.x, position.y + 50 + scroll.y, 100, 25), "Button 1")
    rl.gui_button(rl.Rectangle(position.x + 20 + scroll.x, position.y + 100 + scroll.y, 100, 25), "Button 2")
    rl.gui_button(rl.Rectangle(position.x + 20 + scroll.x, position.y + 150 + scroll.y, 100, 25), "Button 3")
    rl.gui_label(rl.Rectangle(position.x + 20 + scroll.x, position.y + 200 + scroll.y, 250, 25), "A Label")
    rl.gui_label(rl.Rectangle(position.x + 20 + scroll.x, position.y + 250 + scroll.y, 250, 25), "Another Label")
    rl.gui_label(rl.Rectangle(position.x + 20 + scroll.x, position.y + 300 + scroll.y, 250, 25), "Yet Another Label")

def main():
    global minimized, moving, resizing, minimized2, moving2, resizing2

    # Initialization
    rl.init_window(960, 560, "raygui - floating window example")
    rl.set_target_fps(60)
    # TODO gui_load_style_dark() does not seemed to be exposed... Commented out to work-around it
    # rl.gui_load_style_dark()

    # In Python we need to use lists for the boolean references to work as pass-by-reference
    minimized_ref = [minimized]
    moving_ref = [moving]
    resizing_ref = [resizing]
    
    minimized2_ref = [minimized2]
    moving2_ref = [moving2]
    resizing2_ref = [resizing2]

    while not rl.window_should_close():
        # Draw
        rl.begin_drawing()
        
        rl.clear_background(rl.DARKGREEN)
        
        # Draw floating windows
        gui_window_floating(window_position, window_size, minimized_ref, moving_ref, resizing_ref, 
                           draw_content, rl.Vector2(140, 320), scroll, "Movable & Scalable Window")
        
        gui_window_floating(window2_position, window2_size, minimized2_ref, moving2_ref, resizing2_ref, 
                           draw_content, rl.Vector2(140, 320), scroll2, "Another window")
        
        rl.end_drawing()
        
        # Update the global variables
        minimized = minimized_ref[0]
        moving = moving_ref[0]
        resizing = resizing_ref[0]
        
        minimized2 = minimized2_ref[0]
        moving2 = moving2_ref[0]
        resizing2 = resizing2_ref[0]

    # De-Initialization
    rl.close_window()

# Execute the main function
if __name__ == '__main__':
    main()
