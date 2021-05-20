import re

#------------------------Funciones-----------------
def extraer_interlocutor(interlocutor, texto):
    #Parámetro 1: código del interlocutor de interés
    #Parámetro 2: entrevista completa
    #Devuelve: cada intervención separada por un salto de línea (str)
    encabezado = re.search(".*?\(?COSER-\d+-\d+-?\d?\d?\)?", texto) #Extrae encabezado de cada página
    encabezado = re.escape(encabezado[0])#Convierte los caracteres extraños en texto manejable
    texto = re.sub(encabezado, "", texto) #Elimina encabezado
    texto = re.sub("(( |^)\d+ )", "", texto) #Elimina paginación y metadatos circunstanciales
    texto = re.sub("\'", '(comilla)', texto)#Sustituye las comillas para que no molesten a continuación
    texto = re.sub('\[([\s\w:\-áéíóúÁÉÍÓÚñÑ\.\,\¿\?\¡\!\"\“\”\|\-\/\(\)])+?\]', '', texto)#Elimina anotaciones (habla solapada, ininteligible, etc.)
    texto = re.sub('\[([\s\w:\-áéíóúÁÉÍÓÚñÑ\.\,\¿\?\¡\!\"\“\”\|\-\/\(\)])+?\]', '', texto)
    texto = re.sub('\[([\s\w:\-áéíóúÁÉÍÓÚñÑ\.\,\¿\?\¡\!\"\“\”\|\-\/\(\)])+?\]', '', texto)#3 veces, porque hay hasta 3 anidaciones [A:texto[B:texto[D:texto]]]
    texto = re.sub("\(comilla\)", '\'', texto)#Devuelve las comillas a su estado original
    texto = re.sub("\|T[\d][\d]?\|", '', texto)#Elimina anotaciones sobre temas tratados
    texto = re.sub("\|", '', texto)#Elimina anotaciones de pausas
    texto = re.sub("\]", '', texto)#Elimina algunos fallos de las anotaciones
    texto = re.sub("(^| )([\wáéíóúñÁÉÍÓÚÑ])*?\-", '', texto)#Elimina palabras entrecortadas
    extracto = re.findall(interlocutor+':(.*?)([EI]\d?:)|($)', texto)#Se extrae todo lo que hay entre el interlocutor y el siguiente interviniente
    extracto = extracto[1:len(extracto)] #Se elimina el primer resultado porque es un metadato
    limpio = ""
    for linea, termino, final in extracto:#Extracto ahora es una lista con (texto)(interlocutor siguiente)(indicación de final de texto)
        limpio = limpio + "\n" + linea#Se recorre solo el texto y se acumula separado por salto de línea en "limpio"
    return limpio
#--------------------------------------------------
#------------------------Cuerpo del programa-------
abrir = open('TU_RUTA_DE_DIRECTORIO/entrevistas.txt', 'r', encoding='utf8')#Abre el archivo con los datos
entrevistas = abrir.readlines()
abrir.close()
entrevistas = "\n".join(entrevistas)
nombres = re.findall('\w+_\w+_\d+', entrevistas)#Extrae el nombre que le hemos dado a cada entrevista (ej: andalucia_jaen_1)
for nombre in nombres:
    original = open("TU_RUTA_DE_DIRECTORIO/entrevistas_originales_txt/" + nombre + ".txt", 'r')#Lee cada archivo de texto
    texto = original.readlines()#Almacena el contenido en texto
    original.close()
    texto = texto[0]#Se almacena como una lista, así que accedo a la cadena de texto pura
    limpio = ""
    if re.search("I:", texto) != None: #Busca cada posible interlocutor (I, I1, I2) extrae su intervención y la agrega al conjunto almacenado en "limpio"
        limpio = limpio + extraer_interlocutor("I", texto)
    if re.search("I1:", texto) != None:
        limpio = limpio + extraer_interlocutor("I1", texto)
    if re.search("I2:", texto) != None:
        limpio = limpio + extraer_interlocutor("I2", texto)
    if re.search("I3:", texto) != None:
        limpio = limpio + extraer_interlocutor("I3", texto)
    if re.search("I4:", texto) != None:
        limpio = limpio + extraer_interlocutor("I4", texto)
    nuevo = open("TU_RUTA_DE_DIRECTORIO/corpus/" + nombre + ".txt", "w+")#Crea o abre el archivo
    nuevo.write(limpio)#mete las intervenciones en el archivo concreto (sobreescribe el contenido anterior si lo hubiera)
    nuevo.close()
    #--------------------------------------------------