from contextfree import *


@check_limits
def branch():
    line(0, 1)
    with transform(y=0.95, scale=0.7 + rnd(0.1)):
        if core._state["depth"] == 8:
            with color(hue=0, lightness=-0.2, saturation=0.9, alpha=1):
                box()
        with transform(angle=10 + prnd(20)):
            branch()
        with transform(angle=-10 - prnd(20)):
            branch()


init(canvas_size=(1700, 500), face_color="#ffffff", background_color="#000000", max_depth=9)
with transform(scale=3):
    for row in range(4, 0, -1):
        for i in range(4 + row):
            with transform(x=i * 3 + rnd(1.9),
                           y=row / 4,
                           scale=2 - 0.3 * row,
                           lightness=-row / 10):
                branch()
write_to_png("forest.png")
