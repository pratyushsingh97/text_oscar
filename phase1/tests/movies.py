import retrieve_movie

import unittest 
import logging
import sys
import random
import string

class Movies(unittest.TestCase):
    # Test Case 1 - No Movie Passed
    def test_no_movie_title(self):
        self.assertEqual(retrieve_movie.get_movie_metadata(''), "Pass a movie title")

    def test_no_movie_title_multiple_spaces(self):
        self.assertEqual(retrieve_movie.get_movie_metadata('     '), 'Pass a movie title')

    # Test Case 2 - A Movie that doesn't exist
    def test_non_existant_movie(self):
        random_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        expected = f"Unable to retrieve {random_str}"
        self.assertEqual(retrieve_movie.get_movie_metadata(random_str), expected)


    # Test Case 3 - Valid Movie 
  
if __name__ == '__main__': 
    logging.basicConfig( stream=sys.stderr)
    logging.getLogger( "Movies").setLevel(logging.DEBUG)
    
    unittest.main() 
    
    print(s)