import math
import contextfree as cf


# @cf.rule
def PIC():
    with cf.transform(lightness=1, hue=45, saturation=0.99, alpha=-0.5):
        cf.box()
    with cf.transform(x=1.1, lightness=1, hue=55, saturation=0.99, alpha=-0.6):
        cf.box()
    with cf.transform(y=1.1, lightness=1, hue=40, saturation=1, alpha=-0.6):
        cf.box()
    with cf.transform(x=1.1, y=1.1, lightness=1, hue=50, saturation=0.9, alpha=-0.7):
        cf.box()


@cf.rule()
def PICS():
    PIC()
    with cf.transform(x=1.1, angle=90, hue=0.4):
        PICS()


@cf.rule()
def PICS():
    PIC()
    with cf.transform(x=1.1, angle=-90, hue=0.3, saturation=-0.02):
        PICS()

@cf.rule()
def PICS():
    PIC()
    with cf.transform(x=1.1, angle=180, hue=0.6, alpha=0.1):
        PICS()


@cf.rule()
def PICS():
    PIC()
    with cf.transform(x=1.1, hue=0.41):
        PICS()


@cf.rule(0.041)
def PICS():
    PIC()
    with cf.transform(x=1.1, hue=220):
        PICS()


@cf.rule(0.00000000041)
def PICS():
    PIC()
    with cf.transform(y=-1.1, hue=220):
        PICS()


@cf.rule()
def PICS():
    PIC()
    with cf.transform(y=1.1, angle=90, hue=-0.3, saturation=0.03):
        PICS()


@cf.rule()
def PICS():
    PIC()
    with cf.transform(y=1.1, angle=-90, hue=-0.19):
        PICS()


@cf.rule()
def PICS():
    PIC()
    with cf.transform(y=1.1, angle=180, lightness=0.2, hue=-0.1, saturation=-0.39):
        PICS()


@cf.rule()
def PICS():
    PIC()
    with cf.transform(y=1.1, hue=-0.02):
        PICS()


@cf.rule(0.2)
def PICS():
    PIC()


def main():
    cf.init(canvas_size=(600, 600), face_color="#48d341", background_color="#000000", max_depth=1000)
    PICS()
    cf.write_to_png("/tmp/pics.png")


if __name__ == "__main__":
    main()
