import sys
import os
import subprocess

#### import the simple module from the paraview
from paraview.simple import *

if len(sys.argv) < 3:
    print("Number of provided arguments: ", len(sys.argv) - 1)
    print("Usage: pvpython pvLoadSavePngs.py  <solve.exo>  <imgDir/> ")
    sys.exit()

solveexoFileAddress = sys.argv[1]
imageFilesDir = sys.argv[2]
imageName = 'temp.png'

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'ExodusIIReader'
solveexo = ExodusIIReader(FileName=solveexoFileAddress) 
solveexo.PointVariables = []
solveexo.NodeSetArrayStatus = []

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on solveexo
solveexo.PointVariables = ['U', 'NT', 'S', 'HFL']
solveexo.ElementBlocks = ['PNT', 'C3D20 C3D20R', 'COMPOSITE LAYER C3D20', 'Beam B32 B32R', 'CPS8 CPE8 CAX8 S8 S8R', 'C3D8 C3D8R', 'TRUSS2', 'TRUSS2', 'CPS4R CPE4R S4 S4R', 'CPS4I CPE4I', 'C3D10', 'C3D4', 'C3D15', 'CPS6 CPE6 S6', 'C3D6', 'CPS3 CPE3 S3', '2-node 1d network entry elem', '2-node 1d network exit elem', '2-node 1d genuine network elem']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# set the view size
renderView1.ViewSize = [1024, 768]

# show data in view
solveexoDisplay = Show(solveexo, renderView1)
# trace defaults for the display properties.
solveexoDisplay.Representation = 'Surface'
solveexoDisplay.ColorArrayName = [None, '']
solveexoDisplay.EdgeColor = [0.0, 0.0, 0.0]
solveexoDisplay.OSPRayScaleArray = 'GlobalNodeId'
solveexoDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
solveexoDisplay.SelectOrientationVectors = 'GlobalNodeId'
solveexoDisplay.SelectScaleArray = 'GlobalNodeId'
solveexoDisplay.GlyphType = 'Arrow'
solveexoDisplay.PolarAxes = 'PolarAxesRepresentation'
solveexoDisplay.ScalarOpacityUnitDistance = 1.3416442064699057
solveexoDisplay.GaussianRadius = 0.5
solveexoDisplay.SetScaleArray = ['POINTS', 'GlobalNodeId']
solveexoDisplay.ScaleTransferFunction = 'PiecewiseFunction'
solveexoDisplay.OpacityArray = ['POINTS', 'GlobalNodeId']
solveexoDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
solveexoDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
solveexoDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
solveexoDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
solveexoDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# reset view to fit data
renderView1.ResetCamera()

# # set scalar coloring
# ColorBy(solveexoDisplay, ('FIELD', 'vtkBlockColors'))

# # show color bar/color legend
# solveexoDisplay.SetScalarBarVisibility(renderView1, True)

# # get color transfer function/color map for 'vtkBlockColors'
# vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# set scalar coloring
ColorBy(solveexoDisplay, ('POINTS', 'NT'))

# rescale color and/or opacity maps used to include current data range
solveexoDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
solveexoDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'NT'
nTLUT = GetColorTransferFunction('NT')

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
nTLUT.ApplyPreset('jet', True)

animationScene1.GoToLast()

# rescale color and/or opacity maps used to exactly fit the current data range
solveexoDisplay.RescaleTransferFunctionToDataRange(False, True)

animationScene1.GoToFirst()

# change representation type
solveexoDisplay.SetRepresentationType('Surface With Edges')

# get color legend/bar for nTLUT in view renderView1
nTLUTColorBar = GetScalarBar(nTLUT, renderView1)

# Properties modified on nTLUTColorBar
nTLUTColorBar.Title = 'Temperature ($^\\circ$C)'

# Properties modified on nTLUTColorBar
nTLUTColorBar.RangeLabelFormat = '%4.3g'

# Properties modified on nTLUTColorBar
nTLUTColorBar.AutomaticLabelFormat = 0
nTLUTColorBar.LabelFormat = '%-#6.3g'

# Properties modified on nTLUTColorBar
nTLUTColorBar.TitleJustification = 'Right'

# change scalar bar placement
nTLUTColorBar.Position = [0.043, 0.306]
nTLUTColorBar.Position2 = [0.12, 0.43]

# current camera placement for renderView1

renderView1.CameraFocalPoint = [-0.21, -1.33, -1.19]
renderView1.CameraPosition = [8.9, -11.9, 16.6]
renderView1.CameraViewUp = [-0.50, 0.60, 0.62] 
renderView1.CameraParallelScale = 7.09

# save animation images/movie
if not(os.path.exists(imageFilesDir)):
    os.makedirs(imageFilesDir)

WriteAnimation(imageFilesDir + '/' +  imageName, Magnification=1, FrameRate=15.0, Compression=False)

# makeGifArgs = ['convert', '-delay', '15', '-loop', '0', imageFilesDir+'*.png', imageFilesDir+'temp.gif']
# popen = subprocess.Popen(makeGifArgs, stdout=subprocess.PIPE)
# popen.wait()

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
