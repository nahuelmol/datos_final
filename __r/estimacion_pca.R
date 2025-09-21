data(iris)

datos <- iris[,1:4]
datos_std <- scale(datos)

pca <- prcomp(datos_std, center=TRUE, scale=TRUE)
summary(pca)

biplot(pca)
pca$rotation
pca$x