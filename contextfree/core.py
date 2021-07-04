"""CFDG-inspired cairo-based pythonic generative art tool."""


__all__ = ['htmlcolor_to_rgb',
           'surface_to_image',
           'display_ipython',
           'get_npimage',
           'render_record_surface',
           'write_to_png',
           'check_limits',
           'rule',
           'report',
           'init',
           ]

import colorsys
import logging
import sys
from io import BytesIO

import cairocffi as cairo
import numpy as np

from .random import prnd

logger = logging.getLogger(__name__)

MAX_ELEMENTS = 1000000
MAX_DEPTH = 8
HEIGHT = 100
WIDTH = 100
SIZE_MIN_FEATURE = 0.5
_state = {}
_background_color = None
_rules = {}
surface = None


def _init_state():
    global surface
    surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
    _state["ctx"] = cairo.Context(surface)
    _state["color"] = (0, 0, 0, 1)
    _state["depth"] = 0
    _state["cnt_elements"] = 0


def surface_to_image(surface):
    """Renders current buffer surface to IPython image"""
    from IPython.display import Image
    buf = BytesIO()
    surface.write_to_png(buf)
    data = buf.getvalue()
    buf.close()
    return Image(data=data)


def display_ipython():
    """renders global surface to IPython notebook"""
    image_surface = render_record_surface()
    return surface_to_image(image_surface)


def get_npimage(transparent=False, y_origin="top"):
    """ Returns a WxHx[3-4] numpy array representing the RGB picture.

    If `transparent` is True the image is WxHx4 and represents a RGBA picture,
    i.e. array[i,j] is the [r,g,b,a] value of the pixel at position [i,j].
    If `transparent` is false, a RGB array is returned.

    Parameter y_origin ("top" or "bottom") decides whether point (0,0) lies in
    the top-left or bottom-left corner of the screen.
    """
    image_surface = render_record_surface()
    img = 0 + np.frombuffer(image_surface.get_data(), np.uint8)
    img.shape = (HEIGHT, WIDTH, 4)
    img = img[:, :, [2, 1, 0, 3]]
    if y_origin == "bottom":
        img = img[::-1]
    return img if transparent else img[:, :, : 3]


def render_record_surface():
    # image_surface = cairo.SVGSurface(None, HEIGHT, WIDTH)
    x_start, y_start, width_actual, height_actual = surface.ink_extents()
    logger.debug(f"x start={x_start}, y start={y_start}, width actual={width_actual}, height_actual={height_actual}")
    # print(x_start, y_start, width_actual, height_actual)
    # shrink and translate to match specified width and height
    image_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    context = cairo.Context(image_surface)
    scale = min(WIDTH / width_actual, HEIGHT / height_actual)
    if _background_color is not None:
        logger.info("filling background_color")
        source = context.get_source()
        pat = cairo.SolidPattern(* htmlcolor_to_rgb(_background_color))
        context.rectangle(0, 0, WIDTH, HEIGHT)  # Rectangle(x0, y0, x1, y1)
        context.set_source(pat)
        context.fill()
        context.set_source(source)
    context.translate(WIDTH / 2, HEIGHT / 2)
    context.scale(scale, -scale)  # Normalizing the canvas
    context.translate(-x_start - width_actual / 2, -y_start - height_actual / 2)
    context.set_source_surface(surface, 0, 0)
    context.paint()
    return image_surface


def write_to_png(*args, **kwargs):
    """Saves current buffer surface to png file"""
    image_surface = render_record_surface()
    return image_surface.write_to_png(*args, **kwargs)


def check_limits(user_rule):
    """Stop recursion if resolution is too low on number of components is too high """

    def wrapper(*args, **kwargs):
        """The body of the decorator """
        global _state
        _state["cnt_elements"] += 1
        _state["depth"] += 1
        matrix = _state["ctx"].get_matrix()
        # TODO: add check of transparency = 0
        if _state["depth"] >= MAX_DEPTH:
            logger.info("stop recursion by reaching max depth {}".format(MAX_DEPTH))
        else:
            min_size_scaled = SIZE_MIN_FEATURE / min(WIDTH, HEIGHT)
            current_scale = max([abs(matrix[i]) for i in range(2)])
            if (current_scale < min_size_scaled):
                logger.info("stop recursion by reaching min feature size")
                # TODO: check feature size with respect to current ink size
            else:
                if _state["cnt_elements"] > MAX_ELEMENTS:
                    logger.info("stop recursion by reaching max elements")
                else:
                    user_rule(*args, **kwargs)
        _state["depth"] -= 1
    return wrapper


def rule(proba=1):
    def real_decorator(function):
        name = function.__name__

        def wrapper(*args, **kwargs):
            if args:
                raise NotImplementedError("Passing parameters to rules not implemented yet")
            call_rule(name)

        logger.info("registering rule " + name)
        if name not in _rules:
            _rules[name] = []
            last_proba = 0
        else:
            last_proba = _rules[name][-1][0]
        _rules[name].append((last_proba + proba, function))
        return wrapper

    return real_decorator


@check_limits
def call_rule(name):
    rules = _rules[name]
    die_roll = prnd(rules[-1][0])
    for i in range(len(rules)):
        if die_roll < rules[i][0]:
            rules[i][1]()
            break


def report():
    """Prints some stats on current state"""
    global _state
    print("cnt elements drawn:", _state["cnt_elements"])


def init(canvas_size=(512, 512), max_depth=12, face_color=None, background_color=None):
    """Initializes global state"""
    global _background_color
    _background_color = background_color
    global _ctx
    global cnt_elements
    global MAX_DEPTH
    global WIDTH
    global HEIGHT

    _init_state()
    sys.setrecursionlimit(20000)
    MAX_DEPTH = max_depth
    WIDTH, HEIGHT = canvas_size

    if face_color is not None:
        r, g, b = htmlcolor_to_rgb(face_color)
        _state["ctx"].set_source_rgb(r, g, b)
        hue, saturation, brightness = colorsys.rgb_to_hsv(r, g, b)
        _state["color"] = (hue, saturation, brightness, 1)
    logger.debug("Init done")


# -------------------transformations------------------


def htmlcolor_to_rgb(str_color):
    """function to convert HTML-styly color string to RGB values

    Args:
        s: Color in HTML format

    Returns:
        list of three RGB color components
    """
    if not (str_color.startswith('#') and len(str_color) == 7):
        raise ValueError("Bad html color format. Expected: '#RRGGBB' ")
    result = [1.0 * int(n, 16) / 255 for n in (str_color[1:3], str_color[3:5], str_color[5:])]
    return result
