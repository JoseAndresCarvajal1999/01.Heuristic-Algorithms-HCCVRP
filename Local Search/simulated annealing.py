from AlgoritmoConstructivo import *
import matplotlib.pyplot as plt
import time
from AlgoritmosBusquedaLocal import *
from CotaInferior import *
import random
def recocido_simul(k):
    start_time = time.time()
    file_solucion = 'hfccvrp{}.csol'.format(k)
    file_datos = 'hfccvrp{}.vrp'.format(k)
    archivo_solucion = open(file_solucion)
    archivo_datos   = open(file_datos)
    line_datos = archivo_datos.readline().split()
    line_solucion = archivo_solucion.readline().split()
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
    colors = "bgrcmykwbgrcmykw"
    matriz_dist= matriz_distancia(corsx,corsy,n)
    matriz = np.transpose(llenar_matriz(tipos,cantidades,capacidades,velocidades,m))
    vehiculos = replicar_vehiculo(matriz)
    solucion_inicial = []
    valores_nueva_solucion = []
    nodos_finales = []
    cota = cotaInferior(n, matriz_dist, demandas, vehiculos[0][2])
    c = 0
    for i in range(len(vehiculos)):
        resultado = nodos_a_recorrer(vehiculos[i], matriz_dist, visitados, demandas)
        nodo_recorridos = resultado[0]
        solucion_inicial.append(nodo_recorridos) #Solucion inicial
        s = [] in solucion_inicial
        if s == True:
            solucion_inicial.remove([])
            c=c+1
    for i in range(numero_vehiculos-c):
        nodos_recorridos,solucion_min = recocido_simulado(solucion_inicial[i],demandas,matriz_dist,vehiculos[i,2])
        valores_nueva_solucion.append(solucion_min)  # Valores de la nueva solucion
        nodos_finales.append(nodos_recorridos)
        x = []
        y = []
        A = [vehiculos[i, 0], len(nodos_finales[i]), nodos_finales[i]]
        for j in nodos_finales[i]:
            x.append(corsx[j])
            y.append(corsy[j])
        #plt.plot(x, y, '-ok', color=colors[i % len(colors)])
        B.append(A)
    # plt.xlabel('x - axis')
    # plt.ylabel('y - axis')
    # plt.title('Ejemplo' + ' ' + str(k) + ' '  +'recocido simulado')
    # plt.show()
    funcion_objetivo = sum(valores_nueva_solucion)
    print(funcion_objetivo)
    finish_time = time.time()
    Time = finish_time-start_time
    # delta = ((funcion_objetivo - cota) / cota) * 100
    # print(abs(delta))
    # print(Time)
    return B

def print_routes(i):
    routes = recocido_simul(i)
    file   = open('hfccvrp{}.rsol'.format(i), 'w')
    for route in routes:
        string = str(int(route[0])) + ' ' + str(int(route[1]))
        for node in route[2]:
            string += ' ' + str(node)
        file.write(string + '\n')

for i in range(21):
   print_routes(i+1)






     









































             
             
             
             
             





