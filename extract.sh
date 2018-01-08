#!/bin/bash

# USAGE:
# - CalculiX (exo file):
#    ./extract.sh /opt/paraview530/bin sample_inputs/solve.exo sample_inputs/beadOnPlateKPI.json example_outputs example_outputs/metrics.csv 
# - CalculiX (exo file - vgroove with selected elements ): 
#    ./extract.sh /opt/paraview530/bin sample_inputs/vgroove-test/vgrv_s2.exo sample_inputs/vgroove-test/vgroove_test.json  example_outputs/vgroove/ example_outputs/vgroove/metrics.csv
#
# - openFOAM:
#    ./extract.sh /opt/paraview530/bin sample_inputs/elbow-test/system/controlDict sample_inputs/elbowKPI_test.json example_outputs/openFOAM/ example_outputs/openFOAM/metrics.csv  0

paraviewPath=$1
resultsFile=$2
desiredMetricsFile=$3
pvOutputDir=$4
outputMetrics=$5
caseNumber=$6

if [ $# -eq 7 ]
then
	isCellData=$7
else
	isCellData=""
fi

xvfb-run -a --server-args="-screen 0 1024x768x24" $paraviewPath/pvpython  --mesa-llvm   mexdex/extract.py  $resultsFile $desiredMetricsFile  $pvOutputDir $outputMetrics $caseNumber $isCellData


