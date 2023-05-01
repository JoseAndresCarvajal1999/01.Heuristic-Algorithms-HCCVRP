from CotaInferior import *
from AlgoritmosBusquedaLocal import *
from Evolutivos import *
from AlgortimosBusquedaAleatoria import*
import time
import random
def Hibrido(k):
    Start_time = time.time()
    file_datos = 'hfccvrp{}.vrp'.format(k+1)
    archivo_datos   = open(file_datos)
    line_datos = archivo_datos.readline().split()
    n, m            = int(line_datos[0]), int(line_datos[1])
    nodos       = []
    corsx       = []
    corsy       = []
    demandas    = []
    tipos       = []
    cantidades  = []
    capacidades = []
    velocidades = []
    visitados   = [False] * (n+1)
    B = []
    Poblacion_inicial = 10
    penalizacion = 1
    numero_de_generaciones = 30
    respuesta = []
    fo = []

    for i in range(m):
        line = archivo_datos.readline().replace(',', '.').split()
        tipo, cantidad, capacidad, velocidad = int(line[0]), int(line[1]), int(line[2]), float(line[3])
        tipos.append(tipo)
        cantidades.append(cantidad)
        capacidades.append(capacidad)
        velocidades.append(velocidad)

    for i in range(n+1):
        line = archivo_datos.readline().replace(',', '.').split()
        nodo, corx, cory, demanda = int(line[0]), int(line[1]), int(line[2]), float(line[3])
        nodos.append(nodo)
        corsx.append(corx)
        corsy.append(cory)
        demandas.append(demanda)

    numero_vehiculos = sum(cantidades)
    visitados[0] = True
    matriz_dist= matriz_distancia(corsx,corsy,n)
    matriz = np.transpose(llenar_matriz(tipos,cantidades,capacidades,velocidades,m))
    vehiculos = replicar_vehiculo(matriz)
    soluciones = []
    solucion_inicial =[]
    funciones_objetivo_soluciones_iniciales = []
    visitados_soluciones_iniciales = []
    x = []
    y = []
    z = []
    c = 0
    k = 0
    cota = cotaInferior(n, matriz_dist, demandas, vehiculos[0][2])
    # print(cota)
    for j in range(Poblacion_inicial):
        for i in range(len(vehiculos)):
            resultado = busqueda_soluciones_aleatorias(vehiculos[i], matriz_dist, visitados, demandas)
            while (0 in resultado[0]) == True:
                resultado[0].remove(0)
            nodos_recorridos = resultado[0]
            funcion_objetivo = funcion_objetivo_vehiculo1([0] + nodos_recorridos, demandas, matriz_dist, vehiculos[i, 2])
            solucion_inicial.append(nodos_recorridos)
            funciones_objetivo_soluciones_iniciales.append(funcion_objetivo)
        x.append(solucion_inicial)
        y .append(sum(funciones_objetivo_soluciones_iniciales))
        z.append(visitados)
        solucion_inicial = []
        funciones_objetivo_soluciones_iniciales = []
        visitados = [False] * (n + 1)
    for i in range(len(x)-1):
        if (False  in z[i]) == True :
            # print(x[i]) #Soluciones
            # print('hola ' + str(y[i])) #Funciones objetivo
            # print(z[i]) #Visitados
            y[i] += cota*penalizacion*m #Sumar la cota a soluciones no factibles

    mejor_solucion_funcion_objetivo = min(y)
    l = y.index(mejor_solucion_funcion_objetivo)
    mejor_solucion = x[l]
    c = 0
    #------------------------------- EXPLORACION --------------------------------------------------------------------
    while c < numero_de_generaciones:
        #----------------- Seleccion por torneo -------------------------------------------------------------------------
        torneo = seleccion_por_torneo(Poblacion_inicial,x,y)
        #----------------- Cruce ---------------------------------------------------------------------------------------
        hijo1,hijo2 = cruce(torneo[0],torneo[2])
        #---------------- Penalizacion (todos lo nodos visitados una sola vez) -----------------------------------------
        pv1 = penalizacion_visitados(hijo1,n,demandas,matriz_dist,vehiculos,cota,penalizacion)
        pv2 = penalizacion_visitados(hijo1,n,demandas,matriz_dist,vehiculos,cota,penalizacion)
        #---------------- Penalizacion (capacidad vehiculos) -----------------------------------------------------------__
        # print(vehiculos[:,1])
        pc1 = penalizacion_capacidad(hijo1,pv1[1],cota,penalizacion,vehiculos[:,1],demandas)
        pc2 = penalizacion_capacidad(hijo2,pv2[1],cota,penalizacion,vehiculos[:,1],demandas)
        #---------------- Acrualizar poblacion --------------------------------------------------------------------------
        x,y = actualizar_poblacion(x,y,hijo1,hijo2,pc1[1],pc2[1],torneo[4],torneo[5])
        mejor_solucion_funcion_objetivo = min(y)
        l = y.index(mejor_solucion_funcion_objetivo)
        mejor_solucion = x[l]
        # print(c)
        c += 1
    #------------------------------- EXOPLOTACION --------------------------------------------------------------------
    d = 0
    valores_nueva_solucion = []
    nodos_finales = []
    for i in range(len(mejor_solucion)):
        s = [] in mejor_solucion
        if s == True:
            mejor_solucion.remove([])
            d = d + 1
    for i in range(len(mejor_solucion)-d):
        nodos_recorridos,solucion_min = generador_de_vecinos(mejor_solucion[i],demandas,matriz_dist,vehiculos[i,2])
        valores_nueva_solucion.append(solucion_min)  # Valores de la nueva solucion
        nodos_finales.append(nodos_recorridos)
    delta = porcentaje_de_deviacion(sum(valores_nueva_solucion),cota)
    for i in range(len(valores_nueva_solucion)):
        A = [vehiculos[i,0],len(nodos_finales[i]),nodos_finales[i]]
        respuesta.append(A)

    # print(nodos_finales)
    Finish_time = time.time()
    Tiempo = Finish_time - Start_time
    # print(delta)
    return respuesta

def print_routes(i):
    routes = Hibrido(i)
    file = open('hfccvrp{}.sol'.format(i), 'w')
    for route in routes:
        string = str(int(route[0])) + ' ' + str(int(route[1]))
        for node in route[2]:
            string += ' ' + str(node)
        file.write(string + '\n')


for i in range(20):
    print_routes(i + 1)
