import math
# from .core import _ctx
from .core import _state
# import contextfree


def circle(rad=0.5):
    """Draw a circle"""
    _ctx = _state["ctx"]
    _ctx.arc(0, 0, rad, 0, 2 * math.pi)
    _ctx.set_line_width(0)
    _ctx.stroke_preserve()
    # _ctx.set_source_rgb(0.3, 0.4, 0.6)
    _ctx.fill()


def line(x, y, width=0.1):
    """Draw a line"""
    ctx = _state["ctx"]
    ctx.move_to(0, 0)
    ctx.line_to(x, y)
    ctx.close_path()
    # _ctx.set_source_rgb (0.3, 0.2, 0.5)
    ctx.set_line_width(width)
    ctx.stroke()


def triangle(rad=0.5):
    """Draw a triangle"""
    # half_height = math.sqrt(3) * side / 6
    # half_height = side / 2
    ctx = _state["ctx"]
    side = 3 * rad / math.sqrt(3)
    ctx.move_to(0, -rad / 2)
    ctx.line_to(-side / 2, -rad / 2)
    ctx.line_to(0, rad)
    ctx.line_to(side / 2, -rad / 2)
    ctx.close_path()
    ctx.fill()


def box(side=1):
    """Draw a box"""
    half_side = side / 2
    _state["ctx"].rectangle(-half_side, -half_side, side, side)
    _state["ctx"].fill()
