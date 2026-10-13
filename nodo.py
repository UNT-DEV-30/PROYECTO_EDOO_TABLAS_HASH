from typing import Generic, TypeVar

T = TypeVar('T')

class Nodo(Generic[T]):
    def __init__(self, dato : T) -> Nodo[T]:
        self.siguiente : Nodo = None
        self.dato : T = dato