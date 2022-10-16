import sys
import os
repo_path = os.path.abspath('../')
sys.path.append(repo_path)
import scripts.addSA2 as addSA2
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
import imageio

def addSA2(df: pd.DataFrame, use_postcode=False):
    """ Adds SA2 code and geometry of the SA2 value to the dataframe, and 
    converts to GeoDataFrame. Use postcode specifies whether to use the 
    postcode or latitude and longitude.
    """
    
    # If missing longitude and latitude
    if use_postcode:
        postcodes = pd.read_csv("../data/raw/postcode.csv")
        postcodes = postcodes.rename(columns={"lat":"latitude",  \
                                              "long":"longitude"})
        postcodes = postcodes[["postcode", "latitude", "longitude"]]
        postcodes = postcodes.drop_duplicates()
        df = df.join(postcodes.set_index("postcode"), on = "postcode",  \
                     lsuffix = "_l", rsuffix = "")

    shape = gpd.read_file('../data/raw/ShapeFile/SA2_2021_AUST_GDA2020.shp')
    shape = shape.loc[shape.STE_NAME21 == "Victoria"]
    shape = shape.loc[shape.geometry != None]
    shape = shape[["SA2_CODE21", "geometry", "AREASQKM21"]]
    shape = shape.astype({"SA2_CODE21": float})
    df["SA2"] = df.apply(lambda x: find_zone(x["longitude"],  \
                                             x["latitude"],shape), axis=1)
    geo_df = gpd.GeoDataFrame(df.join(shape.set_index("SA2_CODE21")  \
                                      ["geometry"], on = "SA2"))
    
    return geo_df


def find_zone(long, lat, shape_df):
    """ Finds the SA2 value based on the coordinates"""
    if np.isnan(lat) or np.isnan(long):
        return 0
    sa2 = shape_df.loc[shape_df["geometry"].contains(Point(long,lat)),  \
                       "SA2_CODE21"]
    if len(sa2) != 1:
        return 0
    else: 
        return float(sa2)

