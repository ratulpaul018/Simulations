import pygame
import pymunk
import pygame.display
import pymunk.pygame_util
import math

pygame.init()
window = pygame.display.set_mode((1200,600))
font = pygame.font.SysFont(None, 24)

def draw(space, window, draw_options, balls):
    window.fill("white") 
    space.debug_draw(draw_options)
    for index, ball in enumerate(balls):
        velocity = ball.body.velocity
        vx = velocity.x
        vy = velocity.y
        vel = math.sqrt(vx**2 + vy**2)
        velocity_text = f"Ball{index + 1} Velocity: {vel:.2f}"
        velocity_text_surface = font.render(velocity_text, True, (0,0,0))
        velocity_text_position = (400, 200+index*30)
        window.blit(velocity_text_surface, velocity_text_position)
        
        ball_name_text = f"Ball{index + 1}"
        ball_name_text_surface = font.render(ball_name_text, True, (0,0,0))
        ball_name_text_position = ball.body.position
        window.blit(ball_name_text_surface, ball_name_text_position)
    pygame.display.update()

def create_boundary(space, start, end, thickness):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, start, end, thickness)
    shape.color = pygame.Color("blue")
    shape.elasticity = 1
    space.add(body, shape)

def create_charged_particle(space, position, radius, mass, charge, color):
    body = pymunk.Body()
    body.position = position
    body.velocity = (0, 0)
    shape = pymunk.Circle(body, radius)
    shape.color = pygame.Color(f"{color}")
    shape.mass = mass
    shape.elasticity = 0
    shape.charge = charge
    space.add(body, shape)
    return shape

def apply_coulomb_force(shape1, shape2):
    k = 9e9
    dx = shape2.body.position.x - shape1.body.position.x
    dy = shape2.body.position.y - shape1.body.position.y
    
    distance = math.sqrt(dx**2 + dy**2)
    force_magnitude = k * shape1.charge * shape2.charge / distance**2
    force = pymunk.Vec2d(dx, dy).normalized() * force_magnitude
    
    shape1.body.apply_force_at_world_point(-force, shape1.body.position)
    shape2.body.apply_force_at_world_point(-force, shape2.body.position)

def run(window):
    space = pymunk.Space()
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(window)
    space.gravity = (0, 0)
    fps = 60
    dt = 1/fps
    
    create_boundary(space, (10,10), (1190,10), 20)
    create_boundary(space, (10,10), (10,590), 20)
    create_boundary(space, (1190,10), (1190,590), 20)
    create_boundary(space, (10,590), (1190,590), 20)
    create_boundary(space, (590,10), (590,420), 20)
    create_boundary(space, (370,590), (370,180), 20)
    create_boundary(space, (1200-390,590), (1200-390, 180), 20)
    
    ball1 = create_charged_particle(space, (400, 50), 30, 10, 0.2, "green")
    ball2 = create_charged_particle(space, (500, 150), 30, 10, 0.2, "maroon")
    ball3 = create_charged_particle(space, (500, 150), 30, 10, 0.2, "maroon")
    balls = [ball1, ball2, ball3]
    
    run = True
    while run:
        for event  in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        apply_coulomb_force(ball1, ball2)
        draw(space, window, draw_options, balls)
        space.step(dt)
        clock.tick(fps)
         
    pygame.quit()
    
def main():
    run(window)
main()
