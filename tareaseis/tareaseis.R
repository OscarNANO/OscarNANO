l = 1.5
n = 40            #agentes
pi = 0.05         #probabilidad de estar infectado
pr = 0.02         #probabilidad de estar recuperado
v = l/15          #velocidad
PV = seq(0,1,0.1) #probabilidad de estar vacunado
r = 0.1           
t = 1
replicas = 15

Rvacunas = data.frame()
dibujarSistema = FALSE
ggplot = TRUE
pasos = 5

for(pv in PV){
for(rep in 1:replicas){
agentes = data.frame(x = double(), y = double(), dx = double(), dy = double(), estado  = character())
for (i in 1:n) { 
if(runif(1) < pv){ 
e = "R"
} else if(runif(1) < pi){
e = "I"
} else{
e = "S"
}
      
agentes = rbind(agentes, data.frame(x = runif(1, 0, l), y = runif(1, 0, l),
                 dx = runif(1, -v, v), dy = runif(1, -v, v),
                 estado = e))
      
levels(agentes$estado) = c("S", "I", "R")
}
    
epidemia = integer()
mayor = 0
actual = 0
    
while(TRUE) { 
infectados = dim(agentes[agentes$estado == "I",])[1]
epidemia = c(epidemia, infectados)
if (infectados == 0) {
break
}
contagios = rep(FALSE, n)
for (i in 1:n) { #contagios que se pueden dar
a1 = agentes[i, ]
if (a1$estado == "I") { #partiendo de los contagios
for (j in 1:n) {
if (!contagios[j]) { #todavia no se contagian
a2 = agentes[j, ]
if (a2$estado == "S") { #todavia se pueden contagiar
dx = a1$x - a2$x
dy = a1$y - a2$y
d = sqrt(dx^2 + dy^2)
if (d < r) { # umbral
p = (r - d) / r
if (runif(1) < p) {
contagios[j] <- TRUE
}
}
}
}
}
}
}
for (i in 1:n) { #cambios
a = agentes[i, ]
if (contagios[i]) {
a$estado = "I"
} else if (a$estado == "I") { #se encontraba infectada
if (runif(1) < pr) {
a$estado = "R" #se logra recuperar
}
}
a$x = a$x + a$dx
a$y = a$y + a$dy
if (a$x > l) {
a$x = a$x - l
}
if (a$y > l) {
a$y = a$y - l
}
if (a$x < 0) {
a$x = a$x + l
}
if (a$y < 0) {
a$y = a$y + l
}
agentes[i, ] <- a
}
if(dibujarSistema){
aS = agentes[agentes$estado == "S",]
aI = agentes[agentes$estado == "I",]
aR = agentes[agentes$estado == "R",]
tl = paste(tiempo, "", sep="")
while (nchar(tl) < digitos) {
tl = paste("0", tl, sep="")
}
salida = paste("tarea6_t", t6_t, ".png", sep="")
tiempo = paste("Paso", t)
png(salida)
plot(l, type="n", main=tiempo, xlim=c(0, l), ylim=c(0, l), xlab="x", ylab="y")
if (dim(aS)[1] > 0) {
points(aS$x, aS$y, pch=15, col="chartreuse3", bg="chartreuse3")
}
if (dim(aI)[1] > 0) {
points(aI$x, aI$y, pch=16, col="firebrick2", bg="firebrick2")
}
if (dim(aR)[1] > 0) {
points(aR$x, aR$y, pch=17, col="goldenrod", bg="goldenrod")
}
graphics.off()
}
recu <- dim(agentes[agentes$estado == "R",])[1]
if(recu == n){
break
}
t <- t + 1
}
maximo_infectados <- max(epidemia)
porcentaje <- 100 * maximo_infectados / n
Rvacunas <- rbind(Rvacunas, c(pv, rep, maximo_infectados, porcentaje))
print(pv) 
}
}
colnames(Rvacunas) <- c("Probabilidad", "Replicas", "Max_Infectados", "Porcentaje")
print(Rvacunas)
write.table(Rvacunas, "vacunados.txt")
max(Rvacunas)

if(ggplot){

library(ggplot2)
Rvacunas$Probabilidad <- as.factor(Rvacunas$Probabilidad)
tema <- theme(
panel.background = element_rect(fill = "black", colour = "red", size = 0.4, linetype = "solid"),
panel.grid.major = element_line(size = 0.4, linetype = 'solid', colour = "yellow"), 
panel.grid.minor = element_line(size = 0.20, linetype = 'solid', colour = "yellow")
)
 
p = ggplot(Rvacunas, aes(x = Probabilidad, y = Porcentaje, fill = Probabilidad)) + geom_violin()
p = p + geom_violin(scale = "width", alpha = 0.5) + geom_violin(trim = F) + geom_boxplot(width=0.25, alpha=0.7)
p = p + labs(x="Probabilidades de vacunaci\u{F3}n", y = "Porcentaje m\u{E1}ximo de infectados") + tema
ggsave("Tareaseisvacunas.png")

png("tareaseisboxplot.png")
probabilidades = Rvacunas$Probabilidad
porcentaje_maximos = Rvacunas$Porcentaje
boxplot(porcentaje_maximos~probabilidades, col = "blue", border="red", xlab = "Probabilidades de vacunaci\u{F3}n", 
ylab = "Porcentaje m\u{E1}ximo de infectados")
graphics.off()
}