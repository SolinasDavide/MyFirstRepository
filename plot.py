#! /usr/bin/python3

import math

from matplotlib import pyplot as plt
import numpy as np


data = {
    'x': [],
    'y' : []
}
for x in np.arange(int(input('inizio domino: ')), int(input('fine dominio: ')), 0.1 ):
    data['x'].append(x)
    data['y'].append(math.pow(x, 3 ))

plt.plot(data['x'], data['y'])

plt.show() # print