import urllib3
import json
from bs4 import BeautifulSoup

# url = ('https://www.google.com/searchbyimage?image_url=https://filedn.com/ltOdFv1aqz1YIFhf4gTY8D7/ingus-info/BLOGS/Photography-stocks3/stock-photography-slider.jpg&encoded_image=&image_content=&filename=&hl=en-IN')
http = urllib3.PoolManager()
r = http.request('GET', 'https://www.google.com/searchbyimage?image_url=https://filedn.com/ltOdFv1aqz1YIFhf4gTY8D7/ingus-info/BLOGS/Photography-stocks3/stock-photography-slider.jpg&encoded_image=&image_content=&filename=&hl=en-IN')
# request = urllib3.Request(url, None, {})
# response = urllib3.urlopen(request)
# print(r.headers)
# print(r.status)

import pycurl
from flask import Flask, url_for, jsonify, request
from flask_cors import CORS, cross_origin
python3 = False
try:
    from StringIO import StringIO
except ImportError:
    python3 = True
    import io as bytesIOModule
from bs4 import BeautifulSoup
if python3:
    import certifi
import requests

url = 'https://www.google.com/searchbyimage?image_url=https://filedn.com/ltOdFv1aqz1YIFhf4gTY8D7/ingus-info/BLOGS/Photography-stocks3/stock-photography-slider.jpg&encoded_image=&image_content=&filename=&hl=en-IN'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','referer': 'https://www.google.com/','origin': 'https://www.google.com/'}

response = requests.get(url, headers=headers)
# print(response.text)
# print(response.headers)

def doImageSearch(full_url):
    # Directly passing full_url
    """Return the HTML page response."""

    if python3:
        returned_code = bytesIOModule.BytesIO()
    else:
        returned_code = StringIO()
    # full_url = SEARCH_URL + image_url

    # if app.debug:
    print('POST: ' + full_url)

    conn = pycurl.Curl()
    if python3:
        conn.setopt(conn.CAINFO, certifi.where())
    conn.setopt(conn.URL, str(full_url))
    conn.setopt(conn.FOLLOWLOCATION, 1)
    conn.setopt(conn.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0')
    conn.setopt(conn.WRITEFUNCTION, returned_code.write)
    conn.perform()
    conn.close()
    if python3:
        return returned_code.getvalue().decode('UTF-8')
    else:
        return returned_code.getvalue()

def parseResults(code, resized=False):
    print(code)
    """Parse/Scrape the HTML code for the info we want."""

    soup = BeautifulSoup(code, 'html.parser')

    results = {
        'links': [],
        'descriptions': [],
        'titles': [],
        'similar_images': [],
        'best_guess': ''
    }

    for div in soup.findAll('div', attrs={'class':'rc'}):
        sLink = div.find('a')
        results['links'].append(sLink['href'])

    for desc in soup.findAll('span', attrs={'class':'st'}):
        results['descriptions'].append(desc.get_text())

    for title in soup.findAll('h3', attrs={'class':'r'}):
        results['titles'].append(title.get_text())

    for similar_image in soup.findAll('div', attrs={'rg_meta'}):
        tmp = json.loads(similar_image.get_text())
        img_url = tmp['ou']
        results['similar_images'].append(img_url)

    for best_guess in soup.findAll('a', attrs={'class':'fKDtNb'}):
      results['best_guess'] = best_guess.get_text()

    if resized:
        results['resized_images'] = getDifferentSizes(soup)

    print("Successful search")

    return json.dumps(results)

code = doImageSearch('https://www.google.com/searchbyimage?image_url=https://filedn.com/ltOdFv1aqz1YIFhf4gTY8D7/ingus-info/BLOGS/Photography-stocks3/stock-photography-slider.jpg&encoded_image=&image_content=&filename=&hl=en-IN')
# print(parseResults(code))
f = open("response.html", "a",encoding='utf-8')
f.write(code)
f.close()