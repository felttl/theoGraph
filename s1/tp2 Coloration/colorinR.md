

algo donné par la prof pour faire une coloration

```r
coloration <- function(sommets,arets){
  taille=length(sommets)
  M<-Matrix(rep(0,taille^2,taille,taille))
  for (i in 1:length(arets)/2){
    M[arets[i,1],arets[i,2]]=1
    M[arets[i,2],arets[i,1]]=1
  }
  degres<-rowSums(M)
  ordre_degres <- sort(degres,index.return=TRUE)
  sommets<-sommeets[ordre_degres$ix]
  i<-length(sommets)
  sommet_choisi<-c(rep(0,i))
  A = FALSE
  while(A==FALSE){
    new_color = c(rep(0),i)
    if(sommet_choisi[i]==0){
      sommet_choisi[i]=1
      new_color[sommets[i]] = 1
      adj_comment<-M[sommet_choisi[i],]
      
    }  
  }
}
```
