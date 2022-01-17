
from rubiks_color_resolver.base import (
    get_swap_count,
    rgb2lab,
)
from rubiks_color_resolver import (
    hex_to_rgb,
    median,
)
import logging
import unittest
import sys



log = logging.getLogger(__name__)

# For color names to RGB values see:
# https://www.w3schools.com/colors/colors_names.asp


class TestHex2RGB(unittest.TestCase):
    def test_white(self):
        (red, green, blue) = hex_to_rgb("#FFFFFF")
        self.assertEqual(red, 255)
        self.assertEqual(green, 255)
        self.assertEqual(blue, 255)

    def test_black(self):
        (red, green, blue) = hex_to_rgb("#000000")
        self.assertEqual(red, 0)
        self.assertEqual(green, 0)
        self.assertEqual(blue, 0)

    def test_slate_gray(self):
        (red, green, blue) = hex_to_rgb("#708090")
        self.assertEqual(red, 112)
        self.assertEqual(green, 128)
        self.assertEqual(blue, 144)


class TestRGB2Lab(unittest.TestCase):
    def test_white(self):
        lab = rgb2lab((255, 255, 255))
        self.assertEqual(lab.L, 100.0)
        self.assertEqual(lab.a, 0.00526049995830391)
        self.assertEqual(lab.b, -0.010408184525267927)

    def test_black(self):
        lab = rgb2lab((0, 0, 0))
        self.assertEqual(lab.L, 0.0)
        self.assertEqual(lab.a, 0.0)
        self.assertEqual(lab.b, 0.0)

    def test_red(self):
        lab = rgb2lab((255, 0, 0))
        self.assertEqual(lab.L, 53.23288178584245)
        self.assertEqual(lab.a, 80.10930952982204)
        self.assertEqual(lab.b, 67.22006831026425)

    def test_green(self):
        lab = rgb2lab((0, 255, 0))
        self.assertEqual(lab.L, 87.73703347354422)
        self.assertEqual(lab.a, -86.18463649762525)
        self.assertEqual(lab.b, 83.18116474777854)

    def test_blue(self):
        lab = rgb2lab((0, 0, 255))
        self.assertEqual(lab.L, 32.302586667249486)
        self.assertEqual(lab.a, 79.19666178930935)
        self.assertEqual(lab.b, -107.86368104495168)

    def test_slate_gray(self):
        lab = rgb2lab(hex_to_rgb("#708090"))
        self.assertEqual(lab.L, 52.83625796271889)
        self.assertAlmostEqual(lab.a, -2.1385958505868996, places=15)
        self.assertEqual(lab.b, -10.57740141476744)



class TestMedian(unittest.TestCase):
    def test_empty_list(self):
        m = median([])
        self.assertIsNone(m)

    def test_list_of_one(self):
        m = median([7])
        self.assertEqual(m, 7)

    def test_list_of_two(self):
        m = median([8, 7])
        self.assertEqual(m, 7.5)

    def test_list_of_three(self):
        m = median([7, 9, 8])
        self.assertEqual(m, 8)

    def test_list_of_four(self):
        m = median([9, 8, 7, 10])
        self.assertEqual(m, 8.5)


class TestSwapCount(unittest.TestCase):
    def test_zero(self):
        swaps = get_swap_count([1, 2, 3, 0, 4], [1, 2, 3, 0, 4])
        self.assertEqual(swaps, 0)

    def test_even(self):
        # swap 1 and 3
        # swap 2 and 4
        swaps = get_swap_count([1, 2, 3, 0, 4], [3, 4, 1, 0, 2])
        self.assertEqual(swaps, 2)

    def test_odd(self):
        # swap 2 and 4
        swaps = get_swap_count([1, 2, 3, 0, 4], [1, 4, 3, 0, 2])
        self.assertEqual(swaps, 1)


if __name__ == "__main__":

    # setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(filename)16s %(levelname)8s: %(message)s",
    )
    log = logging.getLogger(__name__)

    # micropython does not support the verbosity arg but
    # does give more verbose output by default so just ignore
    # the exception
    try:
        unittest.main(verbosity=2)
    except TypeError:
        unittest.main()
