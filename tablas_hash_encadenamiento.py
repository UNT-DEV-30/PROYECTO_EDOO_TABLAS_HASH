from lista_simple import ListaSimple
from models import Registro, siguiente_primo_rehash

class TablaHashEncadenamiento:
    def __init__(self) -> None:
        self.__capacidad: int = 11
        self.__arreglo: list[ListaSimple] = [None] * self.__capacidad
        self.__num_elementos: int = 0
        
    @property
    def capacidad(self) -> int:
        # Esto permite que tu script Pruebas.py lea la capacidad actual en el Caso 12
        return self.__capacidad

    def insertar(self, registro: Registro) -> None:
        posicion = registro.codigo % self.__capacidad

        if self.__arreglo[posicion] is None:
            self.__arreglo[posicion] = ListaSimple()

        lista = self.__arreglo[posicion]

        # CORRECCIÓN PARA EL CASO 10: Si el código ya existe, se actualiza, NO se lanza error
        if lista.buscar_codigo(registro.codigo) is not None:
            lista.modificar(registro.codigo, registro.nombre)
            return  # Termina aquí, no incrementa el contador

        lista.insertar_final(registro)
        self.__num_elementos += 1

        if self.factor_carga() >= 0.75:
            self.rehashing()

    def buscar(self, codigo: int) -> Registro | None:
        posicion = codigo % self.__capacidad
        lista = self.__arreglo[posicion]
        
        if lista is None:
            return None

        return lista.buscar_codigo(codigo)

    def modificar(self, codigo: int, nombre: str) -> bool:
        posicion = codigo % self.__capacidad
        lista = self.__arreglo[posicion]
        
        if lista is None:
            return False

        return lista.modificar(codigo, nombre)

    def eliminar(self, codigo: int) -> bool:
        posicion = codigo % self.__capacidad
        lista = self.__arreglo[posicion]

        if lista is None:
            return False

        estado = lista.eliminar_codigo(codigo)

        if estado:
            self.__num_elementos -= 1

        return estado

    def mostrar(self) -> None:
        for i in range(self.__capacidad):
            print(f"{i} : {self.__arreglo[i]}")
            
    def factor_carga(self) -> float:
        return self.__num_elementos / self.__capacidad

    def rehashing(self) -> None:
        nueva_capacidad = siguiente_primo_rehash(self.__capacidad)
        nuevo_arreglo: list[ListaSimple] = [None] * nueva_capacidad

        for lista_actual in self.__arreglo:
            if lista_actual is None:
                continue

            for j in range(lista_actual.contar_elementos()):
                registro = lista_actual.obtener_posicion(j)
                nueva_posicion = registro.codigo % nueva_capacidad

                if nuevo_arreglo[nueva_posicion] is None:
                    nuevo_arreglo[nueva_posicion] = ListaSimple()

                nuevo_arreglo[nueva_posicion].insertar_final(registro)

        self.__capacidad = nueva_capacidad
        self.__arreglo = nuevo_arreglo