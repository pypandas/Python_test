from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import random


# 导入Chrome driver
driver = webdriver.Chrome('G:\Python_Project\chromedriver.exe')
driver.maximize_window()


# 登入后台
driver.get('https://web.fghy888.com/superadmin/index.php/Admin/login.html')
driver.find_element_by_id('user_name').send_keys('dehua')
driver.find_element_by_id('user_pwd').send_keys('112233')
driver.find_element_by_id('login_btn').click()

# 刷新浏览器状态
driver.refresh()
print(driver.current_url)

time.sleep(1)


# 点击在线监控
driver.find_element_by_link_text('日常运营管理').click()
driver.find_element_by_link_text('在线玩家列表').click()
driver.find_element_by_link_text('在线普通用户(游戏中)').click()

time.sleep(1)

# 获取在线用户
element = driver.find_element_by_xpath("//tr[@name='1092']")
user_id = element.text.split(" ")[6]


# 名单管理
driver.find_element_by_link_text("玩家管理").click()
driver.find_element_by_link_text("名单管理").click()
driver.find_element_by_id("uid").send_keys(user_id, "\n")
time.sleep(1)
driver.refresh()
time.sleep(1)
driver.find_element_by_xpath("//a[@id='tr-a(0)']").click()
time.sleep(1)
driver.find_element_by_xpath("//li[@class='Popover-li gm_li']//a").click()
time.sleep(1)
driver.find_element_by_xpath("//body//label[6]").click()
time.sleep(1)
driver.find_element_by_xpath("//div[7]//div[2]//select[1]//option[1]").click()
time.sleep(1)
driver.find_element_by_xpath("//body//div//div//div//div//div//div//div//option[3]").click()
time.sleep(1)
driver.find_element_by_xpath("//input[@id='condition']").clear()
time.sleep(1)
driver.find_element_by_xpath("//input[@id='condition']").send_keys(random.randint(300, 1000))
time.sleep(1)
driver.find_element_by_xpath("//button[@id='sub_but']").click()
