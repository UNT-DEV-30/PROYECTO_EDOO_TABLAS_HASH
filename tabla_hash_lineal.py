from typing import Optional
from models import Registro, BORRADO, es_primo


class TablaHashLineal:
    UMBRAL = 0.65

    def __init__(self, capacidad: int = 11) -> None:
        self.__capacidad: int = capacidad
        self.__tabla: list[Optional[Registro] | str | None] = [None] * self.__capacidad
        self.__total: int = 0

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    def __hash(self, codigo: int) -> int:
        return codigo % self.__capacidad

    def insertar(self, reg: Registro) -> None:
        posicion = self.__hash(reg.codigo)
        primer_borrado = -1

        for j in range(self.__capacidad):
            indice = (posicion + j) % self.__capacidad
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
                self.__tabla[indice] = reg
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
        posicion = self.__hash(codigo)

        for j in range(self.__capacidad):
            indice = (posicion + j) % self.__capacidad
            actual = self.__tabla[indice]

            if actual is None:
                return None

            if actual != BORRADO and actual.codigo == codigo:
                return actual

        return None

    def eliminar(self, codigo: int) -> bool:
        posicion = self.__hash(codigo)

        for j in range(self.__capacidad):
            indice = (posicion + j) % self.__capacidad
            actual = self.__tabla[indice]

            if actual is None:
                return False

            if actual != BORRADO and actual.codigo == codigo:
                self.__tabla[indice] = BORRADO
                self.__total -= 1
                return True

        return False

    def mostrar(self) -> None:
        print(f"\nTabla hash lineal (capacidad: {self.__capacidad})")

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

        nueva_capacidad = self.__capacidad * 2 + 1

        while not es_primo(nueva_capacidad):
            nueva_capacidad += 1

        self.__capacidad = nueva_capacidad
        self.__tabla = [None] * self.__capacidad
        self.__total = 0

        for reg in registros:
            self.insertar(reg)