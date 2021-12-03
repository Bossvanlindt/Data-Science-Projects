import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
# sys.path.append(parentdir)
sys.path.append(os.path.join(parentdir, 'src'))
import clean
import json

# Contains unit tests for the clean.py script, testing against the test_data directory
class CleanTest(unittest.TestCase):
    def setUp(self):
        # Load the fixture files as variables, and test your code against them
        self.test_data_dir = Path(parentdir, 'test', 'fixtures')
        
    # Test if posts that don't have a title are removed using test_1.json in the test/fixtures directory
    def test_title(self):
        print("\nFile without title or title_text gets removed")
        # Open test_1.json and clean its first line
        with open(os.path.join(self.test_data_dir, 'test_1.json'), 'r') as f:
            unittest.TestCase.assertEqual(self, clean.clean(f.readline()), None)
        print("OK")

    # createdAt dates that don’t pass the ISO datetime standard should be removed
    def test_createdAt(self):
        print("\nFile with createdAt date that does not pass the ISO datetime standard gets removed")
        # Open test_2.json and clean its first line
        with open(os.path.join(self.test_data_dir, 'test_2.json'), 'r') as f:
            unittest.TestCase.assertEqual(self, clean.clean(f.readline()), None)
        print("OK")

    # Any lines that contain invalid JSON dictionaries should be ignored
    def test_invalid_json(self):
        print("\nFile containing invalid JSON dictionary gets ignored")
        # Open test_3.json and clean its first line
        with open(os.path.join(self.test_data_dir, 'test_3.json'), 'r') as f:
            unittest.TestCase.assertEqual(self, clean.clean(f.readline()), None)
        print("OK")

    # Any lines for which "author" is null, N/A or empty should be removed
    def test_author(self):
        print("\nFile containing invalid author gets removed")
        # Open test_4.json and clean its first line
        with open(os.path.join(self.test_data_dir, 'test_4.json'), 'r') as f:
            unittest.TestCase.assertEqual(self, clean.clean(f.readline()), None)
        print("OK")

    # total_count is a string containing a cast-able number, total_count is cast to an int properly
    def test_total_count(self):
        print("\nFile containing an invalid total_count format gets removed")
        # Open test_5.json and clean its first line
        with open(os.path.join(self.test_data_dir, 'test_5.json'), 'r') as f:
            unittest.TestCase.assertEqual(self, clean.clean(f.readline()), None)
        print("OK")

    # The tags field gets split on spaces when given a tag containing THREE words (e.g., “nba basketball game”)
    def test_tags(self):
        print("\nTags of the file's JSON dictionary get split into a list of individual words")
        # Open test_6.json and clean its first line
        with open(os.path.join(self.test_data_dir, 'test_6.json'), 'r') as f:
            line = f.readline()
            # Read the first line of the file to a dictionary
            json_dict = json.loads(line)
            # Split tags list into individual words
            if 'tags' in json_dict:
                list_of_split_tags = [x.split() for x in json_dict['tags']]
                # Flatten the list of lists into a single list
                json_dict['tags'] = [item for sublist in list_of_split_tags for item in sublist]

            # Compare only the tags field of the cleaned json dict to the json dict formatted above
            unittest.TestCase.assertEqual(self, json.loads(clean.clean(line))['tags'], json_dict['tags'])
        print("OK")

    
if __name__ == '__main__':
    unittest.main()