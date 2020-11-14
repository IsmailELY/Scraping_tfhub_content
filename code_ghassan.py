'''
- Install selenium
- download Chrome WebDriver from https://sites.google.com/a/chromium.org/chromedriver/home if you are using chrome and put it in the some locatin of your program
geckodriver if you are using firefox
  '''

# importation
import csv
from bs4 import BeautifulSoup as bs
import requests
import selenium as se

from selenium import webdriver

options = se.webdriver.ChromeOptions()
options.add_argument('headless')

driver = se.webdriver.Chrome(options=options)

driver.get("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

from selenium.webdriver.support.ui import WebDriverWait

driver.maximize_window()

wait = WebDriverWait(driver, 10)
soup = bs(driver.page_source, "html.parser")
app = soup.body.find('app-root')
mat = app.find('mat-sidenav-container')
content = mat.find('mat-sidenav-content')

model = content.find('model-format-tab')

section = model.find('section')

#Format of the model
formate = section.h2
#number of downloads
download = section.find('download-count-label').span

#Language
languages =  model.find_all('p',{'class':'description ng-star-inserted'})

#Documentation of the model
documentation = model.find('markdown-snippet')

#Details of the model
uls = documentation.find_all('ul')
details = uls[0]

#Learn more
learn_more = documentation.p

#Intend_use
intend_use = uls[1].li

#Factors
factors = uls[2]

#Universal sentence encoder
ps = documentation.find_all('p')
univ = ps[1]
univ_link = documentation.find_next('a').find_next('a').find_next('a')

#Metrics
Metrics = uls[4]

#Prerequisites
Prerequisites = ps[3]
print(Prerequisites)

#Example_use
example_use = soup.find_all('code',{'class':'language-python'})

#versions
version_1 = uls[5]
version_2 = uls[6]
version_3 = uls[7]

#References
ref_1 = ps[6]
ref_2 = ps[7]


def convert(L):
    for i in range(0, len(L)):
        L[i] = str(L[i].encode('utf-8'))
    return L


def listToString(s):
    # initialize an empty string
    str1 = "\n"

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


import csv

with open('tfHub.csv', 'w') as output:
    writer = csv.writer(output, lineterminator='\n', delimiter='|')
    writer.writerow(['Format', 'Downloads', 'languages', 'Details', 'Learn more', 'Intend_use', 'Factors',
                     'Universal sentence encoder', 'Metrics', 'Prerequisites', 'Example_use', 'version_1', 'version_2',
                     'version_3', 'ref_1', 'ref_2', ])

    form = details.text.encode('utf-8').decode('ascii', 'ignore')
    down = download.text.encode('utf-8').decode('ascii', 'ignore')
    lang = languages.text.encode('utf-8').decode('ascii', 'ignore')

    det = details.text.encode('utf-8').decode('ascii', 'ignore')
    lm = learn_more.text.encode('utf-8').decode('ascii', 'ignore')
    iu = intend_use.text.encode('utf-8').decode('ascii', 'ignore')
    fac = factors.text.encode('utf-8').decode('ascii', 'ignore')
    ul = univ_link.text.encode('utf-8').decode('ascii', 'ignore')
    met = Metrics.text.encode('utf-8').decode('ascii', 'ignore')
    preq = Prerequisites.text.encode('utf-8')
    eu = listToString(convert(example_use))
    v1 = version_1.text.encode('utf-8').decode('ascii', 'ignore')
    v2 = version_2.text.encode('utf-8').decode('ascii', 'ignore')
    v3 = version_3.text.encode('utf-8').decode('ascii', 'ignore')
    rf1 = ref_1.text.encode('utf-8').decode('ascii', 'ignore')
    rf2 = ref_2.text.encode('utf-8').decode('ascii', 'ignore')

    writer.writerow([form, down, lang, det, lm, iu, fac, ul, met, preq, eu, v1, v2, v3, rf1, rf2])