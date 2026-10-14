from lista_simple import ListaSimple
from models import Registro

class TablaHashEncadenamiento:
    def __init__(self) -> None:
        self.__capacidad: int = 11
        self.__arreglo: list[ListaSimple] = [None] * self.__capacidad
        self.__num_elementos: int = 0
        

    def insertar(self, registro: Registro) -> None:
        posicion = registro.codigo % self.__capacidad

        if self.__arreglo[posicion] is None:
            self.__arreglo[posicion] = ListaSimple()
            self.__num_elementos += 1

        lista_posicion: ListaSimple = self.__arreglo[posicion]

        if lista_posicion.buscar_codigo(registro.codigo) is None:
            lista_posicion.insertar_final(registro)

        if self.factor_de_carga() >= 0.75:
            self.rehashing()

    def buscar(self, codigo: int) -> Registro | None:
        posicion = codigo % self.__capacidad

        return self.__arreglo[posicion].buscar_codigo(codigo)

    def modificar(self, codigo: int, nombre: str) -> None:
        posicion = codigo % self.__capacidad

        self.__arreglo[posicion].modificar(codigo, nombre)

    def eliminar(self, codigo: int) -> None:
        posicion = codigo % self.__capacidad

        self.__arreglo[posicion].eliminar_codigo(codigo)

    def mostrar(self) -> None:
        for i in range(self.__capacidad):
            print(f"{i} : {self.__arreglo[i]}")
            
    def factor_de_carga(self) -> float:
        return self.__num_elementos/self.__capacidad

    def rehashing(self) -> None:
        nueva_capacidad = 2 * self.__capacidad + 1
        nuevo_arreglo: list[ListaSimple] = [None] * nueva_capacidad
        nuevo_numero_elementos = 0

        for lista_actual in self.__arreglo:
            if lista_actual is None:
                continue

            for j in range(lista_actual.contar_elementos()):
                registro = lista_actual.obtener_posicion(j)

                nueva_posicion = registro.codigo % nueva_capacidad

                if nuevo_arreglo[nueva_posicion] is None:
                    nuevo_arreglo[nueva_posicion] = ListaSimple()
                    nuevo_numero_elementos += 1

                nuevo_arreglo[nueva_posicion].insertar_final(registro)

        self.__capacidad = nueva_capacidad
        self.__arreglo = nuevo_arreglo
        self.__num_elementos = nuevo_numero_elementos
        