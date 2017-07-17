#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Spencer Caplan
# Department of Linguistics, University of Pennsylvania
# Contact: spcaplan@sas.upenn.edu

import sys, math, os, subprocess, glob, nltk, re, operator
import argparse
import readChildes
import syllableCount
from string import punctuation
from nltk import word_tokenize
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

punctuationSet = ['.', '?', '!', ':', '(.)', '+...', '+"/.', '+/.']
morphCue = ['%mor:', '%xmor:', '%newmor:', '%trn:']
motherSet = ['*mot:', '*gra:', '*fat:', '*ann:', '*ant:', '*nan:', '*wom:', '*car:', '*inv:', '*par:', '*mut:', '*vat:', '*oma:', '*exp:', '*car:', '*bri', '*nen:', '*mag:', '*gmt:', '*tmo:', '*exa:']
childSet = ['*chi:', '*eli:', '*gre:', '*mar:', '*tai:']

regex = re.compile('[^a-z]')

missingSpeakerInfoDict = {}

childWords = {}
motherWords = {}
motherIsolatedWords = {}
motherRightEdgeNonIsoWords = {}
charlesFreqDict = {}

# Key: word
# Value: dict mapping from POS to count
wordPOSdict = {}

### Key: Word
### Tuple Value: charlesChildesFrequency(0), motherTotalFreq(1), childTotalFreq(2), motherIsolatedUtterenceCount(3), motherUtteranceFinalLongCount(4)

def readChaFile(dataFileName):
	global motherWords, childWords#, readChinChar
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
					cleanedSpeechLine, cleanedTagLine = readChildes.cleanSpeechGroup(speechGroup)
					#print cleanedSpeechLine
					#print cleanedTagLine
					#print '\n'
					if len(cleanedSpeechLine) > 0:
						speaker = cleanedSpeechLine[0]
						cleanedWords = []
						if not args.readChineseData:
							for word in cleanedSpeechLine[1:]:
								cleanedWord = regex.sub('', word)
								cleanedWords.append(cleanedWord)
						else:
							for word in cleanedSpeechLine[1:]:
								cleanedWords.append(word)

						extractPartOfSpeechInfo(cleanedTagLine)
						if speaker in motherSet:
							for word in cleanedWords:
							#	print word
								motherWords = readChildes.incrementDict(motherWords, word)
							#	print motherWords[word]
							extractMotherUtteranceStats(cleanedWords, cleanedSpeechLine)
							#print cleanedWords
						elif speaker in childSet:
							for word in cleanedWords:
								childWords = readChildes.incrementDict(childWords, word)
							#print cleanedSpeechLine
						else:
							missingSpeakerInfoDict[speaker] = dataFileName
					else:
						print 'EMPTY SPEECH LINE'
						sys.exit()
				speechGroup = []

			speechGroup.append(currLine)

def extractPartOfSpeechInfo(tagLine):
	for entry in tagLine:
		entryPieces = entry.split('|')
		if len(entryPieces) == 2:
			currTag = entryPieces[0]
			currWord = entryPieces[1]

			currWord, sep, tail = currWord.partition('-')
			currWord, sep, tail = currWord.partition('&')
			currWord, sep, tail = currWord.partition('~')
			currWord, sep, tail = currWord.partition('=')

		#	print currWord
			if currWord in wordPOSdict:
				currWordTagDict = wordPOSdict[currWord]
				currWordTagDict = readChildes.incrementDict(currWordTagDict, currTag)
			else:
				currWordTagDict = {}
				currWordTagDict = readChildes.incrementDict(currWordTagDict, currTag)
				wordPOSdict[currWord] = currWordTagDict
		#elif len(entryPieces) > 2:
		#	print entryPieces

def getMostFreqTag(wordToCheck):
	highestTag = 'NA'
	highestTagCount = 0
	if wordToCheck in wordPOSdict:
		currWordTagDict = wordPOSdict[wordToCheck]
		for tag in currWordTagDict:
			count = currWordTagDict[tag]
			if count > highestTagCount:
				highestTagCount = count
				highestTag = tag
	return highestTag

def extractMotherUtteranceStats(words, currLine):
	global motherRightEdgeNonIsoWords, motherIsolatedWords
	#print words
	if len(words) == 1:
		motherIsolatedWords = readChildes.incrementDict(motherIsolatedWords, words[0])
	elif len(words) > 1:
		finalWord = words[-1]
	#	if finalWord == 'the':
	#		print currLine
	#		print words
	#		print finalWord
		motherRightEdgeNonIsoWords = readChildes.incrementDict(motherRightEdgeNonIsoWords, finalWord)


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
			readChildes.updateDictWithValue(charlesFreqDict, cleanedWord, freq)
		#	if cleanedWord == 'you':
		#		print charlesFreqDict[cleanedWord], cleanedWord, freq

def cleanDict(dictToClean, blacklist):
	for word in blacklist:
		if word in dictToClean:
			try:
				del dictToClean[word]
			except KeyError:
				pass
	return dictToClean

def safeDivide(numerator, denominator):
	if denominator > 0:
		return (numerator / (denominator * 1.0))
	else:
		return 0.0


def readInCDI(inputFileName):
	global childWords
	with open(inputFileName,'r') as inputFile:
		for currLine in inputFile:
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
			print currLineTokens
			activeOrPassive = currLineTokens[0]
			#print activeOrPassive
			if activeOrPassive == 'speak' or activeOrPassive == 'understand':
				for word in currLineTokens[1:]:
					print word
					childWords = readChildes.incrementDict(childWords, word)





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
   			motherIsoProb = motherIsoCount / (1.0 * motherTotalIsoCount)
   		#	motherIsoLogProb = math.log(motherIsoProb)
   			motherFinalNonIsoProb = motherFinalNonIsoCount / (1.0 * motherTotalFinalNonIso)
   		#	motherFinalNonIsoLogProb = math.log(motherFinalNonIsoProb)

   			outputFile.write(word + " " + str(charlesFreqCount) + " " + str(charlesFreqProb) + " " + str(childAttested) + " " + str(childCount) + " " + str(childFreqProb) + " " + str(motherCount) + " " + str(motherFreqProb) + " " + str(motherIsoCount) + " " + str(motherIsoProb) + " " + str(motherFinalNonIsoCount) + " " + str(motherFinalNonIsoProb) + "\n")

def printOutputNoGlobalInfo(outputFile):
	global childTotalCorpusCount, motherTotalCorpusCount, motherTotalCorpusCount, motherTotalIsoCount, motherTotalFinalNonIso

	### Add: POS
	wordCount = 0
	#outputFile.write('word POS binarizedTag charLength numSylls childAttested childCount childFreqProb motherCount motherBucket motherFreqProb motherIsoCount motherIsoBucket motherIsoProb motherFinalNonIsoCount motherFinalBucket motherFinalNonIsoProb\n')
	outputFile.write('word POS nounStatus verbStatus charLength numSylls childAttested childCount motherCount motherBucket motherIsoCount motherIsoBucket motherFinalNonIsoCount motherFinalBucket\n')

	#for word in motherWords.iteritems():
	for entry in motherWords.iteritems():
		word = entry[0]
		motherCount = entry[1]

		partOfSpeech = getMostFreqTag(word)
		binarizedTag = binarizePOS(partOfSpeech)
		nounStatus = 0
		verbStatus = 0
		if binarizedTag == 'noun':
			nounStatus = 1
		if binarizedTag == 'verb':
			verbStatus = 1
		wordLength = len(word)
		numSylls = syllableCount.countVowelClusters(word)

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

   		motherTotalBucket = convertFreqCountToBucket(motherCount)
   		motherIsoBucket = convertFreqCountToBucket(motherIsoCount)
   		motherFinalBucket = convertFreqCountToBucket(motherFinalNonIsoCount)


		## elements produced by mother
		wordCount += 1
		## Convert these to proportions as well
		childFreqProb = safeDivide(childCount, childTotalCorpusCount)
		motherFreqProb = safeDivide(motherCount, motherTotalCorpusCount)
		motherIsoProb = safeDivide(motherIsoCount, motherTotalIsoCount)
		motherFinalNonIsoProb = safeDivide(motherFinalNonIsoCount, motherTotalFinalNonIso)

		#outputFile.write(word + " " + partOfSpeech + " " + binarizedTag + " " + str(wordLength) + " " + str(numSylls) + " " + str(childAttested) + " " + str(childCount) + " " + str(childFreqProb) + " " + str(motherCount) + " " + motherTotalBucket + " " + str(motherFreqProb) + " " + str(motherIsoCount) + " " + motherIsoBucket + " " + str(motherIsoProb) + " " + str(motherFinalNonIsoCount) + " " + motherFinalBucket + " " + str(motherFinalNonIsoProb) + "\n")
		outputFile.write(word + " " + partOfSpeech + " " + str(nounStatus) + " " + str(verbStatus) + " " + str(wordLength) + " " + str(numSylls) + " " + str(childAttested) + " " + str(childCount) + " " + str(motherCount) + " " + motherTotalBucket + " " + str(motherIsoCount) + " " + motherIsoBucket + " " + str(motherFinalNonIsoCount) + " " + motherFinalBucket + "\n")



def binarizePOS(currPOS):
	if currPOS == 'n':
		return 'noun'
	elif currPOS == 'v':
		return 'verb'
	else:
		return 'other'

def convertFreqCountToBucket(count):
	if count == 0:
		return 'none'
	elif count < 4:
		return 'rare'
	else:
		return 'frequent'

##
## Main method block
##
if __name__=="__main__":

	parser = argparse.ArgumentParser(description = "Dyad-Extraction for Studying Early Vocabulary Development")

	parser.add_argument("inputDir", help="input directory containing corpus of child/care-giver dyad")
	parser.add_argument("outputFile", help="output filename", type=argparse.FileType('w'))
	parser.add_argument("-cdi", "--cdiFile", help="read in cdi file if provided", type=str, nargs='?', default='')
	parser.add_argument("-ch", "--readChineseData", help="boolean for reading in Chinese data rather than Latin script", type=bool, nargs='?', default=False)
	parser.add_argument("-f", "--globalFreqFile", help="read in global frequency file if provided", type=str, nargs='?', default='')

	args = parser.parse_args()
	print(args)
	if not args.inputDir:
		raise Exception("Need pointer to input directory!")
	if not args.outputFile:
		raise Exception("Need to specify output source!")

	if args.cdiFile:
		print 'reading CDI data'
		readInCDI(args.cdiFile)

	if args.readChineseData:
		print 'reading Chinese data'

	searchDirectory = os.getcwd() + '/' + args.inputDir
	iterateSubDir(searchDirectory)

	blacklist = ['xxx', 'yyy']
	childWords = cleanDict(childWords, blacklist)
	motherWords = cleanDict(motherWords, blacklist)
	motherIsolatedWords = cleanDict(motherIsolatedWords, blacklist)
	motherRightEdgeNonIsoWords = cleanDict(motherRightEdgeNonIsoWords, blacklist)

	childTotalCorpusCount = sum(childWords.values())
	motherTotalCorpusCount = sum(motherWords.values())
	motherTotalIsoCount = sum(motherIsolatedWords.values())
	motherTotalFinalNonIso = sum(motherRightEdgeNonIsoWords.values())


	if args.globalFreqFile:
		readWordList(args.globalFreqFile)
		charlesTotalCorpusCount = sum(charlesFreqDict.values())
		printOutputWithGlobalFreq(args.outputFile, charlesTotalCorpusCount)
	else:
		print('Running without global frequency list')
		printOutputNoGlobalInfo(args.outputFile)

	args.outputFile.close()