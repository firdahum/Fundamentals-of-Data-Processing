import pandas as pd

def transform_to_DataFrame(data):
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"[ERROR] Mengubah ke DataFrame: {e}")
        return pd.DataFrame()

def transform_data(data, exchange_rate):
    try:
        data = data.dropna(subset=['Price']).copy()
        data.loc[:, 'Price'] = data['Price'].astype(float) * exchange_rate
        data.loc[:, 'Rating'] = data['Rating'].astype(str).str.replace("⭐", "").str.strip()
        data.loc[:, 'Colors'] = data['Colors'].astype(str).str.replace("Colors", "").str.strip()
        data = data.dropna().copy()
        data = data[
            (data['Title'] != 'Unknown Product') & 
            (data['Rating'] != 'Not Rated') & 
            (data['Rating'] != 'Invalid Rating')
        ].copy()
        data = data.drop_duplicates().copy()
        data.loc[:, 'Rating'] = pd.to_numeric(data['Rating'], errors='coerce')
        data.loc[:, 'Colors'] = pd.to_numeric(data['Colors'], errors='coerce')
        return data
    except Exception as e:
        print(f"[ERROR] Transformasi data: {e}")
        return pd.DataFrame()
