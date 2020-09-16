pos <- 0
runif(1)
dur <- 10
for (t in 1:dur) {
    if(runif(1)<0.5) {
     pos <- pos +1
    } else {
     pos <- pos -1
    }
    print(pos)
}

dim<-8
largo<-50
pos<-rep(0,dim)
for (t in 1:largo) {
   pos<-paso (pos,dim)
   cat(pos, '\n')
}