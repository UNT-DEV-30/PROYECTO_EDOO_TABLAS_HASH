from typing import Optional
from models import Registro, BORRADO, siguiente_primo_rehash

class TablaHashDoble:
    UMBRAL = 0.65

    def __init__(self, capacidad: int = 11) -> None:
        self.capacidad = capacidad
        self.tabla: list[Registro | str | None] = [
            None
        ] * capacidad
        self.total = 0

    def _h1(self, codigo: int) -> int:
        return codigo % self.capacidad

    def _h2(self, codigo: int) -> int:
        return 1 + (codigo % 10)

    def insertar(self, reg: Registro) -> None:
        posicion_base = self._h1(reg.codigo)
        paso = self._h2(reg.codigo)
        primer_borrado = -1

        for j in range(self.capacidad):
            indice = (posicion_base + j * paso) % self.capacidad
            actual = self.tabla[indice]

            if actual is None:
                if primer_borrado != -1:
                    indice = primer_borrado

                self.tabla[indice] = reg
                self.total += 1

                if self.factor_carga() > self.UMBRAL:
                    self.rehashing()
                return

            if actual == BORRADO:
                if primer_borrado == -1:
                    primer_borrado = indice

            elif actual.codigo == reg.codigo:
                actual.nombre = reg.nombre
                return

        if primer_borrado != -1:
            self.tabla[primer_borrado] = reg
            self.total += 1

            if self.factor_carga() > self.UMBRAL:
                self.rehashing()
            return

        self.rehashing()
        self.insertar(reg)

    def buscar(self, codigo: int) -> Optional[Registro]:
        posicion_base = self._h1(codigo)
        paso = self._h2(codigo)

        for j in range(self.capacidad):
            indice = (posicion_base + j * paso) % self.capacidad
            actual = self.tabla[indice]

            if actual is None:
                return None

            if actual != BORRADO and actual.codigo == codigo:
                return actual

        return None

    def eliminar(self, codigo: int) -> bool:
        posicion_base = self._h1(codigo)
        paso = self._h2(codigo)

        for j in range(self.capacidad):
            indice = (posicion_base + j * paso) % self.capacidad
            actual = self.tabla[indice]

            if actual is None:
                return False

            if actual != BORRADO and actual.codigo == codigo:
                self.tabla[indice] = BORRADO
                self.total -= 1
                return True

        return False

    def mostrar(self) -> None:
        print(f"\nTabla hash doble (capacidad: {self.capacidad})")

        for indice, actual in enumerate(self.tabla):
            print(f"[{indice}] -> {actual}")

        print(f"Registros activos: {self.total}")
        print(f"Factor de carga: {self.factor_carga():.2f}")

    def factor_carga(self) -> float:
        return self.total / self.capacidad

    def rehashing(self) -> None:
        registros = [
            actual
            for actual in self.tabla
            if actual is not None and actual != BORRADO
        ]

        # Llama a la función centralizada de tu compañero
        nueva_capacidad = siguiente_primo_rehash(self.capacidad)

        self.capacidad = nueva_capacidad
        self.tabla = [None] * self.capacidad
        self.total = 0

        for reg in registros:
            self.insertar(reg)