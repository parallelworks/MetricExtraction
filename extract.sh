#!/bin/bash 
paraviewPath=$1
pvpythonExtractScript=$2
resultsExoFile=$3
desiredMetricsFile=$4
pvOutputDir=$5
outputMetrics=$6
pythonPlotScript=$7

export PATH=$PATH:$paraviewPath

xvfb-run -a --server-args="-screen 0 1024x768x24" pvpython  $pvpythonExtractScript  $resultsExoFile $desiredMetricsFile  $pvOutputDir $outputMetrics

#convert -delay 15 -loop 0  $pngDir/*.png $animFile

shopt -s nullglob # sets wildcard response to null
for f in ${pvOutputDir}plot_*.csv;do
	echo $f
    python $pythonPlotScript $f
done