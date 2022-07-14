from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv

import data
import gui


def data_s(string, web_page):

    web_page.find_element(By.XPATH, '//*[@id="DocName"]').clear()
    web_page.find_element(By.XPATH, '//*[@id="DocName"]').send_keys(string)
    time.sleep(0.2)
    doc_name = web_page.find_element(By.XPATH, '//*[@id="DocName_pop"]')
    doc_name_list = doc_name.text.splitlines()
    return doc_name_list

def save_time():
    pass


def month_queue(year, month, days, i):
    with open('doc.csv', 'a', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        if i == 1:
            writer.writerow(('שנה', 'חודש', 'יום'))
        for day in days:
            print(f'{year} month is: {month} and day is: {day.text}')
            tup = (year, month, day.text)
            writer.writerow(tup)


def main():

    chrome_driver_path = 'C:\Program Files (x86)\chromedriver.exe'
    s = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=s)
    driver.get(data.login_page)
    # driver.minimize_window()
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
    # doc = driver.page_source
    # with open('page.txt', 'w') as f:
    #     f.write(doc)
    # city = doc[doc.index("Cities"):]
    # fields = city[city.index('Fields'):]
    # city = city[:city.index('Fields')]
    # fields = fields[:fields.index('ChapterComments')]
    # city_list = re.findall('"[א-ת. -]+"', city)
    # fields_list = re.findall('"[א-ת. -/]+"', fields)
    # print(fields_list, len(fields_list), fields_list[-1])

    # WebDriverWait(driver, 120).until(ec.element_located_to_be_selected(By.XPATH('//*[@id="SearchButton"]')))

    gui.main(driver)

    driver.find_element(By.XPATH, '// *[ @ id = "SearchButton"]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#app > div > div > div > div > div.container.bgNone.infoPage > div.row.padding0Mobile.pageBreak.mitkan > div > div.col-md-6.docPropInnerWrap > div.disNonePrint.noFixed > div > a').click()
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/button').click()
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/button').click()

    driver.implicitly_wait(2)
    for i in range(1, 13):
        month = driver.find_element(By.XPATH, '//div[@class="DayPicker-Caption"]')

        year = re.findall('[0-9]+', month.text)[0]
        month = re.findall('[א-ת]+', month.text)[0]

        free_days = []

        try:
            doc_calender = driver.find_element(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available DayPicker-Day--selected"]')
            free_days.append(doc_calender)
            doc_calender = driver.find_elements(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available"]')
            free_days.extend(doc_calender)

            month_queue(year, month, free_days, i)
        except ec.NoSuchElementException:
            print(f' There is no avalibale day in {month} {year}')

        driver.find_element(By.XPATH, '//span[@class="DayPicker-NavButton DayPicker-NavButton--next"]').click() # next month

    driver.close()


if __name__ == '__main__':
    main()
