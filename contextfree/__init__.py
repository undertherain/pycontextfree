"""CFDG-inspired cairo-based pythonic generative art tool."""

from ._transform import color, flip_y, rotate, scale, transform, translate
from ._version import VERSION
from .core import *
from .random import coinflip, prnd, rnd
from .shapes import box, circle, line, triangle

__version__ = VERSION
