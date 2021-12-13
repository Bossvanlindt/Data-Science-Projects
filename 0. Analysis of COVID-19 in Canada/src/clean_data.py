# Clean up the data as follows:
"""
Remove duplicates (of posts and retweets, so do this by id)
Make sure within 3 day window
Keep only location=Canada (maybe?)
Keep only the tweet column
Final result: csv file with single column for tweets
"""
import pandas as pd
import argparse

def main():
    # Get user inputs in format:
    # python3 clean_data.py -i <input_data_file> -o <output_cleaned_data_file>
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input data file", required=True)
    parser.add_argument("-o", "--output", help="Output data file", required=True)
    args = parser.parse_args()
    data_file = args.input
    output = args.output

    # Load the data into a dataframe
    df = pd.read_csv(data_file)
    print(f"df length initial: {len(df)}")

    # Manage duplicates
    # NOTE: I removed duplicates by text instead of id so we get entirely unique posts, retweets therefore excluded, 
    # since we do have enough data to do that and I find that that gives us a bigger range of tweets in terms of content
    # which could be useful for analysis. 
    df = df.drop_duplicates(subset=['text'])
    print(f"df length after removing duplicates by id: {len(df)}")

    # # Ensure the data is within 3 days of each other
    # # Dates are in this format: 2021-11-21 20:24:29+00:00
    # df['time'] = pd.to_datetime(df['time'])
    # # Sort by time
    # df = df.sort_values(by=['time'])
    # # Get the difference between the time of the first and last tweet
    # time_diff = df['time'].iloc[-1] - df['time'].iloc[0]
    # if time_diff > pd.Timedelta(days=3):
    #     print(f"Time difference between first and last tweet: {time_diff}")
    # # NOTE: What matters is that we downloaded the data within a 3 day window, not that 
    # # this data itself is within a 3 day window, right?

    # Manage locations 
    # NOTE: a fair bit of data, due to how we collected it, was from the US (e.g., Alaska and cities near the border)
    # Drop all rows that do not have a location
    df = df[df['location'].notnull()]
    # Keep only the rows with the location matching words in in_canada list (case insensitive)
    # NOTE: This excludes about 2,201 posts where it's not clear if they're in Canada, but still leaves us with 6,289 which is more than enough
    in_canada = ['Canada', 'CA', 'Ontario', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Manitoba', 'British Columbia', 'Prince Edward Island', 'Saskatchewan', 'Alberta', 'Newfoundland', 'Labrador', 'ON', 'QC', 'NS', 'NB', 'MB', 'BC', 'PE', 'SK', 'AB', 'NL']
    df = df[df['location'].str.contains('|'.join(in_canada), case=False)]
    print(f"df length after removing rows with location not in in_canada list: {len(df)}")

    # Take a random sample of 3,000 posts (to limit number of posts to label in coding process)
    df = df.sample(n=3000)

    # Keep only the text column
    df = df[['text']]

    # Save the dataframe to a csv file
    df.to_csv(output, index=False)


if __name__ == '__main__':
    main()