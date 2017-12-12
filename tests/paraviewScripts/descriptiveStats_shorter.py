#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'ExodusIIReader'
solveexo = ExodusIIReader(FileName=['/home/marmar/Dropbox/parallelWorks/mexdex/MetricExtraction/sample_inputs/solve.exo'])

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on solveexo
solveexo.GenerateObjectIdCellArray = 0
solveexo.GenerateGlobalElementIdArray = 0
solveexo.GenerateGlobalNodeIdArray = 0
solveexo.PointVariables = ['NT']
solveexo.ElementBlocks = ['PNT', 'C3D20 C3D20R', 'COMPOSITE LAYER C3D20', 'Beam B32 B32R', 'CPS8 CPE8 CAX8 S8 S8R', 'C3D8 C3D8R', 'TRUSS2', 'TRUSS2', 'CPS4R CPE4R S4 S4R', 'CPS4I CPE4I', 'C3D10', 'C3D4', 'C3D15', 'CPS6 CPE6 S6', 'C3D6', 'CPS3 CPE3 S3', '2-node 1d network entry elem', '2-node 1d network exit elem', '2-node 1d genuine network elem']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1423, 514]

# show data in view
solveexoDisplay = Show(solveexo, renderView1)
# trace defaults for the display properties.
solveexoDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera()

# set scalar coloring
ColorBy(solveexoDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
solveexoDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# create a new 'Calculator'
calculator1 = Calculator(Input=solveexo)

# Properties modified on calculator1
calculator1.ResultArrayName = 'NT'
calculator1.Function = 'NT'

# show data in view
calculator1Display = Show(calculator1, renderView1)
# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'

# hide data in view
Hide(solveexo, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'NT'
nTLUT = GetColorTransferFunction('NT')

# create a new 'Descriptive Statistics'
descriptiveStatistics1 = DescriptiveStatistics(Input=calculator1,
    ModelInput=None)

CreateLayout('Layout #2')

# set active view
SetActiveView(None)

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

# set active view
SetActiveView(spreadSheetView1)

# set active source
SetActiveSource(descriptiveStatistics1)

# set active view
SetActiveView(renderView1)

animationScene1.GoToPrevious()

animationScene1.GoToPrevious()

animationScene1.GoToNext()

animationScene1.GoToNext()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [2.0, 0.0, 30.065301543155115]
renderView1.CameraFocalPoint = [2.0, 0.0, -0.2500000447034836]
renderView1.CameraParallelScale = 7.846177408964493

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).