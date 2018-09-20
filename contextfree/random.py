import random


def rnd(diap):
    """returns random number in diapason from -diap  to diap"""
    return (random.random() - 0.5) * 2 * diap


def prnd(diap):
    """returns random number in diapasone from 0 to diap"""
    return random.random() * diap


def coinflip(sides):
    """returns true as if coin with `sides` sides is flipped"""
    coin = random.randint(0, sides - 1)
    if coin == 1:
        return True
    return False
