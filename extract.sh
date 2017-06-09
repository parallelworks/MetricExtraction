#!/bin/bash

# USAGE:
# - CalculiX (exo file):
#    ./extract.sh /opt/paraview530/bin utils/extract.py sample_inputs/solve.exo sample_inputs/beadOnPlateKPI.json example_outputs example_outputs/metrics.csv utils/plot.py
# - openFOAM:
#    ./extract.sh /opt/paraview530/bin utils/extract.py sample_inputs/elbow-test/system/controlDict sample_inputs/elbowKPI.json example_outputs/openFOAM/ example_outputs/openFOAM/metrics.csv utils/plot.py 

paraviewPath=$1
pvpythonExtractScript=$2
resultsFile=$3
desiredMetricsFile=$4
pvOutputDir=$5
outputMetrics=$6
pythonPlotScript=$7

export PATH=$PATH:$paraviewPath

xvfb-run -a --server-args="-screen 0 1024x768x24" pvpython  $pvpythonExtractScript  $resultsFile $desiredMetricsFile  $pvOutputDir $outputMetrics

#convert -delay 15 -loop 0  $pngDir/*.png $animFile

shopt -s nullglob # sets wildcard response to null
for f in ${pvOutputDir}plot_*.csv;do
	echo $f
    python $pythonPlotScript $f
done

