# tsp_comparacion.py
import itertools
import time
import math
import os
from multiprocessing import Pool
import random

# --- Funciones comunes ---
def distancia(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def distancia_ruta(cities, ruta):
    return sum(distancia(cities[ruta[i]], cities[ruta[(i+1) % len(ruta)]]) for i in range(len(ruta)))

# --- Secuencial ---
def tsp_sec(cities):
    n = len(cities)
    if n <= 1:
        return list(range(n)), 0.0
    best_d = float('inf')
    best_r = None
    for perm in itertools.permutations(range(1, n)):
        r = [0] + list(perm)
        d = distancia_ruta(cities, r)
        if d < best_d:
            best_d, best_r = d, r
    return best_r, best_d

# --- Paralelo ---
def _eval(args):
    c, p = args
    r = [0] + list(p)
    return r, distancia_ruta(c, r)

def tsp_par(cities, procs=None):
    n = len(cities)
    if n <= 1:
        return tsp_sec(cities)
    if procs is None:
        procs = os.cpu_count()
    perms = list(itertools.permutations(range(1, n)))
    with Pool(procs) as pool:
        res = pool.map(_eval, [(cities, p) for p in perms])
    return min(res, key=lambda x: x[1])

# --- Utilidades ---
def generar_ciudades(n, seed=42):
    random.seed(seed)
    return [[random.randint(0, 100), random.randint(0, 100)] for _ in range(n)]

def medir(func, *args):
    t0 = time.perf_counter()
    r, d = func(*args)
    t1 = time.perf_counter()
    return r, d, t1 - t0

# --- Ejecución ---
if __name__ == "__main__":
    print("=== Comparación: Secuencial vs Paralelo (TSP - Fuerza Bruta) ===\n")
    tamanos = [6, 7, 8]
    procs = os.cpu_count()
    print(f"Hardware: {procs} núcleos lógicos\n")
    print(f"{'N':<4} {'T_sec (s)':<12} {'T_par (s)':<12} {'Speedup':<10} {'Distancia':<10}")
    print("-" * 55)

    for n in tamanos:
        cities = generar_ciudades(n)
        _, d_sec, t_sec = medir(tsp_sec, cities)
        _, d_par, t_par = medir(tsp_par, cities, procs)
        speedup = t_sec / t_par if t_par > 0 else float('inf')
        print(f"{n:<4} {t_sec:<12.4f} {t_par:<12.4f} {speedup:<10.2f} {d_sec:<10.2f}")

