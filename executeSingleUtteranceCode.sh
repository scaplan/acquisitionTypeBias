#!/bin/bash  

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias'
resultSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias/output'

cd $scriptSource

## python tagMultiData.py it ~/CHILDES-EVD/childes-earlyVocab-data/withMorTags/Tonelli_Italian/ > tempItalian.txt

corpora=("Tardif_English" "Morisset_English" "Tonelli_Italian" "Lyon_French" "TCCM_Mandarin" "SelfCleanedTardifEnglish" "SelfCleaned_Italian" "SelfCleaned_German" "SelfCleaned_Hungarian" "SelfCleaned_Indonesian" "SelfCleaned_Spanish" "SelfCleaned_Swedish")
#corpora=("Tardif_English" "SelfCleanedTardifEnglish")

for currCorpus in "${corpora[@]}"; do
	resultFile=$resultSource'/output_'$currCorpus'.txt'
	currCorpus=$currCorpus'/'
	python extract-single-utterance.py $currCorpus > $resultFile
	#python extract-single-utterance.py $currCorpus

done