from models import Registro, BORRADO, siguiente_primo_rehash

class TablaHashCuadratica:
    def __init__(self):
        self.__capacidad: int = 11
        self.__arreglo: list[Registro] = [None] * self.__capacidad
        self.__num_elementos: int = 0  

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    def calcular_posicion(self, posicion_original: int, intento: int) -> int:
        return (posicion_original + intento**2) % self.__capacidad

    def insertar(self, registro: Registro) -> None:
        posicion_original = registro.codigo % self.__capacidad
        intento = 0

        posicion_disponible = None

        while intento < self.__capacidad:
            posicion = self.calcular_posicion(posicion_original, intento)
            registro_actual = self.__arreglo[posicion]

            if not registro_actual is None and registro_actual != BORRADO:
                if registro_actual.codigo == registro.codigo:
                    self.__arreglo[posicion] = registro
                    return


            if (registro_actual is None or registro_actual == BORRADO) and posicion_disponible is None:
                posicion_disponible = posicion

            if registro_actual is None:
                break

            intento += 1

        if not posicion_disponible is None:
            self.__arreglo[posicion_disponible] = registro
            self.__num_elementos += 1

            if self.factor_carga() >= 0.45:
                self.rehashing()

    def buscar(self, codigo: int) -> Registro | None:
        posicion_original = codigo % self.__capacidad
        intento = 0
        
        posicion = self.calcular_posicion(posicion_original, intento)
        registro_actual = self.__arreglo[posicion]
        
        while not registro_actual is None and intento < self.__capacidad:
            if registro_actual != BORRADO and registro_actual.codigo == codigo:
                return registro_actual
            
            intento += 1
            posicion = self.calcular_posicion(posicion_original, intento)
            registro_actual = self.__arreglo[posicion]

        return None

    def eliminar(self, codigo: int) -> bool:
        posicion_original = codigo % self.__capacidad
        intento = 0
         
        posicion = self.calcular_posicion(posicion_original, intento)
        registro_actual = self.__arreglo[posicion]
         
        while not registro_actual is None and intento < self.__capacidad:
            if registro_actual != BORRADO and registro_actual.codigo == codigo:
                self.__arreglo[posicion] = BORRADO
                self.__num_elementos -= 1
                return True
                
            intento += 1
            posicion = self.calcular_posicion(posicion_original, intento)
            registro_actual = self.__arreglo[posicion]
 
        return False

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

        for reg in antiguo_arreglo:
            if reg is None or reg == BORRADO:
                continue

            self.insertar(reg)