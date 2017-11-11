Metric Extraction
-----------------

The below describes a json file syntax created to extract field information from simulation domains. It uses the ParaView Python API to extract these metrics in the form of Probes, Lines, Slices, Clips and Volumes.

-   To convert older csv files to json file use convertcsv2json.py. **Note** that the converted json file might need some editing (e.g., type, field and fieldComponent fields).
-   [Hjson](http://hjson.org/) can be used to convert json files to Hjson files (for easier readability) and vice versa

The below parameters need to be specified for each of the desired metrics:

-   **name**: Unique metric name
-   **field**: Domain field to extract metrics from (must be available in the model). **For `Basic` metric type, specifying `field` is optional (see below)**
-   **fieldComponent**: For vector/tensor quantities specify the desired component as fieldComponent. If `fieldComponent` is not given for vector/tensor quantities, the magnitude of the desired quantity will be extracted, i.e., the default is "fieldComponent": "Magnitude"
-   **type**: Specifies the type of metric. The types are "Clip", "Line", "Probe", "Slice", "Volume" and "StreamLines". Additional fields for each metric type are listed below.
-   **position**: See below type definition for position description
-   **extractStats**: Set to "false" if quantitative metrics to the csv file (ave,min,max,sd) is not needed (default: "true").

Syntax for extracting various metric types are described below:

-   **Basic**: Show the whole domain.
    -   Specifying the `field` is optional. If `field` is not specified, an image of the solution domain will be produced.
-   **Probe**: point extractor in domain
    -   position="x y z"
    -   if "center" is specified in any position, auto calculates focal point of model
-   **Line**:
    -   position="x1 y1 z1 x2 y2 z2" specifies the coordinates of the start point (x1, y1, z1) and end point (x2, y2, z2) of the line segment. If "center" is specified in any position, auto calculates focal point of model.
    -   resolution specifies the number of points/resolution.
    -   **Note** : To plot the line using the "plot" option (see notes below under image or animation) relies on `matplotlib.pyplot` which depends on `python-dateutil`. Loading `matplotlib.pyplot` in `pvpython` raises an error due to this unresolved dependency. To solve this problem install the `python-dateutil` module in the Python `site-packages` directory of Python2.7 that comes with Python.

        ``` example
        pip2 install --target=/ParaviewDirectory/ParaView-5.3.0-Qt5-OpenGL2-MPI-Linux-64bit/lib/python2.7/site-packages python-dateutil
        ```

        This step is not needed if instead of `pvpython` you are running the `extract.py` script using `python2` and setting `PYTHONPATH` to point to where `paraview.simple` modules are.

-   **Clip**: clip through domain with a plane
    -   plane="x","y" or "z" specifies the direction of the clip plane (normal to the "x","y" or "z" axis)
    -   position="x y z" the coordinate of a point on the clip plane
    -   invert="true" or "false" Optional parameter to invert the clip direction (default: "false")
-   **Slice**: slice through domain with a plane
    -   plane="x","y" or "z" specifies the direction of the clip plane (normal to the "x","y" or "z" axis)
    -   position="x y z" the coordinate of a point on the clip plane
-   **Volume**: box in domain
    -   position="xmin xmax ymin ymax zmin zmax"
-   **StreamLines**:
    -   seedType="line" (default) or "plane" specifies the seed type. If seed type is set to "plane", the "plane" and "center" options also need to be provided. See `sample_inputs/cyclone_streamLine.json` for an example.
    -   position:
        -   For "line" seed type position specifies the coordinates of the start point (x1, y1, z1) and end point (x2, y2, z2) of the line segment for seeding Stream lines. The format is "x1 y1 z1 x2 y2 z2" If "center" is specified in any position, auto calculates focal point of model.
        -   For "plane" seed type position specifies the coordinates of the bounding box of the planar section for seeding the points. The format is "x1 x2 y1 y2 z1 z2".
    -   "plane": "x","y" or "z". This option is only required for "plane" seed types to specify the direction of the seed plane (normal to the "x","y" or "z" axis).
    -   "center": "x y z". This option is only required for "plane" seed types the coordinate of a point on the seed plane.
    -   resolution specifies the number of seeds generated on the line.
    -   colorByField: domain field to use for coloring the streamlines. The "Vorticity" vector is also available.
    -   colorByFieldComponent: The component of the vector/tensor fields for coloring the streamlines. If `colorByFieldComponent` is not given for vector/tensor quantities, the magnitude of the desired quantity will be extracted, i.e., the default is "colorByFieldComponent": "Magnitude".
    -   integralDirection: the direction for generating streamlines. The value can be set to "BACKWARD", "FORWARD" or "BOTH".
    -   tubeRadius: The radius of streamlines tubes
    -   maxStreamLength: The maximum length of streamlines.
-   **WarpByVector**:
    -   scaleFactor: specifies the scaling factor for the warp (each component of the selected vector, specified by "field", will be multiplied by the value of this property before being used to compute new point coordinates). default: 1.0
    -   colorByField: domain field to use for coloring the warped shape. Default is set to "field"
    -   colorByFieldComponent: The component of the vector/tensor fields for coloring the warped shape. If `colorByFieldComponent` is not given for vector/tensor quantities, the magnitude of the desired quantity will be extracted, i.e., the default is "colorByFieldComponent": "Magnitude".
    -   "extractStats" is set to "false" for this type.

If an image is desired, define parameters below:

-   **image**: iso, iso-flipped, top (or "+z"), bottom (or "+z"), left (or "-y"), right (or "+y"), front (or "+x"), back (or "-x") - Line type can specify "plot" type to plot the line. To set a view to a customized view set image to "customize" and provide the following properties (see `sample_inputs/elbowKPI.json` for an example)
    -   **CameraPosition** = "x y z"
    -   **CameraFocalPoint** = "x y z"
    -   **CameraViewUp** = "v1 v2 v3"
    -   **CameraParallelScale** = scale value (double number)
    -   **CameraParallelProjection** = 1 or 0

    You can find the above camera properties for your desired view from the "Adjust Camera" window in Paraview, or via starting a trace.
-   **imageName** : This field specifies the image name format. A number can be specified by using Python formatting (using new style, see [see <https://pyformat.info/#number>](https://pyformat.info/#number)). For example,

    ``` example
    "imageName": "domainImage_{:03d}.tif"
    ```

    and running `extract.py` by providing the `caseNumber` of "1" and outputDirectory (`<outputDir>`) of `example_outputs/` results in

    ``` example
    example_outputs/domainImage_001.tif
    ```

    The default image name is `plot_<kpiName>.png` for line plots and `out_<kpiName>.png` for all other image types, where `<kpiName>` is the title of the metrics entery in the kpi.json file.

-   **min**: Minimum value for customizing/rescaling the data range (default: "auto")
-   **max**: Maximum value for customizing/rescaling the data range (default: "auto")
-   **colorscale**: color data by (see <https://www.paraview.org/Wiki/Colormaps>) (default: "Blue to Red Rainbow")
-   **invertcolor**: invert the color scale - true/false (default: "false")
-   **discretecolors**: discretize the colored data by X number of values (default: "20")
-   **opacity**: opacity of the metric on the image (default: "1")
-   **bodyopacity**: opacity of the base domain (can be used to hide domain, default: "0.3")
-   The following parameters for specifying color bar properties are optional and overwrite the default Paraview settings if provided (see `sample_inputs/elbowKPI.json` for an example):
    -   **barTitle** color bar title (LaTeX expressions can also be specified)
    -   **ComponentTitle**
    -   **FontColor** RGB color values. For example for white color specify set to "1 1 1"
    -   **FontSize**
    -   **LabelFormat** format for displaying the color bar numbers, e.g. "%4.3g"
-   **representationType**: Set the representation type to "Surface With Edges", "3D Glyphs", "Outline", "Point Gaussian", "Points", "Surface" or "Wireframe" (default: "Surface")

If animation is desired, define parameters below:

-   **animation**: "true"
-   **animationName** : This field specifies the animation name format. For detailes see the `imageName` entry above. The default image name is `out_<kpiName>.gif` where `<kpiName>` is the title of the metrics entery in the kpi.json file.

-   **image**, **min**, **max**, **colorscale**, **invertcolor**, **discretecolors**, **opacity**, **bodyopacity** and the parameters for specifying color bar properties are the same as parameters in the image section described above.

If blender (.x3d) output is desired, add the parameter **blender** and set it to "true".

### Examples

1.  Example input file for a 2D OpenFOAM case:

    ``` example
     {
      "lateral_area": {
        "IsParaviewMetric": "False",
        "outputName": "lateral_area",
        "outputFileNameTemplate": "../example_inputs/pyCone/results/case_@@i@@/volAndLat.txt",
        "outputFlag": "",
        "delimitor": " ",
        "locationInFile": "0"
      },
      "domainImage": {
        "image": "iso",
        "imageName": "domainImage_{:03d}.tif",
        "type": "Basic"
      },
      "domainUx": {
        "image": "iso-flipped",
        "type": "Basic",
        "field": "U",
        "fieldComponent": "X",
        "animation": "false"
      },
      "ClipUx": {
        "image": "top",
        "field": "U",
        "fieldComponent": "X",
        "position": "10.0  center center",
        "type": "Clip",
        "plane": "X",
        "invert": "true",
        "animation": "false"
      },
      "ClipUMag": {
        "opacity": "1",
        "invertcolor": "0",
        "min": "0",
        "max": "5",
        "image": "top",
        "colorscale": "Blue to Red Rainbow",
        "field": "U",
        "discretecolors": "20",
        "bodyopacity": "0.3",
        "position": "10.0  center center",
        "type": "Clip",
        "plane": "X",
        "invert": "true",
        "animation": "false"
      },
      "sliceUy": {
        "min": "0",
        "max": "4",
        "image": "iso",
        "field": "U",
        "fieldComponent": "Y",
        "position": "center center 0.0",
        "type": "Slice",
        "plane": "Z",
        "animation": "true",
        "animationName": "sliceUy_{:03d}.gif"
      },
      "streamlinesU": {
        "min": "0",
        "max": "2",
        "image": "iso",
        "field": "U",
        "colorByField": "Vorticity",
        "position": "49 62 0 63 62 0",
        "resolution": "10",
        "integralDirection": "BOTH",
        "tubeRadius": "0.2",
        "maxStreamLength": "200",
        "type": "StreamLines",
        "animation": "false",
        "blender": "true"
      },
      "lineUX": {
        "field": "U",
        "fieldComponent": "X",
        "image": "plot",
        "imageName": "out_lineUX_{:03d}.png",
        "type": "Line",
        "resolution": "20",
        "position": "56.0 0.0 0.0 56.0 63.0 0.0"
      },
      "lineP": {
        "field": "p",
        "image": "plot",
        "type": "Line",
        "resolution": "20",
        "position": "56.0 0.0 0.0 56.0 63.0 0.0"
      },
      "volP": {
        "field": "p",
        "type": "Volume",
        "position": "0 16 0 10 -1 1"
      },
      "probeUMagInlet2": {
        "field": "U",
        "type": "Probe",
        "position": "55.0 -3.0 0.0"
      }
    }
    ```

    *Resulting Metric Extractors (note each metric image would be exported separated):*

    ``` example
    metric,ave,min,max,sd
    streamlinesU,1.73188946356,0.710367083286,3.69218988141,0.635220923041
    ClipUx,0.992267233133,0.904910504818,1.02992999554,0.0319378362206
    probeUMagInlet2,3.0086772142,3.0086772142,3.0086772142,0.0
    sliceUy,1.19485028159,-0.0207589007914,3.59215664864,1.03264910435
    lineP,-0.064734678017,-1.81362962723,0.670571267605,0.485642629183
    lineUX,0.193437837818,-0.0237964838743,1.19363594055,0.409159530416
    volP,0.184043353551,0.167160287499,0.207056492567,0.00964242385178
    ClipUMag,0.992305293513,0.904976784638,1.02993442861,0.0319362034963
    domainUx,0.502238381525,-0.0763277485967,1.25048196316,0.443963090027
    ```

    [example\_outputs/openFOAM/domainImage\_001.tif](example_outputs/openFOAM/domainImage_001.tif) ![](example_outputs/openFOAM/out_streamlinesU.png) ![](example_outputs/openFOAM/out_ClipUx.png) ![](example_outputs/openFOAM/out_sliceUy.png) ![](example_outputs/openFOAM/sliceUy_001.gif) ![](example_outputs/openFOAM/out_ClipUMag.png) ![](example_outputs/openFOAM/out_domainUx.png)

    ![](example_outputs/openFOAM/plot_lineP.png) ![](example_outputs/openFOAM/out_lineUX_001.png)

2.  Example for exo metrics

    ``` example
    {
     "sliceNT": {
         "opacity": "0.7",
         "invertcolor": "0",
         "min": "25",
         "max": "93",
         "image": "iso",
         "colorscale": "Blue to Red Rainbow",
         "field": "NT",
         "discretecolors": "20",
         "bodyopacity": "0.3",
         "position": "center center -0.1",
         "type": "Slice",
         "plane": "Z"
     },
     "clipHFLX": {
         "opacity": "0.9",
         "invertcolor": "0",
         "min": "-1200",
         "max": "1700",
         "image": "iso",
         "colorscale": "Blue to Red Rainbow",
         "field": "HFL",
         "fieldComponent": "X",
         "discretecolors": "20",
         "bodyopacity": "0.3",
         "position": "center center -0.1",
         "type": "Clip",
         "plane": "Y",
         "invert": "false"
     },
     "lineS_XY": {
         "field": "S",
         "fieldComponent": "XY",
         "image": "plot",
         "type": "Line",
         "resolution": "20",
         "position": "0.0 -5.0 0.0 0.0 5.0 0.0"
     },
     "volHFLX": {
         "field": "HFL",
         "fieldComponent": "X",
         "type": "Volume",
         "position": "-2 3 -3 -.5 -.1 4"
     },
     "probeUMag": {
         "field": "U",
         "fieldComponent": "Magnitude",
         "type": "Probe",
         "position": "0.0 -5.0 0.0 "
     },
     "streamlinesU": {
         "opacity": "1",
         "invertcolor": "0",
         "min": "0",
         "max": "2",
         "image": "iso",
         "colorscale": "Blue to Red Rainbow",
         "field": "U",
         "colorByField": "Vorticity",
         "colorByFieldComponent": "Magnitude",
         "position":"49 62 0 63 62 0",
         "resolution":"10",
         "integralDirection":"BOTH",
         "discretecolors": "20",
         "tubeRadius":"0.2",
         "maxStreamLength":"200",
         "bodyopacity": "0.3",
         "type": "StreamLines",
         "animation": "false",
         "blender": "true",
         "extractStats":"false"
     }
    }
    ```

    *Resulting Metric Extractors (note each metric image would be exported separated):*

    ``` example
    metric,ave,min,max
    clipHFLX,50.7735883413,-1197.1640625,1798.11987305
    sliceNT,37.9704219826,25.7895435332,92.364784976
    probeUMag,0.00099704706,0.00099704706,0.00099704706
    volHFLX,273.432022586,-435.622624107,1309.98065054
    lineS_XY,-0.0600564658676,-5.07893304083,4.4496566424
    ```

    ![Metric example](example_outputs/metric_example_json.png)

    ![Plot example](example_outputs/plot_example_json.png)
