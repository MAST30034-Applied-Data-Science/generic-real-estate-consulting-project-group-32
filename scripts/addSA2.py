import sys
import os
repo_path = os.path.abspath('../')
sys.path.append(repo_path)
import scripts.addSA2 as addSA2
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
import imageio

def addSA2(df: pd.DataFrame):
    """ Adds SA2 code and geometry of the SA2 value to the dataframe, and converts to GeoDataFrame """

    postcodes = pd.read_csv("../data/raw/australian_postcodes.csv")
    postcodes = postcodes[["postcode", "lat", "long"]]
    postcodes = postcodes.drop_duplicates()

    shape = gpd.read_file('../data/raw/ShapeFile/SA2_2021_AUST_GDA2020.shp')
    shape = shape.loc[shape.STE_NAME21 == "Victoria"]
    shape = shape.loc[shape.geometry != None]
    shape = shape[["SA2_CODE21", "geometry", "AREASQKM21"]]
    shape = shape.astype({"SA2_CODE21": float})
    
    df = df.join(postcodes.set_index("postcode"), on = "postcode", lsuffix = "_l", rsuffix = "_r")
    df["SA2"] = df.apply(lambda x: find_zone(x["long"],x["lat"],shape), axis=1)
    geo_df = gpd.GeoDataFrame(df.join(shape.set_index("SA2_CODE21")["geometry"], on = "SA2"))
    
    return geo_df


def find_zone(long, lat, shape_df):
    """ Finds the SA2 value based on the coordinates"""
    return float(shape_df.loc[shape_df["geometry"].contains(Point(long,lat)), "SA2_CODE21"])
