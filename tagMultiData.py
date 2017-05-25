#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, os, subprocess, glob, nltk, re
from nltk import word_tokenize
from polyglot.text import Text
from polyglot.detect import Detector
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

punctuationSet = ['.', '?', '!', ':', '(.)', '+...', '+"/.', '+/.']

def tagLine(inputLine):
	currLineTokens = inputLine.split()

#	currLineTokensNoPunc = [x for x in currLineTokens if x not in punctuationSet]
	# onlyAlphaNumerics = []
	# for token in currLineTokens:
	# 	valid = re.search('[a-z]', token) is not None
	# 	if valid:
	# 		onlyAlphaNumerics.append(token)

	cleanedLine = " ".join(currLineTokens)
	if len(currLineTokens) < 2:
		return
	tokensToTag = currLineTokens[1:]
	joinedLineToTag = " ".join(tokensToTag)

	textObjectToTag = Text(joinedLineToTag, hint_language_code=currLanguage)
	foundTags = textObjectToTag.pos_tags
	print cleanedLine
	print "%newmor:\t",
	for word, tag in foundTags:
		if tag != 'PUNCT':
			toWrite = tag + '|' + word + ' '
			print toWrite,
	print '\n'


def readUntaggedChaFiles(sourceDir):
	for dataFileName in glob.glob(sourceDir+"*.cha"):
	#	print (os.getcwd() + '/' + dataFileName)
		with open(dataFileName, 'r') as currFile:
			for currLine in currFile:
				if not currLine:
					continue
				if currLine[0] == '@':
					continue
				## so I'm reading in only speech lines
				if currLine[0] != '*':
					### For debugging
				#	if "%mor:" in currLine:
				#		print currLine,

					continue
				
				currLine = currLine.rstrip().lower()
				tagLine(currLine)


def iterateSubDir(directoryName):
	# call function to iterate over any ".cha" files in this directory
	readUntaggedChaFiles(directoryName)

	# going through each immediate subdirectory
	for subDir in next(os.walk(directoryName))[1]:
		subDirPath = directoryName + subDir + '/'
		os.chdir(subDirPath)
		readUntaggedChaFiles(subDirPath)


##
## Main method block
##
if __name__=="__main__":
	if (len(sys.argv) < 3):
		print('incorrect number of arguments')
		exit(0)

	currLanguage = sys.argv[1]
	directoryName = sys.argv[2]

	iterateSubDir(directoryName)