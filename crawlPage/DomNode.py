from bs4.element import Tag, NavigableString


class DomNode:
    __slots__ = (
    'nodeType', 'nodeName','nodeValue', 'visual_cues', 'childNodes', 'parentNode')

    def __init__(self, nodeType):
        self.nodeType = nodeType
        self.childNodes = []
        self.visual_cues = dict()



# class DomNode:
# node = None
# node_type = None
# tag_name = None
# node_name = None
# node_value = None
# attributes = None
# child_nodes = None
# parent_node = None
# visual_cues = None
#
# def __init__(self, node):
#     self.node = node
#     self.node_type = self.get_node_type()
#     self.tag_name = self.get_tag_name()
#     self.node_name = self.get_node_name()
#     self.node_value = self.get_node_value()
#     self.attributes = self.get_attributes()
#     self.child_nodes = self.get_child_nodes()
#     self.parent_node = self.get_parent_node()
#     self.visual_cues = self.get_visual_cues()
#
# def get_node_type(self):
#     if isinstance(self.node, Tag):
#         return 'Element Node'
#     elif isinstance(self.node, NavigableString):
#         return 'Text Node'
#     else:
#         return 'Other Node'
#
# def get_tag_name(self):
#     return self.node.name.lower() if isinstance(self.node, Tag) else None
#
# def get_node_name(self):
#     return self.node.name if isinstance(self.node, Tag) else None
#
# def get_node_value(self):
#     return self.node if isinstance(self.node, NavigableString) else None
#
# def get_attributes(self):
#     return self.node.attrs if isinstance(self.node, Tag) else None
#
# def get_child_nodes(self):
#     if isinstance(self.node, Tag):
#         child_nodes = []
#         for child in self.node.contents:
#             if isinstance(child, (Tag, NavigableString)):
#                 child_nodes.append(child)
#         return child_nodes
#     return None
#
# def get_parent_node(self):
#     if self.node and isinstance(self.node, Tag) and self.node.parent and isinstance(self.node.parent, Tag):
#         return self.node.parent
#     return None
#
# def get_visual_cues(self):
#     return self.node.get('style') if isinstance(self.node, Tag) else None
#
#
# def __repr__(self):
#     return f"DomNode(node_type={self.node_type}, tag_name={self.tag_name}, node_name={self.node_name}, node_value={self.node_value}, attributes={self.attributes}, child_nodes=[...], parent_node={self.parent_node}, visual_cues={self.visual_cues})"
#
# def __str__(self):
#     return self.__repr__()
