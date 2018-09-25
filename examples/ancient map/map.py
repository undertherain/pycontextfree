"""
Ancient Map demo
based on CFDG demo by the same name
https://www.contextfreeart.org/gallery2/#design/185
"""
# import logging
from contextfree import *

# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


# pylint: disable=E0102
@rule(1)
def wall():
    with transform(y=0.95, angle=1, scale_x=0.97):
        wall()


# pylint: disable=E0102
@rule(1)
def wall():
    box()
    with transform(y=0.95, angle=-1, scale_x=0.97, hue=0.1, saturation=0.1, lightness=0.01):
        wall()


# pylint: disable=E0102
@rule(0.09)
def wall():
    # box()
    with transform(y=0.95, scale_x=0.975, angle=90):
        wall()
    with transform(y=0.95, scale_x=0.975, angle=-90):
        wall()


# pylint: disable=E0102
@rule(0.005)
def wall():
    with transform(y=0.97, scale_x=1.5, angle=90):
        wall()
    with transform(y=0.97, scale_x=1.5, angle=-90):
        wall()


def main():
    init(canvas_size=(600, 600), background_color="#e5d5ac", max_depth=122)

    with transform(hue=34, lightness=0.1, saturation=0.25):
        wall()
        with rotate(180):
            wall()

    write_to_png("/tmp/map.png")


if __name__ == "__main__":
    main()
