from random import seed

from contextfree import *

seed(0)


@check_limits
def branch():
    line(0, 1)
    with transform(y=0.9, scale=0.7 + rnd(0.1), alpha=-0.05):
        # TODO: need a less hacky way to do it
        if core._state["depth"] == 8:
            # TODO: need an API to set absolute color
            with color(hue=90, lightness=0.6, saturation=1, alpha=1):
                box()
        with transform(angle=20 + prnd(20)):
            branch()
        with transform(angle=-20 - prnd(20)):
            branch()


init(canvas_size=(400, 400), face_color="#542500", background_color="#FFFFFF", max_depth=9)
with transform(scale=3):
    branch()
write_to_png("tree.png")
