
from models import Registro
from tabla_hash_encadenamiento import TablaHashEncadenamiento
from tabla_hash_lineal import TablaHashLineal
from tabla_hash_cuadratica import TablaHashCuadratica
from tabla_Hash_Doble import TablaHashDoble


def probar_tabla(nombre, tabla):
    print("\n" + "=" * 50)
    print(nombre)
    print("=" * 50)

    print("\n1. Insertar registros")
    tabla.insertar(Registro(22, "Carlos"))
    tabla.insertar(Registro(33, "Ana"))
    tabla.insertar(Registro(44, "Luis"))
    tabla.insertar(Registro(55, "Maria"))
    tabla.mostrar()

    print("\n2. Buscar un registro existente")
    print(tabla.buscar(33))

    print("\n3. Buscar un registro inexistente")
    print(tabla.buscar(99))

    print("\n4. Actualizar un registro duplicado")
    tabla.insertar(Registro(33, "Ana actualizada"))
    print(tabla.buscar(33))

    print("\n5. Eliminar un registro")
    print(tabla.eliminar(44))
    print("Buscar registro eliminado:", tabla.buscar(44))

    print("\n6. Factor de carga")
    print(f"{tabla.factor_carga():.2f}")

    print("\n7. Estado final de la tabla")
    tabla.mostrar()


def main():
    tablas = [
        ("ENCADENAMIENTO", TablaHashEncadenamiento()),
        ("SONDEO LINEAL", TablaHashLineal()),
        ("SONDEO CUADRÁTICO", TablaHashCuadratica()),
        ("DOBLE HASHING", TablaHashDoble())
    ]

    for nombre, tabla in tablas:
        probar_tabla(nombre, tabla)


if __name__ == "__main__":
    main()
