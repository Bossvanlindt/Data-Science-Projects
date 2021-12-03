# For each pony, calculate the tf-idf scores of each word it uses and print the top num_words words
import json
import argparse
import math

def main(): 
    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]

    # Get user inputs in format: 
    # python compute_pony_lang.py -c <pony_counts.json> -n <num_words>
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--counts", help="Path to the json file containing the word counts for each pony", required=True)
    parser.add_argument("-n", "--num_words", help="Number of words to print for each pony", required=True)
    args = parser.parse_args()
    counts = args.counts
    num_words = int(args.num_words)

    # Load the word counts into a dictionary
    with open(counts, 'r') as f:
        word_counts = json.load(f)

    # Get the top num_words words (in terms of tf-idf score) for each pony
    top_words = get_top_words(word_counts, num_words)

    # Remove the tf-idf scores from each word to simply include the word
    for pony in ponies: 
        top_words[pony] = list(top_words[pony].keys())

    # Print the top num_words words to stdout
    print(json.dumps(top_words, indent=4))


# Calculates the tf-idf scores and keeps only the top num_words words for each pony
def get_top_words(word_counts, num_words):
    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]

    # Stores the tf-idf scores for each word for each pony
    tfidf_scores = {}
    # Stores the final top num_words words for each pony
    top_words = {}

    # Go through all words for each pony and save the calculated tf-idf scores in tfidf_scores
    for pony in ponies:
        tfidf_scores[pony] = {}

        # Calculate tf-idf scores for each word
        for word in word_counts[pony]:
            tf = word_counts[pony][word]
            num_of_ponies_using_word = 0
            for pony1 in ponies:
                if word in word_counts[pony1]:
                    num_of_ponies_using_word += 1
            idf = math.log(len(ponies) / num_of_ponies_using_word, 10)
            tfidf_scores[pony][word] = tf * idf

        # Get the top num_words words for each pony
        top_words_for_pony = {word: tfidf_scores[pony][word] for word in sorted(tfidf_scores[pony], key=tfidf_scores[pony].get, reverse=True)[:num_words]}

        # Store the top num_words words for each pony in top_words
        top_words[pony] = top_words_for_pony

    return top_words


if __name__ == '__main__':
    main()