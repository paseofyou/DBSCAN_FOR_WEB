from analyze.dom_analyze import DomAnalyze
from crawlPage.crawler import Crawler
from util.ImageUtil import ImageUtil


def main():
    # crawler = Crawler("https://www.aliyun.com")
    # crawler.saveImageAndHtml()
    # domAnalyze = DomAnalyze(crawler)
    # domAnalyze.toDomJSON()

    domAnalyze = DomAnalyze(None)
    dom_list = domAnalyze.service()
    ImageUtil.drawImage(r"www.aliyun.com_23_09_39_31/www.aliyun.com.png", dom_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
