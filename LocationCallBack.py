# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

file = open(sys.argv[1])
ax = [];
ay = [];
mx = 0;
my = 0;
lid = ''
idx = 0
for l in file:
    ls = tuple(l.split(','))
    print ls[4]
    if lid != ls[4] and len(ax)>0:
        plt.xlim(xmax=mx*2,xmin=0)
        plt.ylim(ymax=mx*2,ymin=0)
        plt.plot(ax,ay,'-')
        plt.draw()
        ax=[]
        ay=[]
    lid = ls[4]
    x = float(ls[2])
    y = float(ls[3])
    plt.text(float(x), float(y), '%d' % idx, ha='center', va= 'bottom',fontsize=9)
    idx = idx + 1
    ax.append(x)
    ay.append(y)
    if x > mx:
        mx = x
    if y > my:
        my = y
print mx,my
plt.xlim(xmax=mx*2,xmin=0)
plt.ylim(ymax=mx*2,ymin=0)
plt.plot(ax,ay,'-')
plt.show()


