import time
from selenium import webdriver
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import TimeoutException

total_list = ['번호', '제목', '날짜', '조회수']

# 파일 초기화
with open('crawl.csv', 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(total_list)

# crawling
url = 'https://nid.naver.com/nidlogin.login'
ids = "null"
pw = "null"
browser = webdriver.Chrome('null')
browser.get(url)

browser.implicitly_wait(2)

browser.execute_script("document.getElementsByName('id')[0].value=\'" + ids + "\'")
browser.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")

# 로그인 버튼 클릭
browser.find_element_by_xpath('//*[@id="log.login"]')

baseurl = 'null'
clubid = 236
userDisplay = 50
boardType = 'L'  # 전체 게시글

i = 0
while True:
    i += 1
    pageNum = i + 1
    print(f'Scraping page {pageNum}')
    url = baseurl + f'&search.page={pageNum}&userDisplay={userDisplay}'
    # url = baseurl + f'&search.page={userDisplay}&search.page={pageNum}'
    browser.get(url)

    # iframe으로 접근
    try:
        iframe = browser.find_element_by_id('cafe_main')
        browser.switch_to.frame(iframe)
    except:
        print('Error switching to iframe')

    soup = bs(browser.page_source, 'html.parser')

    # 게시글만 가져오기
    articles = soup.select("#main-area > div:nth-child(4) > table > tbody > tr")

    if not articles:
        print('No more articles to scrape')
        break

    for article in articles:
        idx = article.find(class_="inner_number")
        title = article.find(class_="article")
        date = article.find(class_='td_date')
        view_count = article.find(class_='td_view')

        if idx:
            idx = idx.get_text().strip()
        else:
            idx = "null"

        if title:
            title = title.get_text().strip()
        else:
            title = "null"

        if date:
            date = date.get_text().strip()
        else:
            date = "null"

        if view_count:
            view_count = view_count.get_text().strip()
        else:
            view_count = "null"

        with open('crawl.csv', 'a+', newline='', encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow([idx, title, date, view_count])

            print(f"Scraped article: {title}")

    # Click on the next button to go to the next page
    try:
        next_btn = browser.find_element_by_css_selector("div.prev-next > div.prev-next-inside > a")
        if next_btn.get_attribute("title") == "다음":
            next_btn.click()
            i += 1
        else:
            print('No more pages to scrape')
            break
    except:
        print('Error clicking on the next button')
    time.sleep(5)

# Close the browser
browser.quit()
# Pause for 5 minutes before scraping again
