# tsp_secuencial.py
import itertools
import time
import math
import random

def distancia_euclidiana(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def calcular_distancia_ruta(cities, ruta):
    total = 0.0
    n = len(ruta)
    for i in range(n):
        total += distancia_euclidiana(cities[ruta[i]], cities[ruta[(i + 1) % n]])
    return total

def tsp_fuerza_bruta_secuencial(cities):
    n = len(cities)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0], 0.0

    ciudad_inicial = 0
    otras_ciudades = list(range(1, n))
    mejor_distancia = float('inf')
    mejor_ruta = None

    for perm in itertools.permutations(otras_ciudades):
        ruta = [ciudad_inicial] + list(perm)
        dist = calcular_distancia_ruta(cities, ruta)
        if dist < mejor_distancia:
            mejor_distancia = dist
            mejor_ruta = ruta

    return mejor_ruta, mejor_distancia

def generar_ciudades_fijas():
    # Puedes cambiar esta lista para tus pruebas
    return [[0, 0], [1, 2], [3, 1], [5, 4], [2, 6], [4, 3], [6, 7], [8, 2]]

if __name__ == "__main__":
    print("=== TSP - Algoritmo Secuencial (Fuerza Bruta) ===")
    cities = generar_ciudades_fijas()
    print(f"Ciudades (N={len(cities)}): {cities}")

    inicio = time.perf_counter()
    ruta, distancia = tsp_fuerza_bruta_secuencial(cities)
    fin = time.perf_counter()

    print(f"Mejor ruta: {ruta}")
    print(f"Distancia total: {distancia:.4f}")
    print(f"Tiempo de ejecución: {fin - inicio:.4f} segundos")