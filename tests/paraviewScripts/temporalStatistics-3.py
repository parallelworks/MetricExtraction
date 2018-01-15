#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
extractSelection1 = FindSource('ExtractSelection1')

# set active source
SetActiveSource(extractSelection1)

# find source
exodusIIReader1 = FindSource('ExodusIIReader1')

# set active source
SetActiveSource(exodusIIReader1)

# create a new 'Temporal Statistics'
temporalStatistics1 = TemporalStatistics(Input=exodusIIReader1)

# find source
calculator1 = FindSource('Calculator1')

# find source
selectionQuerySource1 = FindSource('SelectionQuerySource1')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [700, 600]

# show data in view
temporalStatistics1Display = Show(temporalStatistics1, renderView1)
# trace defaults for the display properties.
temporalStatistics1Display.Representation = 'Surface'
temporalStatistics1Display.ColorArrayName = [None, '']
temporalStatistics1Display.EdgeColor = [0.0, 0.0, 0.0]
temporalStatistics1Display.OSPRayScaleArray = 'GlobalNodeId'
temporalStatistics1Display.OSPRayScaleFunction = 'PiecewiseFunction'
temporalStatistics1Display.SelectOrientationVectors = 'GlobalNodeId'
temporalStatistics1Display.SelectScaleArray = 'GlobalNodeId'
temporalStatistics1Display.GlyphType = 'Arrow'
temporalStatistics1Display.PolarAxes = 'PolarAxesRepresentation'
temporalStatistics1Display.ScalarOpacityUnitDistance = 0.671201527582388
temporalStatistics1Display.GaussianRadius = 0.5
temporalStatistics1Display.SetScaleArray = ['POINTS', 'GlobalNodeId']
temporalStatistics1Display.ScaleTransferFunction = 'PiecewiseFunction'
temporalStatistics1Display.OpacityArray = ['POINTS', 'GlobalNodeId']
temporalStatistics1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
temporalStatistics1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
temporalStatistics1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
temporalStatistics1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
temporalStatistics1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# hide data in view
Hide(exodusIIReader1, renderView1)

# find source
descriptiveStatistics1 = FindSource('DescriptiveStatistics1')

# set scalar coloring
ColorBy(temporalStatistics1Display, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
temporalStatistics1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# set scalar coloring
ColorBy(temporalStatistics1Display, ('POINTS', 'HFL_maximum', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
temporalStatistics1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
temporalStatistics1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'HFL_maximum'
hFL_maximumLUT = GetColorTransferFunction('HFL_maximum')

# set scalar coloring
ColorBy(temporalStatistics1Display, ('POINTS', 'HFL_maximum', 'X'))

# rescale color and/or opacity maps used to exactly fit the current data range
temporalStatistics1Display.RescaleTransferFunctionToDataRange(False, False)

# Update a scalar bar component title.
UpdateScalarBarsComponentTitle(hFL_maximumLUT, temporalStatistics1Display)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [14.069362091033526, -9.069362091033524, 18.08642251129768]
renderView1.CameraFocalPoint = [0.0, 5.0, -0.75]
renderView1.CameraViewUp = [-0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 7.088723439378913

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).