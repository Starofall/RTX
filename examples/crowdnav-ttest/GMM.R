setwd('/Users/A.Gunduz/Desktop/git/RTX/examples/crowdnav-ttest/')
mydata <- read.csv("saved_experiments/exp2/combined.csv", header = TRUE, sep = ',')


library("rebmix")
devAskNewPage(ask = TRUE)

gamma1est <- REBMIX(Dataset = list(as.data.frame(mydata$overhead1)), Preprocessing = "Parzen window",
                    cmax = 2, Criterion = c("AIC", "BIC"), pdf = "normal")
plot(gamma1est, pos = 2, what = c("density", "distribution", "IC", "logL", "D"), ncol = 2, npts = 5000)


summary(gamma1est)
coef(gamma1est)


#plot one of the gamma dist

n <- c(10000)
Theta <- list(pdf1 = "gamma", theta1.1 = c(2.136884), theta2.1 = c(1.707333))
gamma1 <- RNGMIX(Dataset.name = "gamma1", n = n, Theta = Theta)
plot(gamma1)
