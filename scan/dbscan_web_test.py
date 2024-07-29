import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors


class DBScanWeb:
    def __init__(self, eps=50, min_samples=2):
        self.eps = eps
        self.min_samples = min_samples

    def calculate_eps(self, node_data):
        """
        自动计算eps值的方法。
        """
        # 计算每个点到其第 min_samples 个最近邻的距离
        neighbors = NearestNeighbors(n_neighbors=self.min_samples)
        neighbors.fit(node_data)
        distances, _ = neighbors.kneighbors(node_data)
        k_distance = distances[:, -1]

        # 对距离进行排序，并绘制图像
        sorted_distances = np.sort(k_distance)
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_distances)
        plt.xlabel('Points sorted by distance')
        plt.ylabel('Distance to the k-th nearest neighbor')
        plt.title('K-distances Graph')
        plt.grid(True)
        plt.show()

        # 选择eps的建议值（例如，图像中的“膝点”）
        # 确保eps值大于0，并设置合理的下限
        suggested_eps = sorted_distances[int(len(sorted_distances) * 0.95)]
        return max(suggested_eps, 1e-5)  # 确保eps大于0

    def fit(self, nodes):
        # 提取节点的坐标和尺寸信息
        node_data = np.array([[node.x, node.y, node.width, node.height] for node in nodes])

        # 自动计算eps
        self.eps = self.calculate_eps(node_data)

        # 执行DBSCAN算法
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(node_data)
        labels = db.labels_

        return labels