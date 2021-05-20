import re
import urllib.request
abrir = open('TU_RUTA_DE_DIRECTORIO/entrevistas.txt', 'r', encoding='utf8')
entrevistas = abrir.readlines()#Leo el archivo con la información de las entrevistas

for linea in entrevistas:
    nombre = re.findall('\w+_\w+_\d+', linea) #Por cada entrevista extraigo el nombre que le hemos dado y
    codigo = re.findall('COSER-\d+-\d+', linea) #el código que le da el COSER
    nombre = nombre[0]#Trasformo la lista en cadena de texto
    codigo = codigo[0]#Idem
    indices = re.findall('\d\d', linea)#Busco el código que diferencia la entrevista 01, 02, 03, etc. de la misma localidad
    #En el COSER las entrevistas 01 tienen distinta estructura de url que el resto, así que evalúo -
    #- si estamos en la primera o la segunda y adapto la url
    if indices[2] == '01':
        url_origen = 'http://www.corpusrural.es/coser/archivos/pdf/' + indices[0] + '_' + indices[1] + '_es.pdf'
    else:
        url_origen = 'http://www.corpusrural.es/coser/archivos/pdf/' + indices[0] + '_' + indices[1] + '_' + indices[2] + '_'+ 'es.pdf'  
    urllib.request.urlretrieve(url_origen, 'TU_RUTA_DE_DIRECTORIO/entrevistas_originales_pdf/'+ nombre +'.pdf')#La librería ya hace su magia y descarga los pdfs

abrir.close()
