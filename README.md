# Introduction
At AgriTech, we are very interested in how water flows through a maize farm field. This knowledge will help us improve our research on new agricultural products being tested on farms.

How much maize a field produces is very spatially variable. Even if the same farming practices, seeds and fertilizer are applied exactly the same by machinery over a field, there can be a very large harvest at one corner and a low harvest at another corner.  We would like to be able to better understand which parts of the farm are likely to produce more or less maize, so that if we try a new fertilizer on part of this farm, we have more confidence that any differences in the maize harvest 9are due mostly to the new fertilizer changes, and not just random effects due to other environmental factors.  

Water is very important for crop growth and health.  We can better predict maize harvest if we better understand how water flows through a field, and which parts are likely to be flooded or too dry. One important ingredient to understanding water flow in a field is by measuring the elevation of the field at many points. The USGS recently released high resolution elevation data as a lidar point cloud called USGS 3DEP in a public dataset on Amazon. This dataset is essential to build models of water flow and predict plant health and maize harvest. 


## Package Installation 

In order to install geolidar, you need to have pip installed and an active virtual environmen

* using pip
```python
pip install geolidar
```

## Usage
### Loading lidar data

Loading geolidar data has been an old age challenge, and we shall be using this tool to load data from the lidar cloud, there are only two things that you need to know over here, first is the state/region variable, and second you need to have your coordinates ready, and the file which you want to save your resulting raster.

```python
from geolidar import loader
from geolidar.mapper import state_mapper_variables

geo_df = loader.load_geolidar(([-10425171.940, -10423171.940], [5164494.710, 5166494.710]),state_mapper_variables.IA_FullState,"../data/iowa")
```