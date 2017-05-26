#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, os, subprocess, glob, nltk, re
from nltk import word_tokenize
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

punctuationSet = ['.', '?', '!', ':', '(.)', '+...', '+"/.', '+/.']
inputSet = ['*mot:', '*gra:', '*fat:', '*ann:', '*ant:', '*nan:', '*wom:', '*car:', '*inv:', '*par:', '*mut:', '*vat:', '*oma:', '*exp:', '*car:', '*bri', '*nen:', '*mag:', '*gmt:']
childSet = ['*chi:', '*eli:', '*gre:', '*mar:']
morphCue = ['%mor:', '%xmor:', '%newmor:']
## '%xmor:'
inputSingleNounTypeDict = {}
inputSingleVerbTypeDict = {}
inputSingleOtherTypeDict = {}
inputDoubleNounTypeDict = {}
inputDoubleVerbTypeDict = {}
inputDoubleOtherTypeDict = {}
inputTotalNounTypeDict = {}
inputTotalVerbTypeDict = {}
inputTotalOtherTypeDict = {}

inputSingleNounTokenCount = 0
inputSingleVerbTokenCount = 0
inputSingleOtherTokenCount = 0
inputDoubleNounTokenCount = 0
inputDoubleVerbTokenCount = 0
inputDoubleOtherTokenCount = 0
inputTotalNounTokenCount = 0
inputTotalVerbTokenCount = 0
inputTotalOtherTokenCount = 0


nounSet = ['n', 'nn', 'npro', 'noun', 'pron'] #'propn'
verbSet = ['v', 'vt', 'vi', 'vc', 'va', 'verb', 'aux', 'p']

outputNounTokenCount = 0
outputVerbTokenCount = 0
outputOtherTokenCount = 0
outputNounTypeDict = {}
outputVerbTypeDict = {}
outputOtherTypeDict = {}

missingSpeechLines = 0

def readChaFiles(sourceDir):
	for dataFileName in glob.glob(sourceDir+"*.cha"):
	#	print (os.getcwd() + '/' + dataFileName)
		with open(dataFileName, 'r') as currFile:
			# store tuples
			speechGroup = []
			for currLine in currFile:
				if not currLine:
					continue
				if currLine[0] == '@':
					continue
				if currLine == '':
					continue
				currLine = currLine.rstrip().lower()
				currLineTokens = currLine.split()

				if len(currLineTokens) == 0:
					continue

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

	onlyAlphaNumerics = []
	for token in currLineTokens:
		valid = re.search('[a-z]', token) is not None
		if valid:
			onlyAlphaNumerics.append(token)

	if (len(onlyAlphaNumerics) > 1):
		totalDataLength += 1
		if (onlyAlphaNumerics[0] in inputSet):
			totalMotherLines += 1
			cumulativeMotherLinesLength += (len(onlyAlphaNumerics) - 1)
			evalInputData(onlyAlphaNumerics, tagTokensNoPunc)
			
		#	print speechLine
			
		elif (onlyAlphaNumerics[0] in childSet):
			totalChildLines += 1
			cumulativeChildLinesLength += (len(onlyAlphaNumerics) - 1)
			evalOutputData(onlyAlphaNumerics, tagTokensNoPunc)
		else:
			missingSpeechLines += 1

def extractIsolatedWordInfo(length, inputTags, inputNounTypeDict, inputVerbTypeDict, inputOtherTypeDict):
	global inputSingleNounTokenCount, inputSingleVerbTokenCount, inputSingleOtherTokenCount
	global inputDoubleNounTokenCount, inputDoubleVerbTokenCount, inputDoubleOtherTokenCount
	global inputTotalNounTokenCount, inputTotalVerbTokenCount, inputTotalOtherTokenCount

	if (len(inputTags) > 1):
		for wordTag in inputTags[1:]:
			wordTagInfo = wordTag.split("|")
			if len(wordTagInfo) < 2:
				## Malformed morphological tag
				return
			wordMarkupForm = wordTagInfo[1]
			if (wordTagInfo[0] in nounSet):
				if (wordMarkupForm in inputNounTypeDict):
					newCount = 1 + inputNounTypeDict.get(wordMarkupForm)
					inputNounTypeDict[wordMarkupForm] = newCount
				else:
					inputNounTypeDict[wordMarkupForm] = 1
				if (length == 2):
					inputSingleNounTokenCount += 1
					inputTotalNounTokenCount += 1
				elif (length == 3):
					inputDoubleNounTokenCount += 1
					inputTotalNounTokenCount += 1
				else:
					inputTotalNounTokenCount += 1
			elif (wordTagInfo[0] in verbSet):
				if (wordMarkupForm in inputVerbTypeDict):
					newCount = 1 + inputVerbTypeDict.get(wordMarkupForm)
					inputVerbTypeDict[wordMarkupForm] = newCount
				else:
					inputVerbTypeDict[wordMarkupForm] = 1
				if (length == 2):
					inputSingleVerbTokenCount += 1
					inputTotalVerbTokenCount += 1
				elif (length == 3):
					inputDoubleVerbTokenCount += 1
					inputTotalVerbTokenCount += 1
				else:
					inputTotalVerbTokenCount += 1
			else:
				if (wordMarkupForm in inputOtherTypeDict):
					newCount = 1 + inputOtherTypeDict.get(wordMarkupForm)
					inputOtherTypeDict[wordMarkupForm] = newCount
				else:
					inputOtherTypeDict[wordMarkupForm] = 1
				if (length == 2):
					inputSingleOtherTokenCount += 1
					inputTotalOtherTokenCount += 1
				elif (length == 3):
					inputDoubleOtherTokenCount += 1
					inputTotalOtherTokenCount += 1
				else:
					inputTotalOtherTokenCount += 1
		return
	else:
		## Missing morphological tags (despite intro line)
		return

def evalInputData(inputString, inputTags):
	global totalSingleUtteranceMotherLines, inputSingleNounTypeDict, inputSingleVerbTypeDict, totalDoubleWordMotherLines, totalLongMotherLines
	global inputSingleOtherTypeDict, inputDoubleNounTypeDict, inputDoubleVerbTypeDict, inputDoubleOtherTypeDict, exampleFile

#	toTag = inputString[1:]
#	taggedInput = nltk.pos_tag(toTag)

	if (len(inputString) == 2):
		totalSingleUtteranceMotherLines += 1
		for token in inputString:
			exampleFile.write(token + ' ')
		exampleFile.write('\n')
		for inputTag in inputTags:
			exampleFile.write(inputTag + ' ')
		exampleFile.write('\n\n')
		extractIsolatedWordInfo(len(inputString), inputTags, inputSingleNounTypeDict, inputSingleVerbTypeDict, inputSingleOtherTypeDict)
	elif (len(inputString) == 3):
		totalDoubleWordMotherLines += 1
		extractIsolatedWordInfo(len(inputString), inputTags, inputDoubleNounTypeDict, inputDoubleVerbTypeDict, inputDoubleOtherTypeDict)
	
	totalLongMotherLines += 1
	extractIsolatedWordInfo(len(inputString), inputTags, inputTotalNounTypeDict, inputTotalVerbTypeDict, inputTotalOtherTypeDict)


def evalOutputData(outputString, outputTags):
	global outputNounTokenCount, outputVerbTokenCount, outputNounTypeDict, outputVerbTypeDict, outputOtherTokenCount, outputOtherTypeDict

#	if (len(outputString) != len(outputTags)):
#		print outputString
#		print outputTags
#		print ''
	for currTag in outputTags:

		currTagInfo = currTag.split("|")
		if len(currTagInfo) > 1:
			currPos = currTagInfo[0]
			currWord = currTagInfo[1]
			if (currPos in verbSet):
				outputVerbTokenCount += 1
				if (currWord in outputVerbTypeDict):
					newCount = 1 + outputVerbTypeDict.get(currWord)
					outputVerbTypeDict[currWord] = newCount
				else:
					outputVerbTypeDict[currWord] = 1
			elif (currPos in nounSet):
				outputNounTokenCount += 1
				if (currWord in outputNounTypeDict):
					newCount = 1 + outputNounTypeDict.get(currWord)
					outputNounTypeDict[currWord] = newCount
				else:
					outputNounTypeDict[currWord] = 1
			else:
				outputOtherTokenCount += 1
				if (currWord in outputOtherTypeDict):
					newCount = 1 + outputOtherTypeDict.get(currWord)
					outputOtherTypeDict[currWord] = newCount
				else:
					outputOtherTypeDict[currWord] = 1
		# if (currTagInfo[0] == 'n'):
		# 	outputNounTokenCount += 1
		# elif (currTagInfo[0] == 'v'):
		# 	outputVerbTokenCount += 1



def iterateSubDir(directoryName):
	# call function to iterate over any ".cha" files in this directory
	readChaFiles(directoryName)

	# going through each immediate subdirectory
	for subDir in next(os.walk(directoryName))[1]:
		subDirPath = directoryName + subDir + '/'
		os.chdir(subDirPath)
		readChaFiles(subDirPath)

def safeDivide(numerator, denominator):
	if denominator > 0:
		return (numerator / (denominator * 1.0))
	else:
		return 0.0

##
## Main method block
##
if __name__=="__main__":
	if (len(sys.argv) < 3):
		print('incorrect number of arguments')
		exit(0)

	directoryName = sys.argv[1]
	exampleFilename = sys.argv[2]
	with open(exampleFilename, 'w') as exampleFile:

		totalMotherLines = 0
		cumulativeMotherLinesLength = 0
		totalSingleUtteranceMotherLines = 0
		totalDoubleWordMotherLines = 0
		totalLongMotherLines = 0
		totalDataLength = 0

		totalChildLines = 0
		cumulativeChildLinesLength = 0

		searchDirectory = os.getcwd() + '/' + directoryName
		iterateSubDir(searchDirectory)
	exampleFile.close()

	motherMLU = safeDivide(cumulativeMotherLinesLength, totalMotherLines)
	childMLU = safeDivide(cumulativeChildLinesLength, totalChildLines)

	print 'totalDataLength: ' + str(totalDataLength)
	print('-----------------------------------------')
	print 'totalMotherLines: ' + str(totalMotherLines)
	print 'mother MLU: ' + str(motherMLU)

	print 'totalSingleWordUtteranceMotherLines: ' + str(totalSingleUtteranceMotherLines)
	print 'singleWordNounTokens: ' + str(inputSingleNounTokenCount)
	print 'singleWordNounTypes: ' + str(len(inputSingleNounTypeDict))
	print 'singleWordVerbTokens: ' + str(inputSingleVerbTokenCount)
	print 'singleWordVerbTypes: ' + str(len(inputSingleVerbTypeDict))
	print 'singleWordOtherTokens: ' + str(inputSingleOtherTokenCount)
	print 'singleWordOtherTypes: ' + str(len(inputSingleOtherTypeDict))
	singleWordNounTokenProp = inputSingleNounTokenCount / (1.0 * (inputSingleNounTokenCount + inputSingleVerbTokenCount + inputSingleOtherTokenCount))
	singleWordVerbTokenProp = inputSingleVerbTokenCount / (1.0 * (inputSingleNounTokenCount + inputSingleVerbTokenCount + inputSingleOtherTokenCount))
	singleWordOtherTokenProp = inputSingleOtherTokenCount / (1.0 * (inputSingleNounTokenCount + inputSingleVerbTokenCount + inputSingleOtherTokenCount))
	singleWordNounTypeProp = len(inputSingleNounTypeDict) / (1.0 * (len(inputSingleNounTypeDict) + len(inputSingleVerbTypeDict) + len(inputSingleOtherTypeDict)))
	singleWordVerbTypeProp = len(inputSingleVerbTypeDict) / (1.0 * (len(inputSingleNounTypeDict) + len(inputSingleVerbTypeDict) + len(inputSingleOtherTypeDict)))
	singleWordOtherTypeProp = len(inputSingleOtherTypeDict) / (1.0 * (len(inputSingleNounTypeDict) + len(inputSingleVerbTypeDict) + len(inputSingleOtherTypeDict)))
	print 'singleWordNounTokenProp: ' + str(singleWordNounTokenProp)
	print 'singleWordVerbTokenProp: ' + str(singleWordVerbTokenProp)
	print 'singleWordOtherTokenProp: ' + str(singleWordOtherTokenProp)
	print 'singleWordNounTypeProp: ' + str(singleWordNounTypeProp)
	print 'singleWordVerbTypeProp: ' + str(singleWordVerbTypeProp)
	print 'singleWordOtherTypeProp: ' + str(singleWordOtherTypeProp)


	print 'totalTwoWordUtteranceMotherLines: ' + str(totalDoubleWordMotherLines)
	print 'twoWordNounTokens: ' + str(inputDoubleNounTokenCount)
	print 'twoWordNounTypes: ' + str(len(inputDoubleNounTypeDict))
	print 'twoWordVerbTokens: ' + str(inputDoubleVerbTokenCount)
	print 'twoWordVerbTypes: ' + str(len(inputDoubleVerbTypeDict))
	print 'twoWordOtherTokens: ' + str(inputDoubleOtherTokenCount)
	print 'twoWordOtherTypes: ' + str(len(inputDoubleOtherTypeDict))
	doubleWordNounTokenProp = inputDoubleNounTokenCount / (1.0 * (inputDoubleNounTokenCount + inputDoubleVerbTokenCount + inputDoubleOtherTokenCount))
	doubleWordVerbTokenProp = inputDoubleVerbTokenCount / (1.0 * (inputDoubleNounTokenCount + inputDoubleVerbTokenCount + inputDoubleOtherTokenCount))
	doubleWordOtherTokenProp = inputDoubleOtherTokenCount / (1.0 * (inputDoubleNounTokenCount + inputDoubleVerbTokenCount + inputDoubleOtherTokenCount))
	doubleWordNounTypeProp = len(inputDoubleNounTypeDict) / (1.0 * (len(inputDoubleNounTypeDict) + len(inputDoubleVerbTypeDict) + len(inputDoubleOtherTypeDict)))
	doubleWordVerbTypeProp = len(inputDoubleVerbTypeDict) / (1.0 * (len(inputDoubleNounTypeDict) + len(inputDoubleVerbTypeDict) + len(inputDoubleOtherTypeDict)))
	doubleWordOtherTypeProp = len(inputDoubleOtherTypeDict) / (1.0 * (len(inputDoubleNounTypeDict) + len(inputDoubleVerbTypeDict) + len(inputDoubleOtherTypeDict)))
	print 'doubleWordNounTokenProp: ' + str(doubleWordNounTokenProp)
	print 'doubleWordVerbTokenProp: ' + str(doubleWordVerbTokenProp)
	print 'doubleWordOtherTokenProp: ' + str(doubleWordOtherTokenProp)
	print 'doubleWordNounTypeProp: ' + str(doubleWordNounTypeProp)
	print 'doubleWordVerbTypeProp: ' + str(doubleWordVerbTypeProp)
	print 'doubleWordOtherTypeProp: ' + str(doubleWordOtherTypeProp)

	print 'totalMotherLines: ' + str(totalLongMotherLines)
	print 'totalNounTokens: ' + str(inputTotalNounTokenCount)
	print 'totalNounTypes: ' + str(len(inputTotalNounTypeDict))
	print 'totalVerbTokens: ' + str(inputTotalVerbTokenCount)
	print 'totalVerbTypes: ' + str(len(inputTotalVerbTypeDict))
	print 'totalOtherTokens: ' + str(inputTotalOtherTokenCount)
	print 'totalOtherTypes: ' + str(len(inputTotalOtherTypeDict))
	totalWordNounTokenProp = inputTotalNounTokenCount / (1.0 * (inputTotalNounTokenCount + inputTotalVerbTokenCount + inputTotalOtherTokenCount))
	totalWordVerbTokenProp = inputTotalVerbTokenCount / (1.0 * (inputTotalNounTokenCount + inputTotalVerbTokenCount + inputTotalOtherTokenCount))
	totalWordOtherTokenProp = inputTotalOtherTokenCount / (1.0 * (inputTotalNounTokenCount + inputTotalVerbTokenCount + inputTotalOtherTokenCount))
	totalWordNounTypeProp = len(inputTotalNounTypeDict) / (1.0 * (len(inputTotalNounTypeDict) + len(inputTotalVerbTypeDict) + len(inputTotalOtherTypeDict)))
	totalWordVerbTypeProp = len(inputTotalVerbTypeDict) / (1.0 * (len(inputTotalNounTypeDict) + len(inputTotalVerbTypeDict) + len(inputTotalOtherTypeDict)))
	totalWordOtherTypeProp = len(inputTotalOtherTypeDict) / (1.0 * (len(inputTotalNounTypeDict) + len(inputTotalVerbTypeDict) + len(inputTotalOtherTypeDict)))
	print 'totalWordNounTokenProp: ' + str(totalWordNounTokenProp)
	print 'totalWordVerbTokenProp: ' + str(totalWordVerbTokenProp)
	print 'totalWordOtherTokenProp: ' + str(totalWordOtherTokenProp)
	print 'totalWordNounTypeProp: ' + str(totalWordNounTypeProp)
	print 'totalWordVerbTypeProp: ' + str(totalWordVerbTypeProp)
	print 'totalWordOtherTypeProp: ' + str(totalWordOtherTypeProp)

	print('-----------------------------------------')

	print 'totalChildLines: ' + str(totalChildLines)
	print 'child MLU: ' + str(childMLU)
	print 'childNounTokens: ' + str(outputNounTokenCount)
	print 'childNounTypes: ' + str(len(outputNounTypeDict))
	print 'childVerbTokens: ' + str(outputVerbTokenCount)
	print 'childverbTypes: ' + str(len(outputVerbTypeDict))
	print 'childOtherTokens: ' + str(outputOtherTokenCount)
	print 'childOtherTypes: ' + str(len(outputOtherTypeDict))
	totalChildNounTokenProp = outputNounTokenCount / (1.0 * (outputNounTokenCount + outputVerbTokenCount + outputOtherTokenCount))
	totalChildVerbTokenProp = outputVerbTokenCount / (1.0 * (outputNounTokenCount + outputVerbTokenCount + outputOtherTokenCount))
	totalChildOtherTokenProp = outputOtherTokenCount / (1.0 * (outputNounTokenCount + outputVerbTokenCount + outputOtherTokenCount))
	totalChildNounTypeProp = len(outputNounTypeDict) / (1.0 * (len(outputNounTypeDict) + len(outputVerbTypeDict) + len(outputOtherTypeDict)))
	totalChildVerbTypeProp = len(outputVerbTypeDict) / (1.0 * (len(outputNounTypeDict) + len(outputVerbTypeDict) + len(outputOtherTypeDict)))
	totalChildOtherTypeProp = len(outputOtherTypeDict) / (1.0 * (len(outputNounTypeDict) + len(outputVerbTypeDict) + len(outputOtherTypeDict)))
	print 'totalChildNounTokenProp: ' + str(totalChildNounTokenProp)
	print 'totalChildVerbTokenProp: ' + str(totalChildVerbTokenProp)
	print 'totalChildOtherTokenProp: ' + str(totalChildOtherTokenProp)
	print 'totalChildNounTypeProp: ' + str(totalChildNounTypeProp)
	print 'totalChildVerbTypeProp: ' + str(totalChildVerbTypeProp)
	print 'totalChildOtherTypeProp: ' + str(totalChildOtherTypeProp)

	print '\nmissingSpeechLines: ' + str(missingSpeechLines)