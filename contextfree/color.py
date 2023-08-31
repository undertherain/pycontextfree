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
