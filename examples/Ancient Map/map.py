import logging
import math
from contextfree.contextfree import *


# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


@register_rule("wall", 1)
def wall_1():
    with translate(0.95, 0):
        with rotate(0.01):
            with scale(0.975):
                ancient_map()


@register_rule("wall", 1)
def wall_2():
    box()
    with translate(0.95, 0):
        with rotate(-0.0027):
            with scale(0.975):
                with color(hue=0.001, saturation=0.1, lightness=0.003):
                    ancient_map()


@register_rule("wall", 0.09)
def wall_4():
    box()
    with scale(0.975):
        with translate(0.95, 0):
            with rotate(math.pi / 2):
                ancient_map()
            with rotate(- math.pi / 2):
                ancient_map()


@register_rule("wall", 0.05)
def wall_5():
    with translate(0.97, 0):
        with scale(1.5):
            with rotate(math.pi / 2):
                ancient_map()
            with rotate(- math.pi / 2):
                ancient_map()


@check_limits
def ancient_map():
    call_rule("wall")
    #box()
    #with translate(1, 0):
     #   with scale(0.97):
      #      with rotate(0.01):
       #         with color(hue=0.001, saturation=0.1, lightness=0.003):
        #            ancient_map()


def main():
    init(canvas_size=(600, 600), background_color="#e5d5ac", face_color="#0a0707", max_depth=120)

    ancient_map()
    with rotate(math.pi / 2):
        ancient_map()

    write_to_png("/tmp/map.png")


if __name__ == "__main__":
    main()
