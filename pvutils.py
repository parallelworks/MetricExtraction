from paraview.simple import *
import sys

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


def scalar_field(fieldname, delimiter='_'):
    if len(fieldname.split(delimiter)) == 1:
        return True
    elif len(fieldname.split(delimiter)) == 2:
        return False
    else:
        print("Check the format of the field name '" + fieldname + "'")
        sys.exit(1)


def splitfieldComponent(fieldname,delimiter='_'):
    if scalar_field(fieldname, delimiter):
        return fieldname,''
    else:
        return fieldname.split(delimiter)[0], fieldname.split(delimiter)[1]


def getfieldsfromkpihash(kpihash):
    cellsarrays = []
    for kpi in kpihash:
        kpifield = kpihash[kpi]['field']
        cellsarrays.append(kpifield.split('_')[0])

    ca = set(cellsarrays)

    cellsarrays = list(ca)
    return cellsarrays


def getfldComponentMap(arrayInfo):
    compName2num = {}
    numComps = arrayInfo.GetNumberOfComponents()
    if numComps>1:
        for iComp in range(-1,numComps):
            compName2num[arrayInfo.GetComponentName(iComp)] = iComp
    return compName2num


def getfldCompNumber(arrayInfo, kpifld_Comp):
    kpiComp = splitfieldComponent(kpifld_Comp)[1]
    compNumberMap = getfldComponentMap(arrayInfo)
    if not kpiComp:
        compNum = 0
    else:
        compNum = compNumberMap[kpiComp]
    return compNum


def getdatarange(datasource, kpifld_Comp):
    kpifld = splitfieldComponent(kpifld_Comp)[0]
    arrayInfo = datasource.PointData[kpifld]
    compNumber = getfldCompNumber(arrayInfo, kpifld_Comp)
    datarange = arrayInfo.GetRange(compNumber)
    return datarange


def colorMetric(d, kpi, kpihash):
    display = GetDisplayProperties(d)

    kpifld, kpifldcomp = splitfieldComponent(kpihash[kpi]['field'])

    ColorBy(display, ('POINTS', kpifld, kpifldcomp))
    Render()
    UpdateScalarBars()
    ctf = GetColorTransferFunction(kpifld)
    ctf.ApplyPreset(kpihash[kpi]["colorscale"], True)
    if kpihash[kpi]["invertcolor"] == "1":
        ctf.InvertTransferFunction()

    datarange = getdatarange(d, kpihash[kpi]['field'])

    min = datarange[0]
    max = datarange[1]
    if kpihash[kpi]["min"] != "auto" and kpihash[kpi]["min"] != "":
         min = float(kpihash[kpi]["min"]) 
    if kpihash[kpi]["max"] != "auto" and kpihash[kpi]["max"] != "":
         max = float(kpihash[kpi]["max"]) 
    ctf.RescaleTransferFunction(min, max)
    if int(kpihash[kpi]["discretecolors"]) > 0:
        ctf.Discretize = 1
        ctf.NumberOfTableValues = int(kpihash[kpi]["discretecolors"])
    else:
        ctf.Discretize = 0
    GetScalarBar(ctf).TitleColor = [0,0,0]
    GetScalarBar(ctf).LabelColor = [0,0,0]
    GetScalarBar(ctf).Orientation = "Horizontal"
    
    # center
    imgtype=kpihash[kpi]['image'].split("_")[0]
    if (imgtype!="iso"):
        GetScalarBar(ctf).Position = [0.25,0.05]
        GetScalarBar(ctf).Position2 = [0.5,0]
    else:
        # left
        GetScalarBar(ctf).Position = [0.05,0.025]
        GetScalarBar(ctf).Position2 = [0.4,0]
    
    #if individualImages == False:
    #    display.SetScalarBarVisibility(renderView1, False)


def createSlice(kpi, kpihash, dataReader, dataDisplay, isIndivImgs):
    camera = GetActiveCamera()
    renderView1 = GetActiveViewOrCreate('RenderView')

    opacity=float(kpihash[kpi]['opacity'])
    bodyopacity=float(kpihash[kpi]['bodyopacity'])
    if isIndivImgs:
        dataDisplay.Opacity = bodyopacity
    slicetype = "Plane"
    plane=kpihash[kpi]['type'].split("_")[1]
    origin=kpihash[kpi]['position'].split(" ")
    s = Slice(Input=dataReader)
    s.SliceType = slicetype
    s.SliceType.Origin = camera.GetFocalPoint()
    if origin[0] != "center":
        s.SliceType.Origin[0] = float(origin[0])
    if origin[1] != "center":
        s.SliceType.Origin[1] = float(origin[1])
    if origin[2] != "center":
        s.SliceType.Origin[2] = float(origin[2])
    if (plane == "X" or plane == "x"):
        normal = [1.0, 0.0, 0.0]
    if (plane == "Y" or plane == "y"):
        normal = [0.0, 1.0, 0.0]
    if (plane == "Z" or plane == "z"):
        normal = [0.0, 0.0, 1.0]
    s.SliceType.Normal = normal
    sDisplay = Show(s, renderView1)
    sDisplay.ColorArrayName = [None, '']
    sDisplay.SetRepresentationType('Surface')
    sDisplay.DiffuseColor = [0.0, 1.0, 0.0]
    sDisplay.Specular = 0
    sDisplay.Opacity = opacity
    colorMetric(s, kpi, kpihash)
    return s


def createClip(kpi, kpihash, data_reader, data_display, isIndivImages):
    camera = GetActiveCamera()
    renderView1 = GetActiveViewOrCreate('RenderView')

    opacity = float(kpihash[kpi]['opacity'])
    bodyopacity = float(kpihash[kpi]['bodyopacity'])
    if isIndivImages == True:
        data_display.Opacity = bodyopacity
    cliptype = "Plane"
    plane = kpihash[kpi]['type'].split("_")[1]
    try:
        if kpihash[kpi]['type'].split("_")[2] == "Invert":
            invert = 1
    except:
        invert = 0
    origin=kpihash[kpi]['position'].split(" ")
    s = Clip(Input=data_reader)
    s.ClipType = cliptype
    s.ClipType.Origin = camera.GetFocalPoint()
    s.InsideOut = invert
    if origin[0] != "center":
        s.ClipType.Origin[0] = float(origin[0])
    if origin[1] != "center":
        s.ClipType.Origin[1] = float(origin[1])
    if origin[2] != "center":
        s.ClipType.Origin[2] = float(origin[2])
    if plane == "X" or plane == "x":
        normal = [1.0, 0.0, 0.0]
    if plane == "Y" or plane == "y":
        normal = [0.0, 1.0, 0.0]
    if plane == "Z" or plane == "z":
        normal = [0.0, 0.0, 1.0]
    s.ClipType.Normal = normal
    sDisplay = Show(s, renderView1)
    sDisplay.ColorArrayName = [None, '']
    sDisplay.SetRepresentationType('Surface')
    sDisplay.DiffuseColor = [0.0, 1.0, 0.0]
    sDisplay.Specular = 0
    sDisplay.Opacity = opacity
    colorMetric(s, kpi, kpihash)
    try:
        if kpihash[kpi]['image'].split("_")[1] == "solo":
            Hide(data_reader, renderView1)
    except:
        pass
    return s


def createProbe(kpi, kpihash, data_reader):
    camera = GetActiveCamera()
    renderView1 = GetActiveViewOrCreate('RenderView')
    center = kpihash[kpi]['position'].split(" ")
    p = ProbeLocation(Input=data_reader, ProbeType='Fixed Radius Point Source')
    p.PassFieldArrays = 1
    #p.ProbeType.Center = [1.2176899909973145, 1.2191989705897868, 1.5207239668816328]
    p.ProbeType.Center = camera.GetFocalPoint()
    if center[0] != "center":
        p.ProbeType.Center[0] = float(center[0])
    if center[1] != "center":
        p.ProbeType.Center[1] = float(center[1])
    if center[2] != "center":
        p.ProbeType.Center[2] = float(center[2])
    p.ProbeType.NumberOfPoints = 1
    p.ProbeType.Radius = 0.0
    ps = Sphere(Radius=0.025, ThetaResolution=32)
    ps.Center = camera.GetFocalPoint()
    if center[0] != "center":
        ps.Center[0] = float(center[0])
    if center[1] != "center":
        ps.Center[1] = float(center[1])
    if center[2] != "center":
        ps.Center[2] = float(center[2])
    psDisplay = Show(ps, renderView1)
    psDisplay.DiffuseColor = [1.0, 0.0, 0.0]
    psDisplay.Opacity = 0.8
    return p


def createVolume(kpi, kpihash, data_reader):
    bounds = [float(x) for x in kpihash[kpi]['position'].split(" ")]
    renderView1 = GetActiveViewOrCreate('RenderView')
    c = Clip(Input=data_reader)
    c.ClipType = 'Box'
    # (xmin,xmax,ymin,ymax,zmin,zmax)
    #c.ClipType.Bounds = [0.1, 3, 0.1, 2.3, 0.15, 2.3]
    c.ClipType.Bounds = bounds
    c.InsideOut = 1
    cDisplay = Show(c, renderView1)
    cDisplay.ColorArrayName = ['Points', kpihash[kpi]['field']]
    cDisplay.SetRepresentationType('Surface')
    cDisplay.DiffuseColor = [1.0, 1.0, 0.0]
    cDisplay.Specular = 0
    cDisplay.Opacity = 0.1
    return c


def createLine(kpi, kpihash, data_reader):
    resolution = int(kpihash[kpi]['type'].split("_")[1])
    try:
        image = kpihash[kpi]['image']
    except:
        image = None
    point = [x for x in kpihash[kpi]['position'].split(" ")]

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
    kpifld_comp = kpihash[kpi]['field']
    kpifld = splitfieldComponent(kpifld_comp)[0]
    if (image == "plot"):
        f=open("plot_"+kpi+".csv","w")
        f.write(",".join(["point", kpifld_comp])+"\n")
    METRIC_INDEX=0
    for a in range(0,pl.GetPointData().GetNumberOfArrays()):
        if kpifld == pl.GetPointData().GetArrayName(a):
            METRIC_INDEX = a
    sum=0
    num=pl.GetPointData().GetArray(METRIC_INDEX).GetNumberOfTuples()
    # Get the component numbers from the input of line filter (data_reader) (?)
    compNumber = getfldCompNumber(data_reader.PointData[kpifld], kpifld_comp)
    for t in range(0,num):
        dataPoint = pl.GetPointData().GetArray(METRIC_INDEX).GetTuple(t)[compNumber]
        if str(float(dataPoint)).lower() != "nan":
            sum += dataPoint
        if (image == "plot"):
            f.write(",".join([str(t), str(dataPoint)])+"\n")
    if (image == "plot"):
        f.close()
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
        camera.Roll(90)
    elif view == "-Z" or view == "-z" or view == "bottom": 
        camera.SetFocalPoint(0,0,0)
        camera.SetPosition(0,0,-1)
        renderView1.ResetCamera()
        camera.Roll(-90)
        

