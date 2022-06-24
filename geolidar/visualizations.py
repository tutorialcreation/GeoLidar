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
        
        args:
            rast_data (np arrray): an array of the raster image
            title (str): the title of the image
            figsize (tuple): scale of the image to be displayed
        
        returns:
            pyplot image
        """
        plt.figure(figsize = figsize)
        im1 = plt.imshow(np.log1p(rast_data),) # vmin=0, vmax=2.1)

        plt.title("{}".format(title), fontdict = {'fontsize': 20})  
        plt.axis('off')
        plt.colorbar(im1, fraction=0.03)

    def show_raster(self, path_to_raster):
        """
        
        displays a raster from a .tif raster file
        
        args:
            path_to_raster (str): path to the raster file
        
        returns:
            rasterio image
        
        """
        src = rasterio.open(path_to_raster)
        fig, (axrgb, axhist) = plt.subplots(1, 2, figsize=(14,7))
        show((src), cmap='Greys_r', contour=True, ax=axrgb)
        show_hist(src, bins=50, histtype='stepfilled',
                lw=0.0, stacked=False, alpha=0.3, ax=axhist)
        plt.show()

    
    def plot_3d_map(results):
        """
        
        plotting of a 3d map
        
        args: 
            results (list): input a python list of tuples in the form of (X,Y,Z)
        
        return:
            3d plot of the input points
        
        """
        # set data        
        X = np.array([x[0] for x in results])
        Y = np.array([x[1] for x in results])
        Z = np.array([x[2] for x in results])

        # plot data
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        fig.set_size_inches(18.5, 10.5, forward=True)
        ax = plt.axes(projection='3d')
        ax.scatter(X, Y, Z, s=0.01,color="green")
        ax.set_xlabel('long')
        ax.set_ylabel('lat')
        ax.set_zlabel('elevation')
        plt.show()

    def plot_2d_heatmap(self,df,column,title):
        """

        plot a 2d heat map of the terrain
        
        args:
            df (geopndas df): a geopandas dataframe demonstrating the data
            column (str): input column to outline in string
            title (str): input title of the map in string
        
        return:
            2d heat map of terrain
        
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        fig.patch.set_alpha(0)
        plt.grid('on', zorder=0)
        df.plot(column=column, ax=ax, legend=True, cmap="terrain")
        plt.title(title)
        plt.xlabel('long')
        plt.ylabel('lat')
        plt.show()
    



visualize = Visualization()