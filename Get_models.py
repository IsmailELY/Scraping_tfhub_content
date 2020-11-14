import os
import time

from selenium import webdriver

chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

driver.get('https://tfhub.dev/s?subtype=module,placeholder')
time.sleep(5)

while True:
    button = driver.find_element_by_xpath("//button[contains(@aria-label,\"Next page\")]")
    print(button.get_attribute("disabled"))
    if button.get_attribute("disabled") == "true":
        break
    time.sleep(2)
    button.click()
