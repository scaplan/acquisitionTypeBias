#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, os, subprocess, glob
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

def readChaFiles():
	# print os.getcwd()
	for dataFileName in glob.glob("*.cha"):
		print (os.getcwd() + '/' + dataFileName)
		with open(dataFileName, 'r') as currFile:
			for currLine in currFile:
				if not currLine:
					continue
				currLine = currLine.rstrip().lower()
				currLineTokens = currLine.split()
				print currLine + " ::: " + str(len(currLineTokens))


def iterateSubDir(directoryName):
	print 'running iterateSubDir()'
	# call function to iterate over any ".cha" files in this directory
	readChaFiles()

	# going through each immediate subdirectory
	for subDir in next(os.walk(directoryName))[1]:
		subDirPath = directoryName + '/' + subDir
		os.chdir(subDirPath)
		readChaFiles()



##
## Main method block
##
if __name__=="__main__":
	if (len(sys.argv) < 2):
		print('incorrect number of arguments')
		exit(0)

	directoryName = sys.argv[1]

	searchDirectory = os.getcwd() + '/' + directoryName
	iterateSubDir(searchDirectory)
