from IPython.display import display
import pandas as pd
import re
import numpy as np


DIR_RAW = "../data/raw/"
DIR_CUR = "../data/curated/"


df_postcode = pd.read_csv(f"{DIR_RAW}postcodes.csv")
df_postcode = df_postcode[df_postcode["state"] == "VIC"]
suburbs = set(map(lambda x: x.lower(), df_postcode["locality"].unique()))


PATTERN_PRICE = r"\$?\s*(\d[\d\.,]+)(([\s\/]*((per[\s\/]week)|(weekly)|(p[\/.]*w[k\.]*)|(wk)|(a week)|(w)|(week)|(p\/week)|(per weekly)|(per wk))\b)|$)"
PATTERN_BED = r"^(\d+) beds?"
PATTERN_BATH = r"^(\d+) baths?"
PATTERN_CAR = r"^(\d+) parking"
PATTERN_STATE = r".+ (\w+) \d{4}"
PATTERN_SUBURB = f"({'|'.join(suburbs)}|sanctuary lakes)( vic)?"
PATTERN_BOND = r"bond \$?(\d+)"
PATTERN_INTERNAL_AREA = r"internal area ([\d\.]+)m"
PATTERN_LAND_AREA = r"land area ([\d\.]+)m"
PATTERN_LAST_SOLD = r"last sold in (\d{4})"
PATTERN_OTHER_SOLD = r"(\d+) other"
PATTERN_FIRST_LISTED = r"first listed on (\d+ \w+),"
PATTERN_POSTCODE = r"vic (\d{4})"
PATTERN_PERCENTAGE = r"(\d+\.?\d*)"
PATTERN_PERFOMANCE_PRICE = r"(\d+\.?\d*[mk]?)"
PATTERN_INT = r"([\d,]+)"
PATTERN_RANGE = r"(\d+ to \d+)|(\d+\+)"

FUNC_NONE = lambda x: x
FUNC_STR_TO_NUM = lambda x: float(x.replace(",", ""))
FUNC_PRICE_CONVERT = lambda x: (float(x[0:-1])*1000000 if x[-1] in "mM"
                                else float(x[0:-1])*1000 if x[-1] in "kK"
                                else float(x))
FUNC_PERCENTAGE = lambda x:float(x) / 100


# show all attributes when displayed and don't truncate values
pd.options.display.max_columns = None
pd.set_option('display.max_colwidth', None)


def pattern_match(df, feature, pattern, function=FUNC_NONE):
    instances = df[feature]

    values = []
    for instance in instances:
        instance = str(instance).lower()
        match = re.search(pattern, instance, flags=re.IGNORECASE)
        if match:
            values.append(function(match.group(1)))
        else:
            values.append(None)
    
    return values

df_raw = pd.read_csv(f"{DIR_RAW}scraped_properties.csv")
df_cur = pd.DataFrame()


# CLEAN SCRAPED DATA
df_cur["url"] = df_raw["url"]
df_cur["postcode"] = pattern_match(df_raw, "address", PATTERN_POSTCODE)
df_cur["suburb"] = pattern_match(df_raw, "address", PATTERN_SUBURB)  # takes a long time
df_cur["state"] = pattern_match(df_raw, "address", PATTERN_STATE)

df_cur["weekly_rent"] = pattern_match(df_raw, "price", PATTERN_PRICE, FUNC_STR_TO_NUM)
df_cur["bond"] = pattern_match(df_raw, "bond", PATTERN_BOND, FUNC_STR_TO_NUM)

df_cur["num_beds"] = pattern_match(df_raw, "num_beds", PATTERN_BED, FUNC_STR_TO_NUM)
df_cur["num_baths"] = pattern_match(df_raw, "num_bath", PATTERN_BATH, FUNC_STR_TO_NUM)
df_cur["num_parking"] = pattern_match(df_raw, "num_car", PATTERN_CAR, FUNC_STR_TO_NUM)

df_cur["property_type"] = df_raw["property_type"]

df_cur["internal_area"] = pattern_match(df_raw, "internal_area", PATTERN_INTERNAL_AREA, FUNC_STR_TO_NUM)
df_cur["land_area"] = pattern_match(df_raw, "land_area", PATTERN_LAND_AREA, FUNC_STR_TO_NUM)

df_cur["last_sold"] = pattern_match(df_raw, "domain_says", PATTERN_LAST_SOLD)
df_cur["other_sold_n_bed_suburb"] = pattern_match(df_raw, "domain_says", PATTERN_OTHER_SOLD, FUNC_STR_TO_NUM)
#df_cur["first_listed"] = pattern_match(df_raw, "domain_says", PATTERN_FIRST_LISTED)

df_cur["neighbourhood_under_20"] = pattern_match(df_raw, "neighbourhood_under_20", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["neighbourhood_20_to_39"] = pattern_match(df_raw, "neighbourhood_20_to_39", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["neighbourhood_40_to_59"] = pattern_match(df_raw, "neighbourhood_40_to_59", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["neighbourhood_above_60"] = pattern_match(df_raw, "neighbourhood_above_60", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["neighbourhood_long_term_residents"] = pattern_match(df_raw, "neighbourhood_long_term_residents", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["neighbourhood_owners"] = pattern_match(df_raw, "neighbourhood_owners", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["neighbourhood_renter"] = pattern_match(df_raw, "neighbourhood_renter", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["neighbourhood_family"] = pattern_match(df_raw, "neighbourhood_family", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["neighbourhood_single"] = pattern_match(df_raw, "neighbourhood_single", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)

df_cur["performance_median_price"] = pattern_match(df_raw, "performance_median_price", PATTERN_PERFOMANCE_PRICE, FUNC_PRICE_CONVERT)
df_cur["performance_auction_clearance"] = pattern_match(df_raw, "performance_auction_clearance", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["performance_sold_this_year"] = pattern_match(df_raw, "performance_sold_this_year", PATTERN_INT, FUNC_STR_TO_NUM)
df_cur["performance_avg_days_on_market"] = pattern_match(df_raw, "performance_avg_days_on_market", PATTERN_INT, FUNC_STR_TO_NUM)

df_cur["demographic_population"] = pattern_match(df_raw, "demographic_population", PATTERN_INT, FUNC_STR_TO_NUM)
df_cur["demographic_owner"] = pattern_match(df_raw, "demographic_owner", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["demographic_renter"] = pattern_match(df_raw, "demographic_renter", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["demographic_family"] = pattern_match(df_raw, "demographic_family", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["demographic_single"] = pattern_match(df_raw, "demographic_single", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["demographic_average_age"] = pattern_match(df_raw, "demographic_average_age", PATTERN_RANGE)

df_cur["latitude"] = df_raw["latitude"].astype(float)
df_cur["longitude"] = df_raw["longitude"].astype(float)

# MERGING DATASETS
API_FEATURES = ["school_duration", "school_distance",
                "park_duration", "park_distance",
                "shop_duration", "shop_distance",
                "train_duration", "train_distance",
                "stop_duration", "stop_distance"]

df_school = pd.read_csv(f"{DIR_CUR}api_data.csv")
df_cur = df_cur.merge(df_school, on="url")

import geopandas as gpd
from shapely.geometry import Point


def find_zone(long, lat, shape_df):
    """ Finds the SA2 value based on the coordinates"""
    if np.isnan(lat) or np.isnan(long):
        return 0
    sa2 = shape_df.loc[shape_df["geometry"].contains(Point(long, lat)), "SA2_CODE21"]
    if len(sa2) != 1:
        return 0
    else: 
        return float(sa2)
    
sf_sa2 = gpd.read_file(f"{DIR_RAW}abs_data/zone_data/zones/SA2_2021_AUST_GDA2020.shp")
sf_sa2 = sf_sa2[sf_sa2["STE_NAME21"] == "Victoria"]
sf_sa2 = sf_sa2[sf_sa2["geometry"] != None]
sf_sa2 = sf_sa2[["SA2_CODE21", "geometry"]]
sf_sa2 = sf_sa2.astype({"SA2_CODE21": float})

df_cur["SA2"] = df_cur.apply(lambda x: find_zone(x["longitude"], x["latitude"], sf_sa2), axis=1)    

df_pop = pd.read_csv(f"{DIR_RAW}/abs_data/pop_data.csv")
df_pop = df_pop[df_pop["TIME_PERIOD: Time Period"] == 2021]
df_pop = df_pop[["ASGS_2021: Region", "OBS_VALUE"]]
df_pop["ASGS_2021: Region"] = df_pop["ASGS_2021: Region"].apply(lambda x: x.split(':')[0])
df_pop = df_pop.rename(columns = {"ASGS_2021: Region": "SA2",
                                  "OBS_VALUE": "population"})
df_pop = df_pop.astype({"SA2": float})

df_cur = df_cur.merge(df_pop, on="SA2")

df_income = pd.read_csv(f"{DIR_RAW}abs_data/2021_income.csv")

df_income = df_income[df_income["TIME_PERIOD: Time Period"] == 2021]
df_income = df_income[["REGION: Region", "OBS_VALUE"]]
df_income["REGION: Region"] = df_income["REGION: Region"].apply(lambda x: x.split(':')[0])
df_income = df_income.rename(columns={"REGION: Region": "SA2",
                                      "OBS_VALUE": "median_weekly_income"})
df_income = df_income.astype({"SA2": float})

df_cur = df_cur.merge(df_income, on="SA2")

df_cur = df_cur[df_cur["state"] != "nsw"]

df_cur = df_cur[df_cur["property_type"] != "Carspace"]

def box_plot_fences(x):
    Q1 = x.quantile(0.25)
    Q3 = x.quantile(0.75)
    IQR = Q3 - Q1
    
    return Q1 - 1.5*IQR, Q3 + 1.5*IQR


def std_2_bounds(x):
    mean = x.mean()
    std = x.std()
    
    return mean - 2*std, mean + 2*std


def between(df, col, U, L):
    return df[df[col].isnull() | ((df[col] >= L) & (df[col] <= U))]


TEST = ["school_distance", "park_distance",
        "shop_distance", "train_distance",
        "stop_distance"]


df_test = df_cur.copy(deep=True)

print(f"Instances before outlier removal: {len(df_test.index)}")

L, U = box_plot_fences(df_test["weekly_rent"])[0], std_2_bounds(df_test["weekly_rent"])[1]
df_test =  between(df_test, "weekly_rent", U, L)

for col in TEST:
    before = len(df_test.index)
    #L, U = box_plot_fences(df_test[col])
    L, U = std_2_bounds(df_test[col])
    df_test = between(df_test, col, U, L)
    after = len(df_test.index)
    
    #print(f"{col} | [{L:.3f}, {U:.3f}] |  {before - after}")

print(f"Instances after  outlier removal: {len(df_test.index)}")

df_cur = df_test

from sklearn.cluster import KMeans
from statsmodels.stats.outliers_influence import OLSInfluence
import statsmodels.regression.linear_model as lm


PRED = ["num_beds", "num_baths", "num_parking", "bond"] + API_FEATURES

TARG = "weekly_rent"

# impute missing values
df_impute = df_cur.copy(deep=True)
df_impute[PRED + [TARG]] = df_cur[PRED + [TARG]].fillna(df_cur[PRED + [TARG]].mean())

# Fit an ordinary linear model
model = lm.OLS(df_impute[[TARG]], df_impute[PRED])
influence = OLSInfluence(model.fit())

df_cur =  df_cur[influence.cooks_distance[0] < 0.002]

df_cur.to_csv(f"{DIR_CUR}/pre_processed_data.csv", index=False)

NUMERICALS = ["weekly_rent", "bond", "num_beds", "num_baths", "num_parking",
              "internal_area", "land_area",
              "other_sold_n_bed_suburb", "neighbourhood_under_20",
              "neighbourhood_20_to_39", "neighbourhood_40_to_59",
              "neighbourhood_above_60", "neighbourhood_long_term_residents",
              "neighbourhood_owners", "neighbourhood_renter",
              "neighbourhood_family", "neighbourhood_single",
              "performance_median_price", "performance_auction_clearance",
              "performance_sold_this_year", "performance_avg_days_on_market",
              "demographic_population", "demographic_owner",
              "demographic_renter", "demographic_family",
              "demographic_single", "school_distance", "park_distance",
              "shop_distance", "train_distance", "stop_distance", "population", "median_weekly_income"]

#CATEGORICALS = ["property_type", "last_sold", "demographic_average_age"]



df_suburb = df_cur.groupby("suburb")
dict1 = {"url": "count"}
dict2 = {col: "mean" for col in NUMERICALS}
df_suburb = df_suburb.agg({**dict1,**dict2})
df_suburb = df_suburb.rename(columns={"url": "count"})

df_suburb = df_suburb[df_suburb["count"] > 16]

display(df_suburb.head(5))
df_suburb.to_csv(f"{DIR_CUR}/suburb_data.csv")