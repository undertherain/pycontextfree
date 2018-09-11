import unittest
from contextfree.contextfree import init, register_rule, call_rule


@register_rule("wall", 1)
def rule():
    print("I am a rule")


class Tests(unittest.TestCase):

    def test_rnd(self):
        init(face_color="#123456", background_color="#aaaaaa")
        call_rule("wall")
        with self.assertRaises(RuntimeError):
            rule()
