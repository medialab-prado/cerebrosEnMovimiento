#!/sur/bin/env python3

import sys
import csv
from centroides.centroides import Centroides
from operator import itemgetter

fileobject = open('/home/katorien/Desktop/Filtrar_por_ID/migraciones_filtradas.csv')
#Abrimos el archivo que leer.

investigadores_raw_data = csv.reader(fileobject)
investigadores_raw_data = [row for row in investigadores_raw_data if row != []]
fileobject.close()
#Hemos generado un objeto que contiene los datos. Cerramos el fichero de origen (ya no lo necesitamos).

#print(investigaodres_raw_data)






investigadores = dict()
for inv in investigadores_raw_data:
	#print(inv[2])
	if inv[2] in investigadores.keys():
		investigadores[inv[2]].append((inv[3], inv[6], inv[7], inv[8]))
	else:
		investigadores[inv[2]] = [(inv[3], inv[6], inv[7], inv[8])]
#Aquí generamos el diccionario completo Investigadores.

#print(investigadores)
#Imprimimos el diccionario completo de investigadores.

#{1234:[('PT', '2012', '2016','EMPLOYMENT'), ('US', '2010', '2012','EDUCATION'), ('US', '2010', '2012','EDUCATION')], 5678:[('GR', '2011', '2016','EMPLOYMENT'), ('RU', '2009', '2011','EDUCATION'), ('ZA', '2005', '2009','EDUCATION')]}


trips = dict()
#Creamos el diccionario que almacenará todo.
for inv in investigadores.keys():
	investigadores[inv].sort(key=itemgetter(1))    #Aquí ordenamos.
	trips[inv] = []
	#Creamos claves sin valores asociados, por cada pasada del iterados "inv".
	if len(investigadores[inv]) > 1:
		current_country = "" #Definimos la variable.
		
		for i, stay in enumerate(investigadores[inv]):
			if i == 0:
				current_country = stay[0]
			else:
				if current_country != stay[0]:
					trips[inv].append((current_country, stay[0], stay[1], stay[3]))
				current_country = stay[0]
				print(trips[inv])



totals_edu = dict()
for invkey in investigadores.keys():	#Por cada investigador.
	for trip in trips[invkey]:
		print(trip)
		if trip[3] == 'EDUCATION':
			#print(trip[0])
			#Aquí nos hemos introducido en la estructura de "trips". Es como si estuviésemos "en el directorio"...
			#Eso hace que llamar a "trip[0]" sea inequívoco y no requiera más especificación. Está determinado por los "for".
			if trip[0] not in totals_edu.keys():
				totals_edu[trip[0]] = dict()		#Entonces creamos la clave ... dentro de totals_edu.

			if trip[1] not in totals_edu[trip[0]].keys():
				totals_edu[trip[0]][trip[1]] = dict()			#dónde: --> totals_edu[i]

			if trip[2] in totals_edu[trip[0]][trip[1]].keys():
				totals_edu[trip[0]][trip[1]][trip[2]] += 1
			else:
				totals_edu[trip[0]][trip[1]][trip[2]] = 1
		




totals_work = dict()
for invkey in investigadores.keys():	#Por cada investigador.
	for trip in trips[invkey]:			#
		if trip[3] == 'EMPLOYMENT':
			#print(trip[0])
			#Aquí nos hemos introducido en la estructura de "trips". Es como si estuviésemos "en el directorio"...
			#Eso hace que llamar a "trip[0]" sea inequívoco y no requiera más especificación. Está determinado por los "for".
			if trip[0] not in totals_work.keys():
				totals_work[trip[0]] = dict()		#Entonces creamos la clave ES dentro de totals.

			if trip[1] not in totals_work[trip[0]].keys():
				totals_work[trip[0]][trip[1]] = dict()			#dónde: --> totals[i]

			if trip[2] in totals_work[trip[0]][trip[1]].keys():
				totals_work[trip[0]][trip[1]][trip[2]] += 1
			else:
				totals_work[trip[0]][trip[1]][trip[2]] = 1


total_columns = (2016 - 1913 +1 + 1 + 1)
#print(total_columns)
#El header se hace directamente en Excel.


line = 0

csvfile_education = open('migrados_por_estudios.csv', 'w', newline='')
csvfile_work = open('migrados_por_empleo.csv', 'w', newline='')
writer_education = csv.writer(csvfile_education, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer_work = csv.writer(csvfile_work, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

centroides = Centroides()
#Abrimos un objeto para asignar los centroides mediante la función centroides.

for origin_key_edu in totals_edu.keys():
	for destination_key_edu in totals_edu[origin_key_edu].keys():
		line_edu = list()
		line_edu.append(origin_key_edu) #este lo podríamos haber "appendado" en el paso anterior.
		line_edu.append(centroides.getName(origin_key_edu))
		line_edu.append(centroides.getLong(origin_key_edu))
		line_edu.append(centroides.getLat(origin_key_edu))
		line_edu.append(destination_key_edu)
		line_edu.append(centroides.getName(destination_key_edu))
		line_edu.append(centroides.getLong(destination_key_edu))
		line_edu.append(centroides.getLat(destination_key_edu))
		for year in range(1913, 2017):
			if str(year) in totals_edu[origin_key_edu][destination_key_edu].keys():
				line_edu.append(str(totals_edu[origin_key_edu][destination_key_edu][str(year)]))
			else:
				line_edu.append("0")
		#Guardar en fichero.
		writer_education.writerow(line_edu)


for origin_key_work in totals_work.keys():
	for destination_key_work in totals_work[origin_key_work].keys():
		line_work = list()
		line_work.append(origin_key_work) #este lo podríamos haber "appendado" en el paso anterior.
		line_work.append(centroides.getName(origin_key_work))
		line_work.append(centroides.getLong(origin_key_work))
		line_work.append(centroides.getLat(origin_key_work))
		line_work.append(destination_key_work)
		line_work.append(centroides.getName(destination_key_work))
		line_work.append(centroides.getLong(destination_key_work))
		line_work.append(centroides.getLat(destination_key_work))
		for year in range(1913, 2017):
			if str(year) in totals_work[origin_key_work][destination_key_work].keys():
				line_work.append(str(totals_work[origin_key_work][destination_key_work][str(year)]))
			else:
				line_work.append("0")
		#Guardar en fichero.
		writer_work.writerow(line_work)





csvfile_education.close()
csvfile_work.close()