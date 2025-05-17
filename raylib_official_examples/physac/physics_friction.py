import pyray as rl
from pathlib import Path

# Assuming physac_py.py contains the necessary classes and functions
# If not, you'll need to define or import them.
# For this example, I'll assume a simplified physac_py structure
# based on the C example and common patterns.

# Physac_py defines (simplified for this example)
PHYSAC_MAX_BODIES = 64
PHYSAC_CIRCLE_VERTICES = 24
PHYSAC_DEG2RAD = (3.14159265358979323846 / 180.0)

# Mocked Physac classes and functions (replace with actual physac_py.py content)
# These are placeholders to make the script runnable and demonstrate the migration.
class PhysicsBodyData:
    def __init__(self, id, enabled, position, static_friction, dynamic_friction, shape_type, vertex_data, angular_velocity):
        self.id = id
        self.enabled = enabled
        self.position = position
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
        self.shape_type = shape_type
        self.vertex_data = vertex_data
        self.angular_velocity = angular_velocity # Used to store rotation in this simplified model

class PhysicsShapeVertexData:
    def __init__(self, count, positions):
        self.count = count
        self.positions = positions

physics_bodies_py = [None] * PHYSAC_MAX_BODIES
next_body_id = 0

def init_physics_py():
    global physics_bodies_py, next_body_id
    physics_bodies_py = [None] * PHYSAC_MAX_BODIES
    next_body_id = 0
    print("Simplified Physac Initialized")

def create_physics_body_rectangle_py(pos, width, height, density):
    global physics_bodies_py, next_body_id
    if next_body_id >= PHYSAC_MAX_BODIES:
        return None
    # Simplified: density not used directly for mass, just for creation
    vertices = [
        rl.Vector2(-width/2, -height/2),
        rl.Vector2(width/2, -height/2),
        rl.Vector2(width/2, height/2),
        rl.Vector2(-width/2, height/2)
    ]
    vertex_data = PhysicsShapeVertexData(4, vertices)
    body = PhysicsBodyData(next_body_id, True, pos, 0.4, 0.2, 1, vertex_data, 0.0) # shape_type 1 for Polygon
    physics_bodies_py[next_body_id] = body
    next_body_id += 1
    return body

def set_physics_body_rotation_py(body, radians):
    if body:
        body.angular_velocity = radians # Storing rotation directly

def get_physics_bodies_count_py():
    count = 0
    for body in physics_bodies_py:
        if body is not None:
            count += 1
    return count

def get_physics_body_py(index):
    if 0 <= index < next_body_id and physics_bodies_py[index] is not None:
        return physics_bodies_py[index]
    return None

def get_physics_shape_vertices_count_py(body_index): # Changed to accept body_index for consistency
    body = get_physics_body_py(body_index)
    if body:
        return body.vertex_data.count
    return 0

def get_physics_shape_vertex_py(body, vertex_index):
    if not body or not body.vertex_data or vertex_index >= body.vertex_data.count:
        return rl.Vector2(0, 0)

    original_vertex = body.vertex_data.positions[vertex_index]
    angle_rad = body.angular_velocity # Rotation is stored here

    cos_a = rl.math_cos(angle_rad)
    sin_a = rl.math_sin(angle_rad)

    # Rotate
    rotated_x = original_vertex.x * cos_a - original_vertex.y * sin_a
    rotated_y = original_vertex.x * sin_a + original_vertex.y * cos_a

    # Translate
    final_x = rotated_x + body.position.x
    final_y = rotated_y + body.position.y

    return rl.Vector2(final_x, final_y)

def close_physics_py():
    global physics_bodies_py, next_body_id
    physics_bodies_py = [None] * PHYSAC_MAX_BODIES
    next_body_id = 0
    print("Simplified Physac Closed")

# End of Mocks - Replace with actual physac_py.py imports/definitions

THIS_DIR = Path(__file__).resolve().parent

def main():
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "[physac] Friction demo")

    logo_x = screen_width - rl.measure_text("Physac", 30) - 10
    logo_y = 15

    init_physics_py()

    floor = create_physics_body_rectangle_py(rl.Vector2(screen_width / 2, screen_height), screen_width, 100, 10)
    if floor: floor.enabled = False

    wall = create_physics_body_rectangle_py(rl.Vector2(screen_width / 2, screen_height * 0.8), 10, 80, 10)
    if wall: wall.enabled = False

    rect_left = create_physics_body_rectangle_py(rl.Vector2(25, screen_height - 5), 250, 250, 10)
    if rect_left:
        rect_left.enabled = False
        set_physics_body_rotation_py(rect_left, 30 * PHYSAC_DEG2RAD)

    rect_right = create_physics_body_rectangle_py(rl.Vector2(screen_width - 25, screen_height - 5), 250, 250, 10)
    if rect_right:
        rect_right.enabled = False
        set_physics_body_rotation_py(rect_right, 330 * PHYSAC_DEG2RAD)

    body_a = create_physics_body_rectangle_py(rl.Vector2(35, screen_height * 0.6), 40, 40, 10)
    if body_a:
        body_a.static_friction = 0.1
        body_a.dynamic_friction = 0.1
        set_physics_body_rotation_py(body_a, 30 * PHYSAC_DEG2RAD)

    body_b = create_physics_body_rectangle_py(rl.Vector2(screen_width - 35, screen_height * 0.6), 40, 40, 10)
    if body_b:
        body_b.static_friction = 1.0 # Corrected to float
        body_b.dynamic_friction = 1.0 # Corrected to float
        set_physics_body_rotation_py(body_b, 330 * PHYSAC_DEG2RAD)

    rl.set_target_fps(60)

    while not rl.window_should_close():
        # Update (Physac update step would go here in a full implementation)
        # run_physics_step() # Example call

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_fps(screen_width - 90, screen_height - 30)

        bodies_count = get_physics_bodies_count_py()
        for i in range(bodies_count):
            body = get_physics_body_py(i)
            if body:
                vertex_count = get_physics_shape_vertices_count_py(i) # Pass index
                for j in range(vertex_count):
                    vertex_a = get_physics_shape_vertex_py(body, j)
                    jj = (j + 1) % vertex_count
                    vertex_b = get_physics_shape_vertex_py(body, jj)
                    rl.draw_line_v(vertex_a, vertex_b, rl.GREEN)

        rl.draw_rectangle(0, screen_height - 49, screen_width, 49, rl.BLACK)

        rl.draw_text("Friction amount", (screen_width - rl.measure_text("Friction amount", 30)) // 2, 75, 30, rl.WHITE)
        if body_a: # Check if body_a exists before accessing its properties
            rl.draw_text("0.1", int(body_a.position.x - rl.measure_text("0.1", 20) / 2), int(body_a.position.y - 7), 20, rl.WHITE)
        if body_b: # Check if body_b exists before accessing its properties
            rl.draw_text("1", int(body_b.position.x - rl.measure_text("1", 20) / 2), int(body_b.position.y - 7), 20, rl.WHITE)

        rl.draw_text("Physac", logo_x, logo_y, 30, rl.WHITE)
        rl.draw_text("Powered by", logo_x + 50, logo_y - 7, 10, rl.WHITE)

        rl.end_drawing()

    close_physics_py()
    rl.close_window()

if __name__ == '__main__':
    main()
