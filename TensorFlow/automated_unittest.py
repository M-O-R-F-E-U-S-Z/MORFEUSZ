import unittest
import pandas as pd
import main

class Tests(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv('Archive/MovieGenre.csv', encoding='ISO-8859-1')
        classes = []
        for genres in self.df["Genre"].values:
            try:
                classes += genres.split('|')
            except:
                pass
        classes = set(classes)
        self.classes = classes

    def test_genres(self):
        check = all(i in self.classes for i in main.CLASSES)
        self.assertTrue(check)

if __name__ == '__main__':
    unittest.main()
  
