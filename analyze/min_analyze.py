'''
简单合并同层的重叠矩阵块
'''


class MinAnalyze:
    @staticmethod
    def is_overlapping(node1, node2):
        """
        检查两个节点是否重叠
        """
        return not (node1.x >= node2.x + node2.width or
                    node1.x + node1.width <= node2.x or
                    node1.y >= node2.y + node2.height or
                    node1.y + node1.height <= node2.y)

    @staticmethod
    def merge_nodes(parent, child):
        """
        将子节点的尺寸和位置合并到父节点
        """
        parent.x = min(parent.x, child.x)
        parent.y = min(parent.y, child.y)
        parent.width = max(parent.x + parent.width, child.x + child.width) - parent.x
        parent.height = max(parent.y + parent.height, child.y + child.height) - parent.y
        child.block.block_visual = False

    @staticmethod
    def handle_overlaps(node):
        """
        处理节点重叠情况
        """
        for child in node.childNodes:
            MinAnalyze.handle_overlaps(child)

        for child in node.childNodes:
            for sibling in node.childNodes:
                if child != sibling and MinAnalyze.is_overlapping(child, sibling):
                    MinAnalyze.merge_nodes(node, child)
                    node.block.block_visual = True
                    break

    @staticmethod
    def process_nodes(list):
        """
        处理节点树中的重叠情况
        """
        print("去除dom同层重叠节点...")
        for root in list:
            MinAnalyze.handle_overlaps(root)
