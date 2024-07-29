from model.block import Block


class Node:
    __slots__ = (
        'id', 'nodeType', 'tag', 'x', 'y', 'width', 'height', 'text', 'display', 'visibility', 'childNodes',
        'parentNode', "font_size", "font_weight", "block", "background_color")
    clac_count = 0

    def __init__(self, node, parentNode=None):
        Node.clac_count += 1
        self.id = str(Node.clac_count)
        self.nodeType = node.get("nodeType")
        self.tag = node.get("tag")
        self.x = node.get("x")
        self.y = node.get("y")
        self.width = node.get("width")
        self.height = node.get("height")
        self.text = node.get("text")
        self.display = node.get("display")
        self.visibility = node.get("visibility")
        self.font_size = node.get("font_size")
        self.font_weight = node.get("font_weight")
        self.background_color = node.get("background_color")
        self.childNodes = []
        self.parentNode = parentNode
        self.block = Block()
        if isinstance(node.get("childNodes"), list):
            for i in node.get("childNodes"):
                self.childNodes.append(Node(i, self))

    def refresh(self):
        for i in range(len(self.childNodes)):
            child = self.childNodes[i]
            if i == 0:
                self.x = child.x
                self.y = child.y
                self.width = child.width
                self.height = child.height
            else:
                RBX = self.x + self.width
                RBY = self.y + self.height
                childRBX = child.x + child.width
                childRBY = child.y + child.height
                RBX = max(childRBX, RBX)
                RBY = max(childRBY, RBY)
                self.x = min(child.x, self.x)
                self.y = min(child.y, self.y)
                self.width = RBX - self.x
                self.height = RBY - self.y
