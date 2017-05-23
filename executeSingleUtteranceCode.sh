#!/bin/bash  

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias'
resultSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias/output'

cd $scriptSource

corpora=("MorissetEnglish" "TonelliItalian" "TCCM")

for currCorpus in "${corpora[@]}"; do

	resultFile=$resultSource'/output_'$currCorpus'.txt'
	python extract-single-utterance.py $currCorpus > $resultFile

done