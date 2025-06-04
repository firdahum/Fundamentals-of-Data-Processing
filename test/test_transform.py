import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from transform import transform_data, transform_to_DataFrame
import unittest
import pandas as pd

class TestTransformFunctions(unittest.TestCase):

    def setUp(self):
        self.valid_data = [
            {'Title': 'Product 1', 'Price': '400', 'Rating': '⭐4.5', 'Colors': '8 Colors', 'Size': 'XXL', 'Gender': 'Men'},
            {'Title': 'Product 2', 'Price': '800', 'Rating': '⭐3.0', 'Colors': '5', 'Size': 'S', 'Gender': 'Women'},
            {'Title': 'Product 3', 'Price': None, 'Rating': 'Not Rated', 'Colors': '2 Colors', 'Size': 'L', 'Gender': 'Unisex'}
        ]

    def test_transform_to_DataFrame_valid(self):
        df = transform_to_DataFrame(self.valid_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)

    def test_transform_to_DataFrame_invalid_input(self):
        invalid_data = "this is not a list of dicts"
        df = transform_to_DataFrame(invalid_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_transform_data_valid(self):
        data = pd.DataFrame(self.valid_data)
        exchange_rate = 16000
        transformed = transform_data(data, exchange_rate)

        self.assertEqual(len(transformed), 2)
        self.assertEqual(transformed.iloc[0]['Price'], 400 * exchange_rate)
        self.assertEqual(transformed.iloc[1]['Price'], 800 * exchange_rate)
        self.assertTrue(isinstance(transformed.iloc[0]['Price'], float))

    def test_transform_data_invalid_rating_and_unknown_product(self):
        data = pd.DataFrame([
            {'Title': 'Unknown Product', 'Price': '300', 'Rating': '⭐4.0', 'Colors': 'Colors3', 'Size': 'M', 'Gender': 'Men'},
            {'Title': 'Product A', 'Price': '500', 'Rating': 'Invalid Rating', 'Colors': 'Colors2', 'Size': 'M', 'Gender': 'Women'}
        ])
        transformed = transform_data(data, 1)
        self.assertTrue(transformed.empty)

    def test_transform_data_unconvertible_colors(self):
        data = pd.DataFrame([
            {'Title': 'Product B', 'Price': '120', 'Rating': '⭐4.2', 'Colors': 'ColorsXYZ', 'Size': 'S', 'Gender': 'Men'}
        ])
        result = transform_data(data, 1)
        self.assertTrue(pd.isna(result.iloc[0]['Colors']))

    def test_transform_data_duplicates(self):
        data = pd.DataFrame([
            {'Title': 'Product C', 'Price': '200', 'Rating': '⭐2.0', 'Colors': 'Colors1', 'Size': 'M', 'Gender': 'Unisex'},
            {'Title': 'Product C', 'Price': '200', 'Rating': '⭐2.0', 'Colors': 'Colors1', 'Size': 'M', 'Gender': 'Unisex'}
        ])
        result = transform_data(data, 1)
        self.assertEqual(len(result), 1)

    def test_transform_data_all_nan(self):
        data = pd.DataFrame([
            {'Title': 'Product E', 'Price': None, 'Rating': None, 'Colors': None, 'Size': 'M', 'Gender': 'Women'}
        ])
        result = transform_data(data, 1)
        self.assertTrue(result.empty)

if __name__ == "__main__":
    unittest.main()
