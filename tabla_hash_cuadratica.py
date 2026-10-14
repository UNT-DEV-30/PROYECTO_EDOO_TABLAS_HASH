from models import Registro, BORRADO

class TablaHashCuadratica:
    def __init__(self, capacidad: int):
        self.__arreglo: list[Registro] = [None] * capacidad
        self.__capacidad: int = capacidad

    def calcular_posicion(self, posicion_original: int, intento: int) -> int:
        return (posicion_original + intento**2) % self.__capacidad

    def insertar(self, registro: Registro) -> None:
        posicion_original = registro.codigo % self.__capacidad
        intento = 0

        posicion = self.calcular_posicion(posicion_original, intento)

