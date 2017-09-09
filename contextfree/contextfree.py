from IPython.display import Image
from io import BytesIO
import random
import math
import cairocffi as cairo


cnt_elements = 0
depth = 0
MAX_ELEMENTS = 10000
MAX_DEPTH = 8


def surface_to_image(surface):
    buf = BytesIO()
    surface.write_to_png(buf)
    data = buf.getvalue()
    buf.close()
    return Image(data=data)


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
    def __init__(self, factor):
        self.factor = factor

    def __enter__(self):
        global ctx
        self.matrix_old = ctx.get_matrix()
        ctx.scale(self.factor, self.factor)

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


def check_limits(some_function):
    def wrapper(*args, **kwargs):
        global cnt_elements
        global depth
        cnt_elements += 1
        depth += 1
        if cnt_elements < MAX_ELEMENTS and depth < MAX_DEPTH:
            some_function(*args, **kwargs)
        depth -= 1
    return wrapper


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


def init(canvas_size=(512, 512), max_depth=10):
    global surface
    global ctx
    global cnt_elements
    global depth
    global MAX_DEPTH
    MAX_DEPTH = max_depth
    cnt_elements = 0
    depth = 0
    WIDTH, HEIGHT = canvas_size
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.translate(WIDTH / 2, HEIGHT / 2)
    scale = min(WIDTH, HEIGHT) / 2
    ctx.scale(scale, scale)  # Normalizing the canvas
    ctx.rotate(math.pi)


def display_ipython():
    global surface
    return surface_to_image(surface)


def rnd(c):
    return (random.random() - 0.5) * c
