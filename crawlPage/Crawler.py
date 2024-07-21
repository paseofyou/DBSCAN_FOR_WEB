import json
import os
import time
from datetime import datetime
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from crawlPage.DomNode import DomNode
from util.ImageUtil import ImageUtil


class Crawler:
    url = None
    filename = None
    driver = None
    soup = None
    domNodeAllList = None

    def __init__(self, url: str = None):
        self.domNodeAllList = []
        self.url = url
        self.setDriver()
        if url is not None:
            self.get(url)

    def setDriver(self):
        driver_path: str = r'C:\Program Files\Google\Chrome\test\chromedriver-win64\chromedriver.exe'
        chrome_path: str = r'C:\Program Files\Google\Chrome\test\chrome-win64\chrome.exe'

        assert os.path.exists(driver_path), f"浏览器驱动路径错误: {driver_path}"
        assert os.path.exists(chrome_path), f"浏览器exe路径错误: {chrome_path}"
        chrome_options = Options()
        chrome_options.binary_location = chrome_path
        chrome_options.add_argument('--headless')
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(20)

    def get(self, urlStr: str):
        self.setUrl(urlStr)

        # 预加载资源
        default_width = 1920
        default_height = 1080
        self.driver.get(self.url)
        time.sleep(5)
        total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        scroll_position = 0
        self.driver.set_window_size(width=default_width, height=total_height, windowHandle="current")
        num = 0
        while num < 5:
            self.driver.execute_script(f"window.scrollBy(0, 1000)")
            time.sleep(0.5)
            scroll_position += 1000
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            if scroll_position >= total_height:
                num += 1
        self.driver.execute_script(f"window.scrollBy(0, 0)")
        print("爬虫资源加载完毕，开始解析")

        # 解析soup以及dom
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
        self.setDomTree()
        print("dom树解析完成")

    def setUrl(self, urlStr: str):
        # 设置url
        try:
            if urlStr.startswith('https://') or urlStr.startswith('http://'):
                self.url = urlStr
            else:
                self.url = 'http://' + urlStr
            parse_object = urlparse(self.url)
            tmpPath = r'Screenshots/' + parse_object.netloc + '_' + str(
                datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '/'
            self.filename = tmpPath + parse_object.netloc
            os.makedirs(tmpPath)
        except (TypeError, AttributeError):
            print("url无效: " + str(urlStr))
            return

    def saveImage(self):
        print("开始输出初始图像及源码")
        ImageUtil.saveImage(self.driver, self.filename)
        with open(self.filename + "_source.html", "w", encoding="utf-8") as f:
            f.write(self.soup.prettify())

    def setDomTree(self):
        jscript: str = ""
        with open("util/dom.js", "r", encoding="utf-8") as f:
            jscript = f.read()
            jscript += '\nreturn JSON.stringify(toJSON(document.getElementsByTagName("BODY")[0]));'
        body_json = self.driver.execute_script(jscript)
        try:
            json_obj = json.loads(body_json)
        except json.JSONDecodeError as e:
            print("dom转json解析失败")
            return

        self.domCalc(json_obj)

    def domCalc(self, json_obj, parent: DomNode = None):
        nodeType = json_obj.get("nodeType")
        node = DomNode(nodeType)

        if nodeType == 1:
            node.nodeName = json_obj.get('tagName')
            node.visual_cues = json_obj.get('visual_cues')
            if node.nodeName == 'script':
                return None
            # if node.nodeName == 'img':
            #     node.nodeValue = json_obj.get('nodeValue')
        elif nodeType == 3:
            node.nodeName = "#text"
            node.nodeValue = json_obj.get('nodeValue')
            node.parentNode = parent
            if parent != None and parent.visual_cues is not None:
               node.visual_cues = parent.visual_cues
        else:
            return node

        self.domNodeAllList.append(node)

        if nodeType == 1:
            childNodes = json_obj.get('childNodes', [])
            for i in childNodes:
                if (i.get("nodeType") == 1):
                    tmp = self.domCalc(i, node)
                    if tmp is not None:
                        node.childNodes.append(tmp)
                if i.get("nodeType") == 3:
                    try:
                        if not i.get('nodeValue').isspace():
                            tmp = self.domCalc(i, node)
                            if tmp is not None:
                                node.childNodes.append(tmp)
                    except KeyError:
                        print('abnormal text node')
                        print(i)

        return node
