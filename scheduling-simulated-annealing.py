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
        tot_cr = tot_cr + max(df['FL'][i] - inicio, 0) * df['CR'][i]
        tot_cp = tot_cp + max(inicio - df['FL'][i], 0) * df['CP'][i]
    tot_cost = tot_cost + tot_cr + tot_cp
    return tot_cost


def swap(x, y):
    x, y = y, x
    return x, y


def prob_accept(f0, fs, t):
    if fs < f0:
        prob = 1
    else:
        prob = np.exp((-abs(f0 - fs)) / t)

    return prob


def update_temp(t, r):
    temp = r * t

    return temp

def swap_tasks(solucion):
    vecindad = []
    for i in range(len(solucion) - 1):
        vm = solucion[:]
        vm[i], vm[i + 1] = swap(solucion[i], solucion[i + 1])
        vecindad.append(vm)

    return vecindad
np.random.seed(0)
iteraciones = 0
max_iter = 50
max_iter_temp = 3
temp_iter = 0
solucion = [i for i in range(len(df))]
f0 = cost(solucion, df)
temp = f0 * np.random.random(1)
sol_final = solucion
z = f0
len_vecindad = 2
while iteraciones < max_iter:

    vecindad = []
    for i in range(len(solucion) - 1):
        vm = solucion[:]
        vm[i], vm[i + 1] = swap(solucion[i], solucion[i + 1])
        vecindad.append(vm)

    # costos vecindad
    costos_sol = []
    for i in vecindad:
        costos_sol.append(cost(i, df))

    random = np.random.random(1)
    index = int(np.round(random * (len(vecindad) - 1))) #eleccion en vecindad

    costos_ev = cost(vecindad[index], df)
    prob = prob_accept(f0, costos_ev, temp)

    j = 0
    while j < len_vecindad:
        if costos_ev < z:
            z = costos_ev
            solucion = vecindad[index]
            sol_final = solucion

        if random < prob:
            temp_iter = temp_iter + 1
            solucion = vecindad[index]
            f0 = costos_ev
            break
        else:
            vecindad.remove(vecindad[index])
            costos_sol.remove(costos_sol[index])
            j = j + 1
            random = np.random.random(1)
            index = int(np.round(random * (len(vecindad) - 1)))  # eleccion en vecindad
            costos_ev = cost(vecindad[index], df)
            prob = prob_accept(f0, costos_ev, temp)

    if j == len_vecindad:
        break

    if temp_iter >= max_iter_temp:
        temp = update_temp(random, temp)
        temp_iter = 0
    iteraciones = iteraciones + 1

print(iteraciones, z, sol_final, f0)
print(datetime.datetime.now())
