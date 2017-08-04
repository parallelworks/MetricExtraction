from paraview.simple import *
import json
import sys
import pvutils
import data_IO
import os

print(sys.argv)
if len(sys.argv) < 5:
    print("Number of provided arguments: ", len(sys.argv) - 1)
    print("Usage: pvpython extract.py  <dataFile>  <desiredMetrics.json> <outputDir> <outputMetrics.csv>")
    sys.exit()


dataFileAddress = sys.argv[1]
kpiFileAddress = sys.argv[2]
outputDir = sys.argv[3]
metricFile = sys.argv[4]


# Image settings:
individualImages = True
magnification = 2
viewSize = [700, 600]
backgroundColor = [1, 1, 1]   # set background color to white

# Read the desired outputs/metrics from the csv file:
fp_jsonIn = data_IO.open_file(kpiFileAddress)
kpihash = json.load(fp_jsonIn)
kpihash = pvutils.byteify(kpihash)
fp_jsonIn.close()
print(kpihash)

# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Read data file
data2Read = pvutils.getfieldsfromkpihash(kpihash)
dataReader = pvutils.readDataFile(dataFileAddress, data2Read)

# Initialize renderView and display
renderView1, readerDisplay = pvutils.initRenderView(dataReader, viewSize,
                                                    backgroundColor)

print("Generating KPIs")

# Set component to "Magnitude" if not given for vector/tensor fields
for kpi in kpihash:
    kpihash[kpi] = pvutils.correctfieldcomponent(dataReader, kpihash[kpi])

fp_csv_metrics = data_IO.open_file(metricFile, "w")
fp_csv_metrics.write(",".join(['metric','ave','min','max','sd'])+"\n")

renderView1.InteractionMode = '2D'
renderView1.OrientationAxesVisibility = 0

# Save the default STL file
# pvutils.saveSTLfile(renderView1,outputDir + "/out_stl.png",magnification,100)

for kpi in kpihash:
    
    metrichash = kpihash[kpi]
    kpitype = metrichash['type']
    
    if 'field' in metrichash:
        kpifield = metrichash['field']
    else:
        kpifield = "None"
        
    if 'fieldComponent' in metrichash:
        kpiComp = metrichash['fieldComponent']
    else:
        kpiComp = "None"

    if 'image' in metrichash:
        kpiimage = metrichash['image']
    else:
        kpiimage = "None"
        
    if 'imageflip' in metrichash:
        kpiimageflip = metrichash['imageflip']
    else:
        kpiimageflip = "None"

    if individualImages:
        HideAll()
        Show(dataReader, renderView1)
        if kpiimage != "None" and kpiimage != "" and kpiimage != "plot":
            pvutils.adjustCamera(kpiimage, renderView1, metrichash, kpiimageflip)
    
    print(kpi)
    
    if 'extractStats' in metrichash:
        extractStats = data_IO.str2bool(metrichash['extractStats'])
    else:
        extractStats = True

    ave=[]
    if kpitype=="Slice":
        d = pvutils.createSlice(metrichash, dataReader, readerDisplay, individualImages)
    elif kpitype== "Clip":
        d = pvutils.createClip(metrichash, dataReader, readerDisplay, individualImages)
    elif kpitype== "Probe":
        d = pvutils.createProbe(metrichash, dataReader)
    elif kpitype== "Line":
        d,ave = pvutils.createLine(metrichash, kpi, dataReader, outputDir)
    elif kpitype== "StreamLines":
        d = pvutils.createStreamTracer(metrichash, dataReader, readerDisplay, individualImages)
    elif kpitype== "Volume":
        d = pvutils.createVolume(metrichash, dataReader)
    elif kpitype== "Basic":
        d = pvutils.createBasic(metrichash, dataReader, readerDisplay, individualImages)
        if kpifield == "None":
            extractStats = False

    if extractStats:
        #pvutils.extractStatsOld(d, kpi, kpifield, kpiComp, kpitype, fp_csv_metrics, ave)
        pvutils.extractStats(d, kpi, kpifield, kpiComp, kpitype, fp_csv_metrics)

    if individualImages:
        if kpiimage != "None" and kpiimage != "" and kpiimage != "plot":
            if not (os.path.exists(outputDir)):
                os.makedirs(outputDir)
            SaveScreenshot(outputDir + "/out_" + kpi + ".png", magnification=magnification, quality=100)

    if 'animation' in metrichash:
        makeAnim = data_IO.str2bool(metrichash['animation'])
    else:
        makeAnim = False
    if makeAnim:
        pvutils.makeAnimation(outputDir, kpi, magnification)

    if 'blender' in metrichash:
        export2Blender = data_IO.str2bool(metrichash['blender'])
    else:
        export2Blender = False
    if export2Blender:
        try:
            blenderContext=metrichash['blendercontext'].split(",")
        except:
            blenderContext=[]
        try:
            renderBody=metrichash['blenderbody'].split(",")
        except:
            renderBody=False
        pvutils.exportx3d(outputDir, kpi, d, dataReader, renderBody, blenderContext)

fp_csv_metrics.close()
