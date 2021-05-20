import os
import time
import csv
import json

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class ArticleUrl:
    def __init__(self, title, url, asset):
        self.title = title
        self.url = url
        self.asset = asset

    def print(self):
        print(self.title)
        print(self.url)
        print(self.asset)

    def text(self, text):
        self.text = text


symbol_reader = csv.reader(open("./nyse-listed_csv.csv"))
symbols = []
for pair in symbol_reader:
    symbols.append(pair[0])
symbols = symbols[1:]

chrome_driver_path = 'C:\Program Files (x86)\chromedriver.exe'
file_list = os.listdir("./")

not_js_options_headless = Options()
not_js_options_headless.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})
# As other user i dont need headless run, i can run this in "background"
# not_js_options_headless.add_argument("--headless")
headless_options = Options()
# headless_options.add_argument("--headless")
headless_options.add_argument("start-maximized")

driver = webdriver.Chrome(chrome_driver_path, options=headless_options)
driver.get("https://www.reuters.com")
try:
    element = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.ID, "accept-recommended-btn-handler")))
except selenium.common.exceptions.TimeoutException:
    print("WTF there should be data collection question, not timeout")
    quit()
finally:
    element.click()
for symbol in symbols:
    if symbol + ".csv" in file_list:
        print(f"{symbol} already scrapped ( no updating yet )")
        continue
    test_url = f"https://www.reuters.com/companies/{symbol}/news"
    url = test_url
    driver.implicitly_wait(0.5)
    driver.get(test_url)
    asset_site = driver.find_elements_by_xpath(
        "//div[contains(concat(' ',normalize-space(@class),' '),'QuoteRibbon-heading')]")
    if len(asset_site) == 0:
        print(f"No such asset as {symbol}")
        continue
    asset = asset_site[0].find_element_by_tag_name('p').text
    csv_file = open(f'./{asset}.csv', 'w', encoding="utf-8")
    print(f"{asset}")
    csv_writer = csv.writer(csv_file)

    previous_item_count = 0
    scroll_down = ActionChains(driver)
    old_count = len(driver.find_elements_by_class_name("item"))
    while True:
        page_bottom = driver.find_element_by_xpath(
            "//div[contains(concat(' ',normalize-space(@class),' '),'TwoColumnsLayout-footer')]")
        scroll_down.move_to_element(page_bottom).perform()
        time.sleep(0.3)
        new_count = driver.find_elements_by_class_name("item")
        if old_count == new_count:
            break
        old_count = new_count
    articles = driver.find_elements_by_class_name("item")
    usable_articles = []
    for article in articles:
        interesting_class = article.find_element_by_tag_name('a')
        article_object = ArticleUrl(interesting_class.text, interesting_class.get_property('href'), asset)
        usable_articles.append(article_object)
    article_in_file_id = int(1)
    smoll_driver = webdriver.Chrome(chrome_driver_path, options=not_js_options_headless)
    for usable_article in usable_articles:
        smoll_driver.delete_all_cookies()
        smoll_driver.get(usable_article.url)
        date_elements = smoll_driver.find_elements_by_id('__NEXT_DATA__')
        if len(date_elements) == 0:
            date = smoll_driver.find_elements_by_tag_name('time')
            if len(date) == 0:
                continue
            else:
                date = smoll_driver.find_elements_by_tag_name('time')[0].text
        else:
            big_json = json.loads(date_elements[0].get_property('text'))
            date_pretenders = big_json["props"]["initialState"]["meta"]
            for date_pretender in date_pretenders:
                if "props" in date_pretender:
                    if "name" in date_pretender["props"]:
                        if date_pretender["props"]["name"] == "sailthru.date":
                            date = date_pretender["props"]["content"]
        # Without javascript there is nothing to accept
        # try:
        #     element = WebDriverWait(smoll_driver, 10).until(
        #         expected_conditions.element_to_be_clickable((By.ID, "accept-recommended-btn-handler")))
        #     element.click()
        # except selenium.common.exceptions.TimeoutException:
        #     print("Something went wrong")
        paragraphs = smoll_driver.find_elements_by_xpath(
            "//*[contains(concat(' ',normalize-space(@class),' '),'paragraph')" +
            "or contains(concat(' ',normalize-space(@data-testid),' '),'paragraph') ]")
        # Load data from __NEXT_DATA__ all the time
        # if len(date_elements) == 0:
        csv_row = [article_in_file_id, usable_article.url, date.replace("\n", " "),
                   usable_article.title.replace("\n", " ")]
        for paragraph in paragraphs:
            csv_row.append(paragraph.text.replace("\n", " "))
        print(f"Article date {csv_row[2]}")
        csv_writer.writerow(csv_row)
        time.sleep(0.1)
        article_in_file_id += 1
    csv_file.close()
    smoll_driver.close()
