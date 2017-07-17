#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

typicalVowelDict = {"a":1,
					"e":1,
					"i":1,
					"o":1,
					"u":1,
					"å":1,
					"ä":1,
					"ë":1,
					"ö":1,
					"æ":1,
					"ø":1,
					"ı":1,
					"ü":1,
					"á":1,
					"é":1,
					"ẹ":1,
					"í":1,
					"ó":1,
					"ọ":1,
					"ú":1,
					"à":1,
					"è":1,
					"ẹ":1,
					"ì":1,
					"ò":1,
					"ọ":1,
					"ù":1,
					"ő":1,
					"ű":1,
					}

def countVowelClusters(inputWord):
	global typicalVowelDict
	numClusters = 0
	inCluster = False
	for currChar in inputWord:
		if currChar in typicalVowelDict:
			if inCluster:
				inCluster = True
			else:
				inCluster = True
				numClusters += 1
		else:
			inCluster = False
	return numClusters