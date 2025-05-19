"""raygui - custom sliders
DEPENDENCIES:
    raylib 4.0  - Windowing/input management and drawing.
    raygui 3.0  - Immediate-mode GUI controls.
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99
LICENSE: zlib/libpng
Copyright (c) 2016-2024 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

#----------------------------------------------------------------------------------
# Controls Functions Declaration
#----------------------------------------------------------------------------------
def gui_vertical_slider(bounds, text_top, text_bottom, value_ptr, min_value, max_value):
    return gui_vertical_slider_pro(bounds, text_top, text_bottom, value_ptr, min_value, max_value, rl.gui_get_style(rl.SLIDER, rl.SLIDER_WIDTH))

def gui_vertical_slider_bar(bounds, text_top, text_bottom, value_ptr, min_value, max_value):
    return gui_vertical_slider_pro(bounds, text_top, text_bottom, value_ptr, min_value, max_value, 0)

def gui_vertical_slider_pro(bounds, text_top, text_bottom, value_ptr, min_value, max_value, slider_height):
    state = rl.gui_get_state()

    slider_value = int(((value_ptr[0] - min_value)/(max_value - min_value)) * (bounds.height - 2 * rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)))

    slider = rl.Rectangle(
        bounds.x + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH) + rl.gui_get_style(rl.SLIDER, rl.SLIDER_PADDING),
        bounds.y + bounds.height - slider_value,
        bounds.width - 2 * rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH) - 2 * rl.gui_get_style(rl.SLIDER, rl.SLIDER_PADDING),
        0.0
    )

    if slider_height > 0:        # Slider
        slider.y -= slider_height / 2
        slider.height = slider_height
    elif slider_height == 0:  # SliderBar
        slider.y -= rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
        slider.height = slider_value
    
    # Update control
    #--------------------------------------------------------------------
    if ((state != rl.STATE_DISABLED) and not rl.gui_is_locked()):
        mouse_point = rl.get_mouse_position()

        if rl.check_collision_point_rec(mouse_point, bounds):
            if rl.is_mouse_button_down(rl.MOUSE_LEFT_BUTTON):
                state = rl.STATE_PRESSED

                # Get equivalent value and slider position from mousePoint.y
                normalized_value = (bounds.y + bounds.height - mouse_point.y - (slider_height / 2)) / (bounds.height - slider_height)
                new_value = (max_value - min_value) * normalized_value + min_value
                value_ptr[0] = new_value

                if slider_height > 0:  # Slider
                    slider.y = mouse_point.y - slider.height / 2
                elif slider_height == 0:  # SliderBar
                    slider.y = mouse_point.y
                    slider.height = bounds.y + bounds.height - slider.y - rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
            else:
                state = rl.STATE_FOCUSED

        if value_ptr[0] > max_value:
            value_ptr[0] = max_value
        elif value_ptr[0] < min_value:
            value_ptr[0] = min_value

    # Bar limits check
    if slider_height > 0:  # Slider
        if slider.y < (bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)):
            slider.y = bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
        elif (slider.y + slider.height) >= (bounds.y + bounds.height):
            slider.y = bounds.y + bounds.height - slider.height - rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
    elif slider_height == 0:  # SliderBar
        if slider.y < (bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)):
            slider.y = bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
            slider.height = bounds.height - 2 * rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)

    #--------------------------------------------------------------------
    # Draw control
    #--------------------------------------------------------------------
    rl.gui_draw_rectangle(bounds, rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH),
                        rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BORDER + (state*3))), rl.gui_get_alpha()), 
                        rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BASE_COLOR_NORMAL if state != rl.STATE_DISABLED else rl.BASE_COLOR_DISABLED)), rl.gui_get_alpha()))

    # Draw slider internal bar (depends on state)
    if (state == rl.STATE_NORMAL) or (state == rl.STATE_PRESSED):
        rl.gui_draw_rectangle(slider, 0, rl.BLANK, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BASE_COLOR_PRESSED)), rl.gui_get_alpha()))
    elif state == rl.STATE_FOCUSED:
        rl.gui_draw_rectangle(slider, 0, rl.BLANK, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT_COLOR_FOCUSED)), rl.gui_get_alpha()))

    # Draw top/bottom text if provided
    if text_top is not None:
        text_bounds = rl.Rectangle(0, 0, 0, 0)
        text_bounds.width = rl.get_text_width(text_top)
        text_bounds.height = rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)
        text_bounds.x = bounds.x + bounds.width/2 - text_bounds.width/2
        text_bounds.y = bounds.y - text_bounds.height - rl.gui_get_style(rl.SLIDER, rl.TEXT_PADDING)

        rl.gui_draw_text(text_top, text_bounds, rl.TEXT_ALIGN_RIGHT, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT + (state*3))), rl.gui_get_alpha()))

    if text_bottom is not None:
        text_bounds = rl.Rectangle(0, 0, 0, 0)
        text_bounds.width = rl.get_text_width(text_bottom)
        text_bounds.height = rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)
        text_bounds.x = bounds.x + bounds.width/2 - text_bounds.width/2
        text_bounds.y = bounds.y + bounds.height + rl.gui_get_style(rl.SLIDER, rl.TEXT_PADDING)

        rl.gui_draw_text(text_bottom, text_bounds, rl.TEXT_ALIGN_LEFT, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT + (state*3))), rl.gui_get_alpha()))

    return value_ptr[0]

def gui_slider_owning(bounds, text_left, text_right, value_ptr, min_value, max_value, edit_mode):
    return gui_slider_pro_owning(bounds, text_left, text_right, value_ptr, min_value, max_value, rl.gui_get_style(rl.SLIDER, rl.SLIDER_WIDTH), edit_mode)

def gui_slider_bar_owning(bounds, text_left, text_right, value_ptr, min_value, max_value, edit_mode):
    return gui_slider_pro_owning(bounds, text_left, text_right, value_ptr, min_value, max_value, 0, edit_mode)

def gui_slider_pro_owning(bounds, text_left, text_right, value_ptr, min_value, max_value, slider_width, edit_mode):
    state = rl.gui_get_state()

    temp_value = value_ptr[0]
    pressed = False

    slider_value = int(((temp_value - min_value)/(max_value - min_value))*(bounds.width - 2*rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)))

    slider = rl.Rectangle(
        bounds.x,
        bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH) + rl.gui_get_style(rl.SLIDER, rl.SLIDER_PADDING),
        0,
        bounds.height - 2*rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH) - 2*rl.gui_get_style(rl.SLIDER, rl.SLIDER_PADDING)
    )

    if slider_width > 0:        # Slider
        slider.x += (slider_value - slider_width/2)
        slider.width = slider_width
    elif slider_width == 0:  # SliderBar
        slider.x += rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
        slider.width = slider_value

    # Update control
    #--------------------------------------------------------------------
    if (state != rl.STATE_DISABLED) and (edit_mode or not rl.gui_is_locked()):
        mouse_point = rl.get_mouse_position()

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            if rl.check_collision_point_rec(mouse_point, bounds):
                pressed = True
        elif rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON) and edit_mode:
            pressed = True
            
        if edit_mode:
            state = rl.STATE_PRESSED
            temp_value = ((max_value - min_value)*(mouse_point.x - (bounds.x + slider_width/2)))/(bounds.width - slider_width) + min_value

            if slider_width > 0:  # Slider
                slider.x = mouse_point.x - slider.width/2
            elif slider_width == 0:  # SliderBar
                slider.width = slider_value

        elif rl.check_collision_point_rec(mouse_point, bounds):
            state = rl.STATE_FOCUSED

        if temp_value > max_value:
            temp_value = max_value
        elif temp_value < min_value:
            temp_value = min_value

    # Bar limits check
    if slider_width > 0:        # Slider
        if slider.x <= (bounds.x + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)):
            slider.x = bounds.x + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
        elif (slider.x + slider.width) >= (bounds.x + bounds.width):
            slider.x = bounds.x + bounds.width - slider.width - rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
    elif slider_width == 0:  # SliderBar
        if slider.width > bounds.width:
            slider.width = bounds.width - 2 * rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)

    #--------------------------------------------------------------------
    # Draw control
    #--------------------------------------------------------------------
    rl.gui_draw_rectangle(bounds, rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH), 
                        rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BORDER + (state*3))), rl.gui_get_alpha()), 
                        rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BASE_COLOR_NORMAL if state != rl.STATE_DISABLED else rl.BASE_COLOR_DISABLED)), rl.gui_get_alpha()))

    # Draw slider internal bar (depends on state)
    if (state == rl.STATE_NORMAL) or (state == rl.STATE_PRESSED):
        rl.gui_draw_rectangle(slider, 0, rl.BLANK, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BASE_COLOR_PRESSED)), rl.gui_get_alpha()))
    elif state == rl.STATE_FOCUSED:
        rl.gui_draw_rectangle(slider, 0, rl.BLANK, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT_COLOR_FOCUSED)), rl.gui_get_alpha()))

    # Draw left/right text if provided
    if text_left is not None:
        text_bounds = rl.Rectangle(0, 0, 0, 0)
        text_bounds.width = rl.get_text_width(text_left)
        text_bounds.height = rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)
        text_bounds.x = bounds.x - text_bounds.width - rl.gui_get_style(rl.SLIDER, rl.TEXT_PADDING)
        text_bounds.y = bounds.y + bounds.height/2 - rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)/2

        rl.gui_draw_text(text_left, text_bounds, rl.TEXT_ALIGN_RIGHT, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT + (state*3))), rl.gui_get_alpha()))

    if text_right is not None:
        text_bounds = rl.Rectangle(0, 0, 0, 0)
        text_bounds.width = rl.get_text_width(text_right)
        text_bounds.height = rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)
        text_bounds.x = bounds.x + bounds.width + rl.gui_get_style(rl.SLIDER, rl.TEXT_PADDING)
        text_bounds.y = bounds.y + bounds.height/2 - rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)/2

        rl.gui_draw_text(text_right, text_bounds, rl.TEXT_ALIGN_LEFT, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT + (state*3))), rl.gui_get_alpha()))

    value_ptr[0] = temp_value
    return pressed

def gui_vertical_slider_owning(bounds, text_top, text_bottom, value_ptr, min_value, max_value, edit_mode):
    return gui_vertical_slider_pro_owning(bounds, text_top, text_bottom, value_ptr, min_value, max_value, rl.gui_get_style(rl.SLIDER, rl.SLIDER_WIDTH), edit_mode)

def gui_vertical_slider_bar_owning(bounds, text_top, text_bottom, value_ptr, min_value, max_value, edit_mode):
    return gui_vertical_slider_pro_owning(bounds, text_top, text_bottom, value_ptr, min_value, max_value, 0, edit_mode)

def gui_vertical_slider_pro_owning(bounds, text_top, text_bottom, value_ptr, min_value, max_value, slider_height, edit_mode):
    state = rl.gui_get_state()

    temp_value = value_ptr[0]
    pressed = False

    slider_value = int(((temp_value - min_value)/(max_value - min_value)) * (bounds.height - 2 * rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)))

    slider = rl.Rectangle(
        bounds.x + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH) + rl.gui_get_style(rl.SLIDER, rl.SLIDER_PADDING),
        bounds.y + bounds.height - slider_value,
        bounds.width - 2*rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH) - 2*rl.gui_get_style(rl.SLIDER, rl.SLIDER_PADDING),
        0.0
    )

    if slider_height > 0:        # Slider
        slider.y -= slider_height/2
        slider.height = slider_height
    elif slider_height == 0:  # SliderBar
        slider.y -= rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
        slider.height = slider_value
        
    # Update control
    #--------------------------------------------------------------------
    if (state != rl.STATE_DISABLED) and (edit_mode or not rl.gui_is_locked()):
        mouse_point = rl.get_mouse_position()

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            if rl.check_collision_point_rec(mouse_point, bounds):
                pressed = True
        elif rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON) and edit_mode:
            pressed = True
            
        if edit_mode:
            state = rl.STATE_PRESSED

            normalized_value = (bounds.y + bounds.height - mouse_point.y - (slider_height / 2)) / (bounds.height - slider_height)
            temp_value = (max_value - min_value) * normalized_value + min_value

            if slider_height > 0:  # Slider
                slider.y = mouse_point.y - slider.height / 2
            elif slider_height == 0:  # SliderBar
                slider.y = mouse_point.y
                slider.height = bounds.y + bounds.height - slider.y - rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
        elif rl.check_collision_point_rec(mouse_point, bounds):
            state = rl.STATE_FOCUSED

        if temp_value > max_value:
            temp_value = max_value
        elif temp_value < min_value:
            temp_value = min_value

    # Bar limits check
    if slider_height > 0:        # Slider
        if slider.y < (bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)):
            slider.y = bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
        elif (slider.y + slider.height) >= (bounds.y + bounds.height):
            slider.y = bounds.y + bounds.height - slider.height - rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
    elif slider_height == 0:  # SliderBar
        if slider.y < (bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)):
            slider.y = bounds.y + rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)
            slider.height = bounds.height - 2*rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH)

    #--------------------------------------------------------------------
    # Draw control
    #--------------------------------------------------------------------
    rl.gui_draw_rectangle(bounds, rl.gui_get_style(rl.SLIDER, rl.BORDER_WIDTH), 
                        rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BORDER + (state*3))), rl.gui_get_alpha()), 
                        rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BASE_COLOR_NORMAL if state != rl.STATE_DISABLED else rl.BASE_COLOR_DISABLED)), rl.gui_get_alpha()))

    # Draw slider internal bar (depends on state)
    if (state == rl.STATE_NORMAL) or (state == rl.STATE_PRESSED):
        rl.gui_draw_rectangle(slider, 0, rl.BLANK, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.BASE_COLOR_PRESSED)), rl.gui_get_alpha()))
    elif state == rl.STATE_FOCUSED:
        rl.gui_draw_rectangle(slider, 0, rl.BLANK, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT_COLOR_FOCUSED)), rl.gui_get_alpha()))

    # Draw top/bottom text if provided
    if text_top is not None:
        text_bounds = rl.Rectangle(0, 0, 0, 0)
        text_bounds.width = rl.get_text_width(text_top)
        text_bounds.height = rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)
        text_bounds.x = bounds.x + bounds.width/2 - text_bounds.width/2
        text_bounds.y = bounds.y - text_bounds.height - rl.gui_get_style(rl.SLIDER, rl.TEXT_PADDING)

        rl.gui_draw_text(text_top, text_bounds, rl.TEXT_ALIGN_RIGHT, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT + (state*3))), rl.gui_get_alpha()))

    if text_bottom is not None:
        text_bounds = rl.Rectangle(0, 0, 0, 0)
        text_bounds.width = rl.get_text_width(text_bottom)
        text_bounds.height = rl.gui_get_style(rl.DEFAULT, rl.TEXT_SIZE)
        text_bounds.x = bounds.x + bounds.width/2 - text_bounds.width/2
        text_bounds.y = bounds.y + bounds.height + rl.gui_get_style(rl.SLIDER, rl.TEXT_PADDING)

        rl.gui_draw_text(text_bottom, text_bounds, rl.TEXT_ALIGN_LEFT, rl.fade(rl.get_color(rl.gui_get_style(rl.SLIDER, rl.TEXT + (state*3))), rl.gui_get_alpha()))

    value_ptr[0] = temp_value
    return pressed

def main():
    # Initialization
    #---------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raygui - custom sliders")

    # Creates value pointer for function sliders
    value_ptr = rl.ffi.new('float *', 0.5)
    value_ptr2 = rl.ffi.new('float *', 0.5)  # sliders standard
    value_ptr3 = rl.ffi.new('float *', 0.5)  # vertical slider
    value_ptr4 = rl.ffi.new('float *', 0.5)  # vertical slider bar
    
    # Create boolean pointers for edit modes
    slider_edit_mode_ptr = rl.ffi.new('bool *', False)
    v_slider_edit_mode_ptr = rl.ffi.new('bool *', False)
    v_slider_bar_edit_mode_ptr = rl.ffi.new('bool *', False)

    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # Nothing to update here
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        # "0xffff_ffff &" to work-around  rl.gui_get_style returning a negative number
        rl.clear_background(rl.get_color(0xffff_ffff & rl.gui_get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))

        if v_slider_edit_mode_ptr[0] or v_slider_bar_edit_mode_ptr[0]:
            rl.gui_lock()
        else:
            rl.gui_unlock()

        # raygui: controls drawing
        #----------------------------------------------------------------------------------
        rl.gui_group_box(rl.Rectangle(66, 24, 276, 312), "STANDARD")
        rl.gui_slider(rl.Rectangle(96, 48, 216, 16), f"{value_ptr2[0]:.2f}", "", value_ptr2, 0.0, 1.0)
        gui_vertical_slider(rl.Rectangle(120, 120, 24, 192), f"{value_ptr3[0]:.2f}", "", value_ptr3, 0.0, 1.0)
        gui_vertical_slider_bar(rl.Rectangle(264, 120, 24, 192), f"{value_ptr4[0]:.2f}", "", value_ptr4, 0.0, 1.0)

        rl.gui_group_box(rl.Rectangle(378, 24, 276, 312), "OWNING")
        if gui_slider_owning(rl.Rectangle(408, 48, 216, 16), None, f"{value_ptr[0]:.2f}", value_ptr, 0.0, 1.0, slider_edit_mode_ptr[0]):
            slider_edit_mode_ptr[0] = not slider_edit_mode_ptr[0]
        if gui_vertical_slider_owning(rl.Rectangle(432, 120, 24, 192), None, f"{value_ptr[0]:.2f}", value_ptr, 0.0, 1.0, v_slider_edit_mode_ptr[0]):
            v_slider_edit_mode_ptr[0] = not v_slider_edit_mode_ptr[0]
        if gui_vertical_slider_bar_owning(rl.Rectangle(576, 120, 24, 192), None, f"{value_ptr[0]:.2f}", value_ptr, 0.0, 1.0, v_slider_bar_edit_mode_ptr[0]):
            v_slider_bar_edit_mode_ptr[0] = not v_slider_bar_edit_mode_ptr[0]
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
