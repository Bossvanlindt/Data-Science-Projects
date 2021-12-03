import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.compile_word_counts import clean, word_counts
from src.compute_pony_lang import get_top_words
import pandas as pd
import json
import warnings



class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        


    def test_task1(self):
        # Ignore warnings from Pandas cuz all works properly
        warnings.filterwarnings("ignore")
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and
        #  write your own assertion, i.e. self.assertEquals(...)
        
        # Load the dialog into a dataframe
        df = pd.read_csv(self.mock_dialog)
        # Clean the dataframe
        df = clean(df)
        # Calculate the word counts for each pony
        count_dict = word_counts(df)

        # Load the true word counts
        with open(self.true_word_counts) as f:
            true_count_dict = json.load(f)

        # Assert if the word counts are equal
        self.assertEqual(count_dict, true_count_dict)

        

    def test_task2(self):
        warnings.filterwarnings("ignore")
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and 
        # write your own assertion, i.e. self.assertEquals(...)

        # Load the word counts into a dictionary
        with open(self.true_word_counts, 'r') as f:
            word_counts = json.load(f)

        # Get the top num_words words (in terms of tf-idf score) for each pony
        top_words = get_top_words(word_counts, 3)

        # Get the true top words
        with open(self.true_tf_idfs, 'r') as f:
            true_top_words = json.load(f)

        # Assert if the top words are equal
        self.assertEqual(top_words, true_top_words)
        
        
    
if __name__ == '__main__':
    unittest.main()