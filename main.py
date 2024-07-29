import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN

from analyze.dom_analyze import DomAnalyze
from analyze.min_analyze import MinAnalyze
from analyze.vips_analyze import VIPSAnalyze
from common.config import Config
from crawlPage.crawler import Crawler
# from scan.dbscan_web_test import DBScanWeb
from scan.dbscan_web import DBScanWeb
from util.ImageUtil import ImageUtil


def main():
    crawler = Crawler("https://www.aliyun.com")
    crawler.saveImageAndHtml()
    domAnalyze = DomAnalyze(crawler)
    # domAnalyze.toDomJSON()

    # domAnalyze = DomAnalyze(None)
    dom_list = domAnalyze.service()
    ImageUtil.drawImage(crawler.file_path + crawler.filename, dom_list, "raw_draw")

    # 简单处理同层的重叠兄弟节点
    MinAnalyze.process_nodes(dom_list)
    divide_list = VIPSAnalyze().service(dom_list)
    ImageUtil.drawImage(crawler.file_path + crawler.filename, divide_list, "divide")

    # dbscan_web = DBScanWeb(min_samples=2)
    # label = dbscan_web.fit(divide_list)
    label = DBScanWeb(divide_list, crawler.window_width, crawler.window_height, dom_list[0]).DBSCAN()
    ImageUtil.drawImage(crawler.file_path + crawler.filename, divide_list, "scan", label)

    # 绘制聚类结果测试
    # ImageUtil.drawImage(Config.test + "/www.aliyun.com.png", divide_list, "scan")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
