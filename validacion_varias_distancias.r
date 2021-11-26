#Enunciados__

culling = "Culling: "
mfw = "MFW: "
acierto = "Acierto: "
palabrasdisponibles = "Palabras disponibles: "
cambio = "Culling = "
metodo_usado = "Método usado: "
distancia_usada = "Distancia usada: "

#Enunciados__

setwd("DIRECTORIO/corpus")#En la carpeta "corpus" deben estar tus datos
library(stylo)


texts = load.corpus.and.parse(files = "all", corpus.dir = "corpus", ngram.size = 1)#Cambiar el número de n-gramas
freq.list = make.frequency.list(texts, head = 5000)
word.frequencies = make.table.of.frequencies(corpus = texts, features = freq.list)
metodos = list("delta")
distancias = list("eder","wurzburg", "delta", "simple", "entropy", "manhattan", "canberra", "euclidean", "cosine")
for(metodo in metodos){
  for(distancia in distancias){
    for(e in 0:10){
      #Bucle para MFW
      for(i in 1:50){
        #Seleccionamos culling
        tabla = perform.culling(word.frequencies, e*10)
        #Seleccionamos MFW
        tabla1 = t(head(t(tabla), i*100))
        disponibles = ncol(tabla)
        if(i*100> disponibles){break}
        #Se aplica la validación cruzada 
        resultados = crossv(tabla1, cv.mode = "leaveoneout",
                            classification.method = metodo, distance=distancia)
        #Se imprimen los resultados en el archivo de texto
        porcentaje = round(sum(resultados[[1]])/length(resultados[[1]]), 2)
        cat(metodo_usado, metodo, file = "resultados.txt", append = TRUE, fill=TRUE)
        cat(distancia_usada, distancia, file = "resultados.txt", append = TRUE, fill=TRUE)
        cat(culling, e*10, file = "resultados.txt", append = TRUE, fill=TRUE) 
        cat(mfw,i*100, file = "resultados.txt", append = TRUE, fill=TRUE)
        cat(palabrasdisponibles, disponibles, file = "resultados.txt", append =
              TRUE, fill=TRUE)
        cat(acierto, porcentaje, file = "resultados.txt", append = TRUE, 
            fill=TRUE)
        cat(file = "resultados.txt", append = TRUE, fill=TRUE)
      }}

  }
}