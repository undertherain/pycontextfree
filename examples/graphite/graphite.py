"""
Graphite demo
based on CFDG demo by bluesky
https://www.contextfreeart.org/gallery2/#design/561

"""
from contextfree import init, rule, box, transform, write_to_png


# pylint: disable=E0102
@rule(1)
def trunk():
    with transform(scale=0.5, hue=0.001):
        branch()


# pylint: disable=E0102
@rule(1)
def branch():
    with transform(angle=30):
        branch()


# pylint: disable=E0102
@rule(0.01)
def branch():
    line()


# pylint: disable=E0102
@rule(1)
def line():  # {300 * [r .1 x 2] dot {} }
    for i in range(300):
        with transform(angle=i * 0.1, x=2 * i):
            dot()


# pylint: disable=E0102
@rule(1)
def dot():
    with transform(y=0.1):
        dot()


# pylint: disable=E0102
@rule(1)
def dot():
    with transform(angle=90):
        trail()
    trail()


# pylint: disable=E0102
@rule(0.02)
def dot():
    with transform(angle=90):
        line()  # {r 90 h 0 }  }


# pylint: disable=E0102
@rule(0.02)
def dot():
    with transform(angle=90, hue=0.01):
        branch()


# pylint: disable=E0102
@rule(1)
def trail():  # { 200    * [y 2 a -0.02] grain {a -.1} }
    for i in range(200):
        with transform(y=2 * i, alpha=-0.5 ** i):
            grain()


# pylint: disable=E0102
@rule(1)
def grain():
    gr()


@rule(1)
def gr():
    with transform(x=1):
        gr()


# pylint: disable=E0102
@rule(1)
def gr():
    with transform(x=-1):
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
