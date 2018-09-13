"""
Ancient Map demo
based on CFDG demo by the same name
https://www.contextfreeart.org/gallery2/#design/185
"""
import logging
import math
from contextfree.contextfree import *


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


# pylint: disable=E0102
@rule(1)
def wall():
    with translate(0.95, 0):
        with rotate(0.01):
            with scale(0.975):
                ancient_map()


# pylint: disable=E0102
@rule(1)
def wall():
    box()
    with translate(0.95, 0):
        with rotate(-0.0027):
            with scale(0.975):
                with color(hue=0.001, saturation=0.1, lightness=0.003):
                    ancient_map()


# pylint: disable=E0102
@rule(0.09)
def wall():
    box()
    with scale(0.975):
        with translate(0.95, 0):
            with rotate(math.pi / 2):
                ancient_map()
            with rotate(- math.pi / 2):
                ancient_map()


# pylint: disable=E0102
@rule(0.05)
def wall():
    with translate(0.97, 0):
        with scale(1.5):
            with rotate(math.pi / 2):
                ancient_map()
            with rotate(- math.pi / 2):
                ancient_map()


@check_limits
def ancient_map():
    wall()


def main():
    init(canvas_size=(600, 600), background_color="#e5d5ac", face_color="#0a0707", max_depth=120)

    ancient_map()
    with rotate(math.pi / 2):
        ancient_map()

    write_to_png("/tmp/map.png")


if __name__ == "__main__":
    main()
