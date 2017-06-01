#!/bin/bash  

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias'
resultSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias/output'

cd $scriptSource

## python tagMultiData.py it ~/CHILDES-EVD/childes-earlyVocab-data/withMorTags/Tonelli_Italian/ > tempItalian.txt

# "AutoTag_EnglishMorisset" "AutoTag_EnglishTardif" "AutoTag_French" "AutoTag_German" "AutoTag_Hungarian" "AutoTag_Indonesian" "AutoTag_Italian" "AutoTag_Korean" "AutoTag_Spanish" "AutoTag_Swedish"

#corpora=("Tardif_English" "Morisset_English" "Tonelli_Italian" "Lyon_French" "Leo_German" "TCCM_Mandarin" "Miyata_Japanese" "AutoTag_EnglishMorisset" "AutoTag_EnglishTardif" "AutoTag_French" "AutoTag_German" "AutoTag_Hungarian" "AutoTag_Indonesian" "AutoTag_Italian" "AutoTag_Korean" "AutoTag_Spanish" "AutoTag_Swedish")
#corpora=("Tardif_English" "Tonelli_Italian" "Lyon_French" "Leo_German" "TCCM_Mandarin" "Miyata_Japanese")
#corpora=("Tardif_English")
corpora=("Providence/Ethan")

#statsOutputName=$resultSource'/output_plotStats_autoAll.csv'
statsOutputName=$resultSource'/output_plotStats.csv'
if [ -f $statsOutputName ] ; then
    rm $statsOutputName
fi

for currCorpus in "${corpora[@]}"; do
	resultStatFile=$resultSource'/outputStats_'$currCorpus'.txt'
	dataOutputFileTemplate=$resultSource'/outputExamples_'$currCorpus
	currCorpus=$currCorpus'/'
	python extract-single-utterance.py $currCorpus $dataOutputFileTemplate $statsOutputName > $resultStatFile
	#python extract-single-utterance.py $currCorpus $dataOutputFileTemplate
	echo 'Ran: '$currCorpus
done

## Plotting
#plotOutputName=$resultSource'/output_plot_autoAll.png'
plotOutputName=$resultSource'/output_plot.png'
echo 'Running Plot'
#Rscript plotInputOutputCorrespondence.R $statsOutputName $plotOutputName