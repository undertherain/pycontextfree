"""CFDG-inspired cairo-based pythonic generative art tool."""

from ._transform import (
    color,
    flip_y,
    rotate,
    scale,
    set_color,
    set_color_rgba,
    transform,
    translate,
)
from ._version import VERSION
from .core import *
from .random import coinflip, prnd, rnd
from .rule import check_limits, rule
from .shapes import box, circle, line, polygon, triangle

__version__ = VERSION
