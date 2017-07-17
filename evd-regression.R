## Import (packages)
library(ggplot2)
library(Hmisc)

## Parse input args
args = commandArgs(trailingOnly=TRUE)
orig_name_template = args[1]


## Read in data
#data=read.table(orig_name_template,sep=" ", fill = TRUE , header = TRUE, stringsAsFactors=FALSE, na.strings=c(""))

mydata=read.table(orig_name_template,header=TRUE,sep=" ",fill = TRUE)

#nounOrVerbWords <- subset(mydata, binarizedTag=='noun' | binarizedTag=='verb')
nounOrVerbWords <- subset(mydata, nounStatus=='1' | verbStatus=='1')
childWords <- subset(mydata, childAttested=='1')

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

summary(glm(childAttested~motherCount,family=binomial,data=mydata))
summary(glm(childAttested~motherIsoCount,family=binomial,data=mydata))
summary(glm(childAttested~motherFinalNonIsoCount,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+motherIsoCount,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+motherIsoCount+motherFinalNonIsoCount,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+motherFinalNonIsoCount,family=binomial,data=mydata))

summary(glm(childAttested~POS,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+POS,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+POS+motherIsoCount,family=binomial,data=mydata))
summary(glm(childAttested~nounStatus+verbStatus,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+nounStatus+verbStatus,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+nounStatus+verbStatus+motherIsoCount,family=binomial,data=mydata))
summary(glm(childAttested~charLength,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+charLength,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+charLength+motherIsoCount,family=binomial,data=mydata))
summary(glm(childAttested~numSylls,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+numSylls,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+numSylls+motherIsoCount,family=binomial,data=mydata))
summary(glm(childAttested~motherCount+motherFinalNonIsoCount+charLength+numSylls+nounStatus+verbStatus+motherIsoCount,family=binomial,data=mydata))



### Only considering nouns and verbs
summary(glm(childAttested~motherCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherIsoCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherFinalNonIsoCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+motherIsoCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+motherIsoCount+motherFinalNonIsoCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+motherFinalNonIsoCount,family=binomial,data=nounOrVerbWords))

summary(glm(childAttested~POS,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+POS,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+POS+motherIsoCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~nounStatus+verbStatus,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+nounStatus+verbStatus,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+nounStatus+verbStatus+motherIsoCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~charLength,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+charLength,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+charLength+motherIsoCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~numSylls,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+numSylls,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+numSylls+motherIsoCount,family=binomial,data=nounOrVerbWords))
summary(glm(childAttested~motherCount+motherFinalNonIsoCount+charLength+numSylls+nounStatus+verbStatus+motherIsoCount,family=binomial,data=nounOrVerbWords))

# summary(glm(childAttested~motherCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherFinalNonIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+motherIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+motherIsoCount+motherFinalNonIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+motherFinalNonIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~POS,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+POS,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+POS+motherIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~binarizedTag,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+binarizedTag,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+binarizedTag+motherIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~charLength,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+charLength,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+charLength+motherIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~numSylls,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+numSylls,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+numSylls+motherIsoCount,family=binomial,data=nounOrVerbWords))
# summary(glm(childAttested~motherCount+motherFinalNonIsoCount+charLength+numSylls+binarizedTag+motherIsoCount,family=binomial,data=nounOrVerbWords))


# n2 <- 100
# new.df <- data.frame(x1 = runif(n2, 0, 100), x2 = runif(n2,0,100))
# probs <- predict(model, new.df, "response")
# draws <- runif(n2)
# results <- (draws < probs)

# results