#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
selectionQuerySource1 = FindSource('SelectionQuerySource1')

# set active source
SetActiveSource(selectionQuerySource1)

# find source
calculator1 = FindSource('Calculator1')

# set active source
SetActiveSource(calculator1)

# create a new 'Temporal Statistics'
temporalStatistics1 = TemporalStatistics(Input=calculator1)

# find source
extractSelection1 = FindSource('ExtractSelection1')

# find source
exodusIIReader1 = FindSource('ExodusIIReader1')

# find source
descriptiveStatistics1 = FindSource('DescriptiveStatistics1')

# Properties modified on temporalStatistics1
temporalStatistics1.ComputeAverage = 0

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
temporalStatistics1Display.ScaleFactor = 13.257200622558594
temporalStatistics1Display.SelectScaleArray = 'GlobalNodeId'
temporalStatistics1Display.GlyphType = 'Arrow'
temporalStatistics1Display.PolarAxes = 'PolarAxesRepresentation'
temporalStatistics1Display.ScalarOpacityUnitDistance = 18.00282692288048
temporalStatistics1Display.GaussianRadius = 6.628600311279297
temporalStatistics1Display.SetScaleArray = ['POINTS', 'GlobalNodeId']
temporalStatistics1Display.ScaleTransferFunction = 'PiecewiseFunction'
temporalStatistics1Display.OpacityArray = ['POINTS', 'GlobalNodeId']
temporalStatistics1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
temporalStatistics1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
temporalStatistics1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
temporalStatistics1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
temporalStatistics1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# set scalar coloring
ColorBy(temporalStatistics1Display, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
temporalStatistics1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# set scalar coloring
ColorBy(temporalStatistics1Display, ('POINTS', 'NT_s_maximum'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
temporalStatistics1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
temporalStatistics1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'NT_s_maximum'
nT_s_maximumLUT = GetColorTransferFunction('NT_s_maximum')

# rescale color and/or opacity maps used to exactly fit the current data range
temporalStatistics1Display.RescaleTransferFunctionToDataRange(False, True)

# get color legend/bar for nT_s_maximumLUT in view renderView1
nT_s_maximumLUTColorBar = GetScalarBar(nT_s_maximumLUT, renderView1)

# change scalar bar placement
nT_s_maximumLUTColorBar.Orientation = 'Horizontal'
nT_s_maximumLUTColorBar.Position = [0.4564285714285715, 0.7733333333333334]
nT_s_maximumLUTColorBar.Position2 = [0.4299999999999998, 0.1200000000000001]

CreateLayout('Layout #2')

# set active view
SetActiveView(None)

# set active source
SetActiveSource(temporalStatistics1)

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [1735, 862]
renderView2.AnnotationColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.OrientationAxesLabelColor = [0.0, 0.0, 0.0]
renderView2.StereoType = 0
renderView2.Background = [1.0, 1.0, 1.0]

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView2.AxesGrid.XTitleColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.YTitleColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.XLabelColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.YLabelColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

# get layout
layout2 = GetLayout()

# place view in the layout
layout2.AssignView(0, renderView2)

# show data in view
temporalStatistics1Display_1 = Show(temporalStatistics1, renderView2)
# trace defaults for the display properties.
temporalStatistics1Display_1.Representation = 'Surface'
temporalStatistics1Display_1.ColorArrayName = [None, '']
temporalStatistics1Display_1.EdgeColor = [0.0, 0.0, 0.0]
temporalStatistics1Display_1.OSPRayScaleArray = 'GlobalNodeId'
temporalStatistics1Display_1.OSPRayScaleFunction = 'PiecewiseFunction'
temporalStatistics1Display_1.SelectOrientationVectors = 'GlobalNodeId'
temporalStatistics1Display_1.ScaleFactor = 13.257200622558594
temporalStatistics1Display_1.SelectScaleArray = 'GlobalNodeId'
temporalStatistics1Display_1.GlyphType = 'Arrow'
temporalStatistics1Display_1.PolarAxes = 'PolarAxesRepresentation'
temporalStatistics1Display_1.ScalarOpacityUnitDistance = 18.00282692288048
temporalStatistics1Display_1.GaussianRadius = 6.628600311279297
temporalStatistics1Display_1.SetScaleArray = ['POINTS', 'GlobalNodeId']
temporalStatistics1Display_1.ScaleTransferFunction = 'PiecewiseFunction'
temporalStatistics1Display_1.OpacityArray = ['POINTS', 'GlobalNodeId']
temporalStatistics1Display_1.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
temporalStatistics1Display_1.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
temporalStatistics1Display_1.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
temporalStatistics1Display_1.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
temporalStatistics1Display_1.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# reset view to fit data
renderView2.ResetCamera()

# set scalar coloring
ColorBy(temporalStatistics1Display_1, ('POINTS', 'NT_s_maximum'))

# rescale color and/or opacity maps used to include current data range
temporalStatistics1Display_1.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
temporalStatistics1Display_1.SetScalarBarVisibility(renderView2, True)

# rescale color and/or opacity maps used to exactly fit the current data range
temporalStatistics1Display_1.RescaleTransferFunctionToDataRange(False, True)

# set scalar coloring
ColorBy(temporalStatistics1Display_1, ('POINTS', 'NT_s_minimum'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(nT_s_maximumLUT, renderView2)

# rescale color and/or opacity maps used to include current data range
temporalStatistics1Display_1.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
temporalStatistics1Display_1.SetScalarBarVisibility(renderView2, True)

# get color transfer function/color map for 'NT_s_minimum'
nT_s_minimumLUT = GetColorTransferFunction('NT_s_minimum')

# rescale color and/or opacity maps used to exactly fit the current data range
temporalStatistics1Display_1.RescaleTransferFunctionToDataRange(False, True)

#### saving camera placements for all active views

# current camera placement for renderView2
renderView2.CameraPosition = [-196.0573517506465, -243.06678131138762, 183.58772460422358]
renderView2.CameraViewUp = [-0.33473749520235646, 0.7248108613608649, 0.6021627890852884]
renderView2.CameraParallelScale = 93.75696169544071

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [553.8958133549971, -553.895813354997, 782.0163112165337]
renderView1.CameraFocalPoint = [0.0, 0.0, -0.25]
renderView1.CameraViewUp = [-0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 236.7962452180346

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).