import unittest
from contextfree.contextfree import init, get_npimage, write_to_png, circle, translate, color, scale, report, check_limits


class Tests(unittest.TestCase):

    def test_main(self):
        init(face_color="#123456", background_color="#aaaaaa")
        circle(1)
        a = get_npimage()
        print(a.shape)
        report()
        write_to_png("/tmp/test.png")

    def test_color(self):
        init()
        circle(0.5)
        with translate(0.5, 0.5):
            with color(alpha=0.7):
                circle(0.5)
        write_to_png("/tmp/color.png")


    def test_scale_limit(self):
        @check_limits
        def element():
            circle(0.1)
            with translate(0.2, 0):
                with scale(0.5):
                    element()

        init()
        element()
        write_to_png("/tmp/scale.png")
