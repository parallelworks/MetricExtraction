#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get color transfer function/color map for 'PLWWinterMorning'
pLWWinterMorningLUT = GetColorTransferFunction('PLWWinterMorning')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1625, 1159]

# get color legend/bar for pLWWinterMorningLUT in view renderView1
pLWWinterMorningLUTColorBar = GetScalarBar(pLWWinterMorningLUT, renderView1)

# Properties modified on pLWWinterMorningLUTColorBar
pLWWinterMorningLUTColorBar.UseCustomLabels = 1
pLWWinterMorningLUTColorBar.CustomLabels = [1.0, 2.0, 3.0, 4.5, 5.0]

# Properties modified on pLWWinterMorningLUTColorBar
pLWWinterMorningLUTColorBar.CustomLabels = [2.0, 3.0, 4.5, 5.0]

# Properties modified on pLWWinterMorningLUTColorBar
pLWWinterMorningLUTColorBar.AddRangeLabels = 0

# change scalar bar placement
pLWWinterMorningLUTColorBar.Orientation = 'Horizontal'
pLWWinterMorningLUTColorBar.Position = [0.3249230769230768, 0.039447799827437444]
pLWWinterMorningLUTColorBar.ScalarBarLength = 0.33000000000000024

# Properties modified on pLWWinterMorningLUT
pLWWinterMorningLUT.Annotations = ['', '']
pLWWinterMorningLUT.IndexedColors = [0.0, 0.0, 0.0]

# Properties modified on pLWWinterMorningLUT
pLWWinterMorningLUT.Annotations = ['2.5', '']

# Properties modified on pLWWinterMorningLUT
pLWWinterMorningLUT.Annotations = ['2.5', 'test']