#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, os, subprocess, glob
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

punctuationSet = ['.', '?', '!', ':', '(.)', '+...', '+"/.', '+/.']
inputSet = ['*mot:', '*gra:', '*fat:', '*ann:', '*ant:', '*nan:', '*wom:']
childSet = ['*chi:', '*eli:', '*gre:', '*mar:']
morphCue = '%mor:'
inputNounTypeDict = {}
inputVerbTypeDict = {}

outputNounTokenCount = 0
outputVerbTokenCount = 0
outputNounTypeDict = {}
outputVerbTypeDict ={}

missingSpeechLines = 0

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
	global punctuationSet, totalDataLength, totalMotherLines, missingSpeechLines
	global morphCue, cumulativeMotherLinesLength, totalChildLines, cumulativeChildLinesLength
	speechLine = speechGroup[0]
	tagTokens = []
	tagTokensNoPunc = []
	for entry in speechGroup:
		entryTokens = entry.split()
		if (entryTokens[0] == morphCue):
			tagTokens = entryTokens
			tagTokensNoPunc = [x for x in tagTokens if x not in punctuationSet]

	# remove puntuation
	currLineTokens = speechLine.split()
	currLineTokensNoPunc = [x for x in currLineTokens if x not in punctuationSet]

	if (len(currLineTokensNoPunc) > 1):
		totalDataLength += 1
		if (currLineTokensNoPunc[0] in inputSet):
			totalMotherLines += 1
			cumulativeMotherLinesLength += (len(currLineTokensNoPunc) - 1)
			evalInputData(currLineTokensNoPunc, tagTokensNoPunc)
		elif (currLineTokensNoPunc[0] in childSet):
			totalChildLines += 1
			cumulativeChildLinesLength += (len(currLineTokensNoPunc) - 1)
			evalOutputData(currLineTokensNoPunc, tagTokensNoPunc)
		else:
			missingSpeechLines += 1

def evalInputData(inputString, inputTags):
	global totalSingleUtteranceMotherLines, inputNounTypeDict, inputVerbTypeDict, singleWordNouns, singleWordVerbs
	if (len(inputString) == 2):
		totalSingleUtteranceMotherLines += 1
		if (len(inputTags) > 0):
			wordTag = inputTags[1]
			wordTagInfo = wordTag.split("|")
			if (wordTagInfo[0] == 'n'):
				if (inputString[1] in inputNounTypeDict):
					newCount = 1 + inputNounTypeDict.get(inputString[1])
					inputNounTypeDict[inputString[1]] = newCount
				else:
					inputNounTypeDict[inputString[1]] = 1
				singleWordNouns += 1
			elif (wordTagInfo[0] == 'v'):
				if (inputString[1] in inputVerbTypeDict):
					newCount = 1 + inputVerbTypeDict.get(inputString[1])
					inputVerbTypeDict[inputString[1]] = newCount
				else:
					inputVerbTypeDict[inputString[1]] = 1
				singleWordVerbs += 1
		#	print " ".join(inputString) + " ::: " + wordTagInfo[0]

def evalOutputData(outputString, outputTags):
	global outputNounTokenCount, outputVerbTokenCount, outputNounTypeDict, outputVerbTypeDict

#	if (len(outputString) != len(outputTags)):
#		print outputString
#		print outputTags
#		print ''
	for currTag in outputTags:
		# Need to figure out how to align this with original type
		if ('n|' in currTag):
			outputNounTokenCount += 1
		elif ('v|' in currTag):
			outputVerbTokenCount += 1



def iterateSubDir(directoryName):
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
	cumulativeMotherLinesLength = 0
	totalSingleUtteranceMotherLines = 0
	totalDataLength = 0

	totalChildLines = 0
	cumulativeChildLinesLength = 0

	singleWordNouns = 0
	singleWordVerbs = 0

	searchDirectory = os.getcwd() + '/' + directoryName
	iterateSubDir(searchDirectory)

	motherMLU = cumulativeMotherLinesLength / (totalMotherLines * 1.0)
	childMLU = cumulativeChildLinesLength / (totalChildLines * 1.0)

	print 'totalDataLength: ' + str(totalDataLength)
	print 'totalMotherLines: ' + str(totalMotherLines)
	print 'mother MLU: ' + str(motherMLU)

	print 'totalSingleUtteranceMotherLines: ' + str(totalSingleUtteranceMotherLines)
	print 'singleWordNounTokens: ' + str(singleWordNouns)
	print 'singleWordNounTypes: ' + str(len(inputNounTypeDict))
	print 'singleWordVerbTokens: ' + str(singleWordVerbs)
	print 'singleWordVerbTypes: ' + str(len(inputVerbTypeDict))

	print 'totalChildLines: ' + str(totalChildLines)
	print 'child MLU: ' + str(childMLU)
	print 'childNounTokens: ' + str(outputNounTokenCount)
	print 'childVerbTokens: ' + str(outputVerbTokenCount)

	print 'missingSpeechLines: ' + str(missingSpeechLines)