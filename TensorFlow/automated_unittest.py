import unittest
import main

class Tests(unittest.TestCase):
    def test_classes(self):
        self.assertEqual(main.CLASSES, 5)

if __name__ == '__main__':
    unittest.main()
