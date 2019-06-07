import numpy as np
import pandas as pd
import datetime

print(datetime.datetime.now())
df = pd.read_excel('scheduling.xlsx')

def cost(solucion, df):
    inicio = 0
    tot_cr = 0
    tot_cp = 0
    tot_cost = 0
    for i in solucion:
        inicio = inicio + df['TP'][i]
        tot_cr = tot_cr + max(df['FL'][i]-inicio,0)*df['CR'][i]
        tot_cp = tot_cp + max(inicio - df['FL'][i],0)*df['CP'][i]
    tot_cost = tot_cost + tot_cr + tot_cp
    return tot_cost

def swap(x,y):
    x, y = y, x
    return x, y

iteraciones = 0
max_iter = 10
tabu_list = []
solucion = [i for i in range(len(df))]
tabu_len = 3
z = 100000000000000000000
sol_final = []
while iteraciones < max_iter:
    # heuristica para armar soluciones
    vecindad = []
    for i in range(len(solucion) - 1):
        vm = solucion[:]
        vm[i], vm[i + 1] = swap(solucion[i], solucion[i + 1])
        vecindad.append(vm)

    # costos vecindad
    costos_sol = []
    for i in vecindad:
        costos_sol.append(cost(i, df))
        #print(i,cost(i,df),tabu_list,solucion)

    tabu_list.append(solucion)
    j = 0
    while j < tabu_len:
        min_index = np.argmin(costos_sol)
        if vecindad[min_index] not in tabu_list:
            solucion = vecindad[min_index]
            if costos_sol[min_index] < z:
                sol_final = solucion[:]
                z = costos_sol[min_index]
            break
        else:
            vecindad.remove(vecindad[min_index])
            costos_sol.remove(costos_sol[min_index])
            j = j + 1
    if j == tabu_len:
        break
    if len(tabu_list) == tabu_len :
        # actualizar tabu list
        tabu_list = tabu_list[1:]
    iteraciones = iteraciones + 1
print(z, sol_final)
print(datetime.datetime.now())