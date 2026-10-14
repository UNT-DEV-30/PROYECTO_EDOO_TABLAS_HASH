from typing import Optional
from models import Registro, BORRADO, siguiente_primo_rehash

class TablaHashDoble:
    UMBRAL = 0.65

    def __init__(self, capacidad: int = 11) -> None:
        self.__capacidad = capacidad
        self.__tabla: list[Registro | str | None] = [None] * capacidad
        self.__total = 0

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    def _h1(self, codigo: int) -> int:
        return codigo % self.__capacidad

    def _h2(self, codigo: int) -> int:
        return 1 + (codigo % 10)

    def insertar(self, reg: Registro) -> None:
        posicion_base = self._h1(reg.codigo)
        paso = self._h2(reg.codigo)
        primer_borrado = -1

        for j in range(self.__capacidad):
            indice = (posicion_base + j * paso) % self.__capacidad
            actual = self.__tabla[indice]

            if actual is None:
                if primer_borrado != -1:
                    indice = primer_borrado

                self.__tabla[indice] = reg
                self.__total += 1

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
            self.__tabla[primer_borrado] = reg
            self.__total += 1

            if self.factor_carga() > self.UMBRAL:
                self.rehashing()
            return

        self.rehashing()
        self.insertar(reg)

    def buscar(self, codigo: int) -> Optional[Registro]:
        posicion_base = self._h1(codigo)
        paso = self._h2(codigo)

        for j in range(self.__capacidad):
            indice = (posicion_base + j * paso) % self.__capacidad
            actual = self.__tabla[indice]

            if actual is None:
                return None

            if actual != BORRADO and actual.codigo == codigo:
                return actual

        return None

    def eliminar(self, codigo: int) -> bool:
        posicion_base = self._h1(codigo)
        paso = self._h2(codigo)

        for j in range(self.__capacidad):
            indice = (posicion_base + j * paso) % self.__capacidad
            actual = self.__tabla[indice]

            if actual is None:
                return False

            if actual != BORRADO and actual.codigo == codigo:
                self.__tabla[indice] = BORRADO
                self.__total -= 1
                return True

        return False

    def mostrar(self) -> None:
        print(f"\nTabla hash doble (capacidad: {self.__capacidad})")

        for indice, actual in enumerate(self.__tabla):
            print(f"[{indice}] -> {actual}")

        print(f"Registros activos: {self.__total}")
        print(f"Factor de carga: {self.factor_carga():.2f}")

    def factor_carga(self) -> float:
        return self.__total / self.__capacidad

    def rehashing(self) -> None:
        registros = [
            actual
            for actual in self.__tabla
            if actual is not None and actual != BORRADO
        ]

        nueva_capacidad = siguiente_primo_rehash(self.__capacidad)

        self.__capacidad = nueva_capacidad
        self.__tabla = [None] * self.__capacidad
        self.__total = 0

        for reg in registros:
            self.insertar(reg)