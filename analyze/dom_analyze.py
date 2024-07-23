import json

from model.node import Node
from common.config import Config


class DomAnalyze:
    def __init__(self, crawler):
        self.crawler = crawler
        self.domTreeList = []  # 存放dom树的列表
        self.domAllList = []  # 存放dom平面列表

    # 构造dom树，并将其dom平面列表存入domTreeList列表中
    def service(self):
        print("dom树构造中...")
        # self.toDomJSON()
        self.loadDomTree()
        self.loadDomAllList()
        return self.getDomTreeList()

    def toDomJSON(self):
        with open("analyze/to_node.js", "r", encoding="utf-8") as f:
            elements_info = self.crawler.driver.execute_script(f.read() + "\nreturn JSON.stringify(main());")
            if (elements_info is None):
                print("获取dom_json元素信息失败")
                return
            with open(Config.path + "/" + self.crawler.file_path + "toNode.json", "w", encoding="utf-8") as f2:
                f2.write(elements_info)

    # 从内存加载到项目中
    def loadDomTree(self):
        # with open(self.crawler.file_path + "toNode.json", "r", encoding="utf-8") as f:
        with open(r"result/www.aliyun.com_24_01_07_14/" + "toNode.json", "r",
                  encoding="utf-8") as f:
            json_list = json.loads(f.read())
            for obj in json_list:
                try:
                    if isinstance(obj, str):
                        try:
                            json_obj = json.loads(obj)
                        except json.JSONDecodeError as e:
                            json_obj = obj
                    else:
                        json_obj = obj
                    node = Node(json_obj)
                    if node is not None:
                        self.domTreeList.append(node)

                except Exception as e:
                    print(obj)
                    print(e)

    # 层序遍历构造dom平面列表。此处不用担心xy的坐标，都是基于左上角绘制的
    def loadDomAllList(self):
        tmp_queue = []
        for e in self.domTreeList:
            self.domAllList.append(e)
            tmp_queue.append(e)
        while len(tmp_queue) != 0:
            tmp_queue_2 = []
            for i in tmp_queue:
                for j in i.childNodes:
                    self.domAllList.append(j)
                    tmp_queue_2.append(j)
            tmp_queue = tmp_queue_2

    def getDomTreeList(self):
        return self.domTreeList
