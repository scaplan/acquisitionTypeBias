#!/bin/bash  

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias'
resultSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias/output'

cd $scriptSource

## python tagMultiData.py it ~/CHILDES-EVD/childes-earlyVocab-data/withMorTags/Tonelli_Italian/ tempItalian.txt

corpora=("Tardif_English" "Morisset_English" "Tonelli_Italian" "TCCM_Mandarin" "SelfCleanedTardifEnglish")
#corpora=("SelfCleanedTardifEnglish")

for currCorpus in "${corpora[@]}"; do
	resultFile=$resultSource'/output_'$currCorpus'.txt'
	currCorpus=$currCorpus'/'
	python extract-single-utterance.py $currCorpus > $resultFile
	#python extract-single-utterance.py $currCorpus

done