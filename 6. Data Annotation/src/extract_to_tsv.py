# Print a random number (given by the user) of lines from the input file to the 
# output file or the command line
import pandas as pd
import json
import argparse
import os

# Main function gets user inputs and calls the extract_to_tsv function
def main(): 
    # Get input of this format, where the output file is optional
    #  python3 extract_to_tsv.py -o <out_file> <json_file> <num_posts_to_output>
    parser = argparse.ArgumentParser(description='Extract a random number of posts from the file to a tsv file')
    parser.add_argument('-o', '--out_file', help='Output file name', required=False)
    parser.add_argument('json_file', help='Input json file')
    parser.add_argument('num_posts_to_output', help='Number of posts to output')
    args = parser.parse_args()
    output = args.out_file
    json_file = args.json_file
    num_posts = args.num_posts_to_output

    # Extract the posts from the json file
    df = extract_to_tsv(json_file, num_posts)

    # If no output file is given, print to the command line
    if output is None:
        print(df)
    else:
        # Create the directory if it doesn't exist
        if not os.path.exists(os.path.dirname(output)):
            if os.path.dirname(output) != '':
                os.makedirs(os.path.dirname(output))
        df.to_csv(output, sep='\t', index=False)


# Extract the posts from the json file and return a dataframe
def extract_to_tsv(json_file, num_posts):
    # Read the file line by line and extract the data dictionary from each line
    with open(json_file, 'r') as f:
        data = [json.loads(line)['data'] for line in f]

    df = pd.DataFrame(data)

    # Select num_posts random posts from the json file
    # If num_posts is greater than the number of posts in the json file, get everything
    if int(num_posts) > len(df):
        num_posts = len(df)
    df = df.sample(n=int(num_posts))

    # Rename the name column to Name
    df.rename(columns={'name': 'Name'}, inplace=True)
    # Drop all but the Name and title columns
    df = df[['Name', 'title']]
    # Add an empty column called coding
    df['coding'] = ''

    return df


if __name__ == "__main__":
    main()