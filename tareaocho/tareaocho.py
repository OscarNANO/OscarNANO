import numpy as np
from random import randint
from math import exp, floor, log
from random import random
from numpy.random import shuffle
import matplotlib.pyplot as plt
import seaborn as sns

 

kum = [1000,2500,5000,7500,10000]           #cantidad de cumulos 
part = [100000, 500000, 1000000]              #cantidad de particulas
filtrat=[]
filtran=[]
for k in kum:
  c=0
  for n in part:
    orig = np.random.normal(size = k)
    cumulos = orig - min(orig)              
    cumulos += 1                            
    cumulos = cumulos / sum(cumulos)        
    cumulos *= n                            
    cumulos = np.round(cumulos).astype(int) 
    diferencia = n - sum(cumulos)           
    cambio = 1 if diferencia > 0 else -1    
    while diferencia != 0:                   
        p = randint(0, k - 1)
        if cambio > 0 or (cambio < 0 and cumulos[p] > 0): 
            cumulos[p] += cambio
            diferencia -= cambio
    assert all(cumulos != 0)
    print(c)
    assert sum(cumulos) == n                
 
    c = np.median(cumulos)           
    d = np.std(cumulos) / 4          
 
    def rotura(x, c, d):
        return 1 / (1 + exp((c - x) / d))    
     
    def union(x, c):
        return exp(-x / c)                      
 
    def romperse(tam, cuantos):
        if tam == 1:                
            return [tam] * cuantos
        res = []
        for cumulo in range(cuantos):
            if random() < rotura(tam, c, d):
                primera = randint(1, tam - 1)
                segunda = tam - primera
                assert primera > 0
                assert segunda > 0
                assert primera + segunda == tam
                res += [primera, segunda]
            else:
                res.append(tam) 
        assert sum(res) == tam * cuantos
        return res
 
    def unirse(tam, cuantos):
        res = []
        for cumulo in range(cuantos):
            if random() < union(tam, c):
                res.append(-tam) 
            else:
                res.append(tam)
        return res
 
    duracion = 100               
    digitos = floor(log(duracion, 10)) + 1
    nofiltra=[]
    sifiltra=[]
    for paso in range(duracion):
        assert sum(cumulos) == n
        assert all([c > 0 for c in cumulos]) 
        (tams, freqs) = np.unique(cumulos, return_counts = True)
        print(tams,freqs,'cumulos')      # cantidad maxima de cumulos
        cumulos = []
        assert len(tams) == len(freqs)
        for i in range(len(tams)):           
            cumulos += romperse(tams[i], freqs[i]) 
        assert sum(cumulos) == n
        assert all([c > 0 for c in cumulos]) 
        (tams, freqs) = np.unique(cumulos, return_counts = True)
        print(tams,freqs,'filtrados')     #cantidad maxima de filtrados
        sifiltra.append(max(freqs))
        cumulos = []
        assert len(tams) == len(freqs)
        for i in range(len(tams)):
            cumulos += unirse(tams[i], freqs[i])
        cumulos = np.asarray(cumulos)
        print(tams,freqs,'nofiltrados')     #cantidad maximoa de no filtrados
        nofiltra.append([tams])
        neg = cumulos < 0
        a = len(cumulos)
        juntarse = -1 * np.extract(neg, cumulos)     
        cumulos = np.extract(~neg, cumulos).tolist() 
        assert a == len(juntarse) + len(cumulos)
        nt = len(juntarse)
        if nt > 1:
            shuffle(juntarse)                        
        j = juntarse.tolist()
        while len(j) > 1:                            
            cumulos.append(j.pop(0) + j.pop(0))
        if len(j) > 0:                               
            cumulos.append(j.pop(0))                 
        assert len(j) == 0
        assert sum(cumulos) == n
        assert all([c != 0 for c in cumulos])
        cortes = np.arange(min(cumulos), max(cumulos), 50)
        print(cortes,paso,'tam')         

    filtrat.append(sifiltra)
  filtran.append(filtrat)  
print(filtran, kum)
     
plt.boxplot(([filtrat[i] for i in range(len(kum))]), notch=True, sym="o", labels=["Set1", "Set2", "Set3", "Set4", "Set5"])
plt.xticks([i for i in range(1, len(kum)+1)], kum)
plt.grid(True)                            #agrega una malla al grafico
plt.ylabel('Porcentaje de filtración')
plt.xlabel('Cantidad de cúmulos')
plt.savefig('graficatareaocho.png')
plt.show()
plt.close()


