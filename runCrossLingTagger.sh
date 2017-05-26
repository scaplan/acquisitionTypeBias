#!/bin/bash  

dataDir='/home/scaplan/childes-earlyVocab-data/'
outputDir='/home/scaplan/Dropbox/penn_CS_account/acquisitionTypeBias/'

###
currCorpus='Tardif_English'
python tagMultiData.py 'en' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='Morisset_English'
python tagMultiData.py 'en' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='Tonelli_Italian'
python tagMultiData.py 'it' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='Lyon_French'
python tagMultiData.py 'fr' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='Leo_German'
python tagMultiData.py 'de' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='MacWhinney_Hungarian'
python tagMultiData.py 'hu' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='Jakarta_Indonesian'
python tagMultiData.py 'id' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='JacksonThal_Spanish'
python tagMultiData.py 'es' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='Lacerda_Swedish'
python tagMultiData.py 'sv' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

currCorpus='Ryu_Korean'
python tagMultiData.py 'kr' $dataDir$currCorpus'/' > $outputDir$currCorpus'_Cleaned.cha'
echo $currCorpus

echo 'Done tagging!'