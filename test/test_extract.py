import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os

import sys
import os

# Tambahkan folder root proyek ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Sekarang Anda bisa mengimpor module dari utils
from utils.extract import fetching_content, extract_product_data, scrape_all_pages

class TestExtractFunctions(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_fetching_content_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Mocked Page</body></html>"
        mock_get.return_value = mock_response

        result = fetching_content("https://example.com")
        self.assertEqual(result, "<html><body>Mocked Page</body></html>")

    @patch('utils.extract.requests.get')
    def test_fetching_content_failure(self, mock_get):
        mock_get.side_effect = Exception("Request failed")
        result = fetching_content("https://example.com")
        self.assertIsNone(result)

    def test_extract_product_data_all_valid(self):
        html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">T-shirt 716</h3>
                <div class="price-container">
                    <span class="price">$100.00</span>
                </div>
                <p style="font-size: 14px;">Rating: ⭐ 4.2</p>
                <p style="font-size: 14px;">Colors: 10 Colors</p>
                <p style="font-size: 14px;">Size: S</p>
                <p style="font-size: 14px;">Gender: Women</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        item = soup.find("div", class_="collection-card")
        result = extract_product_data(item)
        result.pop("Timestamp")

        expected = {
            "Title": "T-shirt 716",
            "Price": 100.00,
            "Rating": "⭐ 4.2",
            "Colors": "10 Colors",
            "Size": "S",
            "Gender": "Women"
        }
        self.assertEqual(result, expected)

    def test_extract_product_data_invalid_rating(self):
        html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Unknown Product</h3>
                <div class="price-container">
                    <span class="price">$80.00</span>
                </div>
                <p style="font-size: 14px;">Rating: ⭐ Invalid Rating</p>
                <p style="font-size: 14px;">Colors: 8 Colors</p>
                <p style="font-size: 14px;">Size: S</p>
                <p style="font-size: 14px;">Gender: Men</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        item = soup.find("div", class_="collection-card")
        result = extract_product_data(item)
        result.pop("Timestamp")

        expected = {
            "Title": "Unknown Product",
            "Price": 80.00,
            "Rating": "⭐ Invalid Rating",
            "Colors": "8 Colors",
            "Size": "S",
            "Gender": "Men"
        }
        self.assertEqual(result, expected)

    def test_extract_product_data_not_rated(self):
        html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Crewneck 715</h3>
                <p class="price">Price Unavailable</p>
                <p style="font-size: 14px;">Rating: Not Rated</p>
                <p style="font-size: 14px;">Colors: 5 Colors</p>
                <p style="font-size: 14px;">Size: M</p>
                <p style="font-size: 14px;">Gender: Women</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        item = soup.find("div", class_="collection-card")
        result = extract_product_data(item)
        result.pop("Timestamp")

        expected = {
            "Title": "Crewneck 715",
            "Price": None,
            "Rating": "Not Rated",
            "Colors": "5 Colors",
            "Size": "M",
            "Gender": "Women"
        }
        self.assertEqual(result, expected)

    @patch('utils.extract.fetching_content')
    def test_scrape_all_pages_empty(self, mock_fetch):
        mock_fetch.return_value = "<html><body>No products</body></html>"
        result = scrape_all_pages()
        self.assertEqual(result, [])

    @patch('utils.extract.time.sleep', return_value=None)
    @patch('utils.extract.fetching_content')
    def test_scrape_all_pages_mocked(self, mock_fetch, mock_sleep):
        page_1_html = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Hoodie</h3>
                    <span class="price">$80.00</span>
                    <p style="font-size: 14px;">Rating: 4.0</p>
                    <p style="font-size: 14px;">Colors: Black</p>
                    <p style="font-size: 14px;">Size: L</p>
                    <p style="font-size: 14px;">Gender: Men</p>
                </div>
            </body>
        </html>
        """
        empty_html = "<html><body>No products</body></html>"
        mock_fetch.side_effect = [page_1_html] + [empty_html] * 49

        results = scrape_all_pages()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['Title'], 'Hoodie')
        self.assertEqual(results[0]['Price'], 80.00)
        self.assertEqual(results[0]['Size'], 'L')