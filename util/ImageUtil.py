import time


class ImageUtil:
    @staticmethod
    def showImage(img):
        pass

    @staticmethod
    def saveImage(driver, path="screenshot.png"):
        default_width = 1920
        default_height = 1080
        time.sleep(5)
        total_height = driver.execute_script("return document.body.scrollHeight")
        if total_height is None:
            total_height = default_height
        driver.set_window_size(default_width, total_height)
        driver.save_screenshot(path + '.png')
