import unittest
import plotting

class Tests(unittest.TestCase):
    def test_extension(self):
        self.assertIn(plotting.EXTENSION, ['.pdf','.eps','.png'])

    def test_font(self):
        self.assertEqual(plotting.plt.rcParams['font.size'], plotting.FONT)

    def test_ticks(self):
        self.assertEqual(plotting.plt.rcParams['xtick.labelsize'], plotting.XTICK)
        self.assertEqual(plotting.plt.rcParams['ytick.labelsize'], plotting.YTICK)

if __name__ == '__main__':
    unittest.main()
