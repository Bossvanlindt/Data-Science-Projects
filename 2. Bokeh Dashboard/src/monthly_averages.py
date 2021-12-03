from numpy.typing import _128Bit
import pandas as pd

df = pd.read_csv("/Users/yannbonzom/Desktop/COMP 598/hw/hw4/submission_template/data/zip_duration_endMonth.csv", header=None)

months = [1,2,3,4,5,6,7,8,9,10,11,12]

#Get all averages by month
month_means = []
for month in months:
    # Get mean duration of all rows that match that end month
    month_means.append(df[df[2] == month][1].mean())

df_all = pd.DataFrame()
df_all[0] = months
df_all[1] = month_means
df_all.columns = ['Month', 'Create-to-Closed Time']
df_all.to_csv("preprocessed/all.csv", index=None)

# Get averages by zip code
for zip_code in df[0].unique():
    month_means = []

    df_zip_code = df[df[0] == zip_code]

    for month in months:
        month_means.append(df_zip_code[df_zip_code[2] == month][1].mean())

    df_month = pd.DataFrame()
    df_month[0] = months
    df_month[1] = month_means
    df_month.columns = ['Month', 'Create-to-Closed Time']
    df_month.to_csv(f"preprocessed/{zip_code}.csv", index=None)