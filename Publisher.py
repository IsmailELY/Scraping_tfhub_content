#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install requests_html')


# In[1]:


from requests_html import HTML, HTMLSession, AsyncHTMLSession
from selenium import webdriver
import time
import os
import pandas as pd


# In[30]:


chrome = os.path.abspath('C:/Users/dell/Downloads/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(chrome)

driver.get('https://tfhub.dev/s?subtype=publisher')
data = pd.DataFrame(columns=["Publisher","Name_Publisher","Collections","Models","Description"])

while True:
    time.sleep(3)
    button = driver.find_element_by_xpath("//button[contains(@aria-label,\"Next page\")]")
    publisher_links = driver.find_elements_by_xpath(
        '//mat-sidenav-container/mat-sidenav-content//product-list/list-item-wrapper[contains(@class, '
        '\'ng-star-inserted\')]')

    for publisher in publisher_links[:-10]:
        publisher_data = {"Publisher": publisher.find_element_by_css_selector('div.product-eyebrow').text,
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

        data = data.append(publisher_data, ignore_index=True)

    if button.get_attribute("disabled") == "true":
        break
    button.click()
    data.to_csv("D:/Data_publisher.csv", mode="w")

driver.quit()


# In[32]:


data.to_csv("D:/Data_publisher.csv")


# In[ ]:




