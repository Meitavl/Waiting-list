from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
from datetime import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

import gui
import main_gui
import settings
import doc_choose_gui as dcg


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
    time.sleep(0.1)
    ignored_exceptions = (ec.NoSuchElementException, ec.StaleElementReferenceException,)
    WebDriverWait(web_page, 0.5, ignored_exceptions=ignored_exceptions).until(ec.presence_of_element_located((By.XPATH, '//*[@id="DocName_pop"]')))
    doc_name = web_page.find_element(By.XPATH, '//*[@id="DocName_pop"]')
    doc_name = doc_name.text
    doc_name_list = doc_name.splitlines()
    return doc_name_list


def save_time(year: int, month: int, day: int, driver: webdriver, i=0) -> None:

    free_hours = []

    driver.implicitly_wait(1)

    # Morning calender
    try:
        WebDriverWait(driver, 0.5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div')))
        all_day = driver.find_elements(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div')
    except:
        all_day = driver.find_elements(By.XPATH, '//*[@id="tab"]/div[1]/ul/li')
    all_day[0].click()
    mor_hours = driver.find_elements(By.XPATH, '//*[@id="btnsConatiner"]/button')
    for hour in mor_hours:
        free_hours.append(hour.text)

    # Noon calender
    # driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[2]').click()
    all_day[1].click()
    noon_hours = driver.find_elements(By.XPATH, '//*[@id="btnsConatiner"]/button')
    for hour in noon_hours:
        free_hours.append(hour.text)

    # Evening calender
    # driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[3]').click()
    all_day[2].click()
    ev_hours = driver.find_elements(By.XPATH, '//*[@id="btnsConatiner"]/button')  # Hours
    for hour in ev_hours:
        free_hours.append(hour.text)

    month_queue(free_hours, i, year, month, day)


def month_queue(hours: list, i: int, *args) ->None:

    if i == 1:
        with open('doc.csv', 'w', newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(('שנה', 'חודש', 'יום', 'שעה'))
            for hour in hours:
                tup = args + (hour,)
                writer.writerow(tup)
    else:
        with open('doc.csv', 'a', newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            for hour in hours:
                tup = args + (hour,)
                writer.writerow(tup)
                # db.insert_to_table(tup)


def have_queue(driver: webdriver, doc_name, gui_main):
    driver.implicitly_wait(1)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[2]/div/div/nav/div/div[2]/div/div[2]/div/div[3]/div[2]/li[1]/a').click()
    tmp = driver.find_elements(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div/div')
    for ind in range(len(tmp)):
        text_tmp = tmp[ind].text
        if doc_name in text_tmp:
            i = ind + 1
            date = re.findall('[0-9/:]+', text_tmp)
            date = dt.strptime(date[0] + ' ' + date[1], '%d/%m/%y %H:%M')
            gui_main.information(queue=date)
            break
    driver.find_element(By.XPATH, f'//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div/div[{i}]/div[1]/div[2]/span/span[1]').click()

    # driver.find_element(By.LINK_TEXT, 'עריכת תור').click()
    try:
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[7]/button[1]').click()
    except:
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[6]/button[1]').click()
    # חזרה לריצה רגילה


def main(gui_main: main_gui.MainGui) -> None:
    '''
    התוכנה יוצרה לטובת עזרה במציאת תור פנוי בשירותי הבריאות מכבי.
    ניתן לבצע בדיקה לפי שם רופא.

    בהמשך מתוכנן הוספת אופציות של חיפוש לפי תחום ולפי מקום.

    :return:
    '''

    # Starting Chrome window
    login_page = settings.login_page
    s = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=3840,2160")  # Changing Chrome window size for seeing all buttons
    options.add_argument("--window-position=-10000,0")  # Position to working in the background
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(login_page)

    # web page long loading
    driver.implicitly_wait(15)

    # Getting user data from file
    file_name = 'userdata.csv'
    user_data = main_gui.load_data(file_name)

    # Auth part
    driver.find_element(By.LINK_TEXT, 'כניסה עם סיסמה').click()
    driver.find_element(By.ID, 'identifyWithPasswordCitizenId').send_keys(user_data[0][0])
    driver.find_element(By.ID, 'password').send_keys(user_data[0][1])
    driver.find_element(By.XPATH, '//*[@id="IdentifyWithPassword"]/button').click()

    assert driver.find_element(By.XPATH, '//*[@id="IdentifyWithPassword"]/div[3]/div').is_displayed() == False, 'Wrong id or password'
    print(f'Connection establish')

    # Navigating to doctors queue
    WebDriverWait(driver, 2).until(ec.element_to_be_clickable((By.LINK_TEXT, 'הבנתי, תודה')))
    driver.find_element(By.LINK_TEXT, 'הבנתי, תודה').click()
    driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_MainPlaceHolder_Body_wcHomeUserPersonalNavMenu_rptUserPersonalMenu_ctl00_imgOuter"]').click()
    if gui_main.entry['have_queue'].get() == 'כן':
        have_queue(driver, gui_main.entry['doc_name'].get(), gui_main)
        check_queue(driver, gui_main)
        return
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/a[2]/button').click()
    driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/button[1]/div[2]').click()

    # Getting doctor name from user
    # from the second running read name from file

    if gui_main.entry['doc_name'].get() == '':
        gui.main(gui_main, driver)
    else:
        data_s(gui_main.entry['doc_name'].get(), driver)

    doc_name = gui_main.entry['doc_name'].get()
    driver.find_element(By.XPATH, '// *[ @ id = "SearchButton"]').click()

    # Choosing doc office
    tmp = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div/div/div/div[2]/div[3]/div')
    time.sleep(0.5)
    for ind in range(len(tmp)):
        if doc_name in tmp[ind].text:
            i = ind + 1
    if i == 1:
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div[2]/div[3]/div/div[4]/div[4]/div/a').click()
    if i == 2:
        tmp = driver.find_elements(By.XPATH, f'//*[@id="app"]/div/div/div/div/div[2]/div[3]/div[2]/div[2]/div/div')
        address = gui_main.entry['address'].get()
        if address == '':
            choose = dcg.ChooseGui(tmp, driver)
            i = choose.doc_index
            address = tmp[i-1].text.splitlines()
            address = address[address.index('כתובת') + 1]
            gui_main.information(address=address)
        else:
            for ind in range(len(tmp)):
                if address in tmp[ind].text:
                    i = ind + 1
        driver.find_element(By.XPATH, f'//*[@id="app"]/div/div/div/div/div[2]/div[3]/div[2]/div[2]/div/div[{i}]/div[2]/div[4]/a').click()
    # TODO if have queue
    try:
        driver.find_element(By.CSS_SELECTOR, 'body > div > div > div.modal.fade.show > div > div > div.modal-footer > button').click()
        gui_main.information(have_queue='כן')
        driver.close()
        return
    except ec.NoSuchElementException:
        gui_main.information(have_queue='לא')

    check_queue(driver, gui_main)


def check_queue(driver, gui_main):
    try:
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/button').click()
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/button').click()
    except:
        print('')
    driver.implicitly_wait(2)

    date = driver.find_element(By.XPATH, '//div[@class="DayPicker-Caption"]')
    date = date.text
    year = re.findall('[0-9]+', date)[0]
    month = re.findall('[א-ת]+', date)[0]
    month = heb_to_eng[month]

    # WebDriverWait(driver, 2).until(ec.element_to_be_clickable((By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available DayPicker-Day--selected"]') ))
    day = driver.find_element(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available DayPicker-Day--selected"]')
    date = dt.strptime(f'{year}/{str(month)}/{day.text}', '%Y/%m/%d')
    start_date = dt.strptime(gui_main.entry['start_date'].get(), '%Y-%m-%d %H:%M:%S')
    end_date = dt.strptime(gui_main.entry['end_date'].get(), '%Y-%m-%d %H:%M:%S')
    if start_date <= date <= end_date and gui_main.button['set']['bg'] == 'green':  # If date in range set queue
        new_queue = driver.find_elements(By.XPATH, '//*[@id="btnsConatiner"]/button')
        new_queue[0].click()
        date = date.replace(hour=int(new_queue[0].text[:2]), minute=int(new_queue[0].text[3:]))
        gui_main.information(queue=date)
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[2]/button[1]').click()
        driver.find_element(By.XPATH, '//*[@id="app-wrap"]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[5]/button[1]').click()
        gui_main.information(have_queue='כן')
        gui_main.button['set']['bg'] = 'red'

    elif date <= end_date:

        j = 1
        for i in range(1, 13):
            if date > end_date:
                break
            free_days = []
            try:

                date = driver.find_element(By.XPATH, '//div[@class="DayPicker-Caption"]')
                year = re.findall('[0-9]+', date.text)[0]
                month = re.findall('[א-ת]+', date.text)[0]
                month = heb_to_eng[month]

                day = driver.find_element(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available DayPicker-Day--selected"]')
                date = dt.strptime(f'{year}/{str(month)}/{day.text}', '%Y/%m/%d')
                save_time(date.year, date.month, date.day, driver, j)
                j += 1

                doc_calender1 = driver.find_elements(By.XPATH, '//div[@class="DayPicker-Day DayPicker-Day--available"]')
                free_days.extend(doc_calender1)

                for day in free_days:
                    date = dt.strptime(f'{year}/{str(month)}/{day.text}', '%Y/%m/%d')
                    if date > end_date:
                        break
                    day.click()
                    save_time(date.year, date.month, date.day, driver)

            except ec.NoSuchElementException:
                print(f' There is no avalibale day in {date.month} {date.year}')
            driver.implicitly_wait(2)
            driver.find_element(By.XPATH, '//span[@class="DayPicker-NavButton DayPicker-NavButton--next"]').click() # Next month
    driver.close()

