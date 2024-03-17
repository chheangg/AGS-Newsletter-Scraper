from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import json
import pandas as pd
from datetime import datetime

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

    # scrapping images
    image = print_element.find_element(By.CLASS_NAME, 'front').value_of_css_property('background-image')
    image_url = re.search('(?P<url>https?://[^\s;]+)', image)
    if (image_url):
      image_url = image_url.group('url').rstrip('"),')

    # scrape editor under the image
    captions = print_element.find_element(By.TAG_NAME, 'h2').text.split('\n')
    editor = captions[2] if len(captions) == 3 else captions[1]

    # scrape hidden data upon clicking "detailed"
    detailed = print_element.find_element(By.CLASS_NAME, 'details')
    detailed_list = detailed.find_elements(By.TAG_NAME, 'li')

    date = detailed_list[0].get_attribute('innerHTML')
    formatted_date = pd.to_datetime(date)
    issue = detailed_list[1].get_attribute('innerHTML')
    detailed_date = detailed_list[2].get_attribute('innerHTML')
    page_number = detailed_list[3].get_attribute('innerHTML')

    # scrape print url
    print_url = print_element.find_element(By.CLASS_NAME, 'buttons').find_element(By.TAG_NAME, 'a').get_attribute('href')

    # tuple form of print data
    print_data = { 
      'detailed_date': detailed_date, 
      'formatted_date_for_sorting': formatted_date,
      'date': date, 
      'issue': issue, 
      'editor': editor, 
      'image_url': image_url, 
      'page_number': page_number,
      'print_url': print_url
    }

    prints_list.append(print_data)

prints_list.sort(key = lambda p: p['formatted_date_for_sorting'])

for print_data in prints_list:
     del print_data['formatted_date_for_sorting']
  
with open(FILE_PATH, 'w') as output_file:
	json.dump(prints_list, output_file, indent=2)