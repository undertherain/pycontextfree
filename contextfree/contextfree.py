from io import BytesIO
import random
import math
import numpy as np
import cairocffi as cairo


MAX_ELEMENTS = 200000
MAX_DEPTH = 8


def _init_state():
    global state
    state = {}
    state["depth"] = 0
    state["cnt_elements"] = 0


def surface_to_image(surface):
    from IPython.display import Image
    buf = BytesIO()
    surface.write_to_png(buf)
    data = buf.getvalue()
    buf.close()
    return Image(data=data)


def write_to_png(*args, **kwargs):
    return surface.write_to_png(*args, **kwargs)


class rotate:
    def __init__(self, angle):
        self.angle = angle

    def __enter__(self):
        global ctx
        self.matrix_old = ctx.get_matrix()
        ctx.rotate(self.angle)

    def __exit__(self, type, value, traceback):
        global ctx
        ctx.set_matrix(self.matrix_old)


class translate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __enter__(self):
        global ctx
        self.matrix_old = ctx.get_matrix()
        ctx.translate(self.x, self.y)

    def __exit__(self, type, value, traceback):
        global ctx
        ctx.set_matrix(self.matrix_old)


class scale:
    def __init__(self, scale_x, scale_y=None):
        self.scale_x = scale_x
        if scale_y is None:
            self.scale_y = scale_x
        else:
            self.scale_y = scale_y

    def __enter__(self):
        global ctx
        self.matrix_old = ctx.get_matrix()
        ctx.scale(self.scale_x, self.scale_y)

    def __exit__(self, type, value, traceback):
        global ctx
        ctx.set_matrix(self.matrix_old)


class flip_y:
    def __init__(self):
        pass

    def __enter__(self):
        global ctx
        self.matrix_old = ctx.get_matrix()
        ctx.scale(-1, 1)

    def __exit__(self, type, value, traceback):
        global ctx
        ctx.set_matrix(self.matrix_old)


class color:
    def __init__(self, alpha=1):
        self.alpha = alpha

    def __enter__(self):
        global ctx
        self.source_old = ctx.get_source()
        rgba = self.source_old.get_rgba()
        rgba = rgba[:3] + (rgba[-1] * self.alpha,)
        ctx.set_source_rgba(* rgba)

    def __exit__(self, type, value, traceback):
        global ctx
        ctx.set_source(self.source_old)


def check_limits(some_function):
    def wrapper(*args, **kwargs):
        global state
        state["cnt_elements"] += 1
        state["depth"] += 1
        m = ctx.get_matrix()
        if abs(m[0]) > 0.5 and state["cnt_elements"] < MAX_ELEMENTS and state["depth"] < MAX_DEPTH:
            some_function(*args, **kwargs)
        state["depth"] -= 1
    return wrapper


def report():
    global state
    print("cnt elements drawn:", state["cnt_elements"])


def line(x, y, w=0.1):
    global ctx
    ctx.move_to(0, 0)
    ctx.line_to(x, y)
    ctx.close_path()
    # ctx.set_source_rgb (0.3, 0.2, 0.5)
    ctx.set_line_width(w)
    ctx.stroke()


def circle(rad):
    global ctx
    ctx.arc(0, 0, rad, 0, 2 * math.pi)
    # ctx.stroke_preserve()
    # ctx.set_source_rgb(0.3, 0.4, 0.6)
    ctx.fill()


def triangle(side):
    global ctx
    h = math.sqrt(3) * side / 2
    ctx.move_to(0, 0)
    ctx.line_to(-side / 2, 0)
    ctx.line_to(0, h)
    ctx.line_to(side / 2, 0)
    ctx.close_path()
    ctx.fill()


def box(side):
    global ctx
    h = side / 2
    ctx.rectangle(-h, -h, side, side)
    ctx.fill()


def init(canvas_size=(512, 512), max_depth=10, face_color=None, background_color=None):
    global surface
    global ctx
    global cnt_elements
    global depth
    global MAX_DEPTH
    global WIDTH
    global HEIGHT
    _init_state()
    MAX_DEPTH = max_depth
    WIDTH, HEIGHT = canvas_size
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.translate(WIDTH / 2, HEIGHT / 2)
    scale = min(WIDTH, HEIGHT)
    ctx.scale(scale, -scale)  # Normalizing the canvas
    # ctx.rotate(math.pi)

    if background_color is not None:
        source = ctx.get_source()
        pat = cairo.SolidPattern(* htmlcolor_to_rgb(background_color))
        ctx.rectangle(-1, -1, 2, 2)  # Rectangle(x0, y0, x1, y1)
        ctx.set_source(pat)
        ctx.fill()
        ctx.set_source(source)
    if face_color is not None:
        ctx.set_source_rgb(* htmlcolor_to_rgb(face_color))


def display_ipython():
    global surface
    return surface_to_image(surface)


def get_npimage(transparent=False, y_origin="top"):
    """ Returns a WxHx[3-4] numpy array representing the RGB picture.

    If `transparent` is True the image is WxHx4 and represents a RGBA picture,
    i.e. array[i,j] is the [r,g,b,a] value of the pixel at position [i,j].
    If `transparent` is false, a RGB array is returned.

    Parameter y_origin ("top" or "bottom") decides whether point (0,0) lies in
    the top-left or bottom-left corner of the screen.
    """
    global surface
    im = 0 + np.frombuffer(surface.get_data(), np.uint8)
    im.shape = (HEIGHT, WIDTH, 4)
    im = im[:, :, [2, 1, 0, 3]]
    if y_origin == "bottom":
        im = im[::-1]
    return im if transparent else im[:, :, : 3]


def rnd(c):
    return (random.random() - 0.5) * 2 * c


def prnd(c):
    return (random.random() * c)


def coinflip(sides):
    c = random.randint(0, sides - 1)
    if c == 1:
        return True
    return False


def htmlcolor_to_rgb(s):
    if not (s.startswith('#') and len(s) == 7):
        raise ValueError("Bad html color format. Expected: '#RRGGBB' ")
    result = [1.0 * int(n, 16) / 255 for n in (s[1:3], s[3:5], s[5:])]
    return result
