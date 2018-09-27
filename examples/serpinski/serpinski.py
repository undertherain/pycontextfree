from contextfree import *
from math import sqrt

side = 3 / sqrt(3)


@check_limits
def serp():
    triangle()
    with transform(angle=120, saturation=0.3, lightness=0.1, hue=3) as t:
        for _ in range(3):
            with transform(scale=0.5, y=-0.5):
                serp()
            t()


def main():
    init(canvas_size=(600, 600), background_color="#ffffff", max_depth=11)
    with transform(angle=60, scale=2):
        serp()
    write_to_png("/tmp/serpinski.png")


if __name__ == "__main__":
    main()
