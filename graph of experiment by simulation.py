import pymunk
import pygame
import pygame.display
import pymunk.pygame_util
import math 
import matplotlib.pyplot as plt

pygame.init()
window = pygame.display.set_mode((1200,600))
font = pygame.font.SysFont(None, 24)


def draw(window, space, draw_options,balls):
    window.fill("white")
    space.debug_draw(draw_options)
    for index, ball in enumerate(balls):
        velocity = ball.body.velocity
        x = velocity.x
        y = velocity.y
        vel = math.sqrt(x**2+y**2)
        velocity_text = f"Velocity Ball{index + 1}: {vel:.2f}"
        surface_text = font.render(velocity_text, True, (255,0,0))
        text_position = (600,100 + index * 30)
        window.blit(surface_text, text_position)
        
    pygame.display.update()
    
def create_charged_ball(space, position, mass, radius, charge):
    body = pymunk.Body()
    body.position = position
    body.velocity = (0, 0)
    
    shape = pymunk.Circle(body, radius)
    shape.color = pygame.Color("red")
    shape.mass = mass 
    shape.charge = charge
    shape.elasticity = 1
    space.add(body,shape)
    return shape
    
def create_boundaries(space):
    rects = [
        [(600, 590), (1200, 20)],
        [(600, 10), (1200, 20)],
        [(10, 300), (20, 600)],
        [(1190, 300), (20, 600)],
        [(90, 300), (20, 600)],
        [(1110, 300), (20, 600)],
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        
        shape = pymunk.Poly.create_box(body, size)
        shape. elasticity = 1
        shape.color = pygame.Color("blue")
        space.add(body, shape)

def apply_coulomb_force(shape1, shape2):
    k = 9e9
    dx = shape2.body.position.x - shape1.body.position.x
    dy = shape2.body.position.y - shape1.body.position.y
    distance = math.sqrt(dx**2 + dy**2)
    force_magnitude = k * shape1.charge * shape2.charge / distance**2 
    force = pymunk.Vec2d(dx, dy).normalized() * force_magnitude 
    
    shape1.body.apply_force_at_world_point(-force, shape1.body.position)
    shape2.body.apply_force_at_world_point(force, shape2.body.position)  

def run(window):
    space = pymunk.Space()
    space.gravity = (0, 98.1)
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(window)
    fps = 60
    dt = 1/ fps
    
    create_boundaries(space)
    ball1 = create_charged_ball(space, (50,140), 1000, 30, 30)
    ball2 = create_charged_ball(space, (1150,120), 1000, 30, 30)
    
    balls = [ball1, ball2]
    velocity_ball1 = []
    velocity_ball2 = []
    time_steps = []
    
    run = True
    t = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        apply_coulomb_force(ball1, ball2)
        draw(window, space, draw_options, balls)
        space.step(dt)
        clock.tick(fps)
        velocity_ball1.append(ball1.body.velocity.length)
        velocity_ball2.append(ball2.body.velocity.length)
        time_steps.append(t)
        t += dt
                
    pygame.quit()
    plt.close("all")
    plt.figure(figsize = (10,5))
    plt.plot(time_steps, velocity_ball1, label = "Ball 1 velocity", color = "blue")
    plt.plot(time_steps, velocity_ball2, label = "Ball 2 velocity", color = "red")
    plt.xlabel("Time(s)")
    plt.ylabel("Velocity(m/s)")
    plt.title("Velocity vs Time")
    plt.legend()
    plt.tight_layout()
    plt.show()
    
def main():
    run(window)
main()