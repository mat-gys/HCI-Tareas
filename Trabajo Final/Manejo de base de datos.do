global INPUT "C:\Users\Hp Support\Videos\03 - Cursos\05 - Herramientas computacionales\Trabajo Final - replicate paper"

cd "C:\Users\Hp Support\Videos\03 - Cursos\05 - Herramientas computacionales\Trabajo Final - replicate paper\dataverse_files"

use figures1_3_4_data, clear
** 

bys muncod: gen n=_n // ordenamos por código de municipalidad y se asigna un número a cada código
// como hay 16 años entre 1995 y 2010 se asignan números del 1 al 16.  
keep if n==1 // cómo los datos son sólo para un año, el porcentaje de participación se repite en cada
// fila de por cada municipio. Entonces, sólo nos quedamos con un dato. 
drop n // eliminamos ya que no es relevante

**tostring muncod, gen(id_muncod)

**gen id=substr(id_muncod,-3,3)

export delimited using "C:\Users\Hp Support\Videos\03 - Cursos\05 - Herramientas computacionales\Trabajo Final - replicate paper\bd.csv", replace