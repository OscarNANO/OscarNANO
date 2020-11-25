import numpy as np
from numpy import *
import pandas as pd
from random import random, randint, sample, uniform
import matplotlib.pyplot as plt

 
def knapsack(peso_permitido, pesos, valores):
    assert len(pesos) == len(valores)
    peso_total = sum(pesos)
    valor_total = sum(valores)
    if peso_total < peso_permitido: 
        return valor_total
    else:
        V = dict()
        for w in range(peso_permitido + 1):
            V[(w, 0)] = 0
        for i in range(len(pesos)):
            peso = pesos[i]
            valor = valores[i]
            for w in range(peso_permitido + 1):
                cand = V.get((w - peso, i), -float('inf')) + valor
                V[(w, i + 1)] = max(V[(w, i)], cand)
        return max(V.values())
 
def factible(seleccion, pesos, capacidad):
    return np.inner(seleccion, pesos) <= capacidad
  
def objetivo(seleccion, valores):
    return np.inner(seleccion, valores)
 
def normalizar(data):
    menor = min(data)
    mayor = max(data)
    rango  = mayor - menor
    data = data - menor 
    return data / rango 
  
def generador_pesos(cuantos, low, high):
    return np.round(normalizar(np.exp(cuantos)) * (high - low) + low)
 
def generador_valores(pesos, low, high, b, regla):
    n = len(pesos)
    valores = np.empty((n))
    for i in range(n):
        if regla == 1: 
           valores[i] = np.exp(b* pesos[i])
        if regla == 2:
            valores[i] = np.exp(b* pesos[i]) * uniform(0, 0.01)
        if regla == 3:
            valores[i] = uniform(0, 0.01) / np.exp(b* pesos[i])
    return normalizar(valores) * (high - low) + low
 
def poblacion_inicial(n, tam):
    pobl = np.zeros((tam, n))
    for i in range(tam):
        pobl[i] = (np.round(np.random.uniform(size = n))).astype(int)
    return pobl
 
def mutacion(sol, n):
    pos = randint(0, n - 1)
    mut = np.copy(sol)
    mut[pos] = 1 if sol[pos] == 0 else 0
    return mut
  
def reproduccion(x, y, n):
    pos = randint(2, n - 2)
    xy = np.concatenate([x[:pos], y[pos:]])
    yx = np.concatenate([y[:pos], x[pos:]])
    return (xy, yx)

def ruleta (bestpadres):
    padres = sample(bestpadres, 2)
    pa=padres[0]
    ma=padres[1]
    hijos = reproduccion(p[:pa], p[pa:ma], n)
    h1 = hijos[0]
    h2 = hijos[1]
    print(h1,h2,'hijos')
    hijo = h1+h2
    return(hijo)

a=0.5
b=0.001
regla=3
n = 400    
tiempo=[i for i in range (n)]
pesos = generador_pesos(a*array(tiempo), 15, 80)
valores = generador_valores(pesos, 10, 500,b, regla)


plt.plot(tiempo, valores, label='Valores')
plt.plot(tiempo, pesos, label='Pesos')
plt.xlabel('Objetos')
plt.ylabel('Pesos y valores')    #el peso es la linea azul y los valores naranja
plt.grid(True)
plt.legend()
plt.savefig('400GB'+str(regla)+ str(b)+ str(a)+'.png', bbox_inches='tight') 
plt.close

capacidad = int(round(sum(pesos) * 0.65))
optimo = knapsack(capacidad, pesos, valores)
init = 100  
p = poblacion_inicial(n, init)
print(p, p.shape)
tam = p.shape[0]
assert tam == init
pm = 0.05  
rep = 50    
tmax = 50    
mejor = None
mejores = []
for t in range(tmax):
    for i in range(tam): 
        if random() < pm:
            p = np.vstack([p, mutacion(p[i], n)])
    for i in range(rep):  
        padres = sample(range(tam), 2)

        hijos = reproduccion(p[padres[0]], p[padres[1]], n)
        p = np.vstack([p, hijos[0], hijos[1]])
    tam = p.shape[0]
    d = []
    for i in range(tam):          
        d.append({'idx': i, 'obj': objetivo(p[i], valores),   
                  'fact': factible(p[i], pesos, capacidad)})   
    d = pd.DataFrame(d).sort_values(by = ['fact', 'obj'], ascending = False)
    mantener = np.array(d.idx[:init])      
    p = p[mantener, :]
    tam = p.shape[0]
    assert tam == init
    factibles = d.loc[d.fact == True,]
    mejor = max(factibles.obj)
    mejores.append(mejor)
 
plt.figure(figsize=(7, 3), dpi=300)
plt.plot(range(tmax), mejores, 'ks--', linewidth=1, markersize=5)
plt.axhline(y = optimo, color = 'green', linewidth=3)
plt.xlabel('Paso')
plt.ylabel('Valor mayor')
plt.grid(True)
plt.ylim(0.95 * min(mejores), 1.05 * optimo)
plt.savefig('75p10p'+str(regla)+ str(b)+ str(a)+'.png', bbox_inches='tight') 
plt.close()
print(mejor, (optimo - mejor) / optimo)
