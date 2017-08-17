import sys
import data_IO
import json
import pvutils

if len(sys.argv) < 4:
    print("Number of provided arguments: ", len(sys.argv) - 1)
    print("Usage: pvpython convertcsv2json.py <desiredMetrics.csv> <desiredMetrics.json> <outputDir/>")
    sys.exit()

csvkpiAddress = sys.argv[1]
jsonFileName = sys.argv[2]
outputDir = sys.argv[3]

# Read the desired outputs/metrics from the csv file:
fp_csvin = data_IO.open_file(csvkpiAddress)
kpihash = pvutils.read_csv(fp_csvin)
fp_csvin.close()

obj_json = kpihash
#print(json.dumps(obj_json, indent=4))

fkjson = data_IO.open_file(outputDir + "/" +  jsonFileName, "w")
fkjson.write(json.dumps(obj_json, indent=4))
fkjson.close()

