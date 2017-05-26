#!/bin/bash  

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias'
resultSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias/output'

cd $scriptSource

## python tagMultiData.py it ~/CHILDES-EVD/childes-earlyVocab-data/withMorTags/Tonelli_Italian/ > tempItalian.txt

# "AutoTag_EnglishMorisset" "AutoTag_EnglishTardif" "AutoTag_French" "AutoTag_German" "AutoTag_Hungarian" "AutoTag_Indonesian" "AutoTag_Italian" "AutoTag_Korean" "AutoTag_Spanish" "AutoTag_Swedish"

corpora=("Tardif_English" "Morisset_English" "Tonelli_Italian" "Lyon_French" "Leo_German" "TCCM_Mandarin" "Miyata_Japanese" "AutoTag_EnglishMorisset" "AutoTag_EnglishTardif" "AutoTag_French" "AutoTag_German" "AutoTag_Hungarian" "AutoTag_Indonesian" "AutoTag_Italian" "AutoTag_Korean" "AutoTag_Spanish" "AutoTag_Swedish")
#corpora=("Tardif_English" "SelfCleanedTardifEnglish")
#corpora=("Miyata_Japanese")

for currCorpus in "${corpora[@]}"; do
	resultStatFile=$resultSource'/outputStats_'$currCorpus'.txt'
	dataOutputFile=$resultSource'/outputExamples_'$currCorpus'.txt'
	currCorpus=$currCorpus'/'
	python extract-single-utterance.py $currCorpus $dataOutputFile > $resultStatFile
	#python extract-single-utterance.py $currCorpus $dataOutputFile
	echo 'Ran: '$currCorpus
done