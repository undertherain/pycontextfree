from contextfree import *


def sheet():
    with transform(scale=1.3, lightness=-1, alpha=-0.96):
        box()
    with transform(scale=1.007, lightness=-1):
        box()
    box()


@check_limits
def pyramid():
    sheet()
    with transform(scale=0.99, angle=1 + prnd(1), x=rnd(0.1), y=rnd(0.1), hue=rnd(5)):
        pyramid()


def main():
    init(canvas_size=(600, 600), face_color="#48d341", max_depth=10000)
    with transform(scale=3, angle=rnd(90), hue=prnd(360)):
        pyramid()
    write_to_png("/tmp/paper.png")


if __name__ == "__main__":
    main()
