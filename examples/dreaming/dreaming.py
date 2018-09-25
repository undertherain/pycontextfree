"""
Based on `dreaming` CFDG demo by mountain
https://www.contextfreeart.org/gallery2/index.html#design/2508
"""

from contextfree import *


@rule()
def lines():
    with transform(x=8, scale_x=0.8, hue=20):
        lines()
    with transform(scale_x=0.1, alpha=-0.6, lightness=1, saturation=1):
        sq()


@rule()
def lines():
    with transform(angle=90, x=8, scale_x=0.8, hue=20):
        lines()
    with transform(angle=-90, x=8, scale_x=0.8, hue=20):
        lines()
    with transform(scale_x=0.1, alpha=-0.6, lightness=1, saturation=1):
        sq()


@rule()
def lines():
    with transform(angle=90, y=8, scale_x=0.8, hue=20):
        lines()
    with transform(scale_x=0.1, alpha=-0.6, lightness=1, saturation=1):
        sq()


@rule()
def lines():
    with transform(angle=90, y=8, scale_x=0.8, hue=20):
        lines()
    with transform(angle=-90, y=8, scale_x=0.8, hue=20):
        lines()
    with transform(scale_x=0.1, alpha=-0.6, lightness=1, saturation=1):
        sq()


@rule()
def lines():
    with transform(angle=90, x=8, scale_x=0.8, hue=20):
        lines()
    with transform(angle=-90, y=8, scale_x=0.8, hue=10):
        lines()
    with transform(scale_x=0.1, alpha=-0.6, lightness=1, saturation=1):
        sq()


@rule()
def lines():
    with transform(angle=90, y=8, scale_x=0.8, hue=20):
        lines()
    with transform(angle=-90, x=8, scale_x=0.8, hue=10):
        lines()
    with transform(scale_x=0.1, alpha=-0.6, lightness=1, saturation=1):
        sq()


@rule()
def sq():
    with transform(lightness=0):
        thin()
    with transform(scale_x=0.99, x=0.5, y=0.5, lightness=0.1):
        thin()
    with transform(scale_x=0.98, x=0.5, y=0.5, lightness=0.2):
        thin()
    with transform(scale_x=0.97, x=1, y=1, lightness=0.3):
        thin()
    with transform(scale_x=0.96, x=1, y=1, lightness=0.4):
        thin()
    with transform(scale_x=0.95, x=2, y=2, lightness=0.5):
        thin()
    with transform(scale_x=0.94, x=2, y=2, lightness=0.6):
        thin()
    with transform(scale_x=0.93, x=3, y=3, lightness=0.7):
        thin()
    with transform(scale_x=0.92, x=3, y=3, lightness=0.8):
        thin()
    with transform(scale_x=0.91, x=4, y=4, lightness=0.9):
        thin()
    with transform(scale_x=0.9, x=5, y=5, lightness=1):
        thin()


@rule()
def thin():
    angle()
    with transform(x=103, y=-90):
       with transform(angle=136):
            with flip_y():
                with transform(angle=-136):
                    angle()
    #     angle {flip 136 x 103 y 90}


def angle():
    fuzz()
    with transform(angle=44):
        with flip_y():
            with transform(angle=-44):
                fuzz()


def fuzz():
    ln()


def ln():
    with transform(x=2) as t:
        for _ in range(50):
            gr()
            t()


@rule()
def gr():
    with transform(y=1):
        gr()


@rule()
def gr():
    with transform(x=1):
        bit()


def bit():
    box()


def main():
    init(canvas_size=(600, 600), background_color="#000000", max_depth=12)
    lines()
    write_to_png("/tmp/dreaming.png")


if __name__ == "__main__":
    main()
