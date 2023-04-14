import numpy as np
import matplotlib.pyplot as plt

import pygame


# попытка смоделировать магматическую камеру как клеточный автомат
# v0.2.1
# визуализация на pygame
# sorta works but quicky crashes :(((

neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,1), (1,0), (1,1))
L2, L1, L0 = 0, 1, 2
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

    
TIME_INTERVAL = 50
DEBUG_MODE = False
##bounds = [0,1,2,3,4]
##norm = colors.BoundaryNorm(bounds, cmap2.N)

def debug(output):
    if DEBUG_MODE:
        print(output)

def iterate(X):
    """Итерации магматической камеры"""

    X1 = np.zeros((ny, nx))
    for ix in range(nx):
        for iy in range(ny):
            if X[iy,ix] in (ROOF, BACKGROUND):
                X1[iy,ix] = X[iy,ix]

            elif X[iy,ix] == OL and X[iy+1,ix] not in (OL,ROOF):
                #debug('[OL]\tX \t-->\t [X]')
                X1[iy,ix] == X[iy+1,ix]
            elif X[iy,ix] not in [OL,ROOF] and X[iy-1,ix] == OL:
                #debug('OL\t[X] \t-->\t [OL]')
                X1[iy,ix] = OL
           
            elif X[iy,ix] == OL:
                #debug('[OL] \t-->\t [OL]')
                X1[iy,ix] = OL
            
            elif X[iy,ix] == L2 and np.random.random() < 0.005:
                X1[iy,ix] = OL
             
    return X1

def draw(X):
    for ix in range(nx-1):
        for iy in range(ny-1):
            pygame.draw.rect(screen, COLORS[int(X[iy,ix])], [ix*11, iy*11, ix*11+10, iy*11+10])
            
    pygame.display.update()
    


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

nx, ny = 30, 30
X = np.zeros((ny, nx))
X[0] = [ROOF]*nx
X[ny-1] = [BACKGROUND]*nx
X[ny-2] = [ROOF]*nx
X[20,5] = OL

draw(X)

running = True
while running:
    pygame.event.get()
    draw(X)
    X = iterate(X)
##    for i in pygame.event.get():
##        if i.type == QUIT:
##            quit()

pygame.quit()
