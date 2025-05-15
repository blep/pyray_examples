"""raygui - controls test suite
TEST CONTROLS:
    - GuiDropdownBox()
    - GuiCheckBox()
    - GuiSpinner()
    - GuiValueBox()
    - GuiTextBox()
    - GuiButton()
    - GuiComboBox()
    - GuiListView()
    - GuiToggleGroup()
    - GuiColorPicker()
    - GuiSlider()
    - GuiSliderBar()
    - GuiProgressBar()
    - GuiColorBarAlpha()
    - GuiScrollPanel()
DEPENDENCIES:
    raylib 4.5          - Windowing/input management and drawing
    raygui 3.5          - Immediate-mode GUI controls with custom styling and icons
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99
LICENSE: zlib/libpng
Copyright (c) 2016-2024 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Main function
def main():
    # Initialization
    #---------------------------------------------------------------------------------------
    screen_width = 960
    screen_height = 560

    rl.init_window(screen_width, screen_height, "raygui - controls test suite")
    rl.set_exit_key(0)

    # GUI controls initialization
    #----------------------------------------------------------------------------------
    dropdown_box000_active_ptr = rl.ffi.new('int *', 0)
    drop_down000_edit_mode = False

    dropdown_box001_active_ptr = rl.ffi.new('int *', 0)
    drop_down001_edit_mode = False

    spinner001_value_ptr = rl.ffi.new('int *', 0)
    spinner_edit_mode = False

    value_box002_value_ptr = rl.ffi.new('int *', 0)
    value_box_edit_mode = False

    text_box_text = "Text box"
    text_box_edit_mode = False

    text_box_multi_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n\nDuis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n\nThisisastringlongerthanexpectedwithoutspacestotestcharbreaksforthosecases,checkingifworkingasexpected.\n\nExcepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    text_box_multi_edit_mode = False

    list_view_scroll_index_ptr = rl.ffi.new('int *', 0)
    list_view_active_ptr = rl.ffi.new('int *', -1)

    list_view_ex_scroll_index_ptr = rl.ffi.new('int *', 0)
    list_view_ex_active_ptr = rl.ffi.new('int *', 2)
    list_view_ex_focus_ptr = rl.ffi.new('int *', -1)
    list_view_ex_list = ["This", "is", "a", "list view", "with", "disable", "elements", "amazing!"]

    color_picker_value_ptr = rl.ffi.new('Color *')
    color_picker_value_ptr[0] = rl.Color(255, 0, 0, 255)  # rl.RED

    slider_value_ptr = rl.ffi.new('float *', 50.0)
    slider_bar_value_ptr = rl.ffi.new('float *', 60.0)  # Use pointer for slider bar
    progress_value_ptr = rl.ffi.new('float *', 0.1)

    # For checkbox we need a pointer to bool
    force_squared_checked_ptr = rl.ffi.new('bool *', False)

    # For alpha value slider we need a pointer to float
    alpha_value_ptr = rl.ffi.new('float *', 0.5)

    visual_style_active_ptr = rl.ffi.new('int *', 0)
    prev_visual_style_active = 0

    toggle_group_active_ptr = rl.ffi.new('int *', 0)
    toggle_slider_active_ptr = rl.ffi.new('int *', 0)

    view_scroll = rl.Vector2(0, 0)
    #----------------------------------------------------------------------------------

    # Custom GUI font loading
    #font = rl.load_font_ex("fonts/rainyhearts16.ttf", 12, None, 0)
    #rl.gui_set_font(font)

    exit_window = False
    show_message_box = False

    text_input = ""
    text_input_file_name = ""
    show_text_input_box = False

    alpha = 1.0

    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not exit_window:    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        exit_window = rl.window_should_close()

        if rl.is_key_pressed(rl.KEY_ESCAPE):
            show_message_box = not show_message_box

        if rl.is_key_down(rl.KEY_LEFT_CONTROL) and rl.is_key_pressed(rl.KEY_S):
            show_text_input_box = True

        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()

            if (dropped_files.count > 0) and rl.is_file_extension(dropped_files.paths[0], ".rgs"):
                rl.gui_load_style(dropped_files.paths[0])

            rl.unload_dropped_files(dropped_files)    # Clear internal buffers

        #alpha -= 0.002
        if alpha < 0.0:
            alpha = 0.0
        if rl.is_key_pressed(rl.KEY_SPACE):
            alpha = 1.0

        rl.gui_set_alpha(alpha)

        #progress_value += 0.002
        if rl.is_key_pressed(rl.KEY_LEFT):
            progress_value_ptr[0] -= 0.1
        elif rl.is_key_pressed(rl.KEY_RIGHT):
            progress_value_ptr[0] += 0.1
        
        if progress_value_ptr[0] > 1.0:
            progress_value_ptr[0] = 1.0
        elif progress_value_ptr[0] < 0.0:
            progress_value_ptr[0] = 0.0

        if visual_style_active_ptr[0] != prev_visual_style_active:
            rl.gui_load_style_default()

            if visual_style_active_ptr[0] == 0:
                pass  # Default style
            elif visual_style_active_ptr[0] == 1:
                rl.gui_load_style_jungle()
            elif visual_style_active_ptr[0] == 2:
                rl.gui_load_style_lavanda()
            elif visual_style_active_ptr[0] == 3:
                rl.gui_load_style_dark()
            elif visual_style_active_ptr[0] == 4:
                rl.gui_load_style_bluish()
            elif visual_style_active_ptr[0] == 5:
                rl.gui_load_style_cyber()
            elif visual_style_active_ptr[0] == 6:
                rl.gui_load_style_terminal()
            elif visual_style_active_ptr[0] == 7:
                rl.gui_load_style_candy()
            elif visual_style_active_ptr[0] == 8:
                rl.gui_load_style_cherry()
            elif visual_style_active_ptr[0] == 9:
                rl.gui_load_style_ashes()
            elif visual_style_active_ptr[0] == 10:
                rl.gui_load_style_enefete()
            elif visual_style_active_ptr[0] == 11:
                rl.gui_load_style_sunny()
            elif visual_style_active_ptr[0] == 12:
                rl.gui_load_style_amber()

            rl.gui_set_style(rl.LABEL, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_LEFT)

            prev_visual_style_active = visual_style_active_ptr[0]
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        # 0xFFFFFFFF & rl.gui_get_style() is a work-around to convert the negative int32_t to the uint32_t
        # expected by rl.get_color()
        rl.clear_background(rl.get_color(0xFFFFFFFF & rl.gui_get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))

        # raygui: controls drawing
        #----------------------------------------------------------------------------------
        # Check all possible events that require GuiLock
        if drop_down000_edit_mode or drop_down001_edit_mode:
            rl.gui_lock()

        # First GUI column
        #rl.gui_set_style(rl.CHECKBOX, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_LEFT)
        rl.gui_check_box(rl.Rectangle(25, 108, 15, 15), "FORCE CHECK!", force_squared_checked_ptr)

        rl.gui_set_style(rl.TEXTBOX, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_CENTER)
        #rl.gui_set_style(rl.VALUEBOX, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_LEFT)
        
        # For spinner and value box, we need to convert between Python and C
        spinner_result = rl.gui_spinner(rl.Rectangle(25, 135, 125, 30), "", spinner001_value_ptr, 0, 100, spinner_edit_mode)
        if spinner_result:
            spinner_edit_mode = not spinner_edit_mode
        
        value_box_result = rl.gui_value_box(rl.Rectangle(25, 175, 125, 30), "", value_box002_value_ptr, 0, 100, value_box_edit_mode)
        if value_box_result:
            value_box_edit_mode = not value_box_edit_mode
        
        rl.gui_set_style(rl.TEXTBOX, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_LEFT)
        text_box_result = rl.gui_text_box(rl.Rectangle(25, 215, 125, 30), text_box_text, 64, text_box_edit_mode)
        if text_box_result:
            text_box_edit_mode = not text_box_edit_mode

        rl.gui_set_style(rl.BUTTON, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_CENTER)

        if rl.gui_button(rl.Rectangle(25, 255, 125, 30), rl.gui_icon_text(rl.ICON_FILE_SAVE, "Save File")):
            show_text_input_box = True

        rl.gui_group_box(rl.Rectangle(25, 310, 125, 150), "STATES")
        #rl.gui_lock()
        rl.gui_set_state(rl.STATE_NORMAL)
        rl.gui_button(rl.Rectangle(30, 320, 115, 30), "NORMAL")
        rl.gui_set_state(rl.STATE_FOCUSED)
        rl.gui_button(rl.Rectangle(30, 355, 115, 30), "FOCUSED")
        rl.gui_set_state(rl.STATE_PRESSED)
        rl.gui_button(rl.Rectangle(30, 390, 115, 30), "#15#PRESSED")
        rl.gui_set_state(rl.STATE_DISABLED)
        rl.gui_button(rl.Rectangle(30, 425, 115, 30), "DISABLED")
        rl.gui_set_state(rl.STATE_NORMAL)
        #rl.gui_unlock()

        rl.gui_combo_box(rl.Rectangle(25, 480, 125, 30), "default;Jungle;Lavanda;Dark;Bluish;Cyber;Terminal;Candy;Cherry;Ashes;Enefete;Sunny;Amber", visual_style_active_ptr)

        # NOTE: GuiDropdownBox must draw after any other control that can be covered on unfolding
        rl.gui_unlock()
        rl.gui_set_style(rl.DROPDOWNBOX, rl.TEXT_PADDING, 4)
        rl.gui_set_style(rl.DROPDOWNBOX, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_LEFT)
        dropdown_result = rl.gui_dropdown_box(rl.Rectangle(25, 65, 125, 30), "#01#ONE;#02#TWO;#03#THREE;#04#FOUR", dropdown_box001_active_ptr, drop_down001_edit_mode)
        if dropdown_result:
            drop_down001_edit_mode = not drop_down001_edit_mode
        
        rl.gui_set_style(rl.DROPDOWNBOX, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_CENTER)
        rl.gui_set_style(rl.DROPDOWNBOX, rl.TEXT_PADDING, 0)

        dropdown_result = rl.gui_dropdown_box(rl.Rectangle(25, 25, 125, 30), "ONE;TWO;THREE", dropdown_box000_active_ptr, drop_down000_edit_mode)
        if dropdown_result:
            drop_down000_edit_mode = not drop_down000_edit_mode

        # Second GUI column
        #rl.gui_set_style(rl.LISTVIEW, rl.LIST_ITEMS_BORDER_NORMAL, 1)
        rl.gui_list_view(rl.Rectangle(165, 25, 140, 124), "Charmander;Bulbasaur;#18#Squirtel;Pikachu;Eevee;Pidgey", list_view_scroll_index_ptr, list_view_active_ptr)
        rl.gui_list_view_ex(rl.Rectangle(165, 162, 140, 184), list_view_ex_list, 8, list_view_ex_scroll_index_ptr, list_view_ex_active_ptr, list_view_ex_focus_ptr)
        rl.gui_set_style(rl.LISTVIEW, rl.GuiListViewProperty.LIST_ITEMS_BORDER_WIDTH, 0) # PORT: changed from LIST_ITEMS_BORDER_NORMAL

        #rl.gui_toggle(rl.Rectangle(165, 400, 140, 25), "#1#ONE", toggle_group_active_ptr)
        rl.gui_toggle_group(rl.Rectangle(165, 360, 140, 24), "#1#ONE\n#3#TWO\n#8#THREE\n#23#", toggle_group_active_ptr)
        #rl.gui_disable()
        rl.gui_set_style(rl.SLIDER, rl.SLIDER_PADDING, 2)
        rl.gui_toggle_slider(rl.Rectangle(165, 480, 140, 30), "ON;OFF", toggle_slider_active_ptr)
        rl.gui_set_style(rl.SLIDER, rl.SLIDER_PADDING, 0)

        # Third GUI column
        rl.gui_panel(rl.Rectangle(320, 25, 225, 140), "Panel Info")
        rl.gui_color_picker(rl.Rectangle(320, 185, 196, 192), "", color_picker_value_ptr)

        #rl.gui_disable()
        rl.gui_slider(rl.Rectangle(355, 400, 165, 20), "TEST", f"{slider_value_ptr[0]:2.2f}", slider_value_ptr, -50, 100)
        rl.gui_slider_bar(rl.Rectangle(320, 430, 200, 20), "", f"{slider_bar_value_ptr[0]:.1f}", slider_bar_value_ptr, 0, 100)
        
        rl.gui_progress_bar(rl.Rectangle(320, 460, 200, 20), "", f"{int(progress_value_ptr[0]*100)}%", progress_value_ptr, 0.0, 1.0)
        rl.gui_enable()

        # NOTE: View rectangle could be used to perform some scissor test
        view = rl.Rectangle(0, 0, 0, 0)
        rl.gui_scroll_panel(rl.Rectangle(560, 25, 102, 354), "", rl.Rectangle(560, 25, 300, 1200), view_scroll, view)

        mouse_cell = rl.Vector2(0, 0)
        rl.gui_grid(rl.Rectangle(560, 25 + 180 + 195, 100, 120), "", 20, 3, mouse_cell)

        rl.gui_color_bar_alpha(rl.Rectangle(320, 490, 200, 30), f"{alpha_value_ptr[0]*100:.0f}%", alpha_value_ptr)

        rl.gui_set_style(rl.DEFAULT, rl.TEXT_ALIGNMENT_VERTICAL, rl.TEXT_ALIGN_TOP)   # WARNING: Word-wrap does not work as expected in case of no-top alignment
        rl.gui_set_style(rl.DEFAULT, rl.TEXT_WRAP_MODE, rl.TEXT_WRAP_WORD)            # WARNING: If wrap mode enabled, text editing is not supported
        text_box_multi_result = rl.gui_text_box(rl.Rectangle(678, 25, 258, 492), text_box_multi_text, 1024, text_box_multi_edit_mode)
        if text_box_multi_result:
            text_box_multi_edit_mode = not text_box_multi_edit_mode
        
        rl.gui_set_style(rl.DEFAULT, rl.TEXT_WRAP_MODE, rl.TEXT_WRAP_NONE)
        rl.gui_set_style(rl.DEFAULT, rl.TEXT_ALIGNMENT_VERTICAL, rl.TEXT_ALIGN_MIDDLE)

        rl.gui_set_style(rl.DEFAULT, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_LEFT)
        rl.gui_status_bar(rl.Rectangle(0, rl.get_screen_height() - 20, rl.get_screen_width(), 20), "This is a status bar")
        rl.gui_set_style(rl.DEFAULT, rl.TEXT_ALIGNMENT, rl.TEXT_ALIGN_CENTER)
        #rl.gui_set_style(rl.STATUSBAR, TEXT_INDENTATION, 20)

        if show_message_box:
            rl.draw_rectangle(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.fade(rl.RAYWHITE, 0.8))
            result = rl.gui_message_box(rl.Rectangle(rl.get_screen_width()/2 - 125, rl.get_screen_height()/2 - 50, 250, 100), rl.gui_icon_text(rl.ICON_EXIT, "Close Window"), "Do you really want to exit?", "Yes;No")

            if (result == 0) or (result == 2):
                show_message_box = False
            elif result == 1:
                exit_window = True

        if show_text_input_box:
            rl.draw_rectangle(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.fade(rl.RAYWHITE, 0.8))
            result = rl.gui_text_input_box(rl.Rectangle(rl.get_screen_width()/2 - 120, rl.get_screen_height()/2 - 60, 240, 140), rl.gui_icon_text(rl.ICON_FILE_SAVE, "Save file as..."), "Introduce output file name:", "Ok;Cancel", text_input, 255, None)

            if result == 1:
                # TODO: Validate text_input value and save
                text_input_file_name = text_input

            if (result == 0) or (result == 1) or (result == 2):
                show_text_input_box = False
                text_input = ""
        #----------------------------------------------------------------------------------

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------


# Execute the main function
if __name__ == '__main__':
    main()
