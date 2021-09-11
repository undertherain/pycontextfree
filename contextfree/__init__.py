"""CFDG-inspired cairo-based pythonic generative art tool."""

from ._transform import flip_y, scale, transform, translate
from ._version import VERSION
from .core import *
from .random import coinflip, prnd, rnd
from .shapes import box, circle, line, triangle

__version__ = VERSION
