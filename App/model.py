"""
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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
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
                }

    analyzer['ufos'] = lt.newList(datastructure = 'ARRAY_LIST', cmpfunction = cmpListDate)
    
    analyzer['cityIndex'] = mp.newMap(500,
                                    maptype = 'PROBING',
                                    loadfactor = 0.5,
                                    comparefunction = cmpMapCity)

    return analyzer

#===============================================
# Funciones para agregar informacion al catalogo
#===============================================
def addUfo(analyzer, ufo):
    lt.addLast(analyzer['ufos'], ufo)
    Requerimiento1(analyzer['cityIndex'], ufo)
    
    return analyzer

def Requerimiento1(mapa, ufo):
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

#=================================
# Funciones para creacion de datos
#=================================
def getUfosByCity(mapa, ciudad):
    keys_ciudades = mp.keySet(mapa)
    total_ciudades = lt.size(keys_ciudades)

    llave_valor_ciudad = mp.get(mapa, ciudad)
    lt_ciudad = me.getValue(llave_valor_ciudad)
    total_casos_ciudad = lt.size(lt_ciudad)

    return total_ciudades, total_casos_ciudad

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

#==========================
# Funciones de ordenamiento
#==========================