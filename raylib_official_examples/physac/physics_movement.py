import pyray as rl
from pathlib import Path

# Assuming physac_py.py is in the same directory or accessible in PYTHONPATH
# from physac_py import (
#     PhysicsBodyData, PhysicsShapeVertexData, init_physics, create_physics_body_rectangle,
#     get_physics_bodies_count, get_physics_body, get_physics_shape_vertices_count,
#     get_physics_shape_vertex, close_physics, run_physics_step, set_physics_gravity
# )

# Physac_py defines (simplified for this example)
PHYSAC_MAX_BODIES = 64
PHYSAC_CIRCLE_VERTICES = 24 # Not used here but often part of physac
PHYSAC_DEG2RAD = (3.14159265358979323846 / 180.0) # Not used here but often part of physac
VELOCITY = 0.5

# Mocked Physac classes and functions (replace with actual physac_py.py content)
class PhysicsBodyData:
    def __init__(self, id, enabled, position, velocity, freeze_orient, is_grounded, shape_type, vertex_data, angular_velocity, mass, inverse_mass, inertia, inverse_inertia, static_friction, dynamic_friction, restitution, use_gravity):
        self.id = id
        self.enabled = enabled
        self.position = position
        self.velocity = velocity
        self.freeze_orient = freeze_orient
        self.is_grounded = is_grounded # Crucial for this example
        self.shape_type = shape_type
        self.vertex_data = vertex_data
        self.angular_velocity = angular_velocity
        self.mass = mass
        self.inverse_mass = inverse_mass
        self.inertia = inertia
        self.inverse_inertia = inverse_inertia
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
        self.restitution = restitution
        self.use_gravity = use_gravity
        self.force = rl.Vector2(0,0) # Added for basic physics update
        self.torque = 0.0 # Added for basic physics update

class PhysicsShapeVertexData:
    def __init__(self, count, positions):
        self.count = count
        self.positions = positions

physics_bodies_py = [None] * PHYSAC_MAX_BODIES
next_body_id = 0
physics_gravity_force_py = rl.Vector2(0, 9.81 * 20) # Gravity, scaled for visibility
PHYSAC_TIME_STEP = 1.0 / 60.0 # Simplified timestep

def init_physics_py():
    global physics_bodies_py, next_body_id, physics_gravity_force_py
    physics_bodies_py = [None] * PHYSAC_MAX_BODIES
    next_body_id = 0
    physics_gravity_force_py = rl.Vector2(0, 9.81 * 20) # Reset gravity
    print("Simplified Physac Initialized for Movement")

def create_physics_body_rectangle_py(pos, width, height, density):
    global physics_bodies_py, next_body_id
    if next_body_id >= PHYSAC_MAX_BODIES:
        return None
    mass = width * height * density
    inverse_mass = 1.0 / mass if mass != 0 else 0
    # Simplified inertia for a rectangle
    inertia = (width**2 + height**2) * mass / 12.0 if mass !=0 else 0
    inverse_inertia = 1.0 / inertia if inertia != 0 else 0

    vertices = [
        rl.Vector2(-width/2, -height/2),
        rl.Vector2(width/2, -height/2),
        rl.Vector2(width/2, height/2),
        rl.Vector2(-width/2, height/2)
    ]
    vertex_data = PhysicsShapeVertexData(4, vertices)
    # Initial velocity is zero, is_grounded is false by default for dynamic bodies
    body = PhysicsBodyData(next_body_id, True, pos, rl.Vector2(0,0), False, False, 1, vertex_data, 0.0, mass, inverse_mass, inertia, inverse_inertia, 0.4, 0.2, 0.0, True)
    physics_bodies_py[next_body_id] = body
    next_body_id += 1
    return body

def get_physics_bodies_count_py():
    count = 0
    for body in physics_bodies_py:
        if body is not None:
            count += 1
    return count

def get_physics_body_py(index):
    # This should ideally return the body from the active list, not by dense index if bodies can be removed
    # For this example, assume indices are stable or we iterate through the sparse list
    if 0 <= index < next_body_id and physics_bodies_py[index] is not None:
         return physics_bodies_py[index]
    # Fallback for how the original C code might be calling it (iterating 0 to count-1)
    # This requires a more complex lookup if bodies can be None in the middle of the list.
    # For simplicity, the drawing loop will iterate the raw list.
    current_valid_idx = -1
    for b in physics_bodies_py:
        if b is not None:
            current_valid_idx += 1
            if current_valid_idx == index:
                return b
    return None

def get_physics_shape_vertices_count_py(body_index): # Changed to accept body_index
    # Let's assume body_index is an index into the compact list of bodies
    # or we need a way to get the actual body if the list is sparse.
    body = None
    count = 0
    for b_idx in range(next_body_id):
        if physics_bodies_py[b_idx] is not None:
            if count == body_index:
                body = physics_bodies_py[b_idx]
                break
            count +=1
    if body:
        return body.vertex_data.count
    return 0

def get_physics_shape_vertex_py(body, vertex_index):
    if not body or not body.vertex_data or vertex_index >= body.vertex_data.count:
        return rl.Vector2(0, 0)
    original_vertex = body.vertex_data.positions[vertex_index]
    angle_rad = 0.0 if body.freeze_orient else body.angular_velocity
    cos_a = rl.math_cos(angle_rad)
    sin_a = rl.math_sin(angle_rad)
    rotated_x = original_vertex.x * cos_a - original_vertex.y * sin_a
    rotated_y = original_vertex.x * sin_a + original_vertex.y * cos_a
    final_x = rotated_x + body.position.x
    final_y = rotated_y + body.position.y
    return rl.Vector2(final_x, final_y)

def run_physics_step_py(): # Simplified physics update
    global physics_bodies_py, physics_gravity_force_py
    dt = PHYSAC_TIME_STEP # Fixed time step for simplicity

    for body in physics_bodies_py:
        if body and body.enabled and body.mass > 0: # Update dynamic bodies
            # Apply gravity
            if body.use_gravity:
                body.force.y += physics_gravity_force_py.y * body.mass * (dt / 20) # Scaled dt for effect

            # Update velocity from force ( Verlet integration part 1)
            body.velocity.x += (body.force.x / body.mass) * dt
            body.velocity.y += (body.force.y / body.mass) * dt

            # Update position from velocity (Verlet integration part 2)
            body.position.x += body.velocity.x * dt
            body.position.y += body.velocity.y * dt

            # Simple ground collision and is_grounded update
            # This is a HACK, a proper collision system is needed.
            # Assuming screen_height is ground and there's a floor object at screen_height - 50 (half of 100 height)
            # This doesn't account for other platforms or walls properly.
            if body.position.y + body.vertex_data.positions[2].y > screen_height - 50: # Approx bottom of player
                body.position.y = screen_height - 50 - body.vertex_data.positions[2].y
                body.velocity.y = 0
                body.is_grounded = True
            else:
                body.is_grounded = False # In air if not colliding with ground
            
            # Reset force for next frame
            body.force = rl.Vector2(0,0)

            # Dampen velocity (simple friction)
            body.velocity.x *= 0.98
            # body.velocity.y *= 0.99 # Gravity will overcome this

            # Reset horizontal velocity if not actively moved by keys (handled in main loop)
            # This is a bit of a hack to stop sliding without proper friction.
            # if not (rl.is_key_down(rl.KEY_LEFT) or rl.is_key_down(rl.KEY_RIGHT)):
            #     body.velocity.x *= 0.8 # Stronger damping if no input

def close_physics_py():
    global physics_bodies_py, next_body_id
    physics_bodies_py = [None] * PHYSAC_MAX_BODIES
    next_body_id = 0
    print("Simplified Physac Closed for Movement")

# End of Mocks

THIS_DIR = Path(__file__).resolve().parent
screen_height = 450 # Make screen_height global for run_physics_step_py

def main():
    global screen_height # Allow main to set it
    screen_width = 800
    # screen_height is already global

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "[physac] - Body controller demo")

    logo_x = screen_width - rl.measure_text("Physac", 30) - 10
    logo_y = 15

    init_physics_py()

    floor = create_physics_body_rectangle_py(rl.Vector2(screen_width / 2, screen_height - 50), screen_width, 100, 10)
    if floor: floor.enabled = False # Static

    platform_left = create_physics_body_rectangle_py(rl.Vector2(screen_width * 0.25, screen_height * 0.6), screen_width * 0.25, 10, 10)
    if platform_left: platform_left.enabled = False # Static

    platform_right = create_physics_body_rectangle_py(rl.Vector2(screen_width * 0.75, screen_height * 0.6), screen_width * 0.25, 10, 10)
    if platform_right: platform_right.enabled = False # Static

    wall_left = create_physics_body_rectangle_py(rl.Vector2(-5, screen_height / 2), 10, screen_height, 10)
    if wall_left: wall_left.enabled = False # Static

    wall_right = create_physics_body_rectangle_py(rl.Vector2(screen_width + 5, screen_height / 2), 10, screen_height, 10)
    if wall_right: wall_right.enabled = False # Static

    # Create movement physics body
    body = create_physics_body_rectangle_py(rl.Vector2(screen_width / 2, screen_height / 2), 50, 50, 1)
    if body:
        body.freeze_orient = True
        # body.is_grounded = False # Initially in air

    rl.set_target_fps(60)

    while not rl.window_should_close():
        run_physics_step_py() # Update physics state

        if body: # Ensure body exists
            # Horizontal movement input
            current_vel_x = 0 # Start with no external horizontal velocity impulse this frame
            if rl.is_key_down(rl.KEY_RIGHT):
                current_vel_x = VELOCITY
            elif rl.is_key_down(rl.KEY_LEFT):
                current_vel_x = -VELOCITY
            
            body.velocity.x = current_vel_x * 20 # Apply as direct velocity change, scaled for visibility

            # Vertical movement input checking if player physics body is grounded
            if rl.is_key_down(rl.KEY_UP) and body.is_grounded:
                body.velocity.y = -VELOCITY * 4 * 20 # Apply as direct velocity change, scaled
                body.is_grounded = False # No longer grounded after jump

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_fps(screen_width - 90, screen_height - 30)

        # Draw created physics bodies
        # Iterate through the actual list of bodies that might have None entries
        for i in range(next_body_id): # next_body_id is the count of created bodies so far
            current_body_to_draw = physics_bodies_py[i]
            if current_body_to_draw:
                vertex_count = current_body_to_draw.vertex_data.count
                for j in range(vertex_count):
                    vertex_a = get_physics_shape_vertex_py(current_body_to_draw, j)
                    jj = (j + 1) % vertex_count
                    vertex_b = get_physics_shape_vertex_py(current_body_to_draw, jj)
                    rl.draw_line_v(vertex_a, vertex_b, rl.GREEN)

        rl.draw_text("Use 'ARROWS' to move player", 10, 10, 10, rl.WHITE)
        rl.draw_text("Physac", logo_x, logo_y, 30, rl.WHITE)
        rl.draw_text("Powered by", logo_x + 50, logo_y - 7, 10, rl.WHITE)

        rl.end_drawing()

    close_physics_py()
    rl.close_window()

if __name__ == '__main__':
    main()
