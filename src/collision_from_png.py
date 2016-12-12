from PIL import Image
from cymunk import Vec2d


'''
    Returns a list of cymunk shapes

    .png file should use the following format
        - use decrementing R/G/B values for separate shapes, so (255, 0, 0) is
          one line segment, (254, 0, 0) is another, etc.

        - red for endpoints for a line segment

        - green for circles, left-most is center, pixels of the same G-value
          trailing to the right to indicate radius

        - blue for polygons, but lets not use those yet
'''

def getCollisionShapes(png_path, col_type):
    png = Image.open(png_path)

    pixels = list(png.getdata())
    width, height = png.size
    pixels = [pixels[(i * width):((i+1) * width)] for i in range(height)]

    handled_pixels = [[False for x in range(width)] for y in range(height)]
    new_red = (255, 0, 0)
    new_grn = (0, 255, 0)

    # List of points for each color value
    reds = [[] for i in range(256)]
    grns = [[] for i in range(256)]

    for y, row in enumerate(pixels):
        for x, px in enumerate(row):
            if (px[1] == 0) and (px[2] == 0):
                reds[px[0]].append(Vec2d(x - 72, y - 72))

            elif (px[0] == 0) and (px[2] == 0):
                grns[px[1]].append(Vec2d(x - 72, y - 72))

            else:
                pass

    # Delete all empty segments and circles
    reds = list(filter(([]).__ne__, reds))
    grns = list(filter(([]).__ne__, grns))

    shapes = []

    for segment in reds:
        if segment != []:
            shapes.append(getLine(segment, col_type))

    for circle in grns:
        if circle != []:
            shapes.append(getCircle(circle, col_type))

    # Add position after the fact
    physics = {'main_shape': 'circle',
               'velocity': (0, 0),
               'angle': 0,
               'angular_velocity': 0,
               'vel_limit': 0,
               'ang_vel_limit': 0,
               'mass': 0,
               'moment': 0,
               'col_shapes': shapes}

    return physics

def getLine(seg_points, col_type):
    if col_type == 'building':
        shape = {'a': seg_points[0], 'b': seg_points[1], 'mass': 0, 'radius': 0}
        col_shape = {'shape_type': 'segment', 'elasticity': .1,
                     'collision_type': 1, 'shape_info': shape,
                     'friction': 1.0}
    else:
        pass

    return col_shape

def getCircle(circle_points, col_type):
    x_val = []

    for point in circle_points:
        x_val.append(point.x)

    left_most_point_index = x_val.index(min(x_val))
    offset = circle_points[left_most_point_index]
    radius = len(circle_points)

    if col_type == 'building':
        shape = {'inner_radius': 0, 'outer_radius': radius, 'offset': offset,
                 'mass': 0}
        col_shape = {'shape_type': 'circle', 'elasticity': .1,
                     'collision_type': 1, 'shape_info': shape,
                     'friction': 1.0}
    else:
        pass

    return col_shape
