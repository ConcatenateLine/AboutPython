from random import randint

def generate_green_color():
    """
    Generate variations of green colors in hexadecimal format.
    
    Returns:
        str: A string representing the hexadecimal color code.Format as #RRGGBB
    """
    green_value = randint(0, 255)
    return f'#{0:02x}{green_value:02x}{0:02x}'