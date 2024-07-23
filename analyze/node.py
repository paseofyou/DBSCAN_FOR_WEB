class Node:
    __slots__ = (
        'id', 'nodeType', 'tag', 'x', 'y', 'width', 'height', 'text', 'display', 'visibility', 'childNodes',
        'parentNode', 'block_visual',"flag")
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
        self.childNodes = []
        self.parentNode = parentNode
        if isinstance(node.get("childNodes"), list):
            for i in node.get("childNodes"):
                self.childNodes.append(Node(i, self))
        self.block_visual = True
        self.flag = False


    def __str__(self):
        return f"DomNode(id={self.id}, nodeType={self.nodeType}, tag={self.tag}, x={self.x}, y={self.y}, width={self.width}, height={self.height}, text={self.text}, display={self.display}, visibility={self.visibility}, childNodes=[...], parentNode={self.parentNode})"


