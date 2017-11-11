#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
solveexo = FindSource('solve.exo')

# create a new 'Warp By Vector'
warpByVector1 = WarpByVector(Input=solveexo)
warpByVector1.Vectors = ['POINTS', 'HFL']

# Properties modified on warpByVector1
warpByVector1.Vectors = ['POINTS', 'U']
warpByVector1.ScaleFactor = 10.0

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1151, 592]

# show data in view
warpByVector1Display = Show(warpByVector1, renderView1)
# trace defaults for the display properties.
warpByVector1Display.Representation = 'Surface'
warpByVector1Display.ColorArrayName = [None, '']
warpByVector1Display.EdgeColor = [0.0, 0.0, 0.0]
warpByVector1Display.OSPRayScaleArray = 'GlobalNodeId'
warpByVector1Display.OSPRayScaleFunction = 'PiecewiseFunction'
warpByVector1Display.SelectOrientationVectors = 'GlobalNodeId'
warpByVector1Display.ScaleFactor = 1.2023580551147461
warpByVector1Display.SelectScaleArray = 'GlobalNodeId'
warpByVector1Display.GlyphType = 'Arrow'
warpByVector1Display.PolarAxes = 'PolarAxesRepresentation'
warpByVector1Display.ScalarOpacityUnitDistance = 0.6358127008977205
warpByVector1Display.GaussianRadius = 0.6011790275573731
warpByVector1Display.SetScaleArray = ['POINTS', 'GlobalNodeId']
warpByVector1Display.ScaleTransferFunction = 'PiecewiseFunction'
warpByVector1Display.OpacityArray = ['POINTS', 'GlobalNodeId']
warpByVector1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
warpByVector1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
warpByVector1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
warpByVector1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
warpByVector1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# hide data in view
Hide(solveexo, renderView1)

# set scalar coloring
ColorBy(warpByVector1Display, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
warpByVector1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')
vtkBlockColorsLUT.InterpretValuesAsCategories = 1
vtkBlockColorsLUT.Annotations = ['0', '0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '10', '10', '11', '11']
vtkBlockColorsLUT.ActiveAnnotatedValues = ['11']
vtkBlockColorsLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.63, 0.63, 1.0, 0.67, 0.5, 0.33, 1.0, 0.5, 0.75, 0.53, 0.35, 0.7, 1.0, 0.75, 0.5]

# change representation type
warpByVector1Display.SetRepresentationType('Wireframe')

# set active source
SetActiveSource(solveexo)

# show data in view
solveexoDisplay = Show(solveexo, renderView1)
# trace defaults for the display properties.
solveexoDisplay.Representation = 'Surface'
solveexoDisplay.ColorArrayName = ['FIELD', 'vtkBlockColors']
solveexoDisplay.LookupTable = vtkBlockColorsLUT
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

# show color bar/color legend
solveexoDisplay.SetScalarBarVisibility(renderView1, True)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [22.415233146748434, -11.006322516804003, 19.271696361675147]
renderView1.CameraFocalPoint = [2.0000000000000004, -5.527234359715511e-16, -0.2500000447034838]
renderView1.CameraViewUp = [-0.47836820847760725, 0.4501072224497591, 0.7540340479159331]
renderView1.CameraParallelScale = 7.846177408964493

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).