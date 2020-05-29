from path.point import Point


class Text():

    def __init__(self, text, position):
        """pass text and position as a point"""
        self.text = text
        self.position = position


    def get_text(self):
        return self.text


    def get_position(self):
        return self.position


    def transform(self, trans):
        """apply transformation on position"""
        self.position = trans(self.position)



def parse_text(collection):
    """parse the attributes of a text/tspan tag and its text
    collection is a list of tuples
    each tuple is attributes and text
    returns a list of text objects
    """

    for attrib, text in collection:
        ps = position(attrib)
        for l, pos in enumerate(ps):
            alltext.append(Text(text[l], pos))

        #if text left, append it to last
        if len(text) > len(ps):
            alltext[-1].text += text[len(ps):]


    return p



def position(attrib, start = None):
    """extract information on points from attribute"""
    if start is None:
        x, y = 0, 0
    else:
        x, y = start.xy()

    xpos = []
    ypos = []
    dxpos = []
    dypos = []

    if "x" in attrib:
        for xc in attrib["x"].split():
            xpos.append(float(xc))
    if "dx" in attrib:
        for xc in attrib["dx"].split():
            dxpos.append(float(xc))
    if "y" in attrib:
        for yc in attrib["y"].split():
            ypos.append(float(yc))
    if "dy" in attrib:
        for yc in attrib["dy"].split():
            dypos.append(float(yc))

    print(len(xpos))
    print(len(ypos))
    print(len(dxpos))
    print(len(dypos))

    px = [x + dx for x, dx in zip(xpos, dxpos)]
    print(px)
    if len(xpos) > len(dxpos):
        px += xpos[len(dxpos):]
    elif len(xpos) < len(dxpos):
        px += dxpos[len(xpos):]
    print(px)

    py = [y + dy for y, dy in zip(ypos, dypos)]
    print(py)
    if len(ypos) > len(dypos):
        py += ypos[len(dypos):]
    elif len(ypos) < len(dypos):
        py += dypos[len(ypos):]
    print(py)

    ps = [Point(x, y) for x, y in zip(px, py)]
    if len(px) > len(py):
        ps += [Point(x, 0) for x in px[len(py):]]
    elif len(px) < len(py):
        ps += [Point(0, y) for y in py[len(px):]]

    return ps
