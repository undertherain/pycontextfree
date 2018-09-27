from contextfree import *

# try to play with rotation angle ;)


@check_limits
def branch():
    circle(1)
    with transform(y=1.5, alpha=-0.001, angle=1, scale=0.998):
        if coinflip(50):
            with flip_y():
                branch()
        else:
            branch()
        if coinflip(120):
            with flip_y():
                with transform(scale=0.9):
                    branch()


def main():
    init(canvas_size=(600, 600), face_color="#44cc00", background_color="#082019", max_depth=700)
    branch()
    write_to_png("/tmp/curly_branches.png")


if __name__ == "__main__":
    main()
