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

code = doImageSearch('https://www.google.com/search?hl=en-IN&tbs=simg:CAQSiQIJIzJtcCAQEcQa_1QELELCMpwgaOQo3CAQSE5M9AJktkS2qE8wMhwaZLLoY_1hwaGjGjNvet3EM5-Evrnx2Z_1O56xfj6SSUrwlbZIAUwBAwLEI6u_1ggaCgoICAESBOvlKNsMCxCd7cEJGp4BCh4KC25vcm1hbCBsZW5z2qWI9gMLCgkvbS8wMTd4dHIKIgoOdGVsZWNvbXByZXNzb3LapYj2AwwKCi9tLzAzcWYxNHYKGAoFY2Fub27apYj2AwsKCS9tLzAxYnZ4MQobCghraXQgbGVuc9qliPYDCwoJL20vMDdkY3JxCiEKDnRlbGVwaG90byBsZW5z2qWI9gMLCgkvbS8wMWJ0NHcM&q=best+photographer&tbm=isch&sa=X&ved=2ahUKEwic3ovM_ZHvAhW3_XMBHQ5AASoQ2A4oAXoECBAQMQ')
f = open("images.html", "a",encoding='utf-8')
f.write(code)
f.close()