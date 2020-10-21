library(parallel)
library(ggplot2)
library(gridExtra)
library(grid)
library(lattice)

suppressMessages(library(doParallel))
registerDoParallel(makeCluster(detectCores()-1))

calculo <- function(generar) {
  r <- 1 #Radio
  contcirc <- 0 #Cont in
  contcuad <- 0 #Cont out
  num <- generar #Muestra
  for(i in 1:num){
    x <- runif(1) #valor x 
    y <- runif(1) #valor y 
    d <- (x*x) + (y*y) #Calculo de la distancia
    if (d < r*r) { #sin salir del circulo
      contcirc <- contcirc + 1
    } 
  }
  
  pi <- as.double(4 * (contcirc/num)) 
  return(pi)
}

replicas <- 10 #Numero de replicas
datos <- data.frame()
variacion <- c(1000,5000,10000) #Variacion de muestras
for(var in variacion) {
  calcularPi <- foreach(i=1:replicas, .combine = c) %dopar% calculo(var)
  datos <- rbind(datos,calcularPi)
}

resultadoEsp <- 3.1415926 #Resultado igual a valor de pi
resultadoEsp_str <- strsplit(paste(resultadoEsp),split = "") #caracteres en cadena
resultados <- c()
resultados_str <- c()
res_contadores <- c()

for(i in 1:length(data.matrix(datos))) {
  resultados <- c(resultados,data.matrix(datos)[i])
  resultados_str <- c(resultados_str, strsplit(paste(resultados[i]), split=""))
}

for(i in 1:length(resultados)) { #comparacion decimal
  contador <- 0
  for(j in 1:7) {
    b <- unlist(resultados_str[i])[j] == unlist(resultadoEsp_str)[j]
    if(b) {
      contador <- contador + 1
    } 
    else {
      break
    }
    
  }
  
  res_contadores <- c(res_contadores,contador)
}

Valor_Esperado = resultadoEsp
png("Grafica2.png")
graf <- data.frame(Valores_Generados= c(rep("1000",10), rep("5000",10),rep("10000",10)), Valor_PI = resultados)
graf2 <- data.frame(Valores_Generados= c(rep("1000",10), rep("5000",10),rep("10000",10)), Decimales = res_contadores)

g <- ggplot(graf, aes(Valores_Generados,Valor_PI,fill=Valores_Generados)) + geom_hline(aes(yintercept=Valor_Esperado, size=Valor_Esperado), colour="blue") + geom_boxplot(alpha=0.4)  + theme_light()

p <- ggplot(graf2, aes(Valores_Generados,Decimales,fill=Valores_Generados)) + geom_violin(alpha=0.4, draw_quantiles = c(0.25, 0.5, 0.75), trim = FALSE,adjust=1.5)  + geom_jitter() + theme_light()

grid.arrange(g, p, nrow =1 )

dev.off()