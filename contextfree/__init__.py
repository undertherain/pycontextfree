"""CFDG-inspired cairo-based pythonic generative art tool."""

from ._version import VERSION
from .core import *
from .shapes import circle, box, line, triangle
from .random import rnd, prnd, coinflip


__version__ = VERSION
