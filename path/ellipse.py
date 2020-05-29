from path.shape import Shape
import math


class Ellipse(Shape):


    def build(self):
        if "radX" in self.kw:
            self.radx = abs(kw["radX"])
        if "radY" in self.kw:
            self.rady = abs(kw["radY"])
        if "angle" in self.kw:
            self.alpha = kw["angle"]
        if "large" in self.kw:
            self.large = kw["large"]
        if "sweep" in self.kw:
            self.sweep = kw["sweep"]

        if self.radx == 0 or self.rady == 0:
            raise ValueError(f'Check ellipse radii: rad_x = {self.radx}, \
                                                    rad_y = {Self.rady}')

        self.mid  = 0.5 * (self.start + self.end)
        self.half = 0.5 * (self.start - self.end)

        self.c0 = self.find_centre()
        self.t_start, self.t_end = self.parameterise()



    #output
    def __repr__(self):
        """return Point(x, y)"""
        return f'Ellipse(self.start, self.end, \
                         self.rx, self.ry, self.angle, \
                         self.large, self.weep)'


    def __str__(self):
        """return (x, y)"""
        return f'Ellipse(self.rx, self.ry)'



    def find_centre(self):

        self.half.rotate(-self.alpha)
        test = (self.half.x / self.radx)**2 + (self.half.y / self.rady)**2
        if test > 1:
            self.radx *= test**0.5
            self.rady *= test**0.5


        scale = ((self.radx * self.rady)**2 - (self.radx * self.half.y)**2 - (self.rady * self.half.x)**2 ) \
                        / ( (self.radx * self.half.y)**2 + (self.rady * self.half.x)**2 )
        if scale < 1e-9:
            scale = 0
        else:
            scale = scale**0.5

        centre = Point(self.half.y * self.radx/self.rady, -self.half.x * self.rady/self.radx)

        if self.sweep == self.large:
            centre *= -scale
        else:
            centre *= scale

        centre.rotate(self.alpha)
        centre += self.mid

        return centre


    def parameterise(self):

        centre = Point(self.c0.x, self.c0.y)

        centre.rotate(-self.alpha)
        centre -= self.mid

        u = Point(1, 0)

        r1 = self.half - centre 
        r1.x /= self.radx
        r1.y /= self.rady

        r2 = self.half + centre 
        r2.x /= - self.radx
        r2.y /= - self.rady

        h1 = r1.angle(u)
        dh = r1.angle(r2)

        if (u.x * r1.y - u.y * r1.x) < 0:
            h1 *= -1

        if (r1.x * r2.y - r1.y * r2.x) < 0:
            dh *= -1

        if self.sweep and dh < 0:
            dh += 2*math.pi
        elif not self.sweep and dh > 0:
            dh -= 2*math.pi

        return h1, h1 + dh


    def mod(self):
        """call it with .mod(), return length of bezier curve by boole integration"""

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
        """parametrise ellips with t"""
        t = self.t_start + (self.t_end - self.t_start) * t

        p = Point(self.radx * math.cos(t), self.rady * math.sin(t))
        p.rotate(self.alpha)
        return p + self.c0


    def at_dt(self, t):
        """parametrise ellipse derivative"""
        if self.swepp:
            t = self.t_start + (self.t_end - self.t_start) * t
        else:
            t = self.t_start - (self.t_end - self.t_start) * t

        p = Point(-self.radx * math.cos(self.alpha) * math.sin(t)
                -self.rady * math.sin(self.alpha) * math.cos(t),
                -self.radx * math.sin(self.alpha) * math.sin(t)
                +self.rady * math.cos(self.alpha) * math.cos(t))

        return p


    def at_dl(self, t):
        """parametrise derivative of curve with t"""
        return at_dt(t).mod()
