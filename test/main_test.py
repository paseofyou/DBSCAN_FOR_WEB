import time

import cv2
import json
import numpy as np
from scipy.spatial.distance import cdist
from selenium import webdriver
from sklearn.cluster import DBSCAN
from PIL import Image
import matplotlib.pyplot as plt
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# 初始化Selenium WebDriver
gecko_driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(20)
driver.get('https://www.aliyun.com/')

default_width = 1920
default_height = 1080
time.sleep(5)

total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
scroll_position = 0
driver.set_window_size(width=default_width, height=total_height, windowHandle="current")
num = 0
while num < 5:
    driver.execute_script(f"window.scrollBy(0, 1000)")
    time.sleep(1)
    scroll_position += 1000
    total_height = driver.execute_script("return document.body.scrollHeight")
    if scroll_position >= total_height:
        num += 1

driver.execute_script(f"document.documentElement.scrollTop = 0;")
total_height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(default_width, total_height)

# 获取所有元素的位置信息
elements_info = driver.execute_script('''
    let elements = [];
    document.getElementsByTagName("BODY")[0].querySelectorAll('*').forEach(element => {
        let rect = element.getBoundingClientRect();
        let style = window.getComputedStyle(element);
        let tagName = element.tagName.toLowerCase();
        if (style.getPropertyValue("visibility") == 'hidden') return;
        if (tagName == 'html' || tagName == 'script' || tagName == 'noscript' || tagName =='style') return;
        if (rect.width > 0 && rect.height > 0) {
            let item = {
                'tag': tagName,
                'x': rect.left,
                'y': rect.top,
                'width': rect.width,
                'height': rect.height
            };
            elements.push(item);
        }
    });
    return elements;
''')

# 保存元素信息为JSON文件
with open('result/elements_info.json', 'w') as f:
    json.dump(elements_info, f)

# 截取网页截图
screenshot = driver.get_screenshot_as_png()
with open('result/screenshot.png', 'wb') as file:
    file.write(screenshot)

# 关闭WebDriver
driver.quit()

# 加载截图
image = cv2.imread('result/screenshot.png')

# 加载元素信息
with open('result/elements_info.json', 'r') as f:
    elements_info = json.load(f)

# 绘制初始框选框
initial_image = image.copy()
for element in elements_info:
    x, y, width, height = int(element['x']), int(element['y']), int(element['width']), int(element['height'])
    cv2.rectangle(initial_image, (x, y), (x + width, y + height), (0, 0, 255), 2)

# 保存带有初始框选框的图像
cv2.imwrite('result/screenshot_with_boxes.png', initial_image)

# # 显示初始框选框的图像
# img = Image.open('result/screenshot_with_boxes.png')
# img.show()

# 提取框选框的中心点坐标
centers = np.array([
    [int(element['x'] + element['width'] / 2), int(element['y'] + element['height'] / 2)]
    for element in elements_info
])


# 计算预计算的距离矩阵
distance_matrix = cdist(centers, centers, metric='euclidean')

# 使用DBSCAN进行聚类
db = DBSCAN(eps=10, min_samples=2, algorithm='brute', metric='precomputed').fit(distance_matrix)
labels = db.labels_

# 绘制聚类结果
unique_labels = set(labels)
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

# 加载截图
image = cv2.imread('result/screenshot.png')

for k, col in zip(unique_labels, colors):
    if k == -1:
        # 黑色用于噪声点，不绘制
        continue

    class_member_mask = (labels == k)

    xy = centers[class_member_mask]
    for point in xy:
        x, y = int(point[0]), int(point[1])
        cv2.circle(image, (x, y), 5, [int(c * 255) for c in col[:3]], -1)

# 绘制非噪声点的框选框
for i, element in enumerate(elements_info):
    if labels[i] != -1:  # 仅绘制非噪声点的框选框
        x, y, width, height = int(element['x']), int(element['y']), int(element['width']), int(element['height'])
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)

# 保存带有聚类结果和框选框的图像
cv2.imwrite('result/screenshot_with_clusters3.png', image)

# # 显示带有聚类结果的图像
# img = Image.open('screenshot_with_clusters.png')
# img.show()



