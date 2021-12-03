# Scrape the relationships of the target individuals (outlined in the config file)
# using the beautiful soup library and write the results to a output file.
# Cache the target individuals' whosdatedwho page to avoid unnecessary requests.
import bs4
import requests
import argparse
import json
import os

# Main function handles user inputs, calls the scrape function and writes 
# the results to a file.
def main():
    # Get the user input
    parser = argparse.ArgumentParser(description='Scrape the relationships of the target individuals outlined in the config file.')
    parser.add_argument('-c', '--config', help='The config file to use (.json).', required=True)
    parser.add_argument('-o', '--output', help='The output file to write the results to (.json).', required=True)
    args = parser.parse_args()

    # Load the config file
    config = json.load(open(args.config))

    # Create the cache directory using the config file 
    cache_dir = config['cache_dir']
    # If it doesn't exist, create it
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Dictionary to store the results
    results = {}

    # Loop through every target person in the config, scrape their whosdatedwho 
    # page and store results in a dictionary
    for target_name in config['target_people']:
        # Get the target's whosdatedwho page's cache file
        target_cache_file = os.path.join(cache_dir, target_name + '.html')
        
        # If the cache file doesn't exist, scrape the page and write it to the cache file
        if not os.path.exists(target_cache_file):
            # Scrape the page
            target_soup = scrape_page(target_name)
            # Write the soup to the cache file
            with open(target_cache_file, 'w') as f:
                f.write(str(target_soup))
        # If the cache file does exist, load it
        else:
            with open(target_cache_file, 'r') as f:
                target_soup = bs4.BeautifulSoup(f.read(), 'html.parser')

        # Get the target's relationships
        target_relationships = scrape_relationships(target_soup)

        # Append those relationships to the final dictionary
        results[target_name] = target_relationships

    # Write the target's relationships to the output file as json dump
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)
        

# Scrape the page if needed
def scrape_page(target_name):
    # Get the target's whosdatedwho page
    target_whosdatedwho_url = 'https://www.whosdatedwho.com/dating/' + target_name
    target_whosdatedwho_page = requests.get(target_whosdatedwho_url)
    target_soup = bs4.BeautifulSoup(target_whosdatedwho_page.text, 'html.parser')
    return target_soup


# Scrape the relationships of the target individual
def scrape_relationships(target_soup):
    # Go to the h4 tag with the ff-auto-relationships class
    relationships_tag = target_soup.find('h4', 'ff-auto-relationships')

    # Extract the text content of each a href tag in every subsequent p tag until we hit a non-p tag
    relationships = []
    while True:
        relationships_tag = relationships_tag.next_sibling
        if relationships_tag.name != 'p':
            break
        # Get the text content of each a href tag in the p tag
        for a_tag in relationships_tag.find_all('a'):
            # Format the name properly
            person = a_tag.text.lower().replace(' ', '-')
            relationships.append(person)

    return relationships


if __name__ == '__main__':
    main()