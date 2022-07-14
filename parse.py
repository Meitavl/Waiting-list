from bs4 import BeautifulSoup
import html5lib

with open('doc_calender_page.txt', 'r') as f:
    doc_cal_page = f.read()
    soup = BeautifulSoup(doc_cal_page, 'html5lib')
with open('doc_calender_page_html.txt', 'w') as f:
    f.write(soup.prettify())
