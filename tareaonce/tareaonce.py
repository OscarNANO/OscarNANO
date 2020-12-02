import numpy as np
import pandas as pd 
from random import randint, random
 
def poli(maxdeg, varcount, termcount):  #polinomio
    f = []  #dataframe
    for t in range(termcount): 
        var = randint(0, varcount - 1) #variable
        deg = randint(1, maxdeg)         #grado
        f.append({'var': var, 'coef': random(), 'deg': deg})  #coeficiente aleatorio
    return pd.DataFrame(f)  
  
def evaluate(pol, var):  
    return sum([t.coef * var[pol.at[i, 'var']]**t.deg for i, t in pol.iterrows()])
 
 
def domin_by(target, challenger):  #
    if np.any(challenger < target):
        return False
    return np.any(challenger > target)

w=0 
while w <= 12:
    w = w+1  #contador
    vc = 4   #variables posibles
    md = 3   #maximo grado permitido
    tc = 5   #cantidad de terminos
    k = 2 
    obj = [poli(md, vc, tc) for i in range(k)]  #objetivos
    minim = np.random.rand(2) > 0.5
    n = 150 #soluciones
    sol = np.random.rand(n, vc)  
    val = np.zeros((n, k))       
    print(val)
    for i in range(n): 
        for j in range(k):
            val[i, j] = evaluate(obj[j], sol[i])     
    sign = [1 + -2 * m for m in minim]
    mejor1 = np.argmax(sign[0] * val[:, 0])   
    mejor2 = np.argmax(sign[1] * val[:, 1])  
    cual = {True: 'min', False: 'max'}    
    print(val[:, 0],'mejor valor', val[:, 1], 'mejor valor 2')
    #grafica
    import matplotlib.pyplot as plt
    '''
    plt.figure(figsize=(8, 6), dpi=300)        
    plt.plot(val[:, 0], val[:, 1], 'o', fillStyle = 'none')
    plt.xlabel('Primer objetivo')
    plt.ylabel('Segundo objetivo')
    plt.title('Ejemplo en 2 dimensiones')
    plt.savefig('tareaonce_init'+str(w)+'.png', bbox_inches='tight')
    plt.close()
    fig = plt.figure(figsize=(8, 6), dpi=300)        
    ax = plt.subplot(111)
    ax.plot(val[:, 0], val[:, 1], 'o', color = 'k', fillStyle = 'none')
    ax.plot(val[mejor1, 0], val[mejor1, 1], 's', color = 'green')  #mejor del primero
    ax.plot(val[mejor2, 0], val[mejor2, 1], 'o', color = 'red') #mejor del segundo
    plt.xlabel('Primer objetivo ({:s}) mejor con cuadro verde'.format(cual[minim[0]])) 
    plt.ylabel('Segundo objetivo ({:s}) mejor con bolita roja'.format(cual[minim[1]])) 
    plt.title('Ejemplo en 2 dimensiones')
    plt.savefig('tareaonce_mejores'+str(w)+'.png', bbox_inches='tight')
    plt.close()
    '''
    dom = []
    for i in range(n):
        d = [domin_by(sign * val[i], sign * val[j]) for j in range(n)]
        dom.append(sum(d)) 
    frente = val[[d == 0 for d in dom], :]
    print(frente, 'frente')
    fig = plt.figure(figsize=(8, 6), dpi=300)        
    ax = plt.subplot(111)
    ax.plot(val[:, 0], val[:, 1], 'o', color = 'k', fillStyle = 'none')
    print(val, 'val')
    # para opciones de colores, ver https://matplotlib.org/examples/color/named_colors.html
    ax.plot(frente[:, 0], frente[:, 1], 'o', color = 'lime') 
    plt.xlabel('Primer objetivo ({:s})'.format(cual[minim[0]])) 
    plt.ylabel('Segundo objetivo ({:s})'.format(cual[minim[1]])) 
    plt.title('Ejemplo en 2 dimensiones')
    plt.savefig('tareaonce_frente'+str(w)+'.png', bbox_inches='tight')
    plt.close()
    # lo que resta fue adaptado de
    # https://matplotlib.org/3.1.0/gallery/statistics/customized_violin.html##partefrafica
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(4, 12))
    plt.ylabel('Porcentaje')
    plt.title('Cantidad de soluciones dominantes')
    parts = ax.violinplot(dom, showmeans=False, showmedians=False, showextrema=False)
    for p in parts['bodies']:
        p.set_facecolor('blue')
        p.set_edgecolor('black')
        p.set_alpha(1)

    
    d = sorted(dom)
    m = np.median(d)
    q1, m, q3 = np.percentile(d, [25, 50, 75])
    ax.scatter(1, m, marker = '_', color = 'lime', s = 100, zorder = 3)
    ax.vlines(1, q1, q3, color = 'pink', linestyle = '-', lw = 20)
 
    # basemos el filtrado de datos anomales en 
    # https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
    def is_outlier(d, iqr = 0.5):
        p = (1 - iqr) / 2
        s = pd.Series(d)
        qlow, med, qhigh = s.quantile([p, 0.50, 1 - p])
        iqr = qhigh - qlow
        return ((s - med).abs() > iqr).values

    out = is_outlier(d)
    from itertools import compress
    y = list(compress(d, out)) 
    x = [1] * len(y)             
    ax.scatter(x, y, marker = 'o', color = 'lime', s = 3, zorder = 3)
    a = list(compress(d, ~np.array(out))) 
    low, high = a[0], a[-1]
    # agregamos el eje 
    ax.vlines(1, low, high, color = 'lime', linestyle = '-', lw = 2)
    # los bigotes del eje
    ax.scatter([1, 1], [low, high], color = 'lime', marker = '_', s = 100, zorder = 3)
    ax.get_xaxis().set_tick_params(direction = 'out')
    ax.set_xticks([])
    ax.set_xlabel('')
    plt.subplots_adjust(bottom = 0.5, wspace = 0.02)
    plt.savefig('tareaonce_violin'+str(w)+'.png', bbox_inches = 'tight')
    plt.close()

