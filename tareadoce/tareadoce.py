from random import randint
from math import floor, log
import pandas as pd
import numpy as np, array
from sklearn.metrics import f1_score
import mathplotlib.pyplot as plt


proban=[0.995,0.990,0.080,0.001]
probag=[0.92,0.993,0.053,0.99]
probab=[0.002,0.001,0.994,0.023]
listafc=[]
for p in range(4-1):
    #lo tiene en dos dimenciones para poder mapearlo, se entrena al percepron como saber si x es mayor a y
    modelos = pd.read_csv('digits.txt', sep=' ', header = None) #llamamos al archivo de text donde esta codificado los numeros
    modelos = modelos.replace({'n': proban[p], 'g': probag[p], 'b': probab[p]}) #probabilidades de color, se sustituyen las letras por numeros
    r, c = 5, 3 #r es renglon y c es columna
    dim = r * c
 
    tasa = 0.15 #tasa de aprendizaje
    tranqui = 0.99 #taza de tranquilizacion
    tope = 9
    k = tope + 1 # incl. cero
    contadores = np.zeros((k, k + 1), dtype = int)
    n = floor(log(k-1, 2)) + 1
    neuronas = np.random.rand(n, dim) # perceptrones
    print(neuronas, contadores)
    print(n,'n1')

    tasatotal=[]
    tasa_true=[]
    tasaneu=[]
    for t in range(5000): # entrenamiento
        d = randint(0, tope) #elejimos un digito
        pixeles = 1 * (np.random.rand(dim) < modelos.iloc[d]) #genera valores al azar los compara cn las probabilidades y el si o no es mayor a la probabilidad termina siento un verdad o falso donde negros son verdades y blancos los falsos
        correcto = '{0:04b}'.format(d) #revisa cual es el binario correcto
        for i in range(n):
            w = neuronas[i, :] #calculamos usando las neuronas
            deseada = int(correcto[i]) # 0 o 1  que es lo que queriamos que diera
            resultado = sum(w * pixeles) >= 0 #genera algun verdad o falso #suma los pesos de la entrada
            if deseada != resultado:  #coompara si es lo que queriamos es lo mismo que recibimos
                ajuste = tasa * (1 * deseada - 1 * resultado) #cual era la diferencia cuando no son los mismos
                tasa = tranqui * tasa #se tranquiliza la tabla multiplicando por el parametro que se va eliminando
                neuronas[i, :] = w + ajuste * pixeles #se actualizan
                tasatotal.append(tasa)
                print (tasa,n,'n2')
                tasaneu.append([tasa,i])
    mtasa = np.array(tasaneu)
    tasa0=[]
    tasa1=[]
    tasa2=[]
    tasa3=[]
    for t in range (len(tasatotal)):
        if mtasa[t,1] ==0:
            tasa0.append(mtasa)
        if mtasa[t,1] ==1:
            tasa1.append(mtasa)
        if mtasa[t,1] ==2:
            tasa2.append(mtasa)
        if mtasa[t,1] ==3:
            tasa3.append(mtasa)
        
    ptasa0=sum(tasa0)/len(tasa0)
    ptasa1=sum(tasa1)/len(tasa1)
    ptasa2=sum(tasa2)/len(tasa2)
    ptasa3=sum(tasa3)/len(tasa3)
    tasa_true=[ptasa0,ptasa1,ptasa2,ptasa3]
            
    print(tasa_true,n,'tasatruem3')
    #checa si son verdaderos, o no o si son residuos 
    for t in range(300): # prueba
        d = randint(0, tope) #genera un digito al azar
        pixeles = 1 * (np.random.rand(dim) < modelos.iloc[d]) #genera la plantilla
        correcto = '{0:04b}'.format(d) #checacual debio ser
        salida = ''
        for i in range(n):
            salida += '1' if sum(neuronas[i, :] * pixeles) >= 0 else '0'
        r = min(int(salida, 2), k)
        contadores[d, r] += 1
    print(contadores,n,'contadoresn4')
    c = pd.DataFrame(contadores)
    c.columns = [str(i) for i in range(k)] + ['NA']
    c.index = [str(i) for i in range(k)]
    print(correcto,n,'correcto6')
    print(c)
    diagonal=[]
    for i in range (n):
        for j in range (n):
            if i ==j:
                diagonal.append(contadores[i,j])
    print(n,'n5')          
    print(diagonal)
f1_score =(tasa_true, diagonal)
FC= f1_score
print(FC)
listafc.append(FC)



    plt.boxplot(listafc)
    plt.xticks([i for i in range(1, 4)], [i,2,3,4])
    plt.grid(True)                            #agrega cuadros al grafico
    plt.ylabel('Porcentajes')
    plt.xlabel('Combinaciones')
    plt.show()
    plt.close()
    #f score representa la matriz con un numero y luego diseñar el experimento factorial para variar las 3 probabilidades, viendo que le pasa al fscore de la red neuronal cuano hacemos esas variaciones
    #perceptron calcula el producto interno y suma los productos y compara si la suma supera el umbral 

