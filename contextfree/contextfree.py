"""CFDG-inspired cairo-based pythonic generative art tool."""

from io import BytesIO
import random
import math
import colorsys
import logging
import sys
import numpy as np
import cairocffi as cairo


logger = logging.getLogger(__name__)

MAX_ELEMENTS = 200000
MAX_DEPTH = 8
HEIGHT = 100
WIDTH = 100
SIZE_MIN_FEATURE = 0.5
_state = {}
_ctx = None
_background_color = None
_rules = {}


def _init__state():
    global _state
    _state = {}
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


def register_rule(name, proba):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            raise RuntimeError("This function had been registered as a rule and can not be called directly")
        logger.info("registering rule " + name)
        if name not in _rules:
            _rules[name] = []
            last_proba = 0
        else:
            last_proba = _rules[name][-1][0]
        _rules[name].append((last_proba + proba, function))
        return wrapper

    return real_decorator


def call_rule(name):
    rules = _rules[name]
    die_roll = prnd(rules[-1][0])
    for i in range(len(rules)):
        if die_roll < rules[i][0]:
            rules[i][1]()
            break


def check_limits(some_function):
    """Stop recursion if resolution is too low on number of components is too high """

    def wrapper(*args, **kwargs):
        """The body of the decorator """
        global _state
        _state["cnt_elements"] += 1
        _state["depth"] += 1
        matrix = _ctx.get_matrix()
        # print(matrix)
        if _state["depth"] >= MAX_DEPTH:
            logger.info("stop recursion by reaching max depth")
        else:
            if _state["cnt_elements"] > MAX_ELEMENTS:
                logger.info("stop recursion by reaching max elements")
            else:
                min_size_scaled = SIZE_MIN_FEATURE / min(WIDTH, HEIGHT)
                current_scale = max([abs(matrix[i]) for i in range(2)])
                if (current_scale < min_size_scaled):
                    logger.info("stop recursion by reaching min feature size")
                else:
                    some_function(*args, **kwargs)
        _state["depth"] -= 1
    return wrapper


def report():
    """Prints some stats on current state"""
    global _state
    print("cnt elements drawn:", _state["cnt_elements"])


def init(canvas_size=(512, 512), max_depth=12, face_color=None, background_color=None):
    """Initializes global state"""
    global _background_color
    _background_color = background_color
    global surface
    global _ctx
    global cnt_elements
    # global depth
    global MAX_DEPTH
    global WIDTH
    global HEIGHT
    _init__state()
    sys.setrecursionlimit(20000)
    MAX_DEPTH = max_depth
    WIDTH, HEIGHT = canvas_size
    #   surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
    _ctx = cairo.Context(surface)
    # _ctx.translate(WIDTH / 2, HEIGHT / 2)
    # scale = min(WIDTH, HEIGHT)
    # _ctx.scale(scale, -scale)  # Normalizing the canvas
    # _ctx.rotate(math.pi)

    if face_color is not None:
        _ctx.set_source_rgb(* htmlcolor_to_rgb(face_color))
    logger.debug("Init done")


# -------------------transformations------------------

class rotate:
    """Defines a scope of rotated view """

    def __init__(self, angle):
        self.angle = angle
        self.matrix_old = None

    def __enter__(self):
        global _ctx
        self.matrix_old = _ctx.get_matrix()
        _ctx.rotate(self.angle)

    def __exit__(self, type, value, traceback):
        global _ctx
        _ctx.set_matrix(self.matrix_old)


class translate:
    """Defines a scope of linear translation"""

    def __init__(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y

    def __enter__(self):
        global _ctx
        self.matrix_old = _ctx.get_matrix()
        _ctx.translate(self.offset_x, self.offset_y)

    def __exit__(self, type, value, traceback):
        global _ctx
        _ctx.set_matrix(self.matrix_old)


class scale:
    """Defines scope of changed scale"""

    def __init__(self, scale_x, scale_y=None):
        self.scale_x = scale_x
        if scale_y is None:
            self.scale_y = scale_x
        else:
            self.scale_y = scale_y

    def __enter__(self):
        global _ctx
        self.matrix_old = _ctx.get_matrix()
        _ctx.scale(self.scale_x, self.scale_y)

    def __exit__(self, type, value, traceback):
        global _ctx
        _ctx.set_matrix(self.matrix_old)


class flip_y:
    """Defines scope of a view being reflected along the y axis"""

    def __enter__(self):
        global _ctx
        self.matrix_old = _ctx.get_matrix()
        _ctx.scale(-1, 1)

    def __exit__(self, type, value, traceback):
        global _ctx
        _ctx.set_matrix(self.matrix_old)


class color:
    """
        defines scope of changed color
        TODO: describe which one is additive and which one is multiplicative
    """

    def __init__(self, hue=0, lightness=0, saturation=0, alpha=1):
        self.hue = hue
        self.lightness = lightness
        self.saturation = saturation
        self.alpha = alpha
        self.source_old = None

    def __enter__(self):
        global _ctx
        self.source_old = _ctx.get_source()
        r, g, b, a = self.source_old.get_rgba()
        # print("rgb old:", r, g, b)
        hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
        # print("hls old:", hue, lightness, saturation)
        hue = math.modf(hue + self.hue)[0]
        lightness = lightness + self.lightness
        if lightness > 1:
            lightness = 1
        if lightness < 0:
            lightness = 0
        saturation = saturation + self.saturation
        if saturation > 1:
            saturation = 1
        if saturation < 0:
            saturation = 0
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        # print("hls new:", hue, lightness, saturation)
        # print("rgb new:", r, g, b)
        a = min((a * self.alpha), 255)
        # rgba = [int(r * 255), int(g * 255), int(b * 255), a]
        rgba = [r, g, b, a]
        # print(rgba)
        _ctx.set_source_rgba(* rgba)

    def __exit__(self, type, value, traceback):
        global _ctx
        _ctx.set_source(self.source_old)

# ----------------- primitives ----------------------


def line(x, y, width=0.1):
    """Draw a line"""
    global _ctx
    _ctx.move_to(0, 0)
    _ctx.line_to(x, y)
    _ctx.close_path()
    # _ctx.set_source_rgb (0.3, 0.2, 0.5)
    _ctx.set_line_width(width)
    _ctx.stroke()


def circle(rad=0.5):
    """Draw a circle"""
    global _ctx
    _ctx.arc(0, 0, rad, 0, 2 * math.pi)
    # _ctx.stroke_preserve()
    # _ctx.set_source_rgb(0.3, 0.4, 0.6)
    _ctx.fill()


def triangle(rad=0.5):
    """Draw a triangle"""
    global _ctx
    # half_height = math.sqrt(3) * side / 6
    # half_height = side / 2
    side = 3 * rad / math.sqrt(3)
    _ctx.move_to(0, -rad / 2)
    _ctx.line_to(-side / 2, -rad / 2)
    _ctx.line_to(0, rad)
    _ctx.line_to(side / 2, -rad / 2)
    _ctx.close_path()
    _ctx.fill()


def box(side=1):
    """Draw a box"""
    global _ctx
    half_side = side / 2
    _ctx.rectangle(-half_side, -half_side, side, side)
    _ctx.fill()


def rnd(diap):
    """returns random number in diapason from -diap  to diap"""
    return (random.random() - 0.5) * 2 * diap


def prnd(diap):
    """returns random number in diapasone from 0 to diap"""
    return random.random() * diap


def coinflip(sides):
    """returns true as if coin with `sides` sides is flipped"""
    coin = random.randint(0, sides - 1)
    if coin == 1:
        return True
    return False


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
