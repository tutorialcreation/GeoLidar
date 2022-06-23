import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.plot import show
import rasterio
from rasterio.plot import show_hist


class Visualization(object):

    def __init__(self) -> None:
        pass

    def plot_raster(self,rast_data, title='', figsize=(10,10)):
        """
        Plots population count in log scale(+1)
        """
        plt.figure(figsize = figsize)
        im1 = plt.imshow(np.log1p(rast_data),) # vmin=0, vmax=2.1)

        plt.title("{}".format(title), fontdict = {'fontsize': 20})  
        plt.axis('off')
        plt.colorbar(im1, fraction=0.03)

    def show_raster(self, path_to_raster):
        src = rasterio.open(path_to_raster)
        fig, (axrgb, axhist) = plt.subplots(1, 2, figsize=(14,7))
        show((src), cmap='Greys_r', contour=True, ax=axrgb)
        show_hist(src, bins=50, histtype='stepfilled',
                lw=0.0, stacked=False, alpha=0.3, ax=axhist)
        plt.show()

    

    
        
        

visualization = Visualization()