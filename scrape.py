from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import re
import json
from pathlib import Path

# Configs
driver = webdriver.Chrome()
link = 'https://agssmc.org/newsletter/';
FILE_PATH = './AGS_PRINT_LIST.json'


# Open ags website
driver.get(link);

# Locate all prints
prints = driver.find_elements('xpath', '//figure')

prints_list = []

for p in range(len(prints)):
    # print element
    print_element = prints[p]

    # scrape caption under the image
    captions = print_element.find_element(By.TAG_NAME, 'h2').text.split('\n')

    # scrape image element
    image = print_element.find_element(By.CLASS_NAME, 'front').value_of_css_property('background-image')
    # use RE to find the imageUrl
    image_url = re.search('(?P<url>https?://[^\s;]+)', image)

    if (image_url):
      image_url = image_url.group('url').rstrip('"),')

    # information concerning the items
    date = captions[0]
    issue_number = captions[1] if len(captions) == 3 else None
    editor = captions[2] if len(captions) == 3 else captions[1]

    # tuple form of print data
    print_data = { date, issue_number, editor, image_url }

    prints_list.append(print_data)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
  
with open(FILE_PATH, 'w') as output_file:
	json.dump(prints_list, output_file, indent=2, default=set_default)