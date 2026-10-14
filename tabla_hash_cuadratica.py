from models import Registro, BORRADO, siguiente_primo_rehash

class TablaHashCuadratica:
    def __init__(self):
        self.__capacidad: int = 11
        self.__arreglo: list[Registro] = [None] * self.__capacidad
        self.__num_elementos: int = 0

    def calcular_posicion(self, posicion_original: int, intento: int) -> int:
        return (posicion_original + intento**2) % self.__capacidad

    def insertar(self, registro: Registro) -> None:

        if not self.buscar(registro.codigo) is None:
            raise ValueError("Codigo duplicado")

        posicion_original = registro.codigo % self.__capacidad
        intento = 0

        posicion = self.calcular_posicion(posicion_original, intento)
        registro_actual = self.__arreglo[posicion]

        while not registro_actual is None and not registro_actual is BORRADO :
            intento += 1
            posicion = self.calcular_posicion(posicion_original, intento)
            registro_actual = self.__arreglo[posicion]

        self.__arreglo[posicion] = registro
        self.__num_elementos += 1

        if self.factor_carga() >= 0.45:
            self.rehashing()

    def buscar(self, codigo: int) -> Registro | None:
        posicion_original = codigo % self.__capacidad
        intento = 0
        
        posicion = self.calcular_posicion(posicion_original, intento)
        registro_actual = self.__arreglo[posicion]
        
        while not registro_actual is None and intento < self.__capacidad:
            if not registro_actual is BORRADO and registro_actual.codigo == codigo:
                return registro_actual
            
            intento += 1
            posicion = self.calcular_posicion(posicion_original, intento)
            registro_actual = self.__arreglo[posicion]

        return None

    def modificar(self, codigo: int, nombre: str) -> bool:
        posicion_original = codigo % self.__capacidad
        intento = 0
         
        posicion = self.calcular_posicion(posicion_original, intento)
        registro_actual = self.__arreglo[posicion]
         
        while not registro_actual is None and intento < self.__capacidad:
            if not registro_actual is BORRADO and registro_actual.codigo == codigo:
                registro_actual.nombre = nombre
                return True

            intento += 1
            posicion = self.calcular_posicion(posicion_original, intento)
            registro_actual = self.__arreglo[posicion]
 
        return False

    def eliminar(self, codigo: int) -> bool:
        posicion_original = codigo % self.__capacidad
        intento = 0
         
        posicion = self.calcular_posicion(posicion_original, intento)
        registro_actual = self.__arreglo[posicion]
         
        while not registro_actual is None and intento < self.__capacidad:
            if not registro_actual is BORRADO and registro_actual.codigo == codigo:
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
        nueva_capacidad = siguiente_primo_rehash(self.__capacidad)
        nuevo_arreglo: list[Registro] = [None] * nueva_capacidad

        for reg in self.__arreglo:
            if reg is BORRADO or reg is None:
                continue

            posicion_original = reg.codigo % nueva_capacidad
            intento = 0


            
            posicion = (posicion_original + intento**2) % nueva_capacidad
            
            while not nuevo_arreglo[posicion] is None:
                intento += 1
                posicion = (posicion_original + intento**2) % nueva_capacidad
            
            nuevo_arreglo[posicion] = reg

        self.__capacidad = nueva_capacidad
        self.__arreglo = nuevo_arreglo