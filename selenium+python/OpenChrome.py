from selenium import webdriver
import time

def open_chrome(url):
    # 打开Chrome
    driver = webdriver.Chrome('G:/Python_Project/chromedriver.exe')

    # 最大化窗口
    driver.maximize_window()

    # 打开网址
    driver.get(url)

    time.sleep(2)
    # 执行自动化
    driver.find_element_by_id('fromStationText').click()
    driver.find_element_by_id('fromStationText').send_keys('新余', '\n')
    driver.find_element_by_id('toStationText').click()
    driver.find_element_by_id('toStationText').send_keys('上海', '\n')
    driver.find_element_by_xpath("//a[@id='query_ticket']").click()

    driver.refresh()

    s = driver.find_element_by_id('YW_620000K7600K')
    print(s)

