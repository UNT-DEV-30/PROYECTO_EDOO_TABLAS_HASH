from typing import Generic, TypeVar
from nodo import Nodo

T = TypeVar('T')

class ListaSimple(Generic[T]):
    def __init__(self) -> ListaSimple[T]:
        self.primero : Nodo = None

    def esta_vacia(self) -> bool:
        if self.primero == None:
            return True
        else:
            return False

    def contar_elementos(self) -> int:
        contador = 0
        actual = self.primero

        while actual != None:
            contador += 1
            actual = actual.siguiente

        return contador

    def insertar_final(self, dato: T) -> None:
        nuevo = Nodo[T](dato)

        if self.esta_vacia():
            self.primero = nuevo
            return

        actual = self.primero

        while actual.siguiente != None:
            actual = actual.siguiente

        actual.siguiente = nuevo

        return

    def insertar_posicion(self, posicion: int, dato: T) -> None:
        if self.esta_vacia() or posicion >= self.contar_elementos() or posicion < 0:
            raise IndexError("Indice fuera de rangos")

        actual = self.primero
        contador = 0

        while contador != posicion - 1:
            contador += 1
            actual = actual.siguiente

        nuevo = Nodo[T](dato)

        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo

    def obtener_nodo_posicion(self, posicion: int) -> Nodo[T]:

        if self.esta_vacia():
            return None

        if posicion >= self.contar_elementos() or posicion < 0:
            raise IndexError("Indice fuera de rango")

        contador = 0
        actual = self.primero

        while contador != posicion:
            contador += 1
            actual = actual.siguiente

        return actual

    def obtener_posicion(self, posicion: int) -> T:
        return self.obtener_nodo_posicion(posicion).dato

    def eliminar_fin(self) -> None:
        actual = self.obtener_nodo_posicion(self.contar_elementos() - 2)

        actual.siguiente = None

    def eliminar_posicion(self, posicion: int) -> None:
        actual = self.obtener_nodo_posicion(posicion - 1)
        actual.siguiente = actual.siguiente.siguiente

    def modificar(self, posicion: int, dato: T) -> None:
        self.obtener_nodo_posicion(posicion).dato = dato

    def buscar(self, dato: T) -> T | None:
        actual = self.primero
        
        while actual != None:
            if actual.dato == dato:
                return actual.dato
            
            actual = actual.siguiente
        
        return None

    def recorrer(self) -> None:
        actual = self.primero

        while actual != None:
            print(actual.dato, end=" ")
            actual = actual.siguiente

        print(" ")