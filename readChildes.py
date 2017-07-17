#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, os, subprocess, glob, nltk, re
from nltk import word_tokenize
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

punctuationSet = ['.', '?', '!', ':', '(.)', '+...', '+"/.', '+/.']
morphCue = ['%mor:', '%xmor:', '%newmor:', '%trn:']
motherSet = ['*mot:', '*gra:', '*fat:', '*ann:', '*ant:', '*nan:', '*wom:', '*car:', '*inv:', '*par:', '*mut:', '*vat:', '*oma:', '*exp:', '*car:', '*bri', '*nen:', '*mag:', '*gmt:']
childSet = ['*chi:', '*eli:', '*gre:', '*mar:']

missingSpeakerInfoDict = {}

def readChaFile(dataFileName):
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
						if speaker in motherSet:
							print cleanedSpeechLine
						elif speaker in childSet:
							print cleanedSpeechLine
						else:
							missingSpeakerInfoDict[speaker] = dataFileName
					else:
						print 'EMPTY SPEECH LINE'
						sys.exit()
				speechGroup = []

			speechGroup.append(currLine)


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