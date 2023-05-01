import numpy as np
import math as mt

def matriz_distancia(corx, cory,n):
    A = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        for j in range(n + 1):
            distancia = mt.sqrt((corx[i] - corx[j]) ** 2 + (cory[i] - cory[j]) ** 2)
            if i < j:
                A[i][j] = distancia
    B = A + np.transpose(A)
    return B

# Llena la matriz con los parametros de los vehiculos
def llenar_matriz(t, k, c, v, m):
    A = np.zeros((4,m))
    for i in range(m):
        A[0][i] = t[i]
        A[1][i] = k[i]
        A[2][i] = c[i]
        A[3][i] = v[i]
    return A

# Replica cada vehiculo
def replicar_vehiculo(A):
    B = []
    for i in range(len(A)):
        cantidad_vehiculos = int(A[i, 1])
        for j in range(cantidad_vehiculos):
            line = np.delete(A[i], 1)
            B.append(line)
    return np.array(B)

def mayor_distancia_no_recorrida(posicion, capacidad, matriz_distancia, nodos_visitados, demandas):
    fila = matriz_distancia[posicion]
    mayores = sorted(fila, reverse=True)
    for i in range(len(mayores)):
        mayor = mayores[i]
        for j in range(len(mayores)):
            if fila[j] == mayor and nodos_visitados[j] == False and demandas[j] <= capacidad:
                nodos_visitados[j] = True
                return mayor, j, nodos_visitados, demandas[j]

def menor_distancia_no_recorrida(posicion, capacidad, matriz_distancia, nodos_visitados, demandas):
    fila = matriz_distancia[posicion]
    menores = sorted(fila)
    for i in range(len(menores)):
        if demandas[i] <= capacidad:
            menor = menores[i]
            for j in range(len(menores)):
                if fila[j] == menor and nodos_visitados[j] == False and demandas[j] <= capacidad:
                    nodos_visitados[j] = True
                    return menor, j, nodos_visitados, demandas[j]

def nodos_a_recorrer(vehiculo, matriz_distacia, nodos_visitados, demandas):
    capacidad = vehiculo[1]
    nodo = 0
    nodos_a_recorrer = []
    capacidad_nodo  = []
    vector_distancia_recorrida = []
    distancia_recorrida = 0;
    primero = True

    while capacidad != 0:
        resultado = None
        if primero == True:
            resultado = mayor_distancia_no_recorrida(nodo, capacidad, matriz_distacia, nodos_visitados, demandas)
            primero = False
        else:
            resultado = menor_distancia_no_recorrida(nodo, capacidad, matriz_distacia, nodos_visitados, demandas)

        if resultado is None:
            break
        mayor, posicion, nodos_visitados, demanda = resultado
        capacidad -= demanda
        nodo = posicion
        nodos_a_recorrer.append(posicion)
        vector_distancia_recorrida.append(mayor)
        distancia_recorrida += mayor

    return nodos_a_recorrer, distancia_recorrida, nodos_visitados,vector_distancia_recorrida

