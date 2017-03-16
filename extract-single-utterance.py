#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, os, subprocess, glob
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

punctuationSet = ['.', '?', '!', ':', '(.)', '+...', '+"/.', '+/.']
morphCue = '%mor:'

def readChaFiles():
	for dataFileName in glob.glob("*.cha"):
		print (os.getcwd() + '/' + dataFileName)
		with open(dataFileName, 'r') as currFile:
			# store tuples
			speechGroup = []
			for currLine in currFile:
				if not currLine:
					continue
				if currLine[0] == '@':
					continue
				currLine = currLine.rstrip().lower()
				currLineTokens = currLine.split()

				if (currLineTokens[0][0] == "*"):
					# Needs to contain at least speech line and morph tag line
					if (len(speechGroup) > 1):
						evalSpeechGroup(speechGroup)
					speechGroup = []

				speechGroup.append(currLine)


def evalSpeechGroup(speechGroup):
	global punctuationSet, totalDataLength, totalMotherLines, totalSingleUtteranceMotherLines
	global singleWordNouns, singleWordVerbs, morphCue
	speechLine = speechGroup[0]
	tagTokens = []
	for entry in speechGroup:
		entryTokens = entry.split()
		if (entryTokens[0] == morphCue):
			tagTokens = entryTokens

	# remove puntuation
	currLineTokens = speechLine.split()
	currLineTokensNoPunc = [x for x in currLineTokens if x not in punctuationSet]

	if (len(currLineTokensNoPunc) > 1):
		totalDataLength += 1
		# Only printing the mother data
		if (currLineTokensNoPunc[0] == "*mot:"):
			totalMotherLines += 1
			# Need to remove punctuation from end of lines
			if (len(currLineTokensNoPunc) == 2):
				totalSingleUtteranceMotherLines += 1
				if (len(tagTokens) > 0):
					wordTag = tagTokens[1]
					wordTagInfo = wordTag.split("|")
					if (wordTagInfo[0] == 'n'):
						singleWordNouns += 1
					elif (wordTagInfo[0] == 'v'):
						singleWordVerbs += 1
					print speechLine + " ::: " + wordTagInfo[0]

				


				

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
	totalMotherLines = 0
	totalSingleUtteranceMotherLines = 0
	totalDataLength = 0

	singleWordNouns = 0
	singleWordVerbs = 0

	searchDirectory = os.getcwd() + '/' + directoryName
	iterateSubDir(searchDirectory)

	print 'totalDataLength: ' + str(totalDataLength)
	print 'totalMotherLines: ' + str(totalMotherLines)
	print 'totalSingleUtteranceMotherLines: ' + str(totalSingleUtteranceMotherLines)
	print 'singleWordNouns: ' + str(singleWordNouns)
	print 'singleWordVerbs: ' + str(singleWordVerbs)