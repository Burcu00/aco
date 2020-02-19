'''Ant Colony Algorithm to find shortest path in 2D map.'''

from sys import argv

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

DEPOSIT = 0.01
EVAPORATION_RATE = 0.0
image = np.array(Image.open(argv[1]), np.float)
m = np.min(image)
M = np.max(image)
image = 1. - (image - m) / (M - m)
tau = np.pad(image, 1, mode='constant')
phe = np.ones_like(tau)

print(tau)
print(phe)
plt.figure()
plt.imshow(tau, cmap='jet', origin='lower')
plt.colorbar()
#plt.show()
plt.close('All')

steps = [np.array([a, b])
         for a in [-1, 1]
         for b in [-1, 1] if max(abs(a), abs(b)) == 1.]
keys = np.array(range(len(steps)))
print(keys, steps)
paths = list()
try:
    while len(paths) < 50:
        x_max = 1
        y_max = 1
        d_max = 1
        a_pos = np.array([1, 1])
        path_length = 0.
        while not (a_pos == image.shape).all():
            phe[tuple(a_pos)] = phe[tuple(a_pos)] + DEPOSIT
            probs = np.array([tau[tuple(a_pos + steps[s])] * phe[tuple(a_pos + steps[s])] for s in keys])
            probs = probs / probs.sum()
            chosen_key = np.random.choice(keys, 1, p=probs)[0]
            a_pos = a_pos + steps[chosen_key]
            path_length = path_length + 1
            phe = np.maximum(0., phe - EVAPORATION_RATE)
            if a_pos[0] == 512 and a_pos[1] == 512:
                print('done')
            if a_pos[0] > x_max:
                x_max = a_pos[0]
                print(x_max, y_max)
            if a_pos[1] > y_max:
                y_max = a_pos[1]
                print(x_max, y_max)
            if np.sqrt(a_pos[1] ** 2 + a_pos[0] ** 2) > d_max:
                d_max = np.sqrt(a_pos[1] ** 2 + a_pos[0] ** 2)
                print(d_max)
        print(path_length)
        paths.append(path_length)
except KeyboardInterrupt:
    plt.figure()
    plt.imshow(phe, origin='lower', cmap='jet') # density
    plt.colorbar()
    plt.show()
