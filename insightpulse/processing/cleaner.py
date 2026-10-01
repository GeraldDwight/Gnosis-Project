import sqlite3
import pandas as pd
from scraper.collector import scrape_data

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            author TEXT
        )
    ''')
    conn.commit()
    conn.close()

def clean_and_store_data(custom_url=None):
    print("Memulai proses pengambilan dan pembersihan data...")
    
    # Jalankan scraper dengan URL kustom jika ada
    if custom_url:
        raw_data = scrape_data(custom_url)
    else:
        raw_data = scrape_data()
    
    if not raw_data:
        print("Tidak ada data yang berhasil ditarik.")
        return 0

    df = pd.DataFrame(raw_data)
    
    # Proses Data Cleaning
    df = df.drop_duplicates(subset=['text'])
    df = df.dropna()
    df['text'] = df['text'].str.strip()
    df['author'] = df['author'].str.strip()
    
    init_db()
    conn = sqlite3.connect('database.db')
    df.to_sql('quotes', conn, if_exists='append', index=False)
    conn.close()
    
    print(f"Sukses! {len(df)} data bersih berhasil disimpan ke database.")
    return len(df)