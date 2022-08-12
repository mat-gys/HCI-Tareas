En este repositorio, en la carpeta de output, se encuentran:
- Un csv con la matriz OD realizada con QNEAT3 en QGIS entre las capitales de los departamentos de Corrientes, Argentina
- Dos mapas con la ruta más corta entre dos ciudades de Corrientes realizada con la herramiento Shortest path de QNEAT3

## Requisitos
- MMQGIS
- QNEAT3

## Inputs

En la carpeta input se encuentran todos los archivos necesarios para replicar los outputs. Por un lado, está la red vial de Corrientes disponible en [WayBack Machine](https://eb.archive.org/web/20200915000000*/https://datos.transporte.gob.ar/dataset/rutas-provinciales). Por otro lado, en el archivo csv se encuentran los datos necesarios para georeferenciar los departamentos de corrientes con el programa MMQGIS. Por último, en el archivo "arg_admbnda_adm2_unhcr2017.shp" se encuentran los boundries en Argentina obtenidos de [Humanitarian Data Exchange](https://data.humdata.org/dataset/cod-ab-arg).
