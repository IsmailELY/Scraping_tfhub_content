from selenium import webdriver
import time
import os
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# Setting up the driver
chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

# Connecting to publisher's browser (You can adjust the sleep time depending on your network connection)
driver.get('https://tfhub.dev/s?subtype=publisher')
time.sleep(1)

# Creating a dataFrame for our publisher's metadata
data = pd.DataFrame(columns=["url_publisher", "Name_Publisher", "Collections", "Models", "Description"])
button = None

# looping through all pages present in the browser
while True:
    # index refering to the position order of each publisher within the page
    i = 0

    while True:
        try:
            time.sleep(1)

            # Retrieving the tag list of all publishers present in the (reloaded) page
            # This operation is necessary and not redundant
            publisher_links = driver.find_elements_by_xpath(
                '//mat-sidenav-container/mat-sidenav-content//product-list/list-item-wrapper[contains(@class, '
                '\'ng-star-inserted\')]')

            # Selecting a publisher
            publisher = publisher_links[i]

            # Collection metadata about the publisher (the only metadata about the publisher)
            publisher_data = {
                "Name_Publisher": publisher.find_element_by_css_selector('mat-card-title.mat-card-title').text,
                "Link_name": publisher.find_element_by_css_selector('mat-card-subtitle.mat-card-subtitle > h2').text,
                "Description": publisher.find_element_by_css_selector('mat-card-subtitle.mat-card-subtitle > p').text}

            # Some metadata may not be present
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

            # We look into the publisher to retrieve his url (urn unique to publisher)
            publisher.click()
            publisher_data["url_publisher"] = driver.current_url

        # handling reference load error
        except StaleElementReferenceException:
            time.sleep(0.5)
            continue

        # adding row to dataframe
        data = data.append(publisher_data, ignore_index=True)

        # waiting for previous-button to load
        while True:
            try:
                driver.find_element_by_css_selector(
                    "secondary-toolbar.ng-star-inserted mat-toolbar back-button button").click()
                break
            except:
                time.sleep(0.5)

        # next publisher in the list
        i += 1

        # condition to go to next page of publisher if it exists (10 last tags are by default empty)
        if i >= len(publisher_links[:-10]):
            button = driver.find_element_by_xpath("//button[contains(@aria-label,\"Next page\")]")
            break

    # checking if we looped through all the list or not
    if button.get_attribute("disabled") == "true":
        break
    button.click()

# saving the final data
data.to_csv("Publishers.csv", mode="w")
driver.quit()
