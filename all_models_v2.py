from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from tqdm import tqdm
import os
import pandas as pd
import numpy as np

# Setting up the driver
chrome = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(chrome)

# Creating the dataFrame which will contain the model's metadata
data = pd.DataFrame(columns=["Title", "Problem_domain", "Collection", "Publisher", "Updated_date", "Description",
                             "Architecture", "Dataset"])

# Reading the collections we already collected initialy with All_collections.py and adding a new column which will be
# used after to store the parent_collection's id
collections = pd.read_csv("Collection_retrieved.csv", index_col=[0], header=[0])
collections.assign(Collection_parent=np.nan)
dict_coll = {coll: int(c_id) for coll, c_id in zip(collections.loc[:, "Title"], collections.index)}

# We read the publisher's csv file obtained by executing publisher.py since it contains the proper url refering to each publisher.
publishers = pd.read_csv("Publishers.csv", index_col=[0], header=[0])
dict_pub = {pub: url for pub, url in zip(publishers.loc[:, "Name_Publisher"], publishers.loc[:, "url_publisher"])}

for i in tqdm(range(len(collections))):

    # creating the url refering to each collection
    url = dict_pub[collections.loc[i, "Publisher"]] + "/collections/" + collections.loc[i, "Title"] + "/1"

    # establishing a connection with the url and wait 0.5sec for the page to load properly
    driver.get(url=url)
    print("\nRetrieving: ", url)
    time.sleep(0.5)

    # Detect and click on expand button to display all models/collections associated to the main collection
    while True:
        try:
            expand_button = driver.find_element_by_css_selector("expand-button button")
            expand_button.click()
            break
        except NoSuchElementException:
            time.sleep(0.05)  # handling load error since every collection must have that button

    # extracting the number of models/collections logically calculated by the host tfhub for further checking
    nbr_model = driver.find_element_by_css_selector("div.contained-models.ng-star-inserted h2.title span")
    models, sub_collection = [], []  # init

    # Collecting html tags that contains models/collections and waiting for them to be all displayed
    while True:
        try:
            models = driver.find_elements_by_css_selector("div.contained-models.ng-star-inserted div model-card")
            sub_collection = driver.find_elements_by_css_selector("div.contained-models.ng-star-inserted div "
                                                                  "collection-card")
            assert len(models) + len(sub_collection) == int(nbr_model.text[1:-1])
            break
        except AssertionError:
            time.sleep(0.25)

    # Collecting models metadata about each model
    for model in models:
        mod_data = {"Title": model.find_element_by_css_selector('mat-card-title.mat-card-title').text,
                    "Collection": collections.loc[i, "Title"],
                    "Problem_domain": model.find_element_by_css_selector('div.product-eyebrow').text,
                    "Publisher": model.find_element_by_css_selector(
                        'p.product-descriptor__publisher > a.product-descriptor__publisher-name.ng-star-inserted').text,
                    "Updated_date": model.find_element_by_css_selector('span.product-descriptor__last-updated').text,
                    "Description": model.find_element_by_css_selector('mat-card-subtitle.mat-card-subtitle').text}
        # some models doesn't have tags that show the Architecture type or Dataset used
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

        # Filling the csv file
        data = data.append(mod_data, ignore_index=True)

    # save model's metadata we've collected so far from this collection
    data.to_csv("Models_Metadata.csv")

    # Adding the id of actual collection to sub_collection's collection_parent column
    for coll in sub_collection:
        coll_name = coll.find_element_by_css_selector('mat-card-title.mat-card-title').text
        collections.loc[dict_coll[coll_name], "Collection_parent"] = i

# save final collection.csv file
collections.to_csv("Collections.csv")
driver.close()
