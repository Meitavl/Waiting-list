from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
import os.path
from datetime import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import sys

import data
import gui
import database
import user_gui
import data_compare
import main_gui
from email_send import send_email

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



def data_s(string: str, web_page: webdriver) -> list:

    web_page.find_element(By.XPATH, '//*[@id="DocName"]').clear()
    web_page.find_element(By.XPATH, '//*[@id="DocName"]').send_keys(string)
    time.sleep(0.2)
    doc_name = web_page.find_element(By.XPATH, '//*[@id="DocName_pop"]')
    doc_name_list = doc_name.text.splitlines()
    return doc_name_list


def save_time(year: int, month: int, doc_cal: list, driver: webdriver, i: int, db: database.Db) -> None:

    driver.implicitly_wait(0.5)

    for day in doc_cal:
        free_hours = []

        day.click()
        driver.implicitly_wait(0.1)

        # Morning calender
        WebDriverWait(driver, 6).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[1]')))
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

        month_queue(year, month, int(day.text), free_hours, i, db)


def create_sql_table(name: str) -> database.Db:
    db = database.Db()
    db.create_table(name)
    return db


def month_queue(year: int, month: int, day: int, hours: list, i: int, db: database.Db) ->None:

    with open('doc.csv', 'a', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        if i == 1:
            writer.writerow(('שנה', 'חודש', 'יום', 'שעה'))

        for hour in hours:
            tup = (year, month, day, hour)
            writer.writerow(tup)
            db.insert_to_table(tup)


def main(gui_main: main_gui.MainGui) -> None:
    '''
    התוכנה יוצרה לטובת עזרה במציאת תור פנוי בשירותי הבריאות מכבי.
    ניתן לבצע בדיקה לפי שם רופא.

    בהמשך מתוכנן הוספת אופציות של חיפוש לפי תחום ולפי מקום.

    :return:
    '''

    # Starting Chrome window
    s = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=3840,2160")  # Big Chrome window for seeing all buttons
    options.add_argument("--window-position=-10000,0")  # Position to working in the background
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(data.login_page)


    print(f'Program running in: \"{driver.title}\"')

    # web page long loading
    driver.implicitly_wait(20)

    # Getting user data from file
    file_name = 'userdata.csv'
    user_data = main_gui.load_data(file_name)

    # Auth part
    driver.find_element(By.LINK_TEXT, 'כניסה עם סיסמה').click()
    driver.find_element(By.ID, 'identifyWithPasswordCitizenId').send_keys(user_data[0][0])
    driver.find_element(By.ID, 'password').send_keys(user_data[0][1])
    driver.find_element(By.XPATH, '//*[@id="IdentifyWithPassword"]/button').click()

    # Navigating to doctors queue
    WebDriverWait(driver, 2).until(ec.element_to_be_clickable((By.LINK_TEXT, 'הבנתי, תודה')))
    driver.find_element(By.LINK_TEXT, 'הבנתי, תודה').click()
    driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_MainPlaceHolder_Body_wcHomeUserPersonalNavMenu_rptUserPersonalMenu_ctl00_imgOuter"]').click()
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/a[2]/button').click()
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/button[1]/div[2]').click()

    # Getting doctor name from user
    # from the second running read name from file

    if gui_main.entry['doc_name'].get() == '':
        gui.main(gui_main, driver)
    else:
        data_s(gui_main.entry['doc_name'].get(), driver)

    driver.find_element(By.XPATH, '// *[ @ id = "SearchButton"]').click()
    WebDriverWait(driver, 4).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#app > div > div > div > div > div.container.bgNone.infoPage > div.row.padding0Mobile.pageBreak.mitkan > div > div.col-md-6.docPropInnerWrap > div.disNonePrint.noFixed > div > a')))
    driver.find_element(By.CSS_SELECTOR, '#app > div > div > div > div > div.container.bgNone.infoPage > div.row.padding0Mobile.pageBreak.mitkan > div > div.col-md-6.docPropInnerWrap > div.disNonePrint.noFixed > div > a').click()
    WebDriverWait(driver, 4).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/button')))
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/button').click()
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/button').click()

    driver.implicitly_wait(2)

    db = create_sql_table('macc')  # Open sql table (not needed, only for practice)

    for i in range(1, 13):
        month = driver.find_element(By.XPATH, '//div[@class="DayPicker-Caption"]')

        year = re.findall('[0-9]+', month.text)[0]
        month = re.findall('[א-ת]+', month.text)[0]
        month = heb_to_eng[month]
        date = dt.strptime(f'{year}/{str(month)}/1', '%Y/%m/%d')
        end_date = dt.strptime(gui_main.entry['end_date'].get(), '%Y-%m-%d %H:%M:%S')
        if (date.year > end_date.year) or (date.month > end_date.month and date.year == end_date.year):
            break

        free_days = []

        try:
            doc_calender = driver.find_element(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available DayPicker-Day--selected"]')
            free_days.append(doc_calender)
            doc_calender1 = driver.find_elements(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available"]')
            free_days.extend(doc_calender1)

            save_time(date.year, date.month, free_days, driver, i, db)

        except ec.NoSuchElementException:
            print(f' There is no avalibale day in {date.month} {date.year}')
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH, '//span[@class="DayPicker-NavButton DayPicker-NavButton--next"]').click() # Next month

    driver.close()


    # os.remove('userdata.csv')


if __name__ == '__main__':
    count_miss = 0
    count = 0
    while True:
        exc = ''
        try:
            main()
        except:
            exc = sys.exc_info()
            print(exc[0])
            exc = exc[0]
            print(f'Problem with program {dt.now()}')

            count_miss += 1
        break_time = 600  # Running app every 10 minutes
        count += 1
        with open('log.csv', 'a') as f:
            writer = csv.writer(f)
            if count == 1:
                heading = ('Count', 'Time', 'Count miss', 'Exception')
                writer.writerow(heading)
            tup = (count, dt.now(), count_miss, exc)
            writer.writerow(tup)
        time.sleep(break_time)  # Running app every 10 minutes


