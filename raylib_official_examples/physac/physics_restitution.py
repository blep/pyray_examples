import pyray as rl
from pathlib import Path
import math # For PI and trigonometric functions if needed for circle vertices

# Assuming physac_py.py is in the same directory or accessible in PYTHONPATH
# For this example, I'll use a simplified mock structure.

# Physac_py defines (simplified for this example)
PHYSAC_MAX_BODIES = 64
PHYSAC_CIRCLE_VERTICES = 24 # Standard for drawing circles as polygons
PHYSAC_DEG2RAD = (math.pi / 180.0)
PHYSAC_PI = math.pi

# Mocked Physac classes and functions (replace with actual physac_py.py content)
class PhysicsBodyData:
    def __init__(self, id, enabled, position, restitution, shape_type, vertex_data, angular_velocity, mass, inverse_mass, inertia, inverse_inertia, static_friction, dynamic_friction, use_gravity, is_grounded, freeze_orient, velocity, force, torque):
        self.id = id
        self.enabled = enabled
        self.position = position
        self.restitution = restitution # Key property for this example
        self.shape_type = shape_type # 0 for Circle, 1 for Polygon
        self.vertex_data = vertex_data
        self.angular_velocity = angular_velocity # Rotation angle for drawing
        self.mass = mass
        self.inverse_mass = inverse_mass
        self.inertia = inertia
        self.inverse_inertia = inverse_inertia
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
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
next_body_id = 0
physics_gravity_force_py = rl.Vector2(0, 9.81 * 20) # Gravity, scaled
PHYSAC_TIME_STEP = 1.0 / 60.0 # Simplified timestep

def init_physics_py():
    global physics_bodies_py, next_body_id, physics_gravity_force_py
    physics_bodies_py = [None] * PHYSAC_MAX_BODIES
    next_body_id = 0
    physics_gravity_force_py = rl.Vector2(0, 9.81 * 20)
    print("Simplified Physac Initialized for Restitution")

def create_physics_body_rectangle_py(pos, width, height, density):
    global physics_bodies_py, next_body_id
    if next_body_id >= PHYSAC_MAX_BODIES:
        return None
    mass = width * height * density
    inverse_mass = 1.0 / mass if mass != 0 else 0
    inertia = (width**2 + height**2) * mass / 12.0 if mass !=0 else 0
    inverse_inertia = 1.0 / inertia if inertia != 0 else 0
    vertices = [
        rl.Vector2(-width/2, -height/2),
        rl.Vector2(width/2, -height/2),
        rl.Vector2(width/2, height/2),
        rl.Vector2(-width/2, height/2)
    ]
    vertex_data = PhysicsShapeVertexData(4, vertices)
    body = PhysicsBodyData(next_body_id, True, pos, 0.0, 1, vertex_data, 0.0, mass, inverse_mass, inertia, inverse_inertia, 0.4, 0.2, True, False, False, rl.Vector2(0,0), rl.Vector2(0,0), 0.0)
    physics_bodies_py[next_body_id] = body
    next_body_id += 1
    return body

def create_physics_body_circle_py(pos, radius, density):
    global physics_bodies_py, next_body_id
    if next_body_id >= PHYSAC_MAX_BODIES:
        return None
    mass = PHYSAC_PI * radius * radius * density
    inverse_mass = 1.0 / mass if mass != 0 else 0
    inertia = 0.5 * mass * radius * radius # Solid circle inertia
    inverse_inertia = 1.0 / inertia if inertia != 0 else 0
    
    vertices = []
    for i in range(PHYSAC_CIRCLE_VERTICES):
        angle = (i / PHYSAC_CIRCLE_VERTICES) * 2 * PHYSAC_PI
        vertices.append(rl.Vector2(math.cos(angle) * radius, math.sin(angle) * radius))
    vertex_data = PhysicsShapeVertexData(PHYSAC_CIRCLE_VERTICES, vertices)
    
    body = PhysicsBodyData(next_body_id, True, pos, 0.0, 0, vertex_data, 0.0, mass, inverse_mass, inertia, inverse_inertia, 0.4, 0.2, True, False, False, rl.Vector2(0,0), rl.Vector2(0,0), 0.0)
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
    # Simplified: assumes index is into the compact part of the list
    # A robust version would handle sparse arrays or map abstract ID to array index.
    current_valid_idx = -1
    for b_idx in range(next_body_id):
        if physics_bodies_py[b_idx] is not None:
            current_valid_idx +=1
            if current_valid_idx == index:
                return physics_bodies_py[b_idx]
    return None

def get_physics_shape_vertices_count_py(body_index): # Takes index into the conceptual list of bodies
    body = get_physics_body_py(body_index)
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

def run_physics_step_py(): # Simplified physics update with restitution
    global physics_bodies_py, physics_gravity_force_py
    dt = PHYSAC_TIME_STEP

    for body in physics_bodies_py:
        if body and body.enabled and body.mass > 0:
            if body.use_gravity:
                body.force.y += physics_gravity_force_py.y * body.mass * (dt / 20)
            body.velocity.x += (body.force.x / body.mass) * dt
            body.velocity.y += (body.force.y / body.mass) * dt
            body.position.x += body.velocity.x * dt
            body.position.y += body.velocity.y * dt

            # Simplified ground collision with restitution
            # Assumes screen_height is ground, floor object is at screen_height - 50
            # This is a HACK, a proper collision system is needed.
            # For circles, approx bottom is position.y + radius (if radius was stored directly)
            # Using vertex_data for a generic approach, assuming last vertex is somewhat representative for height.
            # This is not accurate for all shapes or rotations.
            body_bottom_y_approx = body.position.y
            if body.shape_type == 0: # Circle
                 # Approximate radius from vertex data if not stored directly
                 if body.vertex_data.count > 0:
                     body_bottom_y_approx += body.vertex_data.positions[0].y # This is not radius, but an offset
                     # A better approx for circle radius if not stored: body.vertex_data.positions[0].x
            elif body.shape_type == 1: # Polygon
                if body.vertex_data.count > 2:
                    body_bottom_y_approx += body.vertex_data.positions[2].y # e.g. for a rectangle
            
            # Collision with floor (at screen_height - 50 for top of floor)
            if body_bottom_y_approx > screen_height - 50: 
                body.position.y -= (body_bottom_y_approx - (screen_height - 50)) # Penetration correction
                body.velocity.y *= -body.restitution # Apply restitution
                if abs(body.velocity.y) < 1.0: # Come to rest if bounce is too small
                    body.velocity.y = 0
                body.is_grounded = True
            else:
                body.is_grounded = False
            
            body.force = rl.Vector2(0,0)
            body.velocity.x *= 0.99 # Air friction/damping

def close_physics_py():
    global physics_bodies_py, next_body_id
    physics_bodies_py = [None] * PHYSAC_MAX_BODIES
    next_body_id = 0
    print("Simplified Physac Closed for Restitution")

# End of Mocks

THIS_DIR = Path(__file__).resolve().parent
screen_height = 450 # Make global for run_physics_step_py

def main():
    global screen_height
    screen_width = 800

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "[physac] - Restitution demo")

    logo_x = screen_width - rl.measure_text("Physac", 30) - 10
    logo_y = 15

    init_physics_py()

    floor = create_physics_body_rectangle_py(rl.Vector2(screen_width / 2, screen_height - 50), screen_width, 100, 10)
    if floor:
        floor.enabled = False
        floor.restitution = 0.9 # Floor restitution (though usually dynamic obj has it)

    circle_a = create_physics_body_circle_py(rl.Vector2(screen_width * 0.25, screen_height / 2), 30, 10)
    if circle_a: circle_a.restitution = 0.0

    circle_b = create_physics_body_circle_py(rl.Vector2(screen_width * 0.5, screen_height / 2), 30, 10)
    if circle_b: circle_b.restitution = 0.5

    circle_c = create_physics_body_circle_py(rl.Vector2(screen_width * 0.75, screen_height / 2), 30, 10)
    if circle_c: circle_c.restitution = 0.9

    rl.set_target_fps(60)

    while not rl.window_should_close():
        run_physics_step_py()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_fps(screen_width - 90, screen_height - 30)

        # Draw created physics bodies
        # Iterate through the actual list of bodies that might have None entries
        for i in range(next_body_id): 
            body = physics_bodies_py[i]
            if body:
                vertex_count = body.vertex_data.count
                for j in range(vertex_count):
                    vertex_a = get_physics_shape_vertex_py(body, j)
                    jj = (j + 1) % vertex_count
                    vertex_b = get_physics_shape_vertex_py(body, jj)
                    rl.draw_line_v(vertex_a, vertex_b, rl.GREEN)

        rl.draw_text("Restitution amount", (screen_width - rl.measure_text("Restitution amount", 30)) // 2, 75, 30, rl.WHITE)
        if circle_a: rl.draw_text("0%", int(circle_a.position.x - rl.measure_text("0%", 20)/2), int(circle_a.position.y - 7), 20, rl.WHITE)
        if circle_b: rl.draw_text("50%", int(circle_b.position.x - rl.measure_text("50%", 20)/2), int(circle_b.position.y - 7), 20, rl.WHITE)
        if circle_c: rl.draw_text("90%", int(circle_c.position.x - rl.measure_text("90%", 20)/2), int(circle_c.position.y - 7), 20, rl.WHITE)

        rl.draw_text("Physac", logo_x, logo_y, 30, rl.WHITE)
        rl.draw_text("Powered by", logo_x + 50, logo_y - 7, 10, rl.WHITE)

        rl.end_drawing()

    close_physics_py()
    rl.close_window()

if __name__ == '__main__':
    main()
