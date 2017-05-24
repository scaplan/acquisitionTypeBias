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


def readUntaggedChaFiles(sourceDir):
	for dataFileName in glob.glob(sourceDir+"*.cha"):
	#	print (os.getcwd() + '/' + dataFileName)
		with open(dataFileName, 'r') as currFile:
			with open(outputFilename, 'a') as outputFile:
				speechGroup = []
				for currLine in currFile:
					if not currLine:
						continue
					if currLine[0] == '@':
						continue
					if currLine[0] != '*':
						continue
					## so I'm reading in only speech lines
					currLine = currLine.rstrip().lower()
					currLineTokens = currLine.split()
					currLineTokensNoPunc = [x for x in currLineTokens if x not in punctuationSet]

					onlyAlphaNumerics = []
					for token in currLineTokensNoPunc:
						valid = re.search('[a-z]', token) is not None
						if valid:
							onlyAlphaNumerics.append(token)


					cleanedLine = " ".join(onlyAlphaNumerics)
					if len(onlyAlphaNumerics) < 2:
						continue
					tokensToTag = onlyAlphaNumerics[1:]
					joinedLineToTag = " ".join(tokensToTag)

					textObjectToTag = Text(joinedLineToTag, hint_language_code=currLanguage)
					foundTags = textObjectToTag.pos_tags
					outputFile.write(cleanedLine + '\n')
					outputFile.write("%newmor:\t")
					for word, tag in foundTags:
						if tag != 'PUNCT':
							toWrite = tag + '|' + word + ' '
							outputFile.write(toWrite)
					outputFile.write('\n\n')
					#print foundTags
			outputFile.close()




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
	if (len(sys.argv) < 4):
		print('incorrect number of arguments')
		exit(0)

	currLanguage = sys.argv[1]
	directoryName = sys.argv[2]
	outputFilename = sys.argv[3]
	os.remove(outputFilename) if os.path.exists(outputFilename) else None

	iterateSubDir(directoryName)