# Collect top 100 reddit posts, 100 per university, and save the outputs
import requests
import requests.auth
import json
import argparse
import os

# Main function creates two samples json files and handles request authentification
def main():
    # Get the reddit token
    token = get_token()

    # Get user inputs from command line of format: 
    # python3 collect_newest.py -o <output_file> -s <subreddit>
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="output file name", required=True)
    parser.add_argument("-s", "--subreddit", help="subreddit name", required=True)
    args = parser.parse_args()
    subreddit = args.subreddit
    output = args.output

    # Get the sample data 
    sample_data = get_sample(subreddit, token)

    # Write the sample data to json files
    # Create the directory if it doesn't exist
    if not os.path.exists(os.path.dirname(output)):
        if os.path.dirname(output) != '':
            os.makedirs(os.path.dirname(output))
    with open(output, 'w') as outfile:
        # With one dictionary inside the data list per line
        for post in sample_data:
            json.dump(post, outfile)
            outfile.write('\n')


# Get the reddit token to use in the requests
def get_token():
    client_auth = requests.auth.HTTPBasicAuth('DmiVJhJ7oPdnQ7OLN7dCjg', '1Zcr-9v84YA8YNHmaqqM6aN2_GEakQ')
    post_data = {"grant_type": "password", "username": "Exact-Attorney-1323", "password": "INSERT_PASSWORD"}
    headers = {"User-Agent": "script:data_annotation:v1.0 (by /u/Exact-Attorney-1323)"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json()["access_token"]


# Get the top 100 posts from a subreddit
def get_sample(subreddit, token):
    # Create a list of dictionaries to store the data
    data = []
    headers = {"Authorization": f"bearer {token}", "User-Agent": "script:data_annotation:v1.0 (by /u/Exact-Attorney-1323)"}

    # Get the json data from the subreddit using oauth
    response = requests.get('https://oauth.reddit.com' + subreddit + '/new.json?limit=100', headers=headers)
    json_data = json.loads(response.text)
    # Iterate through the posts
    for post in json_data['data']['children']:
        data.append(post)

    return data


if __name__ == '__main__':
    main()