import xml.etree.ElementTree as ET


def depth_first(lvl, node):
    """generator looping depth_first

    use as for lvl, node in depth_first(level, root)
    where level is the depth of root

    an example is

        level = 0
        for lvl, path in depth_first(level, root):
            if "id" in path.attrib:
                _, _, path.tag = path.tag.rpartition('}')
                outp = ""
                for i in range(lvl):
                    outp += "\t"
                print (outp + path.tag + " " + path.attrib["id"])
    """

    if node.find("*") is None:
        yield lvl, node
    for child in node.findall("*"):
        lvl += 1
        if len(node.findall("*")) > 1:
            yield lvl, child
        yield from depth_first(lvl, child)
        lvl -= 1




def collect_text_nodes(root):
    """loop from root and find texts"""
    ns = root.tag[root.tag.find('{')+1:root.tag.find('}')]
    text_tag = ".//{" + ns + "}text"
    #print ("namespace " + ns)
    abs_text = []
    for text_node in root.findall(text_tag):
        text_list = parse_text_nodes(text_node) #get list of texts + position

        trans = Transform()
        up_node = text_node
        while up_node is not root:
            if "transform" in up_node.attrib:
                trans.convolve(parse_transform(up_node.attrib["transform"])
            up_node = up_node.find("..")

        abs_list = [text.transform(trans) for text in text_list]
        abs_text += abs_list

    return abs_text


def parse_text_nodes(node):
    """text node is parsed and its children which are tspan"""
    _, _, name = node.tag.rpartition('}')
    if name != "text":
        return None

    text_list = [parse_text(node.attrib, node.text)]
    for child in node.findall("*"):   #find all children
        _, _, name = child.tag.rpartition('}')
        if child != "tspan":
            continue

        text_list.append(parse_text(node.attrib, node.text))

    return text_list



def collect_path_nodes(root):
    """loop from root and find paths"""
    ns = root.tag[root.tag.find('{')+1:root.tag.find('}')]
    path_tag = ".//{" + ns + "}path"
    #print ("namespace " + ns)
    abs_path = []
    for path_node in root.findall(path_tag):
        path_list = parse_path_nodes(path_node) #get list of paths

        trans = Transform()
        up_node = path_node
        while up_node is not root:
            if "transform" in up_node.attrib:
                trans.convolve(parse_transform(up_node.attrib["transform"])
            up_node = up_node.find("..")

        abs_list = [path.transform(trans) for path in path_list]
        abs_path += abs_list

    return abs_path



def parse_path_node(node):
    """path node is extracted, but main information retained is d and color"""
    _, _, name = node.tag.rpartition('}')
    if name != "path":
        return None

    if "d" in node.attrib:
        shapes = parse_d(node.attrib["d"])

    if "style" in node.attrib:
        color = parse_style(node.attrib["style"], opt="stroke")

    return Path(shapes, color)
