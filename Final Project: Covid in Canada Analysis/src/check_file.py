# Simple checker for the validity of the final labeled data file.
import pandas as pd

df = pd.read_csv('data/final_labeled_data.csv')

# Print number of unique values in the 'category' column
print(df['category'].nunique())

# Print number of rows
print(df.shape[0])