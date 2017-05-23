#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, os, subprocess, glob, nltk
from nltk import word_tokenize
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

punctuationSet = ['.', '?', '!', ':', '(.)', '+...', '+"/.', '+/.']
inputSet = ['*mot:', '*gra:', '*fat:', '*ann:', '*ant:', '*nan:', '*wom:', '*car:']
childSet = ['*chi:', '*eli:', '*gre:', '*mar:']
morphCue = ['%mor:', '%xmor:']
## '%xmor:'
inputNounTypeDict = {}
inputVerbTypeDict = {}

nounSet = ['n', 'nn', 'npro']
verbSet = ['v', 'vt', 'vi', 'vc', 'va']

outputNounTokenCount = 0
outputVerbTokenCount = 0
outputNounTypeDict = {}
outputVerbTypeDict ={}

missingSpeechLines = 0

def readChaFiles():
	for dataFileName in glob.glob("*.cha"):
	#	print (os.getcwd() + '/' + dataFileName)
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
		if (entryTokens[0] in morphCue):
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
			
		#	print speechLine
			
		elif (currLineTokensNoPunc[0] in childSet):
			totalChildLines += 1
			cumulativeChildLinesLength += (len(currLineTokensNoPunc) - 1)
			evalOutputData(currLineTokensNoPunc, tagTokensNoPunc)
		else:
			missingSpeechLines += 1

def evalInputData(inputString, inputTags):
	global totalSingleUtteranceMotherLines, inputNounTypeDict, inputVerbTypeDict, singleWordNouns, singleWordVerbs

#	toTag = inputString[1:]
#	taggedInput = nltk.pos_tag(toTag)

	if (len(inputString) == 2):
		totalSingleUtteranceMotherLines += 1
		if (len(inputTags) > 0):
			wordTag = inputTags[1]
			wordTagInfo = wordTag.split("|")
			wordMarkupForm = wordTagInfo[1]
			#wordMarkupForm = inputString[1]
		#	if (wordTagInfo[0] == 'n'):
			if (wordTagInfo[0] in nounSet):
				if (wordMarkupForm in inputNounTypeDict):
					newCount = 1 + inputNounTypeDict.get(wordMarkupForm)
					inputNounTypeDict[wordMarkupForm] = newCount
				else:
					inputNounTypeDict[wordMarkupForm] = 1
				singleWordNouns += 1
			#elif (wordTagInfo[0] == 'v'):
			elif (wordTagInfo[0] in verbSet):
				if (wordMarkupForm in inputVerbTypeDict):
					newCount = 1 + inputVerbTypeDict.get(wordMarkupForm)
					inputVerbTypeDict[wordMarkupForm] = newCount
				else:
					inputVerbTypeDict[wordMarkupForm] = 1
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

		currTagInfo = currTag.split("|")
		if len(currTagInfo) > 1:
			currPos = currTagInfo[0]
			currWord = currTagInfo[1]
			if (currPos == 'v'):
				if (currWord in outputVerbTypeDict):
					newCount = 1 + outputVerbTypeDict.get(currWord)
					outputVerbTypeDict[currWord] = newCount
				else:
					outputVerbTypeDict[currWord] = 1
			elif (currPos == 'n'):
				if (currWord in outputNounTypeDict):
					newCount = 1 + outputNounTypeDict.get(currWord)
					outputNounTypeDict[currWord] = newCount
				else:
					outputNounTypeDict[currWord] = 1
		# if (currTagInfo[0] == 'n'):
		# 	outputNounTokenCount += 1
		# elif (currTagInfo[0] == 'v'):
		# 	outputVerbTokenCount += 1



def iterateSubDir(directoryName):
	# call function to iterate over any ".cha" files in this directory
	readChaFiles()

	# going through each immediate subdirectory
	for subDir in next(os.walk(directoryName))[1]:
		subDirPath = directoryName + '/' + subDir
		os.chdir(subDirPath)
		readChaFiles()

def safeDivide(numerator, denominator):
	if denominator > 0:
		return (numerator / (denominator * 1.0))
	else:
		return 0.0

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

	motherMLU = safeDivide(cumulativeMotherLinesLength, totalMotherLines)
	childMLU = safeDivide(cumulativeChildLinesLength, totalChildLines)

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
	print 'childNounTypes: ' + str(len(outputNounTypeDict))
	print 'childVerbTokens: ' + str(outputVerbTokenCount)
	print 'childverbTypes: ' + str(len(outputVerbTypeDict))

	print 'missingSpeechLines: ' + str(missingSpeechLines)