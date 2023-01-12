import numpy as np
import scripts.addSA2 as addSA2
import geoplot as gplt
import geopandas as gpd
import pandas as pd
import sys
import os
repo_path = os.path.abspath('../')
sys.path.append(repo_path)

# Read in the preprocessed data
df = pd.read_csv(f"../data/curated/pre_processed_data.csv")
df = addSA2.addSA2(df, use_postcode=False)
df = df.loc[df["SA2"] != 0]

# Get population data by SA2 zone
sa2 = pd.read_csv(f"../data/raw/abs_data/pop_data.csv")
sa2 = sa2[sa2["TIME_PERIOD: Time Period"] ==
          2021][["ASGS_2021: Region", "OBS_VALUE"]]
sa2["ASGS_2021: Region"] = sa2["ASGS_2021: Region"].apply(
    lambda x: x.split(':')[0])
sa2 = sa2.rename(columns={"ASGS_2021: Region": "SA2",
                 "OBS_VALUE": "SA2_population"})
sa2 = sa2.astype(float)

# Read in building approvals to the sa2 codes.
building_metrics_2019 = ["sa2_code16", "tot_dwl_num",
                         "value_non_resial_building_aud000"]

buildings_2019 = pd.read_csv(
    f"../data/raw/datasource-AU_Govt_ABS-UoM_AURIN_DB_3 abs_building_approvals_sa2_2018_19.csv")[building_metrics_2019]

buildings_2019 = buildings_2019.rename(
    columns={"tot_dwl_num": "new_dwellings_2019", 
             "value_non_resial_building_aud000":
             "non_residential_value_2019"})

building_metrics_2021 = ["sa2_code", "total_dwellings_no",
                         "value_of_non_residential_building_000"]
buildings_2021 = pd.read_csv(
    f"../data/raw/datasource-AU_Govt_ABS-UoM_AURIN_DB_3 abs_building_approvals_sa2_2020_21.csv")[building_metrics_2021]

buildings_2021 = buildings_2021.rename(
    columns={"total_dwellings_no": "new_dwellings_2021", 
             "value_of_non_residential_building_000": "non_residential_value_2021"})

# Join building approvals to the sa2 codes.
sa2 = sa2.join(buildings_2019.set_index("sa2_code16"), on="SA2")
sa2 = sa2.join(buildings_2021.set_index("sa2_code"), on="SA2")
sa2 = sa2.fillna(0)


# get scores for how much each suburb is present in each SA2 zone
df.loc[:, "count"] = 1
df = df[["suburb", "SA2", "count"]]
sub_count = df.groupby(["suburb", "SA2"]).sum().reset_index()
sa2_count = df[["SA2", "count"]].groupby("SA2").sum()
sa2_count = sa2_count.rename(columns={"count": "sa2_count"})

scores = sub_count.join(sa2_count, on="SA2")
scores["SA2_fraction"] = scores["count"]/scores["sa2_count"]
scores = scores.join(sa2.set_index("SA2"), on="SA2")

# Get the SA2 level statistics converted to suburb level
scores["suburb_population"] = scores["SA2_population"]*scores["SA2_fraction"]
scores["new_dwellings_2019"] = scores["new_dwellings_2019"] * \
    scores["SA2_fraction"]
scores["non_residential_value_2019"] = scores["non_residential_value_2019"] * \
    scores["SA2_fraction"]*1000  # convert to $s
scores["new_dwellings_2021"] = scores["new_dwellings_2021"] * \
    scores["SA2_fraction"]
scores["non_residential_value_2021"] = scores["non_residential_value_2021"] * \
    scores["SA2_fraction"]*1000  # convert to $s
suburb_pop = scores[["suburb", "suburb_population", "new_dwellings_2019", "non_residential_value_2019",
                     "new_dwellings_2021", "non_residential_value_2021"]].groupby("suburb").sum().reset_index()

suburb_sa2 = scores[["suburb", "SA2"]].groupby(
    "suburb").agg(lambda x: x.mode().to_list()[0])


# Load in historical data
h_df = pd.read_csv(f"../data/curated/historical_sales_clean.csv")

h_df = h_df[["suburb", "num_beds", "property_type", "2022_n_sold", "clearance", "avg_days_on_market", "2022_median", "2022_growth",
             "2021_growth", "2020_growth", "2019_growth", "2019_n_sold"]]

# Impute missing values
h_df = h_df.replace('-', 0).astype({"avg_days_on_market": "float"})
h_df.loc[:, '2022_growth'] = h_df['2022_growth'].fillna(
    h_df.groupby("suburb")['2022_growth'].transform("mean"))
h_df.loc[:, '2021_growth'] = h_df['2021_growth'].fillna(
    h_df.groupby("suburb")['2021_growth'].transform("mean"))
h_df.loc[:, '2020_growth'] = h_df['2020_growth'].fillna(
    h_df.groupby("suburb")['2020_growth'].transform("mean"))
h_df.loc[:, '2019_growth'] = h_df['2019_growth'].fillna(
    h_df.groupby("suburb")['2019_growth'].transform("mean"))
h_df.loc[:, '2019_n_sold'] = h_df['2019_n_sold'].fillna(0)
h_df.loc[:, '2022_n_sold'] = h_df['2022_n_sold'].fillna(0)
h_df.loc[:, 'clearance'] = h_df['clearance'].fillna(
    h_df.groupby("suburb")['clearance'].transform("mean"))
h_df.loc[:, 'avg_days_on_market'] = h_df['avg_days_on_market'].fillna(
    h_df.groupby("suburb")['avg_days_on_market'].transform("mean"))
# calculate 3 year growth
h_df.loc[:, "total_growth"] = (
    1+h_df["2019_growth"])*(1+h_df["2020_growth"])*(1+h_df["2021_growth"]) - 1

# get sum of all property types
sums = pd.DataFrame(h_df.groupby("suburb").sum()["2019_n_sold"].reset_index())
sums = sums.rename(columns={"2019_n_sold": "total_sold"})

h_df = h_df.join(sums.set_index("suburb"), on="suburb")

# get weighted averages from different property types, weighted by frequency.
h_df["total_growth"] = (h_df["2019_n_sold"] /
                        h_df["total_sold"])*h_df["total_growth"]
h_df["2022_median"] = (h_df["2019_n_sold"] /
                       h_df["total_sold"])*h_df["2022_median"]
h_df["2022_growth"] = (h_df["2019_n_sold"] /
                       h_df["total_sold"])*h_df["2022_growth"]
h_df["clearance"] = (h_df["2019_n_sold"]/h_df["total_sold"])*h_df["clearance"]
h_df["avg_days_on_market"] = (
    h_df["2019_n_sold"]/h_df["total_sold"])*h_df["avg_days_on_market"]

# clean up final dataframe
fin_df = h_df[["suburb", "clearance", "avg_days_on_market", "total_growth",
               "2019_n_sold", "2022_n_sold", "2022_median", "2022_growth"]]
fin_df = fin_df.groupby("suburb").sum().reset_index()

fin_df = fin_df.rename(columns={"total_growth": "3_year_growth"})
fin_df = fin_df.join(suburb_pop.set_index("suburb"), on="suburb").fillna(0)
fin_df = fin_df.join(suburb_sa2, on="suburb")

fin_df.to_csv(f"../data/curated/future_prediction_data.csv")
