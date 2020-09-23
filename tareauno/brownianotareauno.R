correctos = data.frame()
incorrectos = data.frame()
for (e in 5:10) {
l = 2**e
for (d in 1:8) {       #calculando en 8 dim
for (r in 1:50) {      #cuenta de las repeticiones 
pos = rep(0, d)
regresa = FALSE
for (t in 1:l) {                #determinar tiempo
dd = sample(1:d, 1)
if (runif(1) < 0.5 ) {
pos [dd] = pos [dd] + 1 
} else { 
pos [dd] = pos [dd] - 1 
}
if (all(pos == 0)) { 
correctos = rbind(correctos, c(l, d, t))
regresa = TRUE
break
}
}
if(!regresa) { 
incorrectos = rbind(incorrectos, c(l, d))
}
}
}
}
names(correctos) = c("largo", "dim", "tiempo")
names(incorrectos) = c("largo", "dim")
dim(correctos)
dim(incorrectos)

names(correctos) = c("largo", "dim", "tiempo")
sink('correctos.txt')                            
print(correctos)
png('demo.png')
boxplot(formula = tiempo ~ dim, data =  correctos,
 col=rainbow(8, alpha=0.2),
border = rainbow(8, v=0.6)
)
graphics.off()
file.show('demo.png')