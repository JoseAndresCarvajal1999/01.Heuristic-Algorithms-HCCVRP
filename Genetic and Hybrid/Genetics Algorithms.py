import random
from AlgoritmosBusquedaLocal import *

def seleccion_por_torneo(Poblacion_inicial,x,y):
    a_p = 0
    b_p = 0
    a_m = 0
    b_m = 0
    while a_p == b_p:
        a_p = random.randint(0, Poblacion_inicial - 1)
        b_p = random.randint(0, Poblacion_inicial - 1)
    padre_a = x[a_p]
    # print(' 1 ------------------------------')
    # print(len(x))
    padre_b = x[b_p]
    # print(' 2 ------------------------------')
    # print(len(x))
    fitness_padre_a = y [a_p]
    fitness_padre_b = y [b_p]
    if fitness_padre_a < fitness_padre_b:
        padre = padre_a
        fitness_padre = fitness_padre_a
        posicion_papa = a_p
    else:
        padre = padre_b
        fitness_padre = fitness_padre_b
        posicion_papa = b_p

    while a_m == b_m:
        a_m = random.randint(0, Poblacion_inicial -1)
        b_m = random.randint(0, Poblacion_inicial - 2)
    madre_a = x[a_m]
    madre_b = x[b_m]
    fitness_madre_a = y[a_m]
    fitness_madre_b = y[b_m]
    if fitness_madre_a < fitness_madre_b:
        madre = madre_a
        fitness_madre = fitness_madre_a
        posicion_mama = a_m

    else:
        madre = madre_b
        fitness_madre = fitness_madre_b
        posicion_mama = b_m
    return padre,fitness_padre,madre,fitness_madre,posicion_mama,posicion_papa

def cruce(padre,madre):
    n = len(padre)
    a = random.randint(0,n-1)
    hijo1 = padre[:a] + madre[a:]
    hijo2 = madre[:a] + padre[a:]
    return hijo1, hijo2


def penalizacion_visitados(solucion,numero_nodos,demandas,matriz_dist,velocidad,cota,penalizacion):
    visitados = [False]*(numero_nodos+1)
    visitados[0] = True
    funciones_objetivo = []
    for i in range(len(solucion)):
        for j in range(len(solucion[i])):
            a = solucion[i][j]
            if visitados[a] == False:
                visitados[a] = True
            else:
                visitados[a] = False
        funcion_objetivo_vehiculo = funcion_objetivo_vehiculo1([0] + solucion[i], demandas, matriz_dist, velocidad[i,2])
        funciones_objetivo.append(funcion_objetivo_vehiculo)
    funcion_objetivo = sum(funciones_objetivo)
    if (False  in visitados) == True :
        funcion_objetivo += cota*penalizacion*len(solucion)
    return solucion, funcion_objetivo

def penalizacion_capacidad(solucion,funcion_objetivo,cota,penalizacion,capacidades,demandas):
    capacidad = [True]*len(solucion)
    funciones_objetivo = []
    for i in range(len(solucion)):
        for j in range(len(solucion[i])):
            capacidades[i] -= demandas[solucion[i][j]]
        if capacidades[i]<0:
            capacidad[i] = False
    if (False  in capacidad) == True :
        funcion_objetivo += cota*penalizacion*len(solucion)
    return solucion,funcion_objetivo

def actualizar_poblacion(x,y,hijo1,hijo2,funcion_hijo1,funcion_hijo2,posicion_mama,posicion_papa):
    x[posicion_papa] = hijo1
    x[posicion_mama] = hijo2
    y[posicion_papa] = funcion_hijo1
    y[posicion_mama] = funcion_hijo2
    return x,y





