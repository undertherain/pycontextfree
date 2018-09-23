from contextfree import *
from math import sqrt

side = 3 / sqrt(3)


@check_limits
def serp():
    triangle()
    with scale(0.5):
        with translate(0, -1):
            serp()
        with translate(side / 2, 0.5):
            serp()
        with translate(-side / 2, 0.5):
            serp()


def main():
    init(canvas_size=(600, 600), background_color="#ffffff", max_depth=8)
    with rotate(60):
        with scale(2):
            serp()
    write_to_png("/tmp/serpinski.png")


if __name__ == "__main__":
    main()
