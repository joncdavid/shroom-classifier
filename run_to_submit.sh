#!/usr/bin/env bash

echo "Begin..."
validationfile="./data/validation.dat"
vpath="./results/validation/"
echo "Running experiments to produce predictions on" $validationfile
python3 ./run_experiments.py $validationfile $vpath > $vpath/report.txt
## removethe report.txt file because obviously it has 0% accuracy,
##  and that's because the validation set doesn't provide p/n values.
rm $vpath/report.txt
echo "  The following files are the model predictions for various CI"
echo "  and attribution-selection criteria."
echo ""
echo "  Predictions found in these files:"
echo "  " $vpath/prediction.gain.0%
echo "  " $vpath/prediction.gain.50%
echo "  " $vpath/prediction.gain.95%
echo "  " $vpath/prediction.gain.99%
echo "  " $vpath/prediction.misclassification.0%
echo "  " $vpath/prediction.misclassification.50%
echo "  " $vpath/prediction.misclassification.95%
echo "  " $vpath/prediction.misclassification.99%
echo ""


testingfile="./data/testing.dat"
tpath="./results/test/"
echo "Running experiments to evaluate performance on" $testingfile
python3 ./run_experiments.py $testingfile $tpath > $tpath/report.txt
## remove these files to prevent accidentally picking them up for validation.
rm $tpath/prediction.gain.0%
rm $tpath/prediction.gain.50%
rm $tpath/prediction.gain.95%
rm $tpath/prediction.gain.99%
rm $tpath/prediction.misclassification.0%
rm $tpath/prediction.misclassification.50%
rm $tpath/prediction.misclassification.95%
rm $tpath/prediction.misclassification.99%
echo "  Model performance on test set can is here:" $tpath/report.txt

echo "Complete."
echo ""
