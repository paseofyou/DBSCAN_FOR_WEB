from crawlPage.Crawler import Crawler
from util.ImageUtil import ImageUtil


def main():
    # crawler = Crawler()
    # crawler.get("www.baidu.com")
    # crawler.saveImage()
    # crawler = Crawler("www.baidu.com")
    crawler = Crawler("https://www.istockphoto.com/en/search/2/image-film?family=creative&phrase=mount")
    crawler.saveImage()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

