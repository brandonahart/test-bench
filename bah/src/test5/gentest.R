library(lobstr)

### generate a matrix with rowcnt, colcnt
genmat <- function(rowcnt=1000, colcnt=10) {
    replicate(colcnt, runif(rowcnt))
}


### generate a data frame with rowcnt, colcnt
gendf <- function(rowcnt=1000, colcnt=10) {
    as.data.frame(genmat(rowcnt, colcnt))
}

set.seed(321)

sample <- function(n) {

   for (i in 1:n) {
       start = Sys.time()
       df <- gendf((1e6*i),10)
       stop = Sys.time()
       cat(i, ' rows: ',nrow(df),' time: ',(stop-start),'\n')
       df <- NULL
       gc()
   }

}
