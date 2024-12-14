import pygame
import pymunk
import pygame.display
import pymunk.pygame_util
import math

pygame.init()
window = pygame.display.set_mode((1200,600))

def draw(space,window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()
    
def create_boundaries(space,width, height):
    rects = [
        [(width/2, height -10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width-10, height/2), (20, height)],
        [(90,255),(20,510)],
        [(182.5,510),(205,20)],
        [(275,255),(20,510)],
        [(467.5-20,90),(205,20)],
        [(275+100-20,255+90),(20,510)],
        [(275+285-20,255+90),(20,510)],
        [(275+285+100-40,255),(20,510)],
        [(275+285+100+185-40,255),(20,510)],
        [(275+285+100+185+100-50-3,255+90),(20,510)],
        [(275+285+100+185+100+165,255+90),(20,515)],
        [(467.5+285-40,510),(205,20)],
        [(467.5+285+285-40+3.9,90),(205+30+3,20)],
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape. elasticity = 1
        shape.color = pygame.Color("blue")
        space.add(body,shape)

def create_charged_ball(space, position, radius, mass, charge):
    body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
    body.position = position
    body.velocity = (0, 0)
    shape = pymunk.Circle(body, radius)
    shape.charge = charge
    shape.mass = mass
    shape.color = pygame.Color("red")
    space.add(body, shape)
    shape.elasticity = 1
    return shape


def apply_coulomb_force(shape1, shape2):
    k = 9e9
    dx = shape2.body.position.x - shape1.body.position.x
    dy = shape2.body.position.y - shape1.body.position.y
    distance = math.sqrt(dx**2 + dy**2)
    force_magnitude = k * shape1.charge * shape2.charge/ distance**2
    force = pymunk.Vec2d(dx, dy).normalized() * force_magnitude
    shape1.body.apply_force_at_world_point(-force, shape1.body.position)
    shape2.body.apply_force_at_world_point(force, shape2.body.position)  
         
def create_object(space, mass, radius):
    body = pymunk.Body(body_type= pymunk.Body.DYNAMIC)
    body.position = (600,100)
    body.velocity = (10,10)
    
    shape = pymunk.Circle(body, radius)
    shape.mass = mass 
    shape.color = pygame.Color("red")
    shape.elasticity = 1
    space.add(body,shape)

def run(window):
    space = pymunk.Space(window)
    space.gravity = (0 , 981)
    ball1 = create_charged_ball(space, (15,15), 25, 200,2)
    ball2 = create_charged_ball(space, (15+275,15), 25, 200,2)
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(window)

    fps = 60
    dt = 1 / fps
    create_boundaries(space, 1200,600)
    #create_object(space, 50,40)
    
    #i = 0
    #while i < 100:
        #create_object(space,20,10)
        #i += 1
        
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        apply_coulomb_force(ball1, ball2)
        draw(space,window, draw_options)
        space.step(dt)
        clock.tick(fps)
    pygame.quit()

def main():
    run(window)
main()