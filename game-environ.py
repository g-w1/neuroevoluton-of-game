"""
An attempt at some simple, self-contained pygame-based examples.
Example 02
In short:
One static body:
    + One fixture: big polygon to represent the ground
Two dynamic bodies:
    + One fixture: a polygon
    + One fixture: a circle
And some drawing code that extends the shape classes.
kne
"""
import random
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)

def keymovefunc(args):
    movement = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement -= 1
            if event.key == pygame.K_RIGHT:
                movement += 1
    return movement
def test(func,godisp):
    startrun = 0
    from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)
    if godisp:
        PPM = 20.0  # pixels per meter
        TARGET_FPS = 60
        TIME_STEP = 1.0 / TARGET_FPS
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

    # --- pygame setup ---
    if godisp:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption('Simple pygame example')
        clock = pygame.time.Clock()

    # --- pybox2d world setup ---
    # Create the world
    world = world(gravity=(0, -20), doSleep=True)

    # And a static body to hold the ground shape
    ground_body = world.CreateStaticBody(
        position=(0, 0),
        shapes=polygonShape(box=(50, 1)),
    )
    top = world.CreateStaticBody(
        position=(0,24),
        shapes = polygonShape(box=(50,1))
    )
    side_body = world.CreateStaticBody(
        position = (0,0),
        shapes = polygonShape(box=(1,50)),
    )
    other_side = world.CreateStaticBody(
        position=(32,0),
        shapes = polygonShape(box=(1,50)),
    )

    # Create a couple dynamic bodies
    body = world.CreateDynamicBody(position=(random.randint(10,30), random.randint(10,20)))
    ball = body.CreateCircleFixture(radius=0.5, density=.2, friction=0,restitution=1)

    body = world.CreateDynamicBody(position=(15, 0), angle=0)
    box = body.CreatePolygonFixture(box=(3, .4), density=1, friction=0.3)

    colors = {
        staticBody: (255, 255, 255, 255),
        dynamicBody: (127, 127, 127, 255),
    }

    # Let's play with extending the shape classes to draw for us.

    if godisp:
        def my_draw_polygon(polygon, body, fixture):
            vertices = [(body.transform * v) * PPM for v in polygon.vertices]
            vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(screen, colors[body.type], vertices)
        polygonShape.draw = my_draw_polygon

    if godisp:
        def my_draw_circle(circle, body, fixture):
            position = body.transform * circle.pos * PPM
            position = (position[0], SCREEN_HEIGHT - position[1])
            pygame.draw.circle(screen, colors[body.type], [int(
                x) for x in position], int(circle.radius * PPM))
            # Note: Python 3.x will enforce that pygame get the integers it requests,
            #       and it will not convert from float.
        circleShape.draw = my_draw_circle

    # --- main game loop ---
    world.bodies[4].linearVelocity = (random.randint(-10,10),random.randint(-5,5))
    running = True
    while running:
        startrun+=1
        movement = 0
        # Check the event queue
        if godisp:    
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        movement -= 1
                    if event.key == pygame.K_RIGHT:
                        movement += 1
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    
                    running = False
        if not godisp:
            movement = func([world.bodies[5].position[0],world.bodies[4].linearVelocity,world.bodies[4].position])
        pos = world.bodies[5].position
        world.bodies[5].position = (pos[0]+movement,pos[1])
        if godisp:
            screen.fill((0, 0, 0, 0))
        if world.bodies[4].position[1] <= 1.8:
            running  = False 
        if godisp:
        # Draw the world
            for body in world.bodies:
                for fixture in body.fixtures:
                    fixture.shape.draw(body, fixture)
        # Make Box2D simulate the physics of our world for one step.
            world.Step(TIME_STEP, 10, 10)

        # Flip the screen and try to keep at the target FPS
            pygame.display.flip()
            clock.tick(TARGET_FPS)
    if godisp:
        pygame.quit()
    print(startrun)
    return startrun
test(keymovefunc,True)