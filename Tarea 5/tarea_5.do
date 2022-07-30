global DATA = "C:\Users\Hp Support\Videos\03 - Cursos\05 - Herramientas computacionales\Clase 5 - Data Visualization\videos 2 y 3\data" 
cd "$DATA"

********************************************************************************************
/* 					  INSTALACIÓN DE LOS PAQUETES NECESARIOS    						  */
********************************************************************************************

ssc install spmap
ssc install shp2dta
net install spwmatrix, from(http://fmwww.bc.edu/RePEc/bocode/s)

* Leer la información shape en Stata

shp2dta using london_sport.shp, database(ls) coord(coord_ls) genc(c) genid(id) replace

use ls, clear
describe

use coord_ls, clear
describe

/* Importamos y transformamos los datos de Excel a formato Stata */
import delimited "$DATA/mps-recordedcrime-borough.csv", clear 
* En Stata necesitamos que la variable tenga el mismo nombre en ambas bases para juntarlas
rename borough name
* preserve
collapse (sum) crimecount, by(name)
save "crime.dta", replace

describe

/* Uniremos ambas bases: london_sport y crime. Su usa la función merge con la variable name que se encuentra en ambas bases  */

use ls, clear
merge 1:1 name using crime.dta
*merge 1:1 name using crime.dta, keep(3) nogen
*keep if _m==3
drop _m

save london_crime_shp.dta, replace

************************************************************************************
* Representación por medio de mapas

use london_crime_shp.dta, clear

* Mapa de cuantiles:
spmap crimecount using coord_ls, id(id) clmethod(q) cln(6)

spmap crimecount using coord_ls, id(id) clmethod(q) cln(6) title("Número de crímenes") legend(size(medium) position(5) xoffset(15.05)) fcolor(Blues2) plotregion(margin(b+15)) ndfcolor(gray) name(g1,replace)  

