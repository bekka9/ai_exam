# scraping.py
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def simple_scrape(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = [h1.text for h1 in soup.find_all('h1')]
    return titles

def js_scrape(url: str):
    """Для JavaScript-сайтов"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        # Дополнительная обработка...
        browser.close()
    return content