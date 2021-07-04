"""CFDG-inspired cairo-based pythonic generative art tool."""

from ._version import VERSION
from .core import *
from .random import coinflip, prnd, rnd
from .shapes import box, circle, line, triangle
from ._transform import flip_y, transform

__version__ = VERSION
