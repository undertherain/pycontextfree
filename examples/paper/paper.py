from contextfree import *


def sheet():
    with transform(scale_x=1.3, lightness=-1, alpha=-0.96):
        box()
    with color(lightness=-1):
        with scale(1.007):
            box()
    box()


@check_limits
def pyramid():
    sheet()
    with rotate(0.09 + rnd(0.02)):
        with scale(0.99):
            with translate(rnd(0.08), rnd(0.08)):
                with color(hue=0.1 + rnd(3)):
                    pyramid()


def main():
    init(canvas_size=(600, 600), face_color="#48d341", max_depth=10000)
    with scale(3):
        pyramid()
    write_to_png("/tmp/paper.png")


if __name__ == "__main__":
    main()
