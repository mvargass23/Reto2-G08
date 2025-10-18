import time
import os
import csv
from datetime import datetime
from DataStructures import array_list as al
from DISClib.ADT import map as m

import sys
default_limit = 1000
sys.setrecursionlimit(default_limit * 10)
csv.field_size_limit(2147483647)

def new_logic():
    catalog = {
        'trips': al.new_list(),         
        'load_time': 0,                  
        'total_trips': 0,                
    }
    return catalog
# Funciones para la carga de datos

def load_data(catalog, filename):
    start = get_time()
    data_dir = os.path.dirname(os.path.realpath('file')) + '/Data/'
    trips = catalog['trips']
    path = data_dir + filename + '.csv'
    reader = csv.DictReader(open(path, encoding='utf-8'))

    menor_dist = None
    mayor_dist = None
    primeros = al.new_list()
    ultimos_buffer = [] 

    for fila in reader:
        pickup_str = fila['pickup_datetime']
        dropoff_str = fila['dropoff_datetime']
        distancia = float(fila['trip_distance'])
        total = float(fila['total_amount'])
        pickup_long = float(fila['pickup_longitude'])
        pickup_lat = float(fila['pickup_latitude'])
        dropoff_long = float(fila['dropoff_longitude'])
        dropoff_lat = float(fila['dropoff_latitude'])

        pickup = datetime.strptime(pickup_str, "%Y-%m-%d %H:%M:%S")
        dropoff = datetime.strptime(dropoff_str, "%Y-%m-%d %H:%M:%S")
        duracion = (dropoff - pickup).total_seconds() / 60  # minutos

        registro = {
            'pickup_datetime': pickup,
            'dropoff_datetime': dropoff,
            'trip_duration': duracion,
            'trip_distance': distancia,
            'pickup_longitude': pickup_long,
            'pickup_latitude': pickup_lat,
            'dropoff_longitude': dropoff_long,
            'dropoff_latitude': dropoff_lat,
            'total_amount': total
        }

        al.add_last(trips, registro)

        if al.size(primeros) < 5:
            al.add_last(primeros, registro)

        ultimos_buffer.append(registro)
        if len(ultimos_buffer) > 5:
            ultimos_buffer.pop(0)

        if distancia > 0:
            if menor_dist is None or distancia < menor_dist['trip_distance']:
                menor_dist = registro
            if mayor_dist is None or distancia > mayor_dist['trip_distance']:
                mayor_dist = registro

    ultimos = al.new_list()
    for t in ultimos_buffer:
        al.add_last(ultimos, t)

    total_trips = al.size(trips)
    end = get_time()

    if total_trips == 0:
        return {
            'execution_time': round(delta_time(start, end), 3),
            'total_trips': 0,
            'message': 'No se cargaron trayectos válidos.'
        }

    return {
        'execution_time': round(delta_time(start, end), 3),
        'total_trips': total_trips,
        'menor_distancia': {
            'pickup_datetime': menor_dist['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'trip_distance': round(menor_dist['trip_distance'], 2),
            'total_amount': round(menor_dist['total_amount'], 2)
        },
        'mayor_distancia': {
            'pickup_datetime': mayor_dist['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'trip_distance': round(mayor_dist['trip_distance'], 2),
            'total_amount': round(mayor_dist['total_amount'], 2)
        },
        'first_trips': [{
            'pickup_datetime': t['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'dropoff_datetime': t['dropoff_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'trip_duration': round(t['trip_duration'], 2),
            'trip_distance': round(t['trip_distance'], 2),
            'total_amount': round(t['total_amount'], 2)
        } for t in primeros['elements']],
        'last_trips': [{
            'pickup_datetime': t['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'dropoff_datetime': t['dropoff_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'trip_duration': round(t['trip_duration'], 2),
            'trip_distance': round(t['trip_distance'], 2),
            'total_amount': round(t['total_amount'], 2)
        } for t in ultimos['elements']]
    }


def req_1(catalog, fecha_inicio_str, fecha_fin_str, N):
    start = get_time()
    trips = catalog['trips']

    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d %H:%M:%S")

    filtrados = al.new_list()
    for i in range(al.size(trips)):
        t = al.get_element(trips, i)
        if fecha_inicio <= t['pickup_datetime'] <= fecha_fin:
            al.add_last(filtrados, t)

    total = al.size(filtrados)
    if total == 0:
        end = get_time()
        return {
            'execution_time': round(delta_time(start, end), 3),
            'total_trips': 0,
            'message': 'No se encontraron trayectos en la franja de tiempo dada.'
        }

    for i in range(1, total):
        actual = al.get_element(filtrados, i)
        j = i - 1
        while j >= 0 and al.get_element(filtrados, j)['pickup_datetime'] > actual['pickup_datetime']:
            anterior = al.get_element(filtrados, j)
            filtrados['elements'][j + 1] = anterior
            j -= 1
        filtrados['elements'][j + 1] = actual

    N = N if total >= 2 * N else total // 2
    primeros = al.new_list()
    ultimos = al.new_list()

    for i in range(N):
        t = al.get_element(filtrados, i)
        al.add_last(primeros, {
            'pickup_datetime': t['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'pickup_coord': [t['pickup_latitude'], t['pickup_longitude']],
            'dropoff_datetime': t['dropoff_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'dropoff_coord': [t['dropoff_latitude'], t['dropoff_longitude']],
            'trip_distance': round(t['trip_distance'], 2),
            'total_amount': round(t['total_amount'], 2)
        })

    for i in range(total - N, total):
        t = al.get_element(filtrados, i)
        al.add_last(ultimos, {
            'pickup_datetime': t['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'pickup_coord': [t['pickup_latitude'], t['pickup_longitude']],
            'dropoff_datetime': t['dropoff_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'dropoff_coord': [t['dropoff_latitude'], t['dropoff_longitude']],
            'trip_distance': round(t['trip_distance'], 2),
            'total_amount': round(t['total_amount'], 2)
        })

    end = get_time()
    return {
        'execution_time': round(delta_time(start, end), 3),
        'total_trips': total,
        'first_trips': primeros,
        'last_trips': ultimos
    }


def req_2(catalog, lat_min, lat_max, N):
    pass

def req_3(catalog):
    pass


def req_4(catalog, fecha_str, condicion, hora_ref_str, N):
    start = get_time()
    trips = catalog['trips']

    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    hora_ref = datetime.strptime(hora_ref_str, "%H:%M:%S").time()

    tabla_fechas = m.new_map(100, maptype='PROBING')

    for i in range(al.size(trips)):
        t = al.get_element(trips, i)
        fecha_termina = t['dropoff_datetime'].date()
        entry = m.get(tabla_fechas, fecha_termina)
        if entry:
            lista = entry['value']
            al.add_last(lista, t)
        else:
            nueva_lista = al.new_list()
            al.add_last(nueva_lista, t)
            m.put(tabla_fechas, fecha_termina, nueva_lista)

    entry = m.get(tabla_fechas, fecha_obj)
    if not entry:
        end = get_time()
        return {
            'execution_time': round(delta_time(start, end), 3),
            'total_trips': 0,
            'message': 'No se encontraron trayectos en la fecha indicada.'
        }

    lista_fecha = entry['value']

    filtrados = al.new_list()
    for i in range(al.size(lista_fecha)):
        t = al.get_element(lista_fecha, i)
        hora_fin = t['dropoff_datetime'].time()
        if condicion == "ANTES" and hora_fin < hora_ref:
            al.add_last(filtrados, t)
        elif condicion == "DESPUES" and hora_fin > hora_ref:
            al.add_last(filtrados, t)

    total = al.size(filtrados)
    if total == 0:
        end = get_time()
        return {
            'execution_time': round(delta_time(start, end), 3),
            'total_trips': 0,
            'message': 'No se encontraron trayectos que cumplan la condición indicada.'
        }

    for i in range(1, total):
        actual = al.get_element(filtrados, i)
        j = i - 1
        while j >= 0 and al.get_element(filtrados, j)['dropoff_datetime'] < actual['dropoff_datetime']:
            anterior = al.get_element(filtrados, j)
            filtrados['elements'][j + 1] = anterior
            j -= 1
        filtrados['elements'][j + 1] = actual

    N = N if total >= 2 * N else total // 2
    primeros = al.new_list()
    ultimos = al.new_list()

    for i in range(N):
        t = al.get_element(filtrados, i)
        al.add_last(primeros, {
            'pickup_datetime': t['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'pickup_coord': [t['pickup_latitude'], t['pickup_longitude']],
            'dropoff_datetime': t['dropoff_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'dropoff_coord': [t['dropoff_latitude'], t['dropoff_longitude']],
            'trip_distance': round(t['trip_distance'], 2),
            'total_amount': round(t['total_amount'], 2)
        })

    for i in range(total - N, total):
        t = al.get_element(filtrados, i)
        al.add_last(ultimos, {
            'pickup_datetime': t['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'pickup_coord': [t['pickup_latitude'], t['pickup_longitude']],
            'dropoff_datetime': t['dropoff_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
            'dropoff_coord': [t['dropoff_latitude'], t['dropoff_longitude']],
            'trip_distance': round(t['trip_distance'], 2),
            'total_amount': round(t['total_amount'], 2)
        })

    end = get_time()
    return {
        'execution_time': round(delta_time(start, end), 3),
        'total_trips': total,
        'first_trips': primeros,
        'last_trips': ultimos
    }
    

def req_5(catalog, fecha_inicio_str, fecha_fin_str, filtro):
    start = get_time()
    trips = catalog['trips']
    fecha_i = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
    fecha_f = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
    franjas = al.new_list()
    for h in range(24):
        al.add_last(franjas, [h, 0, 0])
    for i in range(al.size(trips)):
        t = al.get_element(trips, i)
        fecha = t['pickup_datetime'].date()
        if fecha_i <= fecha <= fecha_f:
            hora = t['pickup_datetime'].hour
            par = al.get_element(franjas, hora)
            par[1] += t['total_amount']
            par[2] += 1
    mejor_hora, mejor_prom = None, None
    for i in range(al.size(franjas)):
        hora, suma, n = al.get_element(franjas, i)
        if n > 0:
            prom = suma / n
            if mejor_prom is None:
                mejor_hora, mejor_prom = hora, prom
            else:
                if filtro == "MAYOR" and prom > mejor_prom:
                    mejor_hora, mejor_prom = hora, prom
                elif filtro == "MENOR" and prom < mejor_prom:
                    mejor_hora, mejor_prom = hora, prom
    end = get_time()
    return {
        'execution_time': round(delta_time(start, end), 3),
        'mejor_hora': mejor_hora,
        'promedio_total': round(mejor_prom, 2)
    }

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
