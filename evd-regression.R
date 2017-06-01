## Import (packages)
library(ggplot2)
library(Hmisc)

## Parse input args
args = commandArgs(trailingOnly=TRUE)
orig_name_template = args[1]


## Read in data
#data=read.table(orig_name_template,sep=" ", fill = TRUE , header = TRUE, stringsAsFactors=FALSE, na.strings=c(""))

mydata=read.table(orig_name_template,header=TRUE,sep=" ")

# data$word

# png('childesTotalVsMotherFrequency.png', height=900,width=900)
# attach(data)
# plot(charlesFreqProb, motherFreqProb, main="childesTotalVsMotherFrequency", xlab="charlesFreqProb", ylab="motherFreqProb", pch=19)
# abline(lm(motherFreqProb~charlesFreqProb), col="red") # regression line (y~x) 

# png('FrequncyIsoPlot.png', height=900,width=900)
# attach(data)
# plot(motherIsoProb, motherFreqProb, main="FrequncyIsoPlot", xlab="motherIsoProb", ylab="motherFreqProb", pch=19)
# abline(lm(motherFreqProb~motherIsoProb), col="red") # regression line (y~x) 

# png('FrequncyVsChild.png', height=900,width=900)
# attach(data)
# plot(motherCount, childCount, main="FrequncyIsoPlot", xlab="motherCount", ylab="childCount", pch=19)
# abline(lm(childCount~motherCount), col="red") # regression line (y~x) 

#childProductionMax100 <- data[data[,4]<100,]
#data[data[,4]<100,]
#cat(sprintf("Verbs with ev2 at least five times: %s\n", nrow(dataCleanMin5)))


# png('FrequncyVsChildMax100.png', height=900,width=900)
# attach(childProductionMax100)
# plot(motherCount, childCount, main="FrequncyVsChildMax100", xlab="motherCount", ylab="childCount", pch=19)
# abline(lm(childCount~motherCount), col="red") # regression line (y~x) 

# png('FrequncyIsoPlotChildMax100.png', height=900,width=900)
# attach(childProductionMax100)
# plot(motherIsoProb, childCount, main="FrequncyIsoPlotChildMax100", xlab="motherIsoProb", ylab="childCount", pch=19)
# abline(lm(childCount~motherIsoProb), col="red") # regression line (y~x) 

#dependentVariable = data$childAttested

#childAttestedWords <- data[data[,4]=='yes',]
#childUnknownWords <- data[data[,4]=='no',]

#mean(childAttestedWords$motherCount)
#mean(childUnknownWords$motherCount)

#mean(childAttestedWords$motherIsoCount)
#mean(childUnknownWords$motherIsoCount)

#png('childAttestedVsMotherFrequency.png', height=900,width=900)
#attach(data)
#plot(motherCount, childAttested, main="childAttestedVsMotherFrequency", xlab="motherCount", ylab="childAttested", pch=19)
#abline(lm(childCount~motherIsoProb), col="red") # regression line (y~x) 

#n <- 500
#x1 <- runif(n,0,100)
#x2 <- runif(n,0,100)
#y <- (x2 - x1 + rnorm(n,sd=20)) < 0
#model <- glm(dependentVariable ~ data$motherCount, family="binomial")

reg = glm(childAttested~motherCount,family=binomial,data=mydata)
summary(reg)

#reg = glm(childAttested~motherFreqProb,family=binomial,data=mydata)
#summary(reg)

reg = glm(childAttested~motherIsoCount,family=binomial,data=mydata)
summary(reg)

#reg = glm(childAttested~motherIsoProb,family=binomial,data=mydata)
#summary(reg)

reg = glm(childAttested~motherFinalNonIsoCount,family=binomial,data=mydata)
summary(reg)

#reg = glm(childAttested~motherFinalNonIsoProb,family=binomial,data=mydata)
#summary(reg)

reg = glm(childAttested~charlesFreqCount,family=binomial,data=mydata)
summary(reg)

#reg = glm(childAttested~charlesFreqProb,family=binomial,data=mydata)
#summary(reg)

reg = glm(childAttested~motherCount+motherIsoCount,family=binomial,data=mydata)
summary(reg)

#reg = glm(childAttested~motherFreqProb+motherIsoProb,family=binomial,data=mydata)
#summary(reg)

reg = glm(childAttested~motherCount+motherIsoCount+motherFinalNonIsoCount,family=binomial,data=mydata)
summary(reg)

#reg = glm(childAttested~motherFreqProb+motherIsoProb+motherFinalNonIsoProb,family=binomial,data=mydata)
#summary(reg)





#glm(formula = childAttested ~ charlesFreqProb + motherFreqProb, family="binomial", data = data)


# n2 <- 100
# new.df <- data.frame(x1 = runif(n2, 0, 100), x2 = runif(n2,0,100))
# probs <- predict(model, new.df, "response")
# draws <- runif(n2)
# results <- (draws < probs)

# results