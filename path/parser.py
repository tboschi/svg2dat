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

    return Bezier(p_list)


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

    return Bezier(p_list)


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

        return Ellipse(p_current, p_next, 
                       numbers[0],   #radius x
                       numbers[1],   #radius y
                       numbers[2],   #angle
                       numbers[3],   #large flag
                       numbers[4])   #sweep flag
