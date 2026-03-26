import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


def pars_texno(category):
    texno_data = []
    load_dotenv()

    URL = os.getenv("URL")
    HOST = os.getenv("HOST")
    HEADERS = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/142.0.0.0 Safari/537.36'
    }

    html = requests.get(URL + category, headers=HEADERS).text
    soup = BeautifulSoup(html, 'html.parser')

    blocks = soup.find_all('div', class_='col-3')

    for block in blocks:
        images_link = block.find('a', class_='product-link')
        images = images_link.find('img').get('data-src')
        title = block.find('h2').get_text()
        credit_price = block.find('div', class_='installment-price').get_text(strip=True)
        price = block.find('div', class_='product-price__current').get_text(strip=True)

        texno_data.append({
            'images': images,
            'title': title,
            'credit_price': credit_price,
            'price': price,
        })
    return texno_data


pars_texno("katalog/smartfony-apple/")
