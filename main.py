import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN

from analyze.dom_analyze import DomAnalyze
from crawlPage.crawler import Crawler
from util.ImageUtil import ImageUtil


def main():
    crawler = Crawler("https://www.aliyun.com")
    crawler.saveImageAndHtml()
    domAnalyze = DomAnalyze(crawler)
    domAnalyze.toDomJSON()
    #
    # domAnalyze = DomAnalyze(None)
    # dom_list = domAnalyze.service()
    # ImageUtil.drawImage(r"www.aliyun.com_24_01_07_14/www.aliyun.com.png", dom_list)
    # DomFilter.dividable()
    #
    # # 提取框选框的中心点坐标
    # centers = np.array([
    #     [int(element.x + element.width / 2), int(element.y + element.height / 2)]
    #     for element in dom_list
    # ])
    #
    # # 计算预计算的距离矩阵
    # distance_matrix = cdist(centers, centers, metric='euclidean')
    #
    # # 使用DBSCAN进行聚类
    # db = DBSCAN(eps=10, min_samples=2, algorithm='brute', metric='precomputed').fit(distance_matrix)
    # labels = db.labels_
    #
    # # 绘制聚类结果
    # unique_labels = set(labels)
    # colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    #
    # # 加载截图
    # image = cv2.imread('result/www.aliyun.com_23_09_39_31/raw.png')
    #
    # for k, col in zip(unique_labels, colors):
    #     if k == -1:
    #         # 黑色用于噪声点，不绘制
    #         continue
    #
    #     class_member_mask = (labels == k)
    #
    #     xy = centers[class_member_mask]
    #     for point in xy:
    #         x, y = int(point[0]), int(point[1])
    #         cv2.circle(image, (x, y), 5, [int(c * 255) for c in col[:3]], -1)
    #
    # # 绘制非噪声点的框选框
    # for i, element in enumerate(dom_list):
    #     if labels[i] != -1:  # 仅绘制非噪声点的框选框
    #         x, y, width, height = int(element.x), int(element.y), int(element.width), int(element.height)
    #         cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)
    #
    # # 保存带有聚类结果和框选框的图像
    # cv2.imwrite('result/www.aliyun.com_23_09_39_31/raw_box.png', image)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
