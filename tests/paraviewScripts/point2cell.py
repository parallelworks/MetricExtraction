#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
ped_000degvtk = FindSource('Ped_000deg.vtk')

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(Input=ped_000degvtk)

# find source
probeLocation2 = FindSource('ProbeLocation2')

# find source
probeLocation1 = FindSource('ProbeLocation1')

# find source
descriptiveStatistics1 = FindSource('DescriptiveStatistics1')

# find source
legacyVTKReader1 = FindSource('LegacyVTKReader1')

# find source
clip1 = FindSource('Clip1')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1022, 542]

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, renderView1)
# trace defaults for the display properties.
cellDatatoPointData1Display.Representation = 'Surface'
cellDatatoPointData1Display.ColorArrayName = [None, '']
cellDatatoPointData1Display.EdgeColor = [0.0, 0.0, 0.0]
cellDatatoPointData1Display.OSPRayScaleArray = 'EVO All Year Afternoon'
cellDatatoPointData1Display.OSPRayScaleFunction = 'PiecewiseFunction'
cellDatatoPointData1Display.SelectOrientationVectors = 'EVO All Year Afternoon'
cellDatatoPointData1Display.ScaleFactor = 29.767999267578126
cellDatatoPointData1Display.SelectScaleArray = 'EVO All Year Afternoon'
cellDatatoPointData1Display.GlyphType = 'Arrow'
cellDatatoPointData1Display.PolarAxes = 'PolarAxesRepresentation'
cellDatatoPointData1Display.GaussianRadius = 14.883999633789063
cellDatatoPointData1Display.SetScaleArray = ['POINTS', 'EVO All Year Afternoon']
cellDatatoPointData1Display.ScaleTransferFunction = 'PiecewiseFunction'
cellDatatoPointData1Display.OpacityArray = ['POINTS', 'EVO All Year Afternoon']
cellDatatoPointData1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
cellDatatoPointData1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
cellDatatoPointData1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
cellDatatoPointData1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
cellDatatoPointData1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# hide data in view
Hide(ped_000degvtk, renderView1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.0, 813.3531507230006]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.07615534774959087]
renderView1.CameraParallelScale = 210.49157534686964

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).