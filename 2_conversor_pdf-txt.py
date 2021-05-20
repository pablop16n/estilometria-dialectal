import PyPDF2
import re
 
abrir = open('TU_RUTA_DE_DIRECTORIO/entrevistas.txt', 'r', encoding='utf8')
entrevistas = abrir.readlines()#Leemos la información de las entrevistas
abrir.close()
entrevistas = "\n".join(entrevistas)
nombres = re.findall('\w+_\w+_\d+', entrevistas)#Encontramos los nombres que les hemos dado nosotros

for nombre in nombres:
    pdf = open("TU_RUTA_DE_DIRECTORIO/entrevistas_originales_pdf/" + nombre + ".pdf", 'rb')#Se abre cada pdf
    lector_pdf = PyPDF2.PdfFileReader(pdf)#La librería los lee y almacena
    i = 0
    texto = ''
    while i < lector_pdf.numPages:#Va extrayendo cada página y luego cada texto y lo almacena todo en "texto"
        temporal = lector_pdf.getPage(i)
        texto_temporal = temporal.extractText()
        texto = texto + ' ' + texto_temporal
        i=i+1
    pdf.close()
    texto = re.sub('\n', '', texto)#Quita los saltos de línea porque no tienen ninguna lógica (no sé si es problema de la librería o de los pdfs)
    nuevo = open("TU_RUTA_DE_DIRECTORIO/entrevistas_originales_txt/" + nombre + ".txt", 'w+')#Crea un archivo por cada entrevista
    nuevo.write(texto)#Guarda todo el contenido en su archivo_correspondiente.txt
    nuevo.close()
    