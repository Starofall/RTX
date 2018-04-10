library(plumber)
pr <- plumber::plumb("plumber.R")
pr$run(port = 8004)