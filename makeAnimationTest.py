import subprocess

outputDir = "outputs/png/0/"
kpi = "clipHFLX"

subprocess.call(["convert", "-delay", "15",  "-loop",  "0", outputDir + "/out_" + kpi + ".*.png",
                 outputDir + "/out_" + kpi + ".gif"])

