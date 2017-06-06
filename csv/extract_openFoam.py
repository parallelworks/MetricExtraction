from paraview.simple import *
import sys

paraview.simple._DisableFirstRenderCameraReset()

magnification = 2
individualImages = True

f = open('kpi.csv', 'r')
kpihash={}
cols = [l.replace("\n","") for l in  f.readline().split(",")]
for i,line in enumerate(f):
    data = [l.replace("\n","") for l in line.split(",")]
    kpihash[data[0]]={}
    for ii,v in enumerate(data):
        if ii != 0:
            kpihash[data[0]][cols[ii]] = v
f.close()

cellsarrays=[]
for kpi in kpihash:
    cellsarrays.append(kpihash[kpi]['field'])
ca = set(cellsarrays)
cellsarrays = list(ca)

#casefoam = STLReader(FileNames=['constant/triSurface/main.stl'])
casefoam = OpenFOAMReader(FileName='case.foam')
casefoam.MeshRegions = ['internalMesh']
# only load the data that is needed
casefoam.CellArrays = cellsarrays

latesttime = GetTimeKeeper().TimestepValues[-1]
print "Latest Time: ",latesttime

renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewSize = [700, 600]
renderView1.Background = [1,1,1] # set background color
renderView1.OrientationAxesVisibility=False
renderView1.ViewTime = latesttime

casefoamDisplay = Show(casefoam, renderView1)
casefoamDisplay.ColorArrayName = [None, '']
casefoamDisplay.SetRepresentationType('Surface')
#casefoamDisplay.SetRepresentationType('Wireframe')
casefoamDisplay.AmbientColor = [0.0, 0.0, 0.0]
casefoamDisplay.EdgeColor = [0.0, 0.0, 0.0]
casefoamDisplay.Specular = 0
casefoamDisplay.Opacity = 0.3

#ctf = GetColorTransferFunction('STLSolidLabeling')
#ctf.ApplyPreset('X Ray', True)
#ColorBy(casefoamDisplay, ('CELLS', 'STLSolidLabeling'))

ColorBy(casefoamDisplay, None)

renderView1.ResetCamera()
renderView1.InteractionMode = '2D'

camera=GetActiveCamera()
camera.SetFocalPoint(0,0,0)
camera.SetPosition(0,-1,0)
#camera.SetViewUp(0,0,1)
renderView1.ResetCamera()
# adjust for scale margin
camera.SetFocalPoint(camera.GetFocalPoint()[0],camera.GetFocalPoint()[1],camera.GetFocalPoint()[2]-0.25)
camera.SetPosition(camera.GetPosition()[0],camera.GetPosition()[1],camera.GetPosition()[2]-1)
# isometric view
#camera.Dolly(0.8)
#camera.Roll(0)
camera.Elevation(45)
camera.Azimuth(45)

SaveScreenshot("out_stl.png", magnification=magnification, quality=100)

def colorMetric(d,kpi):
    display = GetDisplayProperties(d)
    ColorBy(display, ('POINTS', kpihash[kpi]['field']))
    Render()
    UpdateScalarBars()
    ctf = GetColorTransferFunction(kpihash[kpi]['field'])
    ctf.ApplyPreset(kpihash[kpi]["colorscale"], True)
    if kpihash[kpi]["invertcolor"] == "1":
        ctf.InvertTransferFunction()
    #datarange = d.GetPointDataInformation().GetArray(kpihash[kpi]['field']).GetComponentRange(0)
    datarange = d.PointData[kpihash[kpi]['field']].GetRange()
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

def createSlice(kpi):
    opacity=float(kpihash[kpi]['opacity'])
    bodyopacity=float(kpihash[kpi]['bodyopacity'])
    if individualImages == True:
        casefoamDisplay.Opacity = bodyopacity
    slicetype="Plane"
    plane=kpihash[kpi]['type'].split("_")[1]
    origin=kpihash[kpi]['position'].split(" ")
    s = Slice(Input=casefoam)
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
    colorMetric(s,kpi)

    return s

def createClip(kpi):
    opacity=float(kpihash[kpi]['opacity'])
    bodyopacity=float(kpihash[kpi]['bodyopacity'])
    if individualImages == True:
        casefoamDisplay.Opacity = bodyopacity
    cliptype="Plane"
    plane=kpihash[kpi]['type'].split("_")[1]
    try:
        if kpihash[kpi]['type'].split("_")[2] == "Invert":
            invert=1
    except:
        invert=0
    origin=kpihash[kpi]['position'].split(" ")
    s = Clip(Input=casefoam)
    s.ClipType = cliptype
    s.ClipType.Origin = camera.GetFocalPoint()
    s.InsideOut = invert
    if origin[0] != "center":
        s.ClipType.Origin[0] = float(origin[0])
    if origin[1] != "center":
        s.ClipType.Origin[1] = float(origin[1])
    if origin[2] != "center":
        s.ClipType.Origin[2] = float(origin[2])
    if (plane == "X" or plane == "x"):
        normal = [1.0, 0.0, 0.0]
    if (plane == "Y" or plane == "y"):
        normal = [0.0, 1.0, 0.0]
    if (plane == "Z" or plane == "z"):
        normal = [0.0, 0.0, 1.0]
    s.ClipType.Normal = normal
    sDisplay = Show(s, renderView1)
    sDisplay.ColorArrayName = [None, '']
    sDisplay.SetRepresentationType('Surface')
    sDisplay.DiffuseColor = [0.0, 1.0, 0.0]
    sDisplay.Specular = 0
    sDisplay.Opacity = opacity
    colorMetric(s,kpi)
    try:
        if kpihash[kpi]['image'].split("_")[1] == "solo":
            Hide(casefoam,renderView1)
    except:
        pass
    return s

def createProbe(kpi):
    center = kpihash[kpi]['position'].split(" ")
    p = ProbeLocation(Input=casefoam,ProbeType='Fixed Radius Point Source')
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

def createVolume(kpi):
    bounds = [float(x) for x in kpihash[kpi]['position'].split(" ")]
    c = Clip(Input=casefoam)
    c.ClipType = 'Box'
    # (xmin,xmax,ymin,ymax,zmin,zmax)
    #c.ClipType.Bounds = [0.1, 3, 0.1, 2.3, 0.15, 2.3]
    c.ClipType.Bounds = bounds
    c.InsideOut = 1
    cDisplay = Show(c, renderView1)
    cDisplay.ColorArrayName = [None, '']
    cDisplay.SetRepresentationType('Surface')
    cDisplay.DiffuseColor = [1.0, 1.0, 0.0]
    cDisplay.Specular = 0
    cDisplay.Opacity = 0.1
    return c

def createLine(kpi):
    resolution=int(kpihash[kpi]['type'].split("_")[1])
    try:
        image=kpihash[kpi]['image']
    except:
        image=None
    point = [x for x in kpihash[kpi]['position'].split(" ")]
    
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
    l = PlotOverLine(Input=casefoam, Source='High Resolution Line Source')
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
    if (image == "plot"):
        f=open("plot_"+kpi+".csv","w")
        f.write(",".join(["point",kpihash[kpi]['field']])+"\n")
    METRIC_INDEX=0
    for a in range(0,pl.GetPointData().GetNumberOfArrays()):
        if kpihash[kpi]['field'] == pl.GetPointData().GetArrayName(a):
            METRIC_INDEX = a
    sum=0
    num=pl.GetPointData().GetArray(METRIC_INDEX).GetNumberOfTuples()
    for t in range(0,num):
        if str(float(pl.GetPointData().GetArray(METRIC_INDEX).GetTuple(t)[0])).lower() != "nan":
            sum+=pl.GetPointData().GetArray(METRIC_INDEX).GetTuple(t)[0]
        if (image == "plot"):
            f.write(",".join([str(t),str(pl.GetPointData().GetArray(METRIC_INDEX).GetTuple(t)[0])])+"\n")
    if (image == "plot"):
        f.close()
    ave=sum/pl.GetPointData().GetArray(METRIC_INDEX).GetNumberOfTuples()
    return l,ave

def adjustCamera(view):
    camera=GetActiveCamera()
    if view == "iso":
        camera.SetFocalPoint(0,0,0)
        camera.SetPosition(0,-1,0)
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
        

print "Generating KPIs"

f = open("metrics.csv","w")
f.write(",".join(['metric','ave','min','max'])+"\n")

for kpi in kpihash:
    
    print kpi
    
    kpitype=kpihash[kpi]['type'].split("_")[0]
    kpifield=kpihash[kpi]['field']
    try:
        kpiimage=kpihash[kpi]['image'].split("_")[0]
    except:
        kpiimage="None"

    if individualImages == True:
        HideAll()
        Show(casefoam,renderView1)
        if kpiimage != "None" and kpiimage != "" and kpiimage != "plot":
            adjustCamera(kpiimage)
    
    if (kpitype=="Slice"):
        d = createSlice(kpi)
    elif (kpitype=="Clip"):
        d = createClip(kpi)
    elif (kpitype=="Probe"):
        d = createProbe(kpi)
    elif (kpitype=="Line"):
        d,ave = createLine(kpi)
    elif (kpitype=="Volume"):
        d = createVolume(kpi)
        
    datarange=d.PointData[kpifield].GetRange()

    if kpitype == "Probe":
        average=(datarange[0]+datarange[1])/2
    elif kpitype == "Line":
        average=ave
    elif kpitype == "Slice":
        # get kpi field value and area - average = value/area
        integrateVariables = IntegrateVariables(Input=d)
        average=integrateVariables.CellData[kpifield].GetRange()[0]/integrateVariables.CellData['Area'].GetRange()[0]
    elif kpitype == "Volume" or kpitype == "Clip":
        integrateVariables = IntegrateVariables(Input=d)
        average=integrateVariables.CellData[kpifield].GetRange()[0]/integrateVariables.CellData['Volume'].GetRange()[0]
    
    f.write(",".join([kpi,str(average),str(datarange[0]),str(datarange[1])])+"\n")
    
    if individualImages == True:
        if kpiimage != "None" and kpiimage != "" and kpiimage != "plot":
            SaveScreenshot("out_"+kpi+".png", magnification=magnification, quality=100)

f.close()

if individualImages == False:
    SaveScreenshot("out.png", magnification=magnification, quality=100)
