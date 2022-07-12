from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import data
import time

chrome_driver_path = 'C:\Program Files (x86)\chromedriver.exe'
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)
driver.get(data.login_page)
print(driver.title)

time.sleep(1)

driver.find_element(By.LINK_TEXT, 'כניסה עם סיסמה').click()
driver.find_element(By.ID, 'identifyWithPasswordCitizenId').send_keys(data.user)
driver.find_element(By.ID, 'password').send_keys(data.password)
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="IdentifyWithPassword"]/button').click()
time.sleep(3)
driver.find_element(By.LINK_TEXT, 'הבנתי, תודה').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_MainPlaceHolder_Body_wcHomeUserPersonalNavMenu_rptUserPersonalMenu_ctl00_imgOuter"]').click()
time.sleep(10)
driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/a[2]/button').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/button[1]/div[2]').click()
doc = driver.page_source
# print(doc)
city = doc[doc.index("Cities"):]
city = city[:city.index('Fields')]
city_list = re.findall('"[א-ת. ]+"', city)
print(city_list[0], len(city_list), city_list[-1])


driver.close()