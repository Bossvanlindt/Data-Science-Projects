# From the input dialog script, generate a json containing the interaction 
# counts between every character that is in the top 101 most frequent characters
import json
import argparse
import pandas as pd
import os

def main(): 
    # Get user inputs in the form: 
    # python build_interaction_network.py -i /path/to/<script_input.csv> -o /path/to/<interaction_network.json>
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input script required", required=True)
    parser.add_argument("-o", "--output", help="Output json file required", required=True)
    args = parser.parse_args()
    # Get inputs
    dialog = args.input
    output = args.output
    # Create output directory if it doesn't exist
    output = args.output
    if not os.path.exists(os.path.dirname(output)):
        if os.path.dirname(output) != '':
            os.makedirs(os.path.dirname(output))

    # Format the dialog file as a dict with only the names of correct format
    names = format_data(dialog)

    # Extract the interaction data from the names in the dict
    interaction_counts = get_interaction_counts(names)

    # Safe the final network as a json in the output file
    with open(output, "w") as f:
        f.write(json.dumps(interaction_counts, indent=4))


# Format data for proper network extraction
def format_data(dialog):
    # Extract dialog data into a dataframe
    df = pd.read_csv(dialog)

    # Format every row as follows:
    # Convert name to lowercase
    df['pony'] = df['pony'].str.lower()
    # 2. If name contains others, ponies, and, or all, replace with NA
    df.loc[df['pony'].str.contains('others|ponies|and|all', regex=True), 'pony'] = 'NA'
    # Get the top 101 most frequent characters
    top_101 = df[df['pony'] != 'NA']['pony'].value_counts()[:101].index.tolist()
    # For each row, if its name is not in the top characters, replace with NA
    df.loc[df['pony'].isin(top_101) == False, 'pony'] = 'NA'
    # Drop all but the names and episode columns
    df = df[['pony', 'title']]
    
    # Return a list of (pony, title) pairs for easier handling
    return [(y,z) for (y,z) in zip(df['pony'], df['title'])]


# Get the interaction counts from the formatted names list
def get_interaction_counts(names):
    # Initialize the resultant dictionary
    res = dict()

    # Go through all (name, title) pairs and udpate counters in res
    prev_name = names[0][0]
    prev_title = names[0][1]
    for name, title in names:
        # If a valid chain, increment counters in res
        if prev_name != name and prev_name != 'NA' and name != 'NA' and prev_title == title:
            if prev_name not in res:
                res[prev_name] = {}
            if name not in res[prev_name]:
                res[prev_name][name] = 0
            if name not in res:
                res[name] = {}
            if prev_name not in res[name]:
                res[name][prev_name] = 0
            res[prev_name][name] += 1
            res[name][prev_name] += 1
        # Update prev_ vars 
        prev_name = name
        prev_title = title

    # Return the resultant dictionary with the interaction counts
    return res


if __name__ == "__main__":
    main()