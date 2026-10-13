from registro import Registro

class Nodo:
    def __init__(self, dato : Registro) -> None:
        self.siguiente : Nodo = None
        self.dato : Registro = dato

class ListaSimple:
    def __init__(self) -> None:
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

    def insertar_final(self, dato: Registro) -> None:
        nuevo = Nodo[Registro](dato)

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

    def eliminar_codigo(self, codigo: int) -> None:
        actual = self.primero

        if actual.dato.codigo == codigo:
            self.primero = actual.siguiente

        while actual.siguiente != None:
            if actual.siguiente.dato.codigo == codigo:
                actual.siguiente = actual.siguiente.siguiente
                return

    def modificar(self, codigo: int, nombre: str) -> None:
        actual = self.primero
                
        while actual != None:
            if actual.dato.codigo == codigo:
                actual.dato.nombre = nombre  
                return             
            actual = actual.siguiente

    def recorrer(self) -> None:
        actual = self.primero

        while actual != None:
            print(actual.dato, end=" ")
            actual = actual.siguiente

        print(" ")