BORRADO = "BORRADO"

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