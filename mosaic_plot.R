gar.no = c(258,280)
gar.si = c(184, 719)

mat=rbind(gar.no, gar.si)
colnames(mat)=c("No considera consumo", "Considera Consumo")
rownames(mat)=c("No considera garantía", "Considera garantia")

mosaicplot(mat, col=c("skyblue", "royalblue"), cex.axis=0.8, main="")

library(ggplot2)
