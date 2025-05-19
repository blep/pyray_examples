"""raygui - custom property list control
DEPENDENCIES:
    raylib 4.0  - Windowing/input management and drawing.
    raygui 3.0  - Immediate-mode GUI controls.
COMPILATION (Windows - MinGW):
    gcc -o $(NAME_PART).exe $(FILE_NAME) -I../../src -lraylib -lopengl32 -lgdi32 -std=c99
LICENSE: zlib/libpng
Copyright (c) 2020-2024 Vlad Adrian (@Demizdor) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import json
from enum import Enum, auto

THIS_DIR = Path(__file__).resolve().parent

# Property types enum
class PropertyType(Enum):
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    TEXT = auto()
    SELECT = auto()
    VECTOR2 = auto()
    COLOR = auto()
    SECTION = auto()

# Property class (simplified from the C version)
class Property:
    def __init__(self, name, prop_type, value, options=None):
        self.name = name
        self.type = prop_type
        self.value = value
        self.options = options
        self.edit_mode = False
        self.expanded = True  # For sections

# Draw a property list
def gui_property_list(bounds, properties, focus_ptr, scroll_ptr):
    item_height = rl.gui_get_style(rl.LISTVIEW, rl.LIST_ITEMS_HEIGHT)
    visible_properties = int(bounds.height / item_height)
    
    # Calculate content height
    content_height = len(properties) * item_height
    
    # Handle scrolling
    if content_height > bounds.height:
        scroll_bar_width = rl.get_style(rl.LISTVIEW, rl.SCROLLBAR_WIDTH)
        scroll_view = rl.gui_scroll_panel(
            bounds,
            None,
            rl.Rectangle(0, 0, bounds.width - scroll_bar_width, content_height),
            scroll_ptr
        )
    else:
        scroll_view = bounds
        scroll_ptr[0] = (0,0)
    
    # Draw visible properties
    start_index = int(scroll_ptr[0] / item_height) if content_height > bounds.height else 0
    end_index = min(start_index + visible_properties + 1, len(properties))
    
    # Begin scissor mode to only draw visible elements
    rl.begin_scissor_mode(int(scroll_view.x), int(scroll_view.y), 
                         int(scroll_view.width), int(scroll_view.height))
    
    # Draw properties
    for i in range(start_index, end_index):
        prop = properties[i]
        
        # Calculate property rectangle
        prop_rect = rl.Rectangle(
            bounds.x,
            bounds.y + (i * item_height) - scroll_ptr[0],
            bounds.width - rl.get_style(rl.LISTVIEW, rl.SCROLLBAR_WIDTH) if content_height > bounds.height else bounds.width,
            item_height
        )
        
        # Draw property background
        prop_bg_color = rl.LIGHTGRAY if i == focus_ptr[0] else rl.get_color(rl.get_style(rl.DEFAULT, rl.BACKGROUND_COLOR))
        rl.draw_rectangle_rec(prop_rect, prop_bg_color)
        
        # Split rectangle for name and value
        name_rect = rl.Rectangle(prop_rect.x, prop_rect.y, prop_rect.width * 0.4, prop_rect.height)
        value_rect = rl.Rectangle(prop_rect.x + name_rect.width, prop_rect.y, 
                                prop_rect.width - name_rect.width, prop_rect.height)
        
        # Draw property name
        name = prop.name
        if prop.type == PropertyType.SECTION:
            name = f"▶ {name}" if not prop.expanded else f"▼ {name}"
        
        rl.draw_text(name, int(name_rect.x + 4), int(name_rect.y + name_rect.height / 2 - 10), 10, rl.BLACK)
        
        # Draw property value based on type
        if prop.type == PropertyType.BOOL:
            old_value = prop.value
            prop.value = rl.gui_check_box(
                rl.Rectangle(value_rect.x + 4, value_rect.y + value_rect.height/2 - 10, 20, 20),
                "", prop.value
            )
            if old_value != prop.value and focus_ptr[0] != i:
                focus_ptr[0] = i
                
        elif prop.type == PropertyType.INT:
            old_edit_mode = prop.edit_mode
            value_ptr = rl.ffi.new('int *', prop.value)
            if rl.gui_value_box(
                rl.Rectangle(value_rect.x + 4, value_rect.y + 2, value_rect.width - 8, value_rect.height - 4),
                None, value_ptr, -1000, 1000, prop.edit_mode
            ):
                prop.edit_mode = not prop.edit_mode
                if focus_ptr[0] != i:
                    focus_ptr[0] = i
            
            prop.value = value_ptr[0]
            
        elif prop.type == PropertyType.FLOAT:
            value_str = f"{prop.value:.3f}"
            rl.draw_text(value_str, int(value_rect.x + 4), int(value_rect.y + value_rect.height/2 - 10), 10, rl.BLACK)
            
            # If clicked, set focus
            if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON) and rl.check_collision_point_rec(rl.get_mouse_position(), value_rect):
                focus_ptr[0] = i
                
        elif prop.type == PropertyType.TEXT:
            text_display = prop.value if len(prop.value) < 15 else prop.value[:12] + "..."
            rl.draw_text(text_display, int(value_rect.x + 4), int(value_rect.y + value_rect.height/2 - 10), 10, rl.BLACK)
            
            # If clicked, set focus
            if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON) and rl.check_collision_point_rec(rl.get_mouse_position(), value_rect):
                focus_ptr[0] = i
                
        elif prop.type == PropertyType.SELECT:
            options = prop.options.split(";")
            option_index_ptr = rl.ffi.new('int *', prop.value)
            
            if rl.gui_combo_box(
                rl.Rectangle(value_rect.x + 4, value_rect.y + 2, value_rect.width - 8, value_rect.height - 4),
                prop.options, option_index_ptr
            ):
                prop.value = option_index_ptr[0]
                if focus_ptr[0] != i:
                    focus_ptr[0] = i
                    
        elif prop.type == PropertyType.VECTOR2:
            vec_text = f"X: {prop.value.x}, Y: {prop.value.y}"
            rl.draw_text(vec_text, int(value_rect.x + 4), int(value_rect.y + value_rect.height/2 - 10), 10, rl.BLACK)
            
            # If clicked, set focus
            if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON) and rl.check_collision_point_rec(rl.get_mouse_position(), value_rect):
                focus_ptr[0] = i
                
        elif prop.type == PropertyType.COLOR:
            # Draw color preview
            color_rect = rl.Rectangle(value_rect.x + 4, value_rect.y + 4, value_rect.width - 8, value_rect.height - 8)
            rl.draw_rectangle_rec(color_rect, prop.value)
            rl.draw_rectangle_lines_ex(color_rect, 1, rl.BLACK)
            
            # If clicked, set focus
            if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON) and rl.check_collision_point_rec(rl.get_mouse_position(), value_rect):
                focus_ptr[0] = i
        
        # Handle section expansion logic
        if prop.type == PropertyType.SECTION:
            if rl.is_mouse_button_released(rl.MOUSE_LEFT_BUTTON) and rl.check_collision_point_rec(rl.get_mouse_position(), name_rect):
                prop.expanded = not prop.expanded
                if focus_ptr[0] != i:
                    focus_ptr[0] = i
    
    rl.end_scissor_mode()
    
    return True

# Save properties to file
def save_properties(file_path, properties):
    # Convert property data to JSON serializable format
    data = []
    for prop in properties:
        if prop.type == PropertyType.VECTOR2:
            value = {"x": prop.value.x, "y": prop.value.y}
        elif prop.type == PropertyType.COLOR:
            value = {"r": prop.value.r, "g": prop.value.g, "b": prop.value.b, "a": prop.value.a}
        else:
            value = prop.value
            
        data.append({
            "name": prop.name,
            "type": prop.type.name,
            "value": value,
            "options": prop.options
        })
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    # Initialization
    #---------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450
    
    rl.init_window(screen_width, screen_height, "raygui - property list (simplified)")
    
    # Create properties
    properties = [
        Property("Bool", PropertyType.BOOL, False),
        Property("Section", PropertyType.SECTION, 2),  # Section with 2 children
        Property("Int", PropertyType.INT, 123),
        Property("Float", PropertyType.FLOAT, 0.99),
        Property("Text", PropertyType.TEXT, "Hello!"),
        Property("Select", PropertyType.SELECT, 0, "ONE;TWO;THREE;FOUR"),
        Property("Vec2", PropertyType.VECTOR2, rl.Vector2(20, 20)),
        Property("Color", PropertyType.COLOR, rl.Color(0, 255, 0, 255))
    ]
    
    # GUI state
    focus_ptr = rl.ffi.new('int *', 0)
    scroll_ptr = rl.ffi.new('Vector2 *')
    scroll_ptr.x = 0
    scroll_ptr.y = 0
    
    grid_mouse_cell = rl.Vector2(0, 0)
    grid_mouse_cell_ptr = rl.ffi.new('Vector2 *')
    grid_mouse_cell_ptr.x = 0
    grid_mouse_cell_ptr.y = 0
    
    # Set style
    rl.gui_load_style_default()
    rl.gui_set_style(rl.LISTVIEW, rl.LIST_ITEMS_HEIGHT, 24)
    rl.gui_set_style(rl.LISTVIEW, rl.SCROLLBAR_WIDTH, 12)
    
    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------
    
    # Main game loop
    while not rl.window_should_close():
        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        # PORT: "0xffff_ffff &" is a work-around for converting the negative int32 to uint32
        rl.clear_background(rl.get_color(0xffff_ffff & rl.gui_get_style(rl.DEFAULT, rl.BACKGROUND_COLOR)))
        
        # Draw grid background
        rl.gui_grid(rl.Rectangle(0, 0, screen_width, screen_height), "Property List", 20.0, 2, grid_mouse_cell_ptr)
        grid_mouse_cell.x = grid_mouse_cell_ptr.x
        grid_mouse_cell.y = grid_mouse_cell_ptr.y
        
        # Draw property list
        gui_property_list(
            rl.Rectangle((screen_width - 180)/2, (screen_height - 280)/2, 180, 280),
            properties,
            focus_ptr,
            scroll_ptr
        )
        
        # Display some info if first property is checked
        if properties[0].value:
            rl.draw_text(
                f"FOCUS: {focus_ptr[0]} | SCROLL: {int(scroll_ptr.y)} | FPS: {rl.get_fps()}",
                int(properties[6].value.x),
                int(properties[6].value.y),
                20,
                properties[7].value  # Color
            )
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------
    
    # De-Initialization
    #--------------------------------------------------------------------------------------
    save_properties(str(THIS_DIR/"test.props.json"), properties)  # Save properties to file on exit
    
    rl.close_window()
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
