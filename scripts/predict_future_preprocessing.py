from IPython.display import display
import pandas as pd
import re
import numpy as np


DIR_RAW = "../data/raw/"
DIR_CUR = "../data/curated/"


df_raw = pd.read_csv(f"{DIR_CUR}historical_sales.csv")
df_cur = pd.DataFrame()


PATTERN_BED = r"^(\d+) beds?"
PATTERN_PERCENTAGE = r"(\d+\.?\d*)"
PATTERN_PERFOMANCE_PRICE = r"(\d+\.?\d*[mk]?)"
PATTERN_INT = r"([\d,]+)"
PATTERN_RANGE = r"(\d+ to \d+)|(\d+\+)"
PATTERN_PROPERTY_TYPE = r"(?<=_)[a-z]+"


def FUNC_NONE(x): return x
def FUNC_STR_TO_NUM(x): return float(x.replace(",", ""))


def FUNC_PRICE_CONVERT(x): return (float(x[0:-1])*1000000 if x[-1] in "mM"
                                   else float(x[0:-1])*1000 if x[-1] in "kK"
                                   else float(x))


def FUNC_PERCENTAGE(x): return float(x) / 100


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
            values.append(function(match.group()))
        else:
            values.append(None)

    return values


df_cur["suburb"] = df_raw["suburb"]
df_cur["postcode"] = df_raw["postcode"]
df_cur["num_beds"] = pattern_match(df_raw, "p_type", PATTERN_INT)
df_cur["property_type"] = pattern_match(
    df_raw, "p_type", PATTERN_PROPERTY_TYPE)
df_cur["avg_days_on_market"] = df_raw["avg_days_on_market"].apply(
    lambda x: x.split()[0])
df_cur["clearance"] = pattern_match(
    df_raw, "clearance", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["2022_median"] = pattern_match(
    df_raw, "2022_median", PATTERN_PERFOMANCE_PRICE, FUNC_PRICE_CONVERT)
df_cur["2022_growth"] = pattern_match(
    df_raw, "2022_growth", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["2022_n_sold"] = df_raw["2022_n_sold"]
df_cur["2021_median"] = pattern_match(
    df_raw, "2021_median", PATTERN_PERFOMANCE_PRICE, FUNC_PRICE_CONVERT)
df_cur["2021_growth"] = pattern_match(
    df_raw, "2021_growth", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["2021_n_sold"] = df_raw["2021_n_sold"]
df_cur["2020_median"] = pattern_match(
    df_raw, "2020_median", PATTERN_PERFOMANCE_PRICE, FUNC_PRICE_CONVERT)
df_cur["2020_growth"] = pattern_match(
    df_raw, "2020_growth", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["2020_n_sold"] = df_raw["2020_n_sold"]
df_cur["2019_median"] = pattern_match(
    df_raw, "2019_median", PATTERN_PERFOMANCE_PRICE, FUNC_PRICE_CONVERT)
df_cur["2019_growth"] = pattern_match(
    df_raw, "2019_growth", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["2019_n_sold"] = df_raw["2019_n_sold"]
df_cur["2018_median"] = pattern_match(
    df_raw, "2018_median", PATTERN_PERFOMANCE_PRICE, FUNC_PRICE_CONVERT)
df_cur["2018_growth"] = pattern_match(
    df_raw, "2018_growth", PATTERN_PERCENTAGE, FUNC_PERCENTAGE)
df_cur["2018_n_sold"] = df_raw["2018_n_sold"]

df_cur.to_csv(f"{DIR_CUR}historical_sales_clean.csv")
