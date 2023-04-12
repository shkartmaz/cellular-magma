import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
from dataclasses import dataclass


#   попытка смоделировать магматическую камеру как клеточный автомат
#   v0.3
#   трех (пяти, семи итд) значений температуры явно мало
#   поэтому придется добавлять температуру как отдельное свойство
#   а может быть, и состав

## Template: {type, temperature, MgO, FeO2, SiO2, CaO, Al2O3}

LIQUID = 0
ROOF, BACKGROUND = 1, 2
OL, PL, OPX, CPX = 3, 4, 5, 6
TIME_INTERVAL = 50
DEBUG_MODE = False

@dataclass
class cell:
    phase:  int = LIQUID
    temperature:    float = 1500
    MgO:    float = 10
    FeO:    float = 10
    CaO:    float = 10
    SiO2:   float = 10
    Al2O3:  float = 10

cmap2 = colors.ListedColormap(['yellow', 'gold', 'orange', 'green', 'dimgray', 'black'])



def debug(output):
    if DEBUG_MODE:
        print(output)

def iterate(X):
    """Итерации магматической камеры"""
    pass
##    X1 = np.zeros((ny, nx))
##    for ix in range(nx):
##        for iy in range(ny):
##            if X[iy,ix] in (ROOF, BACKGROUND):
##                X1[iy,ix] = X[iy,ix]
##
##            elif X[iy,ix] == OL and X[iy+1,ix] not in (OL,ROOF):
##                #debug('[OL]\tX \t-->\t [X]')
##                X1[iy,ix] == X[iy+1,ix]
##            elif X[iy,ix] not in [OL,ROOF] and X[iy-1,ix] == OL:
##                #debug('OL\t[X] \t-->\t [OL]')
##                X1[iy,ix] = OL
##           
##            elif X[iy,ix] == OL:
##                #debug('[OL] \t-->\t [OL]')
##                X1[iy,ix] = OL
##            
##            elif X[iy,ix] == L2 and np.random.random() < 0.005:
##                X1[iy,ix] = OL
##             
##    return X1


fig = plt.figure(facecolor='black',figsize=(5,5))
ax = fig.add_subplot(111)
ax.set_axis_off()

nx, ny = 30, 30
X = np.array([[cell()]*nx]*ny)
X[0] = [cell(ROOF)]*nx
X[ny-1] = [cell(BACKGROUND)]*nx
X[ny-2] = [cell(ROOF)]*nx
X[20,5] = cell(OL)

im = ax.imshow(X, cmap = cmap2, interpolation = 'nearest')


def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)

animate.X = X


anim = animation.FuncAnimation(fig, animate, interval = TIME_INTERVAL, frames = 200)
plt.show()
