BORRADO = "BORRADO"

class Registro:
    def __init__(self, codigo: int, nombre: str) -> None:
        self.codigo = codigo
        self.nombre = nombre

    @property
    def codigo(self) -> int:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: int) -> None:
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("El código debe ser un número entero no negativo.")
        self._codigo = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser una cadena de texto no vacía.")
        self._nombre = valor.strip()

    def __str__(self) -> str:
        return f"[{self._codigo}] {self._nombre}"

    def __repr__(self) -> str:
        return f"Registro({self._codigo}, '{self._nombre}')"

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, Registro):
            return self._codigo == otro._codigo
        return False