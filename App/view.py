import sys
import logic as lg


def new_logic():
  return lg.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    filename = input("Ingrese el nombre del archivo: ")
    result = lg.load_data(control, filename)
    print("\n Datos cargados correctamente")
    print(f"Tiempo de carga: {result['execution_time']} ms")
    print(f"Total de trayectos: {result['total_trips']}")

    print("\nTrayecto de menor distancia:")
    print(result['menor_distancia'])

    print("\nTrayecto de mayor distancia:")
    print(result['mayor_distancia'])

    print("\nPrimeros 5 trayectos:")
    for t in result['first_trips']:
        print(t)

    print("\nÚltimos 5 trayectos:")
    for t in result['last_trips']:
        print(t)

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    fecha_inicio = input("Fecha y hora inicial (YYYY-MM-DD HH:MM:SS): ")
    fecha_fin = input("Fecha y hora final (YYYY-MM-DD HH:MM:SS): ")
    N = int(input("Número de trayectos a mostrar: "))
    result = lg.req_1(control, fecha_inicio, fecha_fin, N)
    print(f"\nTiempo de ejecución: {result['execution_time']} ms")
    print(f"Total de trayectos: {result['total_trips']}")
    print("\nPrimeros trayectos:")
    for t in result['first_trips']:
        print(t)
    print("\nÚltimos trayectos:")
    for t in result['last_trips']:
        print(t)

def print_req_2(control):
    lat_min = float(input("Latitud mínima: "))
    lat_max = float(input("Latitud máxima: "))
    N = int(input("Número de trayectos a mostrar: "))
    result = lg.req_2(control, lat_min, lat_max, N)
    print(f"\nTiempo de ejecución: {result['execution_time']} ms")
    print(f"Total de trayectos: {result['total_trips']}")
    print("\nPrimeros trayectos:")
    for t in result['first_trips']:
        print(t)
    print("\nÚltimos trayectos:")
    for t in result['last_trips']:
        print(t)

def print_req_3(control):
    min_amount = float(input("Monto mínimo: "))
    max_amount = float(input("Monto máximo: "))
    N = int(input("Número de trayectos a mostrar: "))
    result = lg.req_3(control, min_amount, max_amount, N)
    print(f"\nTiempo de ejecución: {result['execution_time']} ms")
    print(f"Total de trayectos: {result['total_trips']}")
    print("\nPrimeros trayectos:")
    for t in result['first_trips']:
        print(t)
    print("\nÚltimos trayectos:")
    for t in result['last_trips']:
        print(t)



def print_req_4(control):
    fecha = input("Fecha de terminación (YYYY-MM-DD): ")
    condicion = input("ANTES o DESPUES del tiempo de referencia: ").upper()
    hora_ref = input("Hora de referencia (HH:MM:SS): ")
    N = int(input("Número de trayectos a mostrar: "))
    result = lg.req_4(control, fecha, condicion, hora_ref, N)
    print(f"\nTiempo de ejecución: {result['execution_time']} ms")
    print(f"Total de trayectos: {result['total_trips']}")
    print("\nPrimeros trayectos:")
    for t in result['first_trips']:
        print(t)
    print("\nÚltimos trayectos:")
    for t in result['last_trips']:
        print(t)


def print_req_5(control):
    fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
    fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
    filtro = input("Filtro (MAYOR o MENOR): ").upper()
    result = lg.req_5(control, fecha_inicio, fecha_fin, filtro)
    print(f"\nTiempo de ejecución: {result['execution_time']} ms")
    print(f"Total de trayectos analizados: {result['total_trips']}")
    print(f"Hora con {filtro} promedio: {result['hora']} -> ${result['promedio']:.2f}")


def print_req_6(control):
    barrio = input("Nombre del barrio: ")
    hora_inicial = input("Hora inicial (0–23): ")
    hora_final = input("Hora final (0–23): ")
    N = int(input("Número de trayectos a mostrar: "))
    
    result = lg.req_6(control, barrio, hora_inicial, hora_final, N)

    print(f"\nTiempo de ejecución: {result['execution_time']} ms")
    print(f"Total de trayectos: {result['total_viajes']}")

    if result["total_viajes"] == 0:
        print(f"\n{result['message']}")
        return

    print("\nPrimeros trayectos encontrados:")
    for t in result["primeros"]:
        print(f"Fecha recogida: {t['pickup_datetime']}")
        print(f"  Coordenadas inicio: {t['pickup_coords']}")
        print(f"Fecha entrega: {t['dropoff_datetime']}")
        print(f"  Coordenadas destino: {t['dropoff_coords']}")
        print(f"  Distancia: {t['trip_distance']} mi")
        print(f"  Valor total: ${t['total_amount']}\n")

    print("Últimos trayectos encontrados:")
    for t in result["ultimos"]:
        print(f"Fecha recogida: {t['pickup_datetime']}")
        print(f"  Coordenadas inicio: {t['pickup_coords']}")
        print(f"Fecha entrega: {t['dropoff_datetime']}")
        print(f"  Coordenadas destino: {t['dropoff_coords']}")
        print(f"  Distancia: {t['trip_distance']} mi")
        print(f"  Valor total: ${t['total_amount']}\n")

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea1, vuelva a elegir.\n")
    sys.exit(0)
