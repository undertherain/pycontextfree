import unittest
from contextfree.contextfree import init, get_npimage, write_to_png, circle


class Tests(unittest.TestCase):

    def test_main(self):
        init(face_color="#123456", background_color="#aaaaaa")
        circle(1)
        a = get_npimage()
        print(a.shape)
        write_to_png("/tmp/test.png")
