from utils.extract import scrape_all_pages
from utils.transform import transform_data, transform_to_DataFrame
from utils.load import store_to_csv, store_to_gsheet

def main():
    # 1. Extract
    print("[INFO] Mulai proses Extract")
    product_data = scrape_all_pages()  
    
    if product_data:
        try:
            # 2. Transform
            print("[INFO] Mulai proses Transform")
            df = transform_to_DataFrame(product_data)  # Mengubah data menjadi DataFrame
            df = transform_data(df, 16000)  

            # 3. Load
            print("[INFO] Mulai proses Load")

            # Simpan ke CSV
            store_to_csv(df, "product_data.csv")  # Simpan data ke file CSV

            # Simpan ke Google Sheets
            sheet_name = "products"
            json_keyfile_name = "submission-fundamental-459814-dad262199609.json"  
            store_to_gsheet(df, sheet_name, json_keyfile_name)  # Simpan data ke Google Sheets

            print("[INFO] Proses selesai, data berhasil disimpan.")
            print(df.head())  # Menampilkan beberapa baris pertama dari DataFrame

        except Exception as e:
            print(f"[ERROR] Terjadi kesalahan dalam proses: {e}")
    else:
        print("[WARNING] Tidak ada data yang ditemukan.")

if __name__ == "__main__":
    main()