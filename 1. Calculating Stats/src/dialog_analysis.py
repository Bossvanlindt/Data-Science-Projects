import sys
import pandas as pd
import json

# Handle inputs
if len(sys.argv) != 4:
    print('Invalid number of arguments. Use: "python3 dialog_analysis.py -o output_file input_file"')
    exit()
output = sys.argv[2]
input = sys.argv[3]

# List of pony names
names = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]

# Set up dictionary to produce final output json
result = {}
result['count'] = {}
result['verbosity'] = {}

df = pd.read_csv(input)
# Make all pony names lowercase to avoid issues with that
df['pony'] = df['pony'].apply(lambda n : n.lower())

# Get the counts
counts = df['pony'].value_counts()
for name in names:
    pony_count = int(counts[name])
    result['count'][name] = pony_count

# Get the verbosities relative to the total script length
for name in names:
    result['verbosity'][name] = round(result['count'][name] / len(df), 2)

# Write result to output.json file
# print(json.dumps(result, indent='\t'))
with open (output, 'w') as output_file:
    output_file.write(json.dumps(result, indent='\t'))