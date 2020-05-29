from path.shape import Shape

class Line(Shape):
    """line is defiend as two points
    
    it inherits the Shape constructor
    """



    #output
    def __repr__(self):
        """return Polygon(size)"""
        return f'Line({self.start}, {self.end})'


    def __str__(self):
        """return (x, y)"""
        return f'Line({self.start}, {self.end})'


    def mod(self):
        """call it with .mod()"""
        p = self.end - self.start
        return p.mod()


    def at(self, t):
        """parametrise curve with t"""
        return self.start + (self.end - self.start) * t


    def is_vertical(self):
        """return true if line is vertical"""
        return self.start.y == self.end.y


    def is_horizontal(self):
        """return true if line is horizontal"""
        return self.start.x == self.end.x

    def is_connected(self, line):
        """return true if self and line share start or end point"""
        return any(ext in (line.start, line.end) \
                    for ext in (self.start, self.end))
