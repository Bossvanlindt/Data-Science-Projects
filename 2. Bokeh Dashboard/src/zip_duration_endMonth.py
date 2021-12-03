import pandas as pd
import datetime

df = pd.read_csv('/Users/yannbonzom/Desktop/COMP 598/hw/hw4/submission_template/data/trimmed_2020_zipcode_enddate_necessarycolumns_postive_durations.csv', header=None)
initial_len = len(df)
print(initial_len)

end_months = []

for index, row in df.iterrows():
    print(f"{index} / {initial_len}")

    end_month = datetime.datetime.strptime(row[1], "%m/%d/%Y %I:%M:%S %p").month
    end_months.append(end_month)

print(len(df))
df[len(df.columns)] = end_months

df = df[[2, 3, 4]]

df.to_csv("zip_duration_endMonth.csv", index=None, header=False)