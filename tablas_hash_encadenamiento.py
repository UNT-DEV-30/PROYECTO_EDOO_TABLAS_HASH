from lista_simple import ListaSimple
from models import Registro, siguiente_primo_rehash

class TablaHashEncadenamiento:
    def __init__(self) -> None:
        self.__capacidad: int = 11
        self.__arreglo: list[ListaSimple] = [None] * self.__capacidad
        self.__num_elementos: int = 0

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    def insertar(self, registro: Registro) -> None:
        posicion = registro.codigo % self.__capacidad

        if self.__arreglo[posicion] is None:
            self.__arreglo[posicion] = ListaSimple()
            

        lista = self.__arreglo[posicion]

        if lista.buscar_codigo(registro.codigo) is None:
            lista.insertar_final(registro)
            self.__num_elementos += 1

            if self.factor_carga() >= 0.75:
                self.rehashing()
        else:
            lista.modificar(registro.codigo, registro.nombre)

        

    def buscar(self, codigo: int) -> Registro | None:
        posicion = codigo % self.__capacidad

        lista = self.__arreglo[posicion]
        
        if lista is None:
            return None

        return lista.buscar_codigo(codigo)

    def eliminar(self, codigo: int) -> bool:
        posicion = codigo % self.__capacidad

        lista = self.__arreglo[posicion]

        if lista is None:
            return False

        estado = self.__arreglo[posicion].eliminar_codigo(codigo)

        if estado:
            self.__num_elementos -= 1

        return estado

    def mostrar(self) -> None:
        for i in range(self.__capacidad):
            print(f"{i} : {self.__arreglo[i]}")
            
    def factor_carga(self) -> float:
        return self.__num_elementos/self.__capacidad

    def rehashing(self) -> None:
        antigua_capacidad = self.__capacidad
        antiguo_arreglo = self.__arreglo.copy()
        self.__num_elementos = 0
        
        self.__capacidad = siguiente_primo_rehash(antigua_capacidad)
        self.__arreglo = [None] * self.__capacidad
        
        for lista in antiguo_arreglo:
            if lista is None:
                continue

            nodo_actual = lista.primero

            while not nodo_actual is None:
                self.insertar(nodo_actual.dato)
                nodo_actual = nodo_actual.siguiente