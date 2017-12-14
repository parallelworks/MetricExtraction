import pvutils
import data_IO

#def extractStats(dataSource, kpi, metrichash, fp_csv_metrics):

dataSource = d

# Get view before adding the spreadsheets to get back to it afterwards.
camera = GetActiveCamera()
renderView1 = GetActiveViewOrCreate('RenderView')

# If kpifield is a vector, add a calculator on top and extract the component of the vector
# as a scalar. Also, add a calculator for scalar data since this resolves a ParaView
# bug/problem with extracting data directly from exo files

kpifield = metrichash['field']
kpiComp = metrichash['fieldComponent']

arrayInfo = dataSource.PointData[kpifield]

# create a new 'Calculator'
if pvutils.isfldScalar(arrayInfo):
    statVarName = kpifield
else:
    statVarName = kpifield + '_' + kpiComp
calc1 = Calculator(Input=dataSource)
calc1.ResultArrayName = statVarName
if kpiComp == 'Magnitude':
    calc1.Function = 'mag(' + kpifield + ')'
else:
    calc1.Function = calc1.ResultArrayName
UpdatePipeline()
dataSource = calc1

# create a new 'Descriptive Statistics'
dStats = DescriptiveStatistics(Input=dataSource, ModelInput=None)

dStats.VariablesofInterest = [statVarName]

########################################################
# Add another layout for viewing the spreadsheets. This is for updating the results
# when switching to different time points at the end.

CreateLayout('Layout #2')
SetActiveView(None)
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024L
layout2 = GetLayout()
layout2.AssignView(0, spreadSheetView1)
dStatsDisplay = Show(dStats, spreadSheetView1)
spreadSheetView2 = CreateView('SpreadSheetView')
spreadSheetView2.ColumnToSort = ''
spreadSheetView2.BlockSize = 1024L
layout2.AssignView(2, spreadSheetView2)
dStatsDisplay_1 = Show(OutputPort(dStats, 1), spreadSheetView2)
SetActiveView(spreadSheetView1)
SetActiveSource(dStats)
########################################################

UpdatePipeline()

dStatsDataInfo = dStats.GetDataInformation()

Times = pvutils.getTimeSteps()
print(Times)
if ("extractStatsTimeSteps" in metrichash):
    Times = pvutils.getTimeStepsSubSet(Times, metrichash["extractStatsTimeSteps"])
    print(Times)
else:
    try:
        Times = data_IO.str2numList(metrichash["extractStatsTimes"])
    except ValueError:
        Times = pvutils.getTimeStepsSubSet(Times, metrichash["extractStatsTimes"])

print(Times)

anim = GetAnimationScene()
anim.PlayMode = 'Real Time'

t =  Times[0]
print(t)
anim.AnimationTime = t
RenderAllViews()
UpdatePipeline()

dStatsDataInfo = dStats.GetDataInformation()
dStatsStatsInfo = dStatsDataInfo.GetRowDataInformation()
numStats = dStatsDataInfo.GetRowDataInformation().GetNumberOfArrays()
statTag = kpi
pvutils.writeCurrentStepStats(numStats, dStatsStatsInfo, fp_csv_metrics, statTag, t)

    ########################################################
    # Set view back to the last view

    # SetActiveView(renderView1)
    # renderView1 = setFrame2latestTime(renderView1)
    # Delete the second layout after writing all the statistics
    # Delete(spreadSheetView1)
    # del spreadSheetView1
    # Delete(spreadSheetView2)
    # del spreadSheetView2
    # # get layout
    # RemoveLayout(layout2)
