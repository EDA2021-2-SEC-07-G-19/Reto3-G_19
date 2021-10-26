"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
import prettytable as pt
from prettytable import PrettyTable, ALL
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

#===================
#Ruta a los archivos
#===================
ufosfile = 'UFOS//UFOS-utf8-small.csv'
cont = None

#==============
#Menú Principal
#==============
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de ufos")
    print("3- Requerimiento 1")
    print("4- Requerimiento 2")
    print("5- Requerimiento 3")
    print("6- Requerimiento 4")
    print("7- Requerimiento 5")
    print("0- Salir")
    print("*******************************************")

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')
    
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de ufos ....")
        controller.loadData(cont, ufosfile)
        
        total_ufos = lt.size(cont['ufos'])

        i = 1
        primeros_5 = lt.newList()
        while i <= 5:
            x = lt.getElement(cont['ufos'], i) 
            lt.addLast(primeros_5, x)
            i += 1

        j = 4
        ultimos_5 = lt.newList()
        while j >= 0:
            x = lt.getElement(cont['ufos'], total_ufos - j)
            lt.addLast(ultimos_5, x)
            j -= 1

        print('Casos de ufos cargados: ' + str(controller.ufosSize(cont)))
        
        print('The first 5 ufo cases are:')   

        tabla1 = pt.PrettyTable(['Datetime', 'City', 'State', 'Country', 'Shape', 'Duration (seconds)', 'Duration (hours/min)', 'Comments', 'Date Posted', 'Latitude', 'Longitude'])

        tabla1.max_width = 8

        for ufo in lt.iterator(primeros_5):
            tabla1.add_row([ufo['datetime'], ufo['city'], ufo['state'], ufo['country'], ufo['shape'], ufo['duration (seconds)'], ufo['duration (hours/min)'], ufo['comments'], ufo['date posted'], ufo['latitude'], ufo['longitude']])

        tabla1.hrules = ALL

        print(tabla1)
        print('\n')

        print('The last 5 ufo cases are:')

        tabla2 = pt.PrettyTable(['Datetime', 'City', 'State', 'Country', 'Shape', 'Duration (seconds)', 'Duration (hours/min)', 'Comments', 'Date Posted', 'Latitude', 'Longitude'])

        tabla2.max_width = 8

        for obra in lt.iterator(ultimos_5):
            tabla2.add_row([ufo['datetime'], ufo['city'], ufo['state'], ufo['country'], ufo['shape'], ufo['duration (seconds)'], ufo['duration (hours/min)'], ufo['comments'], ufo['date posted'], ufo['latitude'], ufo['longitude']])

        tabla2.hrules = ALL

        print(tabla2)
    
    elif int(inputs[0]) == 3:
        mapa = cont['cityIndex']

        ciudad = input('Ingrese el nombre de la ciudad sobre la cual desea calcular los casos de ufos: \n>')
        ciudad_def = ciudad.lower()

        requerimiento1 = controller.Requerimiento1(mapa, ufo)
        getUfos = controller.getUfosByCity(requerimiento1, ciudad_def)

        print('=============== Req No. 1 Inputs ===============')
        print('UFO Sightings in the city of ' + str(ciudad.upper()) + '\n')
        print('=============== Req No. 1 Answer ===============')
        print('There are ' + str(getUfos[0]) + ' different cities with UFO Sightings' + '\n')
        print('There are ' + str(getUfos[1]) + ' sightings at the: ' + str(ciudad.upper()) + ' city')
        print('The first 3 and last 3 UFO sightings in the city are: ')

    else:
        sys.exit(0)
sys.exit(0)
