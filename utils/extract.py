import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

MAX_PAGE = 50

def fetching_content(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log specific HTTP errors
    except Exception as err:
        print(f"Error fetching content: {err}")
    return None

def extract_product_data(item):
    title = item.find('h3', class_='product-title')

    # Tangani dua kemungkinan struktur HTML
    price_tag = item.find('span', class_='price')  # untuk harga yang tersedia
    if not price_tag:
        price_tag = item.find('p', class_='price')  # untuk "Price Unavailable"

    details = item.find_all('p', style=lambda value: value and 'font-size' in value)

    rating = colors = size = gender = price = None

    for detail in details:
        text = detail.text.strip()
        if "Rating" in text:
            rating = text.replace("Rating: ", "").split("/")[0].strip()
        elif "Colors" in text:
            colors = text.replace("Colors: ", "").strip()
        elif "Size" in text:
            size = text.replace("Size: ", "").strip()
        elif "Gender" in text:
            gender = text.replace("Gender: ", "").strip()

    if price_tag:
        price_text = price_tag.text.strip()
        if "Price Unavailable" not in price_text:
            try:
                price = float(price_text.replace("$", "").replace(",", ""))  # Menangani format harga dengan koma
            except ValueError:
                price = None

    # Add timestamp to each product
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        "Title": title.text.strip() if title else None,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
        "Timestamp": timestamp  # Add the timestamp here
    }

def scrape_all_pages():
    all_data = []

    # Halaman pertama
    base_url_first = 'https://fashion-studio.dicoding.dev/'
    print(f"[INFO] Mengakses: {base_url_first}")
    content = fetching_content(base_url_first)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.find_all('div', class_='collection-card')
        if not items:
            print("[WARNING] Tidak ditemukan produk di halaman pertama.")
        for item in items:
            data = extract_product_data(item)
            if data["Title"]:  # Validasi
                all_data.append(data)
        time.sleep(1)

    # Halaman 2 sampai MAX_PAGE
    for page in range(2, MAX_PAGE + 1):
        url = f'https://fashion-studio.dicoding.dev/page{page}'
        print(f"[INFO] Mengakses: {url}")
        content = fetching_content(url)
        if not content:
            continue
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.find_all('div', class_='collection-card')
        if not items:
            print(f"[WARNING] Tidak ditemukan produk di halaman {page}.")
        for item in items:
            data = extract_product_data(item)
            if data["Title"]:
                all_data.append(data)
        time.sleep(1)

    return all_data
