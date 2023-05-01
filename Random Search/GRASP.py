from AlgortimosBusquedaAleatoria import *
from AlgoritmoConstructivo import *
from AlgoritmosBusquedaLocal import *
import matplotlib.pyplot as plt
import time
# def Graps(h):
def Graps(h):
    star_time = time.time()
    a = 0.8
    maximo_iteraciones = 50
    file = 'hfccvrp{}.vrp'.format(h)
    archivo = open(file)
    line = archivo.readline().split()
    n, m = int(line[0]), int(line[1])
    nodos = []
    corsx = []
    corsy = []
    demandas = []
    tipos = []
    cantidades = []
    capacidades = []
    velocidades = []
    visitados = [False] * (n + 1)
    respuesta = []
    fo = []


    for i in range(m):
        line = archivo.readline().replace(',', '.').split()
        tipo, cantidad, capacidad, velocidad = int(line[0]), int(line[1]), int(line[2]), float(line[3])
        tipos.append(tipo)
        cantidades.append(cantidad)
        capacidades.append(capacidad)
        velocidades.append(velocidad)

    for i in range(n + 1):
        line = archivo.readline().replace(',', '.').split()
        nodo, corx, cory, demanda = int(line[0]), int(line[1]), int(line[2]), float(line[3])
        nodos.append(nodo)
        corsx.append(corx)
        corsy.append(cory)
        demandas.append(demanda)

    matriz = llenar_matriz(tipos, cantidades, capacidades, velocidades, m)
    A = np.transpose(matriz)
    vehiculos = replicar_vehiculo(A)
    matriz_dist = matriz_distancia(corsx, corsy, n)
    visitados[0] = False
    solucion_inicial = []
    soluciones_factibles = []
    funciones_objetivo_soluciones_iniciales = [] #no factibles
    funciones__objetivo_soluciones_factibles = []
    lista_restringida_de_elementos = []
    lista_restringida_funciones_objetivo = []
    c = 0
    k = 0
    x = []
    #-------------------- Soluciones Factibles ---------------------------------------------------------
    for j in range(2*n):
        for i in range(len(vehiculos)):
            resultado = busqueda_soluciones_aleatorias(vehiculos[i], matriz_dist, visitados, demandas)
            while (0 in resultado[0]) == True:
                resultado[0].remove(0)
            nodos_recorridos = resultado[0]
            funcion_objetivo = funcion_objetivo_vehiculo1(nodos_recorridos,demandas,matriz_dist,vehiculos[i,2])
            solucion_inicial.append(nodos_recorridos)
            funciones_objetivo_soluciones_iniciales.append(funcion_objetivo)
        for i in range(len(visitados)-1):
            if visitados[i] == False:
                k=k+1
        if k == 0:
            soluciones_factibles.append(solucion_inicial)
            funciones__objetivo_soluciones_factibles.append(sum(funciones_objetivo_soluciones_iniciales))
            c = c+1 #Numero de soluciones factibles
        x.append(solucion_inicial)
        solucion_inicial = []
        funciones_objetivo_soluciones_iniciales = []
        visitados = [False] * (n + 1)
    print(x)
    # --------------------- Lista Restringida de candidatos --------------------------------------------
    if funciones__objetivo_soluciones_factibles == []:
        print('vuelva a intentar')
    else:
        Cmax = max(funciones__objetivo_soluciones_factibles)
        Cmin = min(funciones__objetivo_soluciones_factibles)
        for i in range(len(soluciones_factibles)):
            if funciones__objetivo_soluciones_factibles[i] <= a*(Cmax-Cmin) + Cmin:
                lista_restringida_de_elementos.append(soluciones_factibles[i])
                lista_restringida_funciones_objetivo.append(funciones__objetivo_soluciones_factibles[i])
        #----------------------Busqueda local-------------------------------------------------------------
        valores_nueva_solucion = []
        nodos_finales = []
        funciones_objetivo = []
        cota = max(lista_restringida_funciones_objetivo)
        moco = cota
        solucion_final = []
        c = 0
        for o in range(maximo_iteraciones):
            y = random.randint(0, len(lista_restringida_de_elementos)-1)
            for j in range(len(vehiculos)-1):
                s = [] in lista_restringida_de_elementos[y]
                if s == True:
                    lista_restringida_de_elementos[y].remove([])
                    c = c + 1
            for i1 in range(len(vehiculos)-c):
                solucion_a_mejorar = lista_restringida_de_elementos[y][i1-1] #i1-1
                s, solucion = recocido_simulado(solucion_a_mejorar, demandas, matriz_dist, vehiculos[i1, 2])
                valores_nueva_solucion.append(solucion)
                nodos_finales.append(s)
            if sum(valores_nueva_solucion) <= cota:
                funciones_objetivo = valores_nueva_solucion
                cota = sum(valores_nueva_solucion)
                solucion_final = nodos_finales
            valores_nueva_solucion = []
            nodos_finales = []
            c = 0
        #-------------- Respuesta ---------------------------------------------------
        for y in range(len(solucion_final)):
            A = [vehiculos[y, 0], len(solucion_final[y]), solucion_final[y], funciones_objetivo[y]]
            respuesta.append(A)
        B = cota
        fo.append(B)
        # print('-------'+ ' '+ str(h) + ' ' + '-----------------')
        # print(solucion_final)
        print(cota)
        # print(moco)
        finish_time = time.time()
        Time = finish_time-star_time
        #print(Time)

    return respuesta,fo

def print_routes(i):
    routes,funcion_objetivo = Graps(i)
    file   = open('hfccvrp{}.sol'.format(i), 'w')
    for route in routes:
        string = str(int(route[0])) + ' ' + str(int(route[1]))
        for node in route[2]:
            string += ' ' + str(node)
        string += ' ' + str(float(route[3]))
        file.write(string + '\n')
    string += str(float(sum(funcion_objetivo)))
    fo = str(float(sum(funcion_objetivo)))
    file.write(fo + '\n')


for i in range(21):
   print_routes(i+1)


# colors = "bgrcmykwbgrcmykw"
# for m in range(len(vehiculos)):
#     x = []
#     y = []
#     for l in solucion_final[m]:
#         x.append(corsx[l])
#         y.append(corsy[l])
#     plt.plot(x, y, '-ok', color=colors[m % len(colors)])
# plt.xlabel('x - axis')
# plt.ylabel('y - axis')
# plt.title('Ejemplo' + ' ' + str(1) + ' '  +'recocido simulado')
# plt.show()


