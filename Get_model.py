from selenium import webdriver
import time
import os

from tqdm import tqdm
import pandas as pd

chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

publishers = pd.read_csv("Publishers.csv", index_col=[0], engine='python')
models_Meta = pd.read_csv("model_1stMetadata.csv", index_col=[0], engine='python')

dict_pub = {pub: url for pub, url in zip(publishers.loc[:, "Name_Publisher"], publishers.loc[:, "url_publisher"])}

data = pd.DataFrame(columns=['Name', 'Format', 'Downloads', 'language', 'Description', 'Tunable', 'model_link',
                             'Version', 'Size'])

for i in tqdm(range(models_Meta.shape[0])):
    url = dict_pub[models_Meta.loc[i, "Publisher"]] + "/" + models_Meta.loc[i, "Title"]
    print("\nRetrieving: ", url)
    driver.get(url)
    time.sleep(2)

    form = 0
    while True:
        Formats = driver.find_elements_by_css_selector('div[role=\'tab\']')
        try:
            Formats[form].click()
        except IndexError:
            print(len(Formats), " ", form)
        time.sleep(0.5)
        break_point = False
        i = 0

        while not break_point:
            time.sleep(0.5)
            # get versions
            try:
                Version_button = driver.find_element_by_css_selector(
                    'section.title > mat-form-field div.mat-form-field-wrapper '
                    'div.mat-form-field-flex div.mat-form-field-infix mat-select '
                    'div.mat-select-trigger')
                version = Version_button.find_element_by_css_selector('div span span').text
                Version_button.click()
                Options = driver.find_elements_by_css_selector('div[role="listbox"] > mat-option')
                total_versions = str(len(Options))
            except:
                version = '1'
                total_versions = '1'
                Options = []
                break_point = True

            # Format
            try:
                Format = driver.find_element_by_css_selector('section.overview div p.tag:nth-child(4) span').text
            except:
                Format = None

            # downloads
            try:
                downloads = \
                    driver.find_element_by_css_selector('section.detail-content div.model-formats model-format-tabset '
                                                        'mat-tab-group div.mat-tab-body-wrapper._mat-animation-noopable'
                                                        ' mat-tab-body div model-format-tab div download-count-label '
                                                        'div span').text.split()[0]
            except:
                downloads = None

            # Name,Downloads, Tunable, model, size,Description

            # language
            try:
                language = driver.find_element_by_xpath('//div[contains(text(), "Language:")]/parent::div/a').text
            except:
                language = None

            # links
            a_links = driver.find_elements_by_css_selector('section.documentation markdown-snippet div a')
            links_associated = [x.get_attribute("href") for x in a_links]
            try:
                data_model = {
                    'Name': driver.find_element_by_css_selector('div.overview h2').text,
                    'Format': Format,
                    'Version': version,
                    'Downloads': downloads,
                    'Tunable': driver.find_element_by_css_selector('section.overview div p.tag:nth-child(1) span').text,
                    'model_link': driver.find_element_by_css_selector(
                        'download-button.ng-star-inserted a').get_attribute(
                        "href"),
                    'Size': driver.find_element_by_css_selector(
                        'download-button.ng-star-inserted a button span span').text,
                    'Description': driver.find_element_by_css_selector('section.overview div p.description').text,
                    'total_versions': total_versions,
                    'links_associated': links_associated,
                    'language': language, }
            except:
                time.sleep(0.25)
                print("\nError while retrieving data")
                break
            data = data.append(data_model, ignore_index=True)

            i += 1
            if Options:
                if i >= len(Options):
                    Options[i - 1].click()
                    break_point = True
                else:
                    Options[i].click()
            else:
                break_point = True

        form += 1
        if form >= len(Formats):
            break

    data.to_csv("model_data.csv")
driver.close()

print("End")
