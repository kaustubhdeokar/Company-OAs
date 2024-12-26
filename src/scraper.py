import requests as _requests
import bs4 as _bs4
from typing import List
import os
import configparser

from models.request_dtos import PageRange
from storage.local import LocalStorageStrategy
from storage.db import DBStorageStrategy
from models.counter import ScrapeCounter

from tenacity import retry, wait_fixed, stop_after_attempt
from fastapi import FastAPI, Depends
from auth import get_current_user
import redis 

app = FastAPI()
config = configparser.ConfigParser()
config.read('config.properties')
storage_type = config.get('DEFAULT', 'storage_type')


def generate_url_for_page(page_no: str):
    return f'https://dentalstall.com/shop/page/{page_no}/'

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def get_page(url: str) -> _bs4.BeautifulSoup:

    cached_page = redis_client.get(url)
    if cached_page:
        print('Cache hit!!!')
        soup = _bs4.BeautifulSoup(cached_page, "html.parser")
        return soup

    payload = { 'api_key': 'bd5d5bbb6d360a4f10573f11c709c076', 'url': url }
    response = _requests.get('https://api.scraperapi.com/', params=payload)
    #response = _requests.get(url)
    if response.status_code == 200:
        soup = _bs4.BeautifulSoup(response.content, "html.parser")
        redis_client.setex(url, 3600, response.content)
        return soup
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        return None

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def download_image(image_url: str, image_name: str, folder: str):
    payload = { 'api_key': 'bd5d5bbb6d360a4f10573f11c709c076', 'url': image_url }
    response = _requests.get('https://api.scraperapi.com/', params=payload)
    
    if response.status_code == 200:
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(os.getcwd(), folder, image_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Image saved to: {file_path}')
    else:
        print(f'Failed to download image. Status code: {response.status_code}')



def events_on_page(page_no: str) -> List[str]:
    url = generate_url_for_page(page_no)
    page = get_page(url)
    events = []

    if page:
        
        products = page.find_all('div', class_='mf-product-thumbnail')
        
        for product in products:
            
            name = product.find_next('div', class_='mf-product-content').find('h2').find('a').text
            price = product.find_next('div', class_='mf-product-price-box').find('span', class_='price').find('span', class_='woocommerce-Price-amount amount').find('bdi').text
            image_url = product.find('img')['data-lazy-src']
            image_name = os.path.basename(image_url)
            folder = os.path.join('res', page_no)
            
            events.append({
                'name': name,
                'price': price,
                'image_url': image_url
            })
            
            #print(f'Title: {name}, \nPrice: {price}, \nImage Path: {image_url}\n\n')

            if storage_type == 'local':
                download_image(image_url, image_name, folder)
        
        ScrapeCounter.increment(len(products))
    
    return events
    
@app.get("/events/page/{page_no}")
def get_events(page_no: str, user: dict = Depends(get_current_user)):
    events = events_on_page(page_no)
    
    if storage_type == 'local':
        storage_strategy = LocalStorageStrategy()
    else:
        storage_strategy = DBStorageStrategy()
    storage_strategy.save(events)
    return {"events": events}


@app.get("/events/range")
def get_events(page_range: PageRange, user: dict = Depends(get_current_user)):
    events = fetch_events_for_range(page_range)
    return {"events": events}


def fetch_events_for_range(page_range):
    all_events = []
    for page_no in range(page_range.from_page, page_range.to_page+1):
        events = events_on_page(str(page_no))
        all_events.append(events)
    return events


@app.post("/events/range/save")
def save_events(page_range: PageRange, user: dict = Depends(get_current_user)):
#def save_events(page_range: PageRange):
    all_events = fetch_events_for_range(page_range)
    if storage_type == 'local':
        storage_strategy = LocalStorageStrategy()
    else:
        storage_strategy = DBStorageStrategy()
    storage_strategy.save(all_events)
    return {"message": "Events saved successfully"}


@app.get("/scrape_count")
def get_scrape_count(user: dict = Depends(get_current_user)):
    return {"scrape_count": ScrapeCounter.get_count()}