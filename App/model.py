﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import datetime as dt
import time
import math
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import shellsort as ss
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
#========================
# Construccion de modelos
#========================

def newAnalyzer():
    analyzer = {'ufos': None,
                'cityIndex': None,
                'durationIndex': None,
                'datetimeIndex': None,
                'longitudeIndex':None,
                }

    analyzer['ufos'] = lt.newList(datastructure = 'ARRAY_LIST', cmpfunction = cmpListDate)
    
    analyzer['cityIndex'] = mp.newMap(500,
                                    maptype = 'PROBING',
                                    loadfactor = 0.5,
                                    comparefunction = cmpMapCity)

    analyzer['durationIndex'] = om.newMap(omaptype = 'RBT', comparefunction = cmpMapDuration)

    analyzer['datetimeIndex'] = om.newMap(omaptype = 'RBT', comparefunction = cmpMapDate)

    analyzer['longitudeIndex'] = om.newMap(omaptype = 'RBT', comparefunction = cmpMapLongitude)

    return analyzer

#===============================================
# Funciones para agregar informacion al catalogo
#===============================================
def addUfo(analyzer, ufo):
    lt.addLast(analyzer['ufos'], ufo)
    Requerimiento1(analyzer['cityIndex'], ufo)
    Requerimiento2(analyzer['durationIndex'], ufo)
    Requerimiento4(analyzer['datetimeIndex'], ufo)
    Requerimiento5(analyzer['longitudeIndex'], ufo)
    
    return analyzer

def Requerimiento1(mapa, ufo): #IMPORTANTE!!! Escogí una tabla de hash para hacer este requerimiento por lo cual no puedo retornar nada de info de árboles. Fue recomendado por el profesor y de hecho ya está completamente implementado
    city = ufo['city']
    llave_valor = mp.get(mapa, city)
    
    if llave_valor is None:
        lt_ufos2 = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lt_ufos2, ufo)
        mp.put(mapa, city, lt_ufos2)
    
    else:
        lt_ufos_valor = me.getValue(llave_valor)
        lt.addLast(lt_ufos_valor, ufo)

    return mapa

def Requerimiento2(mapa, ufo):
    duration = float(ufo['duration (seconds)'])
    llave_valor = om.get(mapa, duration)

    if llave_valor is None:
        lt_ufos2 = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lt_ufos2, ufo)
        om.put(mapa, duration, lt_ufos2)

    else:
        lt_ufos_valor = me.getValue(llave_valor)
        lt.addLast(lt_ufos_valor, ufo)

    return mapa

def Requerimiento4(mapa, ufo):
    datetime = ufo['datetime']
    datetime2 = dt.datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S')
    llave_valor = om.get(mapa, str(datetime2.date()))

    if llave_valor is None:
        lt_ufos2 = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lt_ufos2, ufo)
        om.put(mapa, str(datetime2.date()), lt_ufos2)
    
    else:
        lt_ufos_valor = me.getValue(llave_valor)
        lt.addLast(lt_ufos_valor, ufo)

    return mapa

def Requerimiento5(mapa, ufo):
    longitude = ufo['longitude']
    llave_valor = om.get(mapa, longitude)

    if llave_valor is None:
        lt_ufos2 = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lt_ufos2, ufo)
        om.put(mapa, longitude, lt_ufos2)

    else:
        lt_ufos_valor = me.getValue(llave_valor)
        lt.addLast(lt_ufos_valor, ufo)

    return mapa

#=================================
# Funciones para creacion de datos
#=================================
def getUfosByCity(mapa, ciudad):
    keys_ciudades = mp.keySet(mapa)
    total_ciudades = lt.size(keys_ciudades)

    llave_valor_ciudad = mp.get(mapa, ciudad)
    lt_ciudad = me.getValue(llave_valor_ciudad)
    total_casos_ciudad = lt.size(lt_ciudad)
    
    lt_ciudad_ord = ms.sort(lt_ciudad, cmpUfosByDate)

    i = 1
    primeros_3 = lt.newList()
    while i <= 3:
        x = lt.getElement(lt_ciudad_ord, i)
        lt.addLast(primeros_3, x)
        i += 1

    j = 2
    ultimos_3 = lt.newList()
    while j >= 0:
        x = lt.getElement(lt_ciudad_ord, total_casos_ciudad - j)
        lt.addLast(ultimos_3, x)
        j -= 1

    return total_ciudades, total_casos_ciudad, primeros_3, ultimos_3

def getUfosByDuration(mapa, limit_inf, limit_sup):
    total_duraciones = om.size(mapa)
    lt_valores = om.values(mapa, float(limit_inf), float(limit_sup))

    contador_ufos = 0
    lt_ufos_rango = lt.newList(datastructure = 'ARRAY_LIST')
    for lista in lt.iterator(lt_valores):
        for ufo in lt.iterator(lista):
            contador_ufos += 1
            lt.addLast(lt_ufos_rango, ufo)
    
    lt_ufos_rango_ord = ms.sort(lt_ufos_rango, cmpUfosByDate)
    tam = lt.size(lt_ufos_rango_ord)

    i = 1
    primeros_3 = lt.newList()
    while i <= 3:
        x = lt.getElement(lt_ufos_rango_ord, i)
        lt.addLast(primeros_3, x)
        i += 1

    j = 2
    ultimos_3 = lt.newList()
    while j >= 0:
        x = lt.getElement(lt_ufos_rango_ord, tam - j)
        lt.addLast(ultimos_3, x)
        j -= 1

    for ufo in lt.iterator(primeros_3):
        if ufo['state'] == '':
            ufo['state'] = 'Not Available'

    for ufo in lt.iterator(ultimos_3):
        if ufo['state'] == '':
            ufo['state'] = 'Not Available'

    return total_duraciones, contador_ufos, primeros_3, ultimos_3

def getUfosByDatetime(mapa, limit_inf, limit_sup):
    total_datetime = om.size(mapa)
    lt_valores = om.values(mapa, limit_inf, limit_sup)

    contador_ufos = 0
    lt_ufos_rango = lt.newList(datastructure = 'ARRAY_LIST')
    for lista in lt.iterator(lt_valores):
        for ufo in lt.iterator(lista):
            contador_ufos += 1
            lt.addLast(lt_ufos_rango, ufo)
    
    lt_ufos_rango_ord = ms.sort(lt_ufos_rango, cmpUfosByDate)
    tam = lt.size(lt_ufos_rango_ord)

    i = 1
    primeros_3 = lt.newList()
    while i <= 3:
        x = lt.getElement(lt_ufos_rango_ord, i)
        lt.addLast(primeros_3, x)
        i += 1

    j = 2
    ultimos_3 = lt.newList()
    while j >= 0:
        x = lt.getElement(lt_ufos_rango_ord, tam - j)
        lt.addLast(ultimos_3, x)
        j -= 1

    for ufo in lt.iterator(primeros_3):
        if ufo['state'] == '':
            ufo['state'] = 'Not Available'

    for ufo in lt.iterator(ultimos_3):
        if ufo['state'] == '':
            ufo['state'] = 'Not Available'

    return total_datetime, contador_ufos, primeros_3, ultimos_3

def getUfosByLonLat(mapa, lon_inf, lon_sup, lat_inf, lat_sup):
    lt_valores_lon = om.values(mapa, lon_inf, lon_sup)

    lt_ufos_rango = lt.newList(datastructure = 'ARRAY_LIST')
    for lista in lt.iterator(lt_valores_lon):
        for ufo in lt.iterator(lista):
            latitud = round(float(ufo['latitude']),2)
            if float(lat_inf) <= latitud <= float(lat_sup):
                lt.addLast(lt_ufos_rango, ufo)
    
    total_lon_lat = lt.size(lt_ufos_rango)

    lt_ufos_rango_ord = ms.sort(lt_ufos_rango, cmpUfosByDate)

    i = 1
    primeros_5 = lt.newList(datastructure = 'ARRAY_LIST')
    while i <= 5:
        x = lt.getElement(lt_ufos_rango_ord, i) 
        lt.addLast(primeros_5, x)
        i += 1

    j = 4
    ultimos_5 = lt.newList(datastructure = 'ARRAY_LIST')
    while j >= 0:
        x = lt.getElement(lt_ufos_rango_ord, total_lon_lat - j)
        lt.addLast(ultimos_5, x)
        j -= 1

    return total_lon_lat, primeros_5, ultimos_5

#======================
# Funciones de consulta
#======================
def ufosSize(analyzer):

    return lt.size(analyzer['ufos'])

#=================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
#=================================================================
def cmpListDate(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def cmpMapCity(keyname, city):
    city_entry = me.getKey(city)
    if (keyname == city_entry):
        return 0
    elif (keyname > city_entry):
        return 1
    else:
        return -1

def cmpMapDuration(duracion1, duracion2):
    if (duracion1 == duracion2):
        return 0
    elif (duracion1 > duracion2):
        return 1
    else:
        return -1

def cmpMapDate(dateufo1, dateufo2):
    if (dateufo1 == dateufo2):
        return 0
    elif (dateufo1 > dateufo2):
        return 1
    else:
        return -1

def cmpMapLongitude(longitude1, longitude2):
    if (longitude1 == longitude2):
        return 0
    elif (longitude1 > longitude2):
        return 1
    else:
        return -1

def cmpUfosByDate(ufo1, ufo2):
    dateufo1 = ufo1['datetime']
    dateufo2 = ufo2['datetime']

    if dateufo1 == '':
        dateufo1 = '0001-01-01 00:00:00'

    if dateufo2 == '':
        dateufo2 = '0001-01-01 00:00:00'

    if (dt.datetime.strptime(dateufo1, '%Y-%m-%d %H:%M:%S')) < (dt.datetime.strptime(dateufo2, '%Y-%m-%d %H:%M:%S')):
        return 1
    
    else:
        return 0
      
#==========================
# Funciones de ordenamiento
#==========================