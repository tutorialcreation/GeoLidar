import numpy as np
import geopandas as gpd
import pandas as pd
from scipy.interpolate import griddata
import math
import pyproj    
import shapely
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
from functools import partial

class Indexer(object):
    def __init__(self) -> None:
        pass

    def wrap(deg):
        while deg < -180:
            deg += 360
        while deg > 180:
            deg -= 360
        return deg
    
    def area(self,results):
        ## Setup from:
        ## https://github.com/mapbox/cheap-ruler/blob/48ad4768a52dc176b01494d090cce19f02c7afdd/index.js#L71-L82
        long = [x[0] for x in results]
        lat = [x[1] for x in results]
        x = [(long[i],lat[i])for i in range(len(long))]
        geom = Polygon(x)
        
        RE = 6378.137
        RAD = math.pi / 180
        FE = 1 / 298.257223563
        E2 = FE * (2 - FE)

        lat = geom.centroid.y
        m = RAD * RE * 1000
        coslat = math.cos(lat * RAD);

        w2 = 1 / (1 - E2 * (1 - coslat * coslat))
        w = math.sqrt(w2)
        kx = m * w * coslat
        ky = m * w * w2 * (1 - E2)

        ## Area calc from:
        ## https://github.com/mapbox/cheap-ruler/blob/48ad4768a52dc176b01494d090cce19f02c7afdd/index.js#L185-L197
        ring = geom.exterior.coords

        sumVal = 0
        j = 0
        l = len(ring)
        k = l - 1
        while j < l:
            sumVal += wrap(ring[j][0] - ring[k][0]) * (ring[j][1] + ring[k][1])
            k = j
            j += 1

        return (abs(sumVal) / 2) * kx * ky;
    
    def get_topographical_wetness_index(self,results,gdf):
        long = [x[0] for x in results]
        lat = [x[1] for x in results]
        x = [(long[i],lat[i])for i in range(len(long))]
        area_poly = self.area(results)
        twindex = []
        for i in x:
            slope = np.gradient(x[0])[0]
            twindex.append(np.log(area_poly/math.tan(slope)))

        gdf['twi'] = twindex
        return gdf

indexes = Indexer()
