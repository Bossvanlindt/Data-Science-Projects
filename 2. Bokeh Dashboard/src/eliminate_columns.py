import pandas as pd

df = pd.read_csv("/Users/yannbonzom/Desktop/COMP 598/hw/hw4/submission_template/data/trimmed_2020_zipcode_enddate.csv", header=None)

df = df[[1, 2, 8]]

df.to_csv("trimmed_2020_zipcode_enddate_necessarycolumns.csv", index=None, header=False)