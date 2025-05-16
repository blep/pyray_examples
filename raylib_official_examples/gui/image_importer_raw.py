"""raygui - image raw importer
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
import math
import os

THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #---------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 600
    
    rl.init_window(screen_width, screen_height, "raygui - image raw importer")
    
    texture = rl.Texture()
    
    # GUI controls initialization
    #----------------------------------------------------------------------------------
    window_offset = rl.Vector2(screen_width/2 - 200/2, screen_height/2 - 465/2)
    
    import_window_active = False
    
    width_value_ptr = rl.ffi.new('int *', 0)
    width_edit_mode = False
    height_value_ptr = rl.ffi.new('int *', 0)
    height_edit_mode = False
    
    pixel_format_active_ptr = rl.ffi.new('int *', 0)
    pixel_format_text_list = ["CUSTOM", "GRAYSCALE", "GRAY ALPHA", "R5G6B5", "R8G8B8", "R5G5B5A1", "R4G4B4A4", "R8G8B8A8"]
    
    channels_active_ptr = rl.ffi.new('int *', 3)
    channels_text_list = ["1", "2", "3", "4"]
    bit_depth_active_ptr = rl.ffi.new('int *', 0)
    bit_depth_text_list = ["8", "16", "32"]
    
    header_size_value_ptr = rl.ffi.new('int *', 0)
    header_size_edit_mode = False
    #----------------------------------------------------------------------------------
    
    # Image file info
    data_size = 0
    file_name_path = ""
    file_name = ""
    
    btn_load_pressed = False
    
    image_loaded = False
    image_scale = 1.0
    
    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------
    
    # Main game loop
    while not rl.window_should_close():
        # Update
        #----------------------------------------------------------------------------------
        # Check if a file is dropped
        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()
            
            # Check file extensions for drag-and-drop
            if (dropped_files.count == 1) and rl.is_file_extension(dropped_files.paths[0], ".raw"):
                with open(dropped_files.paths[0], "rb") as image_file:
                    image_file.seek(0, os.SEEK_END)
                    data_size = image_file.tell()
                
                file_name_path = dropped_files.paths[0]
                file_name = rl.get_file_name(dropped_files.paths[0])
                
                # Try to guess possible raw values
                # Let's assume image is square, RGBA, 8 bit per channel
                width_value_ptr[0] = int(math.sqrt(data_size/4))
                height_value_ptr[0] = width_value_ptr[0]
                header_size_value_ptr[0] = data_size - width_value_ptr[0] * height_value_ptr[0] * 4
                if header_size_value_ptr[0] < 0:
                    header_size_value_ptr[0] = 0
                
                import_window_active = True
            
            rl.unload_dropped_files(dropped_files)
        
        # Check if load button has been pressed
        if btn_load_pressed:
            # Depending on channels and bit depth, select correct pixel format
            if (width_value_ptr[0] != 0) and (height_value_ptr[0] != 0):
                format_value = -1
                
                if pixel_format_active_ptr[0] == 0:
                    channels = int(channels_text_list[channels_active_ptr[0]])
                    bpp = int(bit_depth_text_list[bit_depth_active_ptr[0]])
                    
                    # Select correct format depending on channels and bpp
                    if bpp == 8:
                        if channels == 1:
                            format_value = rl.PIXELFORMAT_UNCOMPRESSED_GRAYSCALE
                        elif channels == 2:
                            format_value = rl.PIXELFORMAT_UNCOMPRESSED_GRAY_ALPHA
                        elif channels == 3:
                            format_value = rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8
                        elif channels == 4:
                            format_value = rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8
                    elif bpp == 32:
                        if channels == 1:
                            format_value = rl.PIXELFORMAT_UNCOMPRESSED_R32
                        elif channels == 2:
                            rl.trace_log(rl.LOG_WARNING, "Channel bit-depth not supported!")
                        elif channels == 3:
                            format_value = rl.PIXELFORMAT_UNCOMPRESSED_R32G32B32
                        elif channels == 4:
                            format_value = rl.PIXELFORMAT_UNCOMPRESSED_R32G32B32A32
                    elif bpp == 16:
                        rl.trace_log(rl.LOG_WARNING, "Channel bit-depth not supported!")
                else:
                    format_value = pixel_format_active_ptr[0]
                
                if format_value != -1:
                    image = rl.load_image_raw(file_name_path.encode('utf-8'), width_value_ptr[0], height_value_ptr[0], format_value, header_size_value_ptr[0])
                    texture = rl.load_texture_from_image(image)
                    rl.unload_image(image)
                    
                    import_window_active = False
                    btn_load_pressed = False
                    
                    if texture.id > 0:
                        image_loaded = True
                        image_scale = float(screen_height - 100) / texture.height
        
        if image_loaded:
            image_scale += float(rl.get_mouse_wheel_move())  # Image scale control
        #----------------------------------------------------------------------------------
        
        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        # PORT: "0xffff_ffff &" is a work-around for converting the negative int32 to uint32
        rl.clear_background(rl.get_color(0xffff_ffff & rl.gui_get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))
        
        if texture.id != 0:
            rl.draw_texture_ex(texture, 
                              rl.Vector2(screen_width/2 - texture.width*image_scale/2, 
                                        screen_height/2 - texture.height*image_scale/2),
                              0, image_scale, rl.WHITE)
            rl.draw_text(f"SCALE x{int(image_scale)}", 20, screen_height - 40, 20, 
                        rl.get_color(rl.get_style(rl.DEFAULT, rl.LINE_COLOR)))
        else:
            # PORT: "0xffff_ffff &" is a work-around for converting the negative int32 to uint32
            rl.draw_text("drag & drop RAW image file", 320, 180, 10, 
                        rl.get_color(0xffff_ffff & rl.gui_get_style(rl.DEFAULT, rl.LINE_COLOR)))
        
        # raygui: controls drawing
        #----------------------------------------------------------------------------------
        if import_window_active:
            import_window_active = not rl.gui_window_box(
                rl.Rectangle(window_offset.x + 0, window_offset.y + 0, 200, 465),
                "Image RAW Import Options"
            )
            
            rl.gui_label(rl.Rectangle(window_offset.x + 10, window_offset.y + 30, 65, 20), "Import file:")
            rl.gui_label(rl.Rectangle(window_offset.x + 85, window_offset.y + 30, 75, 20), file_name)
            rl.gui_label(rl.Rectangle(window_offset.x + 10, window_offset.y + 50, 65, 20), "File size:")
            rl.gui_label(rl.Rectangle(window_offset.x + 85, window_offset.y + 50, 75, 20), f"{data_size} bytes")
            rl.gui_group_box(rl.Rectangle(window_offset.x + 10, window_offset.y + 85, 180, 80), "Resolution")
            rl.gui_label(rl.Rectangle(window_offset.x + 20, window_offset.y + 100, 33, 25), "Width:")
            if rl.gui_value_box(rl.Rectangle(window_offset.x + 60, window_offset.y + 100, 80, 25), None, width_value_ptr, 0, 8192, width_edit_mode):
                width_edit_mode = not width_edit_mode
            rl.gui_label(rl.Rectangle(window_offset.x + 145, window_offset.y + 100, 30, 25), "pixels")
            rl.gui_label(rl.Rectangle(window_offset.x + 20, window_offset.y + 130, 33, 25), "Height:")
            if rl.gui_value_box(rl.Rectangle(window_offset.x + 60, window_offset.y + 130, 80, 25), None, height_value_ptr, 0, 8192, height_edit_mode):
                height_edit_mode = not height_edit_mode
            rl.gui_label(rl.Rectangle(window_offset.x + 145, window_offset.y + 130, 30, 25), "pixels")
            rl.gui_group_box(rl.Rectangle(window_offset.x + 10, window_offset.y + 180, 180, 160), "Pixel Format")
            rl.gui_combo_box(rl.Rectangle(window_offset.x + 20, window_offset.y + 195, 160, 25), ";".join(pixel_format_text_list), pixel_format_active_ptr)
            rl.gui_line(rl.Rectangle(window_offset.x + 20, window_offset.y + 220, 160, 20), None)
            
            if pixel_format_active_ptr[0] != 0:
                rl.gui_disable()
            rl.gui_label(rl.Rectangle(window_offset.x + 20, window_offset.y + 235, 50, 20), "Channels:")
            rl.gui_toggle_group(rl.Rectangle(window_offset.x + 20, window_offset.y + 255, 156/4, 25), ";".join(channels_text_list), channels_active_ptr)
            rl.gui_label(rl.Rectangle(window_offset.x + 20, window_offset.y + 285, 50, 20), "Bit Depth:")
            rl.gui_toggle_group(rl.Rectangle(window_offset.x + 20, window_offset.y + 305, 160/3, 25), ";".join(bit_depth_text_list), bit_depth_active_ptr)
            if pixel_format_active_ptr[0] != 0:
                rl.gui_enable()
            
            rl.gui_group_box(rl.Rectangle(window_offset.x + 10, window_offset.y + 355, 180, 50), "Header")
            rl.gui_label(rl.Rectangle(window_offset.x + 25, window_offset.y + 370, 27, 25), "Size:")
            if rl.gui_value_box(rl.Rectangle(window_offset.x + 55, window_offset.y + 370, 85, 25), None, header_size_value_ptr, 0, 10000, header_size_edit_mode):
                header_size_edit_mode = not header_size_edit_mode
            rl.gui_label(rl.Rectangle(window_offset.x + 145, window_offset.y + 370, 30, 25), "bytes")
            
            btn_load_pressed = rl.gui_button(rl.Rectangle(window_offset.x + 10, window_offset.y + 420, 180, 30), "Import RAW")
            
        rl.end_drawing()
        #----------------------------------------------------------------------------------
    
    # De-Initialization
    #--------------------------------------------------------------------------------------
    if texture.id != 0:
        rl.unload_texture(texture)
    
    rl.close_window()  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
