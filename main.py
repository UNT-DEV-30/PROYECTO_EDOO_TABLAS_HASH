
from models import Registro
from tabla_hash_encadenamiento import TablaHashEncadenamiento
from tabla_hash_lineal import TablaHashLineal
from tabla_hash_cuadratica import TablaHashCuadratica
from tabla_Hash_Doble import TablaHashDoble


def menu_principal():
    print("\n========== SISTEMA DE TABLAS HASH ==========")
    print("1. Tabla hash por encadenamiento")
    print("2. Tabla hash por sondeo lineal")
    print("3. Tabla hash por sondeo cuadrático")
    print("4. Tabla hash por doble hashing")
    print("5. Ejecutar pruebas demostrativas")
    print("0. Salir")
    return input("Seleccione una opción: ")


def menu_operaciones():
    print("\n========== OPERACIONES ==========")
    print("1. Insertar registro")
    print("2. Buscar registro")
    print("3. Eliminar registro")
    print("4. Mostrar tabla")
    print("5. Mostrar factor de carga")
    print("6. Ejecutar rehashing manual")
    print("7. Cargar datos de prueba (Inventario de Laboratorio)")
    print("0. Volver al menú principal")
    return input("Seleccione una operación: ")


def menu_pruebas():
    print("\n========== PRUEBAS DEMOSTRATIVAS ==========")
    print("1. Encadenamiento")
    print("2. Sondeo lineal")
    print("3. Sondeo cuadrático")
    print("4. Doble hashing")
    print("0. Volver al menú principal")
    return input("Seleccione una estrategia: ")


def cargar_datos_prueba(tabla):
    
    registros_prueba = [
        Registro(10, "Probeta Graduada"),
        Registro(21, "Pipeta Automática"),
        Registro(32, "Mechero Bunsen"),
        Registro(43, "Tubos de Ensayo"),
        Registro(54, "Placa Petri"),
        Registro(65, "Microscopio Óptico"),
        Registro(76, "Centrífuga de Mesa")
    ]
    for reg in registros_prueba:
        tabla.insertar(reg)
    print("\n¡Datos de prueba cargados exitosamente en la tabla!")

def operar(tabla):
    
    while True:
        opcion = menu_operaciones()

        if opcion == "1":
            try:
                codigo = int(input("Código: "))
                nombre = input("Nombre: ")
                tabla.insertar(Registro(codigo, nombre))
                print("Registro insertado o actualizado.")
            except ValueError as error:
                print("Error:", error)

        elif opcion == "2":
            try:
                codigo = int(input("Código a buscar: "))
                registro = tabla.buscar(codigo)

                if registro is None:
                    print("Registro no encontrado.")
                else:
                    print("Registro encontrado:", registro)
            except ValueError:
                print("Ingrese un código numérico válido.")

        elif opcion == "3":
            try:
                codigo = int(input("Código a eliminar: "))

                if tabla.eliminar(codigo):
                    print("Registro eliminado.")
                else:
                    print("Registro no encontrado.")
            except ValueError:
                print("Ingrese un código numérico válido.")

        elif opcion == "4":
            tabla.mostrar()

        elif opcion == "5":
            print(f"Factor de carga: {tabla.factor_carga():.2f}")

        elif opcion == "6":
            capacidad_anterior = tabla.capacidad
            tabla.rehashing()
            print("Rehashing ejecutado.")
            print("Capacidad anterior:", capacidad_anterior)
            print("Capacidad nueva:", tabla.capacidad)
            tabla.mostrar()

        elif opcion == "7":  
            cargar_datos_prueba(tabla)
            tabla.mostrar()
            
        elif opcion == "0":
            break

        else:
            print("Opción no válida.")


def crear_estrategias():
    return [
        ("Encadenamiento", TablaHashEncadenamiento),
        ("Sondeo lineal", TablaHashLineal),
        ("Sondeo cuadrático", TablaHashCuadratica),
        ("Doble hashing", TablaHashDoble)
    ]


def pruebas_demostrativas(nombre, clase):
    tabla = clase()

    print("\n" + "=" * 55)
    print("PRUEBAS:", nombre.upper())
    print("=" * 55)

    print("\n1. INSERTAR REGISTROS (CONTROL DE INVENTARIO DE LABORATORIO) Y PROVOCAR COLISIONES")
    for codigo, nombre_registro in [
        (11, "Microscopio Óptico"),
        (22, "Centrífuga de Mesa"),
        (33, "Matraz Erlenmeyer"),
        (44, "Espectrofotómetro"),
        (55, "Balanza Analítica")
    ]:
        tabla.insertar(Registro(codigo, nombre_registro))

    tabla.mostrar()

    print("\n2. ACTUALIZAR UN CÓDIGO DUPLICADO")
    tabla.insertar(Registro(22, "Centrífuga Digital Avanzada"))
    print("Resultado:", tabla.buscar(22))

    print("\n3. BÚSQUEDA EXITOSA")
    print("Buscar código 33:", tabla.buscar(33))

    print("\n4. BÚSQUEDA FALLIDA")
    print("Buscar código 999:", tabla.buscar(999))

    print("\n5. ELIMINAR UN REGISTRO")
    print("Eliminar código 33:", tabla.eliminar(33))
    print("Buscar código eliminado:", tabla.buscar(33))

    print("\n6. FACTOR DE CARGA Y ESTADO FINAL")
    print(f"Factor de carga: {tabla.factor_carga():.2f}")
    tabla.mostrar()

    print("\n7. DEMOSTRAR REHASHING AUTOMÁTICO")
    capacidad_anterior = tabla.capacidad

    for i in range(6, 31):
        tabla.insertar(Registro(i * 11, f"Registro {i}"))

        if tabla.capacidad != capacidad_anterior:
            print("¡Rehashing automático detectado!")
            print("Capacidad anterior:", capacidad_anterior)
            print("Capacidad nueva:", tabla.capacidad)
            capacidad_anterior = tabla.capacidad

    tabla.mostrar()
    print("\nFin de las pruebas de", nombre)

def ejecutar_pruebas():
    estrategias = crear_estrategias()

    while True:
        opcion = menu_pruebas()

        if opcion == "0":
            break

        elif opcion in ("1", "2", "3", "4"):
            indice = int(opcion) - 1
            nombre, clase = estrategias[indice]
            pruebas_demostrativas(nombre, clase)

        else:
            print("Opción no válida.")

def main():
    estrategias = crear_estrategias()

    while True:
        opcion = menu_principal()

        if opcion == "0":
            print("Programa finalizado.")
            break

        elif opcion == "5":
            ejecutar_pruebas()

        elif opcion in ("1", "2", "3", "4"):
            indice = int(opcion) - 1
            nombre, clase = estrategias[indice]
            print("\nEstrategia seleccionada:", nombre)
            operar(clase())

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()

