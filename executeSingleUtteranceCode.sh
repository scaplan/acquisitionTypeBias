#!/bin/bash  

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias'
resultSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias/output'

cd $scriptSource

## python tagMultiData.py it ~/CHILDES-EVD/childes-earlyVocab-data/withMorTags/Tonelli_Italian/ > tempItalian.txt

corpora=("Tardif_English" "Morisset_English" "Tonelli_Italian" "Lyon_French" "TCCM_Mandarin" "SelfCleanedTardifEnglish" "SelfCleaned_Italian" "SelfCleaned_German" "SelfCleaned_Hungarian" "SelfCleaned_Indonesian" "SelfCleaned_Spanish" "SelfCleaned_Swedish" "SelfCleaned_Korean")
#corpora=("Tardif_English" "SelfCleanedTardifEnglish")
#corpora=("SelfCleaned_Korean")

for currCorpus in "${corpora[@]}"; do
	resultStatFile=$resultSource'/outputStats_'$currCorpus'.txt'
	dataOutputFile=$resultSource'/outputExamples_'$currCorpus'.txt'
	currCorpus=$currCorpus'/'
	python extract-single-utterance.py $currCorpus $dataOutputFile > $resultStatFile
	#python extract-single-utterance.py $currCorpus $dataOutputFile

done