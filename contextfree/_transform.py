import colorsys
import math

from .color import htmlcolor_to_rgb
from .core import _state


def adjust(value, step):
    if step < 0:
        dst = 0.0
    else:
        dst = 1.0
    distance = abs(dst - value)
    actual_step = distance * step
    result = value + actual_step
    if result > 1:
        result = 1.0
    if result < 0:
        result = 0.0
    return result


class transform:
    """Defines a scope of transformed geometry and photometry"""

    def __init__(self,
                 x=0,
                 y=0,
                 angle=None,
                 scale=1,
                 hue=0,
                 brightness=0,
                 saturation=0,
                 alpha=0):
        self.offset_x = x
        self.offset_y = y
        self.angle = angle
        if isinstance(scale, int) or isinstance(scale, float):
            self.scale_x = scale
            self.scale_y = scale
        else:
            self.scale_x, self.scale_y = scale
        self.hue = hue / 360
        # TODO: make it all brightness or all brightness
        self.brightness = brightness
        self.saturation = saturation
        self.alpha = alpha

    def __call__(self):
        ctx = _state["ctx"]
        ctx.translate(self.offset_x, self.offset_y)
        ctx.scale(self.scale_x, self.scale_y)
        if self.angle is not None:
            ctx.rotate(self.angle * math.pi / 180)
        # r, g, b, alpha = ctx.get_source().get_rgba()
        # hue, saturation, brightness = colorsys.rgb_to_hsv(r, g, b)
        hue, saturation, brightness, alpha = _state["color"]
        hue = math.modf(hue + self.hue)[0]
        brightness = adjust(brightness, self.brightness)
        saturation = adjust(saturation, self.saturation)
        alpha = adjust(alpha, self.alpha)
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)
        # alpha = min((alpha * self.alpha), 255)
        rgba = [r, g, b, alpha]
        ctx.set_source_rgba(* rgba)
        # TODO: make it named tuple or class
        _state["color"] = (hue, saturation, brightness, alpha)

    def __enter__(self):
        self.matrix_old = _state["ctx"].get_matrix()
        self.source_old = _state["ctx"].get_source()
        self.color_old = _state["color"]
        self()
        return self

    def __exit__(self, type, value, traceback):
        _state["ctx"].set_matrix(self.matrix_old)
        _state["ctx"].set_source(self.source_old)
        _state["color"] = self.color_old
        # TODO: don't we have to recover color?
        # why not hust restore whole ctx


class translate(transform):
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y)


class scale(transform):
    def __init__(self, factor):
        super().__init__(scale=factor)


class rotate(transform):
    def __init__(self, angle):
        super().__init__(angle=angle)


class color(transform):
    def __init__(self, hue=0, saturation=0, brightness=0, alpha=0):
        super().__init__(hue=hue, brightness=brightness, saturation=saturation, alpha=alpha)


class set_color:
    def __init__(self, hue=None, saturation=None, brightness=None, alpha=None):
        color_old = _state["color"]
        self.hue = hue / 360 if hue else color_old[0]
        self.saturation = saturation if saturation else color_old[1]
        self.brightness = brightness if brightness else color_old[2]
        self.alpha = alpha if alpha else color_old[3]

    def __enter__(self):
        self.color_old = _state["color"]
        _state["color"] = (self.hue,
                           self.saturation,
                           self.brightness,
                           self.alpha)
        # TODO: but here we call HSV, not HSL :-\
        r, g, b = colorsys.hsv_to_rgb(self.hue, self.saturation, self.brightness)
        # alpha = min((alpha * self.alpha), 255)
        rgba = [r, g, b, self.alpha]
        _state["ctx"].set_source_rgba(* rgba)

    def __exit__(self, type, value, traceback):
        _state["color"] = self.color_old


class set_color_rgba:
    def __init__(self, color=None, alpha=1):
        self.color = htmlcolor_to_rgb(color)
        self.alpha = alpha

    def __enter__(self):
        self.color_old = _state["color"]
        _state["color"] = self.color + [self.alpha]
        rgba = * self.color, self.alpha
        _state["ctx"].set_source_rgba(* rgba)

    def __exit__(self, type, value, traceback):
        _state["color"] = self.color_old
        # _state["ctx"].set_source_rgba(* rgba)


class flip_y:
    """Defines scope of a view being reflected along the y axis"""

    def __enter__(self):
        self.matrix_old = _state["ctx"].get_matrix()
        _state["ctx"].scale(-1, 1)

    def __exit__(self, type, value, traceback):
        _state["ctx"].set_matrix(self.matrix_old)
