import pygame
import pymunk
import pygame.display
import pymunk.pygame_util

pygame.init()
window = pygame.display.set_mode((1200, 600))


def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()


def create_object(space, mass, radius):
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = (600, 100)
    body.velocity = (150, 100)

    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    shape.elasticity = 1

    space.add(body, shape)
    return shape


def create_bounaries(space, width, height):
    rects = [
        [(width/2, height-10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width-10, height/2), (20, height)]

    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        space.add(body, shape)
        shape.elasticity = 1


def run(window):
    space = pymunk.Space(window)
    space.gravity = (0, 981)
    draw_options = pymunk.pygame_util.DrawOptions(window)
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    i = 0
    while i < 10:
        create_object(space, 0.01, 20)
        i += 1

    create_bounaries(space, 1200, 600)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(space, window, draw_options)
        clock.tick(fps)
        space.step(dt)
    pygame.quit()


def main():
    run(window)


main()
