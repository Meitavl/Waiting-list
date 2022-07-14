from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import data
import gui


def data_s(string, web_page):

    web_page.find_element(By.XPATH, '//*[@id="DocName"]').clear()
    web_page.find_element(By.XPATH, '//*[@id="DocName"]').send_keys(string)
    time.sleep(0.5)
    doc_name = web_page.find_element(By.XPATH, '//*[@id="DocName_pop"]')
    doc_name_list = doc_name.text.splitlines()
    if len(doc_name_list):
        print(doc_name_list[0], len(doc_name_list))
    return doc_name_list


def main():

    chrome_driver_path = 'C:\Program Files (x86)\chromedriver.exe'
    s = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=s)
    driver.get(data.login_page)
    print(driver.title)

    # time.sleep(1)
    driver.implicitly_wait(20)

    driver.find_element(By.LINK_TEXT, 'כניסה עם סיסמה').click()
    driver.find_element(By.ID, 'identifyWithPasswordCitizenId').send_keys(data.user)
    driver.find_element(By.ID, 'password').send_keys(data.password)
    # time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="IdentifyWithPassword"]/button').click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, 'הבנתי, תודה').click()
    # time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_MainPlaceHolder_Body_wcHomeUserPersonalNavMenu_rptUserPersonalMenu_ctl00_imgOuter"]').click()
    # time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/a[2]/button').click()
    # time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/button[1]/div[2]').click()
    # time.sleep(3)
    doc = driver.page_source
    # with open('page.txt', 'w') as f:
    #     f.write(doc)
    city = doc[doc.index("Cities"):]
    fields = city[city.index('Fields'):]
    city = city[:city.index('Fields')]
    fields = fields[:fields.index('ChapterComments')]
    city_list = re.findall('"[א-ת. -]+"', city)
    fields_list = re.findall('"[א-ת. -/]+"', fields)
    # print(fields_list, len(fields_list), fields_list[-1])

    driver.implicitly_wait(0)
    # WebDriverWait(driver, 120).until(ec.element_located_to_be_selected(By.XPATH('//*[@id="SearchButton"]')))

    doc_n = gui.main(driver)

    time.sleep(20)

    # doc_name = driver.find_element(By.XPATH, '//*[@id="DocName"]').send_keys(doc_n)

    doc_name = driver.find_element(By.XPATH, '//*[@id="DocName"]')
    print(doc_name.text)
    field_area = driver.find_element(By.XPATH, '//*[@id="react-select-Field_select--value"]/div[1]')
    print(field_area.text)
    city_area = driver.find_element(By.XPATH, '//*[@id="react-select-City_select--value"]/div[1]')
    print(city_area.text)

    driver.close()


if __name__ == '__main__':
    main()
