from coordinate.point import Point


class Shape():

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


    def __init__(self, start, end, transform = None, **kw):
        """start and end are required
        if transform is passed it is applied
        kw is shape specific
        """

        self.start = start
        self.end   = end
        self.kw    = kw

        if trans is not None:
            transform(trans)


    def transform(self, trans)

        self.start = trans(start)
        self.end   = trans(end)

        if "control" in self.kw:    #for bezier
            self.kw["control"] = [trans(p) for p in self.kw["control"]]
        if "radX" in self.kw:       #for ellipse
            prx = Point(self.kw["radX"], 0)
            self.kw["radX"] = trans(prx).x
        if "radY" in self.kw:       #for ellipse
            pry = Point(0, self.kw["radY"])
            self.kw["radY"] = trans(pry).y

        #build shape. The function is defined in child classes
        build()
