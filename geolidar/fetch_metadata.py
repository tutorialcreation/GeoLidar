import pandas as pd
from urllib.request import urlopen
from .constants import state_mapper
import json

def fetch_data(filename):
    df = pd.DataFrame()
    for k,state in state_mapper.items():
        url = f"https://s3-us-west-2.amazonaws.com/usgs-lidar-public/{state}/ept.json"
  
        # store the response of URL
        response = urlopen(url)

        # storing the JSON response 
        json_obj = json.loads(response.read())

        # access properties from this file
        df['state_description'] = state
        df['points'] = json_obj['points']
        df['X'] = json_obj['schema'][0]['offset']
        df['Y'] = json_obj['schema'][1]['offset']
        df['Z'] = json_obj['schema'][2]['offset']
        df['EPSG'] = json_obj['srs']['authority']
        df['EPSG_Output'] = json_obj['srs']['horizontal']
    df.to_csv(filename)
    return df