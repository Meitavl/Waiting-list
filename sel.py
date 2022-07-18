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
import database


heb_to_eng = {
    'ינואר': 1,
    'פברואר': 2,
    'מרץ': 3,
    'אפריל': 4,
    'מאי': 5,
    'יוני': 6,
    'יולי': 7,
    'אוגוסט': 8,
    'ספטמבר': 9,
    'אוקטובר': 10,
    'נובמבר': 11,
    'דצמבר': 12,
}


def data_s(string, web_page):

    web_page.find_element(By.XPATH, '//*[@id="DocName"]').clear()
    web_page.find_element(By.XPATH, '//*[@id="DocName"]').send_keys(string)
    time.sleep(0.2)
    doc_name = web_page.find_element(By.XPATH, '//*[@id="DocName_pop"]')
    doc_name_list = doc_name.text.splitlines()
    return doc_name_list


def save_time(year, month, doc_cal, driver, i, db):

    driver.implicitly_wait(0.5)

    for day in doc_cal:
        free_hours = []

        day.click()


        # Morning calender
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[1]').click()
        hours_cal = driver.find_elements(By.XPATH, '//*[@id="btnsConatiner"]/button')
        for item in hours_cal:
            free_hours.append(item.text)

        # Noon calender
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[2]').click()
        hours_cal = driver.find_elements(By.XPATH, '//*[@id="btnsConatiner"]/button')
        for item in hours_cal:
            free_hours.append(item.text)

        # Evening calender
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[3]').click()
        hours_cal = driver.find_elements(By.XPATH, '//*[@id="btnsConatiner"]/button')  # Hours
        for item in hours_cal:
            free_hours.append(item.text)

        month_queue(year, month, day.text, free_hours, i, db)


def create_sql_table(name):
    db = database.Db()
    db.create_table(name)
    return db


def month_queue(year, month, day, hours, i, db):

    with open('doc.csv', 'a', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        if i == 1:
            writer.writerow(('שנה', 'חודש', 'יום', 'שעה'))

        for hour in hours:
            # print(f'{year} month is: {month} and day is: {day}')
            tup = (int(year), month, int(day), hour)
            writer.writerow(tup)
            db.insert_to_table(tup)


def main():

    chrome_driver_path = 'C:\Program Files (x86)\chromedriver.exe'
    s = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=s)
    driver.get(data.login_page)
    driver.maximize_window()
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


    # WebDriverWait(driver, 120).until(ec.element_located_to_be_selected(By.XPATH('//*[@id="SearchButton"]')))

    gui.main(driver)

    driver.find_element(By.XPATH, '// *[ @ id = "SearchButton"]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#app > div > div > div > div > div.container.bgNone.infoPage > div.row.padding0Mobile.pageBreak.mitkan > div > div.col-md-6.docPropInnerWrap > div.disNonePrint.noFixed > div > a').click()
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/button').click()
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/button').click()

    driver.implicitly_wait(2)

    db = create_sql_table('macc')

    for i in range(1, 13):
        month = driver.find_element(By.XPATH, '//div[@class="DayPicker-Caption"]')

        year = re.findall('[0-9]+', month.text)[0]
        month = re.findall('[א-ת]+', month.text)[0]
        month = heb_to_eng[month]



        free_days = []


        try:
            doc_calender = driver.find_element(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available DayPicker-Day--selected"]')
            free_days.append(doc_calender)
            save_time(year, month, free_days, driver, i, db)
            doc_calender = driver.find_elements(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available"]')
            free_days.extend(doc_calender)


            save_time(year, month, free_days[1:], driver, i, db)


        except ec.NoSuchElementException:
            print(f' There is no avalibale day in {month} {year}')
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH, '//span[@class="DayPicker-NavButton DayPicker-NavButton--next"]').click() # next month

    driver.close()


if __name__ == '__main__':
    main()
