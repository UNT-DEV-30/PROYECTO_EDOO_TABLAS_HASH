# VARIABLE UTILIZADA PARA REPRESENTAR UN POSICION BORRADA EN TABLAS HASH
BORRADO = "BORRADO"

# CLASE REGISTRO
class Registro:
    def __init__(self, codigo: int, nombre: str) -> None:
        self.__codigo = codigo
        self.__nombre = nombre

    @property
    def codigo(self) -> int:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: int) -> None:
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("El código debe ser un número entero no negativo.")
        self.__codigo = valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser una cadena de texto no vacía.")
        self.__nombre = valor.strip()

    def __str__(self) -> str:
        return f"[{self.__codigo} : {self.__nombre}]"

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, Registro):
            return self.__codigo == otro.__codigo
        return False

# Verifica si un número es primo de manera iterativa
def es_primo(n: int) -> bool:
    if n < 2:
        return False
    
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
        
    return True

# Calcula el nuevo tamaño de un arreglo, teniendo en cuanta el tamaño anterior
def siguiente_primo_rehash(primo_actual: int) -> int:
    candidato = 2 * primo_actual + 1
    
    while not es_primo(candidato):
        candidato += 1
        
    return candidato