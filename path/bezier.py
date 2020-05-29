from path.shape import Shape

class Bezier(Shape):


    def build(self):
        """build the bezier shape"""
        if "control" in self.kw:
            if not isinstance(self.kw["control"], list) \
                    or not len(self.kw["control"]):
                raise ValueError("Bezier needs a non-empty list of points")

            self.points = self.kw["control"]
            self.derive = [p - self.points[idx-1] for idx, p
                            in enumerate(self.points[1:])]



    #output
    def __repr__(self):
        """return Point(x, y)"""
        return f'Bezier({len(self.points)})'


    def __str__(self):
        """return (x, y)"""
        return f'Bezier({len(self.points)})'


    def mod(self):
        """call it with .mod(),
        return length of bezier curve by boole integration"""
    
        step = 100.0
        grid = [i / step for i in range(int(step))]
        h = grid[1]

        integral = h / 90. *  7 * at_dl(0)
        first = 0

        for a in grid[:-1]:

            integral += first

            integral += h / 90. * 32 * at_dl(a + h * 0.25) #x2
            integral += h / 90. * 12 * at_dl(a + h * 0.50) #x3
            integral += h / 90. * 32 * at_dl(a + h * 0.75) #x4

            first = h / 90. *  7 * at_dl(a + h)   #x5

            integral += first

        return integral




    def at(self, t):
        """parametrise control points of curve with t"""

        return self.bez(t)


    def at_dt(self, t):
        """parametrise derivative of curve with t as dx/dt"""

        return self.bez(t, self.derive[:])


    def at_dl(self, t):
        """parametrise derivative of curve with t"""

        return at_dt(t).mod()


    def bez(self, t, ctrl = None):
        """parametrise a generic set of points, returns a point object
        
           This is the function defining a bezier curve"""

        if not ctrl:
            ctrl = self.points[:]

        for j, _ in enumerate(ctrl[1:]):
            for i, _ in enumerate(ctrl[:-j]):
                ctrl[i] = ctrl[i] * (1 - t) + ctrl[i+1] * t

        return ctrl[0]
