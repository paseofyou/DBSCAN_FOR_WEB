class Config:
    raw_path: str = r"E:\github\DBSCANDemo\DBSCAN_FOR_WEB"
    result_path: str = r"result"
    path: str = raw_path + "\\" + result_path
    # driver_path: str = r'C:\Program Files\Google\Chrome\test\chromedriver-win64\chromedriver.exe'
    # chrome_path: str = r'C:\Program Files\Google\Chrome\test\chrome-win64\chrome.exe'
    driver_path: str = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'
    chrome_path: str = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    VIPS_threshold = 99999

    #     debug
    test = "www.aliyun.com_29_13_46_45"
