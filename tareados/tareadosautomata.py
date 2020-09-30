import numpy as np 
from random import uniform,random 
import matplotlib.cm as cm
import matplotlib.pyplot as plt

dim = 20
num = dim**2
#en el rango entre [0.1-0.9]:
prob = uniform(0.1,0.9)
valores = [round(random())< prob for i in range(num)]   
actual = np.reshape(valores, (dim, dim))
#fin de librerias y variables a utilizar
#modulos o funciones
def mapeo(pos):
    fila = pos // dim
    columna = pos % dim
    return actual[fila, columna]

assert all([mapeo(x) == valores[x]  for x in range(num)])

def paso(pos):
    fila = pos // dim
    columna = pos % dim
    vecindad = actual[max(0, fila - 1):min(dim, fila + 2),
                      max(0, columna - 1):min(dim, columna + 2)]
    return 1 * (np.sum(vecindad) - actual[fila, columna] == 3)

print(actual)
#final modular
#programa principal
if __name__ == "__main__":
    fig = plt.figure()
    plt.imshow(actual, interpolation='nearest', cmap=cm.Greys)
    fig.suptitle('Estado inicial')
    plt.savefig('p2_0_.png')  #se obtuvo una imagen en formato png
    plt.close()
#final grafica
    lista_actual=[]                
    lista_posx=[]         
    lista_posy=[]
    listaiter=[]
    salida=open('vivos.txt','w')
    for iteracion in range(50): #cantidad de iteraciones hechas
        print("Iter", iteracion)
        valores = [paso(x) for x in range(num)]   #vivo o muerto, a esto se le llama juego de la vida
        vivos = sum(valores)
        print(iteracion, vivos)
        if vivos == 0:
            print('# Game Over.')
            break;                          
        actual = np.reshape(valores, (dim, dim))
        lista_actual.append(actual)
        print(actual)
        mvivos=np.equal(actual,1)
        print(mvivos)
        for n in range(dim):
            for m in range (dim):
                if mvivos[n,m]==True:
                   print(n,m,iteracion)
                   lista_posx.append(n)
                   lista_posy.append(m)
                   listaiter.append(iteracion)
                   salida.write("%f %f %f \n" % (n,m,iteracion))           
        fig = plt.figure()
        plt.imshow(actual, interpolation='nearest', cmap=cm.Greys)
        fig.suptitle('Paso {:d}'.format(iteracion + 1))
        plt.savefig('p2_t{:d}_p.png'.format(iteracion + 1))  
        plt.close()
    salida.close()
    plt.plot(lista_posx,lista_posy,'o')
    plt.xlabel('x')
    plt.ylabel('y')
    for i,txt in enumerate (listaiter):
        plt.annotate(str(txt),(lista_posx[i],lista_posy[i]))
    plt.show()
    
