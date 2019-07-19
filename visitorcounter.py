import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# get perpus page 1
url = 'http://www.stmik-abg.net/perpustakaan/Info_DataPengunjung.asp?P=1'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
cells = soup.find_all("td", width=True)
for aCell in cells:
    width=aCell["width"]
    if(width == '14%'):
        print(aCell)
        print(width)