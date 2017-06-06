import sys
import data_IO
import json

if len(sys.argv) < 3:
    print("Number of provided arguments: ", len(sys.argv) - 1)
    print("Usage: python testKPIreaderJSON.py   <desiredMetrics.json> <outputDir> ")
    sys.exit()

kpiFileAddress = sys.argv[1]
outputDir = sys.argv[2]


# Read the desired outputs/metrics from the csv file:
fp_csvin = data_IO.open_file(kpiFileAddress)
kpihash = json.load(fp_csvin)
fp_csvin.close()

print(kpihash)

import json
obj_json = kpihash
print(json.dumps(obj_json, indent=4))

fkjson = data_IO.open_file(outputDir +  "/kpi.json","w")
fkjson.write(json.dumps(obj_json, indent=4))
fkjson.close()

