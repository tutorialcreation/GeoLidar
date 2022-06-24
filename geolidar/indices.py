import numpy as np
import math
from shapely.geometry.polygon import Polygon

class Indexer(object):
    def __init__(self) -> None:
        pass

    def wrap(self, deg):
        """
        these wraps around the longitude and latitude
        args:
            deg (int): the latitude/longitude in degrees
        returns:
            deg in integer format
        """
        while deg < -180:
            deg += 360
        while deg > 180:
            deg -= 360
        return deg
    
    def area(self,results):
        """
        calculate the area in square meters given the latitude and longitude
        args:
            results (list): list of tuples in the format (X,Y,Z)
        returns:
            area (float)
        """
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

        ring = geom.exterior.coords

        sumVal = 0
        j = 0
        l = len(ring)
        k = l - 1
        while j < l:
            sumVal += self.wrap(ring[j][0] - ring[k][0]) * (ring[j][1] + ring[k][1])
            k = j
            j += 1

        return (abs(sumVal) / 2) * kx * ky;
    
    def get_topographical_wetness_index(self,results,gdf):
        """
        calculates the topographical wetness index using the log formula
        args:
            result (list): a list of tuples in the format (X,Y,Z)
            gdf (geopandas dataframe): a geopandas dataframe containing latitude, longitude and elevation information
        return:
            gdf (geopandas dataframe): that contains the twi column
        """
        long = [x[0] for x in results]
        lat = [x[1] for x in results]
        x = [(long[i],lat[i])for i in range(len(long))]
        area_poly = self.area(results)
        twindex = []
        for i,_ in enumerate(x):
            slope = np.gradient(x[i])[0]
            twindex.append(np.log(area_poly/math.tan(slope)))

        gdf['twi'] = twindex
        return gdf

indexes = Indexer()
