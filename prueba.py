from tablas_hash_encadenamiento import TablaHashEncadenamiento
from models import Registro

tabla = TablaHashEncadenamiento()

tabla.insertar(Registro(1, "hila"))


tabla.mostrar()