from contextfree.contextfree import *
@check_limits
def branch():
    line(0, 1)
    with translate(0, 0.9):
        with scale(0.7 + rnd(0.3)):
            with rotate(-0.4 + rnd(0.5)):
                branch()
            with rotate(0.4 + rnd(0.5)):
                branch()
init(canvas_size=(300, 300))
branch()
display_ipython()