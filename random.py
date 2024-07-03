# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 21:27:09 2023

@author: lenovo
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

time = np.arange(0, 5, 0.02)
x = list()
y = list()
x_prev = 1.5
y_prev = 1.5
x.append(1.50)
y.append(1.50)
for _ in range(249):
    dist_x = 0.4 * np.random.random_sample() - 0.2
    dist_y = 0.4 * np.random.random_sample() - 0.2
    
    x_prev += dist_x
    y_prev += dist_y
    
    x.append(x_prev)
    y.append(y_prev)

data = pd.DataFrame(data= {'x' : x, 'y' : y, 'time' : time})
data.to_excel('random.xlsx')
plt.figure()
plt.plot(x, y)
