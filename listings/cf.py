from contextfree import *
@check_limits
def branch():
    line(0, 1)
    with translate(0, 0.9):
        with scale(0.7 + rnd(0.15)):
            with color(alpha=0.95):
                with rotate(rnd(40) - 40):
                    branch()
                with rotate(rnd(40) + 40):
                    branch()
init(canvas_size=(300, 300))
branch()
display_ipython()
