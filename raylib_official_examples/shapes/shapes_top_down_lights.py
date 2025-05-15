"""raylib [shapes] example - top down lights
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 4.2, last time updated with raylib 4.2
Example contributed by Jeffery Myers (@JeffM2501) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2022-2025 Jeffery Myers (@JeffM2501)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Custom Blend Modes
RLGL_SRC_ALPHA = 0x0302
RLGL_MIN = 0x8007
RLGL_MAX = 0x8008

MAX_BOXES = 20
MAX_SHADOWS = MAX_BOXES * 3  # MAX_BOXES *3. Each box can cast up to two shadow volumes for the edges it is away from, and one for the box itself
MAX_LIGHTS = 16

# Shadow geometry type
class ShadowGeometry:
    def __init__(self):
        self.vertices = [rl.Vector2(0, 0) for _ in range(4)]

# Light info type
class LightInfo:
    def __init__(self):
        self.active = False         # Is this light slot active?
        self.dirty = False          # Does this light need to be updated?
        self.valid = False          # Is this light in a valid position?
        
        self.position = rl.Vector2(0, 0)  # Light position
        self.mask = None            # Alpha mask for the light
        self.outer_radius = 0.0     # The distance the light touches
        self.bounds = rl.Rectangle(0, 0, 0, 0)  # A cached rectangle of the light bounds to help with culling
        
        self.shadows = [ShadowGeometry() for _ in range(MAX_SHADOWS)]
        self.shadow_count = 0

# Initialize lights array
lights = [LightInfo() for _ in range(MAX_LIGHTS)]

# Move a light and mark it as dirty so that we update it's mask next frame
def move_light(slot, x, y):
    lights[slot].dirty = True
    lights[slot].position.x = x
    lights[slot].position.y = y
    
    # update the cached bounds
    lights[slot].bounds.x = x - lights[slot].outer_radius
    lights[slot].bounds.y = y - lights[slot].outer_radius

# Compute a shadow volume for the edge
# It takes the edge and projects it back by the light radius and turns it into a quad
def compute_shadow_volume_for_edge(slot, sp, ep):
    if lights[slot].shadow_count >= MAX_SHADOWS:
        return
    
    extension = lights[slot].outer_radius * 2
    
    sp_vector = rl.vector2_normalize(rl.vector2_subtract(sp, lights[slot].position))
    sp_projection = rl.vector2_add(sp, rl.vector2_scale(sp_vector, extension))
    
    ep_vector = rl.vector2_normalize(rl.vector2_subtract(ep, lights[slot].position))
    ep_projection = rl.vector2_add(ep, rl.vector2_scale(ep_vector, extension))
    
    lights[slot].shadows[lights[slot].shadow_count].vertices[0] = sp
    lights[slot].shadows[lights[slot].shadow_count].vertices[1] = ep
    lights[slot].shadows[lights[slot].shadow_count].vertices[2] = ep_projection
    lights[slot].shadows[lights[slot].shadow_count].vertices[3] = sp_projection
    
    lights[slot].shadow_count += 1

# Draw the light and shadows to the mask for a light
def draw_light_mask(slot):
    # Use the light mask
    rl.begin_texture_mode(lights[slot].mask)
    
    rl.clear_background(rl.WHITE)
    
    # Force the blend mode to only set the alpha of the destination
    rl.rl_set_blend_factors(RLGL_SRC_ALPHA, RLGL_SRC_ALPHA, RLGL_MIN)
    rl.rl_set_blend_mode(rl.BLEND_CUSTOM)
    
    # If we are valid, then draw the light radius to the alpha mask
    if lights[slot].valid:
        rl.draw_circle_gradient(
            int(lights[slot].position.x), 
            int(lights[slot].position.y), 
            lights[slot].outer_radius, 
            rl.fade(rl.WHITE, 0), 
            rl.WHITE
        )
    
    rl.rl_draw_render_batch_active()
    
    # Cut out the shadows from the light radius by forcing the alpha to maximum
    rl.rl_set_blend_mode(rl.BLEND_ALPHA)
    rl.rl_set_blend_factors(RLGL_SRC_ALPHA, RLGL_SRC_ALPHA, RLGL_MAX)
    rl.rl_set_blend_mode(rl.BLEND_CUSTOM)
    
    # Draw the shadows to the alpha mask
    for i in range(lights[slot].shadow_count):
        vertices = lights[slot].shadows[i].vertices
        rl.draw_triangle_fan(vertices, 4, rl.WHITE)
    
    rl.rl_draw_render_batch_active()
    
    # Go back to normal blend mode
    rl.rl_set_blend_mode(rl.BLEND_ALPHA)
    
    rl.end_texture_mode()

# Setup a light
def setup_light(slot, x, y, radius):
    lights[slot].active = True
    lights[slot].valid = False  # The light must prove it is valid
    lights[slot].mask = rl.load_render_texture(rl.get_screen_width(), rl.get_screen_height())
    lights[slot].outer_radius = radius
    
    lights[slot].bounds.width = radius * 2
    lights[slot].bounds.height = radius * 2
    
    move_light(slot, x, y)
    
    # Force the render texture to have something in it
    draw_light_mask(slot)

# See if a light needs to update it's mask
def update_light(slot, boxes, count):
    if not lights[slot].active or not lights[slot].dirty:
        return False
    
    lights[slot].dirty = False
    lights[slot].shadow_count = 0
    lights[slot].valid = False
    
    for i in range(count):
        # Are we in a box? if so we are not valid
        if rl.check_collision_point_rec(lights[slot].position, boxes[i]):
            return False
        
        # If this box is outside our bounds, we can skip it
        if not rl.check_collision_recs(lights[slot].bounds, boxes[i]):
            continue
        
        # Check the edges that are on the same side we are, and cast shadow volumes out from them
        
        # Top
        sp = rl.Vector2(boxes[i].x, boxes[i].y)
        ep = rl.Vector2(boxes[i].x + boxes[i].width, boxes[i].y)
        
        if lights[slot].position.y > ep.y:
            compute_shadow_volume_for_edge(slot, sp, ep)
        
        # Right
        sp = ep
        ep.y += boxes[i].height
        if lights[slot].position.x < ep.x:
            compute_shadow_volume_for_edge(slot, sp, ep)
        
        # Bottom
        sp = ep
        ep.x -= boxes[i].width
        if lights[slot].position.y < ep.y:
            compute_shadow_volume_for_edge(slot, sp, ep)
        
        # Left
        sp = ep
        ep.y -= boxes[i].height
        if lights[slot].position.x > ep.x:
            compute_shadow_volume_for_edge(slot, sp, ep)
        
        # The box itself
        lights[slot].shadows[lights[slot].shadow_count].vertices[0] = rl.Vector2(boxes[i].x, boxes[i].y)
        lights[slot].shadows[lights[slot].shadow_count].vertices[1] = rl.Vector2(boxes[i].x, boxes[i].y + boxes[i].height)
        lights[slot].shadows[lights[slot].shadow_count].vertices[2] = rl.Vector2(boxes[i].x + boxes[i].width, boxes[i].y + boxes[i].height)
        lights[slot].shadows[lights[slot].shadow_count].vertices[3] = rl.Vector2(boxes[i].x + boxes[i].width, boxes[i].y)
        lights[slot].shadow_count += 1
    
    lights[slot].valid = True
    
    draw_light_mask(slot)
    
    return True

# Set up some boxes
def setup_boxes(boxes):
    boxes[0] = rl.Rectangle(150, 80, 40, 40)
    boxes[1] = rl.Rectangle(1200, 700, 40, 40)
    boxes[2] = rl.Rectangle(200, 600, 40, 40)
    boxes[3] = rl.Rectangle(1000, 50, 40, 40)
    boxes[4] = rl.Rectangle(500, 350, 40, 40)
    
    for i in range(5, MAX_BOXES):
        boxes[i] = rl.Rectangle(
            rl.get_random_value(0, rl.get_screen_width()),
            rl.get_random_value(0, rl.get_screen_height()),
            rl.get_random_value(10, 100),
            rl.get_random_value(10, 100)
        )
    
    return MAX_BOXES

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450
    
    rl.init_window(screen_width, screen_height, "raylib [shapes] example - top down lights")
    
    # Initialize our 'world' of boxes
    boxes = [rl.Rectangle(0, 0, 0, 0) for _ in range(MAX_BOXES)]
    box_count = setup_boxes(boxes)
    
    # Create a checkerboard ground texture
    img = rl.gen_image_checked(64, 64, 32, 32, rl.DARKBROWN, rl.DARKGRAY)
    background_texture = rl.load_texture_from_image(img)
    rl.unload_image(img)
    
    # Create a global light mask to hold all the blended lights
    light_mask = rl.load_render_texture(rl.get_screen_width(), rl.get_screen_height())
    
    # Setup initial light
    setup_light(0, 600, 400, 300)
    next_light = 1
    
    show_lines = False
    
    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------
    
    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # Drag light 0
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            mouse_pos = rl.get_mouse_position()
            move_light(0, mouse_pos.x, mouse_pos.y)
        
        # Make a new light
        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_RIGHT) and (next_light < MAX_LIGHTS):
            mouse_pos = rl.get_mouse_position()
            setup_light(next_light, mouse_pos.x, mouse_pos.y, 200)
            next_light += 1
        
        # Toggle debug info
        if rl.is_key_pressed(rl.KEY_F1):
            show_lines = not show_lines
        
        # Update the lights and keep track if any were dirty so we know if we need to update the master light mask
        dirty_lights = False
        for i in range(MAX_LIGHTS):
            if update_light(i, boxes, box_count):
                dirty_lights = True
        
        # Update the light mask
        if dirty_lights:
            # Build up the light mask
            rl.begin_texture_mode(light_mask)
            
            rl.clear_background(rl.BLACK)
            
            # Force the blend mode to only set the alpha of the destination
            rl.rl_set_blend_factors(RLGL_SRC_ALPHA, RLGL_SRC_ALPHA, RLGL_MIN)
            rl.rl_set_blend_mode(rl.BLEND_CUSTOM)
            
            # Merge in all the light masks
            for i in range(MAX_LIGHTS):
                if lights[i].active:
                    src_rec = rl.Rectangle(0, 0, float(rl.get_screen_width()), -float(rl.get_screen_height()))
                    rl.draw_texture_rec(lights[i].mask.texture, src_rec, rl.Vector2(0, 0), rl.WHITE)
            
            rl.rl_draw_render_batch_active()
            
            # Go back to normal blend
            rl.rl_set_blend_mode(rl.BLEND_ALPHA)
            rl.end_texture_mode()
        #----------------------------------------------------------------------------------
        
        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.BLACK)
        
        # Draw the tile background
        bg_rect = rl.Rectangle(0, 0, float(rl.get_screen_width()), float(rl.get_screen_height()))
        rl.draw_texture_rec(background_texture, bg_rect, rl.Vector2(0, 0), rl.WHITE)
        
        # Overlay the shadows from all the lights
        light_src_rec = rl.Rectangle(0, 0, float(rl.get_screen_width()), -float(rl.get_screen_height()))
        alpha = 0.75 if show_lines else 1.0
        rl.draw_texture_rec(light_mask.texture, light_src_rec, rl.Vector2(0, 0), rl.fade(rl.WHITE, alpha))
        
        # Draw the lights
        for i in range(MAX_LIGHTS):
            if lights[i].active:
                color = rl.YELLOW if i == 0 else rl.WHITE
                rl.draw_circle(int(lights[i].position.x), int(lights[i].position.y), 10, color)
        
        if show_lines:
            for s in range(lights[0].shadow_count):
                vertices = lights[0].shadows[s].vertices
                rl.draw_triangle_fan(vertices, 4, rl.DARKPURPLE)
            
            for b in range(box_count):
                if rl.check_collision_recs(boxes[b], lights[0].bounds):
                    rl.draw_rectangle_rec(boxes[b], rl.PURPLE)
                
                rl.draw_rectangle_lines(int(boxes[b].x), int(boxes[b].y), int(boxes[b].width), int(boxes[b].height), rl.DARKBLUE)
            
            rl.draw_text("(F1) Hide Shadow Volumes", 10, 50, 10, rl.GREEN)
        else:
            rl.draw_text("(F1) Show Shadow Volumes", 10, 50, 10, rl.GREEN)
        
        rl.draw_fps(screen_width - 80, 10)
        rl.draw_text("Drag to move light #1", 10, 10, 10, rl.DARKGREEN)
        rl.draw_text("Right click to add new light", 10, 30, 10, rl.DARKGREEN)
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------
    
    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(background_texture)
    rl.unload_render_texture(light_mask)
    for i in range(MAX_LIGHTS):
        if lights[i].active:
            rl.unload_render_texture(lights[i].mask)
    
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()