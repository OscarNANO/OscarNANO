from math import ceil, sqrt
def primo(n):
    if n < 4:
        return(-1)
    if n % 2 == 0:
        return (2)
    for i in range(3, int(ceil(sqrt(n))), 2):
        if n % i == 0:
            return(i)
    return (-1)
 
from scipy.stats import describe 
from random import shuffle
import multiprocessing   #paralelizar
from time import time
import psutil
import numpy as np
import matplotlib.pyplot as plt
core = psutil.cpu_count()               #usar los dos nucleos
v_core = psutil.cpu_count(logical = False)
if __name__ == "__main__":
 
    with open('numerosprimos.txt','r')as input: 
        linea=input.readline()
        #print(linea)
        lprimos=[int(valor)for valor in linea.split(',')]
    original=[x for x in lprimos]
    print (len(original))
    desde = original[0]  
    hasta = original[4000]                  
    original2 = [x for x in range(desde, hasta + 1)]
    datos_faciles=[]
    for numero in original2:
            datos_faciles.append(numero)
            resultado=primo(numero)
            print(numero,resultado)
    invertido = original2[::-1]                                            
    aleatorio = original2.copy()
    shuffle(aleatorio)
    replicas = 10
    pg1 = []
    pg2 = []
    pg3 = []
    grafica1 = []
    grafica2 = []
    NUCLEOS = range(1, core + 1) #2nucleos
    tiempos = {"ot": [], "it": [], "at": []}
    for core in NUCLEOS: 
         print("--------", core, "---------")
         with multiprocessing.Pool() as pool:
             for r in range(replicas):
                 t = time()
                 pool.map(primo, original2)
                 tiempos["ot"].append(time() - t)
                 t = time()
                 pool.map(primo, invertido)
                 tiempos["it"].append(time() - t)
                 shuffle(aleatorio)
                 t = time()
                 pool.map(primo, aleatorio)
                 tiempos["at"].append(time() - t)
         for tipo in tiempos:              #2nucleos
             print(describe(tiempos[tipo]))
             if core == 1:
                grafica1.append(tiempos[tipo])
             elif core == 2:
                grafica2.append(tiempos[tipo])
        
         pg1.append(np.mean(tiempos["ot"]))
         pg2.append(np.mean(tiempos["it"]))
         pg3.append(np.mean(tiempos["at"]))

         tiempos = {"ot": [], "it": [], "at": []}
         print("-----------------------", core, "-----------------------")

    print("--------------------", "Global", "---------------------")
    print("")
    print(pg1)
    print("")

    print("")
    print(pg2)
    print("")

    print("")
    print(pg3)
    print("")
    print("--------------------", "Global", "---------------------")

    plt.subplot(211)
    plt.boxplot(grafica1)
    plt.xticks([1, 2, 3], ['original', 'invertido', 'Aleatorio'])
    plt.ylabel('Tiempo (seg)')
    plt.title('1 Núcleo')


    plt.subplot(212)
    plt.boxplot(grafica2)
    plt.xticks([1, 2, 3], ['original', 'invertido', 'Aleatorio'])
    plt.ylabel('Tiempo (seg)')
    plt.title('2 Núcleos')

    plt.subplots_adjust(top=0.95, bottom=0.08, left=0.05, right=0.95, hspace=0.35,
                        wspace=0.2)

    plt.show()
    plt.close()

    plt.plot(pg1, label="original")
    plt.xticks([0, 1], ['1', '2'])
    plt.plot(pg2, label="invertido")
    plt.xticks([0, 1], ['1', '2'])
    plt.plot(pg3, label="aleatorio")
    plt.xticks([0, 1], ['1', '2'])
    plt.xlabel('Núcleos')
    plt.ylabel('Tiempo (seg)')
    plt.legend()
    plt.show()
    plt.close()
