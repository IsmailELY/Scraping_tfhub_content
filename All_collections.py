from selenium import webdriver
import time
import os
from tqdm import tqdm
import pandas as pd

chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

driver.get('https://tfhub.dev/s?subtype=model-family')
data = pd.DataFrame(columns=["Title", "Publisher", "N_Models", "Updated_date", "Description"])

while True:
    time.sleep(3)
    collection_links = driver.find_elements_by_xpath(
        '//mat-sidenav-container/mat-sidenav-content//product-list/list-item-wrapper[contains(@class, '
        '\'ng-star-inserted\')]')

    for coll in tqdm(collection_links[:-10]):
        coll_data = {"Title": coll.find_element_by_css_selector('mat-card-title.mat-card-title').text,
                     "Publisher": coll.find_element_by_css_selector("p.product-descriptor__publisher > "
                                                                    "a.product-descriptor__publisher-name.ng-star"
                                                                    "-inserted").text,
                     "N_Models": coll.find_element_by_css_selector("div.product-descriptor > div > p.ng-star-inserted "
                                                                   "> span").text,
                     "Updated_date": coll.find_element_by_css_selector("span.product-descriptor__last-updated").text,
                     "Description": coll.find_element_by_css_selector("mat-card-subtitle.mat-card-subtitle").text}

        data = data.append(coll_data, ignore_index=True)

    data.to_csv("Collection_retrieved.csv", mode="w")

    button = driver.find_element_by_xpath("//button[contains(@aria-label,\"Next page\")]")
    if button.get_attribute("disabled") == "true":
        break
    button.click()
driver.close()
