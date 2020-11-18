import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colorbar as colorbar
from matplotlib.colors import LinearSegmentedColormap
from math import fabs, sqrt, floor, log
import multiprocessing
from itertools import repeat
from os import popen
from random import uniform

n = 60   #cantidad de particulas
dt=1

x = np.random.normal(size = n)
y = np.random.normal(size = n)
c = np.random.normal(size = n)
m = np.random.normal(size = n)
vx = np.random.normal(size = n)
vy = np.random.normal(size = n)
magv = (vx**2 + vy**2)**0.5

print(m)

xmax = max(x)
xmin = min(x)

#min 1 max 0 

x = (x - xmin) / (xmax - xmin) # de 0 a 1

#cargas entre -1 y 1 
ymax = max(y)
ymin = min(y)
y = (y - ymin) / (ymax - ymin) 
cmax = max(c)
cmin = min(c)

c = 2 * (c - cmin) / (cmax - cmin) - 1 #cargas entre -1 y 1
g = np.round(5 * c).astype(int)        #redondeo cargas
cgravity=6.67e-11           #constante gravitacional
print(g)

p = pd.DataFrame({'x': x, 'y': y, 'c': c, 'g': g, 'm':m})
v = pd.DataFrame({'vx': vx, 'vy': vy, 'c': c, 'magv': magv, 'm':m})

#colors
paso = 256 // 10
niveles = [i/256 for i in range(0, 256, paso)]
colores = [(niveles[i], 0, niveles[-(i + 1)]) for i in range(len(niveles))]
 
palette = LinearSegmentedColormap.from_list('tonos', colores, N = len(colores))


 
eps = 0.001                 #factor para descuento 
def fuerza(i):              #funcion fuerza 
    pi = p.iloc[i]          
    xi = pi.x           
    yi = pi.y                
    ci = pi.c               
    mi = abs(pi.m)
    fx, fy = 0, 0           #fuerzas en 'x' y 'y' comienzan en cero
    fx1,fy1= 0, 0
    for j in range(n):      #comparacion 
        pj = p.iloc[j]      #afuera de la posicion j 
        cj = pj.c
        mj = abs(pj.m)
        dire = (-1)**(1 + (ci * cj < 0))    #direccion y fuerzas
        dire2= (-1)**(1 + (mi < mj))
        dx = xi - pj.x
        dy = yi - pj.y
        factor = dire * fabs(ci * cj) / (sqrt(dx**2 + dy**2) + eps)
        factor2 =dire2 *(mi *  mj) / (sqrt(dx**2+ dy**2) +eps)
        fx -= dx * factor
        fy -= dy * factor
        fx1 -= dx * factor2
        fy1 -= dy * factor2
        print(fy,m,g)
    return (fx + fx1, fy +fy1)

def velocidades(i):
    pi = p.iloc[i]
    mi = abs(pi.m)
    #for j in range (n):
    fuerzai = fuerza(i)
    v = (fuerzai*dt)/(2*mi)
    return v
    
popen('rm -f tareanueve_t*.png')
tmax = 200
digitos = floor(log(tmax, 10)) + 1
fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
pos = plt.scatter(p.x, p.y, c = p.g, s = 70, marker = 's', cmap = palette)
fig.colorbar(pos, ax=ax)
plt.title('Estado inicial')
plt.grid(True)
plt.xlabel('X')
plt.ylabel('Y')
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)
fig.savefig('tareanueve_t0.png')
plt.close()

def actualiza(pos, fuerza, de):
    return max(min(pos + de * fuerza, 1), 0)
 
 
if __name__ == "__main__":
    vtotal=[]
    for t in range(tmax):
        with multiprocessing.Pool() as pool: 
            f = pool.map(fuerza, range(n))
            vv = pool.map(velocidades, range(n))
            delta = 0.02 / max([max(fabs(fx), fabs(fy)) for (fx, fy) in f])   #normalizacion de delta
            #posiciones en 'x' y 'y' 
            p['x'] = pool.starmap(actualiza, zip(p.x, [v[0] for v in f], repeat(delta)))
            p['y'] = pool.starmap(actualiza, zip(p.y, [v[1] for v in f], repeat(delta)))
            v['vx'] = pool.starmap(actualiza, zip(v.vx, [v[0] for v in vv], repeat(delta)))
            v['vy'] = pool.starmap(actualiza, zip(v.vy, [v[1] for v in vv], repeat(delta)))
            v['magv'] = pool.starmap(actualiza, zip(v.magv, [v[0] for v in vv], repeat(delta)))
            vtotal.append(v.magv)    #promedio de las velocidades
            print(v,vv,v.shape)
            #parte grafica
            
            fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
            pos = plt.scatter(p.x, p.y, c = p.g, s = 70, marker = 's', cmap = palette)
            fig.colorbar(pos, ax=ax)
            plt.grid(True)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.xlim(-0.1, 1.1)
            plt.ylim(-0.1, 1.1)            
            plt.title('Paso {:d}'.format(t + 1))
            fig.savefig('tareanueve_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
            plt.close()
        
            plt.hist(v.magv)
            plt.grid(True)
            plt.xlabel('velocidades')
            plt.title('Paso {:d}'.format(t + 1))
            plt.savefig('tareanuevemag_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
            plt.close()
            
    plt.hist(v.m)
    plt.grid(True)
    plt.xlabel('Masas')
    plt.title('Paso {:d}'.format(t + 1))
    plt.savefig('tareanuevemasa_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
    plt.close()

    plt.hist(sum(vtotal)/tmax)
    plt.grid(True)
    plt.xlabel('Promedio de velocidades')
    plt.title('Paso {:d}'.format(t + 1))
    plt.savefig('tareanuevemag_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
    plt.close()

    plt.hist(v.c)
    plt.grid(True)
    plt.xlabel('Cargas')
    plt.title('Paso {:d}'.format(t + 1))
    plt.savefig('tareanuevecarga_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
    plt.close()
#popen('conv


