import numpy as np
import matplotlib.pyplot as plt

import pygame


# попытка смоделировать магматическую камеру как клеточный автомат
# визуализация на pygame
# работает!

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

SCREEN_WIDTH = 250
SCREEN_HEIGHT = 250
CELL_SIZE = 10
BOTTOM_OFFSET = 0
    
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
    for ix in range(nx):
        for iy in range(ny):
            pygame.draw.rect(screen, COLORS[int(X[iy,ix])], [ix*CELL_SIZE,
                                                             iy*CELL_SIZE,
                                                             (ix+1)*CELL_SIZE,
                                                             (iy+1)*CELL_SIZE])
            
    pygame.display.update()
    


pygame.init()


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


nx, ny = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE - BOTTOM_OFFSET
X = np.zeros((ny, nx))
X[0] = [ROOF]*nx
X[ny-1] = [BACKGROUND]*nx
X[ny-2] = [ROOF]*nx
#X[20,5] = OL

draw(X)

iteration = 0
running = True
while running:
    #name = "s" + str(iteration) +".jpg"
    #pygame.image.save(screen, name)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw(X)
    X = iterate(X)
    iteration+=1

pygame.quit()
