import os
import time
from datetime import datetime
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from common.config import Config
from util.ImageUtil import ImageUtil


class Crawler:
    url = None
    filename = None
    file_path = None
    driver = None
    soup = None
    window_width = None
    window_height = None

    def __init__(self, url: str = None):
        print("爬虫资源加载中...")
        self.url = url
        self.setDriver()
        if url is not None:
            self.get(url)

    def setDriver(self):
        assert os.path.exists(Config.driver_path), f"浏览器驱动路径错误: {Config.driver_path}"
        assert os.path.exists(Config.chrome_path), f"浏览器exe路径错误: {Config.chrome_path}"
        chrome_options = Options()
        chrome_options.binary_location = Config.chrome_path
        chrome_options.add_argument('--headless')
        service = Service(executable_path=Config.driver_path)
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
        self.driver.execute_script(f"document.documentElement.scrollTop=0")
        # self.driver.set_window_size(width=default_width, height=total_height, windowHandle="current")
        time.sleep(2)
        self.window_width = default_width
        self.window_height = total_height

        self.driver.set_window_size(self.window_width, self.window_height)
        # 生成soup
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
        print("爬虫资源加载完毕")

    def setUrl(self, urlStr: str):
        # 设置url
        try:
            if urlStr.startswith('https://') or urlStr.startswith('http://'):
                self.url = urlStr
            else:
                self.url = 'http://' + urlStr
            parse_object = urlparse(self.url)
            self.file_path = parse_object.netloc + '_' + str(
                datetime.now().strftime('%d_%H_%M_%S')) + '/'
            self.filename = parse_object.netloc
            os.makedirs(Config.result_path + "/" + self.file_path)
        except (TypeError, AttributeError):
            print("url无效: " + str(urlStr))
            return

    def saveImageAndHtml(self):
        print("初始图像及源码输出中...")
        ImageUtil.saveImage(self.driver, self.file_path + self.filename, self.window_width, self.window_height)
        with open(Config.result_path + "/" + self.file_path + "source.html", "w", encoding="utf-8") as f:
            f.write(self.soup.prettify())
