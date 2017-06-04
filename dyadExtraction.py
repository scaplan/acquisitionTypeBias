#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, os, subprocess, glob, nltk, re, operator
import readChildes
from string import punctuation
from nltk import word_tokenize
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

punctuationSet = ['.', '?', '!', ':', '(.)', '+...', '+"/.', '+/.']
morphCue = ['%mor:', '%xmor:', '%newmor:', '%trn:']
motherSet = ['*mot:', '*gra:', '*fat:', '*ann:', '*ant:', '*nan:', '*wom:', '*car:', '*inv:', '*par:', '*mut:', '*vat:', '*oma:', '*exp:', '*car:', '*bri', '*nen:', '*mag:', '*gmt:']
childSet = ['*chi:', '*eli:', '*gre:', '*mar:']

regex = re.compile('[^a-z]')

missingSpeakerInfoDict = {}

childWords = {}
motherWords = {}
motherIsolatedWords = {}
motherRightEdgeNonIsoWords = {}
charlesFreqDict = {}

### Key: Word
### Tuple Value: charlesChildesFrequency(0), motherTotalFreq(1), childTotalFreq(2), motherIsolatedUtterenceCount(3), motherUtteranceFinalLongCount(4)

def readChaFile(dataFileName):
	global motherWords, childWords
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
				# Needs full group to extract from
				if (len(speechGroup) > 1):
					cleanedSpeechLine, cleanedTagLine = cleanSpeechGroup(speechGroup)
					#print cleanedSpeechLine
					#print cleanedTagLine
					#print '\n'
					if len(cleanedSpeechLine) > 0:
						speaker = cleanedSpeechLine[0]
						cleanedWords = []
						for word in cleanedSpeechLine[1:]:
							cleanedWord = regex.sub('', word)
							cleanedWords.append(cleanedWord)

						if speaker in motherSet:
							for word in cleanedWords:
							#	print word
								motherWords = incrementDict(motherWords, word)
							#	print motherWords[word]
							extractMotherUtteranceStats(cleanedWords, cleanedSpeechLine)
							#print cleanedWords
						elif speaker in childSet:
							for word in cleanedWords:
								childWords = incrementDict(childWords, word)
							#print cleanedSpeechLine
						else:
							missingSpeakerInfoDict[speaker] = dataFileName
					else:
						print 'EMPTY SPEECH LINE'
						sys.exit()
				speechGroup = []

			speechGroup.append(currLine)

def extractMotherUtteranceStats(words, currLine):
	global motherRightEdgeNonIsoWords, motherIsolatedWords
	if len(words) == 1:
		motherIsolatedWords = incrementDict(motherIsolatedWords, words[0])
	else:
		finalWord = words[-1]
	#	if finalWord == 'the':
	#		print currLine
	#		print words
	#		print finalWord
		motherRightEdgeNonIsoWords = incrementDict(motherRightEdgeNonIsoWords, finalWord)


def incrementDict(dictToUpdate, key):
	if key in dictToUpdate:
		prevValue = dictToUpdate.get(key)
		dictToUpdate[key] = prevValue + 1
	else:
		dictToUpdate[key] = 1
	return dictToUpdate

def updateDictWithValue(dictToUpdate, key, value):
	if key in dictToUpdate:
		prevValue = dictToUpdate.get(key)
		dictToUpdate[key] = prevValue + value
	else:
		dictToUpdate[key] = value
	return dictToUpdate

def readChildesDirectory(sourceDir):
	for dataFileName in glob.glob(sourceDir+"*.cha"):
		#	print (os.getcwd() + '/' + dataFileName)
		readChaFile(dataFileName)


def iterateSubDir(directoryName):
	# call function to iterate over any ".cha" files in this directory
	readChildesDirectory(directoryName)

	# going through each immediate subdirectory
	for subDir in next(os.walk(directoryName))[1]:
		subDirPath = directoryName + subDir + '/'
		os.chdir(subDirPath)
		readChildesDirectory(subDirPath)

def readWordList(source):
	with open(source, 'r') as inputFile:
		for currLine in inputFile:
			if not currLine:
				continue
			currTokens = currLine.split()
			freq = int(currTokens[0])
			cleanedWord = regex.sub('', currTokens[1])
			updateDictWithValue(charlesFreqDict, cleanedWord, freq)
		#	if cleanedWord == 'you':
		#		print charlesFreqDict[cleanedWord], cleanedWord, freq

def cleanSpeechGroup(speechGroup):
	speechLine = speechGroup[0]
	tagTokens = []
	tagTokensNoPunc = []
	for entry in speechGroup:
		entryTokens = entry.split()
		if (entryTokens[0] in morphCue):
			tagTokens = entryTokens
			tagTokensNoPunc = [x for x in tagTokens if x not in punctuationSet]

	currLineTokens = speechLine.split()
	onlyAlphaNumerics = []
	for token in currLineTokens:
		valid = re.search('[a-z]', token) is not None
		if valid:
			onlyAlphaNumerics.append(token)

	# print onlyAlphaNumerics
	return onlyAlphaNumerics, tagTokensNoPunc

def printOutputWithGlobalFreq(outputFile, globalTotalCorpusCount):
	global childTotalCorpusCount, motherTotalCorpusCount, motherTotalCorpusCount, motherTotalIsoCount, motherTotalFinalNonIso

	wordCount = 0
	outputFile.write('word charlesFreqCount charlesFreqProb childAttested childCount childFreqProb motherCount motherFreqProb motherIsoCount motherIsoProb motherFinalNonIsoCount motherFinalNonIsoProb\n')
	#for word in motherWords.iteritems():
	for entry in motherWords.iteritems():
		word = entry[0]
		motherCount = entry[1]

		motherIsoCount = 0
		motherFinalNonIsoCount = 0
		childCount = 0
		charlesFreqCount = 0
		childAttested = 0

		if word in motherIsolatedWords:
   			motherIsoCount = motherIsolatedWords[word]
		if word in motherRightEdgeNonIsoWords:
   			motherFinalNonIsoCount = motherRightEdgeNonIsoWords[word]
		if word in childWords:
   			childCount = childWords[word]
   			childAttested = 1
		if word in charlesFreqDict:
   			charlesFreqCount = int(charlesFreqDict[word])

   		if charlesFreqCount > 0:
   			## elements produced by mother (and also in Charles frequency list)
   			wordCount += 1

   			## Convert these to proportions as well
   			charlesFreqProb = charlesFreqCount / (1.0 * globalTotalCorpusCount)
   			charlesFreqLogProb = math.log(charlesFreqProb)
   			childFreqProb = childCount / (1.0 * childTotalCorpusCount)
   		#	childFreqLogProb = math.log(childFreqProb)
   			motherFreqProb = motherCount / (1.0 * motherTotalCorpusCount)
   			motherFreqLogProb = math.log(motherFreqProb)
   			motherIsoProb = motherIsoCount / (1.0 * motherTotalIsoCount)
   		#	motherIsoLogProb = math.log(motherIsoProb)
   			motherFinalNonIsoProb = motherFinalNonIsoCount / (1.0 * motherTotalFinalNonIso)
   		#	motherFinalNonIsoLogProb = math.log(motherFinalNonIsoProb)

   			outputFile.write(word + " " + str(charlesFreqCount) + " " + str(charlesFreqProb) + " " + str(childAttested) + " " + str(childCount) + " " + str(childFreqProb) + " " + str(motherCount) + " " + str(motherFreqProb) + " " + str(motherIsoCount) + " " + str(motherIsoProb) + " " + str(motherFinalNonIsoCount) + " " + str(motherFinalNonIsoProb) + "\n")

def printOutputNoGlobalInfo(outputFile):
	global childTotalCorpusCount, motherTotalCorpusCount, motherTotalCorpusCount, motherTotalIsoCount, motherTotalFinalNonIso

	wordCount = 0
	outputFile.write('word childAttested childCount childFreqProb motherCount motherFreqProb motherIsoCount motherIsoProb motherFinalNonIsoCount motherFinalNonIsoProb\n')
	#for word in motherWords.iteritems():
	for entry in motherWords.iteritems():
		word = entry[0]
		motherCount = entry[1]

		motherIsoCount = 0
		motherFinalNonIsoCount = 0
		childCount = 0
		childAttested = 0

		if word in motherIsolatedWords:
   			motherIsoCount = motherIsolatedWords[word]
		if word in motherRightEdgeNonIsoWords:
   			motherFinalNonIsoCount = motherRightEdgeNonIsoWords[word]
		if word in childWords:
   			childCount = childWords[word]
   			childAttested = 1

		## elements produced by mother
		wordCount += 1
		## Convert these to proportions as well
		childFreqProb = childCount / (1.0 * childTotalCorpusCount)
	#	childFreqLogProb = math.log(childFreqProb)
		motherFreqProb = motherCount / (1.0 * motherTotalCorpusCount)
		motherFreqLogProb = math.log(motherFreqProb)
		motherIsoProb = motherIsoCount / (1.0 * motherTotalIsoCount)
	#	motherIsoLogProb = math.log(motherIsoProb)
		motherFinalNonIsoProb = motherFinalNonIsoCount / (1.0 * motherTotalFinalNonIso)
	#	motherFinalNonIsoLogProb = math.log(motherFinalNonIsoProb)

		outputFile.write(word + " " + str(childAttested) + " " + str(childCount) + " " + str(childFreqProb) + " " + str(motherCount) + " " + str(motherFreqProb) + " " + str(motherIsoCount) + " " + str(motherIsoProb) + " " + str(motherFinalNonIsoCount) + " " + str(motherFinalNonIsoProb) + "\n")

##
## Main method block
##
if __name__=="__main__":
	if (len(sys.argv) < 3):
		print('incorrect number of arguments')
		exit(0)

	directoryName = sys.argv[1]
	outputFileName = sys.argv[2]

	searchDirectory = os.getcwd() + '/' + directoryName
	iterateSubDir(searchDirectory)
	childTotalCorpusCount = sum(childWords.values())
	motherTotalCorpusCount = sum(motherWords.values())
	motherTotalIsoCount = sum(motherIsolatedWords.values())
	motherTotalFinalNonIso = sum(motherRightEdgeNonIsoWords.values())

	with open(outputFileName,'w') as outputFile:
		if (len(sys.argv) > 3):
			print('Running with global frequency list')
			charlesFreqFileName = sys.argv[3]
			readWordList(charlesFreqFileName)
			charlesTotalCorpusCount = sum(charlesFreqDict.values())
			printOutputWithGlobalFreq(outputFile, charlesTotalCorpusCount)
		elif (len(sys.argv) == 3):
			print('Running without global frequency list')
			printOutputNoGlobalInfo(outputFile)
	outputFile.close()