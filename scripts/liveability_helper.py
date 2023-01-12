from scipy.stats import percentileofscore
import numpy as np
import pandas as pd

# This file contains functions to help run Q3 in the summary notebook


def median_rent(df, postcode):
    """Calculates median rent based on scraped properties"""
    df = df[df["postcode"] == postcode]
    n_sold = df.n_sold.values.tolist()
    median = df.median_rent.values.tolist()

    weighted_ave = np.nansum([x * y for x, y in zip(n_sold, median)]) / np.nansum(
        n_sold
    )
    return weighted_ave


def score(
    property_df,
    school_duration,
    school_distance,
    park_duration,
    park_distance,
    shop_duration,
    shop_distance,
    train_duration,
    train_distance,
    stop_duration,
    stop_distance,
    median_rent,
    affordable=False,
):
    """This function scores each suburb"""

    if school_duration == 0:
        school_duration_score = 100
    else:
        school_duration_score = percentileofscore(
            property_df.school_duration.dropna(), school_duration
        )
    if school_distance == 0:
        school_distance_score = 100
    else:
        school_distance_score = percentileofscore(
            property_df.school_distance.dropna(), school_distance
        )
    if park_duration == 0:
        park_duration_score = 100
    else:
        park_duration_score = percentileofscore(
            property_df.park_duration.dropna(), park_duration
        )
    if park_distance == 0:
        park_distace_score = 100
    else:
        park_distace_score = percentileofscore(
            property_df.park_distance.dropna(), park_distance)
    if shop_duration == 0:
        shop_duration_score = 100
    else:
        shop_duration_score = percentileofscore(
            property_df.shop_duration.dropna(), shop_duration
        )
    if shop_distance == 0:
        shop_distance_score = 100
    else:
        shop_distance_score = percentileofscore(
            property_df.shop_distance.dropna(), shop_distance
        )

    if train_duration == 0:
        train_duration_score = 100
    else:
        train_duration_score = percentileofscore(
            property_df.train_duration.dropna(), train_duration
        )
    if train_distance == 0:
        train_distance_score = 100
    else:
        train_distance_score = percentileofscore(
            property_df.train_distance.dropna(), train_distance
        )
    if stop_duration == 0:
        stop_duration_score = 100
    else:
        stop_duration_score = percentileofscore(
            property_df.stop_duration.dropna(), stop_duration
        )
    if stop_distance == 0:
        stop_distance_score = 100
    else:
        stop_distance_score = percentileofscore(
            property_df.stop_distance.dropna(), stop_distance
        )
    if affordable:
        median_rent_score = 4.2 * percentileofscore(
            property_df.median_rent.dropna(), median_rent
        )
    else:
        median_rent_score = 0
    score = (
        school_distance_score
        + park_duration_score
        + park_distace_score
        + shop_duration_score
        + shop_distance_score
        + shop_distance_score
        + train_duration_score
        + train_distance_score
        + stop_duration_score
        + stop_distance_score
        + median_rent_score
    )
    return score
