from math import radians, cos, sin


def rotate_point(point, angle):
    rotated_point = (point[0] * cos(-angle) - point[1] * sin(-angle),
                     point[0] * sin(-angle) + point[1] * cos(-angle))
    return rotated_point


def translate_graphics(graphics, pos, direction):
    translated_graphics = ()
    for t_pos in graphics:
        t_pos = rotate_point(t_pos, direction)
        x = t_pos[0] + pos[0]
        y = t_pos[1] + pos[1]
        translated_graphics = ((x, y),) + (translated_graphics)
    return translated_graphics


def angle_to_vector(angle):
    return [sin(angle), cos(angle)]