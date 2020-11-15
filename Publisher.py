from selenium import webdriver
import time
import os

import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

driver.get('https://tfhub.dev/s?subtype=publisher')
data = pd.DataFrame(columns=["url_publisher", "Name_Publisher", "Collections", "Models", "Description"])
time.sleep(1)
button = None

while True:
    i = 0
    while True:
        try:
            time.sleep(1)
            publisher_links = driver.find_elements_by_xpath(
                '//mat-sidenav-container/mat-sidenav-content//product-list/list-item-wrapper[contains(@class, '
                '\'ng-star-inserted\')]')
            publisher = publisher_links[i]
            publisher_data = {
                "Name_Publisher": publisher.find_element_by_css_selector('mat-card-title.mat-card-title').text,
                "Description": publisher.find_element_by_css_selector('mat-card-subtitle.mat-card-subtitle').text}

            try:
                publisher_data["Collections"] = publisher.find_element_by_css_selector(
                    'p.ng-star-inserted:nth-child(1) > span').text
            except:
                publisher_data["Collections"] = None
            try:
                publisher_data["Models"] = publisher.find_element_by_css_selector(
                    'p.ng-star-inserted:nth-child(2) > span').text
            except:
                publisher_data["Models"] = None

            publisher.click()
            publisher_data["url_publisher"] = driver.current_url
            data = data.append(publisher_data, ignore_index=True)
            time.sleep(0.5)
            try:
                driver.find_element_by_css_selector(
                    "secondary-toolbar.ng-star-inserted mat-toolbar back-button button").click()
            except:
                time.sleep(1)
                driver.find_element_by_css_selector(
                    "secondary-toolbar.ng-star-inserted mat-toolbar back-button button").click()
            i += 1
            if i >= len(publisher_links[:-10]):
                button = driver.find_element_by_xpath("//button[contains(@aria-label,\"Next page\")]")
                break
        except StaleElementReferenceException:
            time.sleep(0.5)
            continue

    if button.get_attribute("disabled") == "true":
        break
    button.click()

data.to_csv("Publishers.csv", mode="w")
driver.quit()

