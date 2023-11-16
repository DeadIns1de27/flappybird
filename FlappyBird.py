import random as rand
import pygame as py
from pygame.locals import *
import sys

# hello
thrust = -30
gravity = 5
terminal = 10
window_width = 900
window_height = 499

window = py.display.set_mode((window_width,window_height))
game_images = { }
framespersecond = 30    

py.init()
framespersecond_clock = py.time.Clock()
py.display.set_caption('Flappy Bird')
bird_image = py.image.load('bird.png').convert_alpha()
game_images['background'] = py.image.load('background.png').convert_alpha()
pipe_image = py.transform.scale(py.image.load('pipe.png').convert_alpha(), (60, 400))
game_images['upper'] = py.transform.rotate(pipe_image,180)
game_images['lower'] = pipe_image
game_images['bird_up'] = py.transform.rotate(bird_image, -20)
game_images['bird_down'] = py.transform.rotate(bird_image, 20)

birdx = 100
birdv = 5
birdy = 200

pipes = []
frames = 50 

start = False

def collision(x1, y1, x2, y2, w1, h1, w2, h2):
    return (x1 + w1 > x2) and (x1 < x2 + w2) and (y1 + h1 > y2) and (y1 < y2 + h2)

def draw():
    global birdx, birdy, pipes

    window.blit(game_images['background'], (0, 0))  

    for x in range(0, len(pipes)): 
        pipex, pipey, pipe_type = pipes[x]
        if pipe_type == "upper": 
            window.blit(game_images['upper'], (pipex, pipey))
        if pipe_type == "lower": 
            window.blit(game_images['lower'], (pipex, pipey))

    if birdv > 0:
        window.blit(game_images['bird_up'], (birdx, birdy))
    else:
        window.blit(game_images['bird_down'], (birdx, birdy))

def handle_events():
    global start, birdv

    for event in py.event.get(): 
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) :
            py.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE :
            start = True
            birdv = thrust

def menu():
    handle_events()
    draw()

def update():
    global birdx, birdy, birdv, pipes, frames

    for x in range(0, len(pipes)):
        # Collision
        pipex, pipey, _ = pipes[x]
        if collision(pipex, pipey, birdx, birdy, 60, 400, 40, 27):   
            print("Game Over")
            py.quit()  
            sys.exit() 

    handle_events()

    if birdy > 500 : 
        print("Game Over")
        py.quit()  
        sys.exit()

    if frames == 50: 
        # add pipe
        cord_random = rand.randint(-350, -100)
        pipes.append((900, cord_random + 550, "upper"))
        pipes.append((900, cord_random, "lower"))
        frames = 0
    frames += 1

    draw()

    for x in range(0, len(pipes)): 
        if x < len(pipes):
            pipex, pipey , pipe_type = pipes[x]
            pipes[x] = (pipex - 5, pipey, pipe_type)

            if pipex < 0:
                pipes.pop(0)
                pipes.pop(0)

    birdv += gravity
    birdy += birdv
    if birdv > terminal:
        birdv = terminal

while True:
    if not start:
        menu()
    else:
        update()
 
    py.display.update()

    framespersecond_clock.tick(framespersecond)
    