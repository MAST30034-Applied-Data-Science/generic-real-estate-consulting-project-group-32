from sklearn.cluster import KMeans
from statsmodels.stats.outliers_influence import OLSInfluence
import statsmodels.regression.linear_model as lm

df = pd.read_csv(f"../data/curated/pre_processed_data.csv")

# Remove any value with a weekly rent past 2 standard deviations. (this just removes extreme outliers where data has been input incorrectly)
mean = df["weekly_rent"].mean()
std = df["weekly_rent"].std()
df = df[df["weekly_rent"] <= mean + 2*std]

df2 = df.copy()

# Define the independent variables
predictors = ["num_beds", "num_baths", "num_parking", "school_distance"]
# Define the dependent variabe
target = ["weekly_rent"]
# Remove NaN values
df[predictors] = df[predictors].fillna(df[predictors].mean())
df[target] = df[target].fillna(df[target].mean())


# Fit an ordinary linear model
model = lm.OLS(df[target], df[predictors])
results = model.fit()
influence = OLSInfluence(results)
# Get the standardised residuals
sres = influence.resid_studentized_internal

# mark points above a certain cooks distance.
df2.loc[influence.cooks_distance[0] < 0.002].to_csv(f"../data/curated/outlier_removed_data.csv")