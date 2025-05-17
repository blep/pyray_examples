import pyray as rl
from pathlib import Path
import math
import random

# Physac_py defines (simplified for this example)
PHYSAC_MAX_BODIES = 128 # Increased for shatter
PHYSAC_CIRCLE_VERTICES = 24
PHYSAC_DEG2RAD = (math.pi / 180.0)
PHYSAC_PI = math.pi
SHATTER_FORCE = 200.0

# Mocked Physac classes and functions (replace with actual physac_py.py content)
class PhysicsBodyData:
    def __init__(self, id, enabled, position, shape_type, vertex_data, angular_velocity, mass, inverse_mass, inertia, inverse_inertia, static_friction, dynamic_friction, restitution, use_gravity, is_grounded, freeze_orient, velocity, force, torque):
        self.id = id
        self.enabled = enabled
        self.position = position
        self.shape_type = shape_type # 0 for Circle, 1 for Polygon
        self.vertex_data = vertex_data
        self.angular_velocity = angular_velocity # Actual angle for drawing
        self.mass = mass
        self.inverse_mass = inverse_mass
        self.inertia = inertia
        self.inverse_inertia = inverse_inertia
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
        self.restitution = restitution
        self.use_gravity = use_gravity
        self.is_grounded = is_grounded
        self.freeze_orient = freeze_orient
        self.velocity = velocity
        self.force = force
        self.torque = torque

class PhysicsShapeVertexData:
    def __init__(self, count, positions):
        self.count = count
        self.positions = positions # Local space vertices

physics_bodies_py = [None] * PHYSAC_MAX_BODIES
next_body_id_counter = 0 # To ensure unique IDs even if list slots are reused

def get_next_available_body_slot():
    for i in range(PHYSAC_MAX_BODIES):
        if physics_bodies_py[i] is None:
            return i
    return -1 # No slot available

def init_physics_py():
    global physics_bodies_py, next_body_id_counter
    for i in range(PHYSAC_MAX_BODIES):
        physics_bodies_py[i] = None
    next_body_id_counter = 0
    print("Simplified Physac Initialized for Shatter")

def set_physics_gravity_py(x, y):
    global physics_gravity_force_py
    physics_gravity_force_py = rl.Vector2(x,y)
    # This mock doesn't use gravity in shatter, but real physac would

def create_physics_body_polygon_py(pos, radius, sides, density):
    global physics_bodies_py, next_body_id_counter
    slot_index = get_next_available_body_slot()
    if slot_index == -1:
        print("Max bodies reached, cannot create polygon.")
        return None

    # Approximate mass and inertia (simplified)
    area = 0.5 * sides * radius * radius * math.sin(2 * PHYSAC_PI / sides) # Area of regular polygon
    mass = area * density
    inverse_mass = 1.0 / mass if mass != 0 else 0
    # Inertia for a regular polygon is complex, using approximation for a disk
    inertia = 0.5 * mass * radius * radius if mass !=0 else 0
    inverse_inertia = 1.0 / inertia if inertia != 0 else 0

    vertices = []
    for i in range(sides):
        angle = (i / sides) * 2 * PHYSAC_PI
        vertices.append(rl.Vector2(math.cos(angle) * radius, math.sin(angle) * radius))
    vertex_data = PhysicsShapeVertexData(sides, vertices)

    body_id = next_body_id_counter
    next_body_id_counter += 1
    body = PhysicsBodyData(body_id, True, pos, 1, vertex_data, 0.0, mass, inverse_mass, inertia, inverse_inertia, 0.4, 0.2, 0.0, False, False, False, rl.Vector2(0,0), rl.Vector2(0,0), 0.0)
    physics_bodies_py[slot_index] = body
    return body

def get_physics_bodies_count_py():
    count = 0
    for body in physics_bodies_py:
        if body is not None:
            count += 1
    return count

def get_physics_body_py(index_in_compact_list): # This index is tricky
    # This function in C physac usually takes an index into its internal dense array.
    # In our Python list, bodies can be None. So, we find the Nth non-None body.
    current_valid_body_idx = -1
    for i in range(PHYSAC_MAX_BODIES):
        if physics_bodies_py[i] is not None:
            current_valid_body_idx += 1
            if current_valid_body_idx == index_in_compact_list:
                return physics_bodies_py[i]
    return None

def get_physics_shape_vertices_count_py(body_index_in_compact_list):
    body = get_physics_body_py(body_index_in_compact_list)
    if body:
        return body.vertex_data.count
    return 0

def get_physics_shape_vertex_py(body, vertex_idx):
    if not body or not body.vertex_data or vertex_idx >= body.vertex_data.count:
        return rl.Vector2(0, 0)
    original_vertex = body.vertex_data.positions[vertex_idx]
    angle_rad = 0.0 if body.freeze_orient else body.angular_velocity
    cos_a = rl.math_cos(angle_rad)
    sin_a = rl.math_sin(angle_rad)
    rotated_x = original_vertex.x * cos_a - original_vertex.y * sin_a
    rotated_y = original_vertex.x * sin_a + original_vertex.y * cos_a
    final_x = rotated_x + body.position.x
    final_y = rotated_y + body.position.y
    return rl.Vector2(final_x, final_y)

def physics_shatter_py(body_to_shatter, shatter_pos, force):
    global physics_bodies_py, next_body_id_counter
    if not body_to_shatter or body_to_shatter.vertex_data.count < 3:
        return

    original_verts = body_to_shatter.vertex_data.positions
    num_original_verts = body_to_shatter.vertex_data.count
    original_center = body_to_shatter.position
    original_angle = body_to_shatter.angular_velocity

    # Remove the original body
    for i in range(PHYSAC_MAX_BODIES):
        if physics_bodies_py[i] and physics_bodies_py[i].id == body_to_shatter.id:
            physics_bodies_py[i] = None
            break

    # Create new triangle bodies (shards)
    for i in range(num_original_verts):
        v1_local = original_verts[i]
        v2_local = original_verts[(i + 1) % num_original_verts]
        # For simplicity, using the body's original local center as the third vertex for shards.
        # A more advanced shatter would calculate a true centroid or use the shatter_pos.
        v3_local = rl.Vector2(0,0) # Local origin

        # Transform these local shard vertices to world space based on original body transform
        cos_orig = math.cos(original_angle)
        sin_orig = math.sin(original_angle)

        v1_world = rl.Vector2(v1_local.x*cos_orig - v1_local.y*sin_orig + original_center.x, v1_local.x*sin_orig + v1_local.y*cos_orig + original_center.y)
        v2_world = rl.Vector2(v2_local.x*cos_orig - v2_local.y*sin_orig + original_center.x, v2_local.x*sin_orig + v2_local.y*cos_orig + original_center.y)
        v3_world = rl.Vector2(v3_local.x*cos_orig - v3_local.y*sin_orig + original_center.x, v3_local.x*sin_orig + v3_local.y*cos_orig + original_center.y)

        # Calculate centroid of the new triangle shard in world space
        shard_centroid_world = rl.Vector2((v1_world.x + v2_world.x + v3_world.x) / 3.0, 
                                         (v1_world.y + v2_world.y + v3_world.y) / 3.0)

        # Define shard vertices relative to its new centroid (local space for the shard)
        shard_v1_local = rl.vector2_subtract(v1_world, shard_centroid_world)
        shard_v2_local = rl.vector2_subtract(v2_world, shard_centroid_world)
        shard_v3_local = rl.vector2_subtract(v3_world, shard_centroid_world)
        
        shard_vertices = [shard_v1_local, shard_v2_local, shard_v3_local]
        shard_vertex_data = PhysicsShapeVertexData(3, shard_vertices)

        slot_index = get_next_available_body_slot()
        if slot_index == -1:
            print("Max bodies reached during shatter.")
            break 
        
        # Simplified mass/inertia for shards (e.g., fraction of original or based on area)
        # For this mock, let's use a small fixed mass.
        shard_mass = body_to_shatter.mass / num_original_verts if num_original_verts > 0 else 1.0
        shard_inverse_mass = 1.0 / shard_mass if shard_mass != 0 else 0
        # Very rough inertia for a small triangle
        shard_inertia = 0.1 * shard_mass # Placeholder
        shard_inverse_inertia = 1.0 / shard_inertia if shard_inertia != 0 else 0

        shard_id = next_body_id_counter
        next_body_id_counter += 1
        
        new_shard = PhysicsBodyData(shard_id, True, shard_centroid_world, 1, shard_vertex_data, 0.0, 
                                    shard_mass, shard_inverse_mass, shard_inertia, shard_inverse_inertia, 
                                    0.4, 0.2, 0.1, False, False, False, 
                                    rl.Vector2(0,0), rl.Vector2(0,0), 0.0)
        
        # Apply force from shatter point
        direction = rl.vector2_normalize(rl.vector2_subtract(shard_centroid_world, shatter_pos))
        impulse = rl.vector2_scale(direction, force / shard_mass if shard_mass > 0 else force) # force is an impulse here
        new_shard.velocity = rl.vector2_add(new_shard.velocity, impulse)
        # Add some angular velocity too
        new_shard.angular_velocity = (random.random() - 0.5) * force * 0.01

        physics_bodies_py[slot_index] = new_shard

def run_physics_step_py(): # Simplified physics update
    dt = 1.0 / 60.0 # Fixed time step
    for body in physics_bodies_py:
        if body and body.enabled:
            # Apply forces (gravity, etc. - none in this example for shatter pieces)
            # Update velocity from force
            body.velocity.x += (body.force.x / body.mass if body.mass != 0 else 0) * dt
            body.velocity.y += (body.force.y / body.mass if body.mass != 0 else 0) * dt
            # Update angular velocity from torque
            body.angular_velocity += (body.torque / body.inertia if body.inertia != 0 else 0) * dt

            # Update position and orientation
            body.position.x += body.velocity.x * dt
            body.position.y += body.velocity.y * dt
            # body.angular_velocity is treated as angle for drawing, so this is direct integration of ang_vel to angle
            # A real physics engine would update orientation (e.g. quaternion or matrix) from angular velocity.
            # For this mock, if angular_velocity is an angle, it's already set.
            # If it were true angular velocity, it would be: body.angle += body.angular_velocity * dt

            # Reset forces/torques
            body.force = rl.Vector2(0,0)
            body.torque = 0

            # Simple damping
            body.velocity = rl.vector2_scale(body.velocity, 0.99)
            body.angular_velocity *= 0.99

def close_physics_py():
    global physics_bodies_py, next_body_id_counter
    for i in range(PHYSAC_MAX_BODIES):
        physics_bodies_py[i] = None
    next_body_id_counter = 0
    print("Simplified Physac Closed for Shatter")

# End of Mocks

THIS_DIR = Path(__file__).resolve().parent

def main():
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "[physac] - Shatter demo")

    logo_x = screen_width - rl.measure_text("Physac", 30) - 10
    logo_y = 15

    init_physics_py()
    set_physics_gravity_py(0, 0)

    # Create random polygon physics body to shatter
    # This body reference needs to be updated if it's shattered and recreated
    # For simplicity, we'll just create one initially.
    # The logic for `shatterBody` in C is that it's the *first* body created.
    # In Python, we'll just try to shatter any body found.
    create_physics_body_polygon_py(rl.Vector2(screen_width / 2, screen_height / 2), 
                                   random.randint(80, 200), 
                                   random.randint(3, 8), 10)

    rl.set_target_fps(60)

    while not rl.window_should_close():
        run_physics_step_py()

        if rl.is_key_pressed(rl.KEY_R):
            close_physics_py()
            init_physics_py()
            set_physics_gravity_py(0, 0)
            create_physics_body_polygon_py(rl.Vector2(screen_width / 2, screen_height / 2), 
                                           random.randint(80, 200), 
                                           random.randint(3, 8), 10)
        elif rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            mouse_pos = rl.get_mouse_position()
            # Iterate over a copy of the list of bodies that exist, as shattering modifies the list
            bodies_to_check = [b for b in physics_bodies_py if b is not None]
            for current_body in bodies_to_check:
                # Simple check: if mouse is within bounding box of the body (approx)
                # A more accurate check would be point-in-polygon.
                # For this demo, we'll try to shatter any body clicked near its center for simplicity.
                # The C version shatters *all* bodies. Let's replicate that.
                if current_body: # Check if it hasn't been shattered already in this same click event
                    physics_shatter_py(current_body, mouse_pos, SHATTER_FORCE)

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        # Draw created physics bodies
        # Iterate through the sparse list directly
        for i in range(PHYSAC_MAX_BODIES):
            body_to_draw = physics_bodies_py[i]
            if body_to_draw:
                vertex_count = body_to_draw.vertex_data.count
                for j in range(vertex_count):
                    vertex_a = get_physics_shape_vertex_py(body_to_draw, j)
                    jj = (j + 1) % vertex_count
                    vertex_b = get_physics_shape_vertex_py(body_to_draw, jj)
                    rl.draw_line_v(vertex_a, vertex_b, rl.GREEN)
        
        rl.draw_fps(screen_width - 90, screen_height - 30)
        rl.draw_text("Left mouse button to shatter bodies", 10, 10, 10, rl.WHITE)
        rl.draw_text("'R' to reset", 10, 30, 10, rl.WHITE)
        rl.draw_text("Physac", logo_x, logo_y, 30, rl.WHITE)
        rl.draw_text("Powered by", logo_x + 50, logo_y - 7, 10, rl.WHITE)

        rl.end_drawing()

    close_physics_py()
    rl.close_window()

if __name__ == '__main__':
    main()
