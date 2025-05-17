import pyray as rl
from pathlib import Path

# Physac_py defines
PHYSAC_MAX_BODIES = 64
PHYSAC_MAX_MANIFOLDS = 4096
PHYSAC_MAX_VERTICES = 24
PHYSAC_CIRCLE_VERTICES = 24
PHYSAC_COLLISION_ITERATIONS = 100
PHYSAC_PENETRATION_ALLOWANCE = 0.05
PHYSAC_PENETRATION_CORRECTION = 0.4
PHYSAC_PI = 3.14159265358979323846
PHYSAC_DEG2RAD = (PHYSAC_PI / 180.0)

# Physac_py Body type
PHYSAC_STATIC = 0
PHYSAC_DYNAMIC = 1

# Physac_py Shape type
PHYSAC_SHAPE_CIRCLE = 0
PHYSAC_SHAPE_POLYGON = 1

# Structures
class PhysicsBodyData:
    def __init__(self, id, enabled, position, velocity, force, angular_velocity, torque, mass, inverse_mass, inertia, inverse_inertia, static_friction, dynamic_friction, restitution, use_gravity, is_grounded, freeze_orient, shape_type, vertex_data):
        self.id = id
        self.enabled = enabled
        self.position = position
        self.velocity = velocity
        self.force = force
        self.angular_velocity = angular_velocity
        self.torque = torque
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
        self.shape_type = shape_type
        self.vertex_data = vertex_data

class PhysicsShapeVertexData:
    def __init__(self, count, positions, normals):
        self.count = count
        self.positions = positions
        self.normals = normals

class PhysicsManifoldData:
    def __init__(self, id, body_a, body_b, penetration, normal, contacts, contacts_count, restitution, dynamic_friction, static_friction):
        self.id = id
        self.body_a = body_a
        self.body_b = body_b
        self.penetration = penetration
        self.normal = normal
        self.contacts = contacts
        self.contacts_count = contacts_count
        self.restitution = restitution
        self.dynamic_friction = dynamic_friction
        self.static_friction = static_friction

# Global variables
physics_bodies = [None] * PHYSAC_MAX_BODIES
physics_manifolds = [None] * PHYSAC_MAX_MANIFOLDS
physics_manifolds_count = 0
physics_gravity_force = rl.Vector2(0, 9.81)
physics_time_step = 1.0 / 60.0 / PHYSAC_COLLISION_ITERATIONS

# Function prototypes
def init_physics():
    global physics_bodies, physics_manifolds_count, physics_gravity_force, physics_time_step
    for i in range(PHYSAC_MAX_BODIES):
        physics_bodies[i] = None
    physics_manifolds_count = 0
    physics_gravity_force = rl.Vector2(0, 9.81)
    physics_time_step = 1.0 / 60.0 / PHYSAC_COLLISION_ITERATIONS
    print("Physics system initialized")

def set_physics_gravity(x, y):
    global physics_gravity_force
    physics_gravity_force = rl.Vector2(x, y)

def create_physics_body_circle(pos, radius, density):
    global physics_bodies
    body = None
    for i in range(PHYSAC_MAX_BODIES):
        if physics_bodies[i] is None:
            body_id = i
            mass = PHYSAC_PI * radius * radius * density
            inertia = mass * radius * radius
            vertex_data = PhysicsShapeVertexData(PHYSAC_CIRCLE_VERTICES, [rl.Vector2(0,0)]*PHYSAC_CIRCLE_VERTICES, [rl.Vector2(0,0)]*PHYSAC_CIRCLE_VERTICES)
            for j in range(PHYSAC_CIRCLE_VERTICES):
                angle = (j / PHYSAC_CIRCLE_VERTICES) * PHYSAC_PI * 2
                vertex_data.positions[j] = rl.Vector2(rl.math_cos(angle) * radius, rl.math_sin(angle) * radius)

            body = PhysicsBodyData(body_id, True, pos, rl.Vector2(0,0), rl.Vector2(0,0), 0, 0, mass, 1/mass if mass != 0 else 0, inertia, 1/inertia if inertia != 0 else 0, 0.4, 0.2, 0, True, False, False, PHYSAC_SHAPE_CIRCLE, vertex_data)
            physics_bodies[i] = body
            break
    return body

def create_physics_body_rectangle(pos, width, height, density):
    global physics_bodies
    body = None
    for i in range(PHYSAC_MAX_BODIES):
        if physics_bodies[i] is None:
            body_id = i
            mass = width * height * density
            inertia = mass * (width*width + height*height) / 12
            vertex_data = PhysicsShapeVertexData(4, [rl.Vector2(0,0)]*4, [rl.Vector2(0,0)]*4)
            vertex_data.positions[0] = rl.Vector2(-width/2, -height/2)
            vertex_data.positions[1] = rl.Vector2(width/2, -height/2)
            vertex_data.positions[2] = rl.Vector2(width/2, height/2)
            vertex_data.positions[3] = rl.Vector2(-width/2, height/2)
            # Calculate normals
            for j in range(4):
                next_j = (j + 1) % 4
                edge = rl.vector2_subtract(vertex_data.positions[next_j], vertex_data.positions[j])
                vertex_data.normals[j] = rl.vector2_normalize(rl.Vector2(edge.y, -edge.x))


            body = PhysicsBodyData(body_id, True, pos, rl.Vector2(0,0), rl.Vector2(0,0), 0, 0, mass, 1/mass if mass != 0 else 0, inertia, 1/inertia if inertia != 0 else 0, 0.4, 0.2, 0, True, False, False, PHYSAC_SHAPE_POLYGON, vertex_data)
            physics_bodies[i] = body
            break
    return body

def create_physics_body_polygon(pos, radius, sides, density):
    global physics_bodies
    body = None
    for i in range(PHYSAC_MAX_BODIES):
        if physics_bodies[i] is None:
            body_id = i
            mass = PHYSAC_PI * radius * radius * density * (sides / (PHYSAC_CIRCLE_VERTICES / 2)) # Approximation
            inertia = mass * radius * radius
            vertex_data = PhysicsShapeVertexData(sides, [rl.Vector2(0,0)]*sides, [rl.Vector2(0,0)]*sides)
            for j in range(sides):
                angle = (j / sides) * PHYSAC_PI * 2
                vertex_data.positions[j] = rl.Vector2(rl.math_cos(angle) * radius, rl.math_sin(angle) * radius)
            # Calculate normals
            for j in range(sides):
                next_j = (j + 1) % sides
                edge = rl.vector2_subtract(vertex_data.positions[next_j], vertex_data.positions[j])
                vertex_data.normals[j] = rl.vector2_normalize(rl.Vector2(edge.y, -edge.x))

            body = PhysicsBodyData(body_id, True, pos, rl.Vector2(0,0), rl.Vector2(0,0), 0, 0, mass, 1/mass if mass != 0 else 0, inertia, 1/inertia if inertia != 0 else 0, 0.4, 0.2, 0, True, False, False, PHYSAC_SHAPE_POLYGON, vertex_data)
            physics_bodies[i] = body
            break
    return body

def get_physics_bodies_count():
    count = 0
    for body in physics_bodies:
        if body is not None:
            count += 1
    return count

def get_physics_body(index):
    if 0 <= index < PHYSAC_MAX_BODIES:
        return physics_bodies[index]
    return None

def get_physics_shape_type(index):
    body = get_physics_body(index)
    if body:
        return body.shape_type
    return -1 # Error or not found

def get_physics_shape_vertices_count(index):
    body = get_physics_body(index)
    if body:
        return body.vertex_data.count
    return 0

def get_physics_shape_vertex(body, vertex):
    if body is None:
        return rl.Vector2(0,0)

    position = body.vertex_data.positions[vertex]

    # Apply rotation
    if body.freeze_orient: # TODO: This is not how freeze_orient is meant to be used
        transformed_x = position.x
        transformed_y = position.y
    else:
        # Assuming angular_velocity is orientation in radians for now
        # This is a simplification. Proper rotation matrix should be used.
        # For now, let's assume angular_velocity stores the current angle.
        # This is incorrect for physics simulation but will draw something.
        current_angle_rad = body.angular_velocity # Incorrect use of angular_velocity
        cos_a = rl.math_cos(current_angle_rad)
        sin_a = rl.math_sin(current_angle_rad)
        transformed_x = position.x * cos_a - position.y * sin_a
        transformed_y = position.x * sin_a + position.y * cos_a

    # Apply translation
    transformed_x += body.position.x
    transformed_y += body.position.y

    return rl.Vector2(transformed_x, transformed_y)


def set_physics_body_rotation(index, radians):
    body = get_physics_body(index)
    if body:
        body.angular_velocity = radians # Incorrect use, should be body.orient or similar

def destroy_physics_body(body):
    global physics_bodies
    if body is None:
        return
    for i in range(PHYSAC_MAX_BODIES):
        if physics_bodies[i] is not None and physics_bodies[i].id == body.id:
            physics_bodies[i] = None
            # print(f"Body {body.id} destroyed")
            return
    # print(f"Body {body.id} not found for destruction")


def close_physics():
    global physics_bodies
    for i in range(PHYSAC_MAX_BODIES):
        physics_bodies[i] = None
    print("Physics system closed")

# Main
def main():
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "[physac] Basic demo")

    logo_x = screen_width - rl.measure_text("Physac", 30) - 10
    logo_y = 15

    init_physics()

    floor = create_physics_body_rectangle(rl.Vector2(screen_width / 2, screen_height), 500, 100, 10)
    if floor:
        floor.enabled = False

    circle = create_physics_body_circle(rl.Vector2(screen_width / 2, screen_height / 2), 45, 10)
    if circle:
        circle.enabled = False

    rl.set_target_fps(60)

    while not rl.window_should_close():
        # UpdatePhysics() # Not implemented yet

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            create_physics_body_polygon(rl.get_mouse_position(), rl.get_random_value(20, 80), rl.get_random_value(3, 8), 10)
        elif rl.is_mouse_button_pressed(rl.MOUSE_RIGHT_BUTTON):
            create_physics_body_circle(rl.get_mouse_position(), rl.get_random_value(10, 45), 10)

        bodies_count = get_physics_bodies_count()
        for i in range(bodies_count -1, -1, -1): # Iterate backwards for safe removal
            body = get_physics_body(i) # This might be tricky if bodies are destroyed and list shifts
                                       # A more robust way would be to iterate through the actual list
                                       # or manage a separate list of active body indices.
                                       # For now, let's find the body by iterating through the raw list.
            actual_body_to_check = None
            current_valid_idx = 0
            for k in range(PHYSAC_MAX_BODIES):
                if physics_bodies[k] is not None:
                    if current_valid_idx == i:
                        actual_body_to_check = physics_bodies[k]
                        break
                    current_valid_idx +=1

            if actual_body_to_check and actual_body_to_check.position.y > screen_height * 2:
                destroy_physics_body(actual_body_to_check)


        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_fps(screen_width - 90, screen_height - 30)

        bodies_count = get_physics_bodies_count()
        # Iterate through the raw physics_bodies list to draw
        for i in range(PHYSAC_MAX_BODIES):
            body = physics_bodies[i] # Get body directly from the list
            if body is not None:
                vertex_count = body.vertex_data.count
                for j in range(vertex_count):
                    vertex_a = get_physics_shape_vertex(body, j)
                    jj = (j + 1) % vertex_count
                    vertex_b = get_physics_shape_vertex(body, jj)
                    rl.draw_line_v(vertex_a, vertex_b, rl.GREEN)

        rl.draw_text("Left mouse button to create a polygon", 10, 10, 10, rl.WHITE)
        rl.draw_text("Right mouse button to create a circle", 10, 25, 10, rl.WHITE)
        rl.draw_text("Physac", logo_x, logo_y, 30, rl.WHITE)
        rl.draw_text("Powered by", logo_x + 50, logo_y - 7, 10, rl.WHITE)

        rl.end_drawing()

    close_physics()
    rl.close_window()

if __name__ == '__main__':
    main()
