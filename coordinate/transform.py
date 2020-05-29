import numpy as np
import math
from coordinate.point import Point


def parse_function(self, function):
    """function is a transform svg string"""
    name, _, values = function[:-1].partition('(')

    entries = []
    num = ""
    #loop over values
    for char in values:
        #check if character is a digit and save it
        if char.isdigit() or char == '+' or char == '-' \
                or (char == '.' and num[-1] != '.'):
            num += char
        #if char is something else and num is not empty, then save num as float
        elif num:
            entries.append(float(num))
            num = ""

    if name == "matrix" and len(entries) == 6:
        #entries is [a b c d e f] and return
        #  a c e
        #  b d f
        #  0 0 1
        mat = np.array(entries)
        mat = np.reshape(mat, (2,3), order='F')
        mat = np.append(mat, [[0, 0, 1]], axis=0)
    
    elif name == "translate" and len(entries) <= 2:
        #entries is [x {y=0}] and return
        #  1 0 x
        #  0 1 y
        #  0 0 1
        if len(entries) < 2:
            entries.append(0)

        mat = np.identity(3)
        mat[0, 2] = entries[0]
        mat[1, 2] = entries[1]

    elif name == "scale" and len(entries) <= 2:
        #entries is [x {y=x}] and return
        #  x 0 0
        #  0 y 0
        #  0 0 1
        if len(entries) < 2:
            entries.append(entries[0])
        entries.append(1)

    elif name == "rotation" and len(entries) <= 3:
        #entries is [a {x=0 y=0}] and return
        #  c -s  (1-c)x + sy
        #  s  c -sx + (1-c)y    where c = cos(a) and s = sin(a)
        #  0  0      1
        if len(entries) < 2:
            entries += [0, 0]

        c = math.cos(math.radians(entries[0]))
        s = math.sin(math.radians(entries[0]))
        x = entries[1]
        y = entries[2]

        mat = np.array( [c, -s,  (1-c)*x + s*y] ,
                        [s,  c, -s*x + (1-c)*y] ,
                        [0,  0,       1       ] )

    elif name == "skewX" and len(entries) == 1:
        #entries is [a] and return
        #  1 t 0
        #  0 1 0    where t = tan(a)
        #  0 0 1

        mat = np.diag(3)
        mat[0, 1] = math.tan(math.radians(entries[0]))

    elif name == "skewY" and len(entries) == 1:
        #entries is [a] and return
        #  1 0 0
        #  t 1 0    where t = tan(a)
        #  0 0 1

        mat = np.diag(3)
        mat[1, 0] = math.tan(math.radians(entries[0]))

    return mat



class Transform:

    def __init__(self, function = None):
        """function is a string describing the transformation"""
        if function is None:
            self.mat = np.identity(3)
        else: 
            self.mat = parse_transform(function)


    def convolve(self, mat):
        if isinstance(mat, Transform):
            self.mat = np.dot(mat.mat, self.mat)
        elif isinstance(mat, np.array):
            self.mat = np.dot(mat, self.mat)
        elif isinstance(mat, str):
            t = Transform(mat)
            self.mat = np.dot(t.mat, self.mat)
        else:
            raise ValueError("Transform.convolve requires a Transform, \
                                a np.array, or a string function")
                                        

    def __call__(self, pt):
        if not isinstance(pt, Point):
            raise ValueError("Transform.__call__ requires a point")

        b = np.array([pt.x, pt.y, 1])
        c = np.dot(self.mat, b)

        return Point(c[0], c[1])
