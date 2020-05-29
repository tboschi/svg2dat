from coordinate.point import Point


class Path():
    """Path object is a dictionary of

    key/color = a RGB hex value storing the stroke colour from style
    shapes    = a list of shapes from a processed d attribute
                with the same color
    """


    def __init__(self, shapes, color, trans = None):
        """shapes is a list of shapes of the same color
        color is a RGB hex value
        if transform is passed, apply transformation
        """
        if not isinstance(shapes, list) or \
                (shapes and not isinstance(shapes[0], Shape)):
            raise ValueError("Path requires a list of shape objects")

        self.shapes = shapes
        self.color  = color

        if transform is not None:
            transform(trans)


    def transform(self, trans):
        self.shapes = [shape.transform(trans) for shape in self.shapes]


    def at(self, t):
        """return point at parameter"""

        for shape in shapes:
            if shape is None:
                continue


    def iterator(self, s = 10):
        return PathIterator(self, s)



class PathIterator:
    """iterator class for path"""


    def __init__(self, path, s = 10):
        """iterator object return points of shapes
        optional parameter defined sampling points
        default to 10 samples"""
        self._path = path
        self.index = 0
        self.samples = [x / float(s) for i in range(s)]
        self.index_sample = 1


    def __iter__(self):
        return self


    def __next__(self):
        """next return start point of first object
        then return end points of lines and arbitrary number of points
        for bezier and ellipses
        """
        if self.index < 0 or self.index >= len(self.shapes):
            raise StopIteration

        if self.shapes[self.index] is None:
            p = self.shapes[self.index]
            self.index += 1

        if self.index == 0:
            p = self.shapes[0].get_start()
            self.index += 1

        elif isinstance(self.shapes[index], Line):
            p = self.shapes[self.index]
            self.index += 1

        elif self.index_sample < len(self.samples):
            #bezier or ellips, use at to get poins at index_sample
            p = self.shapes[self.index].at(self.samples[self.index_sample])
            self.index_sample += 1

        else: #reset
            self.index_sample = 1
            self.index += 1

        return p


########################################
## parsing functions


from coordinate.point     import Point
from path.line      import Line
from path.bezier    import Bezier
from path.ellipse   import Ellipse


def parse_d_fromfile(inf):
    """name is a file object or path to file"""
    if isinstance(inf, str):
        inf = open(inf, "r")

    if isinstance(inf, file):
        inf.seek(0)    #go at the beginning in case file was already open
        d = inf.read()
        inf.close()
        return parse_d(d)
    else:
        return None


def parse_d(d):
    """parse the d attribute of an svg shape
    return a list of shapes separated by a None
    each section of shapes represent a sub shape 
    inside the global shape
    """

    commands = "mzlhvcsqta"
    commands += commands.upper()

    p_current = Point()
    p_start   = Point()

    shapes = []
    subshapes = []
    numbers = []

    #loop over lines first
    for line in d.split('\n'):

        #print(line)

        #remove comments or other stuff
        if '#' in line:
            line = line[:line.find('#')]
        if '$' in line:
            line = line[:line.find('$')+1]
        if '@' in line:
            line = line[:line.find('@')+1]
        if not line:
            continue

        #loop over character of line
        num = ""
        comm = ""
        for char in line:

            #check first if character is a command
            if char in commands:
                comm = char
                
            #check if character is a digit and save it
            elif char.isdigit() or char == '+' or char == '-' \
                    or (char == '.' and num[-1] != '.'):
                num += char
            #if char is something else and num is not empty, then save num as float
            elif num:
                numbers.append(float(num))
                num = ""

            #try to execute some commands

            last_path = None
            path_closed = False

            if comm.upper() == 'M':     #move to defines the start
                p_start = move_to(numbers, p_current, comm.islower())
                if p_start is not None:
                    p_current = p_start
                    path_closed = True
                    if comm.isupper():      #default to straight lines
                        comm = 'L'
                    elif comm.islower():
                        comm = 'l'
                    numbers.clear()         #clear numbers
            elif comm.upper() == 'Z':     #cannot return none
                last_path = close_path(p_current, p_current, p_start)
                if last_path is not None:
                    path_closed = True
                    if comm.isupper():     #next, move to a point
                        comm = 'M'
                    elif comm.islower():
                        comm = 'm'
            elif comm.upper() == 'L':
                last_path = straight_line(numbers, p_current, comm.islower()) 
            elif comm.upper() == 'H':
                last_path = horizontal_line(numbers, p_current, comm.islower()) 
            elif comm.upper() == 'V':
                last_path = vertical_line(numbers, p_current, comm.islower()) 
            elif comm.upper() == 'T' or comm.upper() == 'S':
                p_last = None
                if isinstance(self.subshapes[-1], Bezier):
                    p_last = subpath[-1].points[-2]
                last_path = short_bezier(numbers, p_current, p_last, comm.islower()) 
            elif comm.upper() == 'Q' or comm.upper() == 'C':
                last_path = curve_bezier(numbers, p_current, comm.islower()) 
            elif comm.upper() == 'A':
                last_path = elliptic_arc(numbers, p_current, comm.islower()) 
            elif comm:
                raise ValueError(f"command {comm} is unknown")


            if last_path is not None:
                #print(comm + "-> adding shape " + str(last_path))
                p_current = last_path.get_end()  #current point is end of last shape
                subshapes.append(last_path)
                numbers.clear()         #clear numbers

            if path_closed and subshapes:     #shapes is closed, start a new subpath
                #print(comm + "-> closing shape")
                shapes.append(subshapes)
                shapes.append(None)
                subshapes.clear()

    if subshapes:       #if trailing subshapes, save them
        shapes.append(subshapes)       #subpath finished, append
        shapes.append(None)         
        subshapes.clear()            #and clear             

    return shapes



#close shape: 
def close_path(numbers, p_current, p_start):
    """close shape with a line to the starting point
    trailing coordinates, if any, are dropped
    """
    return Line(p_current, p_start)


def move_to(numbers, p_current, relative = False):
    """create subpath, move pointer at coordinate of first two numbers"""
    if len(numbers) != 2:
        return None

    p_start = Point(numbers[0], numbers[1])  #first point
    if relative:
        p_start += p_current
    return p_start


def straight_line(numbers, p_current, relative = False):
    """straight line from current point"""
    if len(numbers) != 2:
        return None

    p_next = Point(numbers[0], numbers[1])
    if relative:     #relative
        p_next += p_current

    return Line(p_current, p_next)


def horizontal_line(numbers, p_current, relative = False):
    """horizontal line from current point"""
    if len(numbers) != 1:
        return None

    if relative:
        p_next = Point(numbers[0] + p_current.x, p_current.y)
    else:
        p_next = Point(numbers[0], p_current.y)

    return Line(p_current, p_next)


def vertical_line(numbers, p_current, relative = False):
    """vertical line from current point"""
    if len(numbers) != 1:
        return None

    if relative:
        p_next = Point(p_current.x, numbers[0] + p_current.y)
    else:
        p_next = Point(p_current.x, numbers[0])

    return Line(p_current, p_next)



def curve_bezier(numbers, p_current, relative = False):
    """curve bezier with 2 or 3 points, it is the same instruction"""
    if len(numbers) < 2 or len(numbers) > 3:
        return None

    pp = [ Point(numbers[i], numbers[i+1]) \
            for i in range(0, len(numbers), 2) ]
    if relative:
        pp = [ p + p_current for p in pp]

    p_list = [ p_current ]
    p_list.append(pp)

                  #start     #end        #control points
    return Bezier(p_list[0], p_list[-1], control = p_list)


def short_bezier(numbers, p_current, p_last = None, relative = False):
    """short bezier with 2 or 3 points, it is the same instruction
    it requires the second to last point (p_last) of the previous bezier curve
    in order to make a symmetrical one
    """
    if len(numbers) < 1 or len(numbers) > 2:
        return None

    p_next = p_current.copy()
    if p_last is not None:   #if last shape was bezier, copy next to last point
        p_next += p_current - p_last

    pp = [ Point(numbers[i], numbers[i+1]) \
            for i in range(0, len(numbers), 2) ]
    if relative:
        pp = [ p + p_current for p in pp[2:]]

    p_list = [ p_current, p_next ]
    p_list.append(pp)

                  #start     #end        #control points
    return Bezier(p_list[0], p_list[-1], control = p_list)


def elliptic_arc(numbers, p_current, relative = False):
    """elliptic arc from current point
    if any of the two radii are null, then a straight line is created instead
    """
    if len(numbers) != 7:
        return None

    if any(numbers[:2]) == 0:
        return straight_line(numbers, p_current, relative)
    else:
        p_next = Point(numbers[5], numbers[6])
        if relative:
            p_next += p_curent

                       #start     #end
        return Ellipse(p_current, p_next, 
                       radX = numbers[0],   #radius x
                       radY = numbers[1],   #radius y
                       angle = numbers[2],   #angle
                       large = numbers[3],   #large flag
                       sweep = numbers[4])   #sweep flag


def find_axes_tics(path):
    """find axes and tics in path.shapes
    axes and tics are vertical and horizontal lines
    axes are longer on average than tics
    """
    x_lines = []
    y_lines = []
    for shape in path.shapes:
        if isinstance(shape, Line):
            if shape.is_vertical():
                x_lines.append(shape)
            if shape.is_horizontal():
                y_lines.append(shape)

    #sort lines by length
    x_lines.sort(reverse = True, key = lambda line: line.mod())
    y_lines.sort(reverse = True, key = lambda line: line.mod())

    #4 longest lines are axes / frame
    for ix, il in enumerate(x_lines):
        for jx, jl in enumerate(x_lines[ix+1:]):
            #same vertical start and end
            if (il.start.y == jl.start.y and il.end.y == jl.end.y) \
             or (il.start.y == jl.end.y and il.end.y == jl.start.y):

                frame_x   = {il.start.x, jl.start.x}
                frame_x_y = {il.start.y, il.end.y}  #y value from frame
                #x_frame = {il, jl}

                x_lines.pop(ix) #remove axes
                x_lines.pop(jx)
                break
        else:
            continue
        break

    for iy, il in enumerate(y_lines):
        for jy, jl in enumerate(y_lines[iy+1:]):
            #same vertical start and end
            if (il.start.x == jl.start.x and il.end.x == jl.end.x) \
             or (il.start.x == jl.end.x and il.end.x == jl.start.x):

                frame_y   = {il.start.y, jl.start.y}
                frame_y_x = {il.start.x, il.end.x}  #x value from frame
                #y_frame = {il, jl}

                y_lines.pop(iy) #remove axes
                y_lines.pop(jy)
                break
        else:
            continue
        break
    
    #if the sets are equal, then frame found
    if frame_x != frame_y_x and frame_y != frame_x_y:
        raise Exception("frame_x and frame_y do not coincide")

    del frame_y_x, frame_x_y

    #list containing frame limits
    #frame = sorted(x_frame) + sorted(y_frame)


    #rest is tics or other stuff
    x_tics = set()
    for ix, il in enumerate(x_lines):
        if il.start.y in frame_y or il.end.y in frame_y:
            y_tics.add(x_lines.start.y)

    y_tics = set()
    for iy, il in enumerate(y_lines):
        if il.start.x in frame_x or il.end.x in frame_x:
            y_tics.add(il.start.y)



def find_frame(path):
    """find all frames in page
    a frame is a square/rectangle with vertical and horizontal lines
    """
    lines = []
    for shape in path.shapes:
        if isinstance(shape, Line):
            if shape.is_vertical() or shape.is_horizontal():
                lines.append(shape)

    allframes = []
    frame = []
    for k in range(lines):
        li = lines.pop(k)
        for j, lo in enumerate(lines):
            #if lines are connected, save and exit
            if li.is_connected(lo)
                frame.append(li)
                k = j
                break
        else: #else nothing is connected to li
            k = (k + 1) % len(lines)
            if frame: #if there are some connected lines
                allframes.append(Polygon(frame))
                frame.clear()

    boxes = [poly.is_square for poly in allframes]
    boxes.sort(reverse = True, key = lambda box: box.mod())

    return boxes



#if __name__ == "__main__":
    #test
