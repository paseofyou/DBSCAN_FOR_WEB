import numpy as np
from sklearn.cluster import DBSCAN
import copy as cp


class DBScanWeb:
    def __init__(self, nodes, pageWidth, pageHeight, domRoot):
        self.nodes = nodes
        self.outlier_nodes = self.cleanse()
        self.n = len(nodes)
        self.pageWidth = pageWidth
        self.pageHeight = pageHeight
        self.domRoot = domRoot
        self.alpha = (self.pageHeight) / self.find_depth_tree(self.domRoot)

    # 将长宽过小的nodes标记为离散，记录在列表中
    def cleanse(self):
        outlier_nodes = []
        for node in self.nodes:
            if node.width <= 1 or node.height <= 1:
                outlier_nodes.append(cp.deepcopy(node))
                self.nodes.remove(node)
        return outlier_nodes

    # 计算两个节点之间的视觉距离
    def visual_distance(self, n1, n2):
        x_cor = (n1.x - n2.x) * (n1.x + n1.width - n2.x - n2.width)
        y_cor = (n1.y - n2.y) * (n1.y + n1.height - n2.y - n2.height)
        dx = np.where(x_cor <= 0, 0, min(abs(n1.x - n2.x),
                                         abs(n1.x + n1.width - n2.x - n2.width)))
        dy = np.where(y_cor <= 0, 0, min(abs(n1.y - n2.y),
                                         abs(n1.y + n1.height - n2.y - n2.height)))
        return dx + dy

    # 计算两个节点之间的逻辑距离，即在DOM树中的距离
    def logic_distance(self, n1, n2):
        n1_path = []
        temp1 = n1.parentNode
        while temp1 is not None:
            n1_path.append(temp1)
            temp1 = temp1.parentNode

        step = 0
        temp2 = n2.parentNode
        while temp2 not in n1_path:
            step += 1
            if temp2.parentNode is None:
                break
            temp2 = temp2.parentNode

        if temp2 not in n1_path:
            idx = len(n1_path)
        else:
            idx = n1_path.index(temp2)
        return abs(step + idx - 1)

    # 计算DOM树的最大深度

    def find_depth_tree(self, root):
        if root is None:
            return 0
        max_depth = 0
        for child in root.childNodes:
            temp = self.find_depth_tree(child)
            if temp > max_depth:
                max_depth = temp
        return max_depth + 1

    # 检查两个节点是否对齐

    def isAlign(self, n1, n2):
        res = 0
        if abs(n2.x - n1.x) <= 2:
            res += 0.8
        elif abs(n2.x + n2.width - n1.x - n1.width) <= 2:
            res += 0.8

        elif abs(n2.y - n1.y) <= 2:
            res += 0.8
        elif abs(n2.y + n2.height - n1.y - n1.height) <= 2:
            res += 0.8

        if res == 0.8:
            if n2.width == n1.width:
                res += 0.2
            if n2.height == n1.height:
                res += 0.2

        return res

    # 计算节点之间的相似度距离矩阵，并返回矩阵和平均距离
    def similarity_distance_matrix(self, nodes):
        total_valid_distance = 0
        valid_distance_count = 0

        matrix = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(i + 1, self.n):
                visual_distance = self.visual_distance(nodes[i], nodes[j]) * self.n / self.alpha
                logic_distance = self.logic_distance(nodes[i], nodes[j])
                if visual_distance < self.pageHeight / 2:
                    valid_distance_count += 1
                    total_valid_distance += visual_distance

                alignment_distance = self.isAlign(nodes[i], nodes[j])
                dist = visual_distance + self.alpha * (logic_distance * (2 - alignment_distance) / 2)

                matrix[i][j] = matrix[j][i] = max(dist, 0)

        average_distance = total_valid_distance / (valid_distance_count + 1)
        print('eps平均距离: ', average_distance)
        return matrix, average_distance

        # 辅助

    def get_indices(self, list, value):
        return [i for i, val in enumerate(list) if val == value]

    def get_elements(self, list, indices_list):
        return [list[i] for i in indices_list]

    def merge_nodes(self, nodes_list):
        x = min(node.x for node in nodes_list)
        y = min(node.y for node in nodes_list)
        width = max(node.x + node.width for node in nodes_list) - x
        height = max(node.y + node.height for node in nodes_list) - y
        nodes_list[0].x = x
        nodes_list[0].y = y
        nodes_list[0].width = width
        nodes_list[0].height = height
        return nodes_list[0]

    # 聚类算法
    def DBSCAN(self):
        print("DBScan预处理中...")
        similarity_matrix, average_distance = self.similarity_distance_matrix(self.nodes)
        print("DBScan识别中...")
        clustering = DBSCAN(eps=average_distance, min_samples=2,
                            algorithm='brute', metric='precomputed').fit(similarity_matrix)
        labels = clustering.labels_
        max_cluster_index = max(labels)

        # Add noise nodes
        noise_node_indices = self.get_indices(labels, -1)
        new_nodes_list = self.get_elements(self.nodes, noise_node_indices)

        # Add cluster candidates
        for i in range(max_cluster_index + 1):
            element_indices = self.get_indices(labels, i)
            new_nodes_list.append(self.merge_nodes(
                self.get_elements(self.nodes, element_indices)))

        self.nodes = new_nodes_list
        return labels
