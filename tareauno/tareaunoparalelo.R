registro <- data.frame()
dimension <- 8
potencia <- 10
for (pot in 5:potencia){
  duracion <- 2^potencia
  for (dim in 1:dimension) {
    
    datos <- numeric()
    repeticiones <- 50
    for (replica in 1:repeticiones) {
      resultado <- FALSE
      pos <- rep(0, dim)
      for (t in 1:duracion) {
        modificar <- sample(1:dim, 1)
        if (runif(1) < 0.5) {
          pos[modificar] <-  pos[modificar] + 1
        } else {
          pos[modificar] <-  pos[modificar] - 1
        }
        if (all(pos == 0)) {
          resultado = TRUE
          break
        }
      }
      datos <- c(datos, resultado)
}
  porc <- 100 * sum(datos) / repeticiones
  registro <- rbind(registro, c(pot, porc, dim))
  }
}stopCluster(cluster)
if (eucl) {
    png("p1er.png")
    boxplot(data.matrix(datos), use.cols=FALSE, 
       xlab<-"Dimensi\u{F3}n", ylab="Distancia m\u{E1}xima", 
       main<-"Euclideana")
} else {
    png("p1mr.png")
    boxplot(data.matrix(datos), use.cols<-FALSE, 
       xlab<-"Dimensi\u{F3}n", ylab="Distancia m\u{E1}xima", 
       main<-"Manhattan")
}
graphics.off()