"""
Graphite demo
based on CFDG demo by bluesky
https://www.contextfreeart.org/gallery2/#design/561

"""
from contextfree import init, rule, scale, color, box, rotate, translate, write_to_png


# pylint: disable=E0102
@rule(1)
def trunk():
    with scale(0.5):
        with color(hue=0.001):
            branch()


# pylint: disable=E0102
@rule(1)
def branch():
    with rotate(30):
        branch()


# pylint: disable=E0102
@rule(0.01)
def branch():
    line()


# pylint: disable=E0102
@rule(1)
def line():  # {300 * [r .1 x 2] dot {} }
    for i in range(300):
        with rotate(i * 0.1):
            with translate(2 * i, 0):
                dot()


# pylint: disable=E0102
@rule(1)
def dot():
    with translate(0, 0.1):
        dot()


# pylint: disable=E0102
@rule(1)
def dot():
    with rotate(90):
        trail()
    trail()


# pylint: disable=E0102
@rule(0.02)
def dot():
    with rotate(90):
        line()  # {r 90 h 0 }  }


# pylint: disable=E0102
@rule(0.02)
def dot():
    with rotate(90):
        with color(hue=0.01):
            branch()


# pylint: disable=E0102
@rule(1)
def trail():  # { 200    * [y 2 a -0.02] grain {a -.1} }
    for i in range(200):
        with translate(0, 2 * i):
            with color(alpha=0.95 ** i):
                grain()


# pylint: disable=E0102
@rule(1)
def grain():
    gr()


@rule(1)
def gr():
    with translate(1, 0):
        gr()


# pylint: disable=E0102
@rule(1)
def gr():
    with translate(-1, 0):
        gr()


# pylint: disable=E0102
@rule(1)
def gr():
    box()


def main():
    init(canvas_size=(600, 600), background_color="#ffffff", face_color="#0a0707", max_depth=420)
    trunk()
    write_to_png("/tmp/graphite.png")


if __name__ == "__main__":
    main()
