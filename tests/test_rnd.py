import unittest
from contextfree.contextfree import circle
from contextfree.contextfree import init
from contextfree.contextfree import rnd, prnd, coinflip


class Tests(unittest.TestCase):

    def test_rnd(self):
        init(face_color="#123456", background_color="#aaaaaa")
        circle(1)
        res = rnd(1)
        self.assertLess(res, 1.01)
        res = prnd(1)
        self.assertLess(res, 1.01)
        res = coinflip(2)
        self.assertIn(res, [True, False])
        res = coinflip(1)
        self.assertEqual(res, False)
