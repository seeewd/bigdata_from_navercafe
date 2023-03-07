import time
from selenium import webdriver
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()
total_list = ['번호', '제목', '날짜', '조회수']

# 파일 초기화
with open('crawl.csv', 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(total_list)

# crawling
url = 'https://nid.naver.com/nidlogin.login'
ids = os.environ.get("ID")
pw = os.environ.get("PW")
browser = webdriver.Chrome()
browser.get(url)

browser.implicitly_wait(2)

browser.execute_script("document.getElementsByName('id')[0].value=\'" + ids + "\'")
browser.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")

# 로그인 버튼 클릭
browser.find_element(By.XPATH, '//*[@id="log.login"]')

# baseurl = os.environ.get("BASE_URL")
baseurl = "https://cafe.naver.com/ArticleList.nhn?"
baseurl_for_page = "https://cafe.naver.com/ArticleRead.nhn?"
club_id = os.environ.get("CLUB_ID")
menu_id = os.environ.get("MENU_ID")
user_display = 50
boardType = 'L'  # 전체 게시글

i = 0
while True:
    pageNum = i + 1
    url = baseurl + f'&search.clubid={club_id}&search.menuid={menu_id}&search.boardtype=L&search.totalCount=151&search.page={pageNum}&userDisplay={user_display}'
    browser.get(url)

    # iframe으로 접근
    try:
        iframe = browser.find_element(By.ID, 'cafe_main')
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
        #
        if date:
            date = date.get_text().strip()
        else:
            date = "null"
        #
        if view_count:
            view_count = view_count.get_text().strip()
        else:
            view_count = "null"

        # 세부 페이지
        time.sleep(5)
        temp_url = baseurl_for_page
        browser.get(temp_url)
        texts = soup.select(".se-fs-")
        for i in texts:
            if "주소" in i:
                print(i)

        with open('crawl.csv', 'a+', newline='', encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow([idx, title, date, view_count])

    # Click on the next button to go to the next page
    # try:
    #     next_btn = browser.find_element(By.CSS_SELECTOR, "div.prev-next > div.prev-next-inside > a")
    #     if next_btn.get_attribute("title") == "다음":
    #         next_btn.click()
    #         i += 1
    #     else:
    #         print('No more pages to scrape')
    #         break
    # except:
    #     print('Error clicking on the next button')
    time.sleep(5)
    i += 1

# Close the browser
browser.quit()
# Pause for 5 minutes before scraping again
