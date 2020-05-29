import math


class Point:
    """object with coordinates x and y"""


    def __init__(self, x = 0, y = 0):
        """pass coordinates x and y to initialise"""
        self.x = x
        self.y = y


    #output
    def __repr__(self):
        """return Point(x, y)"""
        return f'Point[{self.x}, {self.y}]'


    def __str__(self):
        """return (x, y)"""
        return f'[{self.x}, {self.y}]'


    #addition
    def __iadd__(self, other):
        """override += as (x += o.x, y += o.y)"""
        self.x += other.x
        self.y += other.y

        return self


    def __add__(self, other):
        """override + as +="""
        p = Point(self.x, self.y)
        p += other

        return p


    #subtraction
    def __isub__(self, other):
        """override -= as (x -= o.x, y -= o.y)"""

        self.x -= other.x
        self.y -= other.y

        return self


    def __sub__(self, other):
        """override - using -="""

        p = Point(self.x, self.y)
        p -= other

        return p


    #multiplication
    def __imul__(self, other):
        """multiplication with scalar, override *= """
        self.x *= other
        self.y *= other

        return self


    def __mul__(self, other):
        """multiplication with scalar, override * using *=
        otherwise multiplication with other point
        """
        if isinstance(other, float):
            p = Point(self.x, self.y)
            p *= other
            return p

        elif isinstance(other, Point):
            return self.x * other.x + self.y * other.y


    def __rmul__(self, other):
        if isinstance(other, float):
            p = Point(self.x, self.y)
            p *= other
            return p


    # modulus
    def mod2(self):
        """return absolute value squared"""
        return self.x**2 + self.y**2


    def mod(self):
        """return absolute value"""
        return self.mod2()**0.5


    #equals
    def __eq__(self, other):
        """check if two points are the same"""
        return (self.x == other.x) and (self.y == other.y)
    

    #rotation
    def rotate(self, alpha):
        """apply rotation of angle alpha wrt to origin"""
        p = Point(math.cos(alpha) * self.x - math.sin(alpha) * self.y,
                  math.sin(alpha) * self.x + math.cos(alpha) * self.y,)

        self.x = p.x
        self.y = p.y


    #angle with other point
    def angle(self, other):
        if not isinstance(other, Point):
            raise ValueError("Point.angle expecting a Point")

        cos = (self * other) / self.mod() / other.mod()

        if cos > 1.0:
            return math.acos(1.0)
        elif cos < -1.0:
            return math.acos(-1.0)
        else:
            return math.acos(cos)


    #transform point with matrix and translation
    def transform(self, trans):
        """apply transformation to point

        trans is a list [A, B, C, D, E, F] that is applied as

                 v1  v2              cc

        x'       A   C      x         E
             = (       )  (   )  +  (   )
        y'       B   D      y         F

        return a new object
        """
        if not trans:
            return self.copy()

        v1 = Point(trans[0], trans[1])
        v2 = Point(trans[2], trans[3])
        cc = Point(trans[4], trans[5])

        return v1 * self.x + v2 * self.y + cc


    def copy(self):
        """create and return a copy of this object"""
        p = Point(self.x, self.y)
        return p

    def xy(self):
        """return tuple of coordinates"""
        return (self.x, self.y)


#access
#    def X(self):
#        return self.x
#
#
#    def Y(self):
#        return self.y
