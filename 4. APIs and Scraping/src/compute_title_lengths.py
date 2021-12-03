# Calculate average title length for each reddit post in the json file
import json
import argparse

# Main function takes as input the json file and outputs the average title length
def main():
    # Get the json file from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("sample_json_file", help="The json file to process")
    args = parser.parse_args()
    json_file = args.sample_json_file 

    # Open the json file
    with open(json_file) as f:
        # List to keep track of lengths
        total_length = 0
        num_of_titles = 0

        # Loop through each post in the json file
        for line in f:
            post = json.loads(line)
            total_length += len(post['data']['title'])
            num_of_titles += 1

        # Calculate the average title length
        average_title_length = total_length / num_of_titles

        # Print the average title length to two decimal points
        print("{:.2f}".format(round(average_title_length, 2)))


if __name__ == "__main__":
    main()