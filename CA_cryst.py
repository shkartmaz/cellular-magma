import numpy as np
import pygame

from dataclasses import dataclass

# cell phase color constants
L = 0
OL, ROOF = 3, 4
BACKGROUND = 5

CRYST_PROBABILITY = 0.005

# visuals setup
SCREEN_WIDTH = 250
SCREEN_HEIGHT = 250
CELL_SIZE = 10
BOTTOM_OFFSET = 0

MODE_DEBUG = False
    

@dataclass
class Cell:
    phase:  int = L
    temperature:    float = 2000
##    MgO:    float = 10
##    FeO:    float = 10
##    CaO:    float = 10
##    SiO2:   float = 10
##    Al2O3:  float = 10
    def show(self):
        print(f'Phase {self.phase}, temperature {self.temperature}')
        
    def color(self):
        if self.phase == L:
            # color scale pre-generated with Color_Match module by carpdiem
            # works in range 500..2000 Celsius
            t = self.temperature
            g = int(t*0.0686 - 25.3)
            b = int(0.00002*t**2 - 0.024*t + 8.37)
            return (255, g, b)
        elif self.phase == OL:
            return (0,200,0)
        elif self.phase == ROOF:
            return (50,50,50)
        elif self.phase == BACKGROUND:
            return (0,0,0)
        else:
            return (0,0,200)
            

def iterate(X):
    """Perform a step from X state according to the rules and return new state X1"""

    X1 = np.array([[Cell()]*nx]*ny)
    L_counter = 0
    for ix in range(nx):
        for iy in range(ny):
            if X[iy,ix].phase == L:
                L_counter += 1
            # these cells stay the same
            if X[iy,ix].phase in (ROOF, BACKGROUND):
                X1[iy,ix] = X[iy,ix]

            # OL sinks down one cell
            # Done in two steps
            elif X[iy,ix].phase == OL and X[iy+1,ix].phase not in (OL,ROOF):
                X1[iy,ix], X1[iy+1,ix] = X[iy+1,ix], X[iy,ix]
            elif X[iy,ix].phase == OL and X[iy+1,ix].phase not in (OL,ROOF):
                X1[iy,ix].phase == X[iy+1,ix].phase   
            elif X[iy,ix].phase not in [OL,ROOF] and X[iy-1,ix].phase == OL:
                X1[iy,ix].phase = OL
            
            # If OL has nowhere to sink, it stays in place
            elif X[iy,ix].phase == OL:
                X1[iy,ix] = X[iy,ix]
            
            # every Liquid cell crystallizes with a set chance
            elif X[iy,ix].phase == L and np.random.random() < CRYST_PROBABILITY:
                X1[iy,ix] = Cell(phase = OL)

            # basic cooling
            else:
                X1[iy,ix].temperature = X[iy,ix].temperature - 2
    #print(X1[2,2].temperature)

    if MODE_DEBUG:
        print(f'{L_counter} liquid cells left')

    if L_counter == 0:
        pygame.quit()
    return X1

def draw(X):
    """Draw a rectangle of correcponding for each cell"""
    for ix in range(nx):
        for iy in range(ny):
            pygame.draw.rect(screen, X[iy,ix].color(),
                             [ix*CELL_SIZE,iy*CELL_SIZE,
                              (ix+1)*CELL_SIZE,(iy+1)*CELL_SIZE]
                             )
    pygame.display.update()
    
# initialize the chamber data structure
nx, ny = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE - BOTTOM_OFFSET
##X = np.zeros((ny, nx))
##X[0] = [ROOF]*nx
##X[ny-1] = [BACKGROUND]*nx
##X[ny-2] = [ROOF]*nx

X = np.array([[Cell()]*nx]*ny)
X[0] = [Cell(ROOF)]*nx
X[ny-1] = [Cell(BACKGROUND)]*nx
X[ny-2] = [Cell(ROOF)]*nx
X[5,5] = Cell(phase = OL)
X[10,10] = Cell(X[5,5].phase)

if MODE_DEBUG:
    print(X[5,5].color())
    print(X[3,3].color())
    input()


# initialize pygame
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# main cycle
iteration = 0  # only used for screenshots as of now
running = True
while running:
    # print('step ',iteration)
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
