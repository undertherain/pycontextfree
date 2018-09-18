from contextfree.contextfree import *


@check_limits
def branch():
    circle(1)
    with translate(0, 0.65):
        with color(alpha=0.998):
            with rotate(0.03):
                with scale(0.997):
                    if coinflip(50):
                        with flip_y():
                            branch()
                    else:
                        branch()
            if coinflip(60):
                with flip_y():
                    with scale(0.9):
                        branch()


def main():
    init(canvas_size=(600, 600), face_color="#44cc00", background_color="#082019", max_depth=800)
    with scale(2):
        branch()
    write_to_png("/tmp/round_branches.png")


if __name__ == "__main__":
    main()
