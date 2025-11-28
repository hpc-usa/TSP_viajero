# tsp_paralelo.py
import itertools
import time
import math
import os
from multiprocessing import Pool

def distancia_euclidiana(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def calcular_distancia_ruta(cities, ruta):
    total = 0.0
    n = len(ruta)
    for i in range(n):
        total += distancia_euclidiana(cities[ruta[i]], cities[ruta[(i + 1) % n]])
    return total

def evaluar_ruta(args):
    cities, perm = args
    ruta = [0] + list(perm)
    dist = calcular_distancia_ruta(cities, ruta)
    return ruta, dist

def tsp_fuerza_bruta_paralelo(cities, num_procesos=None):
    n = len(cities)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0], 0.0

    if num_procesos is None:
        num_procesos = os.cpu_count()

    otras = list(range(1, n))
    permutaciones = list(itertools.permutations(otras))
    tareas = [(cities, p) for p in permutaciones]

    with Pool(processes=num_procesos) as pool:
        resultados = pool.map(evaluar_ruta, tareas)

    return min(resultados, key=lambda x: x[1])

def generar_ciudades_fijas():
    return [[0, 0], [1, 2], [3, 1], [5, 4], [2, 6], [4, 3], [6, 7], [8, 2]]

if __name__ == "__main__":
    print("=== TSP - Algoritmo Paralelo (Fuerza Bruta) ===")
    cities = generar_ciudades_fijas()
    print(f"Ciudades (N={len(cities)}): {cities}")

    inicio = time.perf_counter()
    ruta, distancia = tsp_fuerza_bruta_paralelo(cities)
    fin = time.perf_counter()

    print(f"Mejor ruta: {ruta}")
    print(f"Distancia total: {distancia:.4f}")
    print(f"Tiempo de ejecución: {fin - inicio:.4f} segundos")
    print(f"Núcleos usados: {os.cpu_count()}")