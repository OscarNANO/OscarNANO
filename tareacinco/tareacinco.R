cant<-c (100, 1000, 10000, 100000, 1000000)
repeticiones<-c(100)
diferencia<-data.frame()
inicio <- -6
final <- -inicio
paso <- 0.25
x <- seq(inicio, final, paso)
f <- function(x) { return(1 / (exp(x) + exp(-x))) }
suppressMessages(library(distr))
g <- function(x) { return((2 / pi) * f(x)) }
generador  <- r(AbscontDistribution(d = g)) 
desde <- 3
hasta <- 7
parte <- function() {
  valores <- generador(pedazo)
  return(sum(valores >= desde & valores <= hasta))
}
suppressMessages(library(doParallel))
registerDoParallel(makeCluster(detectCores() - 1))
for (resultado in cant){
  for (cantidad in repeticiones) {
    for (repetir in 1:10) {
      pedazo <- resultado
      cuantos <- cantidad
      montecarlo <- foreach(i = 1:cuantos, .combine=c) %dopar% parte()
      stopImplicitCluster()
      integral <- sum(montecarlo) / (cuantos * pedazo)
      aproximar<-((pi / 2) * integral)
      diferencia<-rbind(diferencia, c(abs(aproximar-0.04883505), resultado, cantidad))
    }
  }
}
png("Grafica1.png")
names(diferencia)<-c("Diferencia", "Cantidad","Replicas")
boxplot(diferencia$Diferencia~diferencia$Replicas+diferencia$Cantidad, use.cols=FALSE, ylim = c(0, 0.01), boxwex=0.3, xlab="Tama\u{F1}o de muestra", ylab="Diferencia a la aproximaci�n", names=c(100, 1000, 10000, 100000, 1000000), col=c(rep("pink", 5)))
abline(h=0.01, lty=1, lwd=2, col="yellow")
abline(h=0.001, lty=1, lwd=2, col="blue")
abline(h=0.00001, lty=1, lwd=2, col="green")
abline(h=0.0001, lty=1, lwd=2, col="red")

legend("topright", legend=c("2 d�gitos", "3 d�gitos", "4 d�gitos", "5 d�gitos"), title="Exactitud", cex = 0.8, fill = c("yellow", "blue", "red", "green"))

dev.off()