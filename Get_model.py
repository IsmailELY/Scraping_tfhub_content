from selenium import webdriver
import time
import os

from selenium.webdriver.support.select import Select
from tqdm import tqdm
import pandas as pd

chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

# driver.get('https://tfhub.dev/google/bert_uncased_L-12_H-768_A-12/1')
driver.get('https://tfhub.dev/google/universal-sentence-encoder-large/5')
# driver.get('https://tfhub.dev/google/nonsemantic-speech-benchmark/trill/3')
# driver.get('https://tfhub.dev/tensorflow/coral-model/mobilenet_v1_1.0_224_quantized/1/default/1')

data = pd.DataFrame(columns=['Name', 'Format', 'Downloads', 'language', 'Description', 'Tunable', 'model_link',
                             'Version', 'Size'])

time.sleep(3)

Formats = driver.find_elements_by_css_selector('div[role=\'tab\']')

# Format
try:
    Format = driver.find_element_by_css_selector('section.overview div p.tag:nth-child(4) span').text
except:
    Format = None

# Name,Downloads, Tunable, model, size,Description


# language
try:
    language = driver.find_element_by_xpath('//div[contains(text(), "Language:")]/parent::div/a').text
except:
    language = None

# get versions
try:
    Version_button = driver.find_element_by_css_selector('section.title > mat-form-field div.mat-form-field-wrapper '
                                                         'div.mat-form-field-flex div.mat-form-field-infix mat-select '
                                                         'div.mat-select-trigger')
    version = Version_button.find_element_by_css_selector('div span span').text
    Version_button.click()
    Options = driver.find_elements_by_css_selector('div[role="listbox"] > mat-option')
    total_versions = str(len(Options))
except:
    version = '1'
    total_versions = '1'

# links
a_links = driver.find_elements_by_css_selector('section.documentation markdown-snippet div a')
links_associated = [x.get_attribute("href") for x in a_links]
data_model = {
    'Name': driver.find_element_by_css_selector('div.overview h2').text,
    'Format': Format,
    'Version': version,
    'Downloads':
        driver.find_element_by_css_selector('div.usage.ng-star-inserted > download-count-label span').text.split()[0],
    'Tunable': driver.find_element_by_css_selector('section.overview div p.tag:nth-child(1) span').text,
    'model_link': driver.find_element_by_css_selector('download-button.ng-star-inserted a').get_attribute("href"),
    'Size': driver.find_element_by_css_selector('download-button.ng-star-inserted a button span span').text,
    'Description': driver.find_element_by_css_selector('section.overview div p.description').text,
    'total_versions': total_versions,
    'links_associated': links_associated,
    'language': language,
}
data = data.append(data_model, ignore_index=True)
data.to_csv("model_sample.csv")
driver.close()
