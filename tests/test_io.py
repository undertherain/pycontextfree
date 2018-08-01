import unittest
from contextfree.contextfree import circle
from contextfree.contextfree import init, display_ipython


class Tests(unittest.TestCase):

    def test_ipython(self):
        init(face_color="#123456", background_color="#aaaaaa")
        circle(1)
        display_ipython()
        # a = get_npimage()
        # print(a.shape)
        # report()
        # write_to_png("/tmp/test.png")
