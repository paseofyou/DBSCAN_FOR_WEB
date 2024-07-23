import time

import cv2

from common.config import Config


class ImageUtil:
    @staticmethod
    def drawImage(img_path, node_list, name="raw_draw", labels=None):
        img_path = Config.path + "/" + img_path
        if labels is None:
            labels = [1 for i in range(len(node_list))]
        # 读取截图
        image = cv2.imread(img_path)
        img = image.copy()
        # 绘制非噪声点的框选框
        for i, element in enumerate(node_list):
            if labels[i] != -1 and element.block.block_visual:
                x, y, width, height = int(element.x), int(element.y), int(element.width), int(
                    element.height)
                cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 255), 2)
        _img_name = img_path.split("\\", -1)[-1].split("/", -1)[-1]
        cv2.imwrite(img_path.replace(_img_name, name + ".png"), img)

    @staticmethod
    def saveImage(driver, file_name):
        default_width = 1920
        default_height = 1080
        time.sleep(5)
        total_height = driver.execute_script("return document.body.scrollHeight")
        if total_height is None:
            total_height = default_height
        driver.set_window_size(default_width, total_height)
        driver.save_screenshot(Config.path + "/" + file_name + '.png')
