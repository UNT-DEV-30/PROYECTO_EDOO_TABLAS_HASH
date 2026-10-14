from typing import Optional
from registro import Registro, BORRADO


class TablaHashLineal:
    UMBRAL = 0.65

    def __init__(self, capacidad: int = 11) -> None:
        self.capacidad = capacidad
        self.tabla: list[Optional[Registro] | str | None] = [None] * capacidad
        self.total = 0

    def _hash(self, codigo: int) -> int:
        return codigo % self.capacidad

    def insertar(self, reg: Registro) -> None:
        # Actualizar si el código ya existe.
        posicion = self._hash(reg.codigo)
        primer_borrado = -1

        for j in range(self.capacidad):
            indice = (posicion + j) % self.capacidad
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
                self.tabla[indice] = reg
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
        posicion = self._hash(codigo)

        for j in range(self.capacidad):
            indice = (posicion + j) % self.capacidad
            actual = self.tabla[indice]

            if actual is None:
                return None

            if actual != BORRADO and actual.codigo == codigo:
                return actual

        return None

    def eliminar(self, codigo: int) -> bool:
        posicion = self._hash(codigo)

        for j in range(self.capacidad):
            indice = (posicion + j) % self.capacidad
            actual = self.tabla[indice]

            if actual is None:
                return False

            if actual != BORRADO and actual.codigo == codigo:
                self.tabla[indice] = BORRADO
                self.total -= 1
                return True

        return False

    def mostrar(self) -> None:
        print(f"\nTabla hash lineal (capacidad: {self.capacidad})")

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

        nueva_capacidad = self.capacidad * 2 + 1

        while not self._es_primo(nueva_capacidad):
            nueva_capacidad += 1

        self.capacidad = nueva_capacidad
        self.tabla = [None] * self.capacidad
        self.total = 0

        for reg in registros:
            self.insertar(reg)

    @staticmethod
    def _es_primo(numero: int) -> bool:
        if numero < 2:
            return False

        for divisor in range(2, int(numero ** 0.5) + 1):
            if numero % divisor == 0:
                return False

        return True