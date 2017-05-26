
## Metric Extraction

The below describes a csv file syntax created to extract field information from simulation domains. It uses the Paraview Python API to extract these metrics in the form of Probes, Lines, Slices, Clips and Volumes.

<br>
*Define the below parameters for each desired metric to extract:*

* **name**: unique metric name
* **field or field_component**: domain field to extract metrics from (must be available in the model). For vector/tensor quantities specify the desired component as field_componentName, or field_Magnitude.
* **type**: see metric extract types below
* **position**: see below type definition for position description

<br>
*Metric Extraction Types:*

* **Probe**: point sensor in domain
    * position="x y z"
    * if "center" is specified in any position, auto calculates focal point of model
* **Line_\<Res\>**: line in domain as some number of points/resolution
    * position="x1 y1 z1 x2 y2 z2"
    * if "center" is specified in any position, auto calculates focal point of model
* **Slice_\<Plane\>**: slice through domain
    * position="x y z"
    * Plane=X,Y,Z (select one)
* **Clip_\<Plane\>_\<Invert\>**: clip through domain
    * position="x y z" Plane=X,Y,Z (select one)
    * include "Invert" flag to invert the clip direction
* **Volume**: box in domain
    * position="xmin xmax ymin ymax zmin zmax"

<br>
*If an image is desired, define parameters below:*

* **image**: iso, top, bottom, left, right, front, back - Line type can specify "plot" type to plot the line
* **min**: data range min
* **max**: data range max
* **colorscale**: color data by [ParaView built in color maps](http://www.paraview.org/Wiki/images/7/73/Luts.png)
* **invertcolor**: invert the color scale - Yes=1, No=0
* **discretecolors**: discretize the colored data by X number of values
* **opacity**: opacity of the metric on the image
* **bodyopacity**: opacity of the base domain (can be used to hide domain)

<br>
*Example:*

```
name,field,type,position,image,min,max,colorscale,invertcolor,discretecolors,opacity,bodyopacity
lineAoA,AoA,Line_30,0.1 0.15 0.25 3 0.15 0.25,plot
probeT,T,Probe,0.1 0.1 0.1
volU,U,Volume,0.1 3 0.1 2.3 0.15 2.3
slice1,PMV,Slice_Z,center center 0.1,iso,-3,3,Blue to Red Rainbow,0,20,0.7,0.3
```

*Resulting Metric Extractors (note each metric image would be exported seperated):*

![metric](metric_example.png)

![plot](plot_example.png)
