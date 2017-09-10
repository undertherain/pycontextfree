import unittest
from contextfree.contextfree import init, get_npimage


class Tests(unittest.TestCase):

    def test_main(self):
        init()
        a = get_npimage()
        print(a.shape)
