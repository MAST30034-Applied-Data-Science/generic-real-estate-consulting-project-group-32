import pandas as pd
import re

FILE_DIR = "../data/raw/scrape_2022-09-02_04-12-25-567025.json"


# NOTE: have to remove any property with "Barooga NSW 3644" as it is a NSW property with a VIC postcode

PATTERN_PRICE = r"\$?\s*(\d[\d\.,]+)(([\s\/]*((per[\s\/]week)|(weekly)|(p[\/.]*w[k\.]*)|(wk)|(a week)|(w)|(week)|(p\/week)|(per weekly)|(per wk))\b)|$)"
PATTERN_BED = r"(\d+) beds?"
PATTERN_BATH = r"(\d+) baths?"
PATTERN_CAR = r"(\d+) parking"
PATTERN_BOND = r"bond \$?(\d+)"
PATTERN_INTERNAL_AREA = r"internal area ([\d\.]+)m"
PATTERN_LAND_AREA = r"land area ([\d\.]+)m"
PATTERN_LAST_SOLD = r"last sold in (\d{4})"
PATTERN_OTHER_SOLD = r"(\d+) other"
PATTERN_FIRST_LISTED = r"first listed on (\d+ \w+),"
PATTERN_POSTCODE = r"vic (\d{4})"

#pd.set_option('display.max_colwidth', None)
df = pd.read_json(FILE_DIR)


def pattern_match(df, feature, new_feature, pattern):
    instances = df[feature]

    values = []
    for instance in instances:
        instance = str(instance)
        match = re.search(pattern, instance, flags=re.IGNORECASE)
        if match:
            values.append(match.group(1))
        else:
            values.append(None)


    df[new_feature] = values
    return df


df = pattern_match(df, "price", "weekly_rent_AUS", PATTERN_PRICE)
df = pattern_match(df, "num_beds", "num_beds", PATTERN_BED)
df = pattern_match(df, "num_bath", "num_bath", PATTERN_BATH)
df = pattern_match(df, "num_car", "num_car", PATTERN_CAR)
df = pattern_match(df, "bond", "bond_AUS", PATTERN_BOND)
df = pattern_match(df, "internal_area", "internal_area_m_squared", PATTERN_INTERNAL_AREA)
df = pattern_match(df, "land_area", "land_area_m_squared", PATTERN_LAND_AREA)
df = pattern_match(df, "domain_says", "last_sold", PATTERN_LAST_SOLD)
df = pattern_match(df, "domain_says", "other_n_bedroom_properties_sold_in_suburb", PATTERN_OTHER_SOLD)
df = pattern_match(df, "domain_says", "property_listed", PATTERN_FIRST_LISTED)
df = pattern_match(df, "address", "poscode", PATTERN_POSTCODE)

df = df.replace(",", "", regex=True)

#print(list(df.columns))

#df = df[df["property_type"].str.contains("Semi-Detached", na=False)]
#df = df[["url", "property_type"]]
#print(df.head(5))


#df = price(df)
#df = beds(df)
#df = bath(df)
#df = car(df)
#df = bond(df)


#print(df.groupby("agent")["url"].nunique())

#instances = set(df["domain_says"].unique())
#for instance in instances:
#    print(instance)
#    print("------")

#df = df[["domain_says", "last_sold"]]
#print(df.head(50))
