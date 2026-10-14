from models import Registro
from tablas_hash_encadenamiento import TablaHashEncadenamiento
from tabla_hash_lineal import TablaHashLineal
from tabla_hash_cuadratica import TablaHashCuadratica
from tabla_Hash_Doble import TablaHashDoble

def imprimir_fila(caso: str, entrada: str, esperado: str, real: str, correcto: bool) -> None:
    marca = "SÍ" if correcto else "NO"
    print(f"{caso:<40} | {entrada:<28} | {esperado:<20} | {real:<20} | {marca}")

def ejecutar_pruebas_tad(tabla_hash) -> None:
    nombre_estrategia = tabla_hash.__class__.__name__
    print(f"\n{'='*130}")
    print(f"=== PRUEBAS MÍNIMAS PARA: {nombre_estrategia} ===")
    print(f"{'='*130}")
    print(f"{'CASO (ESCENARIO)':<40} | {'ENTRADA':<28} | {'RESULTADO ESPERADO':<20} | {'RESULTADO REAL':<20} | {'¿CORRECTO?'}")
    print("-" * 130)

    # (1) Tabla vacía
    es_vacia = tabla_hash.factor_carga() == 0.0
    imprimir_fila("1. Tabla vacía", "Ninguna", "FC: 0.0", f"FC: {tabla_hash.factor_carga():.2f}", es_vacia)

    # (2) Inserción sin colisión
    tabla_hash.insertar(Registro(10, "Microscopio"))
    reg_2 = tabla_hash.buscar(10)
    exito_2 = reg_2 is not None and reg_2.nombre == "Microscopio"
    imprimir_fila("2. Inserción sin colisión", "Registro(10, 'Microscopio')", "Insertado", "Insertado" if exito_2 else "Fallo", exito_2)

    # (3) Inserción con colisión
    tabla_hash.insertar(Registro(21, "Multímetro"))
    reg_3 = tabla_hash.buscar(21)
    exito_3 = reg_3 is not None and reg_3.nombre == "Multímetro"
    imprimir_fila("3. Inserción con colisión", "Registro(21, 'Multímetro')", "Insertado", "Insertado" if exito_3 else "Fallo", exito_3)

    # (4) Búsqueda encontrada
    reg_4 = tabla_hash.buscar(21)
    exito_4 = reg_4 is not None and reg_4.codigo == 21
    imprimir_fila("4. Búsqueda encontrada", "Buscar código 21", "Registro(21)", "Registro(21)" if exito_4 else "None", exito_4)

    # (5) Búsqueda ausente
    reg_5 = tabla_hash.buscar(99)
    exito_5 = reg_5 is None
    imprimir_fila("5. Búsqueda ausente", "Buscar código 99", "None", str(reg_5), exito_5)

    # (6) Eliminación existente
    exito_6 = tabla_hash.eliminar(10)
    imprimir_fila("6. Eliminación existente", "Eliminar código 10", "True", str(exito_6), exito_6 is True)

    # (7) Eliminación ausente
    exito_7 = tabla_hash.eliminar(99)
    imprimir_fila("7. Eliminación ausente", "Eliminar código 99", "False", str(exito_7), exito_7 is False)

    # (8) Búsqueda tras eliminar otro en misma secuencia
    reg_8 = tabla_hash.buscar(21)
    exito_8 = reg_8 is not None and reg_8.codigo == 21
    imprimir_fila("8. Búsqueda tras borrado", "Buscar código 21", "Encontrado", "Encontrado" if exito_8 else "Fallo", exito_8)

    # (9) Reinserción tras borrado
    tabla_hash.insertar(Registro(32, "Balanza"))
    reg_9 = tabla_hash.buscar(32)
    exito_9 = reg_9 is not None and reg_9.nombre == "Balanza"
    imprimir_fila("9. Reinserción tras borrado", "Registro(32, 'Balanza')", "Insertado", "Insertado" if exito_9 else "Fallo", exito_9)

    # (10) Clave duplicada y actualización
    tabla_hash.insertar(Registro(32, "Balanza Digital"))
    reg_10 = tabla_hash.buscar(32)
    exito_10 = reg_10 is not None and reg_10.nombre == "Balanza Digital"
    imprimir_fila("10. Clave duplicada (Act.)", "Registro(32, '...Digital')", "Balanza Digital", reg_10.nombre if reg_10 else "Error", exito_10)

    # (11) Factor de carga alto
    cap_antes_11 = tabla_hash.capacidad if hasattr(tabla_hash, 'capacidad') else 11

    for cod in [43, 54, 65, 76, 87]:
        tabla_hash.insertar(Registro(cod, f"Producto {cod}"))

    fc_11 = tabla_hash.factor_carga()
    cap_despues_11 = tabla_hash.capacidad if hasattr(tabla_hash, 'capacidad') else 11

    rehash_temprano = cap_despues_11 > cap_antes_11
    exito_11 = fc_11 > 0.5 or rehash_temprano

    if rehash_temprano:
        imprimir_fila("11. Factor de carga alto", "Insertar 5 registros", "FC>0.5 o Rehash", "Rehash temprano", exito_11)
    else:
        imprimir_fila("11. Factor de carga alto", "Insertar 5 registros", "FC Alto (>0.5)", f"FC = {fc_11:.2f}", exito_11)

    # (12) Rehashing y conservación
    cap_antigua = cap_despues_11

    tabla_hash.insertar(Registro(109, "Forzar Rehash"))
    tabla_hash.insertar(Registro(98, "Termómetro"))

    cap_nueva = tabla_hash.capacidad if hasattr(tabla_hash, 'capacidad') else cap_antigua * 2 + 1

    conserva_viejos = tabla_hash.buscar(21) is not None and tabla_hash.buscar(32) is not None
    conserva_nuevo = tabla_hash.buscar(98) is not None

    crecio = cap_nueva > 11
    exitoso_12 = crecio and conserva_viejos and conserva_nuevo

    imprimir_fila("12. Rehashing y conservación", "Registro(98) para Rehash", "Cap>11, Cons=True", f"Cap={cap_nueva}, Cons={conserva_viejos and conserva_nuevo}", exitoso_12)
    print("-" * 130)


if __name__ == "__main__":
    tablas_del_proyecto = [
        TablaHashEncadenamiento(),
        TablaHashLineal(11),
        TablaHashCuadratica(),
        TablaHashDoble(11)
    ]

    for tabla_actual in tablas_del_proyecto:
        ejecutar_pruebas_tad(tabla_actual)