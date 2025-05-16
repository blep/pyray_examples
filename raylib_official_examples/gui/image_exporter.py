"""raygui - image exporter
DEPENDENCIES:
    raylib 4.0  - Windowing/input management and drawing.
    raygui 3.0  - Immediate-mode GUI controls.
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99
LICENSE: zlib/libpng
Copyright (c) 2015-2024 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import os

THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450
    
    rl.init_window(screen_width, screen_height, "raygui - image exporter")
    
    # GUI controls initialization
    #----------------------------------------------------------------------------------
    window_box_rec = rl.Rectangle(screen_width/2 - 110, screen_height/2 - 100, 220, 190)
    window_box_active = False
    
    file_format_active_ptr = rl.ffi.new('int *', 0)
    file_format_text_list = ["IMAGE (.png)", "DATA (.raw)", "CODE (.h)"]

    pixel_format_active_ptr = rl.ffi.new('int *', 0)
    pixel_format_text_list = ["GRAYSCALE", "GRAY ALPHA", "R5G6B5", "R8G8B8", "R5G5B5A1", "R4G4B4A4", "R8G8B8A8"]

    text_box_edit_mode = False
    file_name = "untitled"
    #--------------------------------------------------------------------------------------
    
    image = rl.Image()
    texture = rl.Texture()
    
    image_loaded = False
    image_scale = 1.0
    image_rec = rl.Rectangle(0, 0, 0, 0)
    
    btn_export_pressed = False

    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()

            if dropped_files.count == 1:
                im_temp = rl.load_image(dropped_files.paths[0])
                
                if im_temp.data:
                    # Unload previous image if loaded
                    if image_loaded:
                        rl.unload_image(image)
                    image = im_temp
                    
                    # Unload previous texture if loaded
                    if texture.id != 0:
                        rl.unload_texture(texture)
                    texture = rl.load_texture_from_image(image)
                    
                    image_loaded = True
                    pixel_format_active_ptr[0] = image.format - 1
                    
                    if texture.height > texture.width:
                        image_scale = (screen_height - 100)/texture.height
                    else:
                        image_scale = (screen_width - 100)/texture.width

            rl.unload_dropped_files(dropped_files)
    
        if btn_export_pressed:
            if image_loaded:
                rl.image_format(image, pixel_format_active_ptr[0] + 1)
                
                if file_format_active_ptr[0] == 0:        # PNG
                    if (rl.get_file_extension(file_name) is None) or (not rl.is_file_extension(file_name, ".png")):
                        file_name += ".png"
                    rl.export_image(image, file_name)
                elif file_format_active_ptr[0] == 1:   # RAW
                    if (rl.get_file_extension(file_name) is None) or (not rl.is_file_extension(file_name, ".raw")):
                        file_name += ".raw"
                    
                    data_size = rl.get_pixel_data_size(image.width, image.height, image.format)
                    
                    # In Python, we need to use a different approach to write binary data
                    raw_data = rl.ffi.buffer(image.data, data_size)
                    with open(file_name, "wb") as raw_file:
                        raw_file.write(raw_data)
                elif file_format_active_ptr[0] == 2:   # CODE
                    rl.export_image_as_code(image, file_name)
            
            window_box_active = False
        
        if image_loaded:
            image_scale += rl.get_mouse_wheel_move() * 0.05   # Image scale control
            if image_scale <= 0.1:
                image_scale = 0.1
            elif image_scale >= 5:
                image_scale = 5
            
            image_rec = rl.Rectangle(
                screen_width/2 - image.width*image_scale/2, 
                screen_height/2 - image.height*image_scale/2, 
                image.width*image_scale, 
                image.height*image_scale
            )
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        if texture.id > 0:
            rl.draw_texture_ex(
                texture, 
                rl.Vector2(screen_width/2 - texture.width*image_scale/2, screen_height/2 - texture.height*image_scale/2), 
                0.0, 
                image_scale, 
                rl.WHITE
            )
            
            border_color = rl.RED if rl.check_collision_point_rec(rl.get_mouse_position(), image_rec) else rl.DARKGRAY
            rl.draw_rectangle_lines_ex(image_rec, 1, border_color)
            # PORT: "0xffff_ffff &" is a work-around for converting the negative int32 to uint32
            rl.draw_text(f"SCALE: {image_scale*100.0:.2f}%", 20, screen_height - 40, 20, 
                        rl.get_color(0xffff_ffff & rl.gui_get_style(rl.DEFAULT, rl.LINE_COLOR)))
        else:
            rl.draw_text("DRAG & DROP YOUR IMAGE!", 350, 200, 10, rl.DARKGRAY)
            rl.gui_disable()
        
        if rl.gui_button(rl.Rectangle(screen_width - 170, screen_height - 50, 150, 30), "Image Export"):
            window_box_active = True
        rl.gui_enable()
        
        # Draw window box: windowBoxName
        #-----------------------------------------------------------------------------
        if window_box_active:
            # PORT: "0xffff_ffff &" is a work-around for converting the negative int32 to uint32
            rl.draw_rectangle(0, 0, screen_width, screen_height,
                              rl.fade(rl.get_color(0xffff_ffff & rl.gui_get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)), 0.7))
            result = rl.gui_window_box(rl.Rectangle(window_box_rec.x, window_box_rec.y, 220, 190), "Image Export Options")
            window_box_active = not result
        
            rl.gui_label(rl.Rectangle(window_box_rec.x + 10, window_box_rec.y + 35, 60, 25), "File format:")
            rl.gui_combo_box(rl.Rectangle(window_box_rec.x + 80, window_box_rec.y + 35, 130, 25), 
                            ";".join(file_format_text_list), file_format_active_ptr)
            
            rl.gui_label(rl.Rectangle(window_box_rec.x + 10, window_box_rec.y + 70, 63, 25), "Pixel format:")
            rl.gui_combo_box(rl.Rectangle(window_box_rec.x + 80, window_box_rec.y + 70, 130, 25), 
                            ";".join(pixel_format_text_list), pixel_format_active_ptr)
            
            rl.gui_label(rl.Rectangle(window_box_rec.x + 10, window_box_rec.y + 105, 50, 25), "File name:")
            if rl.gui_text_box(rl.Rectangle(window_box_rec.x + 80, window_box_rec.y + 105, 130, 25), file_name, 64, text_box_edit_mode):
                text_box_edit_mode = not text_box_edit_mode

            btn_export_pressed = rl.gui_button(rl.Rectangle(window_box_rec.x + 10, window_box_rec.y + 145, 200, 30), "Export Image")
        else:
            btn_export_pressed = False
        
        if btn_export_pressed:
            rl.draw_text("Image exported!", 20, screen_height - 20, 20, rl.RED)
        #-----------------------------------------------------------------------------

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    if image_loaded:
        rl.unload_image(image)
    if texture.id != 0:
        rl.unload_texture(texture)
    
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

# Execute the main function
if __name__ == '__main__':
    main()
