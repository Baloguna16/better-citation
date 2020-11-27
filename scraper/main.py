from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

def create_soup(link):
    sauce = requests.get(link)
    if sauce.status_code == 200:
        soup = BeautifulSoup(sauce.text, 'html.parser')
    #Source: Sandy Lin [1]
    elif sauce.status_code == 403:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(url=link, headers=headers)
        sauce = urlopen(req).read()
        soup = BeautifulSoup(sauce)
    return soup

#See README.md for citation [1]
