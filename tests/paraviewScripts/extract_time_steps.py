#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
model_step2exo = FindSource('model_step2.exo')

# set active source
SetActiveSource(model_step2exo)

# get color transfer function/color map for 'NT'
nTLUT = GetColorTransferFunction('NT')

# find source
temporalStatistics1 = FindSource('TemporalStatistics1')

# set active source
SetActiveSource(temporalStatistics1)

# get color transfer function/color map for 'NT_minimum'
nT_minimumLUT = GetColorTransferFunction('NT_minimum')

# set active source
SetActiveSource(model_step2exo)

# create a new 'Extract Time Steps'
extractTimeSteps2 = ExtractTimeSteps(Input=model_step2exo)
extractTimeSteps2.TimeStepIndices = [0]

# find source
extractTimeSteps1 = FindSource('ExtractTimeSteps1')

# Properties modified on extractTimeSteps2
extractTimeSteps2.TimeStepIndices = [0, 3, 7, 11, 15]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1113, 542]

# show data in view
extractTimeSteps2Display = Show(extractTimeSteps2, renderView1)
# trace defaults for the display properties.
extractTimeSteps2Display.Representation = 'Surface'
extractTimeSteps2Display.ColorArrayName = ['POINTS', 'NT']
extractTimeSteps2Display.LookupTable = nTLUT
extractTimeSteps2Display.EdgeColor = [0.0, 0.0, 0.0]
extractTimeSteps2Display.OSPRayScaleArray = 'GlobalNodeId'
extractTimeSteps2Display.OSPRayScaleFunction = 'PiecewiseFunction'
extractTimeSteps2Display.SelectOrientationVectors = 'GlobalNodeId'
extractTimeSteps2Display.ScaleFactor = 25.50160064697266
extractTimeSteps2Display.SelectScaleArray = 'GlobalNodeId'
extractTimeSteps2Display.GlyphType = 'Arrow'
extractTimeSteps2Display.PolarAxes = 'PolarAxesRepresentation'
extractTimeSteps2Display.ScalarOpacityUnitDistance = 30.76129272694989
extractTimeSteps2Display.GaussianRadius = 12.75080032348633
extractTimeSteps2Display.SetScaleArray = ['POINTS', 'GlobalNodeId']
extractTimeSteps2Display.ScaleTransferFunction = 'PiecewiseFunction'
extractTimeSteps2Display.OpacityArray = ['POINTS', 'GlobalNodeId']
extractTimeSteps2Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
extractTimeSteps2Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
extractTimeSteps2Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
extractTimeSteps2Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
extractTimeSteps2Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# hide data in view
Hide(model_step2exo, renderView1)

# show color bar/color legend
extractTimeSteps2Display.SetScalarBarVisibility(renderView1, True)

# find source
temporalStatistics2 = FindSource('TemporalStatistics2')

# Rescale transfer function
nT_minimumLUT.RescaleTransferFunction(0.100484780967, 22.0666160583)

# get opacity transfer function/opacity map for 'NT_minimum'
nT_minimumPWF = GetOpacityTransferFunction('NT_minimum')

# Rescale transfer function
nT_minimumPWF.RescaleTransferFunction(0.100484780967, 22.0666160583)

# create a new 'Temporal Statistics'
temporalStatistics3 = TemporalStatistics(Input=extractTimeSteps2)

# show data in view
temporalStatistics3Display = Show(temporalStatistics3, renderView1)
# trace defaults for the display properties.
temporalStatistics3Display.Representation = 'Surface'
temporalStatistics3Display.ColorArrayName = [None, '']
temporalStatistics3Display.EdgeColor = [0.0, 0.0, 0.0]
temporalStatistics3Display.OSPRayScaleArray = 'GlobalNodeId'
temporalStatistics3Display.OSPRayScaleFunction = 'PiecewiseFunction'
temporalStatistics3Display.SelectOrientationVectors = 'GlobalNodeId'
temporalStatistics3Display.ScaleFactor = 25.50160064697266
temporalStatistics3Display.SelectScaleArray = 'GlobalNodeId'
temporalStatistics3Display.GlyphType = 'Arrow'
temporalStatistics3Display.PolarAxes = 'PolarAxesRepresentation'
temporalStatistics3Display.ScalarOpacityUnitDistance = 30.76129272694989
temporalStatistics3Display.GaussianRadius = 12.75080032348633
temporalStatistics3Display.SetScaleArray = ['POINTS', 'GlobalNodeId']
temporalStatistics3Display.ScaleTransferFunction = 'PiecewiseFunction'
temporalStatistics3Display.OpacityArray = ['POINTS', 'GlobalNodeId']
temporalStatistics3Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
temporalStatistics3Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
temporalStatistics3Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
temporalStatistics3Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
temporalStatistics3Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# hide data in view
Hide(extractTimeSteps2, renderView1)

# set scalar coloring
ColorBy(temporalStatistics3Display, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
temporalStatistics3Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')