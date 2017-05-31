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
							extractMotherUtteranceStats(cleanedWords)
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

def extractMotherUtteranceStats(words):
	global motherRightEdgeNonIsoWords, motherIsolatedWords
	if len(words) == 1:
		motherIsolatedWords = incrementDict(motherIsolatedWords, words[0])
	else:
		finalWord = words[-1]
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
			freq = currTokens[0]
			cleanedWord = regex.sub('', currTokens[1])
			updateDictWithValue(charlesFreqDict, cleanedWord, freq)
		#	print charlesFreqDict[cleanedWord], cleanedWord, freq

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

##
## Main method block
##
if __name__=="__main__":
	if (len(sys.argv) < 3):
		print('incorrect number of arguments')
		exit(0)


	directoryName = sys.argv[1]
	charlesFreqFileName = sys.argv[2]
	readWordList(charlesFreqFileName)
	searchDirectory = os.getcwd() + '/' + directoryName
	iterateSubDir(searchDirectory)

	wordCount = 0
	#for word in motherWords.iteritems():
	for entry in motherWords.iteritems():
		word = entry[0]
		motherCount = entry[1]

		motherIsoCount = 0
		motherFinalNonIsoCount = 0
		childCount = 0
		charlesFreqCount = 0

		if word in motherIsolatedWords:
   			motherIsoCount = motherIsolatedWords[word]
		if word in motherRightEdgeNonIsoWords:
   			motherFinalNonIsoCount = motherRightEdgeNonIsoWords[word]
		if word in childWords:
   			childCount = childWords[word]
		if word in charlesFreqDict:
   			charlesFreqCount = charlesFreqDict[word]


   		if charlesFreqCount > 0:
   			## elements produced by mother (and also in Charles frequency list)
   			wordCount += 1
   			print word, charlesFreqCount, childCount, motherCount, motherIsoCount, motherFinalNonIsoCount


# print 'Num words: ', wordCount

#	for speaker, filename in readChildes.missingSpeakerInfoDict.iteritems():
#		print speaker, filename

#	childWordsSorted = sorted(childWords.items(), key=operator.itemgetter(1))

	## reversed(list)
#	for entry in childWordsSorted:
#		word = entry[0]
#		freq = entry[1]
	#	print word, freq