import sys
import os
import pvutils
import data_IO

if len(sys.argv) < 5:
    print("Number of provided arguments: ", len(sys.argv) - 1)
    print("Usage: pvpython extractBox.py  <solve.exo>  <desiredMetrics.csv> <outputDir> <outputMetrics.csv>")
    sys.exit()


# solveexoFileAddress = \
#     '/home/marmar/Dropbox/parallelWorks/weldingProject/paraviewPostProcess/outputs/case0/solve.exo'
# kpiFileAddress = 'boxKPI.csv'
# metricFileName = "metrics.csv"

solveexoFileAddress = sys.argv[1]
kpiFileAddress = sys.argv[2]
outputDir = sys.argv[3]
metricFileName = sys.argv[4]
individualImages = True
magnification = 2

# Read the desired outputs/metrics from the csv file:
fp_csvin = data_IO.open_file(kpiFileAddress)
kpihash = pvutils.read_csv(fp_csvin)
fp_csvin.close()

print(kpihash)