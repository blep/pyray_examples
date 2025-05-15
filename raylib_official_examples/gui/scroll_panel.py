"""raygui - Controls test
TEST CONTROLS:
    - GuiScrollPanel()
DEPENDENCIES:
    raylib 4.0  - Windowing/input management and drawing.
    raygui 3.0  - Immediate-mode GUI controls.
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99
COMPILATION (Linux - gcc):
    gcc -o $(NAME_PART) $(FILE_NAME) -I../../src -lraylib -lGL -lm -lpthread -ldl -lrt -lX11 -std=c99
LICENSE: zlib/libpng
Copyright (c) 2019-2024 Vlad Adrian (@Demizdor) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Draw and process scroll bar style edition controls
def draw_style_edit_controls():
    # ScrollPanel style controls
    #----------------------------------------------------------
    rl.gui_group_box(rl.Rectangle(550, 170, 220, 205), "SCROLLBAR STYLE")

    # For spinner controls we need to handle return value
    style_value = rl.gui_get_style(rl.SCROLLBAR, rl.BORDER_WIDTH)
    style_ptr = rl.ffi.new('int *', style_value)
    rl.gui_label(rl.Rectangle(555, 195, 110, 10), "BORDER_WIDTH")
    rl.gui_spinner(rl.Rectangle(670, 190, 90, 20), "", style_ptr, 0, 6, False)
    rl.gui_set_style(rl.SCROLLBAR, rl.BORDER_WIDTH, style_ptr[0])

    style_value = rl.gui_get_style(rl.SCROLLBAR, rl.ARROWS_SIZE)
    style_ptr = rl.ffi.new('int *', style_value)
    rl.gui_label(rl.Rectangle(555, 220, 110, 10), "ARROWS_SIZE")
    rl.gui_spinner(rl.Rectangle(670, 215, 90, 20), "", style_ptr, 4, 14, False)
    rl.gui_set_style(rl.SCROLLBAR, rl.ARROWS_SIZE, style_ptr[0])

    style_value = rl.gui_get_style(rl.SCROLLBAR, rl.SLIDER_PADDING)
    style_ptr = rl.ffi.new('int *', style_value)
    rl.gui_label(rl.Rectangle(555, 245, 110, 10), "SLIDER_PADDING")
    rl.gui_spinner(rl.Rectangle(670, 240, 90, 20), "", style_ptr, 0, 14, False)
    rl.gui_set_style(rl.SCROLLBAR, rl.SLIDER_PADDING, style_ptr[0])

    scroll_bar_arrows_ptr = rl.ffi.new('bool *', bool(rl.gui_get_style(rl.SCROLLBAR, rl.ARROWS_VISIBLE)))
    rl.gui_check_box(rl.Rectangle(565, 280, 20, 20), "ARROWS_VISIBLE", scroll_bar_arrows_ptr)
    rl.gui_set_style(rl.SCROLLBAR, rl.ARROWS_VISIBLE, scroll_bar_arrows_ptr[0])

    style_value = rl.gui_get_style(rl.SCROLLBAR, rl.SLIDER_PADDING)
    style_ptr = rl.ffi.new('int *', style_value)
    rl.gui_label(rl.Rectangle(555, 325, 110, 10), "SLIDER_PADDING")
    rl.gui_spinner(rl.Rectangle(670, 320, 90, 20), "", style_ptr, 0, 14, False)
    rl.gui_set_style(rl.SCROLLBAR, rl.SLIDER_PADDING, style_ptr[0])

    style_value = rl.gui_get_style(rl.SCROLLBAR, rl.SLIDER_WIDTH)
    style_ptr = rl.ffi.new('int *', style_value)
    rl.gui_label(rl.Rectangle(555, 350, 110, 10), "SLIDER_WIDTH")
    rl.gui_spinner(rl.Rectangle(670, 345, 90, 20), "", style_ptr, 2, 100, False)
    rl.gui_set_style(rl.SCROLLBAR, rl.SLIDER_WIDTH, style_ptr[0])

    side_value = rl.gui_get_style(rl.LISTVIEW, rl.SCROLLBAR_SIDE)
    text = "SCROLLBAR: LEFT" if side_value == rl.SCROLLBAR_LEFT_SIDE else "SCROLLBAR: RIGHT"
    toggle_scrollbar_side_ptr = rl.ffi.new('bool *', side_value)
    rl.gui_toggle(rl.Rectangle(560, 110, 200, 35), text, toggle_scrollbar_side_ptr)
    rl.gui_set_style(rl.LISTVIEW, rl.SCROLLBAR_SIDE, toggle_scrollbar_side_ptr[0])
    #----------------------------------------------------------

    # ScrollBar style controls
    #----------------------------------------------------------
    rl.gui_group_box(rl.Rectangle(550, 20, 220, 135), "SCROLLPANEL STYLE")

    style_value = rl.gui_get_style(rl.LISTVIEW, rl.SCROLLBAR_WIDTH)
    style_ptr = rl.ffi.new('int *', style_value)
    rl.gui_label(rl.Rectangle(555, 35, 110, 10), "SCROLLBAR_WIDTH")
    rl.gui_spinner(rl.Rectangle(670, 30, 90, 20), "", style_ptr, 6, 30, False)
    rl.gui_set_style(rl.LISTVIEW, rl.SCROLLBAR_WIDTH, style_ptr[0])

    style_value = rl.gui_get_style(rl.DEFAULT, rl.BORDER_WIDTH)
    style_ptr = rl.ffi.new('int *', style_value)
    rl.gui_label(rl.Rectangle(555, 60, 110, 10), "BORDER_WIDTH")
    rl.gui_spinner(rl.Rectangle(670, 55, 90, 20), "", style_ptr, 0, 20, False)
    rl.gui_set_style(rl.DEFAULT, rl.BORDER_WIDTH, style_ptr[0])
    #----------------------------------------------------------

def main():
    # Initialization
    #---------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raygui - GuiScrollPanel()")

    panel_rec = rl.Rectangle(20, 40, 200, 150)
    panel_content_rec = rl.Rectangle(0, 0, 340, 340)
    panel_view = rl.Rectangle(0, 0, 0, 0)
    panel_scroll = rl.Vector2(99, -20)

    # For the checkbox, we need a pointer to bool
    show_content_area_ptr = rl.ffi.new('bool *', True)

    # Need to use pointers for values that will be modified by sliders
    panel_content_width_ptr = rl.ffi.new('float *', panel_content_rec.width)
    panel_content_height_ptr = rl.ffi.new('float *', panel_content_rec.height)

    rl.set_target_fps(60)
    #---------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # Update the panel content rectangle dimensions
        panel_content_rec.width = panel_content_width_ptr[0]
        panel_content_rec.height = panel_content_height_ptr[0]
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text(f"[{panel_scroll.x}, {panel_scroll.y}]", 4, 4, 20, rl.RED)

        rl.gui_scroll_panel(panel_rec, "", panel_content_rec, panel_scroll, panel_view)

        rl.begin_scissor_mode(int(panel_view.x), int(panel_view.y), int(panel_view.width), int(panel_view.height))
        grid_result = rl.Vector2(0, 0)  # This is to store the cell coordinates
        rl.gui_grid(rl.Rectangle(panel_rec.x + panel_scroll.x, panel_rec.y + panel_scroll.y, 
                               panel_content_rec.width, panel_content_rec.height), 
                  "", 16, 3, grid_result)
        rl.end_scissor_mode()

        if show_content_area_ptr[0]:
            rl.draw_rectangle(int(panel_rec.x + panel_scroll.x), int(panel_rec.y + panel_scroll.y), 
                            int(panel_content_rec.width), int(panel_content_rec.height), 
                            rl.fade(rl.RED, 0.1))

        draw_style_edit_controls()

        rl.gui_check_box(rl.Rectangle(565, 80, 20, 20), "SHOW CONTENT AREA", show_content_area_ptr)

        rl.gui_slider_bar(rl.Rectangle(590, 385, 145, 15), "WIDTH", f"{int(panel_content_width_ptr[0])}",
                        panel_content_width_ptr, 1, 600)
        rl.gui_slider_bar(rl.Rectangle(590, 410, 145, 15), "HEIGHT", f"{int(panel_content_height_ptr[0])}",
                        panel_content_height_ptr, 1, 400)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

# Execute the main function
if __name__ == '__main__':
    main()
