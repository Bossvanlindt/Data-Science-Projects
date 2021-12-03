# Calculate the words most characteristic of each Pony using tf-idf

Using a My Little Pony script, we start by compiling the word counts (via compile_word_counts.py) said by each pony in the script and saving that in word_counts.json (stop words have been removed for more meaningful results). 

Using these word counts, we can calculate the tf-idf scores of each word for every pony and print the top x words for each pony using the compute_pony_lang.py script. 