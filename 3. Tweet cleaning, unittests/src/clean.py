# Load .json file and clean it
import json
import datetime
import argparse


# Function takes as input a json string and returns a cleaned json string
def clean(json_string):
    # Load json_string into a dictionary if it is a valid json string
    try:
        json_dict = json.loads(json_string)
    except:
        return None

    # Return None if the json_dict does not have either the title or title_text key
    if 'title' not in json_dict and 'title_text' not in json_dict:
        return None

    # If it has a title_text key, replace it with the title key
    if 'title_text' in json_dict:
        json_dict['title'] = json_dict['title_text']
        del json_dict['title_text']

    # Standardize the createdAt datetime (of format "2020-10-19T02:56:51+0000") 
    # to the UTC timezone and return None if it is not a valid datetime
    if 'createdAt' in json_dict:
        try:
            json_dict['createdAt'] = datetime.datetime.strptime(json_dict['createdAt'], "%Y-%m-%dT%H:%M:%S%z").astimezone(datetime.timezone.utc).isoformat()
        except ValueError:
            return None

    # Return None if the author field is empty, null, or N/A
    if 'author' in json_dict and json_dict['author'] in ['', None, 'N/A']:
        return None

    # If total_count is not of type int, float, or string, return None
    if 'total_count' in json_dict and not isinstance(json_dict['total_count'], (int, float, str)):
        return None
    # Cast total_count to int if it is of type float
    elif isinstance(json_dict['total_count'], float):
        json_dict['total_count'] = int(json_dict['total_count'])
    # Cast total_count to int since it is of type string
    else:
        try:
            json_dict['total_count'] = int(json_dict['total_count'])
        except ValueError:
            return None

    # If there is a tags field, for each tag, split it into individual words
    # and save all words as a list
    if 'tags' in json_dict:
        list_of_split_tags = [x.split() for x in json_dict['tags']]
        # Flatten the list of lists into a single list
        json_dict['tags'] = [item for sublist in list_of_split_tags for item in sublist]

    # Return json_dict as a string
    return json.dumps(json_dict)


# Main function goes line by line through input file, 
# calls clean function and writes cleaned json string to output file.
# Inputs are given as command line arguments using the argparse module.
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Clean .json file')
    parser.add_argument('-i', '--input', help='Input .json file', required=True)
    parser.add_argument('-o', '--output', help='Output .json file', required=True)
    args = parser.parse_args()

    # Open input file, clean each line, and write to output file
    with open(args.input, 'r') as input_file, open(args.output, 'w') as output_file:
        for line in input_file:
            cleaned_line = clean(line)
            if cleaned_line:
                output_file.write(cleaned_line + '\n')

    # Exit program
    exit()


if __name__ == '__main__':
    main()