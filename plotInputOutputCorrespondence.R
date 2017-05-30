## Import (packages)
library(ggplot2)
library(Hmisc)

## Parse input args
args = commandArgs(trailingOnly=TRUE)
orig_name_template = args[1]
output_name = args[2]

## Read in data
data=read.table(orig_name_template,sep=",", fill = TRUE , header = FALSE, stringsAsFactors=FALSE)

data

png(output_name, height=900,width=900)
attach(data)
plot(V3, V2, main="Noun Bias Plot", xlab="Ratio of N/V in Child Output", ylab="Isolated N/V Ratio in Input Speech", pch=19)
abline(lm(V2~V3), col="red") # regression line (y~x) 