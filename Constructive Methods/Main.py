from AlgoritmoConstructivo import *
from AlgoritmosBusquedaLocal import *
from CotaInferior import *
import numpy as np
import matplotlib.pyplot as plt
import time

def principal(k):
    Start_time = time.time()
    cont        = k
    file        = 'hfccvrp{}.vrp'.format(k)
    archivo     = open(file)
    line        = archivo.readline().split()
    n, m        = int(line[0]), int(line[1])
    nodos       = []
    corsx       = []
    corsy       = []
    demandas    = []
    tipos       = []
    cantidades  = []
    capacidades = []
    velocidades = []
    visitados   = [False] * (n + 1)


    for i in range(m):
        line = archivo.readline().replace(',', '.').split()
        tipo, cantidad, capacidad, velocidad  = int(line[0]), int(line[1]), int(line[2]), float(line[3])
        tipos.append(tipo)
        cantidades.append(cantidad)
        capacidades.append(capacidad)
        velocidades.append(velocidad)

    for i in range(n+1):
        line = archivo.readline().replace(',', '.').split()
        nodo, corx, cory, demanda = int(line[0]), int(line[1]), int(line[2]), float(line[3])
        nodos.append(nodo)
        corsx.append(corx)
        corsy.append(cory)
        demandas.append(demanda)

    matriz = llenar_matriz(tipos,cantidades,capacidades,velocidades,m)
    A = np.transpose(matriz)
    vehiculos = replicar_vehiculo(A)
    matriz_dist = matriz_distancia(corsx, corsy,n)
    visitados[0] = True
    num_vehiculos = len(vehiculos)
    cota = cotaInferior(n,matriz_dist,demandas,vehiculos[0][2])
    #print(sum(demandas))


    B = []

    colors = "bgrcmykwbgrcmykw"
    tiempo_total = 0
    demandas_nodos = []
    for i in range(len(vehiculos)):
        resultado = nodos_a_recorrer(vehiculos[i], matriz_dist, visitados, demandas)
        n_a_recorrer = [0] + resultado[0] + [0]
        dist_recorrida = resultado[1]
        vector_distancia_recorrida = [0] + resultado[3] + [0]
        x = []
        y = []

        for j in n_a_recorrer:
            x.append(corsx[j])
            y.append(corsy[j])
            demandas_nodos.append(demandas[j])
        #a = np.dot(demandas_nodos,vector_distancia_recorrida)
        #tiempo_vehiculos = a * vehiculos[i][2]
        tiempo_vehiculos =  funcion_objetivo_vehiculo(demandas_nodos,vector_distancia_recorrida,vehiculos[i][2])
        plt.plot(x, y, '-ok', color=colors[i % len(colors)])
        A = [i, vehiculos[i, 0], len(n_a_recorrer), n_a_recorrer]
        #print(vector_distancia_recorrida)
        demandas_nodos = []
        tiempo_total += tiempo_vehiculos
        B.append(A)
        delta = ((tiempo_total-cota)/cota)*100
    # print(delta)
    print(tiempo_total)
    #
    # plt.xlabel('x - axis')
    # plt.ylabel('y - axis')
    # plt.title('Ejemplo' + ' ' + str(k) + ' '  +'con método constructivo')
    # plt.show()
    Finish_time = time.time()
    Time = Finish_time-Start_time
    # print(Time)
    return B


def print_routes(i):
    routes = principal(i)
    file   = open('hfccvrp{}.csol'.format(i), 'w')
    for route in routes:
        string = str(int(route[1])) + ' ' + str(int(route[2]))
        for node in route[3]:
            string += ' ' + str(node)
        file.write(string + '\n')


for i in range(21):
    print_routes(i + 1)

