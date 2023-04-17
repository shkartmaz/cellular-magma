import numpy as np
import pandas as pd
import matplotlib as mlt
import pygame

from dataclasses import dataclass

# cell phase color constants
L = 0
OL, ROOF = 3, 4
BACKGROUND = 5

CRYST_PROBABILITY = 0.005
TEMPERATURE_TRANSFER = 0.01
MAX_ITERATION = 100

# visuals setup
SCREEN_WIDTH = 250
SCREEN_HEIGHT = 250
CELL_SIZE = 10

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
            g = abs(int(t*0.0686 - 25.3))
            b = abs(int(0.00002*t**2 - 0.024*t + 8.37))
            return (255, g, b)
        elif self.phase == OL:
            return (50,200,50)
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
                X1[iy,ix].temperature = 0

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
##            elif X[iy,ix].phase == L and np.random.random() < CRYST_PROBABILITY:
##                X1[iy,ix] = Cell(phase = OL)

            # basic cooling
##            else:
##                delta_t = X[iy-1,ix].temperature - X[iy,ix].temperature
##                X1[iy,ix].temperature = X[iy,ix].temperature + delta_t /2
##                X1[iy-1,ix].temperature = X[iy-1,ix].temperature - delta_t /2

    for ix in range(nx):
        for iy in range(ny-1):
            if X[iy,ix].phase == ROOF:
                X[iy,ix].temperature = 0
            else:
                t = X[iy,ix].temperature
                t_up = X[iy-1,ix].temperature
                t_down = X[iy+1,ix].temperature
              
                X1[iy,ix].temperature = t - (2*t - t_up - t_down) * TEMPERATURE_TRANSFER
                
            
    a = [int(X1[i,0].temperature) for i in [0,1,2,3,4]]
    print(a)

    if MODE_DEBUG:
        print(f'{L_counter} liquid cells left')

    if L_counter == 0:
        pygame.quit()
    return X1

def draw(X):
    """Draw a rectangle of corresponding for each cell"""
    for ix in range(nx):
        for iy in range(ny):
            pygame.draw.rect(screen, X[iy,ix].color(),
                             [ix*CELL_SIZE,iy*CELL_SIZE,
                              CELL_SIZE,CELL_SIZE]
                             )
    pygame.display.update()
    
# initialize the chamber data structure
nx, ny = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE
##X = np.zeros((ny, nx))
##X[0] = [ROOF]*nx
##X[ny-1] = [BACKGROUND]*nx
##X[ny-2] = [ROOF]*nx

X = np.array([[Cell()]*nx]*ny)
X[0] = [Cell(ROOF,0)]*nx
X[ny-1] = [Cell(BACKGROUND,0)]*nx
X[ny-2] = [Cell(ROOF, 0)]*nx
##X[5,5] = Cell(phase = OL)
##X[10,10] = Cell(X[5,5].phase)


a = [int(X[i,0].temperature) for i in [0,1,2,3,4]]
print(a)

# initialize pygame
pygame.init()
icon = pygame.image.load('resource/icon.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])




# main cycle
iteration = 0  # only used for screenshots as of now
statistics = []
running = True
while running and X[1,0].temperature > 1 and iteration < MAX_ITERATION:
    pygame.display.set_caption(f'Step {iteration}')
    draw(X)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    X = iterate(X)
    add_stat = [int(X[i,2].temperature) for i in [0,1,2,3,4]]
    statistics.append(add_stat)
        
    iteration += 1

df = pd.DataFrame(statistics)
df.to_excel("temps.xlsx")
pygame.quit()
