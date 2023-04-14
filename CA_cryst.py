import numpy as np
import pygame

# cell phase color constants
L = 0
OL, ROOF = 3, 4
BACKGROUND = 5
COLORS = [
    (255,255,50),
    (0,0,200),
    (0,0,200),
    (0,200,0),
    (50,50,50),
    (0,0,0)
    ]
CRYST_PROBABILITY = 0.005

# visuals setup
SCREEN_WIDTH = 250
SCREEN_HEIGHT = 250
CELL_SIZE = 10
BOTTOM_OFFSET = 0

def iterate(X):
    """Perform a step from X state according to the rules and return new state X1"""

    X1 = np.zeros((ny, nx))
    for ix in range(nx):
        for iy in range(ny):
            # these cells stay the same
            if X[iy,ix] in (ROOF, BACKGROUND):
                X1[iy,ix] = X[iy,ix]

            # OL sinks down one cell
            # Done in two steps
            elif X[iy,ix] == OL and X[iy+1,ix] not in (OL,ROOF):
                X1[iy,ix] == X[iy+1,ix]   
            elif X[iy,ix] not in [OL,ROOF] and X[iy-1,ix] == OL:
                X1[iy,ix] = OL
            
            # If OL has nowhere to sink, it stays in place
            elif X[iy,ix] == OL:
                X1[iy,ix] = OL
            
            # every Liquid cell crystallizes with a set chance
            elif X[iy,ix] == L and np.random.random() < CRYST_PROBABILITY:
                X1[iy,ix] = OL         
    return X1

def draw(X):
    """Draw a rectangle of correcponding for each cell"""
    for ix in range(nx):
        for iy in range(ny):
            pygame.draw.rect(screen, COLORS[int(X[iy,ix])], [ix*CELL_SIZE,
                                                             iy*CELL_SIZE,
                                                             (ix+1)*CELL_SIZE,
                                                             (iy+1)*CELL_SIZE])
    pygame.display.update()
    
# initialize the chamber data structure
nx, ny = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE - BOTTOM_OFFSET
X = np.zeros((ny, nx))
X[0] = [ROOF]*nx
X[ny-1] = [BACKGROUND]*nx
X[ny-2] = [ROOF]*nx

# initialize pygame
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# main cycle
iteration = 0  # only used for screenshots as of now
running = True
while running:
    # making screenshots
    #name = "s" + str(iteration) +".jpg"
    #pygame.image.save(screen, name)
    draw(X)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    X = iterate(X)
    iteration += 1

pygame.quit()
