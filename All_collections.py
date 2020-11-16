from selenium import webdriver
import time
import os
from tqdm import tqdm
import pandas as pd

# Setting up the driver
chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

# Connecting to collection's browser (You can adjust the sleep time depending on your network connection)
driver.get('https://tfhub.dev/s?subtype=model-family')
time.sleep(1)

# Creating the dataFrame which we will be filling with collection metadata
data = pd.DataFrame(columns=["Title", "Publisher", "N_Models", "Updated_date", "Description"])

# Each loop will seek for all collection displayed in the page before hitting the next button
i = 1
while True:
    print("Page N° ", i)
    # time to load all elements
    time.sleep(0.5)
    collection_links = driver.find_elements_by_xpath(
        '//mat-sidenav-container/mat-sidenav-content//product-list/list-item-wrapper[contains(@class, '
        '\'ng-star-inserted\')]')

    # we loop through the collection retrieved but the 10 last elements are just empty tags (excluded)
    for coll in tqdm(collection_links[:-10]):
        coll_data = {"Title": coll.find_element_by_css_selector('mat-card-title.mat-card-title').text,
                     "Publisher": coll.find_element_by_css_selector("p.product-descriptor__publisher > "
                                                                    "a.product-descriptor__publisher-name.ng-star"
                                                                    "-inserted").text,
                     "N_Models": coll.find_element_by_css_selector("div.product-descriptor > div > p.ng-star-inserted "
                                                                   "> span").text,
                     "Updated_date": coll.find_element_by_css_selector("span.product-descriptor__last-updated").text,
                     "Description": coll.find_element_by_css_selector("mat-card-subtitle.mat-card-subtitle").text}

        # Adding the row to our DataFrame
        data = data.append(coll_data, ignore_index=True)

    # Saving collections collected from this page
    data.to_csv("Collection_retrieved.csv", mode="w")

    # Retrieving the next button
    button = driver.find_element_by_xpath("//button[contains(@aria-label,\"Next page\")]")

    # checking if the button is disabled -> last page
    if button.get_attribute("disabled") == "true":
        break

    # next page
    button.click()
    i += 1

driver.close()
