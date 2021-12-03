import pandas as pd
import datetime

df = pd.read_csv("/Users/yannbonzom/Desktop/COMP 598/hw/hw4/submission_template/data/trimmed_2020_zipcode_enddate_necessarycolumns.csv", header=None)
initial_len = len(df)
print(initial_len)

hours = []

for index, row in df.iterrows():
    print(f"{index} / {initial_len}")

    t1 = datetime.datetime.strptime(row[0], "%m/%d/%Y %I:%M:%S %p")
    t2 = datetime.datetime.strptime(row[1], "%m/%d/%Y %I:%M:%S %p")

    diff = (t2 - t1).total_seconds()

    if diff < 0:
        df.drop([index], inplace=True)
    else:
        hours.append(diff / 60 / 60)

print(len(df))
df[len(df.columns)] = hours

df.to_csv("trimmed_2020_zipcode_enddate_necessarycolumns_postive_durations.csv", index=None, header=False)