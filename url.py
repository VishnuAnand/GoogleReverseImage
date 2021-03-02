import json

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

# soup=BeautifulSoup("/search?hl=en-IN&amp;tbs=simg:CAQSiQIJIzJtcCAQEcQa_1QELELCMpwgaOQo3CAQSE5M9AJktkS2qE8wMhwaZLLoY_1hwaGjGjNvet3EM5-Evrnx2Z_1O56xfj6SSUrwlbZIAUwBAwLEI6u_1ggaCgoICAESBOvlKNsMCxCd7cEJGp4BCh4KC25vcm1hbCBsZW5z2qWI9gMLCgkvbS8wMTd4dHIKIgoOdGVsZWNvbXByZXNzb3LapYj2AwwKCi9tLzAzcWYxNHYKGAoFY2Fub27apYj2AwsKCS9tLzAxYnZ4MQobCghraXQgbGVuc9qliPYDCwoJL20vMDdkY3JxCiEKDnRlbGVwaG90byBsZW5z2qWI9gMLCgkvbS8wMWJ0NHcM&amp;q=best+photographer&amp;tbm=isch&amp;sa=X&amp;ved=2ahUKEwi3vc2Qv5HvAhXLUt4KHXqiB8sQ2A4oAXoECBAQMQ","html.parser")
# print(soup.prettify(formatter=None))


# url = 'https://www.google.com/searchbyimage?image_url=https://filedn.com/ltOdFv1aqz1YIFhf4gTY8D7/ingus-info/BLOGS/Photography-stocks3/stock-photography-slider.jpg&encoded_image=&image_content=&filename=&hl=en-IN'
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','referer': 'https://www.google.com/','origin': 'https://www.google.com/'}

# response = requests.get(url, headers=headers)
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

from urllib.parse import quote_plus
imgUrl="https://filedn.com/ltOdFv1aqz1YIFhf4gTY8D7/ingus-info/BLOGS/Photography-stocks3/stock-photography-slider.jpg"
# imgUrl="https://media-exp1.licdn.com/dms/image/C4D0BAQFCrCc_Mtq6YQ/company-logo_200_200/0/1519952271098?e=2159024400&v=beta&t=bZtDouIbGugYnfpi4McBbjvm0ysQ0wQQjn6YTwKDoxU"
# parsedUrl= BeautifulSoup(imgUrl, 'html.parser')

# Parsing the URL as encoded, otherwise main URL will be affected
parsedUrl=quote_plus(imgUrl)
print(parsedUrl)

code = doImageSearch('https://www.google.com/searchbyimage?image_url='+parsedUrl+'&encoded_image=&image_content=&filename=&hl=en-IN')
# print(parseResults(code))
# f = open("response.html", "a",encoding='utf-8')
# f.write(code)
# f.close()

# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

matchObj = re.search(r'(?:Find other sizes of this image:)(?:.+\s+)(?:href=\")(.+)(?:\">All\s+sizes)', code, re.M)
#print(matchObj)
if matchObj:
    # print ("matchObj.group() : ", str(BeautifulSoup(matchObj.group(), 'html.parser')))
    print ("matchObj.group(1) : ", "https://www.google.com"+BeautifulSoup(matchObj.group(1), 'html.parser').prettify(formatter=None))
    import webbrowser
    webbrowser.open("https://www.google.com"+BeautifulSoup(matchObj.group(1), 'html.parser').prettify(formatter=None), new=2)
else:
    print("None")
# for matchNum, match in enumerate(matches, start=1):
    
#     print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
#     for groupNum in range(0, len(match.groups())):
#         groupNum = groupNum + 1
        
#         print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.

