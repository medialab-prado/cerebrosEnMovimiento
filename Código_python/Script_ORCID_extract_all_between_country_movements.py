#!/sur/bin/env python3

import sys
import csv
from centroides.centroides import Centroides
from operator import itemgetter
#import operator


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

#{1234:[('PT', '2012', '2016','EMPLOYMENT'), ('US', '2010', '2012','EDUCATION'), ('US', '2010', '2012','EDUCATION')], 5678:[('GR', '2011', '2016','EMPLOYMENT'), ('RU', '2009', '2011','EDUCATION'), ('ZA', '2005', '2009','EDUCATION')]}
#print(investigadores)
#Imprimimos el diccionario completo de investigadores.

print(investigadores)



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
					trips[inv].append((current_country, stay[0], stay[1]))
				current_country = stay[0]


totals = dict()
for invkey in investigadores.keys():	#Por cada investigador.
	print(invkey)
	for trip in trips[invkey]:			#
		#Aquí nos hemos introducido en la estructura de "trips". Es como si estuviésemos "en el directorio"...
		#Eso hace que llamar a "trip[0]" sea inequívoco y no requiera más especificación. Está determinado por los "for".
		if trip[0] not in totals.keys():
			totals[trip[0]] = dict()		#Entonces creamos la clave ES dentro de totals.

		if trip[1] not in totals[trip[0]].keys():
			totals[trip[0]][trip[1]] = dict()			#dónde: --> totals[i]

		if trip[2] in totals[trip[0]][trip[1]].keys():
			totals[trip[0]][trip[1]][trip[2]] += 1
		else:
			totals[trip[0]][trip[1]][trip[2]] = 1


print(totals)
#{'GB': {'US': {'2000': 1, '1988': 1}, 'CY': {'NA': 1}, 'AU': {'2008': 1}}, 'US': {'GB': {'2002': 1, '1990': 1}, 'IE': {'2015': 1}}, 'CO': {'DE': {'2008': 1}}, 'AO': {'PT': {'1985': 1}}, 'KE': {'DK': {'1999': 1}}, 'IT': {'US': {'2013': 1}}, 'AU': {'GB': {'2002': 1}}}


total_columns = (2016 - 1913 +1 + 1 + 1)
print(total_columns)


header = list()
header = ['', '', ]
header_year = 1913


while header_year <= 2016:
	header.append(str(header_year))
	header_year += 1

print(header)




line = 0

csvfile = open('dummy_output.csv', 'w', newline='')
writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
centroides = Centroides()
#Abrimos un objeto para asignar los centroides mediante la función centroides.

for origin_key in totals.keys():
	for destination_key in totals[origin_key].keys():
		line = list()
		line.append(origin_key) #este lo podríamos haber "appendado" en el paso anterior.
		line.append(centroides.getName(origin_key))
		line.append(centroides.getLong(origin_key))
		line.append(centroides.getLat(origin_key))
		line.append(destination_key)
		line.append(centroides.getName(destination_key))
		line.append(centroides.getLong(destination_key))
		line.append(centroides.getLat(destination_key))
		for year in range(1913, 2017):
			if str(year) in totals[origin_key][destination_key].keys():
				line.append(str(totals[origin_key][destination_key][str(year)]))
			else:
				line.append("0")
		#Guardar en fichero.
		writer.writerow(line)

csvfile.close()


