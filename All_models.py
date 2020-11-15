from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
import time
import os
import pandas as pd

chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

driver.get('https://tfhub.dev/s?subtype=module,placeholder')
data = pd.DataFrame(columns=["Problem_domain", "Title", "Publisher", "Updated_date", "Description", "Architecture",
                             "Dataset"])

time.sleep(3)
while True:
    try:
        model_links = driver.find_elements_by_xpath(
            '//mat-sidenav-container/mat-sidenav-content//product-list/list-item-wrapper[contains(@class, '
            '\'ng-star-inserted\')]')

        for model in model_links[:-10]:
            mod_data = {"Problem_domain": model.find_element_by_css_selector('div.product-eyebrow').text,
                        "Title": model.find_element_by_css_selector('mat-card-title.mat-card-title').text,
                        "Publisher": model.find_element_by_css_selector(
                            'p.product-descriptor__publisher > a.product-descriptor__publisher-name.ng-star-inserted').text,
                        "Updated_date": model.find_element_by_css_selector('span.product-descriptor__last-updated').text,
                        "Description": model.find_element_by_css_selector('mat-card-subtitle.mat-card-subtitle').text}

            try:
                mod_data["Architecture"] = model.find_element_by_css_selector(
                    'div.product-bumper > p.product-chip.ng-star-inserted:nth-child(1) > a').text
            except:
                mod_data["Architecture"] = None
            try:
                mod_data["Dataset"] = model.find_element_by_css_selector(
                    'div.product-bumper > p.product-chip.ng-star-inserted:nth-child(2) > a').text
            except:
                mod_data["Dataset"] = None

            data = data.append(mod_data, ignore_index=True)

        button = driver.find_element_by_xpath("//button[contains(@aria-label,\"Next page\")]")
        if button.get_attribute("disabled") == "true":
            break
        button.click()
    except StaleElementReferenceException:
        time.sleep(0.5)

data.to_csv("model_1stMetadata.csv", mode="w")

driver.quit()
