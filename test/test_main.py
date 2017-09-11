import unittest
from contextfree.contextfree import init, get_npimage, write_to_png, circle, translate, color


class Tests(unittest.TestCase):

    def test_main(self):
        init(face_color="#123456", background_color="#aaaaaa")
        circle(1)
        a = get_npimage()
        print(a.shape)
        write_to_png("/tmp/test.png")

    def test_color(self):
        init()
        circle(0.5)
        with translate(1, 1):
            with color(alpha=0.5):
                circle(0.5)
        write_to_png("/tmp/color.png")
