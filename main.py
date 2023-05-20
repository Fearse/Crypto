# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pprint

from requests import Session,Request
import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = 'https://coinmania.com/news/'
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(request_site).read()
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find_all('article')
    results = []
    for item in news:
        title = item.find('h2').get_text()
        print('title:', title)
        href = item.a.get("href")
        print('href:', href)
        desc = item.find('p').get_text()
        print('description:', desc)
        image = item.find('div', class_='col d-flex justify-content-md-end order-1 order-md-2').find('img')
        if (image != None):
            image = image.get('src')
        print('image', image)
        time = item.find('div', class_='entry-meta-item entry-meta__time').find('time').get_text()
        print('time',time)
        results.append({'title': title, 'href': href, 'description': desc, 'picture': image})

