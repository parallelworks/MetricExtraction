from paraview.simple import *
import sys
import data_IO
import os
import subprocess
import shutil


# For saving plots as pngs
import matplotlib

import numpy as np
import warnings

def byteify(input):
    """
    Got this function from https://stackoverflow.com/questions/2357230/what-is-the-proper-way-to-comment-functions-in-python
    "This short and simple recursive function will convert any decoded JSON object from using unicode strings to 
    UTF-8-encoded byte strings"
    This is not the most efficient solution. See the code provided by Mirec Miskuf to see how to use an object_hook to 
    do this more efficiently.
    """
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def getParaviewVersion():
    """ Return paraview version as a double number: e.g. 5.4"""
    PVversionMajor = paraview.servermanager.vtkSMProxyManager.GetVersionMajor() 
    PVversionMinor = paraview.servermanager.vtkSMProxyManager.GetVersionMinor()
    PVversion = PVversionMajor + PVversionMinor/100.0
    return PVversion


def planeNormalFromName(planeName):
    if planeName == "X" or planeName == "x":
        normal = [1.0, 0.0, 0.0]
    if planeName == "Y" or planeName == "y":
        normal = [0.0, 1.0, 0.0]
    if planeName == "Z" or planeName == "z":
        normal = [0.0, 0.0, 1.0]
    return normal


def setviewposition(position_key, camera):
    center = position_key.split()
    nPoints = len(center)/3
    positionXYZ = []
    for iPoint in range(nPoints):
        positionXYZ.extend(list(camera.GetFocalPoint()))
        for i in range(iPoint*3, 3+iPoint*3):
            if center[i] != "center":
                positionXYZ[i] = float(center[i])
    return positionXYZ


def read_csv(f):
    kpihash = {}
    cols = [l.replace("\n", "") for l in f.readline().split(",")]
    for i, line in enumerate(f):
        data = [l.replace("\n", "") for l in line.split(",")]
        kpihash[data[0]] = {}
        for ii, v in enumerate(data):
            if ii != 0:
                kpihash[data[0]][cols[ii]] = v
    return kpihash


def getfieldsfromkpihash(kpihash):
    cellsarrays = []
    for kpi in kpihash:
        cellsarrays.append(kpihash[kpi]['field'])

    ca = set(cellsarrays)

    cellsarrays = list(ca)
    return cellsarrays


def isfldScalar(arrayInfo):
    numComps = arrayInfo.GetNumberOfComponents()
    if numComps == 1:
        return True
    else:
        return False


def getfldComponentMap(arrayInfo):
    compName2num = {}
    numComps = arrayInfo.GetNumberOfComponents()
    if numComps>1:
        for iComp in range(-1,numComps):
            compName2num[arrayInfo.GetComponentName(iComp)] = iComp
    return compName2num


def getfldCompNumber(arrayInfo, kpiComp):
    compNumberMap = getfldComponentMap(arrayInfo)
    if not kpiComp:
        compNum = 0
    else:
        compNum = compNumberMap[kpiComp]
    return compNum


def getdatarange(datasource, kpifld, kpifldcomp):
    arrayInfo = datasource.PointData[kpifld]
    compNumber = getfldCompNumber(arrayInfo, kpifldcomp)
    datarange = arrayInfo.GetRange(compNumber)
    return datarange


def correctfieldcomponent(datasource, metrichash):
    """
    Set "fieldComponent" to "Magnitude" if the component of vector/tensor fields is not given. For scalar fields set 
    "fieldComponent" to an empty string.
    """
    kpifld = metrichash['field']
    arrayInfo = datasource.PointData[kpifld]
    if isfldScalar(arrayInfo):
        metrichash['fieldComponent'] = ''
    else:
        if not 'fieldComponent' in metrichash:
            metrichash['fieldComponent'] = 'Magnitude'
    return metrichash


def getReaderTypeFromfileAddress(dataFileAddress):
    if dataFileAddress.endswith('.exo'):
        readerType = 'exo'
    elif dataFileAddress.endswith('system/controlDict'):
        readerType = 'openFOAM'
    else:
        print('Error: Reader type cannot be set. Please check data file address')
        sys.exit(1)

    return readerType


def readDataFile(dataFileAddress, dataarray):
    readerType = getReaderTypeFromfileAddress(dataFileAddress)
    if readerType == 'exo':
        # Read the results file : create a new 'ExodusIIReader'
        dataReader = ExodusIIReader(FileName=dataFileAddress)

        dataReader.ElementBlocks = ['PNT', 'C3D20 C3D20R', 'COMPOSITE LAYER C3D20', 'Beam B32 B32R',
                                    'CPS8 CPE8 CAX8 S8 S8R', 'C3D8 C3D8R', 'TRUSS2', 'TRUSS2',
                                    'CPS4R CPE4R S4 S4R', 'CPS4I CPE4I', 'C3D10', 'C3D4', 'C3D15',
                                    'CPS6 CPE6 S6', 'C3D6', 'CPS3 CPE3 S3',
                                    '2-node 1d network entry elem', '2-node 1d network exit elem',
                                    '2-node 1d genuine network elem']

        # only load the data that is needed
        dataReader.PointVariables = dataarray
    elif readerType == 'openFOAM':
        # create a new 'OpenFOAMReader'
        dataReader = OpenFOAMReader(FileName=dataFileAddress)

        dataReader.MeshRegions = ['internalMesh']

        dataReader.CellArrays = dataarray

    return dataReader


def getTimeSteps():
    # get animation scene
    animationScene1 = GetAnimationScene()

    # update animation scene based on data timesteps
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    timeSteps = list(animationScene1.TimeKeeper.TimestepValues)

    return timeSteps


def setFrame2latestTime(renderView1):

    TimeSteps = getTimeSteps()

    latesttime = TimeSteps[-1]
    print("Setting view to latest Time: " + str(latesttime))

    renderView1.ViewTime = latesttime
    return renderView1


def initRenderView (dataReader, viewSize, backgroundColor):
    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    renderView1 = setFrame2latestTime(renderView1)

    # set the view size
    renderView1.ViewSize = viewSize
    renderView1.Background = backgroundColor

    # show data in view
    readerDisplay = Show(dataReader, renderView1)

    # reset view to fit data
    renderView1.ResetCamera()

    return renderView1, readerDisplay



def colorMetric(d, metrichash):
    display = GetDisplayProperties(d)

    kpifld = metrichash['field']
    kpifldcomp = metrichash['fieldComponent']

    ColorBy(display, ('POINTS', kpifld, kpifldcomp))
    Render()
    UpdateScalarBars()
    ctf = GetColorTransferFunction(kpifld)
    ctf.ApplyPreset(metrichash["colorscale"], True)
    if metrichash["invertcolor"] == "1":
        ctf.InvertTransferFunction()
    datarange = getdatarange(d, kpifld, kpifldcomp)

    min = datarange[0]
    max = datarange[1]
    if metrichash["min"] != "auto" and metrichash["min"] != "":
         min = float(metrichash["min"])
    if metrichash["max"] != "auto" and metrichash["max"] != "":
         max = float(metrichash["max"])
    ctf.RescaleTransferFunction(min, max)
    if int(metrichash["discretecolors"]) > 0:
        ctf.Discretize = 1
        ctf.NumberOfTableValues = int(metrichash["discretecolors"])
    else:
        ctf.Discretize = 0
    GetScalarBar(ctf).TitleColor = [0,0,0]
    GetScalarBar(ctf).LabelColor = [0,0,0]
    GetScalarBar(ctf).Orientation = "Horizontal"
    
    imgtype=metrichash['image'].split("_")[0]
    PVversion = getParaviewVersion()
    if (imgtype!="iso"):
        # center
        if PVversion < 5.04:
            GetScalarBar(ctf).Position = [0.25,0.05]
            GetScalarBar(ctf).Position2 = [0.5,0] # no such property in PV 5.04
        else:
            GetScalarBar(ctf).WindowLocation = 'LowerCenter'
    else:
        # left
        if PVversion < 5.04:
            GetScalarBar(ctf).Position = [0.05,0.025]
            GetScalarBar(ctf).Position2 = [0.4,0] # no such property in PV 5.04
        else:
            GetScalarBar(ctf).WindowLocation = 'LowerLeftCorner'

    #if individualImages == False:
    #    display.SetScalarBarVisibility(renderView1, False)


def createSlice(metrichash, dataReader, dataDisplay, isIndivImgs):
    camera = GetActiveCamera()
    renderView1 = GetActiveViewOrCreate('RenderView')

    opacity=float(metrichash['opacity'])
    bodyopacity=float(metrichash['bodyopacity'])
    if isIndivImgs:
        dataDisplay.Opacity = bodyopacity
        dataDisplay.ColorArrayName = ['POINTS', '']
    slicetype = "Plane"
    plane = metrichash['plane']

    s = Slice(Input=dataReader)
    s.SliceType = slicetype
    s.SliceType.Origin = setviewposition(metrichash['position'], camera)
    s.SliceType.Normal = planeNormalFromName(plane)
    sDisplay = Show(s, renderView1)
    sDisplay.ColorArrayName = [None, '']
    sDisplay.SetRepresentationType('Surface')
    sDisplay.DiffuseColor = [0.0, 1.0, 0.0]
    sDisplay.Specular = 0
    sDisplay.Opacity = opacity
    colorMetric(s, metrichash)
    return s


def createStreamTracer(metrichash, data_reader, data_display, isIndivImages):
    camera = GetActiveCamera()
    renderView1 = GetActiveViewOrCreate('RenderView')

    opacity = float(metrichash['opacity'])
    bodyopacity = float(metrichash['bodyopacity'])
    if isIndivImages == True:
        data_display.Opacity = bodyopacity
        data_display.ColorArrayName = ['POINTS', '']

    streamTracer = StreamTracer(Input=data_reader,
                                 SeedType='High Resolution Line Source')

    kpifld = metrichash['field'] #!!!!!!!
    streamTracer.Vectors = ['POINTS', kpifld]
    LinePoints = setviewposition(metrichash['position'], camera)
    streamTracer.SeedType.Point1 = LinePoints[0:3]
    streamTracer.SeedType.Point2 = LinePoints[3:6]
    streamTracer.SeedType.Resolution = int(metrichash['resolution'])
    streamTracer.IntegrationDirection = metrichash['integralDirection'] # 'BACKWARD', 'FORWARD' or  'BOTH'

    # To do : Add a default value based on domain size ?
    streamTracer.MaximumStreamlineLength = float(metrichash['maxStreamLength'])


    ##
    # create a new 'Tube'
    tube = Tube(Input=streamTracer)
    tube.Radius = float(metrichash['tubeRadius'])
    # show data in view
    tubeDisplay = Show(tube, renderView1)
    # trace defaults for the display properties.
    tubeDisplay.Representation = 'Surface'
    tubeDisplay.ColorArrayName = [None, '']
    tubeDisplay.EdgeColor = [0.0, 0.0, 0.0]
    tubeDisplay.DiffuseColor = [0.0, 1.0, 0.0]
    tubeDisplay.Specular = 0
    tubeDisplay.Opacity = opacity

    metrichash['field'] = metrichash['colorByField']
    if 'colorByFieldComponent' in metrichash:
        metrichash['fieldComponent'] = metrichash['colorByFieldComponent']
    metrichash = correctfieldcomponent(streamTracer, metrichash)
    colorMetric(tube, metrichash)
    try:
        if metrichash['image'].split("_")[1] == "solo":
            Hide(data_reader, renderView1)
    except:
        pass
    return tube


def createClip(metrichash, data_reader, data_display, isIndivImages):
    camera = GetActiveCamera()
    renderView1 = GetActiveViewOrCreate('RenderView')

    opacity = float(metrichash['opacity'])
    bodyopacity = float(metrichash['bodyopacity'])
    if isIndivImages == True:
        data_display.Opacity = bodyopacity
        data_display.ColorArrayName = ['POINTS', '']
    cliptype = "Plane"
    plane = metrichash['plane']
    if 'invert' in metrichash.keys():
        invert = data_IO.str2bool(metrichash['invert'])
    else:
        invert = 0


    s = Clip(Input=data_reader)
    s.ClipType = cliptype
    s.ClipType.Origin = camera.GetFocalPoint()
    s.InsideOut = invert
    s.ClipType.Origin = setviewposition(metrichash['position'],camera)
    s.ClipType.Normal = planeNormalFromName(plane)
    sDisplay = Show(s, renderView1)
    sDisplay.ColorArrayName = [None, '']
    sDisplay.SetRepresentationType('Surface')
    sDisplay.DiffuseColor = [0.0, 1.0, 0.0]
    sDisplay.Specular = 0
    sDisplay.Opacity = opacity
    colorMetric(s, metrichash)
    try:
        if metrichash['image'].split("_")[1] == "solo":
            Hide(data_reader, renderView1)
    except:
        pass
    return s


def createProbe(metrichash, data_reader):
    camera = GetActiveCamera()
    renderView1 = GetActiveViewOrCreate('RenderView')

    p = ProbeLocation(Input=data_reader, ProbeType='Fixed Radius Point Source')
    p.PassFieldArrays = 1
    #p.ProbeType.Center = [1.2176899909973145, 1.2191989705897868, 1.5207239668816328]
    p.ProbeType.Center = setviewposition(metrichash['position'], camera)
    p.ProbeType.NumberOfPoints = 1
    p.ProbeType.Radius = 0.0
    ps = Sphere(Radius=0.025, ThetaResolution=32)
    ps.Center = setviewposition(metrichash['position'], camera)
    psDisplay = Show(ps, renderView1)
    psDisplay.DiffuseColor = [1.0, 0.0, 0.0]
    psDisplay.Opacity = 0.8
    return p


def createVolume(metrichash, data_reader):
    bounds = [float(x) for x in metrichash['position'].split(" ")]
    renderView1 = GetActiveViewOrCreate('RenderView')
    c = Clip(Input=data_reader)
    c.ClipType = 'Box'
    # (xmin,xmax,ymin,ymax,zmin,zmax)
    #c.ClipType.Bounds = [0.1, 3, 0.1, 2.3, 0.15, 2.3]
    c.ClipType.Bounds = bounds
    c.InsideOut = 1
    cDisplay = Show(c, renderView1)
    cDisplay.ColorArrayName = ['Points', metrichash['field']]
    cDisplay.SetRepresentationType('Surface')
    cDisplay.DiffuseColor = [1.0, 1.0, 0.0]
    cDisplay.Specular = 0
    cDisplay.Opacity = 0.1
    return c


def plotLine(infile):
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    warnings.filterwarnings('ignore')

    header = np.genfromtxt(infile, delimiter=',', names=True).dtype.names
    data = np.genfromtxt(infile, delimiter=',', skip_header=1)

    x = data[:, 0]
    y = data[:, 1]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y)

    locs, labels = plt.yticks()
    plt.yticks(locs, map(lambda x: "%g" % x, locs))

    plt.xlabel('Point')
    plt.ylabel(header[1])
    plt.title(infile.replace(".csv", "").replace("plot_", "") + ' Plot')
    plt.grid(True)
    plt.savefig(infile.replace(".csv", "") + ".png")


def createLine(metrichash, kpi, data_reader, outputDir="."):
    resolution = int(metrichash['resolution'])
    try:
        image = metrichash['image']
    except:
        image = None

    point = [x for x in metrichash['position'].split()]

    camera = GetActiveCamera()
    renderView1 = GetActiveViewOrCreate('RenderView')

    if point[0] == "center":
        point[0] = camera.GetFocalPoint()[0]
    if point[3] == "center":
        point[3] = camera.GetFocalPoint()[0]
    if point[1] == "center":
        point[1] = camera.GetFocalPoint()[1]
    if point[4] == "center":
        point[4] = camera.GetFocalPoint()[1]
    if point[2] == "center":
        point[2] = camera.GetFocalPoint()[2]
    if point[5] == "center":
        point[5] = camera.GetFocalPoint()[2]
    
    point1=[float(point[0]),float(point[1]),float(point[2])]
    point2=[float(point[3]),float(point[4]),float(point[5])]
    l = PlotOverLine(Input=data_reader, Source='High Resolution Line Source')
    l.PassPartialArrays = 1
    #l.Source.Point1 = [-0.609570026397705, 1.2191989705897868, 1.5207239668816328]
    #l.Source.Point2 = [3.044950008392334, 1.21919897058979, 1.5207239668816328]
    l.Source.Point1 = point1
    l.Source.Point2 = point2
    l.Source.Resolution = resolution
    lDisplay = Show(l, renderView1)
    lDisplay.DiffuseColor = [1.0, 0.0, 0.0]
    lDisplay.Specular = 0
    lDisplay.Opacity = 1
    
    
    # get the line data
    pl = servermanager.Fetch(l)

    kpifld = metrichash['field']
    kpiComp = metrichash['fieldComponent']
    if (image == "plot"):
        if not (os.path.exists(outputDir)):
            os.makedirs(outputDir)
        csvFileName = outputDir + "/plot_" + kpi + ".csv"
        f=open(csvFileName,"w")
        f.write("point,"+kpifld)
        if kpiComp:
            f.write("_" + kpiComp)
        f.write("\n")

    METRIC_INDEX=0
    for a in range(0,pl.GetPointData().GetNumberOfArrays()):
        if kpifld == pl.GetPointData().GetArrayName(a):
            METRIC_INDEX = a
    sum=0
    num=pl.GetPointData().GetArray(METRIC_INDEX).GetNumberOfTuples()
    # Get the component numbers from the input of line filter (data_reader) (?)
    compNumber = getfldCompNumber(data_reader.PointData[kpifld], kpiComp)
    for t in range(0,num):
        dataPoint = pl.GetPointData().GetArray(METRIC_INDEX).GetTuple(t)[compNumber]
        if str(float(dataPoint)).lower() != "nan":
            sum += dataPoint
        if image == "plot":
            f.write(",".join([str(t), str(dataPoint)])+"\n")
    if image == "plot":
        f.close()
        plotLine(csvFileName)
    ave=sum/pl.GetPointData().GetArray(METRIC_INDEX).GetNumberOfTuples()
    return l, ave


def adjustCamera(view, renderView1):
    camera=GetActiveCamera()
    if view == "iso":
        camera.SetFocalPoint(0, 0, 0)
        camera.SetPosition(0, -1, 0)
        renderView1.ResetCamera()
        # adjust for scale margin
        camera.SetFocalPoint(camera.GetFocalPoint()[0],camera.GetFocalPoint()[1],camera.GetFocalPoint()[2]-0.25)
        camera.SetPosition(camera.GetPosition()[0],camera.GetPosition()[1],camera.GetPosition()[2]-1)
        camera.Elevation(45)
        camera.Azimuth(45)
    elif view == "+X" or view == "+x" or view == "back": 
        camera.SetFocalPoint(0,0,0)
        camera.SetPosition(1,0,0)
        renderView1.ResetCamera()
    elif view == "-X" or view == "-x" or view == "front": 
        camera.SetFocalPoint(0,0,0)
        camera.SetPosition(-1,0,0)
        renderView1.ResetCamera()
    elif view == "+Y" or view == "+y" or view == "right": 
        camera.SetFocalPoint(0,0,0)
        camera.SetPosition(0,1,0)
        renderView1.ResetCamera()
    elif view == "-Y" or view == "-y" or view == "left": 
        camera.SetFocalPoint(0,0,0)
        camera.SetPosition(0,-1,0)
        renderView1.ResetCamera()
    elif view == "+Z" or view == "+z" or view == "top": 
        camera.SetFocalPoint(0,0,0)
        camera.SetPosition(0,0,1)
        renderView1.ResetCamera()
#        camera.Roll(90)
    elif view == "-Z" or view == "-z" or view == "bottom": 
        camera.SetFocalPoint(0,0,0)
        camera.SetPosition(0,0,-1)
        renderView1.ResetCamera()
#       camera.Roll(-90)


def makeAnimation(outputDir, kpi, magnification, deleteFrames=True):
    animationFramesDir = outputDir + '/animFrames'
    if not (os.path.exists(animationFramesDir)):
        os.makedirs(animationFramesDir)

    WriteAnimation(animationFramesDir + "/out_" + kpi + ".png", Magnification=magnification, FrameRate=15.0,
                   Compression=False)

    subprocess.call(["convert", "-delay", "15",  "-loop",  "0", animationFramesDir + "/out_" + kpi + ".*.png",
                     outputDir + "/out_" + kpi + ".gif"])

    if deleteFrames:
        shutil.rmtree(animationFramesDir)


def exportx3d(outputDir,kpi, metricObj, dataReader):

    blenderFramesDir = outputDir + kpi + '_blender'

    if not (os.path.exists(blenderFramesDir)):
        os.makedirs(blenderFramesDir)

    TimeSteps = getTimeSteps()


    firstTimeStep = TimeSteps[0]

    renderView1 = GetActiveViewOrCreate('RenderView')

    renderView1.ViewTime = firstTimeStep

    for num, time in enumerate(TimeSteps):
        #name = blenderFramesDir + str(num) + '.x3d'
        name_body = blenderFramesDir + '/' + str(num) + '_body.x3d'
        name_solo = blenderFramesDir + '/' + str(num) + '_solo.x3d'

        Show(metricObj, renderView1)
        Hide(dataReader, renderView1)
        ExportView(name_solo, view=renderView1)

        Show(dataReader, renderView1)
        Hide(metricObj, renderView1)
        ExportView(name_body, view=renderView1)

        animationScene1 = GetAnimationScene()

        animationScene1.GoToNext()

    # tar the directory
    data_IO.tarDirectory(blenderFramesDir + ".tar", blenderFramesDir)
    shutil.rmtree(blenderFramesDir)
