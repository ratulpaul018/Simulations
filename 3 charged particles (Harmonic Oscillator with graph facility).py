import pygame
import pymunk
import pygame.display
import pymunk.pygame_util
import math
import matplotlib.pyplot as plt 

pygame.init()
window = pygame.display.set_mode((1200,600))
font = pygame.font.SysFont(None, 24)

def draw(space,window,draw_options,balls):
    window.fill("white")
    space.debug_draw(draw_options)
    for index,ball in enumerate(balls):
        velocity = ball.body.velocity
        x = velocity.x
        y = velocity.y
        vel = math.sqrt(x**2 + y**2)
        velocity_text = f"Velocity Body{index+1}: {vel:.2f}"
        name_text = f"Ball {index + 1}"
        position = ball.body.position
        surface_text_name = font.render(name_text, True, (0,0,0))
        surface_text = font.render(velocity_text, True, (255,0,0))
        text_position = (500,50+index*30)
        window.blit(surface_text,text_position)
        window.blit(surface_text_name,position)
        
    pygame.display.update()
    
def create_charged_ball(space,position,mass,radius,charge):
    body = pymunk.Body()
    body.position = position
    body.velocity = (0,0)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.charge = charge
    shape.color =pygame.Color("red")
    shape.elasticity = 1
    space.add(body,shape)
    return shape

def create_boundaries(space):
    rects = [
        [(600,590), (1200,20)],
        [(600,10), (1200,20)],
        [(10,300), (20,600)],
        [(1190,300), (20,600)],
        [(90,300), (20,600)],
        [(1110,300), (20,600)],
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position =pos
        shape = pymunk.Poly.create_box(body, size)
        shape.color = pygame.Color("blue")
        shape.elasticity = 0.6
        space.add(body,shape)

def apply_coulomb_force(shape1, shape2, shape3):
    k = 9e9
    dx = shape2.body.position.x - shape1.body.position.x
    dy = shape2.body.position.y - shape1.body.position.y
    
    dz = shape3.body.position.y - shape2.body.position.y
    dp = shape3.body.position.x - shape2.body.position.x
    
    dq = shape3.body.position.y - shape1.body.position.y
    dr = shape3.body.position.x - shape1.body.position.x
    
    distance_1 = math.sqrt(dx**2 + dy**2)
    distance_2 = math.sqrt(dz**2 + dp**2)
    distance_3 = math.sqrt(dq**2 + dr**2)
    
    force_magnitude_3 = k * shape1.charge * shape3.charge / distance_3 **2
    force_3 = pymunk.Vec2d(dq, dr).normalized()* force_magnitude_3
    
    force_magnitude_2 = k * shape2.charge * shape3.charge / distance_2 **2
    force_2 = pymunk.Vec2d(dz, dp).normalized()* force_magnitude_2
    
    force_magnitude_1 = k * shape1.charge * shape2.charge / distance_1 **2
    force_1 = pymunk.Vec2d(dx, dy).normalized() * force_magnitude_1
    
    shape1.body.apply_force_at_world_point(force_1, shape1.body.position)
    shape2.body.apply_force_at_world_point(-force_1, shape2.body.position)
    
    shape2.body.apply_force_at_world_point(force_2, shape2.body.position)
    shape3.body.apply_force_at_world_point(-force_2, shape3.body.position)    
    
    shape3.body.apply_force_at_world_point(force_3, shape3.body.position)    
    shape1.body.apply_force_at_world_point(-force_3, shape1.body.position)
    
def run(window):
    space = pymunk.Space()
    space.gravity = (0, 981)
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(window)
    fps = 60
    dt = 1/fps
    
    create_boundaries(space)
    ball1 = create_charged_ball(space,(50,570),140,30,3)
    ball2 = create_charged_ball(space,(1150,30),140,30,3)
    ball3 = create_charged_ball(space,(400,300),140,30,3)
    
    balls = [ball1,ball2,ball3]
    velocity_ball1 = []
    velocity_ball2 = []
    velocity_ball3 = []
    time_steps = []
        
    run = True
    t = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        apply_coulomb_force(ball1, ball2, ball3)
        draw(space,window,draw_options,balls)
        space.step(dt)
        clock.tick(fps)
        velocity_ball1.append(ball1.body.velocity.length)
        velocity_ball2.append(ball2.body.velocity.length)
        velocity_ball3.append(ball3.body.velocity.length)
        time_steps.append(t)
        t += dt
        
    pygame.quit()
    
    plt.close("all")
    plt.figure(figsize = (10,5))
    plt.plot(time_steps, velocity_ball1, label= "Ball 1", color = "red")
    plt.plot(time_steps, velocity_ball2, label= "Ball 2", color = "blue")
    plt.plot(time_steps, velocity_ball3, label= "Ball 3", color = "green")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity vs Time")
    plt.tight_layout()
    plt.legend()
    plt.show()
    
def main():
    run(window)
main()