#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'ExodusIIReader'
analysisexo = ExodusIIReader(FileName=['/home/marmar/scratch/parallelWorks/weldingProject/EWI-Workflow-Scripts-Dec20-2017-orig/tmp/post-process/analysis.exo'])
analysisexo.PointVariables = []
analysisexo.NodeSetArrayStatus = []

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on analysisexo
analysisexo.PointVariables = ['U', 'NT', 'S', 'PEEQ', 'HFL']
analysisexo.ElementBlocks = ['PNT', 'C3D20 C3D20R', 'COMPOSITE LAYER C3D20', 'Beam B32 B32R', 'CPS8 CPE8 CAX8 S8 S8R', 'C3D8 C3D8R', 'TRUSS2', 'TRUSS2', 'CPS4R CPE4R S4 S4R', 'CPS4I CPE4I', 'C3D10', 'C3D4', 'C3D15', 'CPS6 CPE6 S6', 'C3D6', 'CPS3 CPE3 S3', '2-node 1d network entry elem', '2-node 1d network exit elem', '2-node 1d genuine network elem']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1113, 542]

# show data in view
analysisexoDisplay = Show(analysisexo, renderView1)
# trace defaults for the display properties.
analysisexoDisplay.Representation = 'Surface'
analysisexoDisplay.ColorArrayName = [None, '']
analysisexoDisplay.EdgeColor = [0.0, 0.0, 0.0]
analysisexoDisplay.OSPRayScaleArray = 'GlobalNodeId'
analysisexoDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
analysisexoDisplay.SelectOrientationVectors = 'GlobalNodeId'
analysisexoDisplay.ScaleFactor = 25.50160064697266
analysisexoDisplay.SelectScaleArray = 'GlobalNodeId'
analysisexoDisplay.GlyphType = 'Arrow'
analysisexoDisplay.PolarAxes = 'PolarAxesRepresentation'
analysisexoDisplay.ScalarOpacityUnitDistance = 31.997679787227092
analysisexoDisplay.GaussianRadius = 12.75080032348633
analysisexoDisplay.SetScaleArray = ['POINTS', 'GlobalNodeId']
analysisexoDisplay.ScaleTransferFunction = 'PiecewiseFunction'
analysisexoDisplay.OpacityArray = ['POINTS', 'GlobalNodeId']
analysisexoDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
analysisexoDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
analysisexoDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
analysisexoDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
analysisexoDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# reset view to fit data
renderView1.ResetCamera()

# set scalar coloring
ColorBy(analysisexoDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
analysisexoDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# create a new 'ExodusIIReader'
model_step2exo = ExodusIIReader(FileName=['/home/marmar/scratch/parallelWorks/weldingProject/EWI-Workflow-Scripts-Dec20-2017-orig/tmp/post-process/model_step2.exo'])
model_step2exo.PointVariables = []
model_step2exo.NodeSetArrayStatus = []

# Properties modified on model_step2exo
model_step2exo.PointVariables = ['U', 'NT', 'S', 'PEEQ', 'HFL']
model_step2exo.ElementBlocks = ['PNT', 'C3D20 C3D20R', 'COMPOSITE LAYER C3D20', 'Beam B32 B32R', 'CPS8 CPE8 CAX8 S8 S8R', 'C3D8 C3D8R', 'TRUSS2', 'TRUSS2', 'CPS4R CPE4R S4 S4R', 'CPS4I CPE4I', 'C3D10', 'C3D4', 'C3D15', 'CPS6 CPE6 S6', 'C3D6', 'CPS3 CPE3 S3', '2-node 1d network entry elem', '2-node 1d network exit elem', '2-node 1d genuine network elem']

# show data in view
model_step2exoDisplay = Show(model_step2exo, renderView1)
# trace defaults for the display properties.
model_step2exoDisplay.Representation = 'Surface'
model_step2exoDisplay.ColorArrayName = [None, '']
model_step2exoDisplay.EdgeColor = [0.0, 0.0, 0.0]
model_step2exoDisplay.OSPRayScaleArray = 'GlobalNodeId'
model_step2exoDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
model_step2exoDisplay.SelectOrientationVectors = 'GlobalNodeId'
model_step2exoDisplay.ScaleFactor = 25.50160064697266
model_step2exoDisplay.SelectScaleArray = 'GlobalNodeId'
model_step2exoDisplay.GlyphType = 'Arrow'
model_step2exoDisplay.PolarAxes = 'PolarAxesRepresentation'
model_step2exoDisplay.ScalarOpacityUnitDistance = 30.76129272694989
model_step2exoDisplay.GaussianRadius = 12.75080032348633
model_step2exoDisplay.SetScaleArray = ['POINTS', 'GlobalNodeId']
model_step2exoDisplay.ScaleTransferFunction = 'PiecewiseFunction'
model_step2exoDisplay.OpacityArray = ['POINTS', 'GlobalNodeId']
model_step2exoDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
model_step2exoDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
model_step2exoDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
model_step2exoDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
model_step2exoDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# set scalar coloring
ColorBy(model_step2exoDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
model_step2exoDisplay.SetScalarBarVisibility(renderView1, True)

#################################################333
# Not sure if this is necessary:
#################################################333

# set active source
SetActiveSource(analysisexo)

#################################################333
#################################################333
# destroy analysisexo
# This deletes the source
Delete(analysisexo)
# To fully remove the cone from memory, get rid of the
# variable too
del analysisexo
#################################################333
#################################################333

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [245.96443338734716, 370.95080380773015, 218.3246688545825]
renderView1.CameraFocalPoint = [0.0, 6.349999904632567, -6.349999904632568]
renderView1.CameraViewUp = [-0.07881907478517955, 0.5609805043973737, -0.8240682175257559]
renderView1.CameraParallelScale = 127.82384709638328

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).