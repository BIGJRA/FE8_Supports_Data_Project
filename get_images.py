# CREDIT: Base code written by Jonathan on
# https://stackoverflow.com/questions/18408307/how-to-extract-and-download-all-images-from-a-website-using-beautifulsoup

import re
import requests
from bs4 import BeautifulSoup
import os

try:
    os.mkdir("img")
except:
    pass

site = 'https://serenesforest.net/the-sacred-stones/characters/introduction/'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

urls = ["https://serenesforest.net" + img['src'] for img in img_tags]

print (f"{len(urls)} urls found. Processing...")
#print (urls)

skip = 0
for url in urls:
    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
    if not filename:
         print("Regex didn't match with the url: {}".format(url))
         skip += 1
         continue
    path = os.path.join("img", filename.group(1))
    with open(path, 'wb') as f:
        '''if 'http' not in url:
            # sometimes an image source can be relative
            # if it is provide the base url which also happens
            # to be the site variable atm.
            url = '{}{}'.format(site, url)'''
        response = requests.get(url)
        f.write(response.content)
        print (f"Processed {(filename.group(0))}.")

print (f"Of {len(urls)} urls found, {len(urls) - skip} processed and {skip} skipped.")