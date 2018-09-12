"""Unittests for rule feature"""

import logging
import unittest
from contextfree.contextfree import init, register_rule, call_rule


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


@register_rule(1)
def wall():
    """example of one instance of a rule"""
    print("I am a rule 1")


@register_rule(1)
def wall():
    """example of another instance of a rule"""
    print("I am a rule 2")


class Tests(unittest.TestCase):
    """The actual unittest class"""
    def test_rule(self):
        """envoking the rule"""
        init(face_color="#123456", background_color="#aaaaaa")
        call_rule("wall")
        wall()
        with self.assertRaises(NotImplementedError):
            wall("wrong")
