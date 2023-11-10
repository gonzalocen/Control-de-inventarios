# UCASAL - Programación II
# Autor: Gonzalo Martín Cendoya

import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import time

inventario = {}

#Función para cargar el inventario desde 'invetario.csv'
def cargarDatosDesdeCsv():
    nombre_archivo = r'inventario.csv'  # Ruta del archivo CSV
    archivo = open(nombre_archivo, 'r')
    lector_csv = csv.DictReader(archivo)
    for fila in lector_csv:
        nombre = fila['Producto']
        precio = float(fila['Precio'])
        cantidad = int(fila['Cantidad'])

        producto = {
            'precio': precio,
            'cantidad': cantidad
        }

        inventario[nombre] = producto

    archivo.close()
#Función para Guardar los cambios en un arhcivo .csv
def guardarDatosEnCsv(nombre_archivo):
    archivo = open(nombre_archivo, 'w', newline='')
    campos = ['Producto', 'Precio', 'Cantidad']
    escritor_csv = csv.DictWriter(archivo, fieldnames=campos)
    escritor_csv.writeheader()
    for producto, item in inventario.items():
        fila = {
            'Producto': producto,
            'Precio': item['precio'],
            'Cantidad': item['cantidad'],
        }
        escritor_csv.writerow(fila)

    archivo.close()

#Función para agregar productos
def agregarProducto():
    nombre = input("Ingrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    cantidad = int(input("Ingrese la cantidad disponible: "))

    if nombre in inventario:
        confirmacion = input(f"El producto '{nombre}' ya existe en el inventario. ¿Desea sobrescribir la información existente? (s/n): ")
        if confirmacion.lower() != 's':
            print("No se ha realizado ningún cambio en el inventario.")
            return

    producto = {
        'precio': precio,
        'cantidad': cantidad,
    }

    inventario[nombre] = producto
    nombre_archivo = 'inventario.csv'
    guardarDatosEnCsv(nombre_archivo)
    print(f"El producto '{nombre}' ha sido agregado al inventario.")

#Función para mostar invetario
def mostrarInventario():
    print("Inventario:")
    for nombre, producto in inventario.items():
        print(f"Producto: {nombre}, Precio: {producto['precio']}, Cantidad: {producto['cantidad']}")

#Función para buscar productos
def buscarProducto():
    nombre_producto = input("Ingrese el nombre del producto que desea buscar: ")
    if nombre_producto in inventario:
        producto = inventario[nombre_producto]
        print(f"Detalles del producto '{nombre_producto}':")
        print(f"Precio: {producto['precio']}")
        print(f"Cantidad: {producto['cantidad']}")
    else:
        print(f"No se encontró el producto '{nombre_producto}' en el inventario.")

#Función para actulizar productos del inventario
def actualizarCantidad():
    nombre_producto = input("Ingrese el nombre del producto al que desea ajustar la cantidad: ")
    if nombre_producto in inventario:
        cantidad_actual = inventario[nombre_producto]['cantidad']
        ajuste = int(input("Ingrese la cantidad a ajustar (positiva para aumentar, negativa para disminuir): "))
        nueva_cantidad = cantidad_actual + ajuste
        if nueva_cantidad >= 0:
            inventario[nombre_producto]['cantidad'] = nueva_cantidad
            print(f"La cantidad del producto '{nombre_producto}' ha sido ajustada a {nueva_cantidad}.")
        else:
            print("Atención! La cantidad ajustada resultaría en un valor negativo.")
    else:
        print(f"No se encontró el producto '{nombre_producto}' en el inventario.")
        print(f"Puede agregarlo desde la opción 2 del menú principal")

#Función para graficar Productos vs Cantidad
def generarGrafico():
    nombres_productos = list(inventario.keys())
    cantidades = [producto['cantidad'] for producto in inventario.values()]
    precios = [producto['precio'] for producto in inventario.values()]

    cantidadGreen = []
    nombreGreen = []

    cantidadRed = []
    nombreRed = []

    total_productos = len(nombres_productos)
    total_stock = sum([cantidad * precio for cantidad, precio in zip(cantidades, precios)])

    for i in range(len(nombres_productos)):
        nombre = nombres_productos[i]
        cantidad = cantidades[i]

        if cantidad > 100:
            cantidadGreen.append(cantidad)
            nombreGreen.append(nombre)
        else:
            cantidadRed.append(cantidad)
            nombreRed.append(nombre)

    plt.bar(nombreGreen, cantidadGreen, color='green', alpha=0.7, edgecolor='black', linewidth=1.5)
    plt.bar(nombreRed, cantidadRed, color='red', alpha=0.7, edgecolor='black', linewidth=1.5)

    plt.xlabel("Productos")
    plt.ylabel("Cantidad")
    plt.title("Inventario")
    plt.xticks(rotation=45)

    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(['Mayor a 100 unidades', 'Menor a 100 unidades'], loc='upper right')
    plt.tight_layout()

    # Agregar etiquetas de cantidad a las barras
    j = 0
    for i in range(len(nombreGreen)):
        plt.text(i, cantidadGreen[i] + 5, str(cantidadGreen[i]), ha='center', va='bottom', fontsize=8, fontweight='bold')
        j += 1

    for i in range(len(nombreRed)):
        plt.text(i+j, cantidadRed[i] + 25, str(cantidadRed[i]), ha='center', va='top', fontsize=8, fontweight='bold')

        # Agregar información de cantidad total de productos y monto total del stock
        plt.text(len(nombres_productos), max(cantidades) - 60, f"Total de productos: {total_productos}", ha='right',
                 va='top', fontsize=10, fontstyle='italic')
        plt.text(len(nombres_productos), max(cantidades) - 90, f"Monto total del stock: ${total_stock}", ha='right',
                 va='top', fontsize=10, fontstyle='italic')

    # Mostrar el gráfico
    plt.show()

#Función para mostar las estadisticas del inventario
def mostrarEstadisticas():
    precios = [producto['precio'] for producto in inventario.values()]
    cantidades = [producto['cantidad'] for producto in inventario.values()]
    valores = [producto['precio'] * producto['cantidad'] for producto in inventario.values()]

    print(f"Estadísticas del inventario:")
    print(f"Cantidad total de productos: {len(inventario)}")
    print(f"Precio mínimo: {np.min(precios)}")
    print(f"Precio máximo: {np.max(precios)}")
    print(f"Cantidad mínima: {np.min(cantidades)}")
    print(f"Cantidad máxima: {np.max(cantidades)}")
    print(f"Promedio de precios: {round(np.mean(precios), 2)}")
    print(f"Promedio de cantidades: {round(np.mean(cantidades), 2)}")
    print(f"La cantidad total del inventario en $: {np.sum(valores)}")

#Función para mostar el panel de ayuda
def mostrarAyuda():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║                     Ayuda                        ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║ 1. Cargar inventario desde archivo .csv          ║")
    print("║    - Carga los datos del inventario desde        ║")
    print("║      un archivo CSV.(por defecto 'invetario.csv' ║")
    print("║ 2. Agregar producto                              ║")
    print("║    - Permite agregar un nuevo producto al        ║")
    print("║      inventario.                                 ║")
    print("║ 3. Mostrar inventario                            ║")
    print("║    - Muestra la lista de productos en el         ║")
    print("║      inventario.                                 ║")
    print("║ 4. Buscar producto                               ║")
    print("║    - Busca un producto específico en el          ║")
    print("║      inventario.                                 ║")
    print("║ 5. Actualizar cantidad                           ║")
    print("║    - Permite ajustar la cantidad de un           ║")
    print("║      producto en el inventario.                  ║")
    print("║ 6. Generar gráfico de inventario                 ║")
    print("║    - Genera un gráfico que muestra la            ║")
    print("║      cantidad de productos en el inventario.     ║")
    print("║ 7. Mostrar estadísticas del inventario           ║")
    print("║    - Muestra estadísticas sobre el               ║")
    print("║      inventario, como el precio mínimo y         ║")
    print("║      máximo, la cantidad mínima y máxima,        ║")
    print("║      etc.                                        ║")
    print("║ 8. Guardar inventario en archivo CSV             ║")
    print("║    - Guarda los datos del inventario en un       ║")
    print("║      archivo CSV.                                ║")
    print("╚══════════════════════════════════════════════════╝")

def menuPrincipal():
    time.sleep(2)
    os.system('cls')  # Limpiar la pantalla de la consola
    while True:
            print("\n╔══════════════════════════════════════════════════╗")
            print("║                 MENÚ PRINCIPAL                   ║")
            print("╠══════════════════════════════════════════════════╣")
            print("║ 1. Cargar inventario desde archivo .csv          ║")
            print("║ 2. Agregar producto                              ║")
            print("║ 3. Mostrar inventario                            ║")
            print("║ 4. Buscar producto                               ║")
            print("║ 5. Actualizar cantidad                           ║")
            print("║ 6. Generar gráfico de inventario                 ║")
            print("║ 7. Mostrar estadísticas del inventario           ║")
            print("║ 8. Guardar inventario en archivo CSV             ║")
            print("║ 9. Ayuda                                         ║")
            print("║ 0. Salir                                         ║")
            print("╚══════════════════════════════════════════════════╝")
            opcion = input("\nSeleccione una opción: ")
            if opcion == '1':
                cargarDatosDesdeCsv()
                time.sleep(1)
                print("\nArchivo cargado con éxito")
                time.sleep(2)
                os.system('cls')  # Limpiar la pantalla de la consola
            elif opcion == '2':
                agregarProducto()
            elif opcion == '3':
                mostrarInventario()
                entrada = input("\nPara volver al menú principal presione 0 y luego enter: ")
                while entrada != '0':
                    entrada = input("Opción inválida. Por favor, presione 0 para volver al menú principal.")
                os.system('cls')
            elif opcion == '4':
                buscarProducto()
                entrada = input("\nPara volver al menú principal presione 0 y luego enter: ")
                while entrada != '0':
                    entrada = input("Opción inválida. Por favor, presione 0 para volver al menú principal.")
                os.system('cls')
            elif opcion == '5':
                actualizarCantidad()
                entrada = input("\nPara volver al menú principal presione 0 y luego enter: ")
                while entrada != '0':
                    entrada = input("Opción inválida. Por favor, presione 0 para volver al menú principal.")
            elif opcion == '6':
                generarGrafico()
                os.system('cls')
            elif opcion == '7':
                mostrarEstadisticas()
                entrada = input("\nPara volver al menú principal presione 0 y luego enter: ")
                while entrada != '0':
                    entrada = input("Opción inválida. Por favor, presione 0 para volver al menú principal.")
                os.system('cls')
            elif opcion == '8':
                nombre_archivo = input("Ingrese el nombre del archivo .csv para guardar el inventario: ")
                guardarDatosEnCsv(nombre_archivo)
                time.sleep(1)
                print(f"Inventario guardado con éxito como: {nombre_archivo} ")
                time.sleep(3)
                os.system('cls')
            elif opcion == '9':
                os.system('cls')
                mostrarAyuda()
                entrada = input("\nPara volver al menú principal presione 0 y luego enter: ")
                while entrada != '0':
                    entrada = input("Opción inválida. Por favor, presione 0 para volver al menú principal: ")
                os.system('cls')
            elif opcion == '0':
                print("\n\nGracias por utilizar el programa. ¡Hasta luego!")
                time.sleep(2)
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

# Función para Mostrar la pantalla de bienvenida
def mostrarPantallaBienvenida():
    print("════════════════════════════════════════════════════")
    print("*  Bienvenido al Sistema de Gestión de Inventarios *")
    print("════════════════════════════════════════════════════")
    print("\n╔══════════════════════════════════════════════════╗")
    print("║        Sistema de Gestión de Inventarios         ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║ Sistema para gestionar el inventario             ║")
    print("║ de productos.                                    ║")
    print("║                                                  ║")
    print("║ Versión: 1.1                                     ║")
    print("║ Año: 2.023                                       ║")
    print("║                                                  ║")
    print("║                                                  ║")
    print("║                                                  ║")
    print("║                   Autor: Gonzalo Martín Cendoya  ║")
    print("╚══════════════════════════════════════════════════╝")
    print("\n\nPresione Enter para ejecutar el programa...")
    input()

# Mostrar pantalla de bienvenida
mostrarPantallaBienvenida()

# Ejecutar el programa
print("Aguarde mientras se ejecuta el programa.")
menuPrincipal()