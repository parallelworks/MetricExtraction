#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get color transfer function/color map for 'SHFSummerAllDay'
sHFSummerAllDayLUT = GetColorTransferFunction('SHFSummerAllDay')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1401, 862]

# get color legend/bar for sHFSummerAllDayLUT in view renderView1
sHFSummerAllDayLUTColorBar = GetScalarBar(sHFSummerAllDayLUT, renderView1)

# Properties modified on sHFSummerAllDayLUTColorBar
sHFSummerAllDayLUTColorBar.NumberOfLabels = 11

# Properties modified on sHFSummerAllDayLUTColorBar
sHFSummerAllDayLUTColorBar.RangeLabelFormat = '%-#6.3g'

# Properties modified on sHFSummerAllDayLUTColorBar
sHFSummerAllDayLUTColorBar.DrawTickMarks = 1


# Properties modified on sHFSummerAllDayLUTColorBar
sHFSummerAllDayLUTColorBar.DrawSubTickMarks = 0

# Properties modified on sHFSummerAllDayLUTColorBar
sHFSummerAllDayLUTColorBar.TitleJustification = 'Right'

# Properties modified on sHFSummerAllDayLUT
sHFSummerAllDayLUT.ColorSpace = 'Diverging'

# Properties modified on sHFSummerAllDayLUT
sHFSummerAllDayLUT.Annotations = ['', '']
sHFSummerAllDayLUT.IndexedColors = [0.0, 0.0, 0.0]

# Properties modified on sHFSummerAllDayLUT
sHFSummerAllDayLUT.Annotations = ['0.55', 'test', '.75', 'test2']

# Properties modified on sHFSummerAllDayLUTColorBar
sHFSummerAllDayLUTColorBar.DrawAnnotations = 1

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [143.5566157750024, 155.92819073101654, 813.2285174478097]
renderView1.CameraFocalPoint = [150.00021314620972, 150.00021314620972, -4.999999873689376e-05]
renderView1.CameraViewUp = [5.775251395803652e-05, 0.9999734347879724, -0.007288784740408994]
renderView1.CameraParallelScale = 210.49124001035213
renderView1.CameraParallelProjection = 1

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
