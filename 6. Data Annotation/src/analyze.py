# Outputs the number of each category that appears in your annotated files
import pandas as pd
import json
import argparse
import os

def main(): 
    # Get user input with optional output file with this format:
    # python3 analyze.py -i <coded_file.tsv> [-o <output_file>]
    parser = argparse.ArgumentParser(description='Analyze the number of each category in the annotated file')
    parser.add_argument('-i', '--input', help='The input file to analyze', required=True)
    parser.add_argument('-o', '--output', help='The output file to write to', required=False)
    args = parser.parse_args()
    input = args.input
    output = args.output

    # Load the input file into a dataframe
    df = pd.read_csv(input, sep='\t')

    # Get counts for each category in the coding column
    counts_dict = { 
        'course-related': 0, 
        'food-related': 0, 
        'residence-related': 0, 
        'other': 0
        }    
    
    for label in df['coding']:
        if label == 'o': 
            counts_dict['other'] += 1
        elif label == 'f': 
            counts_dict['food-related'] += 1
        elif label == 'r': 
            counts_dict['residence-related'] += 1
        else: 
            counts_dict['course-related'] += 1

    # If we have an output file, write the counts to it. Else, print to stdout. 
    if output:
        # Create the directory if it doesn't exist
        if not os.path.exists(os.path.dirname(output)):
            if os.path.dirname(output) != '':
                os.makedirs(os.path.dirname(output))
        with open(output, 'w') as f:
            json.dump(counts_dict, f, indent=4)
    else:
        print(json.dumps(counts_dict, indent=4))
    

if __name__ == "__main__":
    main()