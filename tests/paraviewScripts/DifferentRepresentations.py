#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
exodusIIReader1 = GetActiveSource()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [700, 600]

# get display properties
exodusIIReader1Display = GetDisplayProperties(exodusIIReader1, view=renderView1)

# change representation type
exodusIIReader1Display.SetRepresentationType('Surface With Edges')

# change representation type
exodusIIReader1Display.SetRepresentationType('3D Glyphs')

# change representation type
exodusIIReader1Display.SetRepresentationType('Outline')

# change representation type
exodusIIReader1Display.SetRepresentationType('Point Gaussian')

# change representation type
exodusIIReader1Display.SetRepresentationType('Points')

# change representation type
exodusIIReader1Display.SetRepresentationType('Surface')

# set scalar coloring
ColorBy(exodusIIReader1Display, ('POINTS', 'GlobalNodeId'))

# rescale color and/or opacity maps used to include current data range
exodusIIReader1Display.RescaleTransferFunctionToDataRange(True, True)

# change representation type
exodusIIReader1Display.SetRepresentationType('Volume')

# get color transfer function/color map for 'GlobalNodeId'
globalNodeIdLUT = GetColorTransferFunction('GlobalNodeId')

# change representation type
exodusIIReader1Display.SetRepresentationType('Wireframe')