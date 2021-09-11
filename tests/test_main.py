import logging
import unittest
import numpy as np
from contextfree import init, get_npimage, write_to_png, report, check_limits
from contextfree import circle, box, line, triangle
from contextfree import transform, flip_y
from contextfree.core import MAX_ELEMENTS


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class Tests(unittest.TestCase):

    def test_main(self):
        init(face_color="#123456", background_color="#aaaaaa")
        circle(1)
        a = get_npimage()
        print(a.shape)
        report()
        write_to_png("/tmp/test.png")

    def test_primitives(self):
        init(face_color="#123456", background_color="#aaaaaa")
        line(1, 1)
        triangle(0.5)
        a = get_npimage()
        print(a.shape)
        report()
        write_to_png("/tmp/primitives.png")

    def test_color(self):
        init(face_color="#123456", background_color="#aaaaaa")
        circle(0.5)
        with transform(x=1, alpha=1, hue=10):
            circle(0.5)
        with transform(x=1, y=1, scale=0.6, alpha=-0.3, hue=0):
            circle(0.5)
        with transform(x=-1, y=1, scale=0.6, alpha=0.7, hue=10, saturation=-1, lightness=1):
            circle(0.5)
        with transform(x=-1, y=-1, scale=0.6, alpha=0.7, hue=-10, saturation=-1, lightness=-1):
            circle(0.5)

        write_to_png("/tmp/color.png")

    def test_rotate(self):
        init()
        with transform(angle=0.1):
            box(0.5)
        write_to_png("/tmp/rotate.png")
        a = get_npimage()
        self.assertIsInstance(a, np.ndarray)

    def test_loop(self):
        init(background_color="#000000", face_color="#880000")
        with transform(x=1.2, saturation=0.1, lightness=-0.2, hue=10) as t:
            for i in range(12):
                box()
                t()
        write_to_png("/tmp/loop.png")

    def test_flip(self):
        init()
        with flip_y():
            box(0.5)
        a = get_npimage(y_origin="bottom")
        self.assertIsInstance(a, np.ndarray)

    def test_scale_limit(self):
        @check_limits
        def element():
            circle(1)
            with transform(x=1, scale=0.2):
                element()

        init()
        element()
        write_to_png("/tmp/scale.png")

        @check_limits
        def element_non_recursive():
            pass
        init()
        for i in range(MAX_ELEMENTS + 1):
            element_non_recursive()
