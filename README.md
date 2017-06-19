Metric Extraction
-----------------

The below describes a json file syntax created to extract field information from simulation domains. It uses the ParaView Python API to extract these metrics in the form of Probes, Lines, Slices, Clips and Volumes.

-   To convert older csv files to json file use convertcsv2json.py. **Note** that the converted json file might need some editing (e.g., type, field and fieldComponent fields).
-   [Hjson](http://hjson.org/) can be used to convert json files to Hjson files (for easier readability) and vice versa

The below parameters need to be specified for each of the desired metrics:

-   **name**: unique metric name
-   **field**: domain field to extract metrics from (must be available in the model).
-   **fieldComponent**: For vector/tensor quantities specify the desired component as fieldComponent. If `fieldComponent` is not given for vector/tensor quantities, the magnitude of the desired quantity will be extracted, i.e., the default is "fieldComponent": "Magnitude"
-   **type**: specifies the type of metric. The types are "Clip", "Line", "Probe", "Slice", "Volume" and "StreamLines". Additional fields for each metric type are listed below.
-   **position**: see below type definition for position description
-   **extractStats**: Set to "false" if quantitative metrics to the csv file (ave,min,max) is not needed (default: "true"). Note that metrics are not extracted for streamlines.

Syntax for extracting various metric types are described below:

-   **Probe**: point extractor in domain
    -   position="x y z"
    -   if "center" is specified in any position, auto calculates focal point of model
-   **Line**:
    -   position="x1 y1 z1 x2 y2 z2" specifies the coordinates of the start point (x1, y1, z1) and end point (x2, y2, z2) of the line segment. If "center" is specified in any position, auto calculates focal point of model.
    -   resolution specifies the number of points/resolution.
-   **Clip**: clip through domain with a plane
    -   plane="x","y" or "z" specifies the direction of the clip plane (normal to the "x","y" or "z" axis)
    -   position="x y z" the coordinate of a point on the clip plane
    -   invert="true" or "false" Optional parameter to invert the clip direction (default: "false")
-   **Slice**: slice through domain with a plane
    -   plane="x","y" or "z" specifies the direction of the clip plane (normal to the "x","y" or "z" axis)
    -   position="x y z" the coordinate of a point on the clip plane
-   **Volume**: box in domain
    -   position="xmin xmax ymin ymax zmin zmax"
-   **StreamLines**: Note that metrics are not extracted for streamlines.
    -   position="x1 y1 z1 x2 y2 z2" specifies the coordinates of the start point (x1, y1, z1) and end point (x2, y2, z2) of the line segment for seeding Stream lines. If "center" is specified in any position, auto calculates focal point of model.
    -   resolution specifies the number of seeds generated on the line.
    -   colorByField: domain field to use for coloring the streamlines. The "Vorticity" vector is also available.
    -   colorByFieldComponent: The component of the vector/tensor fields for coloring the streamlines. If `colorByFieldComponent` is not given for vector/tensor quantities, the magnitude of the desired quantity will be extracted, i.e., the default is "colorByFieldComponent": "Magnitude".
    -   integralDirection: the direction for generating streamlines. The value can be set to "BACKWARD", "FORWARD" or "BOTH".
    -   tubeRadius: The radius of streamlines tubes
    -   maxStreamLength: The maximum length of streamlines.

If an image is desired, define parameters below:

-   **image**: iso, top, bottom, left, right, front, back - Line type can specify "plot" type to plot the line
-   **min**: data range min
-   **max**: data range max
-   **colorscale**: color data by (<https://www.paraview.org/Wiki/Colormaps>)
-   **invertcolor**: invert the color scale - Yes=1, No=0
-   **discretecolors**: discretize the colored data by X number of values
-   **opacity**: opacity of the metric on the image
-   **bodyopacity**: opacity of the base domain (can be used to hide domain)

If animation is desired, define parameters below:

-   **animation**: "true"
-   **image**: iso, top, bottom, left, right, front, back - Line type can specify "plot" type to plot the line
-   **min**: data range min
-   **max**: data range max
-   **colorscale**: color data by Paraview built in color maps (<https://www.paraview.org/Wiki/Colormaps>)
-   **invertcolor**: invert the color scale - Yes=1, No=0
-   **discretecolors**: discretize the colored data by X number of values
-   **opacity**: opacity of the metric on the image
-   **bodyopacity**: opacity of the base domain (can be used to hide domain)

If blender (.x3d) output is desired, add the parameter **blender** and set it to "true".

Example input file:

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
