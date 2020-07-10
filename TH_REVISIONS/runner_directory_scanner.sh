#!/bin/bash

clear

RUNNING=$(qstat -u aglucaci | wc -l)
now=$(date)

echo $now
echo "Current number of jobs: "$RUNNING


QUEUED=$(qstat | grep 'Q' | wc -l)

echo "Currently Queued: "$QUEUED

ABSREL=$(ls /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/analysis/UNMASKED_SELECTOME/*ABSREL.json | wc -l)

echo "Current number of ABSREL results (json): "$ABSREL

ABSRELMH=$(ls /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/analysis/UNMASKED_SELECTOME/*ABSREL-MH.json | wc -l)

echo "Current number of ABSREL-MH results (json): "$ABSRELMH

BUSTEDS=$(ls /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/analysis/UNMASKED_SELECTOME/*BUSTEDS.json | wc -l)

echo "Current number of BUSTEDSMH results (json): "$BUSTEDS

if [ $RUNNING -lt 200 ]; then
   echo "Less than 200 jobs running"
else
   echo "More than 200 jobs running"
   echo "Exiting"
   exit 1
fi


if [ $QUEUED -lt 100 ]; then
   echo "No jobs are currently queued"
else
   echo "Jobs are currently queued"
   echo "Exiting"
   exit 1
fi


echo "Submitting jobs"

echo python directoryscanner_TH_REVISIONS_ExtendedAnalysis_CheckForErrors.py -a /home/aglucaci/TRIPLE_HITS/data/selectome_trip_ammended -o /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/analysis/UNMASKED_SELECTOME

python directoryscanner_TH_REVISIONS_ExtendedAnalysis_CheckForErrors.py -a /home/aglucaci/TRIPLE_HITS/data/selectome_trip_ammended -o /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/analysis/UNMASKED_SELECTOME


echo "Sleeping 1m"
sleep 1m





exit 0


# End of file
