import seaborn as sns
from math import sqrt,fabs
from scipy.stats import describe
from PIL import Image, ImageColor
from random import randint, choice
import matplotlib.pyplot as plt


n, semillas = 80, []        


 
def celda(pos,k):
    if pos in semillas:
        return semillas.index(pos)
    x, y = pos % n, pos // n
    cercano = None
    menor = n * sqrt(2)
    for i in range(k):
        (xs, ys) = semillas[i]
        dx, dy = x - xs, y - ys
        dist = sqrt(dx**2 + dy**2)
        if dist < menor:
            cercano, menor = i, dist
    return cercano
 
def inicio():
    direccion = randint(0, 3)
    if direccion == 0:            #down to up
        return (0, randint(0, n - 1))
    elif direccion == 1:          #left to right
        return (randint(0, n - 1), 0)
    elif direccion == 2:          #right to left
        return (randint(0, n - 1), n - 1)
    else:
        return (n - 1, randint(0, n - 1))
    
def euclideana(p1, p2):
    return sqrt(sum([(c1 - c2)**2 for (c1, c2) in zip(p1, p2)]))
def manhattan(p1, p2):
    return sum([fabs(c1 - c2) for (c1, c2) in zip(p1, p2)])
def md_orig(p):
    largo = len(p)
    origen = [0] * largo
    return manhattan(p, origen)

 #voronoi

 #grieta
def propaga(replica):
    name=replica
    prob, dificil = 0.9, 0.8
    grieta = voronoi.copy()
    g = grieta.load()
    #(x, y) = inicio()
    (x,y)=(0,0)
    largo = 0
    negro = (0, 0, 0)
       
    while True:
        g[x, y] = negro
        largo += 1
        frontera, interior = [], []
        for v in vecinos:
            (dx, dy) = v
            vx, vy = x + dx, y + dy
            if vx >= 0 and vx < n and vy >= 0 and vy < n: #cuando si hay grieta
               if g[vx, vy] != negro:       #caundo no hay grieta
                   if vor[vx, vy] == vor[x, y]: #grieta en la misma celda
                       interior.append(v)
                       print(v,interior,'misma celda')
                   else:
                       frontera.append(v)
                       print(v,frontera,'no tiene grieta')
        elegido = None
        if len(frontera) > 0:
            elegido = choice(frontera)
            prob = 1
            print(elegido,'frontera mayor que cero')
        elif len(interior) > 0:
            elegido = choice(interior)
            prob *= dificil
            print(elegido,'interior mayor que cero')
        if elegido is not None:
            (dx, dy) = elegido
            x, y = x + dx, y + dy
            print(elegido,'Ninguno')
        else:
            print(elegido,'elegido') 
            break #termina grieta
        p=(dx,dy)+(x,y)    
    muylargo=md_orig(p)
    x=(0,0)
    distancia=euclideana(x,p)
    print(largo,muylargo,distancia,'fin de rutina')
    if largo >= limite:
        visual = grieta.resize((10 * n,10 * n))
        visual.save(str(name)+"40semillas_{:d}.png".format(replica))
    return largo,muylargo,distancia

nsemillas=[]
pg1 = []
pg2 = []
for r in range(15,30): 
    for s in range(r):
        while True:
            x, y = randint(0, n - 1), randint(0, n - 1)
            if (x, y) not in semillas:
                semillas.append((x, y))
                break
    celdas = [celda(i,r) for i in range(n * n)]
    voronoi = Image.new('RGB', (n, n))
    vor = voronoi.load()
    c = sns.color_palette("Paired", r).as_hex()  #grafica
    for i in range(n * n):
        vor[i % n, i // n] = ImageColor.getrgb(c[celdas.pop(0)])
    limite, vecinos = n, []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                vecinos.append((dx, dy))
    L,LG,D=propaga(r)
    print(r,'numero de veces')
    nsemillas.append(r)
    pg1.append(LG)
    pg2.append(D)
    

plt.subplot(211)
plt.plot(nsemillas,pg1, label="Manhathan")    
plt.subplot(212)    
plt.plot(nsemillas,pg2, label="Euclideana")
plt.xlabel('Semillas')
plt.ylabel('Distancia maxima')
plt.legend()
plt.subplots_adjust(top=0.95, bottom=0.08, left=0.05, right=0.95, hspace=0.35,
                        wspace=0.2)
plt.show()
plt.close() 
