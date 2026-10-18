import random
import time
from models import Registro, siguiente_primo_rehash
from tabla_hash_encadenamiento import TablaHashEncadenamiento
from tabla_hash_lineal import TablaHashLineal
from tabla_hash_cuadratica import TablaHashCuadratica
from tabla_Hash_Doble import TablaHashDoble


def crear_tabla(estrategia: str):
    if estrategia == "Encadenamiento":
        return TablaHashEncadenamiento()
    elif estrategia == "Lineal":
        return TablaHashLineal()
    elif estrategia == "Cuadrático":
        return TablaHashCuadratica()
    else:
        return TablaHashDoble()


def calcular_rehashings(capacidad_final: int) -> int:
    # Todas las tablas inician en 11 y crecen al siguiente primo >= 2m + 1
    rehashings = 0
    capacidad = 11
    while capacidad < capacidad_final:
        capacidad = siguiente_primo_rehash(capacidad)
        rehashings += 1
    return rehashings


def contar_sondeos(claves: list[int], m: int, estrategia: str) -> int:
    sondeos = 0


    if estrategia == "Encadenamiento":
        nodos_por_indice = [0] * m
        for codigo in claves:
            indice = codigo % m
            nodos_por_indice[indice] += 1
            sondeos += nodos_por_indice[indice]
        return sondeos

    ocupado = [False] * m
    for codigo in claves:
        h1 = codigo % m
        h2 = 1 + (codigo % 10)

        for j in range(m):
            sondeos += 1
            if estrategia == "Lineal":
                indice = (h1 + j) % m
            elif estrategia == "Cuadrático":
                indice = (h1 + j**2) % m
            else:
                indice = (h1 + j * h2) % m

            if not ocupado[indice]:
                ocupado[indice] = True
                break

    return sondeos


def ejecutar_experimento() -> None:
    generador = random.Random(2026)
    tamanos: list[int] = [100, 1000, 10000]
    repeticiones: int = 5
    estrategias: list[str] = ["Encadenamiento", "Lineal", "Cuadrático", "Doble hash"]

    print("=" * 112)
    print(f"{'Estrategia':<15} | {'n':>6} | {'Inserción(ms)':>13} | {'Búsq. +(ms)':>11} | "
          f"{'Búsq. -(ms)':>11} | {'Elimin.(ms)':>11} | {'Sondeos':>9} | {'Rehash':>6} | {'Cap. m':>6} | {'F.Carga':>7}")
    print("=" * 112)

    for n in tamanos:
        # 1. Generamos los datos para las 5 repeticiones antes de medir tiempos
        # Las 4 tablas reciben exactamente las mismas claves y en el mismo orden
        lotes_insertar: list[list[Registro]] = []
        lotes_busq_exitosa: list[list[int]] = []
        lotes_busq_fallida: list[list[int]] = []
        lotes_eliminar: list[list[int]] = []

        for _ in range(repeticiones):
            # Claves existentes (del 1 al 499,999) y ausentes (del 500,000 al 999,999)
            claves_ex = generador.sample(range(1, 500000), n)
            claves_fa = generador.sample(range(500000, 1000000), n)

            registros = [Registro(cod, f"Producto_{cod}") for cod in claves_ex]
            lotes_insertar.append(registros)

            copia_buscar = list(claves_ex)
            generador.shuffle(copia_buscar)
            lotes_busq_exitosa.append(copia_buscar)

            lotes_busq_fallida.append(claves_fa)

            copia_eliminar = list(claves_ex)
            generador.shuffle(copia_eliminar)
            lotes_eliminar.append(copia_eliminar)

        # 2. Evaluamos el tiempo de cada estrategia con las 5 repeticiones
        for nombre in estrategias:
            t_ins: float = 0.0
            t_bex: float = 0.0
            t_bfa: float = 0.0
            t_eli: float = 0.0
            cap_final: int = 11
            fc_final: float = 0.0

            for r in range(repeticiones):
                tabla = crear_tabla(nombre)

                # Cronometrar Inserción
                inicio = time.perf_counter()
                for reg in lotes_insertar[r]:
                    tabla.insertar(reg)
                t_ins += (time.perf_counter() - inicio) * 1000

                # Guardamos capacidad y factor de carga con los N elementos activos
                cap_final = tabla.capacidad
                fc_final = tabla.factor_carga()

                # Cronometrar Búsqueda Exitosa 
                inicio = time.perf_counter()
                for cod in lotes_busq_exitosa[r]:
                    tabla.buscar(cod)
                t_bex += (time.perf_counter() - inicio) * 1000

                # Cronometrar Búsqueda Fallida 
                inicio = time.perf_counter()
                for cod in lotes_busq_fallida[r]:
                    tabla.buscar(cod)
                t_bfa += (time.perf_counter() - inicio) * 1000

                # Cronometrar Eliminación
                inicio = time.perf_counter()
                for cod in lotes_eliminar[r]:
                    tabla.eliminar(cod)
                t_eli += (time.perf_counter() - inicio) * 1000

            rehashings = calcular_rehashings(cap_final)
            sondeos = contar_sondeos(lotes_busq_exitosa[0], cap_final, nombre)

            # Imprimimos el promedio de las 5 repeticiones
            print(f"{nombre:<15} | {n:>6} | {t_ins/repeticiones:>13.4f} | {t_bex/repeticiones:>11.4f} | "
                  f"{t_bfa/repeticiones:>11.4f} | {t_eli/repeticiones:>11.4f} | "
                  f"{sondeos:>9} | {rehashings:>6} | {cap_final:>6} | {fc_final:>7.4f}")

        print("-" * 112)


if __name__ == "__main__":
    ejecutar_experimento()