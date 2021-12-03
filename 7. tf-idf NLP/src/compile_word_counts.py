# For each pony, count the number of times each word is used and save those counts to a file
import os
import pandas as pd
import argparse
import json
import warnings

def main():
    # Ignore warnings from Pandas cuz all works properly
    warnings.filterwarnings("ignore")

    # Get user inputs in format: 
    # python compile_word_counts.py -o <word_counts_json> -d <clean_dialog.csv file>
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output file name", required=True)
    parser.add_argument("-d", "--dialog", help="Dialog file name", required=True)
    args = parser.parse_args()
    # Create output directory if it doesn't exist
    output = args.output
    if not os.path.exists(os.path.dirname(output)):
        if os.path.dirname(output) != '':
            os.makedirs(os.path.dirname(output))
    # Get dialog file
    dialog = args.dialog

    # Load the dialog into a dataframe
    df = pd.read_csv(dialog)
    # Clean the dataframe
    df = clean(df)
    # Calculate the word counts for each pony
    count_dict = word_counts(df)

    # Save the word counts to the output file
    with open(output, 'w') as f:
        f.write(json.dumps(count_dict, indent=4))


# Clean function
def clean(df):
    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]

    # Make all the ponies as well as the dialogs lowercase
    df['pony'] = df['pony'].str.lower()
    df['dialog'] = df['dialog'].str.lower()

    # Drop any row whose pony is not in the list of ponies, thereby getting only valid speech acts
    df = df[df['pony'].isin(ponies)]

    # Replace all the punctuation (( ) [ ] , - . ? ! : ; # &) with a space
    df.loc[:, 'dialog'] = df['dialog'].str.replace('[\(\)\[\]\,\-\.\?\!\:\;\#\&]', ' ')

    # Remove all the stop words as listed in the data/stopwords.txt file
    # Load all stop words into a list
    with open('data/stopwords.txt', 'r') as f:
        stopwords = f.read().splitlines()
    # Remove all the stop words from the dialog column
    df.loc[:, 'dialog'] = df['dialog'].apply(lambda x: ' '.join([word for word in x.split() if word not in stopwords]))

    # Remove all the words that are not alphabetic
    df.loc[:, 'dialog'] = df['dialog'].apply(lambda x: ' '.join([word for word in x.split() if word.isalpha()]))

    return df


# Word counts function
def word_counts(df):
    word_counts = {}

    # Ensure we have an entry for each pony
    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    for pony in ponies:
        if pony not in word_counts:
            word_counts[pony] = {}

    # Iterate through each pony and count the number of occurences of each word
    for pony in df['pony'].unique():
        # Create a dictionary to store the word counts for each pony
        pony_counts = {}
        # Iterate through each word in the dialog
        for word in df[df['pony'] == pony]['dialog'].str.split().sum():
            if word not in pony_counts:
                pony_counts[word] = 1
            else:
                pony_counts[word] += 1
        word_counts[pony] = pony_counts

    # Remove any words that occur less than 5 times
    for pony in word_counts:
        for word in list(word_counts[pony]):
            if word_counts[pony][word] < 5:
                del word_counts[pony][word]

    return word_counts


if __name__ == "__main__":
    main()