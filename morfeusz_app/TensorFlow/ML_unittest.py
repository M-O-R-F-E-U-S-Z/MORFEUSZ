import unittest
import main

class Tests(unittest.TestCase):
    def test_classes(self):
        self.assertEqual(len(main.CLASSES), 5)

    def test_network_parameters(self):
        self.assertIn(main.layer_sizes[0], [128])
        self.assertIn(main.conv_layers[0], [3,4,5])
        self.assertIn(main.dense_layers[0], [1,2,3])

    def test_minimal_epochs(self):
        min_epochs = 5
        self.assertTrue(main.epochs>min_epochs)

    def test_training_classes(self):
        self.assertEqual(main.CLASSES, main.training.CLASSES)

    def test_model_extention(self):
        self.assertEqual(main.analysis.MODEL_EXTENSION, '.hp5')

if __name__ == '__main__':
    unittest.main()
