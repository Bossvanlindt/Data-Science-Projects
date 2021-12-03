# Collect top 1000 reddit posts, 100 per subreddit, and save the json outputs
# Do this in two sampling ways
import json
import requests
import requests.auth

# Main function creates two samples json files and handles request authentification
def main():
    # Get the reddit token
    token = get_token()

    # Two samples to create
    sample_1_subreddits = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
    sample_2_subreddits = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']

    # Get the sample data for each subreddit list
    sample_1_data = get_sample(sample_1_subreddits, token)
    sample_2_data = get_sample(sample_2_subreddits, token)

    # Write the sample data to json files
    with open('sample1.json', 'w') as outfile:
        # With one dictionary inside the data list per line
        for post in sample_1_data:
            json.dump(post, outfile)
            outfile.write('\n')
    with open('sample2.json', 'w') as outfile:
        for post in sample_2_data:
            json.dump(post, outfile)
            outfile.write('\n')


# Get the reddit token to use in the requests
def get_token():
    client_auth = requests.auth.HTTPBasicAuth('DmiVJhJ7oPdnQ7OLN7dCjg', '1Zcr-9v84YA8YNHmaqqM6aN2_GEakQ')
    post_data = {"grant_type": "password", "username": "Exact-Attorney-1323", "password": "hornek-sogbem-2gUrre"}
    headers = {"User-Agent": "script:comp_598_assignment:v1.0 (by /u/Exact-Attorney-1323)"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json()["access_token"]


# Get the top 1000 posts, with 100 per subreddit
def get_sample(subreddits, token):
    # Create a list of dictionaries to store the data
    data = []
    headers = {"Authorization": f"bearer {token}", "User-Agent": "script:comp_598_assignment:v1.0 (by /u/Exact-Attorney-1323)"}

    # Iterate through the subreddits
    for subreddit in subreddits:
        # Get the json data from the subreddit using oauth
        response = requests.get('https://oauth.reddit.com/r/' + subreddit + '/new.json?limit=100', headers=headers)
        json_data = json.loads(response.text)
        # Iterate through the posts
        for post in json_data['data']['children']:
            data.append(post)

    return data


if __name__ == '__main__':
    main()