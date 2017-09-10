import unittest
from contextfree.contextfree import init, get_npimage, write_to_png, circle


class Tests(unittest.TestCase):

    def test_main(self):
        init(background_color="#aaaaaa")
        circle(1)
        a = get_npimage()
        print(a.shape)
        write_to_png("test.png")
