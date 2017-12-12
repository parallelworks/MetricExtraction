#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find view
spreadSheetView1 = FindViewOrCreate('SpreadSheetView1', viewtype='SpreadSheetView')
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# set active view
SetActiveView(spreadSheetView1)

# destroy spreadSheetView1
Delete(spreadSheetView1)
del spreadSheetView1

# find view
spreadSheetView2 = FindViewOrCreate('SpreadSheetView2', viewtype='SpreadSheetView')
# uncomment following to set a specific view size
# spreadSheetView2.ViewSize = [400, 400]

# destroy spreadSheetView2
Delete(spreadSheetView2)
del spreadSheetView2

# get layout
layout2 = GetLayoutByName("Layout #2")

RemoveLayout(layout2)

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).