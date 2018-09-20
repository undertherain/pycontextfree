import math
# from .core import _ctx
from .core import _state
# import contextfree


def circle(rad=0.5):
    """Draw a circle"""
    _ctx = _state["ctx"]
    _ctx.arc(0, 0, rad, 0, 2 * math.pi)
    _ctx.stroke_preserve()
    # _ctx.set_source_rgb(0.3, 0.4, 0.6)
    _ctx.fill()


def line(x, y, width=0.1):
    """Draw a line"""
    _state["ctx"].move_to(0, 0)
    _state["ctx"].line_to(x, y)
    _state["ctx"].close_path()
    # _ctx.set_source_rgb (0.3, 0.2, 0.5)
    _state["ctx"].set_line_width(width)
    _state["ctx"].stroke()


def triangle(rad=0.5):
    """Draw a triangle"""
    # half_height = math.sqrt(3) * side / 6
    # half_height = side / 2
    side = 3 * rad / math.sqrt(3)
    _state["ctx"].move_to(0, -rad / 2)
    _state["ctx"].line_to(-side / 2, -rad / 2)
    _state["ctx"].line_to(0, rad)
    _state["ctx"].line_to(side / 2, -rad / 2)
    _state["ctx"].close_path()
    _state["ctx"].fill()


def box(side=1):
    """Draw a box"""
    global _ctx
    half_side = side / 2
    _state["ctx"].rectangle(-half_side, -half_side, side, side)
    _state["ctx"].fill()
