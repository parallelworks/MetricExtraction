#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'ExodusIIReader'
pipe_s2exo = ExodusIIReader(FileName=['/home/marmar/scratch/parallelWorks/weldingProject/pipe-problem/pipe_validation-2/test-2-therm-dev/pipe_s2.exo'])
pipe_s2exo.PointVariables = []
pipe_s2exo.NodeSetArrayStatus = []

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on pipe_s2exo
pipe_s2exo.GenerateObjectIdCellArray = 0
pipe_s2exo.GenerateGlobalElementIdArray = 0
pipe_s2exo.GenerateGlobalNodeIdArray = 0
pipe_s2exo.PointVariables = ['NT']
pipe_s2exo.ElementBlocks = ['PNT', 'C3D20 C3D20R', 'COMPOSITE LAYER C3D20', 'Beam B32 B32R', 'CPS8 CPE8 CAX8 S8 S8R', 'C3D8 C3D8R', 'TRUSS2', 'TRUSS2', 'CPS4R CPE4R S4 S4R', 'CPS4I CPE4I', 'C3D10', 'C3D4', 'C3D15', 'CPS6 CPE6 S6', 'C3D6', 'CPS3 CPE3 S3', '2-node 1d network entry elem', '2-node 1d network exit elem', '2-node 1d genuine network elem']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1423, 652]

# show data in view
pipe_s2exoDisplay = Show(pipe_s2exo, renderView1)
# trace defaults for the display properties.
pipe_s2exoDisplay.Representation = 'Surface'
pipe_s2exoDisplay.ColorArrayName = [None, '']
pipe_s2exoDisplay.EdgeColor = [0.0, 0.0, 0.0]
pipe_s2exoDisplay.OSPRayScaleArray = 'NT'
pipe_s2exoDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
pipe_s2exoDisplay.SelectOrientationVectors = 'NT'
pipe_s2exoDisplay.ScaleFactor = 53.097198486328125
pipe_s2exoDisplay.SelectScaleArray = 'NT'
pipe_s2exoDisplay.GlyphType = 'Arrow'
pipe_s2exoDisplay.PolarAxes = 'PolarAxesRepresentation'
pipe_s2exoDisplay.ScalarOpacityUnitDistance = 15.399587304238041
pipe_s2exoDisplay.GaussianRadius = 26.548599243164062
pipe_s2exoDisplay.SetScaleArray = ['POINTS', 'NT']
pipe_s2exoDisplay.ScaleTransferFunction = 'PiecewiseFunction'
pipe_s2exoDisplay.OpacityArray = ['POINTS', 'NT']
pipe_s2exoDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
pipe_s2exoDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
pipe_s2exoDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
pipe_s2exoDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
pipe_s2exoDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# reset view to fit data
renderView1.ResetCamera()

# set scalar coloring
ColorBy(pipe_s2exoDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
pipe_s2exoDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')
vtkBlockColorsLUT.InterpretValuesAsCategories = 1
vtkBlockColorsLUT.Annotations = ['0', '0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '10', '10', '11', '11']
vtkBlockColorsLUT.ActiveAnnotatedValues = ['2', '5']
vtkBlockColorsLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.63, 0.63, 1.0, 0.67, 0.5, 0.33, 1.0, 0.5, 0.75, 0.53, 0.35, 0.7, 1.0, 0.75, 0.5]

# create a new 'Calculator'
calculator1 = Calculator(Input=pipe_s2exo)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.ResultArrayName = 'Nt1'
calculator1.Function = 'NT'

# get color transfer function/color map for 'Nt1'
nt1LUT = GetColorTransferFunction('Nt1')
nt1LUT.RGBPoints = [-85.69471740722656, 0.231373, 0.298039, 0.752941, 433.8585433959961, 0.865003, 0.865003, 0.865003, 953.4118041992188, 0.705882, 0.0156863, 0.14902]
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
calculator1Display.SelectOrientationVectors = 'NT'
calculator1Display.ScaleFactor = 53.097198486328125
calculator1Display.SelectScaleArray = 'Nt1'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.ScalarOpacityUnitDistance = 15.399587304238041
calculator1Display.GaussianRadius = 26.548599243164062
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
Hide(pipe_s2exo, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

CreateLayout('Layout #2')

# set active view
SetActiveView(None)

# create a new 'Descriptive Statistics'
descriptiveStatistics1 = DescriptiveStatistics(Input=calculator1,
    ModelInput=None)
descriptiveStatistics1.VariablesofInterest = ['NT', 'Nt1']

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
descriptiveStatistics1Display.CompositeDataSetIndex = [8]

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

# Properties modified on descriptiveStatistics1
descriptiveStatistics1.TrainingFraction = 1.0


animationScene1.GoToFirst()


# save data
SaveData('/home/marmar/scratch/parallelWorks/weldingProject/pipe-problem/pipe_validation-2/test-2-therm-dev/testAnim/test_pDS.csv', proxy=descriptiveStatistics1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.0, 1107.0416267099943]
renderView1.CameraParallelScale = 286.52345671382193

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).