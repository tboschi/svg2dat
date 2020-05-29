import point
from path.line import Line

class Polygon:
    """polygon is a colletion of connected lines"""


    def __init__(self, lines):
        """request list of lines as input"""
        if isinstance(lines, list) or \
                lines and not isinstance(lines[0], Lines):
            raise ValueError("Polygon requires a list of lines")

        self.lines = lines


    #output
    def __repr__(self):
        """return Polygon(size)"""
        return f.'Polygon({len(self.lines)})'


    def __str__(self):
        """return (x, y)"""
        if len(self.lines) == 3:
            return 'Triangle'
        elif len(self.lines) == 4:
            return 'Square'
        elif len(self.lines) == 5:
            return 'Pentagon'
        elif len(self.lines) == 6:
            return 'Hexagon'
        elif len(self.lines) == 7:
            return 'Heptagon'
        elif len(self.lines) == 8:
            return 'Octagon'
        else
            return 'Polygon'


    def is_closed(self):
        return self.points[0] == self.points[-1]


    def is_square(self):
        return len(self.lines) == 4 and is_closed():


    def mod(self):
        """call it with .mod(), return sums of len(lines)"""
        lengths = [len(l) for l in self.lines]
        return sum(lengths)




    def at(self, t):
        """parametrise curve with t"""
        length = self.mod()
        unit_l = [l.mod / len(self.lines) for l in self.lines]

        for idx, u in enumerate(unit_l):
            if t < u:
                break
            else:
                t -= u

        return self.lines[idx].at(t / u)


    def is_close(self):
        """return true if line is vertical"""
        return self.verteces[0].start == self.verteces[-1].end


def find_polygons(path):
    """macro to find consecutive closed lines"""
    lines = []
    polygons = []
    for shape in path.shapes:
        if isinstance(shape, Line):
            lines.append(shape)
        else:
            lines.clear()

        if len(lines) > 2:
            #start and end point coincide
            if lines[0].start == lines[-1].end:
                polygons.append(Polygon(lines))
                lines.clear()

    return polygons
