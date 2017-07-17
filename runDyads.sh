#!/bin/bash  

# Author: Spencer Caplan
# Department of Linguistics, University of Pennsylvania
# Contact: spcaplan@sas.upenn.edu

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias'
resultSource='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias/output/July'
globalFrequencyFile='/home1/s/spcaplan/Dropbox/penn_CS_account/acquisitionTypeBias/Charles-Childes-Frequency-Table.txt'

cd $scriptSource

#corpora=("Providence/Ethan/" "Tardif_English/" "TCCM_Mandarin/chou/" "Tonelli_Italian/Marco/" "Miyata_Japanese/Tai/")
corpora=("Providence/Ethan/")
#corpora=("Brent/s1/")
#corpora=("LeeWongLeung_Cantonese/")
#corpora_handles=("ENG-Ethan" "ENG-TardifPool" "ZH-Chou" "IT-Marco" "JP-Tai")
corpora_handles=("Ethan")
#corpora_handles=("Brent-s1")
#corpora_handles=("YUE-total")
outputSuffix='_DyadCountsAndProbs_noGlobal.csv'

for ((i=0;i<${#corpora[@]};++i)); do
	currCorpus="${corpora[i]}"
	currHandle="${corpora_handles[i]}"
	resultStatFile=$resultSource'/'$currHandle$outputSuffix
	regressionOutput=$resultSource'/'$currHandle'_regression.txt'

	echo 'Running: '$currCorpus

	
	if [ -f $resultStatFile ] ; then
	    rm $resultStatFile
	fi

	#python dyadExtraction.py $currCorpus $resultStatFile $globalFrequencyFile
	if [ "$currHandle" = "YUE-total" ]; then
		#python dyadExtraction.py $currCorpus $resultStatFile 'chinese'
		python dyadExtraction.py $currCorpus $resultStatFile -ch 'true'
		#python dyadExtraction.py $currCorpus $resultStatFile $scriptSource'/BrentCDI/S1-18monthCDI' 'CDI'
		python dyadExtraction.py $currCorpus $resultStatFile -cdi $scriptSource'/BrentCDI/S1-18monthCDI'
	else
		python dyadExtraction.py $currCorpus $resultStatFile
	fi

	# python BBash.py -c celexsampalemma $datadir/epl.csv $outputdir/output_$LANGUAGE_MODEL"_CELEXSAMPALEMMA_mix"$TOKEN_WEIGHTING"_noun.csv" $ENGLISH_TYPE_CNT_NOUN $ENGLISH_SENSE_CNT_NOUN $LANGUAGE_MODEL -s rando --mixture $TOKEN_WEIGHTING &


	#Rscript evd-regression.R $resultStatFile > $regressionOutput
done

echo 'Completed'