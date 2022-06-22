import geopandas as gpd
import laspy
import pdal
import json,os,subprocess,sys
import pandas as pd

def find_average(a_list:list)->float:
    if type(a_list) not in [list, tuple, set]:
        raise TypeError("Argument Types can only be a list, tuple or a set")

    average = sum(a_list) / len(a_list)

    return float(average)


def count_occurence(a_list:list)->dict:
    if type(a_list) not in [list, tuple, set]:
        raise TypeError("Argument Type can only be a list, tuple or a set")

    empty_dict = {}
    for i in a_list:
        if i in empty_dict:
            empty_dict[i] += 1
        else:
            empty_dict[i] = 1
    return empty_dict

def load_geolidar(boundary,state,filename):
    pipeline = {
        "pipeline": [
            {
                "bounds": f"{boundary}",
                "filename": f"https://s3-us-west-2.amazonaws.com/usgs-lidar-public/{state}/ept.json",
                "type": "readers.ept",
                "tag": "readdata"
            },
            {
                "limits": "Classification![7:7]",
                "type": "filters.range",
                "tag": "nonoise"
            },
            {
                "assignment": "Classification[:]=0",
                "tag": "wipeclasses",
                "type": "filters.assign"
            },
            {
                "out_srs": "EPSG:26915",
                "tag": "reprojectUTM",
                "type": "filters.reprojection"
            },
            {
                "tag": "groundify",
                "type": "filters.smrf"
            },
            {
                "limits": "Classification[2:2]",
                "type": "filters.range",
                "tag": "classify"
            },
            {
                "filename": f"{filename}.laz",
                "inputs": [ "classify" ],
                "tag": "writerslas",
                "type": "writers.las"
            },
            {
                "filename": f"{filename}.tif",
                "gdalopts": "tiled=yes,     compress=deflate",
                "inputs": [ "writerslas" ],
                "nodata": -9999,
                "output_type": "idw",
                "resolution": 1,
                "type": "writers.gdal",
                "window_size": 6
            }
        ]
    }
    json_object = json.dumps(pipeline, indent = 4)

    # Writing to sample.json
    with open(f"{filename}.json", "w") as outfile:
        outfile.write(json_object)
    
    os.system(f'pdal pipeline {filename}.json --debug')
    pipeline=pdal.Reader(f'{filename}.laz').pipeline()
    arrays = pipeline.arrays
    captured_array = arrays.pop()
    results = [captured_array[['X','Y','Z']][i] for i,x in enumerate(captured_array)]
    df = pd.DataFrame({'elevation_m': [x[2] for x in results]})
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy([x[1] for x in results], 
                                                           [x[0] for x in results]))
    return gdf
if __name__ == '__main__':
    data = [0,0,9,0,8,9,0,6]