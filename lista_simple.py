from models import Registro

class Nodo:
    def __init__(self, dato : Registro) -> None:
        self.siguiente : Nodo | None = None
        self.dato : Registro = dato

class ListaSimple:
    def __init__(self) -> None:
        self.primero : Nodo | None = None

    def esta_vacia(self) -> bool:
        return self.primero is None

    def contar_elementos(self) -> int:
        contador = 0
        actual = self.primero

        while actual != None:
            contador += 1
            actual = actual.siguiente

        return contador

    def obtener_posicion(self, posicion: int) -> Registro | None:
        contador = 0
        actual = self.primero

        while actual != None:
            if contador == posicion:
                return actual.dato
            
            actual = actual.siguiente
            contador += 1

        return None


    def insertar_final(self, dato: Registro) -> None:
        nuevo = Nodo(dato)

        if self.esta_vacia():
            self.primero = nuevo
            return

        actual = self.primero

        while actual.siguiente != None:
            actual = actual.siguiente

        actual.siguiente = nuevo

        return

    def buscar_codigo(self, codigo: int) -> Registro | None:
        actual = self.primero
        
        while actual != None:
            if actual.dato.codigo == codigo:
                return actual.dato
            
            actual = actual.siguiente
        
        return None

    def eliminar_codigo(self, codigo: int) -> bool:
        if self.primero is None:
            return False

        actual = self.primero

        if actual.dato.codigo == codigo:
            self.primero = actual.siguiente
            return True

        while actual.siguiente != None:
            if actual.siguiente.dato.codigo == codigo:
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente
            
        return False

    def modificar(self, codigo: int, nombre: str) -> bool:
        actual = self.primero
                
        while actual != None:
            if actual.dato.codigo == codigo:
                actual.dato.nombre = nombre  
                return True      
            actual = actual.siguiente

        return False

    def recorrer(self) -> None:
        actual = self.primero

        while actual != None:
            print(actual.dato, end=" -> ")
            actual = actual.siguiente

        print(" ")

    def __str__(self) -> str:
        elementos = []
        actual = self.primero
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        elementos.append("None")
        return " -> ".join(elementos)