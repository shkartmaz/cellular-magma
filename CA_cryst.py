import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors


# попытка смоделировать магматическую камеру как клеточный автомат
# v0.2
# кристаллы оливина случайным образом формируются в однородной толще расплава
# и тонут. Температура системы постоянна

neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,1), (1,0), (1,1))
L2, L1, L0 = 0, 1, 2
OL, ROOF = 3, 4
BACKGROUND = 5
cmap2 = colors.ListedColormap(['yellow', 'gold', 'orange', 'green', 'dimgray', 'black'])

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


fig = plt.figure(facecolor='black',figsize=(5,5))
ax = fig.add_subplot(111)
ax.set_axis_off()

nx, ny = 30, 30
X = np.zeros((ny, nx))
X[0] = [ROOF]*nx
X[ny-1] = [BACKGROUND]*nx
X[ny-2] = [ROOF]*nx
X[20,5] = OL

im = ax.imshow(X, cmap = cmap2, interpolation = 'nearest')


def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)

animate.X = X


anim = animation.FuncAnimation(fig, animate, interval = TIME_INTERVAL, frames = 200)
plt.show()
