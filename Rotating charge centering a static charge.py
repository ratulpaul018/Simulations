import pygame
import pymunk
import pygame.display
import pymunk.pygame_util
import math

pygame.init()
window = pygame.display.set_mode((1200,600))

def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()
    
def create_boundaries(space):
    rects = [
        [(600,590),(1200, 20)],
        [(600,10),(1200, 20)],
        [(10, 300), (20, 600)],
        [(1190, 300), (20, 600)],
    ]
    for pos,size in rects:
        body = pymunk.Body(body_type= pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.color = pygame.Color("blue")
        shape.elasticity = 1
        space.add(body,shape)   
        
def central_object(space, position, radius, mass, charge, color):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.color = color
    shape.charge = charge
    shape.mass = mass
    shape.elasticity = 1
    space.add(body, shape)
    return shape

def rotating_object(space, position, radius, mass, charge, color):
    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.color = color
    shape.mass = mass
    shape.charge = charge
    shape.elasticity = 1
    space.add(body,shape)
    return shape

def apply_coulomb_force(shape1, shape2,orbit_radius, mass):
    k = 9e9
    dx = shape2.body.position.x - shape1.body.position.x
    dy = shape2.body.position.y - shape1.body.position.y
    distance = math.sqrt(dx**2 + dy**2)
    force_magnitude = k * shape1.charge * shape2.charge/ distance**2
    force = pymunk.Vec2d(dx, dy).normalized() * force_magnitude
    shape1.body.apply_force_at_world_point(-force, shape1.body.position)
    shape2.body.apply_force_at_world_point(force, shape2.body.position)  

    v = math.sqrt(abs(force_magnitude)*orbit_radius/mass)
    angle = math.atan2(dy, dx)
    vx = -v * math.sin(angle)
    vy = v * math.cos(angle)
    rotating_object_velocity = (vx, vy)
    return rotating_object_velocity 
    
def calculate_orbit_velocity(charge1, charge2, mass, orbit_radius):
    k = 9e9
    force = k*abs(charge1*charge2)/orbit_radius**2
    velocity = math.sqrt(force*orbit_radius/mass)
    return velocity

def run(window):
    space = pymunk.Space()
    space.gravity = (0, 0)
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(window)
    fps = 60
    dt = 1/fps
    orbit_radius = 100
    create_boundaries(space)
    ball1 = central_object(space, (600, 300),30, 1, 2e-2, pygame.Color("red"))
    #initial_velocity = calculate_orbit_velocity(1e-2, -1e-2, 1, orbit_radius)
    ball2 = rotating_object(space, (600, 300 - orbit_radius), 15, 1, -2e-2, pygame.Color("black"))
    ball2.body.velocity = apply_coulomb_force(ball1,ball2,orbit_radius,1)
    ball2.body.velocity*orbit_radius == 6.63e-34/(2*3.1416)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(space, window, draw_options)
        apply_coulomb_force(ball1, ball2, 1, orbit_radius)
        space.step(dt)
        clock.tick(fps)
    pygame.quit()

def main():
    run(window)
main()
