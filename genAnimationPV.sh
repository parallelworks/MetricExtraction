#!/bin/bash 
paraviewPath=$1
paraviewPythonScript=$2
resultsExoFile=$3
pngDir=$4
animFile=$5
pngName=temp.png

export PATH=$PATH:$paraviewPath

xvfb-run -a --server-args="-screen 0 1024x768x24" pvpython  $paraviewPythonScript  $resultsExoFile $pngDir $pngName

convert -delay 15 -loop 0  $pngDir/*.png $animFile
