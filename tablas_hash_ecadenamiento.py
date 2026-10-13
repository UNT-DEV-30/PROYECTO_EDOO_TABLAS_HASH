from lista_simple import ListaSimple
from registro import Registro

class TablaHashEncadenamiento:
    def __init__(self, capacidad: int) -> None:
        self.__arreglo: list[Registro] = [None] * capacidad
        self.capacidad = capacidad

    def insertar(self, registro: Registro) -> None:
        posicion = registro.codigo % self.capacidad

        if self.__arreglo[posicion] is None:
            self.__arreglo[posicion] = ListaSimple()

        lista_posicion: ListaSimple = self.__arreglo[posicion]

        if lista_posicion.buscar(registro) is None:
            lista_posicion.insertar_final(registro)
        else:
            return

    def buscar(self, codigo: int) -> Registro | None:
        posicion = codigo % self.capacidad

        