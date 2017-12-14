#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'ExodusIIReader'
solveexo = ExodusIIReader(FileName=['/home/marmar/Dropbox/parallelWorks/mexdex/MetricExtraction/sample_inputs/solve.exo'])
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
# uncomment following to set a specific view size
# renderView1.ViewSize = [1423, 652]

# show data in view
solveexoDisplay = Show(solveexo, renderView1)
# trace defaults for the display properties.
solveexoDisplay.Representation = 'Surface'
solveexoDisplay.ColorArrayName = [None, '']
solveexoDisplay.EdgeColor = [0.0, 0.0, 0.0]
solveexoDisplay.OSPRayScaleArray = 'GlobalNodeId'
solveexoDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
solveexoDisplay.SelectOrientationVectors = 'GlobalNodeId'
solveexoDisplay.ScaleFactor = 1.2000000000000002
solveexoDisplay.SelectScaleArray = 'GlobalNodeId'
solveexoDisplay.GlyphType = 'Arrow'
solveexoDisplay.PolarAxes = 'PolarAxesRepresentation'
solveexoDisplay.ScalarOpacityUnitDistance = 0.6341450083532408
solveexoDisplay.GaussianRadius = 0.6000000000000001
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

# set scalar coloring
ColorBy(solveexoDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
solveexoDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')
vtkBlockColorsLUT.InterpretValuesAsCategories = 1
vtkBlockColorsLUT.Annotations = ['0', '0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '10', '10', '11', '11']
vtkBlockColorsLUT.ActiveAnnotatedValues = ['11']
vtkBlockColorsLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.63, 0.63, 1.0, 0.67, 0.5, 0.33, 1.0, 0.5, 0.75, 0.53, 0.35, 0.7, 1.0, 0.75, 0.5]

# set scalar coloring
ColorBy(solveexoDisplay, ('POINTS', 'NT'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
solveexoDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
solveexoDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'NT'
nTLUT = GetColorTransferFunction('NT')
nTLUT.RGBPoints = [25.000221252441406, 0.231373, 0.298039, 0.752941, 170.75110244750977, 0.865003, 0.865003, 0.865003, 316.5019836425781, 0.705882, 0.0156863, 0.14902]
nTLUT.ScalarRangeInitialized = 1.0

# create a new 'Calculator'
calculator1 = Calculator(Input=solveexo)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.ResultArrayName = 'Nt1'
calculator1.Function = 'NT'

# get color transfer function/color map for 'Nt1'
nt1LUT = GetColorTransferFunction('Nt1')
nt1LUT.RGBPoints = [25.000221252441406, 0.231373, 0.298039, 0.752941, 170.75110244750977, 0.865003, 0.865003, 0.865003, 316.5019836425781, 0.705882, 0.0156863, 0.14902]
nt1LUT.ScalarRangeInitialized = 1.0

# show data in view
calculator1Display = Show(calculator1, renderView1)
# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = ['POINTS', 'Nt1']
calculator1Display.LookupTable = nt1LUT
calculator1Display.EdgeColor = [0.0, 0.0, 0.0]
calculator1Display.OSPRayScaleArray = 'Nt1'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'GlobalNodeId'
calculator1Display.ScaleFactor = 1.2000000000000002
calculator1Display.SelectScaleArray = 'Nt1'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.ScalarOpacityUnitDistance = 0.6341450083532408
calculator1Display.GaussianRadius = 0.6000000000000001
calculator1Display.SetScaleArray = ['POINTS', 'Nt1']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = ['POINTS', 'Nt1']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
calculator1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
calculator1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
calculator1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
calculator1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# hide data in view
Hide(solveexo, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# create a new 'Descriptive Statistics'
descriptiveStatistics1 = DescriptiveStatistics(Input=calculator1,
    ModelInput=None)
descriptiveStatistics1.VariablesofInterest = ['GlobalNodeId', 'HFL', 'NT', 'Nt1', 'PedigreeNodeId', 'S', 'U']

CreateLayout('Layout #2')

# set active view
SetActiveView(None)

# Properties modified on descriptiveStatistics1
descriptiveStatistics1.VariablesofInterest = ['Nt1']

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024L
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# get layout
layout2 = GetLayout()

# place view in the layout
layout2.AssignView(0, spreadSheetView1)

# show data in view
descriptiveStatistics1Display = Show(descriptiveStatistics1, spreadSheetView1)
# trace defaults for the display properties.
descriptiveStatistics1Display.FieldAssociation = 'Row Data'
descriptiveStatistics1Display.CompositeDataSetIndex = [14]

# Create a new 'SpreadSheet View'
spreadSheetView2 = CreateView('SpreadSheetView')
spreadSheetView2.ColumnToSort = ''
spreadSheetView2.BlockSize = 1024L
# uncomment following to set a specific view size
# spreadSheetView2.ViewSize = [400, 400]

# place view in the layout
layout2.AssignView(2, spreadSheetView2)

# show data in view
descriptiveStatistics1Display_1 = Show(OutputPort(descriptiveStatistics1, 1), spreadSheetView2)
# trace defaults for the display properties.
descriptiveStatistics1Display_1.CompositeDataSetIndex = [2]

animationScene1.GoToFirst()

animationScene1.GoToNext()

# Properties modified on descriptiveStatistics1
descriptiveStatistics1.TrainingFraction = 1.0

# Rescale transfer function
nt1LUT.RescaleTransferFunction(25.0002212524, 506.721679688)

# get opacity transfer function/opacity map for 'Nt1'
nt1PWF = GetOpacityTransferFunction('Nt1')
nt1PWF.Points = [25.000221252441406, 0.0, 0.5, 0.0, 316.5019836425781, 1.0, 0.5, 0.0]
nt1PWF.ScalarRangeInitialized = 1

# Rescale transfer function
nt1PWF.RescaleTransferFunction(25.0002212524, 506.721679688)

animationScene1.GoToFirst()

# save data
fileRoot = '/home/marmar/scratch/parallelWorks/weldingProject/pipe-problem/pipe_validation-2/test-2-therm-dev/testAnim/testDS_'
for i in range(5):
    SaveData(fileRoot +str(i)+  '.csv', proxy=descriptiveStatistics1)

    animationScene1.GoToNext()


#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [2.0, 0.0, 30.065301543155115]
renderView1.CameraFocalPoint = [2.0, 0.0, -0.2500000447034836]
renderView1.CameraParallelScale = 7.846177408964493

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
