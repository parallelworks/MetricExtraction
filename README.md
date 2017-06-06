Metric Extraction
-----------------

The below describes a json file syntax created to extract field information from simulation domains. It uses the ParaView Python API to extract these metrics in the form of Probes, Lines, Slices, Clips and Volumes.

-   To convert older csv files to json file use convertcsv2json.py. **Note** that the converted json file might need some editing (e.g., type, field and fieldComponent fields).
-   [Hjson](http://hjson.org/) can be used to convert json files to Hjson files (for easier readability) and vice versa

The below parameters need to be specified for each of the desired metrics:

-   **name**: unique metric name
-   **field**: domain field to extract metrics from (must be available in the model).
-   **fieldComponent**: For vector/tensor quantities specify the desired component as fieldComponent. If `fieldComponent` is not given for vector/tensor quantities, the magnitude of the desired quantity will be extracted, i.e., the default is "fieldComponent": "Magnitude"
-   **type**: specifies the type of metric. The types are "Clip", "Line", "Probe", "Slice" and "Volume". Additional fields for each metric type are listed below.
-   **position**: see below type definition for position description

Syntax for extracting various metric types are described below:

-   **Probe**: point extractor in domain
    -   position="x y z"
    -   if "center" is specified in any position, auto calculates focal point of model
-   **Line**:
    -   position="x1 y1 z1 x2 y2 z2" If "center" is specified in any position, auto calculates focal point of model
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
