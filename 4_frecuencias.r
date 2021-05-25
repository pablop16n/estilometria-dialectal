library(tidyverse)
library(tidytext)
setwd("TU_DIRECTORIO")
ficheros <- list.files(path = "muestra_frecuencias", pattern = "\\w+")

nombre <- gsub("\\.txt", "", ficheros, perl = T)

entrevistas <- tibble(nombre = character(),
                      texto = character())

for (i in 1:length(ficheros)){
  contenido <- readLines(paste("muestra_frecuencias",
                               ficheros[i],
                               sep = "/"))
  
  temporal <- tibble(nombre = nombre[i],
                     texto = contenido)
  entrevistas <- bind_rows(entrevistas,
                           temporal)
}
rm(temporal, contenido, ficheros, i, nombre)

entrevistas_palabras <- entrevistas %>%
  unnest_tokens(palabra,
                texto,
                token = "ngrams",
                n = 1)

palabras_total <- entrevistas_palabras %>%
  count(nombre, sort=T) %>%
  group_by(nombre)


palabras_absolutas <- entrevistas_palabras %>%
  count(nombre, palabra, sort = T) %>%
  group_by(nombre)

palabras_relativas <- palabras_absolutas %>%
  inner_join(palabras_total, by="nombre") %>%
  mutate(frecuencia = n.x/n.y*100)

palabras_relativas %>%
  filter(frecuencia > 0.50) %>%
  ggplot() +
  geom_col(aes(y = frecuencia , x = reorder(palabra, frecuencia)),
           fill = "maroon") +
  coord_flip() +
  facet_wrap(~ nombre, ncol = 10, scales = "free") +
  theme_linedraw() + 
  labs(x = "palabras", y = "frecuencia") + 
  ggtitle("palabras más frecuentes", subtitle = "frecuencia mínima de 0.50%")
