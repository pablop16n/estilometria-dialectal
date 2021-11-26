library(tidyverse)
library(tidytext)
library(udpipe)
setwd("TU_DIRECTORIO")
ficheros <- list.files(path = "corpus", pattern = "\\w+")

modelo_ancora <- udpipe_load_model(file = 'spanish-ancora-ud-2.5-191206.udpipe')
direccion_escritura <- "corpus_categorias/corpus/"

for (i in 1:length(ficheros)){
  contenido <- readLines(paste("corpus",
                               ficheros[i],
                               sep = "/"))
  contenido <- iconv(contenido, from = "Latin1", to = "UTF-8")
  contenido <- udpipe_annotate(modelo_ancora, contenido)
  contenido <- as_tibble(contenido)
  aglutinado = ""
  for(l in 1:length(contenido$upos)){
    aglutinado <- paste(aglutinado, contenido$upos[[l]], sep=" ")
    if(l<length(contenido$upos)){
      if(str_detect(contenido$token_id[[l]], "\\-")){
        actual <- strtoi(str_extract(contenido$token_id[[l]], "\\d\\d?"))
      }else{
        actual <- strtoi(contenido$token_id[[l]])
      }
      if(str_detect(contenido$token_id[[l+1]], "\\-")){
        siguiente <- strtoi(str_extract(contenido$token_id[[l+1]], "\\d\\d?"))
      }else{
        siguiente <- strtoi(contenido$token_id[[l+1]])
      }
      if(siguiente < actual){
        aglutinado <- paste(aglutinado, "\n", sep="")
      }
    }
    
  }
  rm(contenido, l, siguiente, actual)
  direccion_completa <- paste(direccion_escritura, ficheros[i], sep="")
  file.create(direccion_completa)
  conexion <- file(direccion_completa)
  writeLines(aglutinado, direccion_completa)
  close(conexion)
  
}
